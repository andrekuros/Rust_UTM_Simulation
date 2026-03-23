#!/usr/bin/env python3
"""
Run encounter cases with Daidalus + best_genome tunings (2-drone classics plus
center-arena multi-drone layouts that mimic random-traffic density without long cruise legs,
plus `multidrone_perpendicular` / `multidrone_oblique`: one ownship vs two intruders).

Also includes **SJC-style** missions: full pad→climb→cruise→land chains like `sjc_scenario_gen`
scenario 2, plus **`sjc2_*`** cases: **SJC speeds** with the same **two cruise waypoints** as the
classic encounters (isolated geometry vs full-mission profile).

Writes results/<case>/sim_metrics.json, run.log, simulation_telemetry.ndjson (log_level=full),
and sim_config_used.json for each.

Examples:
  python experiments/encounter_battery/run_encounter_experiments.py \\
    --cases head_on perpendicular converging --log-interval 0.5
  python experiments/encounter_battery/run_encounter_experiments.py \\
    --cases multidrone_perpendicular multidrone_oblique
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_BIN = os.path.join(REPO, "target", "release", "hpm_utm_simulator")
BIN = _BIN + (".exe" if sys.platform == "win32" and not _BIN.endswith(".exe") else "")
BEST_GENOME = os.path.join(REPO, "experiments", "daidalus_ga", "best_genome.json")
OUT_BASE = os.path.join(REPO, "experiments", "encounter_battery", "results")

ALT = 40.0
PERF = {
    "mass_kg": 1.5,
    "max_speed_mps": 20.0,
    "battery_discharge_rate": 10.0,
}

# Match `sjc_scenario_gen` scenario 2 (HORIZONTAL_SPEED / VERTICAL_SPEED).
SJC_HS = 15.3
SJC_VS = 3.0
SJC_CRUISE_ALT = 40.0
PERF_SJC = {
    "mass_kg": 1.5,
    "max_speed_mps": SJC_HS,
    "max_vertical_speed_mps": SJC_VS,
    "battery_discharge_rate": 10.0,
}


def drone(did: str, wps: list[list[float]]) -> dict:
    return {
        "id": did,
        "performance": PERF,
        "flight_plan": {"waypoints": wps, "current_waypoint_index": 0},
        "departure_time_s": 0.0,
    }


def sjc_waypoints(
    ox: float,
    oz: float,
    cruise_xz: list[tuple[float, float]],
    dx: float,
    dz: float,
    cruise_alt: float = SJC_CRUISE_ALT,
) -> list[list[float]]:
    """Same chain as sjc `rust_waypoints`: ground @ origin, climb @ origin, cruise XZ, ground @ dest."""
    wps: list[list[float]] = [[ox, 0.0, oz], [ox, cruise_alt, oz]]
    for wx, wz in cruise_xz:
        wps.append([wx, cruise_alt, wz])
    wps.append([dx, 0.0, dz])
    return wps


def drone_sjc(
    did: str,
    wps: list[list[float]],
    departure_time_s: float = 0.0,
) -> dict:
    return {
        "id": did,
        "performance": PERF_SJC,
        "flight_plan": {"waypoints": wps, "current_waypoint_index": 0},
        "departure_time_s": float(departure_time_s),
    }


# Two-drone scenarios (horizontal xz plane, y = ALT).
SCENARIOS: dict[str, dict] = {
    "perpendicular": {
        "description": "Classic cross: A along +X, B along +Z (intersection near origin).",
        "drones": [
            drone("A", [[-900.0, ALT, 0.0], [900.0, ALT, 0.0]]),
            drone("B", [[0.0, ALT, -900.0], [0.0, ALT, 900.0]]),
        ],
    },
    "head_on": {
        "description": "Same line, opposite directions (meet near x=0, z=0).",
        "drones": [
            drone("A", [[-1200.0, ALT, 0.0], [1200.0, ALT, 0.0]]),
            drone("B", [[1200.0, ALT, 0.0], [-1200.0, ALT, 0.0]]),
        ],
    },
    "converging": {
        "description": "Both aim at the same point from different bearings (merge geometry).",
        "drones": [
            drone("A", [[-800.0, ALT, -800.0], [0.0, ALT, 0.0]]),
            drone("B", [[800.0, ALT, -800.0], [0.0, ALT, 0.0]]),
        ],
    },
    "other_acute_crossing": {
        "description": "60° crossing in XZ (same altitude); closes faster than shallow diagonal.",
        "drones": [
            drone("A", [[-1000.0, ALT, 0.0], [1000.0, ALT, 0.0]]),
            drone("B", [[-500.0, ALT, -866.0], [500.0, ALT, 866.0]]),
        ],
    },
    # --- SJC speeds, encounter-style 2 cruise waypoints only (no pad / climb / land chain) ---
    "sjc2_perpendicular": {
        "description": "Same geometry as perpendicular; PERF_SJC (15.3 m/s horizontal, 3 m/s vertical).",
        "drones": [
            drone_sjc("A", [[-900.0, ALT, 0.0], [900.0, ALT, 0.0]]),
            drone_sjc("B", [[0.0, ALT, -900.0], [0.0, ALT, 900.0]]),
        ],
    },
    "sjc2_head_on": {
        "description": "Same geometry as head_on; PERF_SJC.",
        "drones": [
            drone_sjc("A", [[-1200.0, ALT, 0.0], [1200.0, ALT, 0.0]]),
            drone_sjc("B", [[1200.0, ALT, 0.0], [-1200.0, ALT, 0.0]]),
        ],
    },
    "sjc2_converging": {
        "description": "Same geometry as converging; PERF_SJC.",
        "drones": [
            drone_sjc("A", [[-800.0, ALT, -800.0], [100.0, ALT, 100.0]]),
            drone_sjc("B", [[800.0, ALT, -800.0], [-100.0, ALT, 100.0]]),
        ],
    },
    "sjc2_acute_crossing": {
        "description": "Same geometry as other_acute_crossing; PERF_SJC.",
        "drones": [
            drone_sjc("A", [[-1000.0, ALT, 0.0], [1000.0, ALT, 0.0]]),
            drone_sjc("B", [[-500.0, ALT, -866.0], [500.0, ALT, 866.0]]),
        ],
    },
    # --- Center-arena “random-like” density (short legs, |x|,|z| modest) -----------------
    # sjc_scenario_gen traffic is sparse on long cruise; with cpp_distance_filter_m ~200, DAA
    # often only “wakes up” near hubs. These cases keep many pairwise distances <~200 m en route
    # so behavior is comparable to the classic 2-drone encounters above.
    "center_head_on_triple": {
        "description": "Three head-on pairs on parallel X-lanes (z=-300,0,300), ±450 m legs — hub-like en-route density, no dep/land.",
        "drones": [
            drone("HO0_A", [[-450.0, ALT, -300.0], [450.0, ALT, -300.0]]),
            drone("HO0_B", [[450.0, ALT, -300.0], [-450.0, ALT, -300.0]]),
            drone("HO1_A", [[-450.0, ALT, 0.0], [450.0, ALT, 0.0]]),
            drone("HO1_B", [[450.0, ALT, 0.0], [-450.0, ALT, 0.0]]),
            drone("HO2_A", [[-450.0, ALT, 300.0], [450.0, ALT, 300.0]]),
            drone("HO2_B", [[450.0, ALT, 300.0], [-450.0, ALT, 300.0]]),
        ],
    },
    "center_perpendicular_double": {
        "description": "Two independent perpendicular crossings, stacked in z (±220) — four aircraft, all near the origin band.",
        "drones": [
            drone("PX0_AX", [[-450.0, ALT, -220.0], [450.0, ALT, -220.0]]),
            drone("PX0_BZ", [[0.0, ALT, -670.0], [0.0, ALT, 230.0]]),
            drone("PX1_AX", [[-450.0, ALT, 220.0], [450.0, ALT, 220.0]]),
            drone("PX1_BZ", [[0.0, ALT, -230.0], [0.0, ALT, 670.0]]),
        ],
    },
    "center_cross_and_headon": {
        "description": "One perpendicular through (0,0) plus a head-on pair on a parallel lane (z=260) — mixed geometry, still compact.",
        "drones": [
            drone("CR_AX", [[-500.0, ALT, 0.0], [500.0, ALT, 0.0]]),
            drone("CR_BZ", [[0.0, ALT, -500.0], [0.0, ALT, 500.0]]),
            drone("HO_A", [[-450.0, ALT, 260.0], [450.0, ALT, 260.0]]),
            drone("HO_B", [[450.0, ALT, 260.0], [-450.0, ALT, 260.0]]),
        ],
    },
    "center_busy_octet": {
        "description": "Eight aircraft: two perpendicular crossings (z=±220) plus two head-on pairs (z=±80) — busiest fixed ‘random-like’ center mix.",
        "drones": [
            drone("P0_AX", [[-500.0, ALT, -220.0], [500.0, ALT, -220.0]]),
            drone("P0_BZ", [[0.0, ALT, -720.0], [0.0, ALT, 280.0]]),
            drone("P1_AX", [[-500.0, ALT, 220.0], [500.0, ALT, 220.0]]),
            drone("P1_BZ", [[0.0, ALT, -280.0], [0.0, ALT, 720.0]]),
            drone("H0_A", [[-450.0, ALT, -80.0], [450.0, ALT, -80.0]]),
            drone("H0_B", [[450.0, ALT, -80.0], [-450.0, ALT, -80.0]]),
            drone("H1_A", [[-450.0, ALT, 80.0], [450.0, ALT, 80.0]]),
            drone("H1_B", [[450.0, ALT, 80.0], [-450.0, ALT, 80.0]]),
        ],
    },
    # --- One ownship vs two intruders (multi-intruder DAA); compact en-route ---------------
    "multidrone_perpendicular": {
        "description": "Ownship O along +X at z=0; B and C each along ±Z at x=-150 and x=150 — two perpendicular crossings on one cruise leg.",
        "drones": [
            drone("O", [[-750.0, ALT, 0.0], [750.0, ALT, 0.0]]),
            drone("B", [[-150.0, ALT, -600.0], [-150.0, ALT, 600.0]]),
            drone("C", [[-150.0, ALT, 600.0], [-150.0, ALT, -600.0]]),
            drone("D", [[750.0, ALT, 0.0], [-750.0, ALT, 0.0]]),
        ],
    },
    "multidrone_oblique": {
        "description": "Ownship O along +X at z=0; B and C on ±60° tracks in XZ (same family as other_acute_crossing) — triple merge near origin.",
        "drones": [
            drone("O", [[-900.0, ALT, 0.0], [900.0, ALT, 0.0]]),
            drone("B", [[-500.0, ALT, -866.0], [500.0, ALT, 866.0]]),
            drone("C", [[-500.0, ALT, 866.0], [500.0, ALT, -866.0]]),
        ],
    },
    # --- SJC scenario-2 style: vertical legs + cruise waypoints at altitude ----------------
    "sjc_perpendicular_2": {
        "description": "Two missions, SJC waypoint chain; classic cross (meet en route after climb).",
        "duration_s": 320.0,
        "drones": [
            drone_sjc("SA", sjc_waypoints(-900.0, 0.0, [(900.0, 0.0)], 900.0, 0.0)),
            drone_sjc("SB", sjc_waypoints(0.0, -900.0, [(0.0, 900.0)], 0.0, 900.0)),
        ],
    },
    "sjc_head_on_2": {
        "description": "Head-on, SJC profile (each climbs at own pad then cruises into conflict).",
        "duration_s": 320.0,
        "drones": [
            drone_sjc("SA", sjc_waypoints(-1200.0, 0.0, [(1200.0, 0.0)], 1200.0, 0.0)),
            drone_sjc("SB", sjc_waypoints(1200.0, 0.0, [(-1200.0, 0.0)], -1200.0, 0.0)),
        ],
    },
    "sjc_converging_2": {
        "description": "Merge-to-point geometry with SJC takeoff/landing legs.",
        "duration_s": 320.0,
        "drones": [
            drone_sjc("SA", sjc_waypoints(-800.0, -800.0, [(0.0, 0.0)], 0.0, 0.0)),
            drone_sjc("SB", sjc_waypoints(800.0, -800.0, [(0.0, 0.0)], 0.0, 0.0)),
        ],
    },
    "sjc_dogleg_cross_4": {
        "description": "Four SJC missions with two cruise waypoints each + staggered departures (dense en-route like random traffic).",
        "duration_s": 400.0,
        "drones": [
            drone_sjc(
                "D0",
                sjc_waypoints(-520.0, -240.0, [(-120.0, 40.0), (380.0, 320.0)], 380.0, 320.0),
                departure_time_s=0.0,
            ),
            drone_sjc(
                "D1",
                sjc_waypoints(520.0, 260.0, [(140.0, 60.0), (-400.0, -300.0)], -400.0, -300.0),
                departure_time_s=12.0,
            ),
            drone_sjc(
                "D2",
                sjc_waypoints(-480.0, 300.0, [(40.0, 80.0), (360.0, -260.0)], 360.0, -260.0),
                departure_time_s=24.0,
            ),
            drone_sjc(
                "D3",
                sjc_waypoints(500.0, -280.0, [(-60.0, -40.0), (-420.0, 220.0)], -420.0, 220.0),
                departure_time_s=36.0,
            ),
        ],
    },
    "sjc_commuter_lane_6": {
        "description": "Six SJC missions along nearby parallel corridors with small offsets and 10 s stagger (queue-like en route).",
        "duration_s": 420.0,
        "drones": [
            drone_sjc("L0", sjc_waypoints(-700.0, -150.0, [(800.0, -150.0)], 800.0, -150.0), 0.0),
            drone_sjc("L1", sjc_waypoints(-700.0, 0.0, [(800.0, 0.0)], 800.0, 0.0), 10.0),
            drone_sjc("L2", sjc_waypoints(-700.0, 150.0, [(800.0, 150.0)], 800.0, 150.0), 20.0),
            drone_sjc("R0", sjc_waypoints(700.0, -120.0, [(-800.0, -120.0)], -800.0, -120.0), 5.0),
            drone_sjc("R1", sjc_waypoints(700.0, 30.0, [(-800.0, 30.0)], -800.0, 30.0), 15.0),
            drone_sjc("R2", sjc_waypoints(700.0, 180.0, [(-800.0, 180.0)], -800.0, 180.0), 25.0),
        ],
    },
}


def load_genome() -> dict:
    with open(BEST_GENOME) as f:
        data = json.load(f)
    g = data.get("best_genome") or data.get("genome")
    if not isinstance(g, dict):
        raise ValueError(f"{BEST_GENOME}: expected 'best_genome' or 'genome' object")
    out = dict(g)
    out["min_alert_level"] = int(round(float(out["min_alert_level"])))
    return out


def daa_intruder_eval_mode_from_genome(genome: dict) -> str:
    """Rust `DaidalusTuneConfig::daa_intruder_eval_mode`: pairwise | multi."""
    v = str(genome.get("daa_intruder_eval_mode", "pairwise")).strip().lower()
    return v if v in ("pairwise", "multi") else "pairwise"


def build_sim_config(genome: dict, duration_s: float, *, log_interval_s: float = 2.0) -> dict:
    return {
        "simulation": {
            "duration": float(duration_s),
            "collision_threshold": 20.0,
            "show_progress_bar": False,
            "avoidance_mode": "Daidalus",
            "scenario_file": "config/scenario_dynamic.json",
            "enable_mqtt": False,
            "log_level": "full",
            "log_interval_s": float(log_interval_s),
            "physics_hz": 10.0,
            "daa_interval_s": float(genome["daa_interval_s"]),
            "daidalus_tune": {
                "evasion_offset_m": float(genome["evasion_offset_m"]),
                "evasion_duration_s": float(genome["evasion_duration_s"]),
                "heading_blend": float(genome["heading_blend"]),
                "track_mix": float(genome["track_mix"]),
                "min_alert_level": int(genome["min_alert_level"]),
                "cpp_distance_filter_m": float(genome["cpp_distance_filter_m"]),
                "cpp_lookahead_s": float(genome["cpp_lookahead_s"]),
                "cpp_horizontal_nmac_m": float(genome["cpp_horizontal_nmac_m"]),
                "max_cross_track_m": float(genome.get("max_cross_track_m", 350.0)),
                "final_approach_no_reactive_radius_m": float(
                    genome.get("final_approach_no_reactive_radius_m", 120.0)
                ),
                "daa_intruder_eval_mode": daa_intruder_eval_mode_from_genome(genome),
            },
            "route_ideal_distance_mode": "chord",
            # `mission_complete` only folds ideal/real into sim_metrics when a drone lands and
            # despawns; encounter cases stay at cruise until `duration` and never hit that path, so
            # totals stayed 0. `spawn` credits chord ideal at spawn and integrates real path every
            # tick (includes Daidalus lateral offsets).
            "route_metrics_timing": "spawn",
        }
    }


def run_case(
    name: str,
    genome: dict,
    default_duration_s: float = 150.0,
    *,
    log_interval_s: float = 2.0,
    duration_override: float | None = None,
) -> int:
    spec = SCENARIOS[name]
    if duration_override is not None:
        duration_s = float(duration_override)
    else:
        duration_s = float(spec.get("duration_s", default_duration_s))
    scenario_data = {
        "drones": spec["drones"],
        "obstacles": [],
        "departure_landing_zones": [],
    }
    out_dir = os.path.join(OUT_BASE, name)
    os.makedirs(out_dir, exist_ok=True)

    tmp = tempfile.mkdtemp(prefix=f"enc_{name}_")
    try:
        cfg_dir = os.path.join(tmp, "config")
        os.makedirs(cfg_dir)
        with open(os.path.join(cfg_dir, "scenario_dynamic.json"), "w") as f:
            json.dump(scenario_data, f, indent=2)
        with open(os.path.join(cfg_dir, "sim_config.json"), "w") as f:
            json.dump(
                build_sim_config(genome, duration_s, log_interval_s=log_interval_s),
                f,
                indent=2,
            )

        proc = subprocess.run(
            [BIN],
            cwd=tmp,
            capture_output=True,
            text=True,
            timeout=max(900, int(duration_s) + 300),
        )
        log_path = os.path.join(out_dir, "run.log")
        with open(log_path, "w") as f:
            f.write(proc.stdout)
            if proc.stderr:
                f.write("\n--- stderr ---\n")
                f.write(proc.stderr)

        sm = os.path.join(tmp, "sim_metrics.json")
        if os.path.isfile(sm):
            shutil.copy2(sm, os.path.join(out_dir, "sim_metrics.json"))
        else:
            with open(os.path.join(out_dir, "sim_metrics.json"), "w") as f:
                json.dump({"error": "sim_metrics.json missing"}, f, indent=2)

        tel = os.path.join(tmp, "simulation_telemetry.ndjson")
        if os.path.isfile(tel):
            shutil.copy2(tel, os.path.join(out_dir, "simulation_telemetry.ndjson"))

        cfg_used = build_sim_config(genome, duration_s, log_interval_s=log_interval_s)
        with open(os.path.join(out_dir, "sim_config_used.json"), "w") as f:
            json.dump(cfg_used, f, indent=2)

        meta = {
            "case": name,
            "description": spec["description"],
            "duration_s": duration_s,
            "default_duration_s": default_duration_s,
            "genome_source": BEST_GENOME,
            "returncode": proc.returncode,
        }
        with open(os.path.join(out_dir, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)

        return proc.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser(description="Run encounter scenarios with Daidalus + best_genome.")
    ap.add_argument(
        "--cases",
        nargs="+",
        metavar="NAME",
        help="Subset of scenario names (default: run all). Example: --cases head_on perpendicular converging",
    )
    ap.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Override simulation duration (seconds) for every selected case",
    )
    ap.add_argument(
        "--log-interval",
        type=float,
        default=2.0,
        dest="log_interval",
        help="NDJSON telemetry sample period for log_level=full (default 2.0 s; use 0.5 for smoother viewer)",
    )
    args = ap.parse_args()

    if not os.path.isfile(BIN):
        print(f"Build release binary first: {BIN}", file=sys.stderr)
        sys.exit(1)
    genome = load_genome()
    default_duration_s = 150.0

    names = list(args.cases) if args.cases else list(SCENARIOS.keys())
    unknown = [n for n in names if n not in SCENARIOS]
    if unknown:
        print(f"Unknown case(s): {unknown}. Valid: {', '.join(sorted(SCENARIOS))}", file=sys.stderr)
        sys.exit(2)

    print("Genome from", BEST_GENOME)
    print("Default duration:", default_duration_s, "s (SJC-style cases override via scenario duration_s)")
    print("Running:", ", ".join(names))
    print("log_interval_s:", args.log_interval)
    print()

    rows = []
    for name in names:
        print(f"=== {name} ===", flush=True)
        rc = run_case(
            name,
            genome,
            default_duration_s,
            log_interval_s=args.log_interval,
            duration_override=args.duration,
        )
        out_dir = os.path.join(OUT_BASE, name)
        sm_path = os.path.join(out_dir, "sim_metrics.json")
        m: dict = {}
        if os.path.isfile(sm_path):
            with open(sm_path) as f:
                m = json.load(f)
        rows.append((name, rc, m))
        print(f"  rc={rc}  daa_alert_pairs={m.get('daa_alert_pairs')}  "
              f"macproxy_count={m.get('macproxy_count')}  "
              f"completed_missions={m.get('completed_missions')}")
        print()

    print("--- Summary ---")
    for name, rc, m in rows:
        ineff = m.get("route_inefficiency_pct")
        print(
            f"{name:18} rc={rc}  alerts={m.get('daa_alert_pairs')}  "
            f"macproxy={m.get('macproxy_count')}  done={m.get('completed_missions')}  "
            f"route_ineff%={ineff if ineff is not None else 'n/a'}"
        )

    bad = [r for r in rows if r[1] != 0]
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
