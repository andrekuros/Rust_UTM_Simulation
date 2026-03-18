# xTM Experiments and Rust/DAIDALUS Integration Analysis

## 1. Python Experiment Scenarios (testeprimordial series)

All five scripts simulate **8 hours** of drone operations inside a geofenced area around **Sao Jose dos Campos (SJC)**, using lat/lon geodesic coordinates, 1-second timesteps, and spatial hashing for efficient proximity checks.

### 1.1 Scenario 1 — Baseline: Blind Flight (No DAA, No xTM)

**File:** `testeprimordial1.py`

- **Purpose:** Establish a safety baseline by measuring how many near-collisions occur when drones fly with **no awareness of each other** — no DAA, no centralized traffic management.
- **Drone model:** Random origin/destination within SJC geofence; takeoff, cruise at 30–50 m AGL at 15.3 m/s, landing, 5-min idle, repeat.
- **Collision metric:** **MACproxy** — unique drone pairs breaching 20 m horizontal / 10 m vertical separation.
- **Scale sweep:** 5 to 150 drones (step 5), each run independently via multiprocessing.
- **Key output:**
  - `grafico_macproxy_cenario1.png` — MACproxy count vs drone density ("chaos curve").
  - `log_consolidado_macproxy.json` — detailed collision log per density level.
  - 3 playback JSONs (low / medium / high density) containing 5-minute critical clips.

### 1.2 Scenario 2 — DAA Only (No xTM)

**File:** `testeprimordial2.py`

- **Purpose:** Show how a **reactive DAA layer alone** (without strategic traffic management) affects safety and route efficiency.
- **DAA technique:** Each drone scans for the closest threat within 150 m horizontal / 30 m vertical. On detection, it evades tangentially (90 deg from the threat bearing) for 8 seconds.
- **Metrics:**
  - Unique collisions (pairs breaching 20 m H / 10 m V).
  - Unique DAA evasion events.
  - Route inefficiency % (actual distance / ideal distance).
  - Completed missions.
- **Auto-stop:** When route inefficiency >= 10% **or** collisions >= 50.
- **Scale sweep:** Starts at 50 drones, increments by 50 until saturation.
- **Key output:**
  - `grafico_ineficiencia_rota.png` — inefficiency vs drone count with collapse threshold.
  - `log_consolidado_cenario2.json`.
  - 3 playback JSONs (start / mid / saturated).

### 1.3 Scenario 3 — xTM Only (No DAA)

**File:** `testeprimordial3.py`

- **Purpose:** Evaluate capacity when using **centralized 4D trajectory reservations** as the sole separation mechanism (no runtime DAA).
- **xTM technique:** The `xTMCentral` class pre-deconflicts 4D tubes (30 m H / 15 m V) before approving takeoff. Rejected drones wait in 15-second retry slots. Routes use Dijkstra shortest-path around a restricted area (military/airport polygon).
- **Metrics:**
  - Mean takeoff delay (minutes) — ATFM slot metric.
  - Route inefficiency %.
  - Completed missions.
- **Auto-stop:** When mean takeoff delay >= 5 minutes.
- **Scale sweep:** Starts at 100, increments by 100.
- **Key output:**
  - `grafico_atraso_solo_xtm.png` — mean takeoff delay vs drone count.
  - `log_consolidado_cenario3.json`.
  - 3 playback JSONs (300-second clips from tick 3600–3900).

### 1.4 Scenario 4A — Optimized xTM + DAA (Deterministic)

**File:** `testeprimordial4.py`

- **Purpose:** Demonstrate that a **tactical DAA layer** lets the xTM use **tighter corridors**, increasing airspace capacity before ground saturation.
- **Strategic layer:** xTM with reduced separation tubes (22 m H / 12 m V).
- **Tactical layer:** Runtime DAA detects threats within 25 m H / 12 m V; adds a 5 m distance penalty per evasion.
- **Metrics:**
  - Mean takeoff delay.
  - Route inefficiency %.
  - Unique DAA evasion events.
  - MACproxy (20 m H / 10 m V).
  - Completed missions.
- **Auto-stop:** Mean delay >= 5 minutes.
- **Key output:**
  - `grafico_atraso_cenario4A.png`.
  - `log_consolidado_cenario4A.json` (includes evasion + MACproxy counts).
  - 3 playback JSONs.

