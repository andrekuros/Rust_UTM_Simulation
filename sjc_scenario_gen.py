#!/usr/bin/env python3
"""
SJC Scenario Generator for Rust/DAIDALUS xTM experiments.

Generates Rust-compatible scenario JSONs that match the Python xTM experiments
(testeprimordial 1-4B) using equirectangular projection from SJC lat/lon to
Cartesian XYZ metres.  Also performs xTM 4D tube pre-computation for Scenarios
3, 4A and 4B, outputting departure delays in the scenario.

Usage:
    python sjc_scenario_gen.py --scenario 1 --num_drones 50 --output_dir runs/sc1_50
"""

import argparse
import json
import math
import os
import random
import heapq
from typing import List, Tuple, Dict, Optional

# ── Constants matching Python experiments ───────────────────────────────

R_EARTH = 6_371_000.0

SJC_GEOFENCE_LATLON = [
    (-23.1500, -45.9700),
    (-23.1300, -45.7500),
    (-23.2800, -45.7500),
    (-23.2800, -45.9700),
]

RESTRICTED_AREA_LATLON = [
    (-23.207232, -45.886221),
    (-23.246663, -45.860730),
    (-23.221120, -45.839731),
    (-23.192784, -45.867164),
]

AVOIDANCE_CORNERS_LATLON = [
    (-23.204232, -45.889221),
    (-23.249663, -45.863730),
    (-23.224120, -45.836731),
    (-23.189784, -45.864164),
]

HORIZONTAL_SPEED = 15.3  # m/s
VERTICAL_SPEED = 3.0     # m/s
ALT_MIN, ALT_MAX = 30.0, 50.0
IDLE_TIMER_INITIAL_MAX = 120.0  # first idle 0-120 s
IDLE_TIMER_CYCLE = 300.0        # 5 min between missions
MAX_MISSION_DISTANCE = 12_000.0 # metres (sc2+)
SIM_DURATION = 28_800.0         # 8 hours

# xTM tube parameters per scenario
XTM_PARAMS = {
    3:   {"sep_h": 30.0, "sep_v": 15.0, "time_buf": 0},
    "4a": {"sep_h": 22.0, "sep_v": 12.0, "time_buf": 0},
    "4b": {"sep_h": 30.0, "sep_v": 15.0, "time_buf": 2},
}

# Projection reference point (centre of SJC geofence)
REF_LAT = -23.21
REF_LON = -45.86

# ── Coordinate helpers ──────────────────────────────────────────────────

def latlon_to_xy(lat: float, lon: float) -> Tuple[float, float]:
    """Equirectangular projection: returns (x_east, z_south) in metres."""
    x = (lon - REF_LON) * math.radians(1) * R_EARTH * math.cos(math.radians(REF_LAT))
    z = -(lat - REF_LAT) * math.radians(1) * R_EARTH  # negative so north is -Z
    return x, z

def fast_distance_m(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
    return R_EARTH * math.sqrt(dlat * dlat + dlon * dlon)

def point_in_polygon(lat, lon, polygon):
    """Ray-casting algorithm. Polygon is list of (lat, lon) tuples."""
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        lat_i, lon_i = polygon[i]
        lat_j, lon_j = polygon[j]
        if ((lat_i > lat) != (lat_j > lat)) and \
           (lon < (lon_j - lon_i) * (lat - lat_i) / (lat_j - lat_i) + lon_i):
            inside = not inside
        j = i
    return inside

def random_point_in_geofence(geofence=SJC_GEOFENCE_LATLON, exclude_restricted=False):
    lats = [p[0] for p in geofence]
    lons = [p[1] for p in geofence]
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    for _ in range(10_000):
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        if point_in_polygon(lat, lon, geofence):
            if exclude_restricted and point_in_polygon(lat, lon, RESTRICTED_AREA_LATLON):
                continue
            return lat, lon
    raise RuntimeError("Could not find a valid point inside geofence")

# ── Dijkstra routing around restricted area ─────────────────────────────

def segments_cross(a1, a2, b1, b2):
    """Check if segment a1-a2 crosses segment b1-b2 (lat/lon tuples)."""
    def cross2d(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1 = cross2d(b1, b2, a1)
    d2 = cross2d(b1, b2, a2)
    d3 = cross2d(a1, a2, b1)
    d4 = cross2d(a1, a2, b2)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False

def line_crosses_polygon(p1, p2, polygon):
    n = len(polygon)
    for i in range(n):
        if segments_cross(p1, p2, polygon[i], polygon[(i + 1) % n]):
            return True
    return False

def route_around_restricted(origin_ll, dest_ll):
    """Dijkstra shortest path around restricted area, returns list of (lat,lon) waypoints."""
    if not line_crosses_polygon(origin_ll, dest_ll, RESTRICTED_AREA_LATLON):
        return [dest_ll]

    nodes = [origin_ll, dest_ll] + AVOIDANCE_CORNERS_LATLON
    n = len(nodes)
    adj = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if not line_crosses_polygon(nodes[i], nodes[j], RESTRICTED_AREA_LATLON):
                d = fast_distance_m(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1])
                adj[i].append((j, d))
                adj[j].append((i, d))

    dist = [float("inf")] * n
    prev = [-1] * n
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))

    path = []
    cur = 1  # destination index
    while cur != 0 and cur != -1:
        path.append(nodes[cur])
        cur = prev[cur]
    path.reverse()
    return path  # excludes origin, includes destination

