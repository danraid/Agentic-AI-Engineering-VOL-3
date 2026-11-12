# Chapter 19: Worked solutions

### Exercise 1: Threshold boundary

**Suggested solution.** Exactly £100 requires approval because the rule uses `>= 10_000`. The laboratory rejects `USD` before applying the threshold. A multi-currency system needs an explicit currency policy; it must not assume that equal numeric amounts represent equal value.

### Exercise 2: An unsafe transition

**Suggested solution.** Request-level at-most-one-effect safety is endangered. The first call may have succeeded, and a new key permits the bank to interpret the retry as a separate payment. Reconcile or retry with the original key only under a suitable bank contract. Do not infer failure from the timeout.

### Exercise 3: Approval binding

**Suggested solution.** The changed payee is a material change, so the old approval does not authorise version 2. Obtain a new approval bound to the revised contents. Before dispatching version 2, establish that version 1 is not in flight, unknown or already paid. A new key alone does not prevent a duplicate effect.

### Exercise 4: Ambiguous absence

**Suggested solution.** Not unless the bank contract makes that lookup a final determination. The original request may still be executing or the lookup index may lag. Keep the operation unresolved, use a same-key retry if the documented idempotency contract permits it, or wait and escalate.

### Exercise 5: Retry assumptions

**Suggested solution.** Both attempts may use the same expired credential. Their failures are correlated, so the independent-attempt calculation is inappropriate. Classify the error, refresh the credential or escalate, and retry only when the relevant condition has changed. For a side-effecting call, preserve the operation identity and resolve any uncertainty about the prior attempt.

### Exercise 6: Concurrent dispatchers

**Suggested solution.** Claim the entry with an atomic update or lease, and ensure both workers use the same key and fingerprint. Record attempt identifiers for diagnosis. A lease alone is insufficient if its former holder continues after expiry. Downstream atomic deduplication or downstream-supported fencing must address overlapping calls. Test the actual bank contract, not just the local lock.

### Exercise 7: Approval expiry

**Suggested solution.** Specify whether approval must be valid at local dispatch or at bank acceptance. A local check cannot guarantee arrival before expiry. If validity at acceptance is required, the downstream system may need to verify a short-lived signed authorisation or another enforceable condition. The clock and failure treatment must also be specified.

### Exercise 8: Extend the laboratory

**Suggested solution.** Version 1 becomes `UNKNOWN` even though the fake bank has inserted an effect. Version 2 must be blocked before reconciliation. Reconciliation should return the version 1 receipt and set its status to `CONFIRMED`; version 2 must remain blocked afterwards. The test demonstrates both uncertainty and the rule that confirmation does not authorise a second versioned payment.

### Exercise 9: Evaluate two architectures

**Suggested solution.** Use the same privacy-safe cases, tool permissions and budget. Include ordinary invoices, threshold boundaries, altered payees, conflicting evidence, stale approvals and timeout scenarios. Measure end-to-end decisions, unsafe submissions, unresolved cases, human interventions, latency and cost. Use independent review for sampled cases and disagreements. Report failure categories and uncertainty; do not treat model confidence or another model’s judgement as ground truth.
