import unittest


class Rejected(Exception):
    """The requested transition is not permitted."""


class LostResponse(Exception):
    """The transition committed, but its response was lost."""


class Ledger:
    """Single-process teaching model; not a production datastore."""

    def __init__(self):
        self.version = 0
        self.limit = 20_000  # GBP minor units: £200.00
        self.invoices = {
            "INV-1": {"amount": 12_500, "currency": "GBP",
                      "status": "pending"},
            "INV-2": {"amount": 7_500, "currency": "GBP",
                      "status": "pending"},
            "INV-3": {"amount": 25_000, "currency": "GBP",
                      "status": "pending"},
        }
        self.operations = {}

    def approve(self, invoice_id, key, expected_version, fault=None):
        # Only these two fault points are part of the laboratory.
        if fault not in (None, "before_commit", "lost_response"):
            raise ValueError("unknown fault")
        if not isinstance(key, str) or not key:
            raise Rejected("invalid operation key")
        if type(expected_version) is not int:
            raise Rejected("invalid version")

        request = (invoice_id, expected_version)

        # Replay must precede the current-version check.
        if key in self.operations:
            saved_request, saved_result = self.operations[key]
            if request != saved_request:
                raise Rejected("operation key reused")
            return dict(saved_result)

        if expected_version != self.version:
            raise Rejected("stale version")
        invoice = self.invoices.get(invoice_id)
        if invoice is None:
            raise Rejected("unknown invoice")
        if invoice["status"] != "pending":
            raise Rejected("invoice is not pending")
        if invoice["currency"] != "GBP":
            raise Rejected("unsupported currency")
        if invoice["amount"] > self.limit:
            raise Rejected("approval limit exceeded")

        # Stage copies; no persistent state has changed yet.
        staged_invoices = {
            name: dict(record) for name, record in self.invoices.items()
        }
        staged_invoices[invoice_id]["status"] = "approved"
        result = {"invoice_id": invoice_id, "version": self.version + 1}
        staged_operations = dict(self.operations)
        staged_operations[key] = (request, dict(result))

        if fault == "before_commit":
            raise RuntimeError("injected failure before commit")

        # Logical commit under the model's single-thread assumption.
        self.invoices = staged_invoices
        self.operations = staged_operations
        self.version = result["version"]

        if fault == "lost_response":
            raise LostResponse("injected loss after commit")
        return dict(result)


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.ledger = Ledger()

    def test_two_approvals_and_old_replay(self):
        first = self.ledger.approve("INV-1", "op-1", 0)
        second = self.ledger.approve("INV-2", "op-2", 1)
        replay = self.ledger.approve("INV-1", "op-1", 0)
        self.assertEqual(first, {"invoice_id": "INV-1", "version": 1})
        self.assertEqual(second["version"], 2)
        self.assertEqual(replay, first)
        self.assertEqual(self.ledger.version, 2)

    def test_failure_before_commit(self):
        with self.assertRaises(RuntimeError):
            self.ledger.approve("INV-1", "op-1", 0, "before_commit")
        self.assertEqual(self.ledger.version, 0)
        self.assertEqual(self.ledger.invoices["INV-1"]["status"], "pending")
        self.assertNotIn("op-1", self.ledger.operations)
        self.assertEqual(self.ledger.approve("INV-1", "op-1", 0)["version"], 1)

    def test_lost_response_after_commit(self):
        with self.assertRaises(LostResponse):
            self.ledger.approve("INV-1", "op-1", 0, "lost_response")
        self.assertEqual(self.ledger.version, 1)
        receipt = self.ledger.approve("INV-1", "op-1", 0)
        self.assertEqual(receipt["version"], 1)
        self.assertEqual(self.ledger.version, 1)
        self.assertEqual(self.ledger.invoices["INV-1"]["status"], "approved")

    def test_stale_request_and_key_reuse(self):
        self.ledger.approve("INV-1", "op-1", 0)
        with self.assertRaisesRegex(Rejected, "stale"):
            self.ledger.approve("INV-2", "op-2", 0)
        with self.assertRaisesRegex(Rejected, "reused"):
            self.ledger.approve("INV-2", "op-1", 0)
        self.assertEqual(self.ledger.invoices["INV-2"]["status"], "pending")
        self.assertEqual(self.ledger.version, 1)

    def test_limit_rejection(self):
        with self.assertRaisesRegex(Rejected, "limit"):
            self.ledger.approve("INV-3", "op-3", 0)
        self.assertEqual(self.ledger.invoices["INV-3"]["status"], "pending")
        self.assertEqual(self.ledger.version, 0)
        self.assertNotIn("op-3", self.ledger.operations)


if __name__ == "__main__":
    unittest.main(verbosity=2)
