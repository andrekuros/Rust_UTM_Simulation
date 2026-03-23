#!/usr/bin/env python3
"""
Paired Monte Carlo: same `multidrone_perpendicular` geometry (with reproducible XZ jitter)
run under `daa_intruder_eval_mode` pairwise vs multi — for mean/std and paired tests.

Example:
  python experiments/encounter_battery/compare_multidrone_pairwise_multi.py --runs 30
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

_ENC = os.path.dirname(os.path.abspath(__file__))
if _ENC not in sys.path:
    sys.path.insert(0, _ENC)

import run_encounter_experiments as enc  # noqa: E402

try:
    from scipy.stats import ttest_rel
except ImportError:
    ttest_rel = None

REPO = enc.REPO
BIN = enc.BIN
OUT_DIR = os.path.join(enc.OUT_BASE, "multidrone_perpendicular_pairwise_multi_cmp")


def _deep_copy_drones(drones: list[dict]) -> list[dict]:
    return copy.deepcopy(drones)


def apply_xz_jitter(drones: list[dict], rng: random.Random, amp_m: float) -> list[dict]:
    out = _deep_copy_drones(drones)
    for d in out:
        for wp in d["flight_plan"]["waypoints"]:
            wp[0] = float(wp[0]) + rng.uniform(-amp_m, amp_m)
            wp[2] = float(wp[2]) + rng.uniform(-amp_m, amp_m)
    return out


def run_simulation(
    drones: list[dict],
    genome: dict,
    duration_s: float,
    daa_mode: str,
    log_interval_s: float,
) -> tuple[int, dict]:
    tmp = tempfile.mkdtemp(prefix="cmp_mdrone_")
    try:
        cfg_dir = os.path.join(tmp, "config")
        os.makedirs(cfg_dir, exist_ok=True)
        scenario_data = {"drones": drones, "obstacles": [], "departure_landing_zones": []}
        with open(os.path.join(cfg_dir, "scenario_dynamic.json"), "w") as f:
            json.dump(scenario_data, f, indent=2)
        cfg = enc.build_sim_config(genome, duration_s, log_interval_s=log_interval_s)
        cfg["simulation"]["daidalus_tune"]["daa_intruder_eval_mode"] = daa_mode
        with open(os.path.join(cfg_dir, "sim_config.json"), "w") as f:
            json.dump(cfg, f, indent=2)
        proc = subprocess.run(
            [BIN],
            cwd=tmp,
            capture_output=True,
            text=True,
            timeout=max(600, int(duration_s) + 120),
        )
        sm_path = os.path.join(tmp, "sim_metrics.json")
        metrics: dict = {}
        if os.path.isfile(sm_path):
            with open(sm_path) as f:
                metrics = json.load(f)
        return proc.returncode, metrics
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _summarize(xs: list[float]) -> dict:
    import statistics

    if not xs:
        return {"n": 0, "mean": None, "stdev": None}
    return {
        "n": len(xs),
        "mean": statistics.mean(xs),
        "stdev": statistics.stdev(xs) if len(xs) > 1 else 0.0,
        "min": min(xs),
        "max": max(xs),
    }


def _normal_two_tail_p_from_t(t_stat: float, n: int) -> float:
    """Rough two-tailed p using normal approximation (ok for n≈30)."""
    z = abs(float(t_stat))
    # Phi(z) = 0.5 * (1 + erf(z / sqrt(2)))
    phi = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    return max(0.0, min(1.0, 2.0 * (1.0 - phi)))


def paired_test(a: list[float], b: list[float]) -> dict:
    """Paired test for mean(a - b); a = pairwise, b = multi → positive => pairwise more than multi."""
    import statistics

    n = len(a)
    if n != len(b) or n < 2:
        return {"t_statistic": None, "p_value_two_tail": None, "note": "insufficient samples"}
    d = [float(x) - float(y) for x, y in zip(a, b)]
    db = statistics.mean(d)
    sd = statistics.stdev(d)
    if sd == 0.0:
        return {
            "mean_diff_pairwise_minus_multi": db,
            "t_statistic": float("inf") if db != 0 else 0.0,
            "p_value_two_tail": 0.0 if db != 0 else 1.0,
            "note": "zero stdev of differences",
        }
    t_stat = db / (sd / math.sqrt(n))
    if ttest_rel is not None:
        # SciPy: ttest_rel(pairwise, multi) tests mean(a-b)=0 same as above
        _t2, p2 = ttest_rel(a, b)
        return {
            "mean_diff_pairwise_minus_multi": db,
            "t_statistic": float(_t2),
            "p_value_two_tail": float(p2),
            "method": "scipy.stats.ttest_rel",
        }
    return {
        "mean_diff_pairwise_minus_multi": db,
        "t_statistic": t_stat,
        "p_value_two_tail": _normal_two_tail_p_from_t(t_stat, n),
        "method": "normal_approx_two_tail",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="multidrone_perpendicular", help="SCENARIOS key")
    ap.add_argument("--runs", type=int, default=30)
    ap.add_argument("--jitter-m", type=float, default=12.0, help="Uniform XZ jitter amplitude (m)")
    ap.add_argument("--seed-base", type=int, default=9_001_001)
    ap.add_argument("--duration", type=float, default=None, help="Override sim duration (s)")
    ap.add_argument("--log-interval", type=float, default=2.0, dest="log_interval")
    args = ap.parse_args()

    if not os.path.isfile(BIN):
        print(f"Build release binary first: {BIN}", file=sys.stderr)
        return 1

    if args.case not in enc.SCENARIOS:
        print(f"Unknown case {args.case!r}", file=sys.stderr)
        return 2

    genome = enc.load_genome()
    spec = enc.SCENARIOS[args.case]
    base_drones = spec["drones"]
    duration_s = float(args.duration) if args.duration is not None else float(
        spec.get("duration_s", 150.0)
    )

    os.makedirs(OUT_DIR, exist_ok=True)

    rows: list[dict] = []
    ineff_pw: list[float] = []
    ineff_m: list[float] = []
    mac_pw: list[float] = []
    mac_m: list[float] = []

    t0 = time.perf_counter()
    for k in range(args.runs):
        rng = random.Random(args.seed_base + k)
        drones = apply_xz_jitter(base_drones, rng, args.jitter_m)

        print(f"--- run {k + 1}/{args.runs} (seed={args.seed_base + k}) ---", flush=True)
        rc_p, m_p = run_simulation(
            drones, genome, duration_s, "pairwise", args.log_interval
        )
        rc_mu, m_mu = run_simulation(
            drones, genome, duration_s, "multi", args.log_interval
        )

        ip = float(m_p.get("route_inefficiency_pct") or 0.0)
        im = float(m_mu.get("route_inefficiency_pct") or 0.0)
        ineff_pw.append(ip)
        ineff_m.append(im)
        mac_pw.append(float(m_p.get("macproxy_count") or 0))
        mac_m.append(float(m_mu.get("macproxy_count") or 0))

        row = {
            "run_index": k,
            "seed": args.seed_base + k,
            "returncode_pairwise": rc_p,
            "returncode_multi": rc_mu,
            "route_inefficiency_pct_pairwise": ip,
            "route_inefficiency_pct_multi": im,
            "macproxy_count_pairwise": m_p.get("macproxy_count"),
            "macproxy_count_multi": m_mu.get("macproxy_count"),
            "daa_alert_pairs_pairwise": m_p.get("daa_alert_pairs"),
            "daa_alert_pairs_multi": m_mu.get("daa_alert_pairs"),
        }
        rows.append(row)
        print(
            f"  ineff%  pairwise={ip:.4f}  multi={im:.4f}  |  mac  p={m_p.get('macproxy_count')}  m={m_mu.get('macproxy_count')}  |  rc  {rc_p},{rc_mu}",
            flush=True,
        )

    elapsed = time.perf_counter() - t0

    test_ineff = paired_test(ineff_pw, ineff_m)
    test_mac = paired_test(mac_pw, mac_m)

    summary = {
        "case": args.case,
        "runs": args.runs,
        "jitter_m": args.jitter_m,
        "seed_base": args.seed_base,
        "duration_s": duration_s,
        "elapsed_wall_s": elapsed,
        "genome_source": enc.BEST_GENOME,
        "route_inefficiency_pct": {
            "pairwise": _summarize(ineff_pw),
            "multi": _summarize(ineff_m),
            "paired_test_pairwise_minus_multi": test_ineff,
        },
        "macproxy_count": {
            "pairwise": _summarize(mac_pw),
            "multi": _summarize(mac_m),
            "paired_test_pairwise_minus_multi": test_mac,
        },
        "runs_detail": rows,
    }

    out_json = os.path.join(OUT_DIR, "comparison_summary.json")
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)

    print()
    print("=== Summary ===")
    print(f"Wrote {out_json}")
    print(f"Wall time: {elapsed:.1f} s")
    si_p = summary["route_inefficiency_pct"]["pairwise"]
    si_m = summary["route_inefficiency_pct"]["multi"]
    print(
        f"route_inefficiency_pct  pairwise: mean={si_p['mean']:.4f} stdev={si_p['stdev']:.4f}"
    )
    print(
        f"route_inefficiency_pct  multi:    mean={si_m['mean']:.4f} stdev={si_m['stdev']:.4f}"
    )
    print(f"Paired test (pairwise - multi): {test_ineff}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
