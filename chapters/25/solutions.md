# Chapter 25: Worked solutions

### 1. Identify an instruction’s authority

**Suggested solution.** The bank-detail instruction is email content and may be reported in the summary. It is not, by itself, authenticated authority to modify payment records. A separate verified business process should establish the supplier’s identity and authorise the change.

### 2. Map the refinement

**Suggested solution.** \(P\) contains the rule for interpreting capability fields; \(c\) binds \(C\) to the authenticated principal and task. The protected history or state represented by \(h_t\) contains the current approval status and count or reservation state \(n\). The proposal \(a_t\) supplies values to be checked. The concrete send rule is an instantiation of the general `Allowed` predicate.

### 3. Find the concurrency failure

**Suggested solution.** Atomic commitment fails. Reserve the quota and create a durable outbox entry in one transaction, then dispatch with a stable idempotency key. Test simultaneous requests, crashes before and after dispatch, retries, and reconciliation of unknown outcomes. The remote transport’s guarantees still limit any exactly-once claim.

### 4. Reason about combined detectors

**Suggested solution.** No. One per cent follows only if their misses are independent on the relevant attack population. If the same attacks defeat both, the joint miss rate is 10%. Evaluate joint outcomes, including adaptive cases, rather than multiplying marginal rates without justification.

### 5. Approve a corrected summary

**Suggested solution.** First, require renewed approval of the corrected artefact. This is straightforward to audit but adds delay. Secondly, apply a trusted deterministic normaliser before both approval and delivery. This reduces repeat review, but its specification and implementation become security-critical. Unrestricted model editing after approval is not covered by exact-body authorisation.

### 6. Compare disclosure controls

**Suggested solution.** The same mailbox can receive an authorised summary or prohibited payroll information. Source-level taint can track labelled inputs under specified propagation rules, but can over- or under-taint. A semantic policy states the desired flow restriction, but enforcing it for arbitrary paraphrase is difficult. Content classification screens the output but can miss or misclassify content. Human approval can bind a decision to the actual body, but reviewers can overlook derived secrets. Restricting access to payroll may remove the path more directly.

### 7. Extend the laboratory

**Suggested solution.** The host constructs `Scope.reports` from authenticated workflow state, not from report text. `read_allowed` checks exact task equality and membership in that host-created set. In a real system, the scope must also be protected from the model process and bound to stable resource identities.

### 8. Analyse evidence

**Suggested solution.** In the laboratory, `True` means the single-threaded mock appended the request to its in-memory list. It does not establish a real mail-service effect. In a deployed system, an allow decision, outbox insertion, transport acceptance and confirmed delivery are distinct events. Consult protected execution and reconciliation records for the claim being made.
