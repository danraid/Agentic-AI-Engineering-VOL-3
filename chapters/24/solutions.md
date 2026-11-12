# Chapter 24: Worked solutions

### 1. Specify a repository migration

**Suggested solution.** Preconditions could require a clean repository at a recorded commit and an approved target dependency version. Acceptance checks could require a successful build, unchanged protected tests passing, and review of the dependency and source diff against the requested scope. Add compatibility or integration tests for important public behaviours. None of these checks alone proves equivalence.

### 2. Analyse a longer workflow

**Suggested solution.** The ten-step probability is approximately \(0.737\); the twenty-step probability is

\[
0.97^{20}\approx0.544.
\]

The calculation motivates removing unnecessary steps, but cannot predict real performance without validating the independence and constant-probability assumptions. Removing an essential verification step could reduce the number of actions while making the overall workflow less safe.

### 3. Trace a replay

**Suggested solution.** The retry returns `{"invoice_id": "INV-1", "version": 1}`. The current ledger version remains 2. The saved receipt describes the first commit; it is not a current-state response.

### 4. Repair an unsafe check order

**Suggested solution.** `test_two_approvals_and_old_replay` fails. At retry time the ledger version is 2, while the original request carries version 0. The implementation rejects the retry before discovering that `op-1` already has a saved result. Restoring replay lookup before the version check fixes this case. Production must also verify that the saved fingerprint matches the retry and that the caller may access the result.

### 5. Design a concurrent transition

**Suggested solution.** Within a transaction, reserve each key under a unique constraint and perform a conditional update requiring the expected version and pending status. Exactly one update should affect the qualifying invoice row; the other transaction must abort or record a rejection according to the service contract. The winning invoice update and receipt must commit together. Test the actual database’s isolation, locking and retry behaviour rather than relying on application-level reads.

### 6. Handle an unknown GUI outcome

**Suggested solution.** Do not click again immediately or report failure as fact. Preserve the invoice identifier, time and observed action; attempt an authorised refresh or query of the most authoritative available record. If the state remains uncertain, stop and request reconciliation. The reviewer needs to know that approval may already have occurred. If the application offers no reliable way to resolve the ambiguity, the workflow must document that limitation and may require manual handling.

### 7. Extend the laboratory

**Suggested solution.** Give the new operation a distinct key and expected version `1`; its result should contain version `2`. Retrying `INV-1` with its original key and original expected version should return its saved version-1 result, while the current ledger version remains `2`. Also assert that the fourth invoice is approved and that unrelated records and amounts are unchanged. This extends the model’s tests but does not add persistence or concurrency guarantees.

### 8. Evaluate batching

**Suggested solution.** Define the four intended transitions and their invariants first. Run matched scenarios with the original and batched workflows, injecting a failure after each intermediate action. Inspect authoritative final state, unintended effects, recoverability and whether uncertainty is reported accurately. Measure latency, tool calls and reviewer effort as separate outcomes. Accept batching only for the tested contract if intermediate failures can be detected and handled without violating required invariants; happy-path success alone is insufficient.
