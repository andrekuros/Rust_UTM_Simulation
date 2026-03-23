#!/usr/bin/env python3
"""Run the simulator on multiple scenario seeds (sjc_scenario_gen --seed).

Default: GA champion + Daidalus. Use --avoidance-mode Python2 (or other) to compare without NASA DAIDALUS.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

REPO = os.path.dirname(os.path.abspath(__file__))
BIN_SIM = os.path.join(REPO, "target", "release", "hpm_utm_simulator")
SCENARIO_GEN = os.path.join(REPO, "sjc_scenario_gen.py")


def apply_genome(cfg_base: dict, genome: dict, duration: float) -> dict:
    cfg = copy.deepcopy(cfg_base)
    sim = cfg.setdefault("simulation", {})
    sim["avoidance_mode"] = "Daidalus"
    sim["duration"] = float(duration)
    sim["show_progress_bar"] = False
    sim["daa_interval_s"] = float(genome["daa_interval_s"])
    _dm = str(genome.get("daa_intruder_eval_mode", "pairwise")).strip().lower()
    daa_mode = _dm if _dm in ("pairwise", "multi") else "pairwise"
    sim["daidalus_tune"] = {
        "evasion_offset_m": float(genome["evasion_offset_m"]),
        "evasion_duration_s": float(genome["evasion_duration_s"]),
        "heading_blend": float(genome["heading_blend"]),
        "track_mix": float(genome["track_mix"]),
        "min_alert_level": int(genome["min_alert_level"]),
        "cpp_distance_filter_m": float(genome["cpp_distance_filter_m"]),
        "cpp_lookahead_s": float(genome["cpp_lookahead_s"]),
        "cpp_horizontal_nmac_m": float(genome["cpp_horizontal_nmac_m"]),
        "daa_intruder_eval_mode": daa_mode,
    }
    return cfg


def apply_baseline(cfg_base: dict, duration: float, avoidance_mode: str) -> dict:
    """Same template + route metrics; geometric/Python modes, no GA genome."""
    cfg = copy.deepcopy(cfg_base)
    sim = cfg.setdefault("simulation", {})
    sim["avoidance_mode"] = avoidance_mode
    sim["duration"] = float(duration)
    sim["show_progress_bar"] = False
    sim.setdefault("route_ideal_distance_mode", "chord")
    sim.setdefault("route_metrics_timing", "mission_complete")
    return cfg


def main() -> None:
    ap = argparse.ArgumentParser(description="Evaluate across scenario seeds (Daidalus GA or baseline mode)")
    ap.add_argument(
        "--avoidance-mode",
        default="Daidalus",
        choices=["Daidalus", "Python2", "Python4a", "Python4b", "None", "Fixed"],
        help="Scenario 2 non-Daidalus baseline is Python2",
    )
    ap.add_argument("--best", default=os.path.join(REPO, "experiments", "daidalus_ga", "best_genome.json"))
    ap.add_argument("--scenario", default="2")
    ap.add_argument("--num_drones", type=int, default=50)
    ap.add_argument("--duration", type=float, default=1200.0)
    ap.add_argument("--seeds", type=int, default=10, help="Use base_seed, base_seed+1, ...")
    ap.add_argument("--base-seed", type=int, default=42)
    ap.add_argument(
        "--out",
        default=None,
        help="Output JSON (default: champion_seed_runs.json or python2_seed_runs.json by mode)",
    )
    ap.add_argument(
        "--template-sim-config",
        default=os.path.join(REPO, "experiments", "daidalus_ga", "template_cache", "config", "sim_config.json"),
        help="Full base sim_config.json (required fields for the Rust binary)",
    )
    args = ap.parse_args()

    if args.out is None:
        if args.avoidance_mode == "Daidalus":
            args.out = os.path.join(REPO, "experiments", "daidalus_ga", "champion_seed_runs.json")
        else:
            args.out = os.path.join(
                REPO, "experiments", "daidalus_ga", f"seed_runs_{args.avoidance_mode.lower()}.json"
            )

    if not os.path.isfile(BIN_SIM):
        print(f"Missing {BIN_SIM}; build release first.", file=sys.stderr)
        sys.exit(1)
    genome = None
    if args.avoidance_mode == "Daidalus":
        if not os.path.isfile(args.best):
            print(f"Missing --best {args.best}", file=sys.stderr)
            sys.exit(1)
        with open(args.best) as f:
            pack = json.load(f)
        genome = pack["genome"]
    with open(args.template_sim_config) as f:
        cfg_template = json.load(f)

    rows = []
    for k in range(args.seeds):
        seed = args.base_seed + k
        tmp = tempfile.mkdtemp(prefix=f"ga_seed_{seed}_")
        try:
            subprocess.run(
                [
                    sys.executable,
                    SCENARIO_GEN,
                    "--scenario",
                    args.scenario,
                    "--num_drones",
                    str(args.num_drones),
                    "--seed",
                    str(seed),
                    "--output_dir",
                    tmp,
                    "--log_level",
                    "metrics",
                ],
                cwd=REPO,
                check=True,
            )
            if args.avoidance_mode == "Daidalus":
                cfg = apply_genome(cfg_template, genome, float(args.duration))
            else:
                cfg = apply_baseline(cfg_template, float(args.duration), args.avoidance_mode)
            with open(os.path.join(tmp, "config", "sim_config.json"), "w") as f:
                json.dump(cfg, f, indent=2)

            t0 = time.perf_counter()
            r = subprocess.run(
                [BIN_SIM],
                cwd=tmp,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=7200,
            )
            wall = time.perf_counter() - t0
            mp = os.path.join(tmp, "sim_metrics.json")
            if r.returncode != 0 or not os.path.isfile(mp):
                rows.append({"seed": seed, "error": r.returncode, "wall_time_s": wall})
                print(f"seed={seed} FAIL rc={r.returncode} wall={wall:.1f}s", flush=True)
                continue
            with open(mp) as f:
                m = json.load(f)
            m["seed"] = seed
            m["wall_time_s"] = wall
            m["rtf"] = float(args.duration) / wall if wall > 0 else None
            rows.append(m)
            print(
                f"seed={seed}  missions={m.get('completed_missions')}  "
                f"ineff={m.get('route_inefficiency_pct'):.2f}%  "
                f"daa_pairs={m.get('daa_alert_pairs')}  wall={wall:.1f}s  rtf={m['rtf']:.1f}x",
                flush=True,
            )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    ok = [r for r in rows if "error" not in r]
    summary = {}
    if ok:
        missions = [float(r["completed_missions"]) for r in ok]
        ineff = [float(r["route_inefficiency_pct"]) for r in ok]
        walls = [float(r["wall_time_s"]) for r in ok]
        summary = {
            "n_ok": len(ok),
            "completed_missions_mean": statistics.mean(missions),
            "completed_missions_stdev": statistics.stdev(missions) if len(missions) > 1 else 0.0,
            "route_inefficiency_pct_mean": statistics.mean(ineff),
            "route_inefficiency_pct_stdev": statistics.stdev(ineff) if len(ineff) > 1 else 0.0,
            "wall_time_s_mean": statistics.mean(walls),
            "wall_time_s_stdev": statistics.stdev(walls) if len(walls) > 1 else 0.0,
        }

    meta = {
        "avoidance_mode": args.avoidance_mode,
        "genome_source": args.best if args.avoidance_mode == "Daidalus" else None,
    }
    out = {
        **meta,
        "scenario": args.scenario,
        "num_drones": args.num_drones,
        "duration": args.duration,
        "seeds": [args.base_seed + k for k in range(args.seeds)],
        "runs": rows,
        "summary": summary,
    }
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {args.out}", flush=True)
    if summary:
        print(
            f"Summary: missions {summary['completed_missions_mean']:.1f} ± {summary['completed_missions_stdev']:.1f}  |  "
            f"ineff {summary['route_inefficiency_pct_mean']:.2f}% ± {summary['route_inefficiency_pct_stdev']:.2f}%  |  "
            f"wall {summary['wall_time_s_mean']:.1f}s ± {summary['wall_time_s_stdev']:.1f}s",
            flush=True,
        )


if __name__ == "__main__":
    main()
