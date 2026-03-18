#!/usr/bin/env python3
"""
Analyse city-saturation experiment results.
Reads per-run metrics.json + optionally re-scans NDJSON telemetry for richer
collision stats, then produces comparison tables and publication-ready charts.
"""

import os
import sys
import json
import math
import glob
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

EXPERIMENT_ROOT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "experiments",
    "city_saturation",
)
OUT_DIR = os.path.join(EXPERIMENT_ROOT, "analysis")


# ── helpers ──────────────────────────────────────────────────────────────────


def load_all_metrics():
    rows = []
    for mf in sorted(glob.glob(os.path.join(EXPERIMENT_ROOT, "mode_*", "metrics.json"))):
        with open(mf) as f:
            rows.append(json.load(f))
    return rows


def recount_collisions_from_telemetry(ndjson_path):
    """
    Re-scan telemetry to compute *total unique collision pairs ever seen*
    (the stored metric only keeps currently-active pairs at the end).
    Also computes: peak concurrent alerts, total alert-seconds (approx).
    """
    all_ever_pairs = set()
    peak_concurrent = 0
    current_active = set()
    drone_last_pairs = {}
    alert_pair_seconds = 0.0
    last_time = None

    with open(ndjson_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if "metadata" in entry:
                continue

            t = entry["time_elapsed"]
            drone_id = entry["drone_id"]
            alerts = entry.get("collision_alerts", [])

            if last_time is not None and t > last_time:
                dt = t - last_time
                alert_pair_seconds += len(current_active) * dt
            last_time = t

            cur = set()
            for a in alerts:
                pair = tuple(sorted([drone_id, a["other_drone_id"]]))
                cur.add(pair)
                all_ever_pairs.add(pair)
                current_active.add(pair)

            prev = drone_last_pairs.get(drone_id, set())
            for p in prev - cur:
                current_active.discard(p)
            drone_last_pairs[drone_id] = cur

            if len(current_active) > peak_concurrent:
                peak_concurrent = len(current_active)

    return {
        "total_unique_pairs_ever": len(all_ever_pairs),
        "peak_concurrent_alert_pairs": peak_concurrent,
        "alert_pair_seconds": alert_pair_seconds,
    }


# ── main analysis ────────────────────────────────────────────────────────────


def run_analysis():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = load_all_metrics()
    if not rows:
        print("No metrics.json files found – nothing to analyse.")
        sys.exit(1)

    # ── enrich with deep telemetry re-scan ───────────────────────────────
    print("Re-scanning NDJSON telemetry for richer collision statistics …")
    for r in rows:
        run_name = f"mode_{r['mode']}_N{r['num_drones']}"
        ndjson = os.path.join(EXPERIMENT_ROOT, run_name, "simulation_telemetry.ndjson")
        if os.path.exists(ndjson):
            extra = recount_collisions_from_telemetry(ndjson)
            r.update(extra)
        else:
            r["total_unique_pairs_ever"] = r.get("total_unique_collision_pairs", 0)
            r["peak_concurrent_alert_pairs"] = 0
            r["alert_pair_seconds"] = 0.0

    # ── split by mode ────────────────────────────────────────────────────
    by_mode = defaultdict(list)
    for r in rows:
        by_mode[r["mode"]].append(r)
    for v in by_mode.values():
        v.sort(key=lambda r: r["num_drones"])

    # ── print table ──────────────────────────────────────────────────────
    header = (
        f"{'Mode':<10} {'N':>5} {'Uniq Pairs':>11} {'Peak Conc':>10} "
        f"{'Pair·s':>10} {'Dist (km)':>10} {'Avg Flt(s)':>10} "
        f"{'Frames':>9} {'Wall(s)':>9} {'Speed(x)':>9}"
    )
    sep = "─" * len(header)
    print(f"\n{sep}\n{header}\n{sep}")
    for r in sorted(rows, key=lambda r: (r["mode"], r["num_drones"])):
        spd = r["sim_duration_s"] / r["simulation_wall_time_s"] if r["simulation_wall_time_s"] > 0 else 0
        print(
            f"{r['mode']:<10} {r['num_drones']:>5} "
            f"{r['total_unique_pairs_ever']:>11} "
            f"{r['peak_concurrent_alert_pairs']:>10} "
            f"{r['alert_pair_seconds']:>10.0f} "
            f"{r['total_distance_m']/1000:>10.0f} "
            f"{r['average_flight_time_s']:>10.0f} "
            f"{r['frame_count']:>9} "
            f"{r['simulation_wall_time_s']:>9.0f} "
            f"{spd:>9.1f}"
        )
    print(sep)

    # ── save enriched summary json ───────────────────────────────────────
    summary_path = os.path.join(OUT_DIR, "enriched_summary.json")
    with open(summary_path, "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\nEnriched summary → {summary_path}")

    # ── charts ───────────────────────────────────────────────────────────
    plot_collision_pairs(by_mode)
    plot_peak_concurrent(by_mode)
    plot_alert_pair_seconds(by_mode)
    plot_sim_speed(by_mode)
    plot_wall_time(by_mode)
    plot_distance_per_drone(by_mode)
    plot_combined_dashboard(by_mode)

    print(f"\nAll charts saved to {OUT_DIR}/")


# ── chart helpers ────────────────────────────────────────────────────────────


COLORS = {"None": "#e74c3c", "Daidalus": "#2980b9"}
MARKERS = {"None": "o", "Daidalus": "s"}


def _style(ax, title, xlabel, ylabel):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)


