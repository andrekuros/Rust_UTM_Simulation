#!/usr/bin/env python3
"""
xTM Experiment Orchestrator — runs all five Python-equivalent scenarios
through the Rust simulator and produces comparison charts.

Tactical DAA follows the original testeprimordial*.py geometry (Python2 / Python4a / Python4b
in sim_config.json), not NASA DAIDALUS — use avoidance_mode \"Daidalus\" in sim_config only if
you explicitly want the C++ DAIDALUS monitor + bands.

Scenarios:
  1   Baseline (no DAA, no xTM)
  2   Python-style DAA only (150m/30m, 90° / 8s)
  3   xTM only (30m/15m tubes)
  4a  xTM (22m/12m) + Python 4A DAA (25m/12m, route penalty)
  4b  xTM (30m/15m elastic) + Python 4B DAA (±60° / 3s) + wind on cruise speed

Usage:
    python xtm_experiments.py                        # run all defaults
    python xtm_experiments.py --scenarios 1 2        # run only 1 & 2
    python xtm_experiments.py --drone_counts 50 100  # custom sweep
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, List, Any, Tuple

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
BIN_SIM = os.path.join(REPO_ROOT, "target", "release", "hpm_utm_simulator")
EXPERIMENT_ROOT = os.path.join(REPO_ROOT, "experiments", "xtm_comparison")

ALL_SCENARIOS = ["1", "2", "3", "4a", "4b"]

DEFAULT_COUNTS = {
    "1":  [5, 10, 25, 50, 75, 100, 150],
    "2":  [50, 100, 150, 200],
    "3":  [100, 200, 300, 400],
    "4a": [100, 200, 300, 400],
    "4b": [100, 200, 300, 400],
}

MAX_WORKERS = min(8, os.cpu_count() or 1)


def run_single(args: Tuple[str, int, int, float, str]) -> Dict[str, Any]:
    """Generate scenario, run Rust sim, compute metrics. Returns metrics dict."""
    scenario, num_drones, seed, log_interval, log_level = args
    run_name = f"sc{scenario}_N{num_drones}"
    run_dir = os.path.join(EXPERIMENT_ROOT, run_name)

    # 1. Generate scenario
    subprocess.run(
        [
            sys.executable, os.path.join(REPO_ROOT, "sjc_scenario_gen.py"),
            "--scenario", scenario,
            "--num_drones", str(num_drones),
            "--output_dir", run_dir,
            "--seed", str(seed),
            "--log_interval", str(log_interval),
            "--log_level", log_level,
        ],
        check=True,
        cwd=REPO_ROOT,
    )

    # 2. Run Rust simulation
    t0 = time.time()
    subprocess.run([BIN_SIM], check=True, cwd=run_dir)
    wall_time = time.time() - t0

    # 3. Compute metrics (reads sim_metrics.json or NDJSON depending on log_level)
    result = subprocess.run(
        [
            sys.executable, os.path.join(REPO_ROOT, "analyze_xtm_metrics.py"),
            "--run_dir", run_dir,
        ],
        check=True,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    print(result.stdout)

    metrics_path = os.path.join(run_dir, "xtm_metrics.json")
    with open(metrics_path) as f:
        metrics = json.load(f)

    metrics["wall_time_s"] = wall_time
    metrics["run_name"] = run_name

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    return metrics


def generate_charts(all_results: List[Dict[str, Any]]):
    """Generate comparison charts from collected metrics."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available — skipping charts")
        return

    chart_dir = os.path.join(EXPERIMENT_ROOT, "charts")
    os.makedirs(chart_dir, exist_ok=True)

    # Group results by scenario
    by_scenario: Dict[str, List] = {}
    for r in all_results:
        sc = r.get("scenario", "?")
        by_scenario.setdefault(sc, []).append(r)

    for sc in by_scenario:
        by_scenario[sc].sort(key=lambda x: x["num_physical_drones"])

    # ── Chart 1: MACproxy vs Drone Count ────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    for sc, runs in sorted(by_scenario.items()):
        xs = [r["num_physical_drones"] for r in runs]
        ys = [r["macproxy_count"] for r in runs]
        ax.plot(xs, ys, "o-", label=f"Scenario {sc}")
    ax.set_xlabel("Number of drones")
    ax.set_ylabel("MACproxy events")
    ax.set_title("MACproxy vs Drone Density — Rust/DAIDALUS")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(chart_dir, "macproxy_vs_density.png"), dpi=150)
    plt.close(fig)

    # ── Chart 2: Route inefficiency ─────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    for sc, runs in sorted(by_scenario.items()):
        xs = [r["num_physical_drones"] for r in runs]
        ys = [r["route_inefficiency_pct"] for r in runs]
        ax.plot(xs, ys, "o-", label=f"Scenario {sc}")
    ax.set_xlabel("Number of drones")
    ax.set_ylabel("Route inefficiency (%)")
    ax.set_title("Route Inefficiency vs Drone Density — Rust/DAIDALUS")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(chart_dir, "inefficiency_vs_density.png"), dpi=150)
    plt.close(fig)

    # ── Chart 3: Mean xTM delay (Scenarios 3, 4a, 4b) ──────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    for sc in ["3", "4a", "4b"]:
        if sc not in by_scenario:
            continue
        runs = by_scenario[sc]
        xs = [r["num_physical_drones"] for r in runs]
        ys = [r["mean_xtm_delay_min"] for r in runs]
        ax.plot(xs, ys, "o-", label=f"Scenario {sc}")
    ax.set_xlabel("Number of drones")
    ax.set_ylabel("Mean takeoff delay (min)")
    ax.set_title("xTM Ground Delay vs Drone Density — Rust/DAIDALUS")
    ax.axhline(y=5.0, color="red", linestyle="--", alpha=0.5, label="Saturation (5 min)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(chart_dir, "xtm_delay_vs_density.png"), dpi=150)
    plt.close(fig)

    # ── Chart 4: DAA alert pairs ────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 6))
    for sc, runs in sorted(by_scenario.items()):
        xs = [r["num_physical_drones"] for r in runs]
        ys = [r["daa_alert_pairs"] for r in runs]
        ax.plot(xs, ys, "o-", label=f"Scenario {sc}")
    ax.set_xlabel("Number of drones")
    ax.set_ylabel("Unique DAA alert pairs")
    ax.set_title("DAIDALUS Alert Pairs vs Drone Density")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(chart_dir, "daa_alerts_vs_density.png"), dpi=150)
    plt.close(fig)

    # ── Summary dashboard ───────────────────────────────────────────
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    titles = ["MACproxy", "Route Inefficiency (%)", "Mean Delay (min)", "DAA Alerts"]
    keys = ["macproxy_count", "route_inefficiency_pct", "mean_xtm_delay_min", "daa_alert_pairs"]
    for idx, (ax, title, key) in enumerate(zip(axes.flat, titles, keys)):
        for sc, runs in sorted(by_scenario.items()):
            xs = [r["num_physical_drones"] for r in runs]
            ys = [r.get(key, 0) for r in runs]
            ax.plot(xs, ys, "o-", label=f"Sc {sc}", markersize=4)
        ax.set_title(title)
        ax.set_xlabel("Drones")
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
    fig.suptitle("xTM Experiment Dashboard — Rust/DAIDALUS vs Python Scenarios", fontsize=13)
    fig.tight_layout()
    fig.savefig(os.path.join(chart_dir, "dashboard.png"), dpi=150)
    plt.close(fig)

    print(f"Charts saved to {chart_dir}/")


