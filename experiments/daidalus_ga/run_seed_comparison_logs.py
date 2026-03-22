#!/usr/bin/env python3
"""One shared seed: Daidalus (GA champion) vs Python2 — full stdout/stderr logs for inspection.

Why en-route can look "inactive" vs small encounter tests:
  - `min_alert_level` in `daidalus_tune`: reactive steering only runs when
    DAIDALUS alert_level >= this value. With **2**, many cruise encounters stay at
    **level 1** only → no lateral maneuver; departure/landing often spike to 2–3.
    Use **1** in `best_genome.json` (default here) so level-1 conflicts steer.
  - `cpp_distance_filter_m`: if > 0, C++ may ignore traffic beyond that horizontal
    range. Large values (e.g. 4500) consider more traffic; **0** = library default.
    Override: `CPP_DISTANCE_FILTER_M=0`.
  - `final_approach_no_reactive_radius_m`: if > 0, Daidalus reactive steering is cleared
    on the **final leg** within that horizontal distance of the last waypoint. The old
    script default **120** made this unlike `run_mixed_20_encounters.py` (which uses **0**
    when the genome omits the key). Default here is now **0** unless the genome sets it.
    Override: `FINAL_APPROACH_NO_REACTIVE_RADIUS_M=120` to restore pad-orbit suppression.
  - Base `config/sim_config.json` still adds **hub** behaviour: `landing_collision_ignore_radius_m`
    (e.g. 50 m) and `departure_landing_zones`. Synthetic encounter scripts omit those fields.
    To match a “clean air” test: `LANDING_COLLISION_IGNORE_RADIUS_M=off` (writes JSON null).

Env: SIM_DURATION_S, PHYSICS_HZ, MIN_ALERT_LEVEL, CPP_DISTANCE_FILTER_M (optional),
     FINAL_APPROACH_NO_REACTIVE_RADIUS_M, LANDING_COLLISION_IGNORE_RADIUS_M (=off to disable),
     LOG_LEVEL (default **full** = periodic NDJSON), LOG_INTERVAL_S (Daidalus, default 5),
     LOG_INTERVAL_PYTHON2_S (Python2, default 1).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIN = os.path.join(REPO, "target", "release", "hpm_utm_simulator")
SCENARIO_GEN = os.path.join(REPO, "sjc_scenario_gen.py")
BASE_SIM_CONFIG = os.path.join(REPO, "config", "sim_config.json")
BEST = os.path.join(REPO, "experiments", "daidalus_ga", "best_genome.json")
OUT_DIR = os.path.join(REPO, "experiments", "daidalus_ga", "comparison_logs")

SEED = 42
DURATION = float(os.environ.get("SIM_DURATION_S", "1200"))
PHYSICS_HZ = float(os.environ.get("PHYSICS_HZ", "10.0"))
# Seed comparison defaults to **full** logging (large `simulation_telemetry.ndjson`).
LOG_LEVEL = os.environ.get("LOG_LEVEL", "full").strip().lower()
LOG_INTERVAL_D = float(os.environ.get("LOG_INTERVAL_S", "1.0"))
LOG_INTERVAL_P2 = float(os.environ.get("LOG_INTERVAL_PYTHON2_S", "10.0"))


def load_base_config() -> dict:
    """Rust `SimConfigRoot`: `simulation` + optional `departure_landing_zones`."""
    if not os.path.isfile(BASE_SIM_CONFIG):
        print(f"Missing {BASE_SIM_CONFIG}", file=sys.stderr)
        sys.exit(1)
    with open(BASE_SIM_CONFIG) as f:
        root = json.load(f)
    return {
        "simulation": root["simulation"],
        "departure_landing_zones": root.get("departure_landing_zones") or [],
    }


def apply_genome(cfg_base: dict, genome: dict, duration: float) -> dict:
    import copy

    cfg = copy.deepcopy(cfg_base)
    sim = cfg.setdefault("simulation", {})
    sim["avoidance_mode"] = "Daidalus"
    sim["duration"] = float(duration)
    sim["show_progress_bar"] = False
    sim["daa_interval_s"] = float(genome["daa_interval_s"])
    tune = {
        "evasion_offset_m": float(genome["evasion_offset_m"]),
        "evasion_duration_s": float(genome["evasion_duration_s"]),
        "heading_blend": float(genome["heading_blend"]),
        "track_mix": float(genome["track_mix"]),
        "min_alert_level": int(
            os.environ.get("MIN_ALERT_LEVEL", str(genome["min_alert_level"]))
        ),
        "cpp_distance_filter_m": float(
            os.environ.get(
                "CPP_DISTANCE_FILTER_M", str(genome["cpp_distance_filter_m"])
            )
        ),
        "cpp_lookahead_s": float(genome["cpp_lookahead_s"]),
        "cpp_horizontal_nmac_m": float(genome["cpp_horizontal_nmac_m"]),
        "max_cross_track_m": float(genome.get("max_cross_track_m", 350.0)),
        "final_approach_no_reactive_radius_m": float(
            os.environ.get(
                "FINAL_APPROACH_NO_REACTIVE_RADIUS_M",
                str(genome.get("final_approach_no_reactive_radius_m", 120.0)),
            )
        ),
    }
    sim["daidalus_tune"] = tune
    sim.setdefault("route_ideal_distance_mode", "chord")
    sim.setdefault("route_metrics_timing", "mission_complete")
    sim["physics_hz"] = float(PHYSICS_HZ)
    sim.setdefault("scenario_file", "config/scenario_dynamic.json")
    sim.setdefault("enable_mqtt", False)
    # Override base sim_config (often 30): matches encounter scripts and pairwise DAA cutoff.
    sim["collision_threshold"] = 20.0
    _lig = os.environ.get("LANDING_COLLISION_IGNORE_RADIUS_M")
    if _lig is not None and _lig.strip().lower() in ("", "none", "null", "off"):
        sim["landing_collision_ignore_radius_m"] = None
    elif _lig is not None and _lig.strip():
        sim["landing_collision_ignore_radius_m"] = float(_lig.strip())
    # Periodic NDJSON: `full` + log_interval_s (overrides anything from base sim_config).
    sim["log_level"] = LOG_LEVEL
    sim["log_interval_s"] = LOG_INTERVAL_D
    return cfg


def apply_python2(cfg_base: dict, duration: float) -> dict:
    import copy

    cfg = copy.deepcopy(cfg_base)
    sim = cfg.setdefault("simulation", {})
    sim["avoidance_mode"] = "Python2"
    sim["duration"] = float(duration)
    sim["show_progress_bar"] = False
    sim.setdefault("route_ideal_distance_mode", "chord")
    sim.setdefault("route_metrics_timing", "mission_complete")
    sim["physics_hz"] = float(PHYSICS_HZ)
    sim.setdefault("scenario_file", "config/scenario_dynamic.json")
    sim.setdefault("enable_mqtt", False)
    sim["collision_threshold"] = 20.0
    _lig = os.environ.get("LANDING_COLLISION_IGNORE_RADIUS_M")
    if _lig is not None and _lig.strip().lower() in ("", "none", "null", "off"):
        sim["landing_collision_ignore_radius_m"] = None
    elif _lig is not None and _lig.strip():
        sim["landing_collision_ignore_radius_m"] = float(_lig.strip())
    sim["log_level"] = LOG_LEVEL
    sim["log_interval_s"] = LOG_INTERVAL_P2
    return cfg


def run_case(
    name: str,
    cfg: dict,
    log_path: str,
    artifact_prefix: str,
    *,
    scenario_log_interval: float,
) -> int:
    """Writes stdout log; copies sim_metrics.json + simulation_telemetry.ndjson next to it."""
    tmp = tempfile.mkdtemp(prefix=f"cmp_{name}_")
    try:
        subprocess.run(
            [
                sys.executable,
                SCENARIO_GEN,
                "--scenario",
                "2",
                "--num_drones",
                "50",
                "--seed",
                str(SEED),
                "--output_dir",
                tmp,
                "--log_level",
                LOG_LEVEL,
                "--log_interval",
                str(scenario_log_interval),
                "--physics_hz",
                str(PHYSICS_HZ),
            ],
            cwd=REPO,
            check=True,
        )
        with open(os.path.join(tmp, "config", "sim_config.json"), "w") as f:
            json.dump(cfg, f, indent=2)
        with open(log_path, "w") as f:
            p = subprocess.run(
                [BIN],
                cwd=tmp,
                stdout=f,
                stderr=subprocess.STDOUT,
                timeout=7200,
            )
        out_dir = os.path.dirname(log_path)
        sm = os.path.join(tmp, "sim_metrics.json")
        if os.path.isfile(sm):
            shutil.copy2(sm, os.path.join(out_dir, f"{artifact_prefix}_sim_metrics.json"))
        nd = os.path.join(tmp, "simulation_telemetry.ndjson")
        if os.path.isfile(nd):
            shutil.copy2(nd, os.path.join(out_dir, f"{artifact_prefix}_telemetry.ndjson"))
        return p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if LOG_LEVEL not in ("metrics", "compact", "full"):
        print(f"Invalid LOG_LEVEL={LOG_LEVEL!r} (use metrics|compact|full)", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(BIN):
        print(f"Missing {BIN}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(BEST):
        print(f"Missing {BEST}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(OUT_DIR, exist_ok=True)

    base = load_base_config()
    with open(BEST) as f:
        genome = json.load(f)["genome"]

    meta = {
        "seed": SEED,
        "duration_s": DURATION,
        "scenario": "2",
        "num_drones": 50,
        "log_level": LOG_LEVEL,
        "log_interval_s_daidalus": LOG_INTERVAL_D,
        "log_interval_s_python2": LOG_INTERVAL_P2,
        "physics_hz": PHYSICS_HZ,
        "base_sim_config": BASE_SIM_CONFIG,
        "outputs": {},
    }

    cfg_d = apply_genome(base, genome, DURATION)
    cfg_p = apply_python2(base, DURATION)

    log_d = os.path.join(OUT_DIR, f"seed{SEED}_daidalus_ga.log")
    log_p = os.path.join(OUT_DIR, f"seed{SEED}_python2.log")

    print(
        f"Logging: log_level={LOG_LEVEL}  interval_daidalus={LOG_INTERVAL_D}s  "
        f"interval_python2={LOG_INTERVAL_P2}s",
        flush=True,
    )
    print("Running Daidalus + GA champion →", log_d, flush=True)
    rc_d = run_case(
        "daidalus",
        cfg_d,
        log_d,
        f"seed{SEED}_daidalus_ga",
        scenario_log_interval=LOG_INTERVAL_D,
    )
    with open(os.path.join(OUT_DIR, f"seed{SEED}_daidalus_ga_sim_config.json"), "w") as f:
        json.dump(cfg_d, f, indent=2)
    meta["outputs"]["daidalus_ga"] = {
        "log": log_d,
        "sim_metrics": os.path.join(OUT_DIR, f"seed{SEED}_daidalus_ga_sim_metrics.json"),
        "telemetry_ndjson": os.path.join(OUT_DIR, f"seed{SEED}_daidalus_ga_telemetry.ndjson"),
        "rc": rc_d,
    }

    print("Running Python2 →", log_p, flush=True)
    rc_p = run_case(
        "python2",
        cfg_p,
        log_p,
        f"seed{SEED}_python2",
        scenario_log_interval=LOG_INTERVAL_P2,
    )
    with open(os.path.join(OUT_DIR, f"seed{SEED}_python2_sim_config.json"), "w") as f:
        json.dump(cfg_p, f, indent=2)
    meta["outputs"]["python2"] = {
        "log": log_p,
        "sim_metrics": os.path.join(OUT_DIR, f"seed{SEED}_python2_sim_metrics.json"),
        "telemetry_ndjson": os.path.join(OUT_DIR, f"seed{SEED}_python2_telemetry.ndjson"),
        "rc": rc_p,
    }

    meta_path = os.path.join(OUT_DIR, f"seed{SEED}_run_meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    print("Wrote meta:", meta_path, flush=True)
    print("rc Daidalus:", rc_d, "rc Python2:", rc_p, flush=True)
    sys.exit(0 if rc_d == 0 and rc_p == 0 else 1)
