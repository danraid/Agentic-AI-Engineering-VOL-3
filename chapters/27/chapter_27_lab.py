import hashlib
import hmac
import json
import os
import sqlite3
import tempfile
import threading
import unittest

# TEST FIXTURE ONLY: never embed a production signing key in code.
KEY = b"hypothetical-test-key"
NOW = 1_000
POLICY = "v1"
SUPPLIERS = {"library-supplies"}


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def signature(payload):
    return hmac.new(KEY, canonical(payload), hashlib.sha256).hexdigest()


def issue_test_approval(order_id, supplier, amount, version, expires):
    """Simulate an already authenticated approval service."""
    payload = {
        "order_id": order_id,
        "supplier": supplier,
        "amount": amount,
        "version": version,
        "expires": expires,
    }
    return {"payload": payload, "signature": signature(payload)}


def approval_valid(token, order_id, supplier, amount):
    if not isinstance(token, dict):
        return False
    payload = token.get("payload")
    supplied = token.get("signature")
    if not isinstance(payload, dict) or not isinstance(supplied, str):
        return False
    expires = payload.get("expires")
    if type(expires) is not int or expires < NOW:
        return False

    expected = {
        "order_id": order_id,
        "supplier": supplier,
        "amount": amount,
        "version": POLICY,
        "expires": expires,
    }
    return payload == expected and hmac.compare_digest(
        supplied, signature(payload)
    )


def initialise(path, budget):
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE budget (available INTEGER NOT NULL)")
        db.execute("INSERT INTO budget VALUES (?)", (budget,))
        db.execute("""
            CREATE TABLE reservations (
                order_id TEXT PRIMARY KEY,
                supplier TEXT NOT NULL,
                amount INTEGER NOT NULL,
                version TEXT NOT NULL
            )
        """)


def reserve(path, order_id, supplier, amount, token=None):
    # Hard rules apply before review; approval cannot override them.
    if (
        not isinstance(order_id, str) or not order_id
        or supplier not in SUPPLIERS
        or type(amount) is not int
        or not 0 < amount <= 500
    ):
        return "DENY_POLICY"

    with sqlite3.connect(path, timeout=10) as db:
        # Serialises competing SQLite writers before reading the balance.
        db.execute("BEGIN IMMEDIATE")
        previous = db.execute(
            "SELECT supplier, amount, version FROM reservations "
            "WHERE order_id = ?",
            (order_id,),
        ).fetchone()

        if previous is not None:
            if previous == (supplier, amount, POLICY):
                return "ALREADY_RESERVED"
            return "ID_CONFLICT"

        if amount > 100 and not approval_valid(
            token, order_id, supplier, amount
        ):
            return "DENY_APPROVAL"

        changed = db.execute(
            "UPDATE budget SET available = available - ? "
            "WHERE available >= ?",
            (amount, amount),
        ).rowcount
        if changed != 1:
            return "DENY_BUDGET"

        db.execute(
            "INSERT INTO reservations VALUES (?, ?, ?, ?)",
            (order_id, supplier, amount, POLICY),
        )
        return "RESERVED"


def available(path):
    with sqlite3.connect(path) as db:
        return db.execute("SELECT available FROM budget").fetchone()[0]


def run_tests():
    supplier = "library-supplies"
    with tempfile.TemporaryDirectory() as directory:
        path = os.path.join(directory, "lab.sqlite")
        initialise(path, 600)

        # Failure injection 1: corrupt an otherwise valid signature.
        forged = issue_test_approval("F", supplier, 360, POLICY, 1100)
        forged["signature"] = "0" * 64
        assert reserve(path, "F", supplier, 360, forged) == "DENY_APPROVAL"

        # Failure injection 2: change the order after approval.
        changed = issue_test_approval("C", supplier, 360, POLICY, 1100)
        assert reserve(path, "C", supplier, 400, changed) == "DENY_APPROVAL"

        # Failure injection 3: approval was issued under an old policy.
        old = issue_test_approval("O", supplier, 360, "v0", 1100)
        assert reserve(path, "O", supplier, 360, old) == "DENY_APPROVAL"

        expired = issue_test_approval("E", supplier, 360, POLICY, 999)
        assert reserve(path, "E", supplier, 360, expired) == "DENY_APPROVAL"
        assert reserve(path, "X", "unknown", 10) == "DENY_POLICY"
        assert available(path) == 600

        # Two £360 orders compete for £600.
        barrier = threading.Barrier(2)
        results = []
        result_lock = threading.Lock()

        def worker(order_id):
            token = issue_test_approval(
                order_id, supplier, 360, POLICY, 1100
            )
            barrier.wait()
            outcome = reserve(path, order_id, supplier, 360, token)
            with result_lock:
                results.append((order_id, outcome))

        threads = [
            threading.Thread(target=worker, args=(order_id,))
            for order_id in ("A", "B")
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert sorted(outcome for _, outcome in results) == [
            "DENY_BUDGET", "RESERVED"
        ]
        assert available(path) == 240

        winner = next(i for i, outcome in results if outcome == "RESERVED")
        assert reserve(path, winner, supplier, 360) == "ALREADY_RESERVED"
        assert reserve(path, winner, supplier, 100) == "ID_CONFLICT"
        assert available(path) == 240


def public_digest(action):
    """An action fingerprint, not proof of a human decision."""
    return hashlib.sha256(canonical(action)).hexdigest()


def insecure_digest_gate(action, claimed_approval):
    """Deliberately unsafe: accepts any matching public fingerprint."""
    return claimed_approval == public_digest(action)


class TestOversightLab(unittest.TestCase):
    def test_reservation_scenarios(self):
        run_tests()

    def test_public_digest_is_forgeable(self):
        action = {
            "order_id": "P-17",
            "supplier": "library-supplies",
            "amount": 360,
            "version": POLICY,
        }
        # An unauthorised caller can compute the same public digest.
        attacker_claim = public_digest(action)
        self.assertTrue(insecure_digest_gate(action, attacker_claim))


if __name__ == "__main__":
    unittest.main()
