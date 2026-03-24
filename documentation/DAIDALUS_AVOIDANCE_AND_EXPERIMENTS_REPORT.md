# DAIDALUS, Avoidance Logic, and Experiment Infrastructure — Technical Report

This document consolidates design decisions, implementation details, and configuration options for NASA DAIDALUS integration, tactical avoidance, Python *testeprimordial* parity, and the unified experiment runners. It is intended as source material for papers or project reports.

---

## 1. System overview

- **Simulator**: Rust (`hpm_utm_simulator`), Bevy ECS + Rapier3D, scenario from JSON (`config/scenario_dynamic.json`), simulation parameters from `config/sim_config.json`.
- **DAIDALUS**: NASA Detect and Avoid logic in C++, called from Rust via **CXX** (`src/daidalus/`). The bridge evaluates pairwise or multi-intruder geometry and returns alert level, time-to-violation (TTV), horizontal safe-heading bands, and (optionally) **preferred horizontal resolution** heading.
- **Strategic layer (xTM)**: 4D tube / routing logic is largely represented in generated scenarios (Python `sjc_scenario_gen.py`); Rust consumes the resulting missions.
- **Reference behavior**: Python scripts under `xTM_refs/testeprimordial*.py` define scenario semantics and simple geometric DAA for scenes 2, 4a, 4b.

---

## 2. Avoidance modes (`AvoidanceMode`)

Defined in `src/main.rs` and selected by `simulation.avoidance_mode` in `sim_config.json`.

| Mode        | Meaning |
|------------|---------|
| `None`     | No tactical DAA; blind baseline (scene 1 style). |
| `Fixed`    | Simple fixed lateral offset; uses DAIDALUS evaluation path for alerts in monitoring. |
| `Daidalus` | NASA DAIDALUS C++ evaluation + Rust **reactive** layer (configurable action/trigger). |
| `Python2`  | Geometric DAA: 150 m / 30 m shell, 90° tangential evasion ~8 s (`testeprimordial2.py`). |
| `Python4a` | 25 m / 12 m geometric DAA + **route penalty** per tick (no lateral reactive steer to match Python 4A). |
| `Python4b` | 25 m / 12 m, ±60° from track ~3 s + **cruise speed ±1.5 m/s** perturbation (`testeprimordial4b.py`). |

Wind for 4B is implemented in Rust when `avoidance_mode == Python4b` (`Python4bWind` resource); cruise horizontal speed gets `uniform(-1.5, +1.5)` m/s per step, analogous to Python’s `speed_ms_vento`.

---

## 3. DAIDALUS C++ bridge

- **Files**: `src/daidalus/src/daidalus_bridge.cpp`, `src/daidalus/include/daidalus_bridge.h`, Rust FFI in `src/daidalus/mod.rs` (`#[cxx::bridge]`).
- **Initialization**: `DaidalusWrapper` applies `set_DO_365B()`, then optional overrides from tune: `setDistanceFilter`, `setLookaheadTime`, `setHorizontalNMAC`.
- **Outputs per evaluation**:
  - `alert_level`
  - `time_to_violation` (from horizontal CPA-style timing where applicable)
  - `min_safe_heading` / `max_safe_heading` (horizontal direction bands, radians, simulator convention)
  - `preferred_resolution_heading` — DAIDALUS **preferred horizontal resolution** when computable (used by the `preferred_horizontal_resolution` action mode)

**Important limitation**: DAIDALUS receives **current positions and velocities**, not full mission polylines. Route-following is handled by the Rust movement and reactive layers, not inside the DAIDALUS core.

---

## 4. `DaidalusTuneConfig` (Rust + JSON `daidalus_tune`)

Serialized under `simulation.daidalus_tune` in `sim_config.json`. Main fields:

