use bevy::prelude::*;
use serde::Serialize;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::sync::Mutex;
use lazy_static::lazy_static;
use std::collections::{HashMap, HashSet};

lazy_static! {
    static ref TELEMETRY_WRITER: Mutex<Option<BufWriter<File>>> = Mutex::new(None);
    static ref TELEMETRY_COUNT: Mutex<u64> = Mutex::new(0);
}

// ── Log level ──────────────────────────────────────────────────────────

/// Three logging tiers:
///  - **Metrics**: no NDJSON file at all; only in-simulation counters
///    (MACproxy, DAA alerts, completed missions) written to `sim_metrics.json`.
///  - **Compact**: event-based NDJSON (state changes only). Small files,
///    enough for the 3D viewer and basic analysis.
///  - **Full**: periodic NDJSON at `interval_s`. Large files, full replay
///    fidelity. Use only when you need the viewer *and* position-level data.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LogLevel {
    Metrics,
    Compact,
    Full,
}

// ── Shared serialisation types ─────────────────────────────────────────

#[derive(Serialize, Clone)]
pub struct CollisionLog {
    pub other_drone_id: String,
    pub distance: f32,
    pub alert_level: i32,
    pub time_to_violation: f32,
    pub min_safe_heading: f32,
    pub max_safe_heading: f32,
}

#[derive(Serialize, Clone)]
pub struct TelemetryEntry {
    pub time_elapsed: f32,
    pub drone_id: String,
    pub position: [f32; 3],
    #[serde(skip_serializing_if = "Option::is_none")]
    pub velocity: Option<[f32; 3]>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub flight_state: Option<String>,
    /// True when `ReactiveAvoidance.target` is set (lateral virtual waypoint active).
    /// Compare with `collision_alerts`: alerts without reactive target indicate DAA saw traffic
    /// but steering did not engage (e.g. final-approach guard, cooldown, or filter mismatch).
    #[serde(default)]
    pub has_reactive_target: bool,
    pub collision_alerts: Vec<CollisionLog>,
}

#[derive(Serialize)]
pub struct TelemetryData {
    pub metadata: crate::ScenarioMetadata,
    pub frames: Vec<TelemetryEntry>,
}

// ── Config resource ────────────────────────────────────────────────────

#[derive(Resource)]
pub struct LoggerConfig {
    pub level: LogLevel,
    pub interval_s: f32,
}

impl Default for LoggerConfig {
    fn default() -> Self {
        Self { level: LogLevel::Compact, interval_s: 5.0 }
    }
}

// ── In-simulation metrics (MACproxy etc.) ──────────────────────────────

const MACPROXY_H: f32 = 20.0;
const MACPROXY_V: f32 = 10.0;
const MACPROXY_RESET_H: f32 = 40.0;

#[derive(Resource, Default)]
pub struct SimMetrics {
    pub macproxy_count: u32,
    pub macproxy_active: HashSet<(String, String)>,
    pub daa_alert_pairs: HashSet<(String, String)>,
    pub completed_missions: u32,
    /// Set from scenario at load (`scenario.drones.len()`).
    pub total_scheduled_missions: u32,
    pub total_real_distance: f64,
    pub total_ideal_distance: f64,
    /// Filled on exit: why missions were still incomplete at `duration` (not spawned, or still in world).
    pub incomplete_missions_by_reason: HashMap<String, u32>,
    drone_last_pos: HashMap<String, Vec3>,
}

fn ordered_pair(a: &str, b: &str) -> (String, String) {
    if a < b { (a.to_string(), b.to_string()) } else { (b.to_string(), a.to_string()) }
}

// ── Plugin ─────────────────────────────────────────────────────────────

pub struct LoggerPlugin;

impl Plugin for LoggerPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<LoggerConfig>()
           .init_resource::<LogTimer>()
           .init_resource::<SimMetrics>()
           .add_systems(Startup, init_logging)
           .add_systems(Update, macproxy_system)
           // After Daidalus reactive_avoidance_system (Update) so has_reactive_target matches steering.
           .add_systems(Last, telemetry_system)
           .add_systems(Last, export_on_exit);
    }
}

#[derive(Resource)]
struct LogTimer(Timer);

impl Default for LogTimer {
    fn default() -> Self {
        Self(Timer::from_seconds(5.0, TimerMode::Repeating))
    }
}

// ── Startup ────────────────────────────────────────────────────────────

