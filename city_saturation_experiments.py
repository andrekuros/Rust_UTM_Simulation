import os
import json
import time
import math
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Dict, Any, List, Tuple


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_SIM_CONFIG = os.path.join(REPO_ROOT, "config", "sim_config.json")
BIN_SCENARIO_GEN = os.path.join(REPO_ROOT, "target", "release", "scenario_gen")
BIN_SIM = os.path.join(REPO_ROOT, "target", "release", "hpm_utm_simulator")

EXPERIMENT_ROOT = os.path.join(REPO_ROOT, "experiments", "city_saturation")

# 3 hours window in seconds
SIM_DURATION_S = 3 * 3600.0
TIME_WINDOW_S = SIM_DURATION_S

# Drone counts to sweep
DRONE_COUNTS = [50, 100, 200, 400, 800, 1200, 1600, 2000]

# Avoidance modes to test (must match AvoidanceMode enum variants)
MODES = ["None", "Daidalus"]

MAX_WORKERS = min(16, os.cpu_count() or 1)


def load_base_config() -> Dict[str, Any]:
    with open(BASE_SIM_CONFIG, "r") as f:
        return json.load(f)


def write_run_config(
    base_cfg: Dict[str, Any],
    run_dir: str,
    mode: str,
    num_drones: int,
) -> None:
    cfg = json.loads(json.dumps(base_cfg))  # deep copy via JSON

    # Simulation block
    sim = cfg.setdefault("simulation", {})
    sim["duration"] = SIM_DURATION_S
    sim["time_window"] = TIME_WINDOW_S  # in case scenario_gen uses this
    sim["avoidance_mode"] = mode
    sim["show_progress_bar"] = False
    sim["enable_mqtt"] = False

    # Scenario block
    scen = cfg.setdefault("scenario", {})
    scen["num_drones"] = num_drones
    scen["time_window"] = TIME_WINDOW_S

    # Always use dynamic scenario inside the run directory
    sim["scenario_file"] = "config/scenario_dynamic.json"

    cfg_dir = os.path.join(run_dir, "config")
    os.makedirs(cfg_dir, exist_ok=True)
    sim_cfg_path = os.path.join(cfg_dir, "sim_config.json")

    with open(sim_cfg_path, "w") as f:
        json.dump(cfg, f, indent=4)


def compute_metrics_from_telemetry(path: str) -> Dict[str, Any]:
    """
    Stream NDJSON telemetry and compute coarse metrics:
    - number of drones simulated
    - total unique collision pairs observed
    - total distance travelled per drone and in aggregate
    - average flight time
    """
    drone_distances: Dict[str, float] = {}
    drone_last_pos: Dict[str, List[float]] = {}
    drone_start_time: Dict[str, float] = {}
    drone_end_time: Dict[str, float] = {}

    global_active_alerts = set()
    drone_last_pairs: Dict[str, set] = {}

    frame_count = 0

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            entry = json.loads(line)

            # First line is metadata
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
                dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos, last_pos)))
                drone_distances[drone_id] = drone_distances.get(drone_id, 0.0) + dist
            drone_last_pos[drone_id] = pos

            current_pair_set = set()
            for alert in alerts:
                other_id = alert["other_drone_id"]
                pair = tuple(sorted([drone_id, other_id]))
                current_pair_set.add(pair)

                if pair not in global_active_alerts:
                    global_active_alerts.add(pair)

            last_pair_set = drone_last_pairs.get(drone_id, set())
            dropped_pairs = last_pair_set - current_pair_set
            for p in dropped_pairs:
                global_active_alerts.discard(p)

            drone_last_pairs[drone_id] = current_pair_set

    total_distance = sum(drone_distances.values())
    flight_times = [
        drone_end_time[d] - drone_start_time[d]
        for d in drone_start_time
        if drone_end_time[d] > drone_start_time[d]
    ]
    avg_flight_time = sum(flight_times) / len(flight_times) if flight_times else 0.0

    metrics = {
        "num_drones_simulated": len(drone_start_time),
        "total_unique_collision_pairs": len(global_active_alerts),
        "total_distance_m": total_distance,
        "average_flight_time_s": avg_flight_time,
        "frame_count": frame_count,
    }
    return metrics


