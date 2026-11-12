# Chapter 18: Worked solutions

### 1. Allocation perturbation

**Suggested solution.** \(A\to X,\ B\to Y\) costs \(2+8=10\). \(A\to Y,\ B\to X\) costs \(5+4=9\), so the latter wins. Independent selectors choose \(A\) for both packages because \(2<4\) and \(5<8\); that violates the one-package capacity constraint.

### 2. Duplicated evidence

**Suggested solution.** No. Copying a reading does not create a second independent observation. The posterior remains \(2/3\). The value \(16/17\) requires two conditionally independent positive readings with the specified likelihoods. An observation identifier and provenance allow the recipient to recognise the common source.

### 3. Lease boundary

**Suggested solution.** Expiry is \(5+4=9\). The validity interval is \([5,9)\), so a request at time \(8\) is eligible and one at time \(9\) is rejected. A deployment must also define which clock is authoritative and how clock failure is handled.

### 4. Separate delivery from physical completion

**Suggested solution.** The request may never have reached the resource; alternatively, the release may have occurred and the response may have been lost. The vehicle cannot infer which from silence alone. It should retry the same operation identifier if the resource supports safe idempotency, or enter reconciliation. It should not invent a new operation identifier and assume that a missing response means no physical action occurred.

### 5. Operation identifiers

**Suggested solution.** The first request is `duplicate`: the ledger recognises the accepted identifier and payload. The second is `rejected`: it is a new request against a completed task. The third is `conflict`: an accepted identifier has been reused with different fields. In a real service, identifiers must be appropriately scoped, authenticated and durably recorded.

### 6. Capacity and concurrency

**Suggested solution.** Before assigning a package, inspect all other records and reject if one has the same vehicle, status `active`, and expiry later than the current authoritative time. Completed and expired records do not count as active leases under that simplified rule. However, two concurrent calls could both scan before either writes, then both assign work to the same vehicle. The scan and write must therefore be one serialised transaction or an equivalent atomic operation.

Expiry also does not prove that physical work stopped. A deployment may need to reserve capacity until uncertain work is reconciled, even if the software lease has expired.

### 7. Evaluate an architecture

**Suggested solution.** Use the same task instances, available information, resource constraints, safety rules and evaluation procedure as far as possible. Where feasible, hold agent count and model capability fixed while varying topology. Report allocation cost, completion and unsafe-attempt rates, latency, message and compute costs, partition behaviour, reconciliation time and human workload. Include common-source errors: agreement among agents sharing faulty evidence is not independent verification. Report failures and uncertainty rather than only successful demonstrations.

### 8. Crash window

**Suggested solution.** After restart, the server may find no deduplication record and perform the effect again. The design must coordinate durable authority, the actuator and evidence of physical state. Depending on the device, that may require an actuator-side operation log, an independently verifiable state check or human reconciliation. A database transaction alone does not make a separate mechanical action atomic.

### 9. Optional capacity extension

**Suggested solution.** In `assign`, after checking the target package and before writing the new record, scan the other task records. Return `None` if another record has the requested vehicle, is active and has `expiry > self.time`. Test both rejection while the first lease is active and acceptance after it expires or completes. This repairs only the sequential model: the scan and write still need atomic serialisation in a concurrent service. A further test should attempt conflicting assignments concurrently against an implementation that actually provides a transaction or equivalent synchronisation mechanism.
