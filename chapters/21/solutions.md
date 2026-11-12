# Chapter 21: Worked solutions

**1. Freshness.** `(True, 0, 1, "owner")` is accepted because \(0\leq1\), although the draft is stale under equality. The change alters the requirement. Accepting an older version would need a separately validated definition of freshness.

**2. Safety and progress.** The gate satisfies the send-safety implication vacuously because no send passes through it. It may fail the goal of providing support or a conditional eventual-disposition requirement. An allowed-path test prevents this trivial implementation from satisfying the whole test suite unnoticed.

**3. Unknown consent.** Do not commit automatically; create a review task. The operational contract must define durable storage, access control, ownership, expiry, escalation and a terminal disposition. A set in memory establishes none of these.

**4. Race and binding point.** If `send` denotes the 10:02 event and consent is invalid immediately before it, the property fails. A 10:00 check does not prove otherwise. If policy instead binds permission at a local commitment, the specification must say so and separately address later external delivery.

**5. Retry.** Not necessarily. In the toy, `duplicate` acknowledges an existing commitment and adds no new dictionary entry. It is not a new commitment. In a real integration, however, a retry might resubmit externally; its actual effects and idempotency contract must be examined.

**6. Audit oracle.** Test that an approved schema rejects unexpected fields, and test representative exception and application-log paths with sensitive inputs. Also inspect transformations such as encoding or truncation. Even these tests cannot establish absence of all leakage across every downstream system; access controls and broader information-flow analysis are needed.

**7. Bypass.** The proof’s premise that every new commitment passes through the conditional authority is false. Remove or restrict the credential, enforce queue access at the receiving boundary, and inventory other paths. Then gather evidence that the controls are active; changing a diagram alone is insufficient.

**8. Consent scope.** Global `valid` conflates permission to prepare with permission to disclose. Represent authenticated subject, purpose, recipient, category, time and status; evaluate the disclosure request against authoritative records. The resulting rule still needs stakeholder approval and correct enforcement.

**9. Distributed boundary.** One design commits an outbox intent after a local consent check, then submits it with provider idempotency and reconciliation. It protects a local boundary but may deliver after withdrawal. Another rechecks immediately before provider submission and cancels pending work on withdrawal. This narrows the window but cannot guarantee consent at delivery if the provider cannot enforce it. Each design needs an explicitly accepted binding point.

**10. Assurance argument.** Claim: every *new local commitment in the toy sequential model* occurs when its selected consent value is valid. Evidence: the `commit` branch checks that value before insertion; the withdrawal test exercises a valid-to-invalid sequence. Defeater: the stale-injection test demonstrates that selecting an obsolete value can permit commitment after withdrawal. Neither evidence item proves scoped consent, atomic database behaviour or complete mediation in deployment.