fn init_logging(
    metadata: Res<crate::ScenarioMetadata>,
    cfg: Res<LoggerConfig>,
    mut timer: ResMut<LogTimer>,
) {
    timer.0.set_duration(std::time::Duration::from_secs_f32(cfg.interval_s));
    timer.0.reset();

    if cfg.level == LogLevel::Metrics {
        // No NDJSON file at all — fastest mode
        return;
    }

    if let Ok(file) = File::create("simulation_telemetry.ndjson") {
        let mut writer = BufWriter::with_capacity(256 * 1024, file);
        let meta_json = serde_json::json!({ "metadata": (*metadata).clone() });
        if let Ok(json) = serde_json::to_string(&meta_json) {
            let _ = writeln!(writer, "{}", json);
        }
        *TELEMETRY_WRITER.lock().unwrap() = Some(writer);
    }
}

// ── MACproxy system (runs every tick, cheap) ───────────────────────────

fn macproxy_system(
    route_cfg: Res<crate::core::route_metrics::RouteMetricsConfig>,
    mut query: Query<(
        &crate::agents::Drone,
        &Transform,
        &crate::agents::Velocity,
        &crate::agents::FlightState,
        &mut crate::core::route_metrics::MissionRouteMetrics,
    )>,
    metadata: Res<crate::ScenarioMetadata>,
    landing_ignore: Res<crate::daidalus::LandingCollisionIgnoreConfig>,
    active_collisions: Res<crate::daidalus::ActiveCollisions>,
    mut metrics: ResMut<SimMetrics>,
) {
    use crate::core::route_metrics::RouteMetricsTiming;

    // Track distance for all moving drones
    for (drone, transform, _vel, _state, mut route) in query.iter_mut() {
        let pos = transform.translation;
        match route_cfg.timing {
            RouteMetricsTiming::Spawn => {
                if let Some(last) = metrics.drone_last_pos.get(&drone.id) {
                    let d = pos.distance(*last);
                    if d < 500.0 {
                        // sanity cap to ignore teleports
                        metrics.total_real_distance += d as f64;
                    }
                }
                metrics.drone_last_pos.insert(drone.id.clone(), pos);
            }
            RouteMetricsTiming::MissionComplete => {
                if let Some(last) = route.last_pos {
                    let d = pos.distance(last);
                    if d < 500.0 {
                        route.real_m += d as f64;
                    }
                }
                route.last_pos = Some(pos);
            }
        }
    }

    // Track DAA alert pairs
    for alert in active_collisions.alerts.iter() {
        if alert.alert_level > 0 {
            let pair = ordered_pair(&alert.drone_a, &alert.drone_b);
            metrics.daa_alert_pairs.insert(pair);
        }
    }

    // MACproxy: check all airborne pairs using spatial hashing
    let airborne: Vec<(String, Vec3)> = query.iter()
        .filter(|(_, t, _, _, _)| t.translation.y >= 5.0)
        .map(|(d, t, _, _, _)| (d.id.clone(), t.translation))
        .collect();

    let cell = 50.0_f32;
    let mut grid: HashMap<(i32, i32), Vec<usize>> = HashMap::new();
    for (i, (_, pos)) in airborne.iter().enumerate() {
        let cx = (pos.x / cell).floor() as i32;
        let cz = (pos.z / cell).floor() as i32;
        grid.entry((cx, cz)).or_default().push(i);
    }

    let mut check = |i: usize, j: usize| {
        let (ref id_a, pos_a) = airborne[i];
        let (ref id_b, pos_b) = airborne[j];
        if crate::daidalus::landing_collision_pair_ignored(
            metadata.as_ref(),
            pos_a,
            pos_b,
            landing_ignore.as_ref(),
        ) {
            return;
        }
        let dh = ((pos_a.x - pos_b.x).powi(2) + (pos_a.z - pos_b.z).powi(2)).sqrt();
        let dv = (pos_a.y - pos_b.y).abs();
        let pair = ordered_pair(id_a, id_b);

        if dh < MACPROXY_H && dv < MACPROXY_V {
            if !metrics.macproxy_active.contains(&pair) {
                metrics.macproxy_active.insert(pair.clone());
                metrics.macproxy_count += 1;
            }
        } else if dh > MACPROXY_RESET_H {
            metrics.macproxy_active.remove(&pair);
        }
    };

    for (&(cx, cz), idxs) in grid.iter() {
        for i in 0..idxs.len() {
            for j in (i + 1)..idxs.len() {
                check(idxs[i], idxs[j]);
            }
        }
        for &(dx, dz) in &[(1,0),(0,1),(1,1),(1,-1)] {
            if let Some(nbr) = grid.get(&(cx + dx, cz + dz)) {
                for &a in idxs {
                    for &b in nbr {
                        check(a, b);
                    }
                }
            }
        }
    }
}

