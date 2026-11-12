# Chapter 19: Exercises

### Exercise 1: Threshold boundary

A GBP request is for exactly £100. Does it require approval? What does the laboratory do with 10,000 minor units labelled `USD`?

### Exercise 2: An unsafe transition

A supervisor times out while submitting `R1` and creates a new operation key for the retry. Which property is endangered?

### Exercise 3: Approval binding

A reviewer approves `R2` version 1 for £150 to supplier B. Before dispatch, the payee is changed to supplier C. What must happen?

### Exercise 4: Ambiguous absence

Two seconds after a timeout, a bank lookup returns no matching record. May the supervisor mark the payment rejected and submit a replacement?

### Exercise 5: Retry assumptions

The probability derivation assumed independent attempts. Give a counterexample and explain how the response should differ from an immediate retry.

### Exercise 6: Concurrent dispatchers

Two workers read the same pending outbox entry and both send it. Propose controls and explain their limits.

### Exercise 7: Approval expiry

An approval expires at noon. The supervisor checks it at 11:59:59 but dispatch occurs after noon. What must the design decide?

### Exercise 8: Extend the laboratory

The cross-version test uses a timeout before the fake bank effect. Add a test using `fault="after"`. What should happen before and after reconciliation?

### Exercise 9: Evaluate two architectures

How would you compare a single-agent payment assistant with a specialist-agent workflow?
