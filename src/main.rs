use bevy::prelude::*;
use bevy::render::mesh::Mesh;
use serde::{Deserialize, Serialize};
use std::time::Duration;
use bevy::time::TimeUpdateStrategy;

mod core;
mod agents;
mod sensors;
mod daidalus;
mod negotiation;
mod comms;

use crate::agents::{AircraftKind, DepartureTime, Drone, DronePerformance, FlightPlan, FlightState, Obstacle, RectZone, ReactiveAvoidance, Velocity};
use crate::sensors::{SensorsPlugin, SensorSuite};
use crate::core::CorePlugin;
use crate::negotiation::NegotiationPlugin;
use crate::comms::CommsPlugin;

use crate::daidalus::DaidalusPlugin;

#[derive(Serialize, Deserialize, Resource)]
struct ScenarioData {
    drones: Vec<DroneConfig>,
    obstacles: Vec<ObstacleConfig>,
    #[serde(default)]
    pub departure_landing_zones: Vec<RectZone>,
}

#[derive(Serialize, Deserialize, Clone)]
struct DroneConfig {
    id: String,
    performance: DronePerformance,
    flight_plan: DroneFlightPlanConfig,
    #[serde(default)]
    pub departure_time_s: f32,
    #[serde(default)]
    pub aircraft_kind: Option<AircraftKind>,
}

#[derive(Serialize, Deserialize, Clone)]
struct DroneFlightPlanConfig {
    waypoints: Vec<[f32; 3]>,
    current_waypoint_index: usize,
}

#[derive(Serialize, Deserialize, Clone)]
struct ObstacleConfig {
    id: String,
    geometry_type: String, // "Cylinder", "Box"
    dimensions: [f32; 3],
    position: [f32; 3],
}

#[derive(Resource, Default, Serialize, Clone)]
pub struct ScenarioMetadata {
    pub departure_points: Vec<[f32; 3]>,
    pub landing_points: Vec<[f32; 3]>,
    pub obstacles: Vec<ObstacleConfig>,
    pub departure_landing_zones: Vec<RectZone>,
}

#[derive(Serialize, Deserialize, Default, Clone, Copy, PartialEq, Eq)]
pub enum AvoidanceMode {
    #[default]
    None,
    Fixed,
    Daidalus,
}

/// `log_level`: "metrics" = no NDJSON (just counters in sim_metrics.json),
///              "compact" = event-based NDJSON (small, for viewer),
///              "full"    = periodic NDJSON at log_interval_s (large, for detailed replay).
#[derive(Serialize, Deserialize)]
struct SimulationConfigJSON {
    duration: f32,
    collision_threshold: f32,
    show_progress_bar: Option<bool>,
    #[serde(default)]
    avoidance_mode: AvoidanceMode,
    scenario_file: Option<String>,
    enable_mqtt: Option<bool>,
    #[serde(default)]
    log_level: Option<String>,
    #[serde(default)]
    log_interval_s: Option<f32>,
    /// Physics tick rate in Hz. Python sims use 1Hz. Default 1.0.
    #[serde(default)]
    physics_hz: Option<f64>,
    /// DAIDALUS evaluation interval in seconds. Higher = faster but less responsive. Default 5.
    #[serde(default)]
    daa_interval_s: Option<f32>,
    // Legacy field — mapped to log_level internally
    #[serde(default)]
    log_periodic: Option<bool>,
}

#[derive(Serialize, Deserialize)]
struct SimConfigRoot {
    simulation: SimulationConfigJSON,
    #[serde(default)]
    departure_landing_zones: Option<Vec<RectZone>>,
}

#[derive(Resource, Default)]
struct PendingDrones(pub Vec<DroneConfig>);

#[derive(Resource, Default)]
struct ConfigDepartureZones(pub Vec<RectZone>);

