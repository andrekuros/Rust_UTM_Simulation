"""
Daidalus / reactive avoidance — **optimization objective** and **scenario suites**.

## Mapping to `xTM_refs/testeprimordial*.py` (Python) vs Rust `sim_metrics.json`

| testeprimordial / paper | Rust `sim_metrics.json` | Notes |
|-------------------------|-------------------------|--------|
| `ineficiencia_pct` (real vs ideal path) | `route_inefficiency_pct` | Same idea; chord/polyline via `route_ideal_distance_mode`. |
| `macproxy` / “proximity failures” | `macproxy_count` | MACproxy-style near-miss counter (see `logger.rs`). |
| DAA “evasions” / unique threat events | `daa_alert_pairs` (length) | Pairs with DAIDALUS alerts; not identical to Python grid DAA, but same *role* in the objective (safety load). |
| `missoes_concluidas`, throughput | `completed_missions` / `total_scheduled_missions` | Use completion fraction when duration allows all missions to finish. |
| xTM **delay** (`atraso_medio_min`) | *Not exported yet* | Reserve weight 0 or add a Rust metric later (tube delay / departure slip). |

Scenario IDs follow **testeprimordial** naming: scenario **1** = baseline blind, **2** = DAA w/o xTM (Rust: `sjc_scenario_gen --scenario 2`), **3/4a/4b** = xTM + DAA variants. Drone IDs in Python are `DRN_{i}`; SJC generator uses `UAV_{i:05d}_m{k}` — both are covered by **encounter** (short IDs) and **generated** (scheduler) cases.

**Optimization default:** minimize a weighted scalar `J` (lower is better):

  - MACproxy (safety)
  - route inefficiency (economy)
  - incomplete missions / uncompleted fraction (service)
  - optional penalty on excessive DAA pair churn

Use `evaluate_genome_suite.py` to run the suite and print `J`.

## Parameters optimized (Rust `daidalus_tune` + scheduler)

These are the genes in `GENOME_KEYS` / `DEFAULT_SEARCH_BOUNDS`:

| Key | Role |
|-----|------|
| `evasion_offset_m` | Lateral displacement of reactive avoidance target. |
| `evasion_duration_s` | How long a reactive target stays active. |
| `heading_blend` | Blend between min/max DAIDALUS safe heading. |
| `track_mix` | Blend safe heading vs track-to-waypoint (with distance scaling in Rust). |
| `cpp_distance_filter_m` | C++ DAIDALUS horizontal distance gate for intruders. |
| `cpp_lookahead_s` | Lookahead horizon for C++ layer. |
| `cpp_horizontal_nmac_m` | Horizontal NMAC threshold (C++). |
| `daa_interval_s` | How often DAA/reactive systems run vs physics. |
| `min_alert_level` | Minimum alert level (integer 0–2) to accept for reactive steering. |
| `max_cross_track_m` | Corridor clamp for evasion target vs active route leg. |
| `final_approach_no_reactive_radius_m` | Radius near last waypoint where reactive avoidance is disabled. |
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@dataclass
class ObjectiveWeights:
    """Lower `scalar_objective` is better."""

    macproxy: float = 3.0
    route_inefficiency_pct: float = 1.0
    mission_incomplete_fraction: float = 25.0
    daa_pairs: float = 0.02
    scenario_weight: float = 1.0  # multiplied per scenario before mean


@dataclass
class ScenarioSpec:
    """One eval case: either a named encounter (see `run_encounter_experiments.SCENARIOS`) or SJC gen."""

    name: str
    duration_s: float
    encounter_key: str | None = None
    """If set, scenario JSON is taken from encounter battery."""
    sjc: tuple[str, int, int] | None = None
    """If set: (scenario_id_str, num_drones, seed) for `sjc_scenario_gen.py`."""
    cpp_distance_filter_m: float | None = None
    """None = use genome value; 0.0 for sparse cruise (recommended for SJC sweep)."""
    weight: float = 1.0
    tags: tuple[str, ...] = ()


def scenario_spec_to_dict(s: ScenarioSpec) -> dict[str, Any]:
    return {
        "name": s.name,
        "duration_s": s.duration_s,
        "encounter_key": s.encounter_key,
        "sjc": list(s.sjc) if s.sjc else None,
        "cpp_distance_filter_m": s.cpp_distance_filter_m,
        "weight": s.weight,
        "tags": list(s.tags),
    }


def scenario_spec_from_dict(d: dict[str, Any]) -> ScenarioSpec:
    sj = d.get("sjc")
    t = d.get("tags") or []
    return ScenarioSpec(
        name=str(d["name"]),
        duration_s=float(d["duration_s"]),
        encounter_key=d.get("encounter_key"),
        sjc=tuple(sj) if sj else None,
        cpp_distance_filter_m=d.get("cpp_distance_filter_m"),
        weight=float(d.get("weight", 1.0)),
        tags=tuple(t),
    )


def default_fast_suite() -> list[ScenarioSpec]:
    """Encounter battery only — **no** `sjc_scenario_gen` (no large random traffic). Faster for GA."""
    return [
        ScenarioSpec("perpendicular", 150.0, encounter_key="perpendicular", tags=("encounter", "2wp")),
        ScenarioSpec("head_on", 150.0, encounter_key="head_on", tags=("encounter", "2wp")),
        ScenarioSpec("sjc2_perpendicular", 180.0, encounter_key="sjc2_perpendicular", tags=("sjc_speed", "2wp")),
        ScenarioSpec("sjc_perpendicular_2", 180.0, encounter_key="sjc_perpendicular_2", tags=("sjc_full", "4wp")),
        ScenarioSpec("center_busy_octet", 320.0, encounter_key="center_busy_octet", tags=("multi", "dense")),
    ]


def default_core_suite() -> list[ScenarioSpec]:
    """Default search list: **fast** encounters + optional large SJC generation (heavy)."""
    return default_fast_suite() + [
        ScenarioSpec(
            "sjc_gen_s2_n50_seed42",
            600.0,
            sjc=("2", 50, 42),
            cpp_distance_filter_m=0.0,
            tags=("sjc_gen", "sparse"),
        ),
    ]


def default_full_suite() -> list[ScenarioSpec]:
    """Core + extra encounters + second SJC random seed."""
    s = list(default_core_suite())
    s.append(
        ScenarioSpec(
            "sjc_gen_s2_n50_seed43",
            600.0,
            sjc=("2", 50, 43),
            cpp_distance_filter_m=0.0,
            tags=("sjc_gen", "sparse"),
        )
    )
    for key in ("converging", "other_acute_crossing", "sjc_dogleg_cross_4"):
        s.append(ScenarioSpec(key, 200.0, encounter_key=key, tags=("encounter",)))
    return s


def suite_by_name(name: str) -> list[ScenarioSpec]:
    n = name.strip().lower()
    if n in ("fast", "encounters"):
        return default_fast_suite()
    if n in ("core", "default"):
        return default_core_suite()
    if n in ("full", "wide"):
        return default_full_suite()
    raise ValueError(f"Unknown suite {name!r}; use fast, core, or full")


def load_sim_metrics(path: str) -> dict[str, Any]:
    with open(path) as f:
        return json.load(f)


def metrics_vector(m: dict[str, Any]) -> dict[str, float]:
    """Normalized fields for objective composition."""
    sched = int(m.get("total_scheduled_missions") or 0)
    done = int(m.get("completed_missions") or 0)
    incomplete = float(m.get("incomplete_missions_total") or 0)
    if sched > 0:
        inc_frac = (sched - done) / float(sched)
    else:
        inc_frac = 0.0
    return {
        "macproxy_count": float(m.get("macproxy_count") or 0),
        "route_inefficiency_pct": float(m.get("route_inefficiency_pct") or 0.0),
        "mission_incomplete_fraction": inc_frac,
        "daa_alert_pairs": float(m.get("daa_alert_pairs") or 0),
        "completed_missions": float(done),
        "total_scheduled_missions": float(sched),
    }


def scalar_objective(
    m: dict[str, Any],
    w: ObjectiveWeights | None = None,
    *,
    scenario_weight: float = 1.0,
) -> float:
    """
    Single scalar to minimize. Uses positive weights on "bad" quantities.
    """
    w = w or ObjectiveWeights()
    v = metrics_vector(m)
    return scenario_weight * w.scenario_weight * (
        w.macproxy * v["macproxy_count"]
        + w.route_inefficiency_pct * max(0.0, v["route_inefficiency_pct"])
        + w.mission_incomplete_fraction * v["mission_incomplete_fraction"]
        + w.daa_pairs * v["daa_alert_pairs"]
    )


def aggregate_objectives(per_scenario: list[tuple[str, float]], mode: str = "mean") -> float:
    """Combine per-scenario objectives (already weighted). mode: mean | max | sum."""
    if not per_scenario:
        return float("inf")
    vals = [x[1] for x in per_scenario]
    if mode == "mean":
        return sum(vals) / len(vals)
    if mode == "max":
        return max(vals)
    if mode == "sum":
        return sum(vals)
    raise ValueError(mode)


GENOME_KEYS = (
    "evasion_offset_m",
    "evasion_duration_s",
    "heading_blend",
    "track_mix",
    "cpp_distance_filter_m",
    "cpp_lookahead_s",
    "cpp_horizontal_nmac_m",
    "daa_interval_s",
    "min_alert_level",
    "max_cross_track_m",
    "final_approach_no_reactive_radius_m",
)

# Suggested bounds for global search (CMA-ES / random / Optuna); tune to your risk model.
DEFAULT_SEARCH_BOUNDS: dict[str, tuple[float, float]] = {
    "evasion_offset_m": (40.0, 220.0),
    "evasion_duration_s": (0.5, 8.0),
    "heading_blend": (0.0, 0.5),
    "track_mix": (0.05, 0.95),
    "cpp_distance_filter_m": (0.0, 400.0),
    "cpp_lookahead_s": (30.0, 300.0),
    "cpp_horizontal_nmac_m": (15.0, 80.0),
    "daa_interval_s": (0.25, 2.0),
    "min_alert_level": (0.0, 2.0),  # int cast in JSON
    "max_cross_track_m": (80.0, 500.0),
    "final_approach_no_reactive_radius_m": (0.0, 200.0),
}
