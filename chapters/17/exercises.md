# Chapter 17: Exercises

### Exercises

1. **Belief update.** In the hypothetical sensor example, change the prior probability of low stock to \(0.1\), retaining the same sensor assumptions. Calculate the posterior after a low report. Under the original loss assumptions, should the system raise an alarm?

2. **Freshness boundaries.** With \(t_{\text{now}}=1{,}000\) and a maximum age of 60 seconds, classify observations timestamped 940, 939 and 1,001. State one reason why an accepted timestamp does not establish that the quantity is correct.

3. **Approval binding.** An approver accepts five units of `widget-A` for `intent-17`. The runtime later proposes six units under the same intent. Explain the binding, authentication and authorisation questions separately.

4. **Matching digest.** An attacker chooses a valid-looking proposal and computes its digest using `approval_token`. Why can the digest match without proving that an authenticated and authorised person approved the transaction?

5. **Architectural decision.** An organisation wants to replace the deterministic quantity rule with a language model because users describe stock needs in varied language. Choose an architecture for interpretation, calculation and purchase approval. Justify the trust boundaries and identify one disadvantage of your design.

6. **Crash recovery.** A runtime persists `SUBMITTING`, sends a request and crashes before recording a response. The supplier supports a status query keyed by intent but does not promise idempotent writes. Give a recovery procedure for confirmed, conclusively absent and inconclusive results. State the assumptions needed to treat absence as conclusive.

7. **Concurrent workers.** Two workers read an approved intent at the same time. Describe a local coordination mechanism and explain why it is not an end-to-end exactly-once guarantee.

8. **Extend the laboratory.** Add an authenticated-source field and a controllable clock abstraction to the observation interface. List tests for item identity, time boundaries and source handling. What can a fake authentication test establish, and what can it not establish?

9. **Evaluation design.** Propose three outcome measures for an agent that prepares purchase requests. Explain why final-answer accuracy alone is inadequate and specify a denominator for each measure.
