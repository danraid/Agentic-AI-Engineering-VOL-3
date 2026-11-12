# Chapter 26: Exercises

### 1. Scope a delegation

An analyst may read all records in two organisations. A task concerns one incident in one organisation. What should the task delegation contain?

### 2. Identify the confused deputy

A retrieved log asks the agent to upload a configuration file. The agent’s adapter holds a credential that can read and transmit that file. Which component can become a confused deputy, and why?

### 3. Derive an effective authority

A user may read incidents 41 and 42. The task grant permits only incident 42. The tool can read both, while the environment denies all network export. Which operations lie in the intended intersection?

### 4. Challenge the invariant

Assume the monitor correctly rejects direct exports of confidential records. Give a counterexample in which confidential data still leaves the organisation.

### 5. Bind approval to content

How would you extend the laboratory so that approval covers the record version as well as the recipient?

### 6. Compare sandboxing and egress control

A code sandbox has no direct network access but writes a report that another tool can email. Is exfiltration impossible?

### 7. Analyse an uncertain outcome

An export adapter times out and the provider’s status endpoint is unavailable. Should the system release the budget and retry?

### 8. Design a concurrency test

Two workers attempt different operation identifiers against a one-export budget. What must a production test check?

### 9. Exercise the label branch

Why does a test that requests `credentials` under the original task scope not establish that the confidential-label export check works?

### 10. Separate evidence claims

CI records that all laboratory tests passed. Which conclusions are justified, and which are not?
