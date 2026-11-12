# Chapter 28: Exercises

All scenarios and numerical values in these exercises are **hypothetical**.

### Exercise 1: Scope and purpose

A user belongs to tenant `north` and is assigned to case `R1`. The user requests its repair summary for marketing. Evaluate the single-record `Read` predicate. Would changing only the purpose to `repair` establish that a real request is authorised?

### Exercise 2: Labels and provenance

A draft combines a `PUBLIC` summary and an `INTERNAL` note. Derive its label. Suppose a model then rewrites it as a short, apparently harmless sentence. May the gateway automatically classify that sentence as `PUBLIC`?

### Exercise 3: Approval, concurrency and recovery

Two workers simultaneously read an unused approval and both attempt to send the same message. Why does the laboratory’s `used` flag not prevent both sends in a concurrent implementation? Propose a stronger design and identify a remaining uncertainty.

### Exercise 4: Proportionate evidence

An investigator asks why a proposed message was denied. List useful evidence that need not include the full resident history. Give one privacy limitation of that evidence.

### Exercise 5: Policy change

A message was approved under policy `v1`; before execution, `v2` prohibits its destination. What should happen to the queued job, and what does the laboratory actually demonstrate?

### Exercise 6: Probability and assumptions

Assume two independent transmissions, each with event probability \(0.02\). Calculate the probability of at least one event. Explain why this does not establish the risk of the housing deployment.

### Exercise 7: Forged authority

The laboratory accepts a directly constructed `Draft("Access code 4821", "PUBLIC")` after a fixture approval. Identify the defect and explain why rejecting extra request fields in `untrusted_send` is not a complete repair.

### Exercise 8: Compliance evidence

A team has passed every laboratory test and asks whether its UK deployment is compliant. What answer should the governance owner give, and what should be assembled next?