// ── Telemetry system (NDJSON writing) ──────────────────────────────────

struct DroneLogState {
    wp_idx: usize,
    has_avoidance: bool,
    alerts: Vec<String>,
}

fn write_entry(entry: &TelemetryEntry) {
    if let Ok(mut guard) = TELEMETRY_WRITER.lock() {
        if let Some(ref mut writer) = *guard {
            if let Ok(json) = serde_json::to_string(entry) {
                let _ = writeln!(writer, "{}", json);
                *TELEMETRY_COUNT.lock().unwrap() += 1;
            }
        }
    }
}

fn build_alerts_for_drone(
    drone_id: &str,
    active_collisions: &crate::daidalus::ActiveCollisions,
) -> (Vec<CollisionLog>, Vec<String>) {
    let mut alerts = Vec::new();
    let mut alert_ids = Vec::new();
    for alert in active_collisions.alerts.iter() {
        let ownship_ok = alert.ownship_id.is_empty() || alert.ownship_id == drone_id;
        if !ownship_ok {
            continue;
        }
        if alert.drone_a == drone_id {
            alerts.push(CollisionLog {
                other_drone_id: alert.drone_b.clone(),
                distance: alert.distance,
                alert_level: alert.alert_level,
                time_to_violation: alert.time_to_violation,
                min_safe_heading: alert.min_safe_heading,
                max_safe_heading: alert.max_safe_heading,
            });
            alert_ids.push(format!("{}_{}", alert.drone_b, alert.alert_level));
        } else if alert.drone_b == drone_id {
            alerts.push(CollisionLog {
                other_drone_id: alert.drone_a.clone(),
                distance: alert.distance,
                alert_level: alert.alert_level,
                time_to_violation: alert.time_to_violation,
                min_safe_heading: alert.min_safe_heading,
                max_safe_heading: alert.max_safe_heading,
            });
            alert_ids.push(format!("{}_{}", alert.drone_a, alert.alert_level));
        }
    }
    alert_ids.sort();
    (alerts, alert_ids)
}

fn telemetry_system(
    time: Res<Time>,
    cfg: Res<LoggerConfig>,
    mut log_timer: ResMut<LogTimer>,
    mut last_states: Local<HashMap<String, DroneLogState>>,
    query: Query<(
        &crate::agents::Drone,
        &Transform,
        &crate::agents::Velocity,
        &crate::agents::FlightPlan,
        Option<&crate::agents::ReactiveAvoidance>,
        Option<&crate::agents::FlightState>,
    )>,
    active_collisions: Res<crate::daidalus::ActiveCollisions>,
) {
    if cfg.level == LogLevel::Metrics {
        return; // no NDJSON output
    }

    let current_time = time.elapsed_seconds();

    if cfg.level == LogLevel::Full {
        if !log_timer.0.tick(time.delta()).just_finished() {
            return;
        }
        for (drone, transform, vel, _plan, avoid_opt, fs_opt) in query.iter() {
            let pos = transform.translation;
            let is_airborne = pos.y >= 2.0 || vel.0.length() > 0.5;
            if !is_airborne { continue; }
            let (alerts, _) = build_alerts_for_drone(&drone.id, &active_collisions);
            let has_reactive = avoid_opt.map(|a| a.target.is_some()).unwrap_or(false);
            write_entry(&TelemetryEntry {
                time_elapsed: current_time,
                drone_id: drone.id.clone(),
                position: [pos.x, pos.y, pos.z],
                velocity: Some([vel.0.x, vel.0.y, vel.0.z]),
                flight_state: fs_opt.map(|s| s.to_string()),
                has_reactive_target: has_reactive,
                collision_alerts: alerts,
            });
        }
        return;
    }

    // Compact: event-based
    for (drone, transform, vel, flight_plan, avoidance_opt, fs_opt) in query.iter() {
        let pos = transform.translation;
        let (alerts, alert_ids) = build_alerts_for_drone(&drone.id, &active_collisions);

        let has_avoid = avoidance_opt.map(|a| a.target.is_some()).unwrap_or(false);
        let wp_idx = flight_plan.current_waypoint_index;

        let mut changed = false;
        if let Some(state) = last_states.get(&drone.id) {
            if state.wp_idx != wp_idx || state.has_avoidance != has_avoid || state.alerts != alert_ids {
                changed = true;
            }
        } else {
            changed = true;
        }

        if changed {
            last_states.insert(drone.id.clone(), DroneLogState {
                wp_idx,
                has_avoidance: has_avoid,
                alerts: alert_ids,
            });
            write_entry(&TelemetryEntry {
                time_elapsed: current_time,
                drone_id: drone.id.clone(),
                position: [pos.x, pos.y, pos.z],
                velocity: Some([vel.0.x, vel.0.y, vel.0.z]),
                flight_state: fs_opt.map(|s| s.to_string()),
                has_reactive_target: has_avoid,
                collision_alerts: alerts,
            });
        }
    }
}

