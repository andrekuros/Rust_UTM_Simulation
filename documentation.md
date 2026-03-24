# UTM Simulation Models Documentation

**Extended report (DAIDALUS, avoidance modes, experiments, config):** see [`documentation/DAIDALUS_AVOIDANCE_AND_EXPERIMENTS_REPORT.md`](documentation/DAIDALUS_AVOIDANCE_AND_EXPERIMENTS_REPORT.md).

## Overview
The **UTM_Sim_Models** project provides a highly scalable drone Unmanned Traffic Management (UTM) simulation engine built in Rust using the Bevy ECS framework and Rapier physics. It integrates the NASA Daidalus (Detect and Avoid Alerting Logic for Unmanned Systems) library for continuous collision monitoring and alerting.

## Core Components
### 1. Scenario Generator (`src/bin/scenario_gen.rs`)
A standalone CLI tool that generates dynamic simulated UTM airspaces.
- **Inputs**: Number of drones.
- **Configurable Parameters**: 
  - Airspace Dimensions: $5km \times 5km$ ($5000 \times 5000$ meters) and $1000m$ in altitude.
  - Departure & Landing Pads: Specific 3D coordinates.
  - Performance: Random speeds (10-30 m/s), flight levels, and constraints.
- **Output**: Serializes to `config/scenario_dynamic.json` containing `DroneConfig` and `ObstacleConfig`.

### 2. Main Simulation Engine (`src/main.rs`)
The engine leverages Bevy ECS to spawn entities based on the scenario JSON.
- **Agents**: Each drone is modeled as an entity with `Drone`, `DronePerformance`, `FlightPlan`, and `Transform` components.
- **Physics**: Bevy Rapier3D handles kinematic movements and spatial queries.
- **Timeout System**: Runs a fast-forwarded or real-time loop for a pre-defined interval (e.g., 60 seconds) and automatically exits gracefully.

### 3. Daidalus Integration (`src/daidalus/mod.rs`)
Connects the C++ Daidalus Library to the Rust backend to assert safety boundaries.
- Uses the `cxx` crate to build a safe C++ to Rust bridge.
- Calculates spatial proximity and issues simulated or real NASA DAIDALUS alerts.
- A Bevy system periodically passes drone coordinates to the Daidalus wrapper to collect and log alerts.

### 4. Telemetry Logging (`src/core/logger.rs`)
Captures high-frequency data for off-line playback.
- **Frequency**: 1 Hz (Configurable).
- **Data Logged**: Elapsed time, Drone ID, 3D Position $(X, Y, Z)$.
- **Thread-Safety**: Uses a `lazy_static` Mutex to push logs concurrently across Bevy systems.
- **Serialization**: Dumps an array of `TelemetryEntry` to `simulation_telemetry.json` right before the application (`AppExit`) closes.

### 5. Playback Viewer (`viewer/index.html`)
A standalone, zero-dependency HTML/JavaScript WebGL viewer using Three.js.
- Loads `simulation_telemetry.json`.
- Renders the entire UTM environment, mapping drone IDs to 3D meshes.
- Includes a UI scrubber to rewind and fast-forward the simulation playback visually.

## Experimentation and Automation
The repository includes an `experiment.py` script designed to automate test runs.
- **Purpose**: Compare collision frequency across variable Drone Densities.
- **Process**: Iterates over configurations (e.g., 10, 50, 100, 200 drones). For each iteration:
  1. Generates the respective `scenario_dynamic.json`.
  2. Runs the compiled `hpm_utm_simulator` release binary for 60 seconds.
  3. Parses `stdout` to count Daidalus collision alerts and tracks Telemetry lines.
- **Output**: Saves aggregated metrics to `experiment_results.json`.

## Experiment Results (Summary)
The following table summarizes the findings from the automated experiment (60s runs):

| Drone Count | Pairs Checked | Total Collision Alerts | FPS (est.) | Telemetry Records |
|-------------|---------------|------------------------|------------|-------------------|
| 10          | 45            | 17.6M                  | 6500       | 600               |
| 50          | 1225          | 39.3M                  | 530        | 3000              |
| 100         | 4950          | 40.9M                  | 137        | 6000              |
| 200         | 19900         | 38.5M                  | 32         | 12000             |

**Observations**:
- The bottleneck for scalability in this phase is the output printing and $O(N^2)$ proximity checks.
- Telemetry logging remained highly efficient and linear.
- Total alerts peaked around 100 drones, likely due to saturation of the $500m$ safety radius within the $5km$ box.

## Extending the Platform
Developers can seamlessly add new sensors (e.g., Lidar, Acoustic) by implementing components inside `src/sensors/` and plugging them into the `SensorSuite`.
