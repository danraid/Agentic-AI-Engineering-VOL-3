# Chapter 22: Exercises

### Exercise 1: Timeout and evidence

A transfer request times out. A later status query returns no record, but the service documentation says its status index can lag behind commitment. What should the agent report at timeout and after the query?

### Exercise 2: A paired policy comparison

Design a comparison between the laboratory’s fresh-key and status-first policies. Identify what is held fixed, the primary disagreement and one limitation.

### Exercise 3: A misleading invariant

A verifier checks only that the sum of balances remains 120. Give two incorrect outcomes that pass this check.

### Exercise 4: Permission changes

A request commits under Alice’s authority. Her permission is revoked before she retries the identical request. What does the laboratory return, and what does that result establish?

### Exercise 5: Mutation-test the oracle

Construct a case where final balances are unchanged but the trajectory violates the contract. What should the verifier do?

### Exercise 6: Status freshness

Modify the laboratory so that status becomes available only on a later query. How should the policy and budget be specified?

### Exercise 7: A document-agent contract

An agent searches reports and writes a briefing. State one outcome condition, one path condition and one unresolved case.

### Exercise 8: Zero observed unsafe events

A hypothetical team observes no unsafe events in 100 trials. Under the independent, identical Bernoulli assumptions in this chapter, calculate the one-sided 95% upper bound and explain two reasons it may not describe deployment risk.

### Exercise 9: Evaluator versioning

A new verifier begins rejecting runs with a prohibited intermediate event, although their final states are unchanged. How should a team compare results before and after the change?

### Exercise 10: Concurrent delivery

Why does the sequential duplicate-delivery test not establish exactly-once commitment under concurrent requests? Outline a laboratory extension.

### Exercise 11: The event-count oracle

For an authorised case, the supplied final balances and disposition match expectations, and the audit record contains one `committed` event with the wrong key. Does the laboratory verifier necessarily reject it?

### Exercise 12: Evidence tiers

Classify the following proposed claims as supported by checked FULLTEXT evidence, usable only as broad ABSTRACT-tier context, supported by a supplied BOOK_FULLTEXT source, or unsupported by the packet:

1. Traceability and transparency are among the pillars identified by the conceptual framework in [S01].
2. Agent evaluation should consider concerns beyond final task completion, with [S13] cited as context.
3. A particular numerical benchmark result stated in an abstract is established by checked full text.
4. A numerical claim attributed to a book not included in the packet.

### Exercise 13: Paired discordances

In a **hypothetical** comparison of 20 paired cases, B alone is accepted on five cases and A alone on two. Calculate the observed paired difference. What additional information is needed before treating it as a deployment estimate?
