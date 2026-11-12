# Chapter 23: Worked solutions

### Exercise 1: Trace and state oracles

**Suggested solution.** An output oracle might pass if it checks only for the refusal sentence. A trace oracle should reject the successful unauthorised call, and a state oracle should reject the committed refund if no matching approval existed. The test must inspect approval at the relevant decision point rather than assume that the final explanation describes what happened. A separate quality assessment may still judge the wording.

### Exercise 2: Approval expiry and retries

**Suggested solution.** The identical retry can return the stored result because it does not create a new operation. A first request at time 250 fails the exclusive expiry rule \(t<200\). A retry with a changed amount and the same scoped key is a conflict and must not create another local operation. This reasoning is local: it does not establish what a payment provider did.

### Exercise 3: Confidence after no observed failures

**Suggested solution.**

\[
p_{\mathrm{upper}}=1-0.05^{1/100}\approx 0.0295.
\]

The bound is approximately 2.95% under the stated sampling model. It cannot automatically be applied to adversarial production traffic: the distribution may differ, trials may be correlated and the oracle may miss failures. Report the sampled cases and assumptions rather than turning the bound into an unconditional safety claim.

### Exercise 4: Boolean amounts

**Suggested solution.** Add this method to `RefundTests`, then run the modified laboratory:

```python
def test_boolean_amount_is_rejected(self):
    with self.assertRaises(Rejected):
        self.service.refund("alice", {**self.p, "amount": True}, 100)
    self.assertEqual(self.state(), (5000, 0, 0, 0))
```

In Python, `bool` is a subclass of `int`, so `isinstance(True, int)` is true. The exact type check excludes Boolean values. This additional test changes the laboratory source: any CI evidence for the canonical six-test version must not be presented as evidence for the modified version.

### Exercise 5: Choosing a replay cut point

**Suggested solution.** Fix the relevant document and model proposal, preserving the principal and operation context as controlled fixtures. Execute the current guard and adapter rather than replaying the old guard decision or final answer. Inspect both the guard outcome and resulting state. This tests the changed boundary against the recorded proposal; it does not estimate how frequently a live model will generate that proposal.

### Exercise 6: A gate with missing evidence

**Suggested solution.** With a compatible integration failure, \(G=\text{FAIL}\), even though another record is missing. If that failure is incompatible, it is not the candidate’s failure; the missing live record and incompatible integration evidence make \(G=\text{INCONCLUSIVE}\). Both outcomes block promotion under the proposed rule. The old failure remains available for investigation.

### Exercise 7: Provider ambiguity

**Suggested solution.** The provider may already have accepted the original request. A fresh key may cause a second payment. Reconcile using the provider’s documented lookup and key semantics, retaining the original operation identifier and request. Record whether the outcome is confirmed, rejected or still uncertain; escalate if the provider cannot resolve it safely. A local ledger row alone is not evidence of settlement.

### Exercise 8: Extending the local policy

**Suggested solution.** Add a revocation field or authoritative revocation relation, seed a matching approval, revoke it before the decision, and assert that a first refund is rejected without changing balance, consumption, refund count or audit count. Then specify and test the ordering of a concurrent revocation and commit using separate connections under the intended database isolation. The policy must say which event wins and what time or transaction boundary is authoritative. A sequential test with a Boolean fixture alone does not establish concurrent correctness.