### 1.5 Scenario 4B — xTM + Intelligent DAA + Stochastic Wind

**File:** `testeprimordial4b.py`

- **Purpose:** The "real-world chaos" variant — test resilience of the combined xTM + DAA system under **wind perturbation**.
- **Strategic layer:** xTM with elastic time-buffered reservations (30 m H / 15 m V, +/- 2 s temporal buffer).
- **Tactical layer:** Intelligent reactive DAA — determines whether the threat is left or right of the base bearing and evades 60 deg to the opposite side for 3 seconds.
- **Wind model:** Stochastic perturbation of +/- 1.5 m/s on cruise speed per tick.
- **Metrics:** Same as Scenario 4A (delay, inefficiency, DAA evasions, MACproxy, missions).
- **Auto-stop:** Mean delay >= 5 minutes.
- **Key output:**
  - `grafico_atraso_cenario4B.png` — "Resilience: Ground Delay Under Stochastic Wind".
  - `log_consolidado_cenario4B.json`.
  - 3 playback JSONs.

### 1.6 Summary Table


| Aspect               | Scenario 1         | Scenario 2                 | Scenario 3     | Scenario 4A        | Scenario 4B            |
| -------------------- | ------------------ | -------------------------- | -------------- | ------------------ | ---------------------- |
| **xTM**              | No                 | No                         | Yes (30/15 m)  | Yes (22/12 m)      | Yes (30/15 m, elastic) |
| **DAA**              | No                 | Reactive (150/30 m)        | No             | Tactical (25/12 m) | Intelligent (25/12 m)  |
| **Wind**             | No                 | No                         | No             | No                 | Yes (+/- 1.5 m/s)      |
| **Restricted area**  | No                 | No                         | Yes            | Yes                | Yes                    |
| **Primary metric**   | MACproxy           | Inefficiency + collisions  | Mean delay     | Mean delay         | Mean delay             |
| **MACproxy counted** | Yes                | Indirectly (collisions)    | No             | Yes                | Yes                    |
| **Auto-stop**        | None (fixed sweep) | Ineff >= 10% or coll >= 50 | Delay >= 5 min | Delay >= 5 min     | Delay >= 5 min         |


---

## 2. ConOps v0 Context — Relation to DECEA Evaluation

The ConOps v0 document (`conops_v0.md`) is an Operational Concept Description for integrating UTM/UAM into the Brazilian Airspace Control System (SISCEAB). The Python experiments are designed to demonstrate key ConOps principles to DECEA.

### 2.1 Three-Layer Conflict Management

The ConOps defines three conflict management layers (Section 4.x.1.5):

1. **Strategic conflict management** — airspace organization, demand/capacity balancing, traffic synchronization. Reduces the need for tactical intervention.
2. **Separation provision** — tactical process of keeping aircraft away from hazards when strategic management is insufficient.
3. **Collision avoidance (DAA)** — activated when separation provision has been compromised; last-resort safety net.

The Python experiments **map directly to these layers**:


| ConOps Layer              | Scenario 1 | Scenario 2 | Scenario 3 | Scenario 4A/4B            |
| ------------------------- | ---------- | ---------- | ---------- | ------------------------- |
| Strategic (xTM)           | —          | —          | Active     | Active                    |
| Tactical separation       | —          | —          | —          | Active (via DAA feedback) |
| Collision avoidance (DAA) | —          | Active     | —          | Active                    |


This progression demonstrates to DECEA that each layer independently improves safety, and that **combining all layers** (Scenarios 4A/4B) yields the best safety-vs-capacity tradeoff.

### 2.2 Performance-Based Authorization

The ConOps establishes that airspace capacity should scale with vehicle equipage: better-equipped aircraft (with DAA capability) can operate in tighter corridors. Scenario 4A directly demonstrates this principle — DAA backing allows xTM to reduce tube separation from 30/15 m to 22/12 m, admitting more drones before ground saturation.

### 2.3 MACproxy as Safety Metric

MACproxy (Mid-Air Collision Proxy) is the primary safety indicator used across the experiments and is referenced in the ConOps as a key DECEA evaluation metric. It is defined as any unique pair of drones simultaneously breaching 20 m horizontal and 10 m vertical separation.

