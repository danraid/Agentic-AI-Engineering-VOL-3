# Chapter 28: Worked solutions

### Exercise 1: Scope and purpose

**Suggested solution.** Tenant, case and assignment comparisons may be true, but the purpose comparison is false, so the conjunction is false. Changing the purpose makes the fixture comparisons true, assuming the stated assignment. It does not establish real authorisation: identity, assignment freshness, delegation and the actual workflow must be validated by authoritative services. A caller-controlled purpose string is not proof of purpose.

### Exercise 2: Labels and provenance

**Suggested solution.** The join is `INTERNAL`, because `PUBLIC` is below `INTERNAL`. The rewrite remains conservatively `INTERNAL` if it derives from the note. A safe declassification process could examine the sentence and its provenance against approved criteria, but brevity and a model’s self-assessment do not establish safe disclosure. The gateway also needs trusted provenance; accepting the model’s claimed source list would leave the original problem unresolved.

### Exercise 3: Approval, concurrency and recovery

**Suggested solution.** The check and assignment are separate operations. Both workers can observe `used == False` before either sets it to `True`. A durable store can perform an atomic conditional transition from unused to consumed, bound to the action and expiry; only the successful worker proceeds. An idempotency key and reconciliation process can reduce duplicate external effects. A crash or timeout between consumption and a provider response still creates uncertainty about whether the provider acted. Recovery must distinguish confirmed delivery, confirmed failure and unknown outcome rather than blindly retrying.

### Exercise 4: Proportionate evidence

**Suggested solution.** The event could contain an action reference, time, decision and reason code, policy version, destination category, approval reference and appropriately protected case and actor references. The investigator may also need a controlled route to inspect relevant source material if the reason code is disputed. Even without message text, identifiers, timestamps and destination categories can reveal relationships or behaviour. Access, retention and permitted uses therefore still require governance.

### Exercise 5: Policy change

**Suggested solution.** The production gateway should obtain authoritative current policy, stop or re-evaluate the queued action, invalidate incompatible approval and notify the responsible workflow owner as appropriate. It should also consider related cached decisions and pending jobs. The laboratory demonstrates only that differing caller-supplied version strings cause denial and leave the fixture approval unused. It does not fetch authoritative policy or invalidate a distributed queue.

### Exercise 6: Probability and assumptions

**Suggested solution.**

\[
P(\text{at least one})=1-(1-0.02)^2
=1-0.9604=0.0396.
\]

The result is 3.96% under the exercise’s assumptions. The probabilities are hypothetical, the events may be dependent, and the calculation treats events alike without measuring their consequences. Real assessment requires evidence about the deployment and its uncertainty; the formula alone supplies none.

### Exercise 7: Forged authority

**Suggested solution.** `send` trusts the draft’s caller-supplied label and `approve` can be called without authenticating a reviewer. The toy interface rejects extra claims and resolves references in local dictionaries, but callers can bypass it and construct objects directly. A production boundary would need protected draft and provenance storage, authenticated reviewer approval, controlled credentials and a gateway that cannot be bypassed. Tests should also exercise forged references, revoked authority and stale classifications through the real boundary.

### Exercise 8: Compliance evidence

**Suggested solution.** The tests do not establish compliance. They exercise a local simulation with explicitly omitted authentication, provenance, durable controls and legal assessment. The owner should use the worklist to identify applicable current primary sources and guidance, establish organisational and contractual responsibilities, map requirements to controls and evidence, record gaps, and obtain qualified review. The outcome depends on deployment facts and the applicable obligations, not solely on the test suite.
