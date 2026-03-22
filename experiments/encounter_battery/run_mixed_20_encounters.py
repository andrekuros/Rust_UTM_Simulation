#!/usr/bin/env python3
"""20 drones: 5 head-on pairs + 5 perpendicular pairs, separated in space; Daidalus + best_genome.

Outputs to experiments/encounter_battery/results/mixed_20_encounters/
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

_ENC_BATTERY = os.path.dirname(os.path.abspath(__file__))
if _ENC_BATTERY not in sys.path:
    sys.path.insert(0, _ENC_BATTERY)
from daidalus_sim_config_shared import build_daidalus_sim_config  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BIN = os.path.join(REPO, "target", "release", "hpm_utm_simulator")
BEST_GENOME = os.path.join(REPO, "experiments", "daidalus_ga", "best_genome.json")
OUT_DIR = os.path.join(REPO, "experiments", "encounter_battery", "results", "mixed_20_encounters")

ALT = 40.0
PERF = {
    "mass_kg": 1.5,
    "max_speed_mps": 20.0,
    "battery_discharge_rate": 10.0,
}


def drone(did: str, wps: list[list[float]]) -> dict:
    return {
        "id": did,
        "performance": PERF,
        "flight_plan": {"waypoints": wps, "current_waypoint_index": 0},
        "departure_time_s": 0.0,
    }


def build_scenario() -> dict:
    """5 head-on pairs (negative Z lanes) + 5 perpendicular pairs (positive Z lanes)."""
    drones: list[dict] = []
    half = 1200.0

    # Head-on: same X line, opposite directions; lanes along Z so pairs do not overlap.
    z_head = [-1800.0, -1350.0, -900.0, -450.0, 0.0]
    for i, z in enumerate(z_head):
        drones.append(
            drone(
                f"HO_A{i}",
                [[-half, ALT, z], [half, ALT, z]],
            )
        )
        drones.append(
            drone(
                f"HO_B{i}",
                [[half, ALT, z], [-half, ALT, z]],
            )
        )

    # Perpendicular: A along ±X, B along ±Z; meet at (0, ALT, zc); spaced in zc.
    z_centers = [450.0, 950.0, 1450.0, 1950.0, 2450.0]
    leg = 900.0
    for i, zc in enumerate(z_centers):
        drones.append(
            drone(
                f"CR_A{i}",
                [[-leg, ALT, zc], [leg, ALT, zc]],
            )
        )
        drones.append(
            drone(
                f"CR_B{i}",
                [[0.0, ALT, zc - leg], [0.0, ALT, zc + leg]],
            )
        )

    return {"drones": drones, "obstacles": [], "departure_landing_zones": []}


def load_genome() -> dict:
    with open(BEST_GENOME) as f:
        return json.load(f)["genome"]


def main() -> None:
    if not os.path.isfile(BIN):
        print(f"Build release binary first: {BIN}", file=sys.stderr)
        sys.exit(1)
    genome = load_genome()
    duration_s = 180.0
    scenario = build_scenario()
    cfg = build_daidalus_sim_config(
        genome,
        duration_s,
        cpp_distance_filter_m=float(genome["cpp_distance_filter_m"]),
    )

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "scenario_dynamic.json"), "w") as f:
        json.dump(scenario, f, indent=2)
    with open(os.path.join(OUT_DIR, "sim_config_used.json"), "w") as f:
        json.dump(cfg, f, indent=2)

    tmp = tempfile.mkdtemp(prefix="mixed20_")
    try:
        cfg_dir = os.path.join(tmp, "config")
        os.makedirs(cfg_dir)
        shutil.copy(os.path.join(OUT_DIR, "scenario_dynamic.json"), os.path.join(cfg_dir, "scenario_dynamic.json"))
        with open(os.path.join(cfg_dir, "sim_config.json"), "w") as f:
            json.dump(cfg, f, indent=2)

        log_path = os.path.join(OUT_DIR, "run.log")
        print(f"Drones: {len(scenario['drones'])}  duration: {duration_s}s  out: {OUT_DIR}")
        proc = subprocess.run([BIN], cwd=tmp, capture_output=True, text=True, timeout=3600)
        with open(log_path, "w") as f:
            f.write(proc.stdout or "")
            if proc.stderr:
                f.write("\n--- stderr ---\n")
                f.write(proc.stderr)

        sm = os.path.join(tmp, "sim_metrics.json")
        if os.path.isfile(sm):
            shutil.copy2(sm, os.path.join(OUT_DIR, "sim_metrics.json"))
        tel = os.path.join(tmp, "simulation_telemetry.ndjson")
        if os.path.isfile(tel):
            shutil.copy2(tel, os.path.join(OUT_DIR, "simulation_telemetry.ndjson"))

        meta = {
            "description": "5 head-on + 5 perpendicular pairs (20 drones), separated lanes",
            "duration_s": duration_s,
            "returncode": proc.returncode,
        }
        with open(os.path.join(OUT_DIR, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)

        print("returncode:", proc.returncode)
        if os.path.isfile(os.path.join(OUT_DIR, "sim_metrics.json")):
            with open(os.path.join(OUT_DIR, "sim_metrics.json")) as f:
                print("sim_metrics:", json.load(f))
        sys.exit(proc.returncode)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
