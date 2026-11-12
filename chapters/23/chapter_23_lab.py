import sqlite3
import unittest


class Rejected(Exception):
    pass


class RefundService:
    def __init__(self):
        self.db = sqlite3.connect(":memory:", isolation_level=None)
        self.db.executescript("""
            CREATE TABLE orders (
                owner TEXT NOT NULL, order_id TEXT NOT NULL,
                remaining INTEGER NOT NULL,
                PRIMARY KEY (owner, order_id)
            );
            CREATE TABLE approvals (
                approval_id TEXT PRIMARY KEY, owner TEXT NOT NULL,
                order_id TEXT NOT NULL, amount INTEGER NOT NULL,
                idem_key TEXT NOT NULL, expires INTEGER NOT NULL,
                used INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE refunds (
                owner TEXT NOT NULL, idem_key TEXT NOT NULL,
                order_id TEXT NOT NULL, amount INTEGER NOT NULL,
                approval_id TEXT NOT NULL,
                PRIMARY KEY (owner, idem_key)
            );
            CREATE TABLE audit (
                owner TEXT NOT NULL, idem_key TEXT NOT NULL,
                event TEXT NOT NULL
            );
        """)

    def seed(self):
        self.db.execute("INSERT INTO orders VALUES (?, ?, ?)",
                        ("alice", "order-1", 5000))
        self.db.execute(
            "INSERT INTO approvals VALUES (?, ?, ?, ?, ?, ?, 0)",
            ("A1", "alice", "order-1", 1500, "K1", 200),
        )

    def refund(self, principal, proposal, now, fault=None):
        # In production, principal and now come from trusted services.
        required = {"order", "amount", "approval", "key"}
        if not isinstance(proposal, dict) or set(proposal) != required:
            raise Rejected("invalid proposal shape")
        if not isinstance(principal, str) or not principal:
            raise Rejected("invalid principal")
        for field in ("order", "approval", "key"):
            value = proposal[field]
            if not isinstance(value, str) or not value or len(value) > 64:
                raise Rejected("invalid identifier")
        amount = proposal["amount"]
        if type(amount) is not int or amount <= 0:
            raise Rejected("invalid amount")
        if type(now) is not int:
            raise Rejected("invalid time")
        if fault not in (None, "before_commit", "after_commit"):
            raise ValueError("unknown fault")

        order = proposal["order"]
        approval = proposal["approval"]
        key = proposal["key"]
        db = self.db
        db.execute("BEGIN IMMEDIATE")
        try:
            old = db.execute(
                "SELECT order_id, amount, approval_id FROM refunds "
                "WHERE owner=? AND idem_key=?", (principal, key)
            ).fetchone()
            if old is not None:
                if old != (order, amount, approval):
                    raise Rejected("idempotency key conflict")
                db.execute("COMMIT")
                return "ledger_committed"

            row = db.execute(
                "SELECT owner, order_id, amount, idem_key, expires, used "
                "FROM approvals WHERE approval_id=?", (approval,)
            ).fetchone()
            if (row is None or row[:4] != (principal, order, amount, key)
                    or now >= row[-2] or row[-1] != 0):
                raise Rejected("approval unavailable")

            changed = db.execute(
                "UPDATE orders SET remaining=remaining-? "
                "WHERE owner=? AND order_id=? AND remaining>=?",
                (amount, principal, order, amount),
            ).rowcount
            if changed != 1:
                raise Rejected("order or balance unavailable")

            db.execute("UPDATE approvals SET used=1 WHERE approval_id=?",
                       (approval,))
            db.execute("INSERT INTO refunds VALUES (?, ?, ?, ?, ?)",
                       (principal, key, order, amount, approval))
            db.execute("INSERT INTO audit VALUES (?, ?, ?)",
                       (principal, key, "ledger_refund_committed"))
            if fault == "before_commit":
                raise RuntimeError("injected pre-commit failure")
            db.execute("COMMIT")
        except Exception:
            if db.in_transaction:
                db.execute("ROLLBACK")
            raise

        if fault == "after_commit":
            raise TimeoutError("injected lost response")
        # Provider acceptance and settlement are outside this state model.
        return "ledger_committed"


class RefundTests(unittest.TestCase):
    def setUp(self):
        self.service = RefundService()
        self.service.seed()
        self.p = {
            "order": "order-1", "amount": 1500,
            "approval": "A1", "key": "K1",
        }

    def state(self):
        db = self.service.db
        (remaining,) = db.execute(
            "SELECT remaining FROM orders WHERE owner='alice'"
        ).fetchone()
        (used,) = db.execute(
            "SELECT used FROM approvals WHERE approval_id='A1'"
        ).fetchone()
        (refunds,) = db.execute(
            "SELECT COUNT(*) FROM refunds"
        ).fetchone()
        (audits,) = db.execute(
            "SELECT COUNT(*) FROM audit"
        ).fetchone()
        return remaining, used, refunds, audits

    def test_success_and_retry_after_expiry(self):
        self.assertEqual(self.service.refund("alice", self.p, 100),
                         "ledger_committed")
        self.assertEqual(self.service.refund("alice", self.p, 250),
                         "ledger_committed")
        self.assertEqual(self.state(), (3500, 1, 1, 1))

    def test_expired_approval(self):
        with self.assertRaises(Rejected):
            self.service.refund("alice", self.p, 200)
        self.assertEqual(self.state(), (5000, 0, 0, 0))

    def test_other_principal_and_invalid_shape(self):
        with self.assertRaises(Rejected):
            self.service.refund("bob", self.p, 100)
        with self.assertRaises(Rejected):
            self.service.refund("alice", {**self.p, "extra": 1}, 100)
        self.assertEqual(self.state(), (5000, 0, 0, 0))

    def test_failure_before_commit_rolls_back(self):
        with self.assertRaises(RuntimeError):
            self.service.refund("alice", self.p, 100, "before_commit")
        self.assertEqual(self.state(), (5000, 0, 0, 0))
        self.assertEqual(self.service.refund("alice", self.p, 100),
                         "ledger_committed")
        self.assertEqual(self.state(), (3500, 1, 1, 1))

    def test_lost_response_and_retry(self):
        with self.assertRaises(TimeoutError):
            self.service.refund("alice", self.p, 100, "after_commit")
        self.assertEqual(self.state(), (3500, 1, 1, 1))
        self.assertEqual(self.service.refund("alice", self.p, 250),
                         "ledger_committed")
        self.assertEqual(self.state(), (3500, 1, 1, 1))

    def test_key_conflict_has_no_extra_effect(self):
        self.service.refund("alice", self.p, 100)
        with self.assertRaises(Rejected):
            self.service.refund("alice", {**self.p, "amount": 2000}, 101)
        self.assertEqual(self.state(), (3500, 1, 1, 1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