# ── xTM 4D Tube Reservation ────────────────────────────────────────────

class XtmCentral:
    def __init__(self, sep_h: float, sep_v: float, time_buf: int = 0):
        self.sep_h = sep_h
        self.sep_v = sep_v
        self.time_buf = time_buf
        self.reservations: Dict[int, Dict[Tuple[int, int], List]] = {}

    def _grid_key(self, x: float, z: float) -> Tuple[int, int]:
        return (int(x / 50.0), int(z / 50.0))

    def simulate_trajectory(self, start_tick, origin_xy, dest_xy, waypoints_xy,
                            cruise_alt, speed=HORIZONTAL_SPEED, vspeed=VERTICAL_SPEED):
        """Simulate tick-by-tick trajectory, returns list of (tick, x, y_alt, z)."""
        traj = []
        x, y, z = origin_xy[0], 0.0, origin_xy[1]
        tick = start_tick
        dt = 1.0

        # Takeoff
        while y < cruise_alt:
            y = min(y + vspeed * dt, cruise_alt)
            traj.append((tick, x, y, z))
            tick += 1

        # Cruise through waypoints
        for wp_x, wp_z in waypoints_xy:
            while True:
                dx = wp_x - x
                dz = wp_z - z
                dist = math.sqrt(dx * dx + dz * dz)
                if dist < speed * dt:
                    x, z = wp_x, wp_z
                    traj.append((tick, x, y, z))
                    tick += 1
                    break
                ratio = speed * dt / dist
                x += dx * ratio
                z += dz * ratio
                traj.append((tick, x, y, z))
                tick += 1

        # Landing
        while y > 0:
            y = max(y - vspeed * dt, 0.0)
            traj.append((tick, x, y, z))
            tick += 1

        return traj

    def request_flight_plan(self, drone_id, start_tick, trajectory):
        """Check trajectory against existing reservations. Returns True if no conflict."""
        for (tick, x, y, z) in trajectory:
            check_ticks = range(tick - self.time_buf, tick + self.time_buf + 1)
            gx, gz = self._grid_key(x, z)
            for ct in check_ticks:
                if ct not in self.reservations:
                    continue
                for dgx in range(gx - 1, gx + 2):
                    for dgz in range(gz - 1, gz + 2):
                        for (rid, rx, ry, rz) in self.reservations.get(ct, {}).get((dgx, dgz), []):
                            if rid == drone_id:
                                continue
                            dh = math.sqrt((x - rx) ** 2 + (z - rz) ** 2)
                            dv = abs(y - ry)
                            if dh < self.sep_h and dv < self.sep_v:
                                return False
        # Approved — store reservations
        for (tick, x, y, z) in trajectory:
            gk = self._grid_key(x, z)
            self.reservations.setdefault(tick, {}).setdefault(gk, []).append(
                (drone_id, x, y, z)
            )
        return True

# ── Mission generation ──────────────────────────────────────────────────

