from dataclasses import asdict, dataclass, replace
import hashlib
import json
import unittest


@dataclass(frozen=True)
class Request:
    request_id: str
    version: int
    amount_pence: int
    currency: str
    payee: str


def fingerprint(request):
    encoded = json.dumps(
        asdict(request), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def operation_key(request):
    return (request.request_id, request.version)


class FakeBank:
    def __init__(self):
        # key -> (fingerprint, receipt); insertion simulates an effect.
        self.effects = {}

    def transfer(self, request, fault=None):
        key = operation_key(request)
        digest = fingerprint(request)

        if key in self.effects:
            old_digest, receipt = self.effects[key]
            if old_digest != digest:
                raise ValueError("operation key reused with new contents")
            return receipt

        if fault == "before":
            raise TimeoutError("response unavailable")

        receipt = "receipt-" + str(len(self.effects) + 1)
        self.effects[key] = (digest, receipt)

        if fault == "after":
            raise TimeoutError("response unavailable")
        return receipt

    def lookup(self, request):
        entry = self.effects.get(operation_key(request))
        if entry is None:
            return None
        digest, receipt = entry
        if digest != fingerprint(request):
            raise ValueError("operation key reused with new contents")
        return receipt


class Supervisor:
    def __init__(self, bank):
        self.bank = bank
        self.approvals = set()
        self.events = []
        self.fingerprints = {}  # operation key -> request fingerprint
        self.status = {}        # operation key -> local status

    def _remember(self, request):
        key = operation_key(request)
        digest = fingerprint(request)
        previous = self.fingerprints.get(key)
        if previous is not None and previous != digest:
            raise ValueError("operation key reused with new contents")
        self.fingerprints[key] = digest

    def _check_other_versions(self, request):
        key = operation_key(request)
        blocking = {"SUBMITTING", "UNKNOWN", "CONFIRMED"}
        for other_key, state in self.status.items():
            if (other_key != key
                    and other_key[0] == request.request_id
                    and state in blocking):
                raise ValueError(
                    "another version may have effected payment"
                )

    def approve_for_test(self, request):
        # Simulation only: this does not authenticate a human.
        self._remember(request)
        self.approvals.add(fingerprint(request))
        self.events.append(("approved", operation_key(request)))

    def submit(self, request, fault=None):
        if request.currency != "GBP" or request.amount_pence <= 0:
            raise ValueError("invalid request")

        self._remember(request)
        self._check_other_versions(request)
        key = operation_key(request)

        if (request.amount_pence >= 10_000
                and fingerprint(request) not in self.approvals):
            self.status[key] = "WAITING_APPROVAL"
            self.events.append(("waiting_approval", key))
            return "WAITING_APPROVAL"

        self.status[key] = "SUBMITTING"
        self.events.append(("submitting", key))
        try:
            receipt = self.bank.transfer(request, fault)
        except TimeoutError:
            self.status[key] = "UNKNOWN"
            self.events.append(("unknown", key))
            return "UNKNOWN"

        self.status[key] = "CONFIRMED"
        self.events.append(("confirmed", key))
        return receipt

    def reconcile(self, request):
        self._remember(request)
        receipt = self.bank.lookup(request)
        if receipt is None:
            self.events.append(("still_unknown", operation_key(request)))
            return "UNKNOWN"
        self.status[operation_key(request)] = "CONFIRMED"
        self.events.append(("confirmed", operation_key(request)))
        return receipt


def run_tests():
    bank = FakeBank()
    supervisor = Supervisor(bank)

    r1 = Request("R1", 1, 7_500, "GBP", "supplier-A")
    r2 = Request("R2", 1, 15_000, "GBP", "supplier-B")

    # Failure 1: effect committed, response lost.
    assert supervisor.submit(r1, fault="after") == "UNKNOWN"
    assert len(bank.effects) == 1
    assert supervisor.reconcile(r1) == "receipt-1"
    assert supervisor.submit(r1) == "receipt-1"
    assert len(bank.effects) == 1

    # Approval binds to the exact version and contents.
    assert supervisor.submit(r2) == "WAITING_APPROVAL"
    supervisor.approve_for_test(r2)
    revised = replace(r2, version=2, payee="supplier-C")
    assert supervisor.submit(revised) == "WAITING_APPROVAL"

    # Failure 2: no effect committed, but outcome is still UNKNOWN.
    assert supervisor.submit(r2, fault="before") == "UNKNOWN"
    assert supervisor.reconcile(r2) == "UNKNOWN"
    assert supervisor.submit(r2) == "receipt-2"
    assert len(bank.effects) == 2

    # Same key with different contents is rejected by the bank.
    conflicting = replace(r1, payee="different-supplier")
    try:
        bank.transfer(conflicting)
    except ValueError:
        pass
    else:
        raise AssertionError("conflicting reuse was not rejected")

    # R1: 5 events; R2 approval/revision: 3; timeout: 2;
    # reconciliation: 1; final submission: 2.
    assert len(supervisor.events) == 13

    print("All deterministic scenario assertions passed.")
    print("Committed simulated effects:", len(bank.effects))
    print("Recorded supervisor events:", len(supervisor.events))


class HandoffLaboratoryTests(unittest.TestCase):
    def test_original_scenario(self):
        run_tests()

    def test_unknown_version_blocks_replacement(self):
        bank = FakeBank()
        supervisor = Supervisor(bank)
        original = Request("R1", 1, 7_500, "GBP", "supplier-A")
        replacement = replace(original, version=2, payee="supplier-C")

        self.assertEqual(
            supervisor.submit(original, fault="before"), "UNKNOWN"
        )
        with self.assertRaisesRegex(ValueError, "another version"):
            supervisor.submit(replacement)
        self.assertEqual(len(bank.effects), 0)

        # A missing lookup is not treated as final cancellation.
        self.assertEqual(supervisor.reconcile(original), "UNKNOWN")
        with self.assertRaisesRegex(ValueError, "another version"):
            supervisor.submit(replacement)

        # Same-key retry confirms version 1; version 2 remains blocked.
        self.assertEqual(supervisor.submit(original), "receipt-1")
        with self.assertRaisesRegex(ValueError, "another version"):
            supervisor.submit(replacement)
        self.assertEqual(len(bank.effects), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
