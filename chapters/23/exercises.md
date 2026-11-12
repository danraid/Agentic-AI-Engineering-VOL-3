# Chapter 23: Exercises

### Exercise 1: Trace and state oracles

**Question.** A refund agent replies, “I cannot refund this invoice without approval.” The trace shows a refund call followed by a successful local commit. Identify two oracles and the likely outcome under each.

### Exercise 2: Approval expiry and retries

**Question.** Approval `A1` expires at time 200. Compare an identical retry at time 250 after a local commit with a first request at time 250. What happens if the retry changes the amount?

### Exercise 3: Confidence after no observed failures

**Question.** Under independent, identically distributed trials, calculate the one-sided 95% upper bound for a failure probability after 100 trials with no observed failures. Can it be applied automatically to adversarial production traffic?

### Exercise 4: Boolean amounts

**Question.** Add a direct test that `True` is rejected as an amount and that local state is unchanged. Why does the code use an exact type check?

### Exercise 5: Choosing a replay cut point

**Question.** A recorded incident contains a malicious document, a model proposal to refund, an old guard decision and a final answer. Which elements would you replay to test a changed guard?

### Exercise 6: A gate with missing evidence

**Question.** A candidate has a compatible passing policy-test record, a compatible failing integration record and no live-evaluation record. What is \(G\)? What if the integration failure is incompatible with the candidate?

### Exercise 7: Provider ambiguity

**Question.** A provider times out after submission. The local outbox says “submitted”, but there is no confirmed response. Why is a fresh idempotency key unsafe, and what evidence is needed?

### Exercise 8: Extending the local policy

**Question.** Suppose approvals can be revoked. Describe a test and an implementation concern; do not assume that the current laboratory supports revocation.
