# Plan: Default City Scenario and Simulation Features

## 1. Default scenario – city with rectangular no-fly zones (buildings)

- **Scene layout**
  - Add a **default scenario** (e.g. `config/scenario_city_default.json`) used when no dynamic scenario is specified (or make it selectable in sim config).
  - **No-fly zones (NFZ)** as **rectangular boxes** (buildings): extend `ObstacleConfig` / scenario JSON to support `"Box"` with `dimensions: [length_x, height_y, depth_z]` and `position` (already supported in code; ensure rendering uses grey boxes).
  - **City density**
    - **Central area**: higher density of rectangular NFZs (grid of blocks), smaller spacing.
    - **Periphery**: fewer/smaller NFZs, more open; density falls off with distance from center (e.g. by radial bands or a simple 2D density function).
  - **Rendering**: ensure obstacles with `geometry_type: "Box"` are drawn as grey rectangular meshes (no-fly zones = buildings). Keep a single representation (Box = building).

- **Drone routes**
  - Routes must **avoid buildings and NFZs**: waypoint generation (in `scenario_gen` or a city-specific generator) must:
    - Use **rectangular** intersection checks for Box NFZs (not only cylinder).
    - Build waypoints that go around buildings (e.g. A* or simple detour waypoints so segments do not intersect any NFZ).

---

## 2. Drone departure schedule (staggered start times)

- **Config**
  - In **sim config** (e.g. `sim_config.json` under `simulation` or `scenario`), add a **departure schedule**:
    - Option A: per-drone `departure_time_s` in the **scenario** JSON (each drone has `departure_time_s: f32`).
    - Option B: in **sim_config**, e.g. `departure_schedule: "uniform" | "random"` plus `time_window` (already exists), and generator spreads departures over `[0, time_window]`.
- **Runtime**
  - **Do not spawn** drones at simulation start; spawn when `sim_time >= departure_time_s` (use a system that checks `Time::elapsed_seconds()` and spawns from a “pending” list, or spawn with a `ScheduledDeparture { at: f32 }` and keep drones inactive until that time).
  - **Movement**: drone movement (e.g. `drone_movement_system`) runs only when `elapsed >= departure_time` for that drone (add a component or field “active from time”).

**Result**: Drones depart at different times over the simulation, not all at t=0.

---

## 3. Drone characteristics for Daidalus (dynamic avoid zones)

- **Model**
  - Extend **`DronePerformance`** (and scenario/sim config) with Daidalus-relevant parameters, e.g.:
    - `max_speed_mps` (already present)
    - `max_vertical_speed_mps` (climb/sink)
    - `max_turn_rate_deg_s` or `min_turn_radius_m`
    - Optional: `bank_angle_deg`, `acceleration_mps2`
  - These are used when calling Daidalus (or the C++ bridge) to compute **kinematic bands** and dynamic avoid zones per aircraft.

- **Daidalus bridge**
  - Extend **`daidalus_bridge`** (and Rust `DaidalusBridge`) to accept per-aircraft parameters (speed, vertical speed, turn rate) and return bands or conflict information. The current C++ wrapper is a stub; plan to pass aircraft state + performance and use it in `get_kinematic_bands()` or equivalent.

---

## 4. Reactive drones (configurable)

- **Config**
  - In **sim config** (e.g. `simulation`), add a flag: `reactive_drones: bool` (default e.g. `false`).
- **Behavior**
  - When `reactive_drones: true` and **Daidalus** (or internal collision logic) raises an **alert** for a drone:
    - That drone switches to a **reactive avoidance** behavior: e.g. insert an avoidance waypoint or apply an evasive maneuver (e.g. from Daidalus bands: turn/climb) instead of blindly following the original plan.
  - Implementation: a system that reads `ActiveCollisions` (and optionally Daidalus bands), and for each involved drone with “reactive” enabled, updates `FlightPlan` (e.g. insert waypoint) or sets a short-term “avoidance” target. Keep logic in one place (e.g. `core` or `daidalus`).

---