### 2.4 DAA Regulatory Reference

The ConOps references ASTM F3442-25 (Standard Specification for Detect and Avoid System Performance Requirements). NASA DAIDALUS, implementing DO-365B, is the reference implementation for this standard — which is exactly what the Rust simulation integrates.

---

## 3. Comparison: Python Experiments vs Rust/DAIDALUS Simulation

### 3.1 Structured Comparison


| Dimension                   | Python Experiments (testeprimordial)                    | Rust/DAIDALUS Simulation                                                      |
| --------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Coordinate system**       | Lat/lon geodesic (SJC area)                             | Cartesian XYZ (5 km x 5 km box)                                               |
| **DAA engine**              | Custom heuristic (proximity + tangential evasion)       | NASA DAIDALUS (DO-365B) via C++ bridge                                        |
| **Alert information**       | Binary (threat detected / not detected)                 | Multi-level alerts (1–3), TTV, heading bands (min/max safe heading)           |
| **Avoidance maneuver**      | Fixed angular evasion (90 deg or 60 deg)                | DAIDALUS heading bands + configurable horizontal/vertical offset              |
| **xTM / strategic layer**   | Centralized 4D tube reservation with Dijkstra routing   | Not yet implemented (avoidance only)                                          |
| **Physics engine**          | Simple kinematic integration (dt = 1 s)                 | Bevy ECS + Rapier3D at 50 Hz                                                  |
| **Scale tested**            | Up to 150+ drones, 8-hour runs                          | Up to 200 drones (density sweeps); 2-drone controlled experiments             |
| **Scenario geography**      | Real-world SJC geofence with restricted areas           | Abstract city with CBD, suburbs, NFZs, hub-based routing                      |
| **Metrics**                 | MACproxy, route inefficiency, takeoff delay, throughput | Min separation distance, alert counts, TTV, alert levels                      |
| **Visualization**           | Matplotlib plots + JSON playback clips                  | Interactive 3D WebGL viewer + 2D/3D matplotlib path plots                     |
| **Telemetry format**        | Per-tick JSON arrays                                    | NDJSON (streaming, per-event or fixed-interval)                               |
| **Wind / perturbation**     | Scenario 4B: stochastic +/- 1.5 m/s                     | Not yet implemented                                                           |
| **Configurable parameters** | Hardcoded in each script                                | JSON-driven (evaluation radius, offset, burst, vertical offset, log interval) |


### 3.2 Complementary Strengths

**Python experiments** excel at:

- Proving the **conceptual layered model** (no DAA vs DAA vs xTM vs both) at scale.
- Using **geodesic coordinates** tied to a real Brazilian location (SJC).
- Speaking the **ConOps language** (MACproxy, ATFM delay, route inefficiency) that DECEA evaluates.
- Running **long-duration** scenarios (8 hours) with many density levels.

**Rust/DAIDALUS simulation** excels at:

- Providing **real DAA fidelity**: NASA DO-365B alert levels, time-to-violation, heading bands — the actual standard referenced by ASTM F3442-25.
- **High-performance physics** (50 Hz ECS + Rapier3D) for accurate kinematic modeling.
- **Rich visualization**: interactive 3D viewer with alert bubbles, safe heading arcs, drone heading arrows.
- **Controlled experiments**: precise two-drone encounters (head-on, 90-deg crossing, overtaking) for detailed DAIDALUS behavior analysis.
- **JSON-configurable** avoidance parameters for systematic tuning.

### 3.3 Current Gaps in Each System

**Python experiments lack:**

- Real DAIDALUS integration (DAA is a simple proximity heuristic, not standards-compliant).
- Multi-level alert severity and heading band guidance.
- High-fidelity physics and visualization.

**Rust/DAIDALUS simulation lacks:**

- Strategic xTM layer (4D tube reservation, Dijkstra routing, ATFM delay).
- MACproxy metric computation (currently uses min-distance and alert counts).
- Geodesic coordinate support for real-world geography.
- Long-duration density sweeps with the ConOps metrics (delay, inefficiency, throughput).
- Wind/perturbation modeling.

---

## 4. Integration Proposals

Three concrete paths to combine both systems for a stronger DECEA demonstration.

### 4.1 Path A — Feed Rust/DAIDALUS Telemetry into Python MACproxy Analysis

