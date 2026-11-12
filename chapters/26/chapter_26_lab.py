from dataclasses import asdict, dataclass
import hashlib
import json
import unittest


@dataclass(frozen=True)
class Action:
    op: str
    tenant: str
    record: str
    destination: str = ""


class Gate:
    def __init__(self):
        # Hypothetical records; these are not real secrets.
        self.records = {
            ("north", "incident-42"): ("public", "Service recovered"),
            ("north", "credentials"): ("confidential", "MOCK-SECRET"),
        }
        self.allowed_record = "incident-42"
        self.destinations = {"review-a", "review-b"}
        self.approvals = set()
        self.remaining = 4
        self.effects = []

    @staticmethod
    def digest(action):
        encoded = json.dumps(
            asdict(action), sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def approve_from_trusted_channel(self, action):
        # In this simulation the test harness represents an approver.
        self.approvals.add(self.digest(action))

    def execute(self, action):
        if not isinstance(action, Action):
            return "DENY"
        if action.tenant != "north":
            return "DENY"
        if action.record != self.allowed_record:
            return "DENY"
        if self.remaining <= 0:
            return "DENY"

        entry = self.records.get((action.tenant, action.record))
        if entry is None:
            return "DENY"
        label, text = entry

        if action.op == "read":
            if action.destination:
                return "DENY"
            self.remaining -= 1
            return "OK: " + text

        if action.op == "export":
            if label != "public" or action.destination not in self.destinations:
                return "DENY"
            token = self.digest(action)
            if token not in self.approvals:
                return "PENDING"
            self.approvals.remove(token)  # one use
            self.remaining -= 1
            self.effects.append((action.destination, text))
            return "OK"

        return "DENY"


class GateTests(unittest.TestCase):
    def test_original_scenario(self):
        gate = Gate()
        read = Action("read", "north", "incident-42")
        cross_tenant = Action("read", "south", "incident-42")
        secret = Action("read", "north", "credentials")
        export_a = Action("export", "north", "incident-42", "review-a")
        export_b = Action("export", "north", "incident-42", "review-b")

        self.assertEqual(gate.execute(read), "OK: Service recovered")
        self.assertEqual(gate.execute(cross_tenant), "DENY")
        self.assertEqual(gate.execute(secret), "DENY")
        self.assertEqual(gate.execute(export_a), "PENDING")
        gate.approve_from_trusted_channel(export_a)
        self.assertEqual(gate.execute(export_b), "PENDING")
        self.assertEqual(gate.execute(export_a), "OK")
        self.assertEqual(gate.execute(export_a), "PENDING")

        # Original scenario's effect and budget assertions.
        self.assertEqual(gate.effects, [("review-a", "Service recovered")])
        self.assertEqual(gate.remaining, 2)

    def test_confidential_label_denies_export(self):
        gate = Gate()
        gate.allowed_record = "credentials"
        action = Action("export", "north", "credentials", "review-a")
        gate.approve_from_trusted_channel(action)

        self.assertEqual(gate.execute(action), "DENY")
        self.assertEqual(gate.effects, [])
        self.assertEqual(gate.remaining, 4)
        self.assertIn(gate.digest(action), gate.approvals)

    def test_unknown_destination_denied_even_with_approval(self):
        gate = Gate()
        action = Action("export", "north", "incident-42", "outside")
        gate.approve_from_trusted_channel(action)

        self.assertEqual(gate.execute(action), "DENY")
        self.assertEqual(gate.effects, [])
        self.assertEqual(gate.remaining, 4)

    def test_budget_blocks_approved_export(self):
        gate = Gate()
        action = Action("export", "north", "incident-42", "review-a")
        gate.approve_from_trusted_channel(action)
        gate.remaining = 0

        self.assertEqual(gate.execute(action), "DENY")
        self.assertEqual(gate.effects, [])
        self.assertIn(gate.digest(action), gate.approvals)

    def test_read_with_destination_denied(self):
        gate = Gate()
        action = Action("read", "north", "incident-42", "review-a")

        self.assertEqual(gate.execute(action), "DENY")
        self.assertEqual(gate.remaining, 4)

    def test_missing_record_denied(self):
        gate = Gate()
        gate.allowed_record = "missing"
        action = Action("read", "north", "missing")

        self.assertEqual(gate.execute(action), "DENY")
        self.assertEqual(gate.remaining, 4)

    def test_invalid_input_and_operation_denied(self):
        gate = Gate()

        self.assertEqual(gate.execute("not an action"), "DENY")
        self.assertEqual(
            gate.execute(Action("delete", "north", "incident-42")), "DENY"
        )
        self.assertEqual(gate.effects, [])
        self.assertEqual(gate.remaining, 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
