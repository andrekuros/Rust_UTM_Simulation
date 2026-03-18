#!/usr/bin/env python3
"""
MACproxy and xTM-compatible metrics analyser for Rust/DAIDALUS telemetry.

Reads periodic NDJSON telemetry (1-second snapshots) and computes:
  - MACproxy  (unique pairs breaching 20m H / 10m V, with 40m H hysteresis)
  - Route inefficiency %
  - Mean takeoff delay (from generation_metrics.json)
  - Completed missions / throughput
  - DAA evasion events (DAIDALUS alerts with level >= 1)

Usage:
    python analyze_xtm_metrics.py --run_dir experiments/xtm/sc1_N50
"""

import argparse
import json
import math
import os
from collections import defaultdict
from typing import Dict, List, Any, Set, Tuple

MACPROXY_H = 20.0
MACPROXY_V = 10.0
MACPROXY_RESET_H = 40.0


def load_telemetry(ndjson_path: str):
    """Yield parsed telemetry entries (skipping metadata line)."""
    with open(ndjson_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if "metadata" in entry:
                continue
            yield entry


def compute_metrics(run_dir: str) -> Dict[str, Any]:
    sim_metrics_path = os.path.join(run_dir, "sim_metrics.json")
    ndjson_path = os.path.join(run_dir, "simulation_telemetry.ndjson")
    gen_metrics_path = os.path.join(run_dir, "generation_metrics.json")

    gen_info = {}
    if os.path.exists(gen_metrics_path):
        with open(gen_metrics_path) as f:
            gen_info = json.load(f)

    # ── Fast path: use Rust-computed sim_metrics.json (metrics mode) ─
    if os.path.exists(sim_metrics_path):
        with open(sim_metrics_path) as f:
            sim_m = json.load(f)

        metrics = {
            "scenario": gen_info.get("scenario", "?"),
            "num_physical_drones": gen_info.get("num_physical_drones", 0),
            "total_drone_entities": gen_info.get("total_drone_entities", 0),
            "macproxy_count": sim_m.get("macproxy_count", 0),
            "macproxy_unique_pairs": sim_m.get("macproxy_active_pairs", 0),
            "daa_alert_pairs": sim_m.get("daa_alert_pairs", 0),
            "completed_missions": sim_m.get("completed_missions", 0),
            "total_real_distance_m": sim_m.get("total_real_distance_m", 0),
            "total_ideal_distance_m": sim_m.get("total_ideal_distance_m", 0),
            "route_inefficiency_pct": sim_m.get("route_inefficiency_pct", 0),
            "mean_xtm_delay_s": gen_info.get("mean_xtm_delay_s", 0),
            "mean_xtm_delay_min": gen_info.get("mean_xtm_delay_s", 0) / 60.0,
            "source": "sim_metrics.json (Rust in-simulation)",
        }

        if not os.path.exists(ndjson_path):
            return metrics

    ideal_by_id = gen_info.get("ideal_dist_by_id", {})

    # ── Full path: parse NDJSON telemetry ───────────────────────────
    if not os.path.exists(ndjson_path):
        return {"error": "No telemetry data or sim_metrics.json found"}

    snapshots: Dict[int, Dict[str, Dict]] = defaultdict(dict)
    drone_positions: Dict[str, List[Tuple[float, List[float]]]] = defaultdict(list)
    all_alert_events: Set[Tuple[str, str]] = set()

    for entry in load_telemetry(ndjson_path):
        t = int(round(entry["time_elapsed"]))
        did = entry["drone_id"]
        snapshots[t][did] = entry
        drone_positions[did].append((entry["time_elapsed"], entry["position"]))

        for alert in entry.get("collision_alerts", []):
            if alert.get("alert_level", 0) >= 1:
                pair = tuple(sorted([did, alert["other_drone_id"]]))
                all_alert_events.add(pair)

    if not snapshots:
        return {"error": "No telemetry data found"}

    macproxy_pairs: Set[Tuple[str, str]] = set()
    active_macproxy: Set[Tuple[str, str]] = set()
    macproxy_count = 0

    sorted_ticks = sorted(snapshots.keys())
    for tick in sorted_ticks:
        snap = snapshots[tick]
        airborne = {did: e for did, e in snap.items()
                    if e["position"][1] >= 5.0}
        drone_ids = list(airborne.keys())
        n = len(drone_ids)

        for i in range(n):
            for j in range(i + 1, n):
                da = drone_ids[i]
                db = drone_ids[j]
                pair = (min(da, db), max(da, db))

                pa = airborne[da]["position"]
                pb = airborne[db]["position"]
                dh = math.sqrt((pa[0] - pb[0]) ** 2 + (pa[2] - pb[2]) ** 2)
                dv = abs(pa[1] - pb[1])

                if dh < MACPROXY_H and dv < MACPROXY_V:
                    if pair not in active_macproxy:
                        active_macproxy.add(pair)
                        macproxy_count += 1
                        macproxy_pairs.add(pair)
                elif dh > MACPROXY_RESET_H:
                    active_macproxy.discard(pair)

    total_real_distance = 0.0
    total_ideal_distance = 0.0
    completed_missions = 0
    for did, positions in drone_positions.items():
        positions.sort(key=lambda x: x[0])
        d = 0.0
        for k in range(1, len(positions)):
            p0 = positions[k - 1][1]
            p1 = positions[k][1]
            seg = math.sqrt(sum((a - b) ** 2 for a, b in zip(p0, p1)))
            d += seg
        total_real_distance += d
        if did in ideal_by_id:
            total_ideal_distance += ideal_by_id[did]
        last_pos = positions[-1][1]
        if last_pos[1] < 2.0:
            completed_missions += 1

    if total_ideal_distance > 0:
        inefficiency_pct = (total_real_distance - total_ideal_distance) / total_ideal_distance * 100.0
    else:
        inefficiency_pct = 0.0

    metrics = {
        "scenario": gen_info.get("scenario", "?"),
        "num_physical_drones": gen_info.get("num_physical_drones", 0),
        "total_drone_entities": gen_info.get("total_drone_entities", len(drone_positions)),
        "macproxy_count": macproxy_count,
        "macproxy_unique_pairs": len(macproxy_pairs),
        "daa_alert_pairs": len(all_alert_events),
        "completed_missions": completed_missions,
        "total_real_distance_m": total_real_distance,
        "total_ideal_distance_m": total_ideal_distance,
        "route_inefficiency_pct": inefficiency_pct,
        "mean_xtm_delay_s": gen_info.get("mean_xtm_delay_s", 0),
        "mean_xtm_delay_min": gen_info.get("mean_xtm_delay_s", 0) / 60.0,
        "telemetry_ticks": len(sorted_ticks),
        "telemetry_time_range_s": (sorted_ticks[-1] - sorted_ticks[0]) if sorted_ticks else 0,
        "source": "simulation_telemetry.ndjson (Python post-process)",
    }
    return metrics


def main():
    parser = argparse.ArgumentParser(description="xTM metrics analyser")
    parser.add_argument("--run_dir", required=True, help="Directory containing simulation_telemetry.ndjson")
    args = parser.parse_args()

    metrics = compute_metrics(args.run_dir)

    metrics_path = os.path.join(args.run_dir, "xtm_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  xTM Metrics — Scenario {metrics.get('scenario','?')}")
    print(f"{'='*60}")
    print(f"  Physical drones:       {metrics['num_physical_drones']}")
    print(f"  Drone entities:        {metrics['total_drone_entities']}")
    print(f"  MACproxy events:       {metrics['macproxy_count']}")
    print(f"  MACproxy unique pairs: {metrics['macproxy_unique_pairs']}")
    print(f"  DAA alert pairs:       {metrics['daa_alert_pairs']}")
    print(f"  Completed missions:    {metrics['completed_missions']}")
    print(f"  Route inefficiency:    {metrics['route_inefficiency_pct']:.2f}%")
    print(f"  Mean xTM delay:        {metrics['mean_xtm_delay_min']:.2f} min")
    print(f"{'='*60}\n")

    return metrics


if __name__ == "__main__":
    main()
