# Chapter 27: Worked solutions

### 1. Specify a delegation

**Suggested solution.** The organisation delegates password resets after verification through an independent identity service. The reset tool denies recovery-address changes and routes them to a separate authorised process. Record the account identifier, verification result, policy version and outcome, minimising sensitive data. Escalate missing or contradictory verification evidence rather than allowing the agent to substitute a conversational claim.

### 2. Calculate a review threshold

**Suggested solution.** Avoided expected loss is

\[
pL(1-q)=0.01(5000)(0.8)=£40.
\]

Thus \(c+£4<£40\), or \(c<£36\). At exactly £36 the model gives equal expected costs. The answer does not override a mandatory review rule.

### 3. Distinguish binding from authentication

**Suggested solution.** The digest is computable from public action data, so an unauthorised caller can supply the matching value without a human decision. The passing assertion confirms that the deliberately unsafe gate accepts the forgery. The HMAC fixture instead assumes that the signing key is held by a trusted service which issues tokens only after valid human authentication and authorisation. The code does not enforce that assumption.

### 4. Extend the concurrency test

**Suggested solution.** With distinct identifiers, both reservations may succeed and the balance must be

\[
£800-£360-£360=£80.
\]

With the same identifier and details, one request creates the reservation and the other returns `ALREADY_RESERVED`; the balance is £440. The first test concerns budget isolation. The second concerns idempotency. Neither proves correctness under all schedules or distributed failures.

### 5. Design recovery after a timeout

**Suggested solution.** Mark execution **unknown**, retain the reservation and route the case to an authorised operator with the proposal, submission time and available evidence. Do not automatically retry or release funds merely because the response was lost. The operator should seek independent confirmation through an agreed channel and record the resolution. An unresolved commitment needs a documented exception process and owner.

### 6. Challenge an assurance claim

**Suggested solution.**

1. **No bypass:** the agent cannot reach the supplier or budget service around the gateway. Examine credentials, network paths and access-control tests.
2. **Trusted approval:** only an authenticated, authorised reviewer can cause the signer to issue a token. Test identity, role changes, signer access and key protection.
3. **Faithful external execution:** the supplier receives and executes the approved action only once. Test request construction, idempotency where supported, status handling and reconciliation.

Additional assumptions concern policy correctness, state integrity, clocks, incident response and reviewer capacity. Local test success cannot establish them.

### 7. Add a missing field

**Suggested solution.** Add destination to the proposal accepted by `reserve`, the hard-policy check, the approval payload and expected payload in `approval_valid`, and the reservation record used for idempotency comparisons. Update `issue_test_approval` and existing calls. Add tests for an unapproved destination and for a destination changed after approval. The invariant is that neither an approval for another destination nor reuse of an identifier with changed destination permits a new reservation. A production design must also obtain the registered address from an authoritative source.