| Field | Role |
|-------|------|
| `evasion_offset_m` | Lateral virtual target distance for reactive steering. |
| `evasion_duration_s` | Hold time for **safe_band** / **preferred_horizontal_resolution** (with turn-rate floor for non-discrete modes). |
| `heading_blend` | In **safe_band**: blend between band lower edge and circular midpoint of `[min,max]` safe heading. |
| `track_mix` | In **safe_band**: blend between “safe” horizontal direction and bearing to next waypoint. |
| `min_alert_level` | Minimum DAIDALUS alert level to start reactive steering when `trigger_mode = alert_level`. |
| `cpp_distance_filter_m` | Passed to C++ `setDistanceFilter` if &gt; 0. |
| `cpp_lookahead_s` | Passed to C++ `setLookaheadTime` if &gt; 0. **Very large values** can change band geometry and perceived “convergence” vs separation. |
| `cpp_horizontal_nmac_m` | Passed to C++ `setHorizontalNMAC` if &gt; 0. |
| `max_cross_track_m` | Clamps reactive target to active route leg in XZ (0 = off). |
| `final_approach_no_reactive_radius_m` | Disables lateral DAIDALUS targets near last waypoint on final leg. |
| `daa_intruder_eval_mode` | `pairwise` (one solve per neighbor pair) vs `multi` (one solve per ownship with capped intruder set). |
| `action_mode` | `safe_band` \| `preferred_horizontal_resolution` \| `discrete_action` (see §5). |
| `trigger_mode` | `alert_level` \| `ttv` (see §6). |
| `ttv_threshold_s` | Used when `trigger_mode = ttv`: react when `0 ≤ TTV ≤ threshold`. |
| `discrete_turn_deg` / `discrete_hold_s` | Used when `action_mode = discrete_action`. |

**Aircraft-aware tweaks** (Rust reactive layer): fixed-wing scaling on offset and longer effective hold when turn rate is low (see `reactive_avoidance_system` in `src/daidalus/mod.rs`). Movement also enforces **horizontal turn-rate limits** from `DronePerformance` (`src/core/mod.rs`).

---

## 5. DAIDALUS tactical action modes (`action_mode`)

All apply only when `avoidance_mode == Daidalus` and after the chosen **trigger** fires.

1. **`safe_band` (default)**  
   Uses DAIDALUS NONE-band interval to derive a horizontal steering direction, with `heading_blend`, `track_mix`, and severity-based route blending. Can produce trajectories that are **valid under DAIDALUS lookahead** but **visually** appear to point toward the other aircraft briefly — because bands encode feasible headings, not “maximize separation,” and the blend with route can pull toward the original leg.

2. **`preferred_horizontal_resolution`**  
   Steers using DAIDALUS **preferred horizontal resolution** heading from the C++ core when available; falls back to step away from intruder if unresolved.

3. **`discrete_action`**  
   Hybrid: DAIDALUS still supplies detection (and TTV/alert for triggers), but maneuver is **primordial-style**: fixed turn left/right relative to route vs threat bearing (`discrete_turn_deg`), held for `discrete_hold_s` (not `evasion_duration_s` from genome for the hold duration itself).

---

## 6. Trigger modes (`trigger_mode`)

- **`alert_level`**: Start / select maneuver when `alert_level ≥ min_alert_level`, with legacy allowance for distance-pair fallback (alert 0) in dense evaluation.
- **`ttv`**: Among candidate alerts for the ownship, prefer the pair with smallest non-negative TTV that satisfies `TTV ≤ ttv_threshold_s`. **Note**: TTV can be `0` or noisy; threshold tuning matters for repeatability.

---

## 7. Monitoring vs reactive steering

- **DAA monitoring** (`daa_monitoring_system`): periodic grid-based neighbor search, then DAIDALUS (or legacy geometry for Python modes), fills `ActiveCollisions`.
- **Reactive avoidance** (`reactive_avoidance_system`): consumes alerts, sets `ReactiveAvoidance.target` for a duration.
- **Landing / terminal suppression**: configurable ignore of pairwise DAA/MACproxy when both aircraft are in the same terminal volume (`LandingCollisionIgnoreConfig`, `landing_collision_ignore_radius_m` in sim config).

---

## 8. Parity with Python *testeprimordial* experiments

| Python | Rust `AvoidanceMode` | Notes |
|--------|----------------------|--------|
| Scene 1 | `None` | No DAA/xTM in ref; Rust scene 1 equivalent is blind. |
| Scene 2 | `Python2` | Geometric thresholds and tangential evasion. |
| Scene 3 | xTM in scenario, typically `None` DAA | Authorization delay from generation metrics. |
| Scene 4A | `Python4a` | Route penalty in `src/core/mod.rs` (`python4a_route_penalty_system`). |
| Scene 4B | `Python4b` | Wind + intelligent ±60° evasion. |