// ── Exit: flush NDJSON + write metrics JSON ────────────────────────────

fn export_on_exit(
    mut exit_events: EventReader<bevy::app::AppExit>,
    pending: Res<crate::PendingDrones>,
    drones: Query<(
        &crate::agents::Drone,
        &crate::agents::FlightState,
        &Transform,
        &crate::agents::FlightPlan,
    )>,
    mut metrics: ResMut<SimMetrics>,
    cfg: Res<LoggerConfig>,
    route_cfg: Res<crate::core::route_metrics::RouteMetricsConfig>,
) {
    let mut n_exit = 0u32;
    for _ in exit_events.read() {
        n_exit += 1;
    }
    if n_exit == 0 {
        return;
    }

    use crate::agents::FlightState;
    use crate::core::route_metrics::{RouteIdealDistanceMode, RouteMetricsTiming};

    metrics.incomplete_missions_by_reason.clear();
    *metrics
        .incomplete_missions_by_reason
        .entry("not_spawned".to_string())
        .or_insert(0) += pending.0.len() as u32;

    for (drone, state, transform, _plan) in drones.iter() {
        let y = transform.translation.y;
        let key = match *state {
            FlightState::Idle => "active_idle",
            FlightState::Takeoff => "active_takeoff",
            FlightState::Cruise => "active_cruise",
            FlightState::Landing => "active_landing",
            FlightState::Completed if y >= 2.0 => "completed_airborne_not_landed",
            FlightState::Completed => "completed_on_ground_pending_despawn",
        };
        *metrics
            .incomplete_missions_by_reason
            .entry(key.to_string())
            .or_insert(0) += 1;
    }

    // Always write sim_metrics.json (tiny file, always useful)
    let total_ideal = metrics.total_ideal_distance;
    let total_real = metrics.total_real_distance;
    let ineff_pct = if total_ideal > 0.0 {
        (total_real - total_ideal) / total_ideal * 100.0
    } else { 0.0 };

    let ideal_mode_s = match route_cfg.ideal_mode {
        RouteIdealDistanceMode::Polyline => "polyline",
        RouteIdealDistanceMode::Chord => "chord",
    };
    let timing_s = match route_cfg.timing {
        RouteMetricsTiming::Spawn => "spawn",
        RouteMetricsTiming::MissionComplete => "mission_complete",
    };

    let incomplete_sum: u32 = metrics.incomplete_missions_by_reason.values().sum();
    let balance_ok = metrics.total_scheduled_missions == metrics.completed_missions + incomplete_sum;

    let metrics_json = serde_json::json!({
        "macproxy_count": metrics.macproxy_count,
        "macproxy_active_pairs": metrics.macproxy_active.len(),
        "daa_alert_pairs": metrics.daa_alert_pairs.len(),
        "total_scheduled_missions": metrics.total_scheduled_missions,
        "completed_missions": metrics.completed_missions,
        "incomplete_missions_by_reason": metrics.incomplete_missions_by_reason,
        "incomplete_missions_total": incomplete_sum,
        "mission_count_balance_ok": balance_ok,
        "total_real_distance_m": total_real,
        "total_ideal_distance_m": total_ideal,
        "route_inefficiency_pct": ineff_pct,
        "route_ideal_distance_mode": ideal_mode_s,
        "route_metrics_timing": timing_s,
    });
    if let Ok(mut f) = File::create("sim_metrics.json") {
        let _ = f.write_all(serde_json::to_string_pretty(&metrics_json).unwrap_or_default().as_bytes());
    }
    println!("Metrics: MACproxy={}, DAA_pairs={}, completed={}",
        metrics.macproxy_count, metrics.daa_alert_pairs.len(), metrics.completed_missions);

    // Flush NDJSON if open
    if cfg.level != LogLevel::Metrics {
        if let Ok(mut guard) = TELEMETRY_WRITER.lock() {
            if let Some(ref mut writer) = *guard {
                let _ = writer.flush();
            }
        }
        let count = *TELEMETRY_COUNT.lock().unwrap();
        println!("Telemetry: {} entries to simulation_telemetry.ndjson", count);
    }
}
