# Chapter 26: Worked solutions

### 1. Scope a delegation

**Suggested solution.** Bind the authenticated analyst, organisation, task identifier, incident identifier, permitted operations and expiry. Specify export destinations and budget separately if export is needed. The agent should not inherit the analyst’s full cross-organisation authority merely because the analyst possesses it.

### 2. Identify the confused deputy

**Suggested solution.** The adapter, or the agent runtime acting through it, can become the deputy. It has legitimate service authority but may exercise that authority for an instruction originating in a lower-trust log. Separate evidence from instructions and authorise the actual read and destination using trusted task context.

### 3. Derive an effective authority

**Suggested solution.** Reading incident 42 lies in the intersection if all four sets permit it. Reading incident 41 is excluded by the task grant. Network export is excluded by the environment even if another layer would otherwise allow it. This conclusion depends on those restrictions being enforced rather than merely documented.

### 4. Challenge the invariant

**Suggested solution.** A sandbox writes the data to an output file, and an unmonitored notification service emails that file externally. The direct-export predicate remains correct, but not every disclosure passes through it. Complete mediation, an assumption of the induction argument, is false.

### 5. Bind approval to content

**Suggested solution.** Include a trusted immutable version identifier or content digest in the action representation. At execution, fetch the authorised content, verify its version or digest, and pass those exact bytes to the adapter. Protect the version source and approval store; a digest supplied only by the model is not proof of approval.

### 6. Compare sandboxing and egress control

**Suggested solution.** No. The report is an indirect output channel. Restrict sensitive inputs, treat the output according to its data sensitivity, and enforce destination and data-flow policy at the email boundary. Sandboxing and final-effect mediation address different links in the chain.

### 7. Analyse an uncertain outcome

**Suggested solution.** Not automatically: delivery may already have occurred. Keep the operation in an `unknown` state and retain its reservation. Reconcile through trusted provider evidence or escalate to an authorised operator. A retry requires understood idempotency semantics or another justified recovery decision.

### 8. Design a concurrency test

**Suggested solution.** Run both against the real transactional reservation store, synchronising immediately before reservation. Assert that at most one reservation commits and that the stored budget never becomes negative. Inject aborts and crashes, then verify durable recovery and actual effects. Repeated testing can find defects; it does not by itself prove all possible schedules safe.

### 9. Exercise the label branch

**Suggested solution.** The request is denied by the earlier `allowed_record` check. The label branch is never reached. The laboratory’s separate fixture changes the allowed record to `credentials`, supplies an approval and attempts export; the confidential label must then cause denial.

### 10. Separate evidence claims

**Suggested solution.** The record supports the claim that the extracted program’s tests passed under the recorded interpreter, platform and invocation. It does not establish concurrency safety, process isolation, real credential confinement, correct external delivery or production security. Those require additional evidence about the relevant implementation and environment.
