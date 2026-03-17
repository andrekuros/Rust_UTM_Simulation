---
name: daidalus-consensus-avoidance
overview: Integrate DAIDALUS alert levels with a consensus-based multi-drone avoidance decision so that only the lowest-cost drones maneuver while maintaining well-clear requirements.
todos:
  - id: analyze-current-avoidance
    content: Locate and summarize current DAIDALUS-based avoidance logic and where maneuvers are chosen in the Rust simulator.
    status: pending
  - id: define-cost-model
    content: Design a simple but extensible cost function for deviation, delay, and maneuver aggressiveness, and expose it via a small API.
    status: pending
  - id: implement-pairwise-consensus
    content: Add a pairwise conflict resolver that selects which of two drones maneuvers (or both) based on total cost while respecting DAIDALUS bands.
    status: pending
  - id: integrate-simulator
    content: Wire the new consensus-based resolver into the main simulation loop where DAIDALUS alerts are processed.
    status: pending
  - id: evaluate-scenarios
    content: Run crossing and city scenarios comparing current avoidance vs consensus-based avoidance using plots and summary metrics.
    status: pending
isProject: false
---

### Goal

Integrate DAIDALUS-style detect-and-avoid alerts with a decentralized decision layer (inspired by CBBA) so that, for each detected conflict, the swarm selects the avoidance maneuver assignment with minimal global cost, often allowing only the lowest-cost drone(s) to deviate.

### High-level approach

- **Use DAIDALUS as the safety oracle**: Keep DAIDALUS (or your existing Well-Clear checks) as the module that determines conflict pairs and severity levels (preventive/corrective/warning) and, optionally, candidate maneuver bands per aircraft.
- **Add a consensus/cost layer on top**: For each active conflict pair or small conflict cluster, let involved drones propose avoidance options with associated costs; run a lightweight consensus/allocation step to choose which drones actually maneuver.
- **Preserve safety guarantees**: Ensure any selected assignment only uses maneuvers that are in the DAIDALUS-safe bands for all involved aircraft and respects timing constraints (e.g. react before tau threshold).

### Key design decisions

- **Decision granularity**
  - Per **conflict pair**: simplest – for each (i,j) with a DAIDALUS alert, decide whether i maneuvers, j maneuvers, or both, based on cost.
  - Per **conflict cluster**: more advanced – when aircraft share multiple conflicts (i-j, j-k, etc.), run allocation over a small set of drones simultaneously so assignments are globally consistent.
- **Cost model**
  - Combine factors like: path deviation from nominal route, delay to goal, fuel/energy, future conflict risk increase, and maneuver aggressiveness.
  - Normalize costs so they are comparable across drones; optionally weight by drone priority (e.g. manned vs unmanned, high-priority missions).
- **Triggering logic from DAIDALUS**
  - Low alert levels (preventive): allow simple heuristic (e.g. always have the more maneuverable / lower-priority drone move) without full CBBA.
  - Higher levels (corrective/warning): run the consensus-based allocation to minimize system-wide impact while still guaranteeing separation.

### Algorithm sketch (pairwise version)

1. **Conflict detection**
  - DAIDALUS flags pair (i,j) with alert level L and provides allowed maneuver bands for each.
2. **Local option generation**
  - Drone i computes 1–3 candidate maneuvers within its DAIDALUS bands (e.g. change heading, change speed, change altitude) plus a "no-maneuver" option, each with a scalar cost.
  - Drone j does the same.
3. **Feasible joint options**
  - Enumerate joint assignments such as: only i maneuvers, only j maneuvers, both maneuver with specific options.
  - Discard any joint assignment where either drone’s maneuver is outside its DAIDALUS safe bands or re-creates a near-term violation.
4. **Consensus/selection**
  - For just 2 drones, a simple exchange of their local costs and a deterministic tie-break rule (e.g. lowest ID wins) is sufficient; for 3+ drones, use a CBBA-style round where each drone bids for keeping its nominal path (high cost to deviate) and conflicts are resolved toward minimal global cost.
5. **Maneuver execution**
  - Apply the chosen maneuver(s) and feed updated trajectories back into the simulator / DAIDALUS for continuous monitoring.

### Relation to CBBA and similar work

- **Concept alignment**
  - CBBA is typically used for multi-task allocation (who does which task) using local bids and consensus. Your avoidance idea is analogous: the “tasks” are avoidance maneuvers or “keep-nominal”, and drones bid based on the cost of deviating.
- **Known patterns**
  - Multi-UAV literature includes CBBA-based **deconfliction and scheduling**, where routes or tasks are adjusted cooperatively to avoid conflicts while maximizing team reward.
  - Safety systems often use a **hierarchical structure**: DAIDALUS for pairwise well-clear logic, with a higher-level coordinator resolving which aircraft maneuvers when multiple constraints interact.
- **Feasibility**
  - For small conflict clusters (2–5 drones), the computation is light and can be done in real time.
  - The approach is conceptually sound: preserve DAIDALUS for correctness, and use consensus only to choose among DAIDALUS-approved safe options according to a global cost metric.

### Implementation plan in this repo

- **1. Analyze current avoidance logic**
  - Inspect where DAIDALUS alerts are consumed and how current heading/speed/altitude changes are chosen in the Rust simulator.
  - Identify the place where pairwise conflicts are mapped to concrete maneuver commands.
- **2. Define a cost function API**
  - Introduce a small struct (e.g. `AvoidanceOption { maneuver: ..., cost: f64 }`) and a trait or helper that, given the current state and a candidate maneuver, evaluates cost.
  - Start with a simple cost (path deviation + delay) and keep it easily extensible.
- **3. Add a consensus allocator**
  - For the pairwise case, implement a minimal allocator that, given two drones’ option sets, selects the joint assignment with lowest total cost subject to DAIDALUS feasibility.
  - Abstract the interface (e.g. `resolve_pair_conflict(i_state, j_state, alert_info) -> (opt_i, opt_j)`) so it can later be extended to 3+ drones or a full CBBA implementation.
- **4. Integrate with the simulator loop**
  - When DAIDALUS raises an alert, instead of immediately applying a fixed avoidance rule, call the new allocator.
  - Ensure that in the absence of consensus (e.g. timeout, no feasible solution) you fall back to a conservative default (e.g. both perform current DAIDALUS advisory).
- **5. Testing and evaluation**
  - Re-run existing crossing scenarios (default vs stronger avoidance) and log:
    - Which drone(s) maneuvered.
    - Total path deviation and delay per drone.
    - Number of conflicts and lowest separation achieved.
  - Compare metrics vs the current rule-based avoidance; generate updated 2D/3D path plots and histograms.

### Next steps

If you confirm this direction, we can next:

- Pin down the exact cost terms you care about most (e.g. mission time vs safety margin vs fuel), and
- Implement the pairwise allocator in the Rust simulator, keeping the design modular so a more complete CBBA-like scheme can be plugged in later.

