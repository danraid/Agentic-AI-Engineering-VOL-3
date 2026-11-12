# Chapter 20: Worked solutions

### 1. Construct a dependency DAG

**Suggested solution.** Begin address validation and product retrieval concurrently. Draw an edge from product retrieval to reservation. Draw edges from reservation and address validation to charge; include price validation and authorisation as additional prerequisites. The overlap is safe only if the reads’ freshness and permissions meet the business rules. Reservation and address validation can overlap once product details are available.

### 2. Calculate a critical path

**Suggested solution.** The ideal duration is \(0.5+0.2=0.7\) seconds. Scheduling overhead, finite connections, contention, rate limits and variable call durations can increase it. If the merge can proceed with partial results, that is a different dependency and completion policy.

### 3. Calculate retry load

**Suggested solution.** Expected attempts per job are \(1+0.4+0.4^2=1.56\). The expected attempt rate is \(6\times1.56=9.36\) attempts per second. The calculation omits correlated failures: during a provider outage, many jobs may retry together. It also assumes a constant retry probability and does not account for deadlines or back-off.

### 4. Interpret nominal multi-worker load

**Suggested solution.** Nominal load is \((0.6\times3)/3=0.6\). It does not determine waiting time. A multi-server waiting model needs additional assumptions about arrivals and service, and shared provider limits or heterogeneous workers may dominate. Do not substitute the M/M/1 waiting formula.

### 5. Design a transition table

**Suggested solution.**

| Event | Transition | Required basis |
|---|---|---|
| Dispatch may begin | `PENDING` → `IN_DOUBT` | Valid intent, authorisation and current dispatch ownership |
| Payment verified | `IN_DOUBT` → `SUCCEEDED` | Evidence validated against the intended key and payload |
| Final failure verified | `IN_DOUBT` → `FAILED_CONFIRMED` | Provider evidence whose contract establishes final failure |
| Outcome unresolved | `IN_DOUBT` → `MANUAL_REVIEW` | Insufficient evidence or authority for safe automation |
| Cancellation before dispatch | `PENDING` → `CANCELLED` | Conditional proof that no dispatch has begun and cancellation is authorised |

A real table must also define who may make each transition, transaction boundaries and whether review can later be resolved.

### 6. Reconstruct an adversarial interleaving

**Suggested solution.** The conditional acknowledgement rejects A: the current owner and epoch are B and 5, and A’s lease has expired. The receipt may still be valuable evidence for B or a reconciler. The local fence does not prevent A from having sent the payment, nor does it stop an unfenced remote request. Stable provider idempotency or another remote control is still needed.

### 7. Decide on retention

**Suggested solution.** No. The provider may have discarded the association and may treat the same key as a new operation. Seek evidence whose documented authority and freshness can establish the outcome; otherwise escalate. An automatic retry window must be shorter than the applicable retention window with suitable allowance for uncertainty. A new key would not solve the problem.

### 8. Test evidence validation

**Suggested solution.** Submit an authorised `GBP` intent, claim it and mark it `IN_DOUBT`. Present structured evidence with the matching key and amount but currency `EUR`. A validating implementation should reject the evidence and leave the job and outbox without a success acknowledgement, preferably recording the discrepancy for investigation. The supplied laboratory does not enforce this: its `acknowledge` function accepts an opaque string. Adding only a test without adding validation would expose the defect, not repair it.

### 9. Scope effect guarantees

**Suggested solution.** Under the stated provider assumptions, \(E_{\mathrm{charge}}(k)\leq1\). The two accepted requests produce two notifications under the stated notification rule. The charge guarantee says nothing about notification deduplication. If the business requires one notification, that effect needs its own identity and control.

### 10. Strengthen the expiry experiment

**Suggested solution.** Separate the provider’s key-to-result table from an append-only simulated effect ledger. On a new acceptance, insert an effect with a distinct effect identifier and associate the key with that result atomically. On an equivalent repeat while the key is retained, return the existing result without inserting another effect. Delete only the key association to model expiry; the first ledger entry must remain. A subsequent acceptance can then insert a second distinct ledger entry, which the test should count and inspect. The example remains a simulated provider, not evidence about a real service.