fn main() {
    let mut config_file = std::fs::File::open("config/sim_config.json").expect("Failed to open sim_config.json");
    let mut config_data = String::new();
    std::io::Read::read_to_string(&mut config_file, &mut config_data).unwrap();
    let root_config: SimConfigRoot = serde_json::from_str(&config_data).unwrap();
    
    let sim_duration = root_config.simulation.duration;
    let collision_threshold = root_config.simulation.collision_threshold;
    let show_progress = root_config.simulation.show_progress_bar.unwrap_or(false);
    let avoidance_mode = root_config.simulation.avoidance_mode;
    let scenario_file = root_config.simulation.scenario_file
        .unwrap_or_else(|| "config/scenario_dynamic.json".to_string());
    let enable_mqtt = root_config.simulation.enable_mqtt.unwrap_or(true);
    let log_interval_s = root_config.simulation.log_interval_s.unwrap_or(5.0);

    // Resolve log_level: explicit field > legacy log_periodic > default "compact"
    let log_level_str = root_config.simulation.log_level
        .unwrap_or_else(|| {
            if root_config.simulation.log_periodic.unwrap_or(false) {
                "full".to_string()
            } else {
                "compact".to_string()
            }
        });
    let log_level = match log_level_str.as_str() {
        "metrics" => crate::core::logger::LogLevel::Metrics,
        "full" => crate::core::logger::LogLevel::Full,
        _ => crate::core::logger::LogLevel::Compact,
    };
    let physics_hz = root_config.simulation.physics_hz.unwrap_or(1.0);
    let daa_interval_s = root_config.simulation.daa_interval_s.unwrap_or(5.0);

    println!(
        "Starting simulation: duration {}s, collision threshold {}m, scenario {}, avoidance_mode {:?}, mqtt_enabled {}, log_level {:?}, physics_hz {}",
        sim_duration,
        collision_threshold,
        scenario_file,
        avoidance_mode as u8,
        enable_mqtt,
        log_level_str,
        physics_hz
    );

    let mut app = App::new();

    app.add_plugins(MinimalPlugins)
        .add_plugins(AssetPlugin::default())
        .add_plugins(bevy::scene::ScenePlugin::default())
        .insert_resource(TimeUpdateStrategy::ManualDuration(Duration::from_secs_f64(
            1.0,
        )))
        .insert_resource(SimulationConfig {
            duration: sim_duration,
            show_progress,
            scenario_file: scenario_file.clone(),
            avoidance_mode,
        })
        .insert_resource(crate::daidalus::SafetyConfig {
            collision_threshold,
        })
        .insert_resource(crate::daidalus::ReactiveDronesConfig(avoidance_mode))
        .insert_resource(crate::daidalus::DaaIntervalConfig(daa_interval_s))
        .insert_resource(crate::core::logger::LoggerConfig {
            level: log_level,
            interval_s: log_interval_s,
        })
        .insert_resource(crate::core::PhysicsHz(physics_hz))
        .insert_resource(ProgressTimer(Timer::from_seconds(1.0, TimerMode::Repeating)))
        .init_resource::<ScenarioMetadata>()
        .init_resource::<Assets<Mesh>>()
        .insert_resource(PendingDrones(Vec::new()))
        .insert_resource(ConfigDepartureZones(
            root_config
                .departure_landing_zones
                .unwrap_or_default(),
        ))
        .add_plugins(CorePlugin)
        .add_plugins(SensorsPlugin)
        .add_plugins(NegotiationPlugin)
        .add_plugins(DaidalusPlugin)
        .add_systems(Startup, load_scenario)
        .add_systems(Update, (spawn_drones_by_schedule, flight_state_system, despawn_completed_drones, timeout_system, progress_system));

    if enable_mqtt {
        app.add_plugins(CommsPlugin);
    }

    app.run();
}

#[derive(Resource)]
struct SimulationConfig {
    duration: f32,
    show_progress: bool,
    scenario_file: String,
    avoidance_mode: AvoidanceMode,
}

#[derive(Resource)]
struct ProgressTimer(Timer);

fn progress_system(
    time: Res<Time>,
    config: Res<SimulationConfig>,
    mut timer: ResMut<ProgressTimer>,
) {
    if !config.show_progress {
        return;
    }
    if timer.0.tick(time.delta()).just_finished() {
        let elapsed = time.elapsed_seconds();
        let total = config.duration;
        let p = (elapsed / total).clamp(0.0, 1.0);
        let bar_len = 40;
        let filled = (p * bar_len as f32) as usize;
        let empty = bar_len - filled;
        
        use std::io::Write;
        print!("\r[ {}{} ] {:.1}% ({:.0}s / {:.0}s)", 
            "=".repeat(filled), 
            " ".repeat(empty), 
            p * 100.0,
            elapsed, 
            total
        );
        let _ = std::io::stdout().flush();
    }
}

fn timeout_system(
    time: Res<Time>,
    config: Res<SimulationConfig>,
    mut exit: EventWriter<bevy::app::AppExit>,
) {
    if time.elapsed_seconds() > config.duration {
        if config.show_progress {
            println!("\nSimulation completed.");
        }
        exit.send(bevy::app::AppExit);
    }
}

