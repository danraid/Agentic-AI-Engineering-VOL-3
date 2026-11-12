# Chapter 22: Worked solutions

### Exercise 1: Timeout and evidence

**Suggested solution.** At timeout, report `unknown`. The later missing record is also insufficient because the index may be stale. Continue the documented reconciliation process or escalate; do not report safe failure solely because the status query returned no record. If an authoritative, sufficiently current source later establishes the outcome, record that outcome with its evidence. If this occurs after the evaluation cut-off, preserve the original unresolved label and add a reconciliation label.

### Exercise 2: A paired policy comparison

**Suggested solution.** Use the same request, initial balances, permissions, service version, post-commit response-loss fault, tool budget and verifier. Change only the policy’s choice after `unknown`. In the hypothetical fixture, fresh-key retry can cause two commitments, while status-first queries the original operation. This controlled comparison does not estimate performance on a deployment population or establish the safety of a real status service.

### Exercise 3: A misleading invariant

**Suggested solution.** A wrong-direction transfer yielding A = 130 and B = −10 conserves the total. So can an unauthorised transfer yielding A = 95 and B = 25. The verifier needs expected account-level changes, an appropriate disposition and authorisation evidence, not conservation alone.

### Exercise 4: Permission changes

**Suggested solution.** It returns `refused`, because current authorisation is checked before replay lookup. Refusal does not reverse the earlier transfer and does not establish that no transfer occurred. The same current-authorisation rule applies to the laboratory’s status query. A production design may choose a different historical-status right, but must specify and test it separately.

### Exercise 5: Mutation-test the oracle

**Suggested solution.** For an unauthorised request, supply an observed `committed` event followed by a compensating event and unchanged final balances. The verifier should reject the run and flag the observed prohibited commitment. This checks the oracle’s event-count rule; it does not establish that the event record is complete.

### Exercise 6: Status freshness

**Suggested solution.** Add a deterministic status sequence, such as `unknown` followed by `completed`, to the environment. Give the status-first policy an explicit bounded retry rule and record each query and observation. Test both resolution within budget and exhaustion with final `unknown`. The policy must not create a new transfer key while waiting. The test should not assume that a real status system has the same consistency behaviour.

### Exercise 7: A document-agent contract

**Suggested solution.** An outcome condition is that the requested briefing is saved at the designated location. A path condition is that no unapproved confidential report was read. An unresolved case occurs when the save tool times out and there is no reliable way to determine whether the file was written. A final text-quality score alone cannot establish any of these conditions.

### Exercise 8: Zero observed unsafe events

**Suggested solution.** The bound is

\[
1-0.05^{1/100}\approx 0.0295,
\]

or about 2.95%. It may not describe deployment risk if cases are not representative, trials are dependent, hazards are absent from the suite, or instrumentation misses events. The calculation is a hypothetical statistical illustration, not an observed safety result.

### Exercise 9: Evaluator versioning

**Suggested solution.** Record both verifier versions and retain the original results. Where traces contain sufficient evidence, rescore the same runs under both versions and report differences as evaluator changes. Do not attribute a score change to the agent unless the agent or its conditions also changed and the comparison isolates that change. If old traces lack event evidence, mark the relevant checks unavailable rather than assuming they passed.

### Exercise 10: Concurrent delivery

**Suggested solution.** Two callers could both check that a key is absent before either records the result. The existing test runs calls sequentially and never exercises that interleaving. Against a suitable transactional test service, coordinate two same-key callers so that their submissions overlap, then inspect an independently queried durable record for one effect and a consistent stored result. Repeat with conflicting payloads and interruption around commitment. A durable uniqueness or locking mechanism must be coordinated with the transfer transaction. Adding threads to the in-memory teaching model alone does not establish that property, and passing tests remains evidence about tested conditions rather than a universal proof.

### Exercise 11: The event-count oracle

**Suggested solution.** No. The verifier counts `committed` events but does not compare their keys or payloads with the request. With matching final state and disposition, the count may satisfy its rule. Extend the case and event schema to include a canonical operation identity and payload, then independently check their correspondence. This still would not detect effects absent from the audit record.

### Exercise 12: Evidence tiers

**Suggested solution.** Claim 1 is supported by the checked FULLTEXT excerpt for [S01], within its conceptual scope. Claim 2 is suitable as broad context from the ABSTRACT-tier source [S13], not as evidence for detailed results. Claim 3 is unsupported under the chapter’s evidence rule: the packet supplies no checked FULLTEXT evidence for that result. Claim 4 is unsupported; no BOOK_FULLTEXT source is supplied. Bibliographic verification alone does not change any of these classifications.

### Exercise 13: Paired discordances

**Suggested solution.** Here \(b=5\), \(c=2\), so

\[
\widehat\Delta=(5-2)/20=0.15.
\]

The observed difference is 15 percentage points on those cases. Interpretation requires the case-selection process, dependence between cases, repeated-run behaviour, the verifier’s limitations and the deployment population. The seven discordant pairs are especially relevant to a paired analysis, but a deterministic convenience suite does not by itself justify population inference.
