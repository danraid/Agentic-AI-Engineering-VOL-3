import sqlite3
import unittest


def database():
    return sqlite3.connect(":memory:")


def create_databases():
    local = database()
    provider = database()

    local.executescript("""
    CREATE TABLE job (
        k TEXT PRIMARY KEY,
        amount INTEGER NOT NULL,
        currency TEXT NOT NULL,
        state TEXT NOT NULL,
        receipt TEXT,
        address TEXT NOT NULL,
        version INTEGER NOT NULL
    );
    CREATE TABLE outbox (
        k TEXT PRIMARY KEY,
        state TEXT NOT NULL,
        owner TEXT,
        lease_until INTEGER NOT NULL,
        epoch INTEGER NOT NULL
    );
    """)

    provider.execute("""
    CREATE TABLE charge (
        k TEXT PRIMARY KEY,
        amount INTEGER NOT NULL,
        currency TEXT NOT NULL,
        receipt TEXT NOT NULL
    )
    """)
    return local, provider


def submit(local, k, amount, currency, address):
    # The business record and dispatch intent commit together locally.
    with local:
        local.execute(
            "INSERT INTO job VALUES (?, ?, ?, 'PENDING', NULL, ?, 0)",
            (k, amount, currency, address),
        )
        local.execute(
            "INSERT INTO outbox VALUES (?, 'READY', NULL, 0, 0)",
            (k,),
        )


def claim(local, k, worker, now, duration):
    # Logical time makes the scenario independent of the system clock.
    with local:
        changed = local.execute("""
            UPDATE outbox
               SET owner = ?, lease_until = ?, epoch = epoch + 1
             WHERE k = ? AND state = 'READY'
               AND (owner IS NULL OR lease_until <= ?)
               AND EXISTS (
                   SELECT 1 FROM job
                    WHERE job.k = outbox.k
                      AND job.state IN ('PENDING', 'IN_DOUBT')
               )
        """, (worker, now + duration, k, now)).rowcount
        if not changed:
            return None
        return local.execute(
            "SELECT epoch FROM outbox WHERE k = ?", (k,)
        ).fetchone()[0]


def mark_in_doubt(local, k, worker, epoch, now):
    # Record uncertainty before entering the simulated external boundary.
    with local:
        owner = local.execute("""
            SELECT 1 FROM outbox
             WHERE k = ? AND state = 'READY'
               AND owner = ? AND epoch = ? AND lease_until > ?
        """, (k, worker, epoch, now)).fetchone()
        if not owner:
            return False
        changed = local.execute("""
            UPDATE job SET state = 'IN_DOUBT'
             WHERE k = ? AND state = 'PENDING'
        """, (k,)).rowcount
        return changed == 1


def pay(provider, k, amount, currency):
    # A hypothetical provider's key/payload check, on one connection.
    with provider:
        row = provider.execute(
            "SELECT amount, currency, receipt FROM charge WHERE k = ?",
            (k,),
        ).fetchone()
        if row:
            if row[:2] != (amount, currency):
                raise ValueError("operation key reused with different intent")
            return row[2]
        receipt = "receipt:" + k
        provider.execute(
            "INSERT INTO charge VALUES (?, ?, ?, ?)",
            (k, amount, currency, receipt),
        )
        return receipt


def acknowledge(local, k, worker, epoch, now, receipt):
    # The lab trusts a receipt obtained directly from pay().
    # A real system must independently validate provider evidence.
    with local:
        changed = local.execute("""
            UPDATE outbox SET state = 'DONE'
             WHERE k = ? AND state = 'READY'
               AND owner = ? AND epoch = ? AND lease_until > ?
        """, (k, worker, epoch, now)).rowcount
        if not changed:
            return False
        changed = local.execute("""
            UPDATE job SET state = 'SUCCEEDED', receipt = ?
             WHERE k = ? AND state = 'IN_DOUBT'
        """, (receipt, k)).rowcount
        if changed != 1:
            # Raising rolls back the outbox update as well.
            raise RuntimeError("illegal job state for acknowledgement")
        return True


def human_edit(local, k, address):
    with local:
        local.execute("""
            UPDATE job SET address = ?, version = version + 1
             WHERE k = ?
        """, (address, k))