def generate_missions(num_drones: int, scenario: str, seed: int = 42):
    """
    Generate all missions for `num_drones` physical drones over SIM_DURATION.
    Returns list of drone configs (each a dict ready for Rust scenario JSON)
    and a dict of metrics (delays, ideal distances, etc).
    """
    random.seed(seed)
    use_restricted = scenario in ("3", "4a", "4b")
    use_xtm = scenario in ("3", "4a", "4b")

    xtm = None
    if use_xtm:
        key = int(scenario) if scenario == "3" else scenario
        params = XTM_PARAMS[key]
        xtm = XtmCentral(params["sep_h"], params["sep_v"], params["time_buf"])

    drones_out = []
    delays = []
    ideal_distances = []
    mission_counter = 0

    for drone_idx in range(num_drones):
        phys_id = f"UAV_{drone_idx:05d}"
        current_tick = int(random.uniform(0, IDLE_TIMER_INITIAL_MAX))
        # Random starting position
        start_lat, start_lon = random_point_in_geofence(exclude_restricted=use_restricted)
        cur_lat, cur_lon = start_lat, start_lon

        while current_tick < SIM_DURATION:
            # Pick destination
            for _ in range(500):
                dest_lat, dest_lon = random_point_in_geofence(exclude_restricted=use_restricted)
                d = fast_distance_m(cur_lat, cur_lon, dest_lat, dest_lon)
                if scenario != "1" and d > MAX_MISSION_DISTANCE:
                    continue
                if d > 100:  # avoid trivially short missions
                    break

            cruise_alt = random.uniform(ALT_MIN, ALT_MAX)
            ideal_dist = fast_distance_m(cur_lat, cur_lon, dest_lat, dest_lon)

            # Compute waypoints (Dijkstra routing for restricted-area scenarios)
            if use_restricted:
                wp_latlon = route_around_restricted((cur_lat, cur_lon), (dest_lat, dest_lon))
            else:
                wp_latlon = [(dest_lat, dest_lon)]

            origin_xy = latlon_to_xy(cur_lat, cur_lon)
            wp_xy = [latlon_to_xy(lat, lon) for lat, lon in wp_latlon]
            dest_xy = wp_xy[-1]

            # xTM reservation
            delay_s = 0
            if xtm is not None:
                traj = xtm.simulate_trajectory(
                    current_tick, origin_xy, dest_xy, wp_xy, cruise_alt
                )
                approved = xtm.request_flight_plan(
                    f"{phys_id}_m{mission_counter}", current_tick, traj
                )
                retry = 0
                while not approved and retry < 200:
                    delay_s += 15
                    current_tick += 15
                    if current_tick >= SIM_DURATION:
                        break
                    traj = xtm.simulate_trajectory(
                        current_tick, origin_xy, dest_xy, wp_xy, cruise_alt
                    )
                    approved = xtm.request_flight_plan(
                        f"{phys_id}_m{mission_counter}", current_tick, traj
                    )
                    retry += 1
                if current_tick >= SIM_DURATION:
                    break

            delays.append(delay_s)
            ideal_distances.append(ideal_dist)

            # Build waypoint list for Rust: [ground, takeoff, cruise_wps..., landing_ground]
            rust_waypoints = []
            ox, oz = origin_xy
            rust_waypoints.append([ox, 0.0, oz])      # ground start
            rust_waypoints.append([ox, cruise_alt, oz]) # takeoff
            for (wx, wz) in wp_xy:
                rust_waypoints.append([wx, cruise_alt, wz])
            dx, dz = dest_xy
            rust_waypoints.append([dx, 0.0, dz])      # landing to ground

            # Estimate flight duration
            flight_time = cruise_alt / VERTICAL_SPEED  # takeoff
            prev = origin_xy
            for (wx, wz) in wp_xy:
                seg = math.sqrt((wx - prev[0]) ** 2 + (wz - prev[1]) ** 2)
                flight_time += seg / HORIZONTAL_SPEED
                prev = (wx, wz)
            flight_time += cruise_alt / VERTICAL_SPEED  # landing

            drone_cfg = {
                "id": f"{phys_id}_m{mission_counter}",
                "performance": {
                    "mass_kg": 1.5,
                    "max_speed_mps": HORIZONTAL_SPEED,
                    "max_vertical_speed_mps": VERTICAL_SPEED,
                    "battery_discharge_rate": 10.0,
                },
                "flight_plan": {
                    "waypoints": rust_waypoints,
                    "current_waypoint_index": 0,
                },
                "departure_time_s": float(current_tick),
            }
            drones_out.append(drone_cfg)
            mission_counter += 1

            # Advance time: flight + idle
            current_tick += int(flight_time) + int(IDLE_TIMER_CYCLE)
            cur_lat, cur_lon = dest_lat, dest_lon

    # Build per-entity ideal distance map
    ideal_dist_by_id = {}
    for i, d in enumerate(drones_out):
        ideal_dist_by_id[d["id"]] = ideal_distances[i]

    metrics_info = {
        "total_missions": mission_counter,
        "mean_delay_s": sum(delays) / len(delays) if delays else 0,
        "mean_ideal_distance_m": sum(ideal_distances) / len(ideal_distances) if ideal_distances else 0,
        "delays": delays,
        "ideal_distances": ideal_distances,
        "ideal_dist_by_id": ideal_dist_by_id,
    }

    return drones_out, metrics_info

