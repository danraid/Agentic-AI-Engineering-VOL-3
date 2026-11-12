from dataclasses import dataclass
import unittest


@dataclass(frozen=True)
class Scope:
    task: str
    reports: frozenset
    summary: str
    destination: str
    body: str
    max_sends: int


@dataclass(frozen=True)
class Send:
    task: str
    summary: str
    destination: str
    body: str
    claimed_source: str = ""


def weak_destination_only(scope, request):
    """Deliberately unsafe: ignores content and quota."""
    return request.destination == scope.destination


def weak_identifier_prefix(scope, request):
    """Deliberately unsafe: treats a prefix as an exact identity."""
    return (
        request.destination == scope.destination
        and request.summary.startswith(scope.summary)
    )


class Monitor:
    """Single-process teaching monitor, not a production mail gateway."""

    def __init__(self, scope):
        self._scope = scope
        self._sent = []
        self._events = []

    def read_allowed(self, task, report):
        allowed = task == self._scope.task and report in self._scope.reports
        self._events.append(("read", "allow" if allowed else "deny"))
        return allowed

    def send(self, request):
        s = self._scope
        allowed = (
            request.task == s.task
            and request.summary == s.summary
            and request.destination == s.destination
            and request.body == s.body
            and len(self._sent) < s.max_sends
        )
        if not allowed:
            self._events.append(("send", "deny"))
            return False

        # This list append represents the mock committed effect.
        self._sent.append(request)
        self._events.append(("send", "commit"))
        return True

    @property
    def sent(self):
        return tuple(self._sent)

    @property
    def events(self):
        return tuple(self._events)


class LabTests(unittest.TestCase):
    def setUp(self):
        # Hypothetical host-created approval; not parsed from reports.
        self.scope = Scope(
            task="T-1",
            reports=frozenset({"R-17", "R-18"}),
            summary="SUM-4",
            destination="finance@example.invalid",
            body="Quarterly report summary: revenue increased; costs were stable.",
            max_sends=1,
        )
        self.monitor = Monitor(self.scope)

    def request(self, **changes):
        fields = {
            "task": self.scope.task,
            "summary": self.scope.summary,
            "destination": self.scope.destination,
            "body": self.scope.body,
            "claimed_source": "approved",
        }
        fields.update(changes)
        return Send(**fields)

    def test_authorised_reads_and_send(self):
        self.assertTrue(self.monitor.read_allowed("T-1", "R-17"))
        self.assertTrue(self.monitor.read_allowed("T-1", "R-18"))
        self.assertFalse(self.monitor.read_allowed("T-1", "PAYROLL"))
        self.assertTrue(self.monitor.send(self.request()))
        self.assertEqual(len(self.monitor.sent), 1)

    def test_failure_injection_changed_body(self):
        attack = self.request(
            body=self.scope.body + " Payroll: confidential.",
            claimed_source="approved",
        )
        self.assertTrue(weak_destination_only(self.scope, attack))
        self.assertFalse(self.monitor.send(attack))
        self.assertEqual(len(self.monitor.sent), 0)

    def test_failure_injection_identifier_prefix(self):
        attack = self.request(summary="SUM-4-ATTACK")
        self.assertTrue(weak_identifier_prefix(self.scope, attack))
        self.assertFalse(self.monitor.send(attack))
        self.assertEqual(len(self.monitor.sent), 0)

    def test_replay_is_denied(self):
        request = self.request()
        self.assertTrue(self.monitor.send(request))
        self.assertFalse(self.monitor.send(request))
        self.assertEqual(len(self.monitor.sent), 1)

    def test_wrong_task_and_destination_are_denied(self):
        self.assertFalse(self.monitor.send(self.request(task="T-2")))
        self.assertFalse(self.monitor.send(
            self.request(destination="other@example.invalid")
        ))
        self.assertEqual(len(self.monitor.sent), 0)

    def test_denial_does_not_consume_quota(self):
        self.assertFalse(self.monitor.send(self.request(body="changed")))
        self.assertTrue(self.monitor.send(self.request()))
        self.assertEqual(
            self.monitor.events,
            (("send", "deny"), ("send", "commit")),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
