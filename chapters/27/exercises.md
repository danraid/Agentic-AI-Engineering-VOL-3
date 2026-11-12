# Chapter 27: Exercises

Use the canonical file **`oversight_lab.py`** and the `unittest` command above for laboratory exercises. Modify a copy so that the original baseline remains available.

### 1. Specify a delegation

**Exercise.** A support agent may reset passwords but must not change an account’s registered recovery address. Specify the principal, permitted action, prohibited action, evidence and escalation condition.

### 2. Calculate a review threshold

**Exercise.** In the expected-loss model, let \(p=0.01\), \(L=£5{,}000\), \(q=0.2\) and \(d=£4\). What is the largest review cost \(c\) for which review has strictly lower expected cost?

### 3. Distinguish binding from authentication

**Exercise.** Inspect `public_digest`, `insecure_digest_gate` and `test_public_digest_is_forgeable`. Why does the passing test demonstrate a failure? What additional assumption is made by the HMAC fixture?

### 4. Extend the concurrency test

**Exercise.** In a copy of `run_tests`, change the initial budget to £800 while retaining two distinct approved £360 orders. State the invariant and expected balance. Then use the same order identifier and identical details for both requests.

### 5. Design recovery after a timeout

**Exercise.** A supplier accepts an order, but the response times out before the purchasing service records success. The supplier supports neither idempotency keys nor a reliable status API. What should happen?

### 6. Challenge an assurance claim

**Exercise.** A team passes the local tests and claims: “No unauthorised purchase can occur.” Identify three missing assumptions and suitable evidence for each.

### 7. Add a missing field

**Exercise.** The full hypothetical policy requires delivery to the registered laboratory, but `reserve` has no destination parameter. In a copy of the file, identify all places that must change to bind and check a destination.
