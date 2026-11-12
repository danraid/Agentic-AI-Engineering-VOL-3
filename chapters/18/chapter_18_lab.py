import unittest
from itertools import permutations


def allocate(costs):
    """Return the minimum (cost, assignment), breaking ties deterministically."""
    vehicles = tuple(sorted(costs))
    packages = tuple(sorted(next(iter(costs.values()))))
    if len(vehicles) != len(packages):
        raise ValueError("This demonstration requires equal-sized sets")
    candidates = []
    for order in permutations(vehicles):
        pairs = tuple(zip(packages, order))
        total = sum(costs[vehicle][package] for package, vehicle in pairs)
        candidates.append((total, pairs))
    return min(candidates)


class Ledger:
    """Sequential in-memory model; not a distributed or physical service."""

    def __init__(self):
        self.time = 0
        self.tasks = {}
        self.operations = {}
        self.effects = 0

    def advance(self, ticks):
        if ticks < 0:
            raise ValueError("Time cannot move backwards")
        self.time += ticks

    def assign(self, package, vehicle, duration):
        if duration <= 0:
            raise ValueError("Duration must be positive")
        old = self.tasks.get(package)
        if old is not None:
            if old["status"] == "complete":
                return None
            if self.time < old["expiry"]:
                return None
        epoch = 1 if old is None else old["epoch"] + 1
        self.tasks[package] = {
            "vehicle": vehicle,
            "epoch": epoch,
            "expiry": self.time + duration,
            "status": "active",
        }
        return epoch

    def release(self, package, vehicle, epoch, operation):
        payload = (package, vehicle, epoch)
        if operation in self.operations:
            if self.operations[operation] == payload:
                return "duplicate"
            return "conflict"

        task = self.tasks.get(package)
        if (
            task is None
            or task["status"] != "active"
            or task["vehicle"] != vehicle
            or task["epoch"] != epoch
            or self.time >= task["expiry"]
        ):
            return "rejected"

        # One simulated atomic transition: no real actuator is called.
        task["status"] = "complete"
        self.operations[operation] = payload
        self.effects += 1
        return "accepted"


class CoordinationTests(unittest.TestCase):
    def test_allocation(self):
        costs = {
            "A": {"X": 2, "Y": 5},
            "B": {"X": 4, "Y": 3},
        }
        self.assertEqual(
            allocate(costs), (5, (("X", "A"), ("Y", "B")))
        )

    def test_completion_and_operation_identifiers(self):
        ledger = Ledger()
        self.assertEqual(ledger.assign("X", "A", 3), 1)
        self.assertIsNone(ledger.assign("X", "B", 3))
        self.assertEqual(ledger.release("X", "A", 1, "op-1"), "accepted")
        self.assertEqual(ledger.release("X", "A", 1, "op-1"), "duplicate")
        self.assertEqual(ledger.release("X", "B", 1, "op-1"), "conflict")
        self.assertEqual(ledger.release("X", "A", 1, "op-new"), "rejected")
        self.assertEqual(ledger.effects, 1)
        self.assertIsNone(ledger.assign("X", "B", 3))

    def test_expiry_and_stale_request(self):
        ledger = Ledger()
        self.assertEqual(ledger.assign("X", "A", 3), 1)
        ledger.advance(3)
        self.assertEqual(ledger.release("X", "A", 1, "expired"), "rejected")
        self.assertEqual(ledger.assign("X", "B", 4), 2)
        self.assertEqual(ledger.release("X", "A", 1, "stale"), "rejected")
        self.assertEqual(ledger.release("X", "B", 2, "op-2"), "accepted")
        self.assertEqual(ledger.release("X", "B", 2, "op-2"), "duplicate")
        self.assertEqual(ledger.effects, 1)

    def test_invalid_time_and_duration(self):
        ledger = Ledger()
        with self.assertRaises(ValueError):
            ledger.advance(-1)
        with self.assertRaises(ValueError):
            ledger.assign("X", "A", 0)

    def test_fresh_ledger_loses_state(self):
        ledger = Ledger()
        self.assertEqual(ledger.assign("X", "A", 3), 1)
        self.assertEqual(ledger.release("X", "A", 1, "op-1"), "accepted")

        restarted = Ledger()  # No persistence or recovery is implemented.
        self.assertEqual(restarted.tasks, {})
        self.assertEqual(restarted.operations, {})
        self.assertEqual(restarted.effects, 0)
        self.assertEqual(restarted.assign("X", "B", 3), 1)

    @unittest.expectedFailure
    def test_vehicle_capacity_should_prevent_two_active_packages(self):
        ledger = Ledger()
        self.assertEqual(ledger.assign("X", "A", 3), 1)
        # Desired behaviour: reject a second active task for A.
        # The current per-package ledger instead returns epoch 1.
        self.assertIsNone(ledger.assign("Y", "A", 3))

    @unittest.skip("No concurrent or transactional ledger is implemented")
    def test_concurrent_conflicting_assignments_are_serialised(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
