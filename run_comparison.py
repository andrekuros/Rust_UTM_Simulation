import subprocess
import json
import time
import os

def run_experiment_for_mode(mode_name):
    # Update config
    with open("config/sim_config.json", "r") as f:
        config = json.load(f)
    
    config["simulation"]["avoidance_mode"] = mode_name

    with open("config/sim_config.json", "w") as f:
        json.dump(config, f, indent=4)
        
    num_drones = config["scenario"]["num_drones"]
    duration = config["simulation"]["duration"]
    
    print(f"\n--- Running experiment mode '{mode_name}' with {num_drones} drones for {duration}s ---")
    
    print(f"[{mode_name}] Generating scenario...")
    subprocess.run(["./target/release/scenario_gen"], check=True)
    
    print(f"[{mode_name}] Running simulation...")
    start_time = time.time()
    try:
        subprocess.run(["./target/release/hpm_utm_simulator"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Simulation failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
        return False

    elapsed = time.time() - start_time
    print(f"[{mode_name}] Simulation finished in {elapsed:.2f} seconds.")
    
    # Rename telemetry out
    out_file = f"telemetry_{mode_name.lower()}.ndjson"
    if os.path.exists("simulation_telemetry.ndjson"):
        os.rename("simulation_telemetry.ndjson", out_file)
        print(f"[{mode_name}] Saved telemetry to {out_file}")
    else:
        print(f"[{mode_name}] ERROR: telemetry file not generated.")
        return False
        
    return True

if __name__ == "__main__":
    print("Building release binaries...")
    subprocess.run(["cargo", "build", "--release"], check=True)

    modes = ["None", "Fixed", "Daidalus"]
    for mode in modes:
        if not run_experiment_for_mode(mode):
            print("Experiment aborted due to failure.")
            break
            
    print("\nAll comparative experiments completed! Telemetry files are ready for analysis.")