def cancel_unclaimed(local, k, expected_version):
    # Sequential model only: the ownership read is not a concurrency proof.
    with local:
        row = local.execute("""
            SELECT state, owner FROM outbox WHERE k = ?
        """, (k,)).fetchone()
        if row != ("READY", None):
            raise RuntimeError("unsafe to cancel this outbox item")
        changed = local.execute("""
            UPDATE job SET state = 'CANCELLED'
             WHERE k = ? AND state = 'PENDING' AND version = ?
        """, (k, expected_version)).rowcount
        if changed:
            local.execute(
                "UPDATE outbox SET state = 'CANCELLED' WHERE k = ?", (k,)
            )
            return True
        local.execute("""
            UPDATE job SET state = 'MANUAL_REVIEW'
             WHERE k = ? AND state = 'PENDING'
        """, (k,))
        local.execute(
            "UPDATE outbox SET state = 'BLOCKED' WHERE k = ?", (k,)
        )
        return False


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.local, self.provider = create_databases()

    def tearDown(self):
        self.local.close()
        self.provider.close()

    def test_lost_response_and_stale_worker(self):
        key = "order-17:charge:v1"
        submit(self.local, key, 800, "GBP", "Old Street")
        epoch_a = claim(self.local, key, "worker-a", now=0, duration=5)
        self.assertEqual(epoch_a, 1)
        self.assertTrue(
            mark_in_doubt(self.local, key, "worker-a", epoch_a, now=0)
        )

        # Provider commits; the response is then treated as lost.
        try:
            receipt = pay(self.provider, key, 800, "GBP")
            raise TimeoutError("simulated lost response after commit")
        except TimeoutError:
            pass

        self.assertEqual(
            self.local.execute(
                "SELECT state FROM job WHERE k = ?", (key,)
            ).fetchone()[0],
            "IN_DOUBT",
        )

        # B takes over after expiry; A's late acknowledgement is fenced.
        epoch_b = claim(self.local, key, "worker-b", now=6, duration=5)
        self.assertEqual(epoch_b, 2)
        self.assertFalse(
            acknowledge(self.local, key, "worker-a", epoch_a, 6, receipt)
        )
        retry_receipt = pay(self.provider, key, 800, "GBP")
        self.assertEqual(retry_receipt, receipt)
        self.assertTrue(
            acknowledge(self.local, key, "worker-b", epoch_b, 6,
                        retry_receipt)
        )
        self.assertEqual(
            self.provider.execute("SELECT COUNT(*) FROM charge").fetchone()[0],
            1,
        )
        self.assertEqual(
            self.local.execute(
                "SELECT state, receipt FROM job WHERE k = ?", (key,)
            ).fetchone(),
            ("SUCCEEDED", receipt),
        )

    def test_conflicting_payment_key(self):
        key = "order-17:charge:v1"
        pay(self.provider, key, 800, "GBP")
        with self.assertRaises(ValueError):
            pay(self.provider, key, 801, "GBP")

    def test_human_edit_blocks_stale_cancellation(self):
        key = "order-18:charge:v1"
        submit(self.local, key, 1200, "GBP", "First Address")
        saved_version = 0
        human_edit(self.local, key, "Corrected Address")
        self.assertFalse(cancel_unclaimed(self.local, key, saved_version))
        self.assertEqual(
            self.local.execute(
                "SELECT state, address, version FROM job WHERE k = ?", (key,)
            ).fetchone(),
            ("MANUAL_REVIEW", "Corrected Address", 1),
        )
        self.assertEqual(
            self.local.execute(
                "SELECT state FROM outbox WHERE k = ?", (key,)
            ).fetchone()[0],
            "BLOCKED",
        )

    def test_ordinary_undispatched_cancellation(self):
        key = "order-19:charge:v1"
        submit(self.local, key, 500, "GBP", "New Street")
        self.assertTrue(cancel_unclaimed(self.local, key, 0))
        self.assertEqual(
            self.local.execute(
                "SELECT state FROM job WHERE k = ?", (key,)
            ).fetchone()[0],
            "CANCELLED",
        )
        self.assertEqual(
            self.local.execute(
                "SELECT state FROM outbox WHERE k = ?", (key,)
            ).fetchone()[0],
            "CANCELLED",
        )

    def test_deduplication_record_loss_allows_second_acceptance_path(self):
        key = "order-20:charge:v1"

        # This list is test instrumentation for distinct acceptances.
        # It is not the simulated provider's durable financial ledger.
        acceptances = []

        def attempt():
            existed = self.provider.execute(
                "SELECT 1 FROM charge WHERE k = ?", (key,)
            ).fetchone() is not None
            receipt = pay(self.provider, key, 800, "GBP")
            if not existed:
                acceptances.append((key, 800, "GBP"))
            return receipt

        first = attempt()
        self.assertEqual(attempt(), first)
        self.assertEqual(len(acceptances), 1)

        # Mutation: discard the record used for deduplication.
        with self.provider:
            self.provider.execute("DELETE FROM charge WHERE k = ?", (key,))

        self.assertEqual(attempt(), first)
        self.assertEqual(len(acceptances), 2)

    def test_claim_rejects_ineligible_job_state(self):
        key = "order-21:charge:v1"
        submit(self.local, key, 600, "GBP", "High Street")
        # Deliberately create an inconsistent job/outbox combination.
        with self.local:
            self.local.execute(
                "UPDATE job SET state = 'SUCCEEDED' WHERE k = ?", (key,)
            )
        self.assertIsNone(
            claim(self.local, key, "worker-a", now=0, duration=5)
        )
        self.assertEqual(
            self.local.execute(
                "SELECT state, owner, lease_until, epoch "
                "FROM outbox WHERE k = ?", (key,)
            ).fetchone(),
            ("READY", None, 0, 0),
        )


if __name__ == "__main__":
    unittest.main()
