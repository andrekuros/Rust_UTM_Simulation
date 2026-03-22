#!/usr/bin/env python3
"""Daidalus + best_genome with **encounter-style** sim config (minimal, no hub ignore) but the
**same random scenario** as `daidalus_ga/run_seed_comparison_logs.py` (`sjc_scenario_gen`).

Use this when the full seed comparison (base `config/sim_config.json` + zones) misbehaves but
the small encounter battery tests look good.

`best_genome.json` often sets `cpp_distance_filter_m` around **200 m** — fine for 2-drone encounters
where everyone is close; on **large random routes** intruders stay beyond 200 m until seconds before
CPA, so DAIDALUS drops them and you see “no avoidance en route”. This script defaults
**`cpp_distance_filter_m` to 0** (no C++ distance filter) unless you set **`CPP_DISTANCE_FILTER_M`**
(e.g. `200` to match the GA genome).

Env (optional): SIM_DURATION_S, SEED, NUM_DRONES, SCENARIO, PHYSICS_HZ, LOG_LEVEL, LOG_INTERVAL_S (default 1.0, same as mixed_20),
  MIN_ALERT_LEVEL, CPP_DISTANCE_FILTER_M (unset = 0; set to match genome if desired),
  FINAL_APPROACH_NO_REACTIVE_RADIUS_M
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
SCENARIO_GEN = os.path.join(REPO, "sjc_scenario_gen.py")
BEST_GENOME = os.path.join(REPO, "experiments", "daidalus_ga", "best_genome.json")
OUT_DIR = os.path.join(REPO, "experiments", "encounter_battery", "results", "gen_scenario_like_seed")

SEED = int(os.environ.get("SEED", "42"))
NUM_DRONES = int(os.environ.get("NUM_DRONES", "50"))
SCENARIO_ID = os.environ.get("SCENARIO", "2")
DURATION = float(os.environ.get("SIM_DURATION_S", "1200"))
PHYSICS_HZ = float(os.environ.get("PHYSICS_HZ", "10.0"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "full").strip().lower()
LOG_INTERVAL = float(os.environ.get("LOG_INTERVAL_S", "1.0"))


def load_genome() -> dict:
    with open(BEST_GENOME) as f:
        return json.load(f)["genome"]


def _cpp_distance_filter_m() -> float:
    env = os.environ.get("CPP_DISTANCE_FILTER_M")
    if env is None or not str(env).strip():
        return 0.0
    return float(str(env).strip())


def build_sim_config(genome: dict, duration_s: float) -> dict:
    """Same `simulation` block as `run_mixed_20_encounters.py`; cpp filter from env by default."""
    cfg = build_daidalus_sim_config(
        genome,
        duration_s,
        cpp_distance_filter_m=_cpp_distance_filter_m(),
        log_interval_s=LOG_INTERVAL,
        show_progress_bar=True,
        physics_hz=PHYSICS_HZ,
        log_level=LOG_LEVEL,
    )
    tune = cfg["simulation"]["daidalus_tune"]
    tune["min_alert_level"] = int(
        os.environ.get("MIN_ALERT_LEVEL", str(genome["min_alert_level"]))
    )
    tune["final_approach_no_reactive_radius_m"] = float(
        os.environ.get(
            "FINAL_APPROACH_NO_REACTIVE_RADIUS_M",
            str(genome.get("final_approach_no_reactive_radius_m", 0.0)),
        )
    )
    return cfg


def main() -> int:
    if LOG_LEVEL not in ("metrics", "compact", "full"):
        print(f"Invalid LOG_LEVEL={LOG_LEVEL!r}", file=sys.stderr)
        return 1
    if not os.path.isfile(BIN):
        print(f"Missing {BIN}", file=sys.stderr)
        return 1
    if not os.path.isfile(BEST_GENOME):
        print(f"Missing {BEST_GENOME}", file=sys.stderr)
        return 1

    genome = load_genome()
    cfg = build_sim_config(genome, DURATION)
    cpp_df = cfg["simulation"]["daidalus_tune"]["cpp_distance_filter_m"]
    print(
        f"daidalus_tune.cpp_distance_filter_m={cpp_df} "
        f"(genome has {genome.get('cpp_distance_filter_m')}; "
        "unset env → 0 for wide-area)",
        flush=True,
    )
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(os.path.join(OUT_DIR, "sim_config_used.json"), "w") as f:
        json.dump(cfg, f, indent=2)

    tmp = tempfile.mkdtemp(prefix="enc_gen_")
    try:
        subprocess.run(
            [
                sys.executable,
                SCENARIO_GEN,
                "--scenario",
                SCENARIO_ID,
                "--num_drones",
                str(NUM_DRONES),
                "--seed",
                str(SEED),
                "--output_dir",
                tmp,
                "--log_level",
                LOG_LEVEL,
                "--log_interval",
                str(LOG_INTERVAL),
                "--physics_hz",
                str(PHYSICS_HZ),
            ],
            cwd=REPO,
            check=True,
        )
        cfg_dir = os.path.join(tmp, "config")
        os.makedirs(cfg_dir, exist_ok=True)
        with open(os.path.join(cfg_dir, "sim_config.json"), "w") as f:
            json.dump(cfg, f, indent=2)

        log_path = os.path.join(OUT_DIR, "run.log")
        print(
            f"scenario={SCENARIO_ID} seed={SEED} drones={NUM_DRONES} duration={DURATION}s "
            f"physics_hz={PHYSICS_HZ} → {OUT_DIR}",
            flush=True,
        )
        proc = subprocess.run(
            [BIN],
            cwd=tmp,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=7200,
        )
        with open(log_path, "w") as f:
            f.write(proc.stdout or "")

        for name, dest in (
            ("sim_metrics.json", "sim_metrics.json"),
            ("simulation_telemetry.ndjson", "simulation_telemetry.ndjson"),
            (
                os.path.join("config", "scenario_dynamic.json"),
                "scenario_dynamic.json",
            ),
        ):
            src = os.path.join(tmp, name)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(OUT_DIR, dest))

        meta = {
            "description": "Encounter-style sim_config + sjc_scenario_gen like seed comparison",
            "seed": SEED,
            "scenario": SCENARIO_ID,
            "num_drones": NUM_DRONES,
            "duration_s": DURATION,
            "physics_hz": PHYSICS_HZ,
            "genome_source": BEST_GENOME,
            "returncode": proc.returncode,
        }
        with open(os.path.join(OUT_DIR, "meta.json"), "w") as f:
            json.dump(meta, f, indent=2)

        print("returncode:", proc.returncode, flush=True)
        sm_path = os.path.join(OUT_DIR, "sim_metrics.json")
        if os.path.isfile(sm_path):
            with open(sm_path) as f:
                print("sim_metrics:", json.load(f))
        return proc.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