**Metrics alignment** (selected items):

- **MACproxy**: horizontal 20 m / vertical 10 m unique pair counts; low-altitude handling adjusted so pairs are not dropped when only one aircraft is near ground (`src/core/logger.rs`).
- **Route metrics**: `route_ideal_distance_mode` (`chord` vs `polyline`) and `route_metrics_timing` (`mission_complete` vs `spawn`) for Python-style totals.
- **Authorization delay**: mean xTM delay from scenario generation (`generation_metrics.json` / `mean_xtm_delay_s`) surfaced in `run_from_config.py` summaries.

**Scenario 4c** (`sjc_scenario_gen.py`): heterogeneous fleet (rotor / fixed-wing, multiple performance profiles); avoidance mapping uses Python4b-style reactive rules when not in DAIDALUS mode.

---

## 9. Experiment runners and configuration

### 9.1 Unified runner — `experiments/xtm_primordial_rust/run_from_config.py`

- Single JSON config drives scenario cache, baseline vs DAIDALUS arms, and summaries.
- **Binary**: `target/release/hpm_utm_simulator` (or `.exe` on Windows). **After changing Rust code**, run `cargo build --release` or the simulator will not match new JSON fields (serde will panic on unknown enum variants).

### 9.2 Genome vs run config (DAIDALUS)

- Numeric / enum overrides in the **run JSON** are merged into `daidalus_tune` when building the DAIDALUS arm.
- `daa_intruder_eval_mode`: run config wins over `best_genome.json` if valid (`pairwise` | `multi`).
- Example genome path: `experiments/daidalus_ga/best_genome.json`.

### 9.3 Baseline (`no_daidalus`) avoidance

- `no_daidalus_avoidance_mode` in run JSON overrides `simulation.avoidance_mode` for the baseline arm.
- If unset, defaults by **scenario** string: `2`→`Python2`, `4a`→`Python4a`, `4b`/`4c`→`Python4b`, else `None`.

### 9.4 Scenario cache invalidation

- Standard runs: `_scenario_cache` keyed by `scenario`, `num_drones`, `seed`, `physics_hz`, `log_level`, `log_interval_s` (`cache_meta.json`) so changing drone count regenerates the scenario.

### 9.5 Encounter density sweep

- `encounter_drone_counts`: e.g. `[50,100,150]` runs separate cases under `output_dir/encounter_<N>/`, plus `summary_encounter.json`.

### 9.6 Structured encounter suite

- `experiment_type: encounter_suite` with `encounter_cases`: `head_on_2`, `cross_90_2`, `oblique_45_2`, `overtake_2`, `cross_90_3`, `merge_3`, `box_4`.
- `encounter_mixed_fleet`: mix rotorcraft/fixed-wing vs rotor-only.
- Generates minimal `scenario_dynamic.json` in each case cache (not via `sjc_scenario_gen.py`).
- Aggregate: `summary_encounter_suite.json`.

### 9.7 Progress bar

- Simulator prints progress when `show_progress_bar: true`; runner streams child stdout so the bar is visible during runs.

### 9.8 Example config

- `experiments/xtm_primordial_rust/run_from_config.example.json` — documents options via `_comment_*` keys (JSON does not support `//` comments).

---

## 10. Metrics and outputs (summary)

- **`sim_metrics.json`**: `macproxy_count`, `daa_alert_pairs`, `route_inefficiency_pct`, completed missions, etc.
- **`simulation_telemetry.ndjson`**: first line metadata includes partial `daidalus_tune` snapshot (not full tune); per-tick drone samples when `log_level` is `compact`/`full`.
- **Runner summary**: `summary.json` per run; `study_metrics` includes authorization delay when generation metrics exist; **real-time factor** = simulation duration / wall time.

---

## 11. Performance: apparent “slowdown” over long runs

Several effects can make **wall-clock real-time factor** drop during a long simulation even when RAM is stable:

