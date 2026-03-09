import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

def load_metrics(filename, mode_name):
    if not os.path.exists(filename):
        return None
        
    time_points = []
    alert_levels = []
    ttv_values = []
    active_alerts_over_time = {}

    with open(filename, "r") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            if "metadata" in entry:
                continue

            t = entry.get("time_elapsed", 0)
            alerts = entry.get("collision_alerts", [])
            
            num_alerts = len(alerts)
            if num_alerts > 0:
                active_alerts_over_time[t] = active_alerts_over_time.get(t, 0) + num_alerts

            for alert in alerts:
                lvl = alert.get("alert_level") or 0
                ttv = alert.get("time_to_violation") or 0.0
                
                time_points.append(t)
                alert_levels.append(lvl)
                if ttv > 0.0:
                    ttv_values.append(ttv)

    total_warnings = sum(1 for lvl in alert_levels if lvl >= 2)
    return {
        "mode": mode_name,
        "total_warnings": total_warnings,
        "avg_ttv": np.mean(ttv_values) if ttv_values else 0.0,
        "alert_timeline": active_alerts_over_time,
        "ttvs": ttv_values
    }

def analyze_comparisons():
    print("Loading NDJSON telemetry profiles for None, Fixed, and Daidalus...")
    
    data_none = load_metrics("telemetry_none.ndjson", "None (Blind)")
    data_fixed = load_metrics("telemetry_fixed.ndjson", "Fixed Vector")
    data_daidalus = load_metrics("telemetry_daidalus.ndjson", "NASA Daidalus")
    
    datasets = [d for d in [data_none, data_fixed, data_daidalus] if d is not None]
    
    if not datasets:
        print("No telemetry files found to compare!")
        return

    # 1. Total Warnings Bar Chart
    plt.figure(figsize=(10, 6))
    modes = [d["mode"] for d in datasets]
    warnings = [d["total_warnings"] for d in datasets]
    
    sns.barplot(x=modes, y=warnings, palette="Set2", hue=modes, legend=False)
    plt.title("Total Severe Collision Warnings (Level 2+) Generated per Mode")
    plt.ylabel("Number of Warning Instances")
    plt.grid(axis='y', alpha=0.3)
    plt.savefig("comparison_total_warnings.png")
    plt.close()

    # 2. Cumulative Active Alerts Over Time Side-by-Side
    plt.figure(figsize=(12, 6))
    colors = {"None (Blind)": "red", "Fixed Vector": "orange", "NASA Daidalus": "green"}
    
    for d in datasets:
        timeline = d["alert_timeline"]
        if not timeline:
            continue
        times = sorted(list(timeline.keys()))
        counts = [timeline[t] for t in times]
        plt.plot(times, counts, label=d["mode"], color=colors.get(d["mode"], "blue"), alpha=0.8)

    plt.title("Active Collision Constraints Over 2-Hour Simulation")
    plt.xlabel("Simulation Time (Seconds)")
    plt.ylabel("Active Alert Pairs")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("comparison_alerts_timeline.png")
    plt.close()

    print("--- 3-Way Comparative Results ---")
    for d in datasets:
        print(f"[{d['mode']}] Total Warnings: {d['total_warnings']} | Avg TTV triggers: {d['avg_ttv']:.2f}s")
    
    print("\nGraphs generated: comparison_total_warnings.png, comparison_alerts_timeline.png")

if __name__ == "__main__":
    analyze_comparisons()
