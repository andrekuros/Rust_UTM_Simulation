use bevy::prelude::*;
use serde::Serialize;
use std::fs::File;
use std::io::Write;
use std::sync::Mutex;
use lazy_static::lazy_static;

lazy_static! {
    static ref TELEMETRY_LOGS: Mutex<Vec<TelemetryEntry>> = Mutex::new(Vec::new());
}

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
    pub collision_alerts: Vec<CollisionLog>,
}

#[derive(Serialize)]
pub struct TelemetryData {
    pub metadata: crate::ScenarioMetadata,
    pub frames: Vec<TelemetryEntry>,
}

pub struct LoggerPlugin;

impl Plugin for LoggerPlugin {
    fn build(&self, app: &mut App) {
        app.insert_resource(LogTimer(Timer::from_seconds(5.0, TimerMode::Repeating)))
           .add_systems(Update, logging_system)
           .add_systems(Last, export_logs_on_exit);
    }
}

#[derive(Resource)]
struct LogTimer(Timer);

use std::collections::HashMap;

struct DroneLogState {
    wp_idx: usize,
    has_avoidance: bool,
    alerts: Vec<String>,
}

fn logging_system(
    time: Res<Time>,
    mut last_states: Local<HashMap<String, DroneLogState>>,
    query: Query<(
        &crate::agents::Drone, 
        &Transform, 
        &crate::agents::FlightPlan, 
        Option<&crate::agents::ReactiveAvoidance>
    )>,
    active_collisions: Res<crate::daidalus::ActiveCollisions>,
) {
    let mut logs = TELEMETRY_LOGS.lock().unwrap();
    let current_time = time.elapsed_seconds();
    
    for (drone, transform, flight_plan, avoidance_opt) in query.iter() {
        let pos = transform.translation;
        
        let mut alerts = Vec::new();
        let mut alert_ids = Vec::new();
        for alert in active_collisions.alerts.iter() {
            if alert.drone_a == drone.id {
                alerts.push(CollisionLog {
                    other_drone_id: alert.drone_b.clone(),
                    distance: alert.distance,
                    alert_level: alert.alert_level,
                    time_to_violation: alert.time_to_violation,
                    min_safe_heading: alert.min_safe_heading,
                    max_safe_heading: alert.max_safe_heading,
                });
                alert_ids.push(format!("{}_{}", alert.drone_b, alert.alert_level)); // trigger log if alert level changes
            } else if alert.drone_b == drone.id {
                alerts.push(CollisionLog {
                    other_drone_id: alert.drone_a.clone(),
                    distance: alert.distance,
                    alert_level: alert.alert_level,
                    time_to_violation: alert.time_to_violation,
                    min_safe_heading: alert.min_safe_heading,
                    max_safe_heading: alert.max_safe_heading,
                });
                alert_ids.push(format!("{}_{}", alert.drone_a, alert.alert_level)); // trigger log if alert level changes
            }
        }
        alert_ids.sort();

        let has_avoid = avoidance_opt.map(|a| a.target.is_some()).unwrap_or(false);
        let wp_idx = flight_plan.current_waypoint_index;

        let mut changed = false;
        if let Some(state) = last_states.get(&drone.id) {
            if state.wp_idx != wp_idx || state.has_avoidance != has_avoid || state.alerts != alert_ids {
                changed = true;
            }
        } else {
            // First time seeing this drone (Spawn)
            changed = true;
        }

        if changed {
            last_states.insert(drone.id.clone(), DroneLogState {
                wp_idx,
                has_avoidance: has_avoid,
                alerts: alert_ids,
            });

            logs.push(TelemetryEntry {
                time_elapsed: current_time,
                drone_id: drone.id.clone(),
                position: [pos.x, pos.y, pos.z],
                collision_alerts: alerts,
            });
        }
    }
}

fn export_logs_on_exit(
    mut exit_events: EventReader<bevy::app::AppExit>,
    metadata: Res<crate::ScenarioMetadata>,
) {
    if !exit_events.is_empty() {
        let logs = TELEMETRY_LOGS.lock().unwrap();
        if logs.is_empty() { return; }
        
        if let Ok(mut file) = File::create("simulation_telemetry.ndjson") {
            // Write metadata as first line
            let meta_json = serde_json::json!({ "metadata": (*metadata).clone() });
            if let Ok(json) = serde_json::to_string(&meta_json) {
                let _ = writeln!(file, "{}", json);
            }
            
            // Write frames line by line
            for frame in logs.iter() {
                if let Ok(json) = serde_json::to_string(frame) {
                    let _ = writeln!(file, "{}", json);
                }
            }
            println!("Exported telemetry log with {} entries to simulation_telemetry.ndjson", logs.len());
        }
    }
}
