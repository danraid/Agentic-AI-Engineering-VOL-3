# Chapter 17: Worked solutions

**1.** Bayes’ rule gives

\[
P(L\mid\text{report low})
=\frac{0.8(0.1)}{0.8(0.1)+0.2(0.9)}
=\frac{4}{13}\approx 0.308.
\]

The alarm threshold remains \(0.2\), so an alarm is preferred under the stated losses. The result depends on the assumed prior, sensor probabilities and loss model; it does not authorise a purchase.

**2.** Their ages are 60, 61 and \(-1\) seconds. The first is accepted at the boundary, the second is too old and the third is rejected as future-dated. An accepted timestamp could accompany a stale cached value or a fresh but inaccurate measurement.

**3.** The original approval is not bound to the changed quantity, so the changed proposal requires renewed approval or an explicitly authorised alternative. Even a correctly bound digest does not establish who approved it. Authentication must identify the approver; authorisation must establish that the identified person had the relevant permission.

**4.** The digest function is public and has no secret or trusted identity assertion. Matching it shows only that the supplied digest corresponds to the chosen representation under the function. It does not show who created it, whether that person approved anything, or whether they had authority. A trusted approval mechanism must establish those facts separately.

**5.** One defensible design uses the model to interpret the user’s request into a candidate structured item and goal. Deterministic code validates the item, obtains a scoped observation, applies the approved quantity rule and constructs the transaction. A trusted approval service authorises the exact material terms; a guarded purchasing adapter submits them. This retains flexibility in interpretation without granting the model purchasing credentials. A disadvantage is that ambiguous or novel requests may require clarification or a rule change rather than being handled autonomously. The design also needs testing against misinterpretation and malicious retrieved text.

**6.** Preserve the original intent and treat the outcome as potentially unknown. Query the supplier’s authoritative status service. If it confirms the exact order, validate the evidence and record confirmation. Treat absence as conclusive only under a trustworthy contract with sufficient consistency and scope to rule out delayed or concurrent processing. Even then, follow the organisation’s approved recovery procedure: absence itself neither authorises resubmission nor creates an idempotent write contract. If the result is inconclusive, retain **UNKNOWN** and escalate rather than blindly retrying.

**7.** Use an atomic conditional transition or unique database constraint so that one worker claims the approved intent. This prevents duplicate local claims under that database’s guarantees. It does not prevent a duplicate from another client or resolve a crash after the supplier acts; remote deduplication and reconciliation are still needed.

**8.** Test matching and mismatching item identifiers, age exactly at the limit, one unit beyond it, future timestamps, malformed times and clock assumptions. Test that an untrusted or missing source is rejected and that an accepted source is associated with the correct observation. A fake can test local handling of a simulated identity result; it cannot establish the security of a real identity provider, transport, credentials or deployment configuration.

**9.** Examples include: confirmed valid requests divided by eligible requests; unauthorised submissions divided by all submission attempts; and unresolved outcomes divided by all consequential submissions. Also measure human-review workload and latency. Final-answer accuracy can be high while the system submits an unauthorised order, duplicates an effect or falsely reports confirmation.
