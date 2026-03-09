import subprocess
import json
import time
import os

def run_experiment():
    print("Building release binaries first...")
    build_process = subprocess.run(["cargo", "build", "--release"], check=True)

    try:
        with open("config/sim_config.json", "r") as f:
            config = json.load(f)
            num_drones = config["scenario"]["num_drones"]
            duration = config["simulation"]["duration"]
            threshold = config["simulation"]["collision_threshold"]
    except Exception as e:
        print(f"Failed to read config/sim_config.json: {e}")
        return

    print(f"\n--- Running experiment with {num_drones} drones for {duration}s (Threshold: {threshold}m) ---")
    
    print("Generating scenario...")
    subprocess.run(["./target/release/scenario_gen"], check=True)
    
    print("Running simulation...")
    start_time = time.time()
    try:
        process = subprocess.run(["./target/release/hpm_utm_simulator"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Simulation failed: {e}")
        return
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
        return

    elapsed = time.time() - start_time
    print(f"Simulation finished in {elapsed:.2f} seconds.")
    
    try:
        with open("simulation_telemetry.ndjson", "r") as f:
            print("Processing metrics from NDJSON telemetry file...")
            
            import math
            drone_distances = {}
            drone_last_pos = {}
            drone_start_time = {}
            drone_end_time = {}
            global_active_alerts = set()
            drone_last_pairs = {}
            total_unique_collisions = 0
            
            frame_count = 0
            
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                entry = json.loads(line)
                
                # Skip metadata line
                if "metadata" in entry:
                    continue
                
                frame_count += 1
                t = entry["time_elapsed"]
                drone_id = entry["drone_id"]
                pos = entry["position"]
                alerts = entry.get("collision_alerts", [])
                
                if drone_id not in drone_start_time:
                    drone_start_time[drone_id] = t
                drone_end_time[drone_id] = t
                
                if drone_id in drone_last_pos:
                    last_pos = drone_last_pos[drone_id]
                    dist = math.sqrt(sum((a - b)**2 for a, b in zip(pos, last_pos)))
                    drone_distances[drone_id] = drone_distances.get(drone_id, 0.0) + dist
                drone_last_pos[drone_id] = pos
                
                current_pair_set = set()
                for alert in alerts:
                    other_id = alert["other_drone_id"]
                    pair = tuple(sorted([drone_id, other_id]))
                    current_pair_set.add(pair)
                    
                    if pair not in global_active_alerts:
                        total_unique_collisions += 1
                        global_active_alerts.add(pair)
                        
                last_pair_set = drone_last_pairs.get(drone_id, set())
                dropped_pairs = last_pair_set - current_pair_set
                for p in dropped_pairs:
                    global_active_alerts.discard(p)
                    
                drone_last_pairs[drone_id] = current_pair_set
            
            print(f"Processed {frame_count} frames.")
            total_distance = sum(drone_distances.values())
            flight_times = [drone_end_time[d] - drone_start_time[d] for d in drone_start_time if drone_end_time[d] > drone_start_time[d]]
            avg_flight_time = sum(flight_times) / len(flight_times) if flight_times else 0
            
            metrics = {
                "num_drones_simulated": len(drone_start_time),
                "total_unique_collisions": total_unique_collisions,
                "total_distance_m": total_distance,
                "average_flight_time_s": avg_flight_time
            }
            
            print("\n--- Experiment Results ---")
            print(json.dumps(metrics, indent=4))
            
            with open("experiment_results.json", "w") as rf:
                json.dump(metrics, rf, indent=4)
                
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Could not read telemetry or calculate metrics: {e}")

if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.makedirs("logs")
    if not os.path.exists("config"):
        os.makedirs("config")
        
    run_experiment()
