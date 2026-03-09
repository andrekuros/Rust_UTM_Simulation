import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def analyze():
    print("Loading NDJSON telemetry...")
    
    time_points = []
    alert_levels = []
    ttv_values = []
    
    active_alerts_over_time = {}

    with open("simulation_telemetry.ndjson", "r") as f:
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

    if not alert_levels:
        print("No alerts found in telemetry! Simulation ran perfectly clean.")
        return

    # 1. Alert Level Distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(x=alert_levels, palette="viridis")
    plt.title("Distribution of NASA DAIDALUS Alert Levels")
    plt.xlabel("Alert Level (1 = Corrective, 2+ = Warning)")
    plt.ylabel("Number of Instances")
    plt.grid(axis='y', alpha=0.3)
    plt.savefig("daidalus_alert_levels.png")
    plt.close()

    # 2. Time-To-Violation Histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(ttv_values, bins=30, kde=True, color='red')
    plt.title("Distribution of Time-To-Violation (TTV) before Conflict")
    plt.xlabel("Time To Violation (Seconds)")
    plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.3)
    plt.savefig("daidalus_ttv_histogram.png")
    plt.close()

    # 3. Active Alerts Over Time
    if active_alerts_over_time:
        times = sorted(list(active_alerts_over_time.keys()))
        counts = [active_alerts_over_time[t] for t in times]
        
        plt.figure(figsize=(12, 6))
        plt.plot(times, counts, color='orange')
        plt.fill_between(times, counts, color='orange', alpha=0.3)
        plt.title("Active Collision Alerts Over Simulation Time")
        plt.xlabel("Simulation Time (Seconds)")
        plt.ylabel("Active Alert Pairs")
        plt.grid(True, alpha=0.3)
        plt.savefig("daidalus_alerts_timeline.png")
        plt.close()

    print("--- DAIDALUS Analytics Results ---")
    print(f"Total Alert Instances Logged: {len(alert_levels)}")
    lvl_1 = sum(1 for lvl in alert_levels if lvl == 1)
    lvl_2 = sum(1 for lvl in alert_levels if lvl >= 2)
    print(f"Corrective Alerts (Level 1): {lvl_1}")
    print(f"Warning Alerts (Level 2+): {lvl_2}")
    if ttv_values:
        print(f"Average Time-to-Violation Warning: {np.mean(ttv_values):.2f} seconds")
    
    print("Graphs generated: daidalus_alert_levels.png, daidalus_ttv_histogram.png, daidalus_alerts_timeline.png")

if __name__ == "__main__":
    analyze()