## 5. Departure zones = landing areas; collision alerts off nearby

- **Zones**
  - Define **departure/landing zones** as **rectangular areas** (side-by-side), not just points:
    - In **ScenarioMetadata** (or config): e.g. `departure_landing_zones: Vec<{ name, min: [x,z], max: [x,z], height_max? }>`.
  - First waypoint of each drone lies in one zone; last waypoint (landing) in another (or same) zone. Scenario generator already uses “departures” and “landings”; extend to **rectangles** so multiple drones can use the same zone.

- **Collision alerts**
  - **Deactivate** Daidalus/collision alerts when **both** aircraft are inside a **departure/landing zone** (or within a small margin of it). In `daidalus_monitoring_system` (or where `check_collisions` is used): before adding an alert, check if both `drone_a` and `drone_b` are inside any `departure_landing_zone`; if yes, skip that pair.

---

## 6. Fixed-wing aircraft

- **Model**
  - Add an **aircraft type** (e.g. `VehicleType: Rotorcraft | FixedWing`) on the agent (e.g. `Drone` renamed to `Vehicle` or add `AircraftKind` component). Fixed-wing has different performance (e.g. min speed, different turn rate, climb rate).
- **Performance**
  - **DronePerformance** (or a shared “AircraftPerformance”) already has speed; add/use **max_turn_rate**, **min_speed_mps** for fixed-wing. Different params in scenario/config per vehicle type.
- **Daidalus**
  - Collision alerts and bands **depend on Daidalus** and aircraft type: pass fixed-wing vs rotorcraft into the Daidalus bridge so that different BADA-like or performance models can be used (even if the C++ side is still a stub, the interface should accept type/performance).

---

## 7. City look: dense center, open periphery

- **Generation**
  - In the **default city scenario** (or `scenario_gen` for city mode):
    - Define a **center** (e.g. `[0,0]` in XZ).
    - **Building density**: function of distance from center (e.g. number of boxes per unit area decreases with radius).
    - **Central area**: e.g. radius 500–800 m, high density (grid of rectangles, grey NFZs).
    - **Mid**: medium density.
    - **Periphery**: few or no buildings, open.
  - **Departure/landing zones**: place at the **edges** of the city (e.g. side-by-side rectangles in the “open” area) so routes go from edge → center → edge or similar, avoiding the dense center or crossing through gaps.

---

## Implementation order (suggested)

1. **Config and scenario format**: departure schedule (per-drone time), departure/landing rectangles, `reactive_drones`, NFZ as Box; city default scenario JSON schema.
2. **City scenario content**: default scenario with rectangular NFZs, density (center dense, periphery open).
3. **Scenario generator**: rectangular NFZ avoidance, departure time spread, use of departure/landing zones.
4. **Runtime**: spawn drones by schedule; deactivate collision in departure/landing zones; optional reactive avoidance when `reactive_drones: true`.
5. **Drone/aircraft model**: Daidalus-related performance params; fixed-wing type and params; wire Daidalus bridge to use them.
6. **Rendering**: grey boxes for Box obstacles so the scene clearly looks like a city.

---

## Files to touch (summary)

| Area | Files |
|------|--------|
| Config / scenario | `config/sim_config.json`, `config/scenario_city_default.json` (new), `src/main.rs` (ScenarioData, load_scenario, config parsing) |
| Schedule / spawn | `src/main.rs` (spawn by time), `src/core/mod.rs` (movement only when active) |
| Agents | `src/agents/mod.rs` (DronePerformance + Daidalus params, VehicleType or FixedWing) |
| Daidalus | `src/daidalus/mod.rs` (reactive logic, zone exclusion), C++ bridge (params, bands) |
| Metadata | `src/main.rs` (ScenarioMetadata: departure_landing_zones) |
| Generator | `src/bin/scenario_gen.rs` (rectangles, density, departure times, Box NFZ avoidance) |
| Rendering | Wherever obstacles are drawn: ensure Box → grey rectangular mesh |

This keeps the plan in one place and avoids creating many small docs.
