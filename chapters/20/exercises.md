# Chapter 20: Exercises

### 1. Construct a dependency DAG

**Exercise.** A workflow validates an address, retrieves product details, reserves stock and charges a card. Product details determine price; successful reservation and address validation are required before charging. Draw the dependencies and identify the safe initial overlap.

### 2. Calculate a critical path

**Exercise.** Four independent calls each take a hypothetical \(0.5\) seconds, followed by a \(0.2\)-second merge. Find the ideal concurrent duration and identify two reasons the observed duration could differ.

### 3. Calculate retry load

**Exercise.** A service receives six new jobs per second. Each attempt independently needs another attempt with probability \(0.4\), with at most three attempts. Estimate the attempt rate. What important failure pattern does the model omit?

### 4. Interpret nominal multi-worker load

**Exercise.** A system receives \(0.6\) jobs per second; mean service time is \(3\) seconds and there are three equivalent workers. Calculate offered traffic per worker. Does the result determine mean waiting time?

### 5. Design a transition table

**Exercise.** Give a permitted transition and evidence requirement for each of: dispatch, verified payment, confirmed failure, uncertain outcome and undispatched cancellation.

### 6. Reconstruct an adversarial interleaving

**Exercise.** A claims epoch 4 until time 10 and sends a payment. At time 11 B claims epoch 5. A receives a receipt and attempts acknowledgement at time 12. Explain the local result and the remaining remote risk.

### 7. Decide on retention

**Exercise.** A provider retains keys for 24 hours from first receipt of a request. A payment response is lost, and the queue presents the same operation 25 hours later. Is reusing the key sufficient to justify an automatic retry?

### 8. Test evidence validation

**Exercise.** Design a negative test for a current worker that presents a receipt for the wrong currency. State what should happen and whether the supplied laboratory already enforces it.

### 9. Scope effect guarantees

**Exercise.** A provider guarantees at most one charge-ledger entry for each retained key but sends a notification for every accepted request. Two equivalent requests are accepted. What can be inferred about charge entries and notifications?

### 10. Strengthen the expiry experiment

**Exercise.** Modify the laboratory design so that loss of a deduplication record can demonstrate two distinct durable simulated effects. What must remain after the mutation?
