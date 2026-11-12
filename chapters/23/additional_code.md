# Additional illustrative Python fragments

## Fragment 1

```python
def gate(required_kinds, records, candidate):
    if not required_kinds:
        return "INCONCLUSIVE"

    incomplete = False
    for kind in required_kinds:
        record = records.get(kind)
        if record is None or not compatible(record, candidate, kind):
            incomplete = True
            continue

        status = record.get("status")
        if status == "FAIL":
            return "FAIL"
        if status != "PASS":
            incomplete = True

    return "INCONCLUSIVE" if incomplete else "PASS"
```

## Fragment 2

```python
def test_boolean_amount_is_rejected(self):
    with self.assertRaises(Rejected):
        self.service.refund("alice", {**self.p, "amount": True}, 100)
    self.assertEqual(self.state(), (5000, 0, 0, 0))
```