def main():
    parser = argparse.ArgumentParser(description="xTM experiment orchestrator")
    parser.add_argument("--scenarios", nargs="+", default=ALL_SCENARIOS,
                        choices=ALL_SCENARIOS, help="Scenarios to run")
    parser.add_argument("--drone_counts", nargs="+", type=int, default=None,
                        help="Override drone counts (applies to all scenarios)")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max_workers", type=int, default=MAX_WORKERS)
    parser.add_argument("--log_interval", type=float, default=5.0,
                        help="Telemetry logging interval in seconds (only for 'full' mode)")
    parser.add_argument("--log_level", default="metrics",
                        choices=["metrics", "compact", "full"],
                        help="Rust log level: metrics (fastest, no NDJSON), compact (events), full (periodic)")
    parser.add_argument("--skip_build", action="store_true")
    args = parser.parse_args()

    if not args.skip_build:
        print("Building release binaries...")
        subprocess.run(["cargo", "build", "--release"], cwd=REPO_ROOT, check=True)

    os.makedirs(EXPERIMENT_ROOT, exist_ok=True)

    jobs: List[Tuple[str, int, int, float, str]] = []
    for sc in args.scenarios:
        counts = args.drone_counts if args.drone_counts else DEFAULT_COUNTS.get(sc, [50, 100])
        for n in counts:
            jobs.append((sc, n, args.seed, args.log_interval, args.log_level))

    print(f"Running {len(jobs)} experiments across scenarios {args.scenarios}...")

    all_results: List[Dict[str, Any]] = []
    t_start = time.time()

    with ProcessPoolExecutor(max_workers=args.max_workers) as executor:
        future_to_job = {executor.submit(run_single, job): job for job in jobs}
        done = 0
        for future in as_completed(future_to_job):
            sc, n, *_ = future_to_job[future]
            try:
                metrics = future.result()
                all_results.append(metrics)
                done += 1
                elapsed = time.time() - t_start
                print(f"[{done}/{len(jobs)}] sc={sc} N={n} "
                      f"MACproxy={metrics['macproxy_count']} "
                      f"wall={metrics['wall_time_s']:.1f}s "
                      f"total_elapsed={elapsed / 60:.1f}min")
            except Exception as e:
                print(f"[ERROR] sc={sc} N={n}: {e}")

    # Save summary
    summary_path = os.path.join(EXPERIMENT_ROOT, "summary_results.json")
    with open(summary_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSummary saved to {summary_path}")

    # Generate charts
    generate_charts(all_results)

    print(f"\nAll experiments done in {(time.time() - t_start) / 60:.1f} minutes.")


if __name__ == "__main__":
    main()
