#!/usr/bin/env python3
"""
SJC scenario **1 / 2 / 3 / 4a / 4b**: same generated traffic, two runs — **without** Daidalus
(``sjc_scenario_gen`` avoidance: None / Python2 / …) vs **with** Daidalus (``best_genome.json``).

Uses ``log_level: full`` so ``simulation_telemetry.ndjson`` is written at ``LOG_INTERVAL_S``.
Daidalus arm uses ``build_daidalus_sim_config`` with ``cpp_distance_filter_m=0``.

  PYTHONUNBUFFERED=1 python3 -u experiments/xtm_primordial_rust/run_scen4b_full_log.py --scenario 2

Environment: same as before (``PRIMORDIAL_DURATION_S``, ``PRIMORDIAL_NUM_DRONES``, …).
Default ``--scenario`` is ``4b`` for backward compatibility.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ENC = os.path.join(REPO, "experiments", "encounter_battery")
_GA = os.path.join(REPO, "experiments", "daidalus_ga")
if _ENC not in sys.path:
    sys.path.insert(0, _ENC)
from daidalus_sim_config_shared import build_daidalus_sim_config  # noqa: E402

BIN = os.path.join(REPO, "target", "release", "hpm_utm_simulator")
SJC_GEN = os.path.join(REPO, "sjc_scenario_gen.py")
SCENARIO_CHOICES = ("1", "2", "3", "4a", "4b", "4c")


def _load_genome(path: str) -> dict:
    with open(path) as f:
        raw = json.load(f)
    g = raw.get("best_genome") if isinstance(raw.get("best_genome"), dict) else raw
    if not isinstance(g, dict):
        raise ValueError(f"No genome dict in {path}")
    return g


def _read_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _ensure_scenario(
    scenario: str, cache_dir: str, num_drones: int, seed: int, physics_hz: float
) -> None:
    scen_path = os.path.join(cache_dir, "config", "scenario_dynamic.json")
    if os.path.isfile(scen_path):
        return
    os.makedirs(cache_dir, exist_ok=True)
    cmd = [
        sys.executable,
        SJC_GEN,
        "--scenario",
        scenario,
        "--num_drones",
        str(num_drones),
        "--seed",
        str(seed),
        "--output_dir",
        cache_dir,
        "--log_level",
        "metrics",
        "--log_interval",
        "5.0",
        "--physics_hz",
        str(physics_hz),
    ]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"sjc_scenario_gen failed: {p.stderr or p.stdout}")


def _patch_baseline_full_log(
    base_sim: dict,
    *,
    duration_s: float,
    physics_hz: float,
    log_interval_s: float,
) -> dict:
    cfg = json.loads(json.dumps(base_sim))
    sim = cfg.setdefault("simulation", {})
    sim["duration"] = float(duration_s)
    sim["physics_hz"] = float(physics_hz)
    sim["log_interval_s"] = float(log_interval_s)
    sim["log_level"] = "full"
    sim["show_progress_bar"] = False
    sim["route_ideal_distance_mode"] = "chord"
    sim["route_metrics_timing"] = "mission_complete"
    return cfg


def _run_arm(payload: dict) -> dict:
    tag = payload["tag"]
    work = payload["work_dir"]
    genome = payload["genome"]
    mode = payload["mode"]
    cache_dir = payload["cache_dir"]
    duration_s = float(payload["duration_s"])
    physics_hz = float(payload["physics_hz"])
    log_interval_s = float(payload["log_interval_s"])
    bin_path = payload["bin_path"]

    out: dict = {"tag": tag, "mode": mode, "rc": -1, "work_dir": work, "error": None}
    try:
        os.makedirs(os.path.join(work, "config"), exist_ok=True)
        shutil.copy2(
            os.path.join(cache_dir, "config", "scenario_dynamic.json"),
            os.path.join(work, "config", "scenario_dynamic.json"),
        )
        base = _read_json(os.path.join(cache_dir, "config", "sim_config.json"))
        if mode == "no_daidalus":
            cfg = _patch_baseline_full_log(
                base,
                duration_s=duration_s,
                physics_hz=physics_hz,
                log_interval_s=log_interval_s,
            )
        else:
            cfg = build_daidalus_sim_config(
                genome,
                duration_s,
                cpp_distance_filter_m=0.0,
                log_interval_s=log_interval_s,
                show_progress_bar=False,
                physics_hz=physics_hz,
                log_level="full",
            )
            # Apple-to-apple with Python refs and no_daidalus arm.
            cfg.setdefault("simulation", {})["route_ideal_distance_mode"] = "chord"
            cfg["simulation"]["route_metrics_timing"] = "mission_complete"
        with open(os.path.join(work, "config", "sim_config.json"), "w") as f:
            json.dump(cfg, f, indent=2)

        timeout_s = max(600, int(duration_s * 6) + 600)
        proc = subprocess.run(
            [bin_path],
            cwd=work,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        out["rc"] = proc.returncode
        out["stderr_tail"] = (proc.stderr or "")[-8000:]
        sm = os.path.join(work, "sim_metrics.json")
        tel = os.path.join(work, "simulation_telemetry.ndjson")
        out["has_telemetry"] = os.path.isfile(tel)
        out["telemetry_bytes"] = os.path.getsize(tel) if out["has_telemetry"] else 0
        if os.path.isfile(sm):
            out["sim_metrics"] = _read_json(sm)
        if proc.returncode != 0:
            out["error"] = f"exit {proc.returncode}"
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="SJC scenario: baseline vs Daidalus with full NDJSON log"
    )
    ap.add_argument(
        "--scenario",
        default="4b",
        choices=SCENARIO_CHOICES,
        help="sjc_scenario_gen scenario (default 4b)",
    )
    ap.add_argument("--genome", default=os.path.join(_GA, "best_genome.json"))
    ap.add_argument("--out", default=None, help="Output directory base")
    args = ap.parse_args()
    scenario = args.scenario

    if not os.path.isfile(BIN):
        print(f"Missing {BIN}", file=sys.stderr)
        return 1

    duration_s = float(os.environ.get("PRIMORDIAL_DURATION_S", "28800"))
    num_drones = int(os.environ.get("PRIMORDIAL_NUM_DRONES", "50"))
    seed = int(os.environ.get("PRIMORDIAL_SEED", "42"))
    physics_hz = float(os.environ.get("PRIMORDIAL_PHYSICS_HZ", "1.0"))
    log_interval_s = float(os.environ.get("LOG_INTERVAL_S", "1.0"))
    genome_path = os.environ.get("PRIMORDIAL_GENOME", args.genome)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_base = args.out or os.environ.get("OUT_DIR")
    if not out_base:
        out_base = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "results",
            f"scen{scenario}_fulllog_{stamp}",
        )
    os.makedirs(out_base, exist_ok=True)

    cache_dir = os.path.join(out_base, f"_scenario_cache_{scenario}")
    _ensure_scenario(scenario, cache_dir, num_drones, seed, physics_hz)
    genome = _load_genome(genome_path)

    meta = {
        "scenario": scenario,
        "duration_s": duration_s,
        "num_drones": num_drones,
        "seed": seed,
        "physics_hz": physics_hz,
        "log_level": "full",
        "log_interval_s": log_interval_s,
        "genome_path": os.path.abspath(genome_path),
        "output_dir": os.path.abspath(out_base),
    }
    with open(os.path.join(out_base, "run_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    jobs = [
        {
            "tag": f"scen{scenario}_n{num_drones}_s{seed}_no_daidalus_fulllog",
            "work_dir": os.path.join(out_base, "no_daidalus"),
            "mode": "no_daidalus",
            "cache_dir": cache_dir,
            "genome": genome,
            "duration_s": duration_s,
            "physics_hz": physics_hz,
            "log_interval_s": log_interval_s,
            "bin_path": BIN,
        },
        {
            "tag": f"scen{scenario}_n{num_drones}_s{seed}_daidalus_fulllog",
            "work_dir": os.path.join(out_base, "daidalus"),
            "mode": "daidalus",
            "cache_dir": cache_dir,
            "genome": genome,
            "duration_s": duration_s,
            "physics_hz": physics_hz,
            "log_interval_s": log_interval_s,
            "bin_path": BIN,
        },
    ]

    print(
        f"scenario={scenario} out={out_base}\n"
        f"duration_s={duration_s} drones={num_drones} log_interval_s={log_interval_s} full telemetry",
        flush=True,
    )

    results = []
    with ProcessPoolExecutor(max_workers=2) as ex:
        futs = {ex.submit(_run_arm, j): j["tag"] for j in jobs}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            print(
                f"  {r.get('tag')} rc={r.get('rc')} "
                f"telemetry={r.get('telemetry_bytes', 0)} B "
                f"{'ERR ' + str(r.get('error')) if r.get('error') else 'ok'}",
                flush=True,
            )

    summary = {"meta": meta, "runs": results}
    with open(os.path.join(out_base, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    with open(os.path.join(out_base, "README.txt"), "w") as f:
        f.write(
            f"scenario {scenario} — no_daidalus/ uses sjc_scenario_gen avoidance; "
            f"daidalus/ uses NASA Daidalus + best_genome.json\n"
            "Full NDJSON: simulation_telemetry.ndjson, sim_metrics.json\n"
        )

    ok = all(r.get("rc") == 0 for r in results)
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