fn load_scenario(
    mut commands: Commands,
    mut metadata: ResMut<ScenarioMetadata>,
    mut pending: ResMut<PendingDrones>,
    config: Res<SimulationConfig>,
    config_zones: Res<ConfigDepartureZones>,
) {
    let data = std::fs::read_to_string(&config.scenario_file).expect("Unable to read scenario file");
    let scenario: ScenarioData = serde_json::from_str(&data).expect("Unable to parse scenario JSON");
    // Drop the raw JSON string immediately to free memory
    drop(data);

    metadata.departure_landing_zones = if scenario.departure_landing_zones.is_empty() {
        config_zones.0.clone()
    } else {
        scenario.departure_landing_zones.clone()
    };

    // Only store first/last 50 departure/landing points in metadata (for viewer);
    // full list would waste memory with thousands of drone entities.
    let cap = 50;
    for drone_config in scenario.drones.iter().take(cap) {
        if let Some(first) = drone_config.flight_plan.waypoints.first() {
            metadata.departure_points.push(*first);
        }
        if let Some(last) = drone_config.flight_plan.waypoints.last() {
            metadata.landing_points.push(*last);
        }
    }

    for obstacle_config in scenario.obstacles {
        metadata.obstacles.push(obstacle_config.clone());
        let pos = obstacle_config.position;
        commands.spawn((
            Obstacle {
                id: obstacle_config.id.clone(),
                geometry_type: obstacle_config.geometry_type.clone(),
                dimensions: Vec3::new(obstacle_config.dimensions[0], obstacle_config.dimensions[1], obstacle_config.dimensions[2]),
            },
            Transform::from_translation(Vec3::new(pos[0], pos[1], pos[2])),
        ));
    }

    let drone_count = scenario.drones.len();
    pending.0 = scenario.drones;
    println!("Scenario loaded: {} obstacles, {} drones (scheduled), {} departure/landing zones",
        metadata.obstacles.len(), drone_count, metadata.departure_landing_zones.len());
}

fn spawn_drones_by_schedule(
    time: Res<Time>,
    config: Res<SimulationConfig>,
    mut pending: ResMut<PendingDrones>,
    mut commands: Commands,
    mut metrics: ResMut<crate::core::logger::SimMetrics>,
) {
    let now = time.elapsed_seconds();
    let to_spawn: Vec<DroneConfig> = pending.0.iter()
        .filter(|d| d.departure_time_s <= now)
        .cloned()
        .collect();
    for drone_config in &to_spawn {
        let waypoints: Vec<Vec3> = drone_config.flight_plan.waypoints.iter()
            .map(|wp| Vec3::new(wp[0], wp[1], wp[2]))
            .collect();
        let start = waypoints.first().copied().unwrap_or(Vec3::ZERO);
        // Accumulate ideal (flight-plan) distance for route inefficiency metric
        let ideal_dist: f32 = waypoints.windows(2)
            .map(|w| w[0].distance(w[1]))
            .sum();
        metrics.total_ideal_distance += ideal_dist as f64;
        let mut entity = commands.spawn((
            Drone { id: drone_config.id.clone() },
            drone_config.performance.clone(),
            FlightPlan {
                waypoints: waypoints.clone(),
                current_waypoint_index: drone_config.flight_plan.current_waypoint_index,
            },
            SensorSuite { sensors: vec![] },
            DepartureTime(drone_config.departure_time_s),
            ReactiveAvoidance::default(),
            FlightState::default(),
            Transform::from_translation(start),
            Velocity::default(),
        ));
        if let Some(kind) = drone_config.aircraft_kind {
            entity.insert(kind);
        }
    }
    pending.0.retain(|d| d.departure_time_s > now);
}

/// Remove drone entities once they finish all waypoints and land,
/// preventing unbounded ECS growth during long simulations.
fn despawn_completed_drones(
    mut commands: Commands,
    query: Query<(Entity, &FlightState, &Transform)>,
) {
    for (entity, state, transform) in query.iter() {
        if *state == FlightState::Completed && transform.translation.y < 2.0 {
            commands.entity(entity).despawn();
        }
    }
}

fn flight_state_system(
    mut query: Query<(
        &Transform,
        &Velocity,
        &FlightPlan,
        &DepartureTime,
        &mut FlightState,
    )>,
    time: Res<Time>,
) {
    let now = time.elapsed_seconds();
    for (transform, vel, plan, dep_time, mut state) in query.iter_mut() {
        if now < dep_time.0 {
            *state = FlightState::Idle;
            continue;
        }
        let alt = transform.translation.y;
        let vy = vel.0.y;
        let completed = plan.current_waypoint_index >= plan.waypoints.len();

        if completed {
            *state = FlightState::Completed;
        } else if alt < 5.0 && vel.0.length() < 0.5 {
            *state = FlightState::Idle;
        } else if vy > 0.5 {
            *state = FlightState::Takeoff;
        } else if vy < -0.5 {
            *state = FlightState::Landing;
        } else if alt >= 5.0 {
            *state = FlightState::Cruise;
        }
    }
}
