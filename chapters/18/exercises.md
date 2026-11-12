# Chapter 18: Exercises

### 1. Allocation perturbation

Using the canonical matrix, change only \(c_{BY}\) from \(3\) to \(8\). Which feasible allocation wins? Would independent package-by-package choices be feasible?

### 2. Duplicated evidence

Two agents each report the same original positive sensor reading from the blockage example. Is the posterior \(16/17\)?

### 3. Lease boundary

A lease begins at logical time \(5\) with duration \(4\). Assuming all other checks pass, is a new request eligible at times \(8\) and \(9\)?

### 4. Separate delivery from physical completion

A vehicle sends a release request and receives no response. List two possible world states and a safe next step.

### 5. Operation identifiers

After an accepted `op-1`, a client sends the same payload under `op-1`, then under `op-2`. It also sends a different payload under `op-1`. Explain the laboratory responses.

### 6. Capacity and concurrency

Sketch a capacity check for the laboratory. Why is a simple scan insufficient in a concurrent service?

### 7. Evaluate an architecture

Design a comparison between a central coordinator and decentralised proposals. What should be controlled and reported?

### 8. Crash window

A physical release occurs, but the server crashes before recording its operation identifier. Why is retrying dangerous?

### 9. Optional capacity extension

Modify the laboratory so that a vehicle cannot receive a second unexpired active assignment. Preserve the existing tests, then remove the `expectedFailure` marker only when the formerly failing assertion is intended to pass. What further test would you add?
