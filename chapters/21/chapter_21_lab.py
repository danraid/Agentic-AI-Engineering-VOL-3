from dataclasses import dataclass
import re
import unittest


VALID = "valid"
INVALID = "invalid"
UNKNOWN = "unknown"
POLICY = "hypothetical-v1"


@dataclass(frozen=True)
class Proposal:
    request_id: str
    destination: str
    summary: str


class Authority:
    """In-memory sequential model, not a production transaction."""

    def __init__(self, status, stale=False, leak=False):
        if status not in (VALID, INVALID, UNKNOWN):
            raise ValueError("unsupported consent status")
        self.status = status
        self.previous = status
        self.stale = stale
        self.leak = leak
        self.deliveries = {}   # request_id -> (destination, summary)
        self.reviews = set()   # request identifiers only
        self.audit = []        # metadata, except in leak injection

    def set_status(self, status):
        if status not in (VALID, INVALID, UNKNOWN):
            raise ValueError("unsupported consent status")
        self.previous = self.status
        self.status = status

    def _record(self, proposal, outcome):
        record = {
            "request_id": proposal.request_id,
            "policy": POLICY,
            "outcome": outcome,
        }
        if self.leak:  # Deliberate defect: violates R6.
            record["summary"] = proposal.summary
        self.audit.append(record)

    def commit(self, proposal):
        # Restrict identifiers so arbitrary text cannot enter audit
        # via this field. This is not a complete privacy control.
        if not re.fullmatch(r"req-[0-9]+", proposal.request_id):
            raise ValueError("invalid request identifier")

        payload = (proposal.destination, proposal.summary)
        existing = self.deliveries.get(proposal.request_id)

        if existing is not None:
            outcome = "duplicate" if existing == payload else "conflict"
        else:
            checked = self.previous if self.stale else self.status
            if checked == VALID:
                self.deliveries[proposal.request_id] = payload
                outcome = "committed"
            elif checked == INVALID:
                outcome = "denied"
            else:
                self.reviews.add(proposal.request_id)
                outcome = "deferred"

        self._record(proposal, outcome)
        return outcome


def contains_summary(authority, summary):
    """Toy oracle: detect this exact summary in audit values."""
    return any(
        summary in str(value)
        for record in authority.audit
        for value in record.values()
    )


class LaboratoryTests(unittest.TestCase):
    def setUp(self):
        self.p = Proposal("req-17", "support-desk", "PRIVATE-SENTINEL")

    def test_valid_commit_and_identical_retry(self):
        a = Authority(VALID)
        self.assertEqual(a.commit(self.p), "committed")
        self.assertEqual(a.commit(self.p), "duplicate")
        self.assertEqual(len(a.deliveries), 1)
        self.assertEqual(
            [r["outcome"] for r in a.audit],
            ["committed", "duplicate"],
        )

    def test_changed_payload_is_a_conflict(self):
        a = Authority(VALID)
        self.assertEqual(a.commit(self.p), "committed")
        changed = Proposal("req-17", "support-desk", "different")
        self.assertEqual(a.commit(changed), "conflict")
        self.assertEqual(a.deliveries["req-17"][1], self.p.summary)

    def test_invalid_and_unknown_do_not_commit(self):
        denied = Authority(INVALID)
        deferred = Authority(UNKNOWN)
        self.assertEqual(denied.commit(self.p), "denied")
        self.assertEqual(deferred.commit(self.p), "deferred")
        self.assertEqual(denied.deliveries, {})
        self.assertEqual(deferred.deliveries, {})
        self.assertEqual(deferred.reviews, {"req-17"})

    def test_withdrawal_before_commit_is_enforced(self):
        a = Authority(VALID)
        a.set_status(INVALID)
        self.assertEqual(a.commit(self.p), "denied")
        self.assertEqual(a.deliveries, {})

    def test_stale_consent_injection_is_detected(self):
        broken = Authority(VALID, stale=True)
        broken.set_status(INVALID)
        self.assertEqual(broken.commit(self.p), "committed")
        self.assertEqual(broken.status, INVALID)
        self.assertIn("req-17", broken.deliveries)

    def test_audit_and_leak_injection(self):
        safe = Authority(VALID)
        broken = Authority(VALID, leak=True)
        safe.commit(self.p)
        broken.commit(self.p)
        self.assertFalse(contains_summary(safe, self.p.summary))
        self.assertTrue(contains_summary(broken, self.p.summary))
        self.assertEqual(
            set(safe.audit[0]), {"request_id", "policy", "outcome"}
        )

    def test_bad_identifier_is_rejected(self):
        a = Authority(VALID)
        bad = Proposal("PRIVATE-SENTINEL", "support-desk", "text")
        with self.assertRaises(ValueError):
            a.commit(bad)
        self.assertEqual(a.audit, [])
        self.assertEqual(a.deliveries, {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