def _savefig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)
    print(f"  → {name}")


def plot_collision_pairs(by_mode):
    fig, ax = plt.subplots(figsize=(8, 5))
    for mode, data in by_mode.items():
        ns = [d["num_drones"] for d in data]
        vals = [d["total_unique_pairs_ever"] for d in data]
        ax.plot(ns, vals, marker=MARKERS.get(mode, "^"), color=COLORS.get(mode, "gray"),
                label=mode, linewidth=2, markersize=7)
    _style(ax, "Total Unique Collision Pairs vs Drone Count",
           "Number of drones", "Total unique collision pairs (ever)")
    _savefig(fig, "collision_pairs_vs_N.png")


def plot_peak_concurrent(by_mode):
    fig, ax = plt.subplots(figsize=(8, 5))
    for mode, data in by_mode.items():
        ns = [d["num_drones"] for d in data]
        vals = [d["peak_concurrent_alert_pairs"] for d in data]
        ax.plot(ns, vals, marker=MARKERS.get(mode, "^"), color=COLORS.get(mode, "gray"),
                label=mode, linewidth=2, markersize=7)
    _style(ax, "Peak Concurrent Alert Pairs vs Drone Count",
           "Number of drones", "Peak concurrent alert pairs")
    _savefig(fig, "peak_concurrent_vs_N.png")


def plot_alert_pair_seconds(by_mode):
    fig, ax = plt.subplots(figsize=(8, 5))
    for mode, data in by_mode.items():
        ns = [d["num_drones"] for d in data]
        vals = [d["alert_pair_seconds"] for d in data]
        ax.plot(ns, vals, marker=MARKERS.get(mode, "^"), color=COLORS.get(mode, "gray"),
                label=mode, linewidth=2, markersize=7)
    _style(ax, "Cumulative Alert·Pair-Seconds vs Drone Count",
           "Number of drones", "Alert·pair-seconds")
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k" if x >= 1000 else f"{x:.0f}"))
    _savefig(fig, "alert_pair_seconds_vs_N.png")