def run_single_sim(args: Tuple[str, int]) -> Dict[str, Any]:
    mode, num_drones = args

    run_name = f"mode_{mode}_N{num_drones}"
    run_dir = os.path.join(EXPERIMENT_ROOT, run_name)

    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(run_dir, exist_ok=True)

    base_cfg = load_base_config()
    write_run_config(base_cfg, run_dir, mode, num_drones)

    telemetry_path = os.path.join(run_dir, "simulation_telemetry.ndjson")

    env = os.environ.copy()

    # Generate scenario
    start_gen = time.time()
    subprocess.run(
        [BIN_SCENARIO_GEN],
        check=True,
        cwd=run_dir,
        env=env,
    )
    gen_elapsed = time.time() - start_gen

    # Run simulation
    start_sim = time.time()
    subprocess.run(
        [BIN_SIM],
        check=True,
        cwd=run_dir,
        env=env,
    )
    sim_elapsed = time.time() - start_sim

    if not os.path.exists(telemetry_path):
        raise RuntimeError(f"Telemetry not found for run {run_name}")

    metrics = compute_metrics_from_telemetry(telemetry_path)
    metrics.update(
        {
            "mode": mode,
            "num_drones": num_drones,
            "sim_duration_s": SIM_DURATION_S,
            "scenario_generation_time_s": gen_elapsed,
            "simulation_wall_time_s": sim_elapsed,
        }
    )

    # Store metrics alongside raw telemetry
    metrics_path = os.path.join(run_dir, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=4)

    return metrics


def run_all_experiments() -> None:
    print("Building release binaries...")
    subprocess.run(["cargo", "build", "--release"], cwd=REPO_ROOT, check=True)

    os.makedirs(EXPERIMENT_ROOT, exist_ok=True)

    jobs: List[Tuple[str, int]] = []
    for mode in MODES:
        for n in DRONE_COUNTS:
            jobs.append((mode, n))

    total_jobs = len(jobs)
    print(
        f"Launching {total_jobs} simulations "
        f"({len(MODES)} modes x {len(DRONE_COUNTS)} densities) "
        f"with up to {MAX_WORKERS} workers..."
    )

    all_results: List[Dict[str, Any]] = []

    started_at = time.time()

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_job = {executor.submit(run_single_sim, job): job for job in jobs}

        completed = 0
        for future in as_completed(future_to_job):
            mode, n = future_to_job[future]
            try:
                res = future.result()
                all_results.append(res)
                completed += 1
                sim_speed = (
                    res["sim_duration_s"] / res["simulation_wall_time_s"]
                    if res["simulation_wall_time_s"] > 0
                    else 0.0
                )
                overall_pct = 100.0 * completed / total_jobs
                elapsed_wall = time.time() - started_at

                print(
                    f"[DONE] mode={mode}, N={n}, "
                    f"unique_pairs={res['total_unique_collision_pairs']}, "
                    f"wall_time={res['simulation_wall_time_s']:.1f}s, "
                    f"sim_speed={sim_speed:.1f}x realtime, "
                    f"overall_progress={overall_pct:.1f}%, "
                    f"total_wall_elapsed={elapsed_wall/60.0:.1f} min"
                )
            except Exception as e:
                print(f"[ERROR] mode={mode}, N={n}: {e}")

    # Aggregate results into a single JSON for easy plotting
    summary_path = os.path.join(EXPERIMENT_ROOT, "summary_results.json")
    with open(summary_path, "w") as f:
        json.dump(all_results, f, indent=4)

    print(f"\nAll experiments completed. Summary saved to {summary_path}")


if __name__ == "__main__":
    run_all_experiments()