# ── Avoidance mode mapping ──────────────────────────────────────────────

# Matches testeprimordial*.py tactical layer (geometric DAA only — no NASA DAIDALUS).
SCENARIO_AVOIDANCE = {
    "1": "None",
    "2": "Python2",
    "3": "None",
    "4a": "Python4a",
    "4b": "Python4b",
}

# ── Output generation ───────────────────────────────────────────────────

def write_scenario(output_dir: str, scenario: str, num_drones: int, seed: int = 42,
                    log_interval: float = 5.0, log_level: str = "metrics",
                    physics_hz: float = 1.0):
    os.makedirs(os.path.join(output_dir, "config"), exist_ok=True)

    drones, metrics_info = generate_missions(num_drones, scenario, seed=seed)

    scenario_data = {
        "drones": drones,
        "obstacles": [],
        "departure_landing_zones": [],
    }
    scenario_path = os.path.join(output_dir, "config", "scenario_dynamic.json")
    with open(scenario_path, "w") as f:
        json.dump(scenario_data, f)

    sim_config = {
        "simulation": {
            "duration": SIM_DURATION,
            "collision_threshold": 20.0,
            "show_progress_bar": True,
            "avoidance_mode": SCENARIO_AVOIDANCE[scenario],
            "scenario_file": "config/scenario_dynamic.json",
            "enable_mqtt": False,
            "log_level": log_level,
            "log_interval_s": log_interval,
            "physics_hz": physics_hz,
            "daa_interval_s": 1.0,
        },
    }
    config_path = os.path.join(output_dir, "config", "sim_config.json")
    with open(config_path, "w") as f:
        json.dump(sim_config, f, indent=2)

    # Save generation metrics for the analyzer
    meta_path = os.path.join(output_dir, "generation_metrics.json")
    summary = {
        "scenario": scenario,
        "num_physical_drones": num_drones,
        "total_missions": metrics_info["total_missions"],
        "total_drone_entities": len(drones),
        "mean_xtm_delay_s": metrics_info["mean_delay_s"],
        "mean_ideal_distance_m": metrics_info["mean_ideal_distance_m"],
        "delays": metrics_info["delays"],
        "ideal_distances": metrics_info["ideal_distances"],
        "ideal_dist_by_id": metrics_info["ideal_dist_by_id"],
    }
    with open(meta_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Generated scenario {scenario} with {num_drones} drones "
          f"({len(drones)} entities, {metrics_info['total_missions']} missions) "
          f"in {output_dir}")
    return summary


def main():
    parser = argparse.ArgumentParser(description="SJC xTM scenario generator")
    parser.add_argument("--scenario", required=True, choices=["1", "2", "3", "4a", "4b"])
    parser.add_argument("--num_drones", type=int, required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--log_interval", type=float, default=5.0,
                        help="Telemetry logging interval in seconds (default 5s)")
    parser.add_argument("--log_level", default="metrics",
                        choices=["metrics", "compact", "full"],
                        help="Rust log level: metrics (no NDJSON), compact (events), full (periodic)")
    parser.add_argument("--physics_hz", type=float, default=1.0,
                        help="Physics tick rate in Hz (Python uses 1Hz, default 1)")
    args = parser.parse_args()

    write_scenario(args.output_dir, args.scenario, args.num_drones,
                   seed=args.seed, log_interval=args.log_interval,
                   log_level=args.log_level, physics_hz=args.physics_hz)


if __name__ == "__main__":
    main()