def plot_sim_speed(by_mode):
    fig, ax = plt.subplots(figsize=(8, 5))
    for mode, data in by_mode.items():
        ns = [d["num_drones"] for d in data]
        vals = [d["sim_duration_s"] / d["simulation_wall_time_s"]
                if d["simulation_wall_time_s"] > 0 else 0 for d in data]
        ax.plot(ns, vals, marker=MARKERS.get(mode, "^"), color=COLORS.get(mode, "gray"),
                label=mode, linewidth=2, markersize=7)
    ax.axhline(1.0, color="black", linestyle="--", alpha=0.5, label="Real-time (1x)")
    ax.set_yscale("log")
    _style(ax, "Simulation Speed vs Drone Count",
           "Number of drones", "Sim speed (× real-time, log scale)")
    _savefig(fig, "sim_speed_vs_N.png")


def plot_wall_time(by_mode):
    fig, ax = plt.subplots(figsize=(8, 5))
    for mode, data in by_mode.items():
        ns = [d["num_drones"] for d in data]
        vals = [d["simulation_wall_time_s"] / 60.0 for d in data]
        ax.plot(ns, vals, marker=MARKERS.get(mode, "^"), color=COLORS.get(mode, "gray"),
                label=mode, linewidth=2, markersize=7)
    _style(ax, "Wall-Clock Time vs Drone Count",
           "Number of drones", "Wall time (minutes)")
    _savefig(fig, "wall_time_vs_N.png")


def plot_distance_per_drone(by_mode):
    fig, ax = plt.subplots(figsize=(8, 5))
    for mode, data in by_mode.items():
        ns = [d["num_drones"] for d in data]
        vals = [(d["total_distance_m"] / d["num_drones_simulated"]) / 1000
                if d["num_drones_simulated"] > 0 else 0 for d in data]
        ax.plot(ns, vals, marker=MARKERS.get(mode, "^"), color=COLORS.get(mode, "gray"),
                label=mode, linewidth=2, markersize=7)
    _style(ax, "Average Distance per Drone vs Drone Count",
           "Number of drones", "Distance per drone (km)")
    _savefig(fig, "distance_per_drone_vs_N.png")


def plot_combined_dashboard(by_mode):
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle("City Saturation Experiment — Dashboard", fontsize=16, fontweight="bold", y=0.98)

    charts = [
        (axes[0, 0], "total_unique_pairs_ever", "Unique Collision Pairs", "Pairs", False),
        (axes[0, 1], "peak_concurrent_alert_pairs", "Peak Concurrent Alerts", "Pairs", False),
        (axes[0, 2], "alert_pair_seconds", "Alert·Pair-Seconds", "Pair·s", False),
        (axes[1, 0], "_sim_speed", "Simulation Speed", "× real-time", True),
        (axes[1, 1], "_wall_min", "Wall-Clock Time", "Minutes", False),
        (axes[1, 2], "_dist_per_drone_km", "Avg Distance / Drone", "km", False),
    ]

    for ax, key, title, ylabel, log_y in charts:
        for mode, data in by_mode.items():
            ns = [d["num_drones"] for d in data]
            if key == "_sim_speed":
                vals = [d["sim_duration_s"] / d["simulation_wall_time_s"]
                        if d["simulation_wall_time_s"] > 0 else 0 for d in data]
            elif key == "_wall_min":
                vals = [d["simulation_wall_time_s"] / 60 for d in data]
            elif key == "_dist_per_drone_km":
                vals = [(d["total_distance_m"] / d["num_drones_simulated"]) / 1000
                        if d["num_drones_simulated"] > 0 else 0 for d in data]
            else:
                vals = [d.get(key, 0) for d in data]
            ax.plot(ns, vals, marker=MARKERS.get(mode, "^"),
                    color=COLORS.get(mode, "gray"), label=mode, linewidth=2, markersize=5)
        if log_y:
            ax.set_yscale("log")
            ax.axhline(1.0, color="black", linestyle="--", alpha=0.4, linewidth=0.8)
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_xlabel("Drones")
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.25)
        ax.legend(fontsize=8)

    _savefig(fig, "dashboard.png")


# ── entry ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_analysis()