1. **MACproxy spatial grid (fixed in code)**  
   An earlier implementation bucketed aircraft by **horizontal (X,Z) cell only**. Many drones sharing the same map column but separated in altitude were placed in one bucket, making pair checks **O(k²)** in the worst case. As more aircraft are airborne and use the same corridors, *k* grows and CPU cost rises through the run.  
   **Current behavior**: MACproxy uses a **3D grid** (50 m × 10 m vertical × 50 m) and checks all **26** face-adjacent 3D neighbor cells so vertical separation is respected in the broad phase.

2. **Telemetry cost**  
   With `log_level: full` and hundreds of drones, each log tick serializes many lines to `simulation_telemetry.ndjson`. The file grows without bound; **disk I/O** often slows wall-clock time as the file reaches gigabytes. For long jobs, prefer `metrics` or a larger `log_interval_s`, or disable full NDJSON.

3. **More concurrent traffic**  
   Staggered departures mean early simulated time has fewer active aircraft than mid-run; **DAIDALUS / physics / pair checks** naturally scale with the number of simultaneous drones.

4. **Heap churn from pair bookkeeping (fixed in code)**  
   MACproxy and DAA metrics used to build `HashSet<(String, String)>` keys via **new `String` allocation on every spatial pair check and every alert, every frame**. With hundreds of drones that is **millions of small allocations per simulated second**, which fragments the allocator and makes wall-clock time **creep down** over long jobs even when RAM usage looks flat.  
   **Current behavior**: unordered pairs are keyed by a stable **`u128`** (FNV-1a of the two ids). `sim_metrics.json` still reports the same **counts** (`daa_alert_pairs`, `macproxy_active_pairs` as set lengths). Theoretical hash collisions are negligible for experiment use.

---

## 12. Known limitations and operational notes

1. **DAIDALUS compute cost**: High drone counts + `pairwise` or tight `daa_interval_s` can make the DAIDALUS arm much slower than baseline; `multi` caps intruders per ownship (`MAX_MULTI_INTRUDERS` in `src/daidalus/mod.rs`).
2. **Safe-band semantics vs intuition**: Bands are **feasible** headings under DAIDALUS models, not guaranteed “turn away from threat” in the viewer sense; use **`preferred_horizontal_resolution`** or **`discrete_action`** for simpler or more predictable tactics.
3. **Rebuild requirement**: New `daidalus_tune` enum values require a **release** rebuild for `run_from_config.py`.
4. **TTV trigger**: Sensitive to DAIDALUS TTV definition and zeros; validate on small encounter cases before large sweeps.

---

## 13. Primary file index

| Topic | Location |
|-------|----------|
| Sim entry, `AvoidanceMode`, JSON load | `src/main.rs` |
| DAIDALUS plugin, monitoring, reactive logic | `src/daidalus/mod.rs` |
| DAIDALUS C++ bridge | `src/daidalus/src/daidalus_bridge.cpp` |
| Movement, wind, turn limits | `src/core/mod.rs` |
| MACproxy, logging, metrics | `src/core/logger.rs` |
| SJC / xTM scenario generation | `sjc_scenario_gen.py` |
| Unified config runner | `experiments/xtm_primordial_rust/run_from_config.py` |
| Matrix / full-log variants | `experiments/xtm_primordial_rust/run_primordial_matrix.py`, `run_scen4b_full_log.py` |
| Python references | `xTM_refs/testeprimordial*.py` |
| GA genome defaults | `experiments/daidalus_ga/best_genome.json` |

---

## 14. Suggested citations for an external report

- NASA DAIDALUS library (Detect and Avoid Alerting Logic for Unmanned Systems) as integrated via the project’s CXX bridge.
- Python *primordial* scenarios as behavioral baseline for geometric DAA and xTM delay metrics.
- This repository’s explicit definitions of MACproxy thresholds (20 m / 10 m), chord vs polyline ideal distance, and `mission_complete` route accounting.

---

*Document generated to reflect the codebase structure and discussions through the DAIDALUS tactical modes, triggers, experiment runners, and parity work. Update this file when adding new `AvoidanceMode` values, `daidalus_tune` fields, or runner JSON keys.*