**Goal:** Use the Python analysis pipeline to compute ConOps-standard metrics (MACproxy, inefficiency, delay) from Rust simulation telemetry.

**Steps:**

1. Add a coordinate transform to the Rust telemetry exporter: convert Cartesian XYZ positions to lat/lon using a reference point (e.g., SJC center: -23.21, -45.86).
2. Export the transformed telemetry in the same per-tick JSON format used by the Python scripts (tick, drone list with lat/lon/alt/state).
3. Write a thin Python adapter that reads Rust NDJSON and feeds it into the existing MACproxy counting logic from `testeprimordial1.py`.
4. Run Rust density sweeps (50–200 drones) with DAIDALUS avoidance, then compute MACproxy using the Python pipeline.
5. Overlay the Rust/DAIDALUS MACproxy curve on the Scenario 1 "chaos curve" and Scenario 2 "DAA-only curve" to show the improvement from standards-compliant DAA.

**Deliverable:** A comparison chart showing MACproxy vs drone density for: no DAA (Scenario 1), heuristic DAA (Scenario 2), and DAIDALUS DAA (Rust).

### 4.2 Path B — Run Python Scenarios Through Rust/DAIDALUS

**Goal:** Replace the Python heuristic DAA with real DAIDALUS while keeping the same scenario geometry and xTM logic.

**Steps:**

1. Convert the SJC geofence and drone configs from Python lat/lon to Rust Cartesian coordinates (using equirectangular projection centered on SJC).
2. Generate Rust scenario JSONs that match the Python drone populations (random origins/destinations within the projected SJC area).
3. Implement a basic xTM strategic layer in Rust (4D tube reservation with configurable separation, matching the Python `xTMCentral` logic).
4. Run the Rust simulator with DAIDALUS for the same density levels as Scenarios 3, 4A, and 4B.
5. Compute the same metrics (mean takeoff delay, MACproxy, inefficiency) and compare against the Python results.

**Deliverable:** Side-by-side comparison of Scenarios 3/4A/4B with heuristic DAA vs DAIDALUS DAA, using identical scenario geometry and xTM parameters.

### 4.3 Path C — Combined Reporting for DECEA

**Goal:** Produce a single unified report that demonstrates the full value chain: ConOps layers, heuristic experiments, and DAIDALUS-validated results.

**Structure:**

1. **Introduction**: ConOps v0 three-layer conflict management model and DECEA evaluation criteria.
2. **Baseline (Scenario 1)**: MACproxy chaos curve — the problem statement.
3. **DAA-only (Scenario 2 + Rust/DAIDALUS)**: Show that reactive DAA improves safety but saturates; show that DAIDALUS (standards-compliant) performs better than the heuristic.
4. **xTM-only (Scenario 3)**: Show that strategic management alone has a capacity ceiling (ground delay).
5. **Combined xTM + DAA (Scenarios 4A/4B + Rust/DAIDALUS)**: Show that the hybrid approach maximizes capacity while maintaining safety, and that DAIDALUS provides the strongest safety guarantee.
6. **Two-drone encounter analysis**: Detailed DAIDALUS behavior (heading bands, alert levels, TTV) from the Rust controlled experiments, demonstrating compliance with ASTM F3442-25 / DO-365B.
7. **Visualization showcase**: Screenshots from the 3D viewer, 2D/3D path plots, and MACproxy charts.

**Deliverable:** A presentation-ready document (or slide deck source material) with charts, tables, and viewer screenshots that maps directly to the ConOps layered model and DECEA evaluation framework.

---

## 5. Recommended Priority

For the most immediate impact on the DECEA presentation:

1. **Path A** (lowest effort, highest immediate value): compute MACproxy from existing Rust telemetry and overlay on the Python chaos curve. This directly shows "DAIDALUS eliminates near-collisions that the baseline and heuristic DAA cannot prevent."
2. **Path C** (medium effort): assemble the combined report using existing Python results + existing Rust two-drone experiments + the Path A overlay chart. This gives DECEA a complete narrative from problem statement to validated solution.
3. **Path B** (highest effort, strongest result): full scenario parity between Python and Rust. This is the gold standard for a peer-reviewed comparison but requires implementing xTM in Rust and coordinate transforms.

