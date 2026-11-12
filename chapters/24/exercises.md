# Chapter 24: Exercises

### 1. Specify a repository migration

An agent must upgrade a dependency while preserving public behaviour. State two preconditions and three acceptance checks.

### 2. Analyse a longer workflow

Assume independent step success probability \(p=0.97\). Compare ten steps with twenty.

### 3. Trace a replay

Starting from a fresh `Ledger`, approve `INV-1` with `("op-1", 0)`, approve `INV-2` with `("op-2", 1)`, and retry the first request. What does the retry return, and what is the current version?

### 4. Repair an unsafe check order

Suppose the version comparison is moved before the operation-key lookup. Which existing test detects the defect, and why?

### 5. Design a concurrent transition

Two workers submit different keys for the same pending invoice at the same version. Describe a database-level design that prevents both from succeeding.

### 6. Handle an unknown GUI outcome

A legacy GUI displays a spinner after an approval click, then disconnects. No idempotency key is available. The agent can read the invoice list, but it may be delayed. What should it do?

### 7. Extend the laboratory

Add a fourth pending invoice below the limit. Approve it after `INV-1`, then retry the first operation. What should be asserted?

### 8. Evaluate batching

A team proposes batching four GUI actions to save model calls. Construct an acceptance test for deciding whether the optimisation is safe.
