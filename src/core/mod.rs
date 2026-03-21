use bevy::prelude::*;
use bevy_rapier3d::prelude::*;
use rand::Rng;
use std::collections::{HashMap, HashSet};

pub mod logger;
use logger::LoggerPlugin;

/// Physics tick rate. Python xTM sims use 1 Hz. Higher values give smoother
/// trajectories but cost more CPU. For UTM-scale waypoint navigation, 1 Hz is enough.
#[derive(Resource)]
pub struct PhysicsHz(pub f64);

impl Default for PhysicsHz {
    fn default() -> Self { Self(1.0) }
}

pub struct CorePlugin;

impl Plugin for CorePlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<PhysicsHz>();
        app.add_plugins(RapierPhysicsPlugin::<NoUserData>::default());
        app.add_plugins(LoggerPlugin);

        app.add_systems(Startup, configure_physics_hz);
        app.add_systems(
            FixedUpdate,
            (physics_step, drone_movement_system, python4a_route_penalty_system).chain(),
        );
    }
}

fn configure_physics_hz(hz: Res<PhysicsHz>, mut fixed_time: ResMut<Time<Fixed>>) {
    let rate = hz.0.max(0.1);
    *fixed_time = Time::<Fixed>::from_hz(rate);
    println!("Physics tick rate set to {} Hz (dt = {:.3}s)", rate, 1.0 / rate);
}

fn drone_movement_system(
    time: Res<Time>,
    wind_4b: Option<Res<crate::daidalus::Python4bWind>>,
    mut query: Query<(
        &crate::agents::DronePerformance,
        &crate::agents::DepartureTime,
        &mut crate::agents::FlightPlan,
        &mut crate::agents::ReactiveAvoidance,
        &mut Transform,
        &mut crate::agents::Velocity,
    )>,
) {
    let now = time.elapsed_seconds();
    let dt = time.delta_seconds();
    let mut rng = rand::thread_rng();
    let wind_on = wind_4b.map(|w| w.0).unwrap_or(false);
    for (perf, dep_time, mut plan, mut avoidance, mut transform, mut velocity) in query.iter_mut() {
        if now < dep_time.0 {
            continue;
        }
        let current = transform.translation;
        let (target, is_avoidance) = if let Some(avoid_target) = avoidance.target {
            if now >= avoidance.until_time {
                avoidance.target = None;
                avoidance.until_time = 0.0;
                (plan.waypoints.get(plan.current_waypoint_index).copied(), false)
            } else {
                (Some(avoid_target), true)
            }
        } else {
            (plan.waypoints.get(plan.current_waypoint_index).copied(), false)
        };
        if target.is_none() {
            continue;
        }
        let target = target.unwrap();
        let diff = target - current;
        let distance = diff.length();

        if distance < 1.0 {
            velocity.0 = Vec3::ZERO;
            if is_avoidance {
                avoidance.target = None;
                avoidance.until_time = 0.0;
            } else {
                plan.current_waypoint_index += 1;
            }
        } else {
            let direction = diff.normalize();
            let speed = if wind_on {
                (perf.max_speed_mps + rng.gen_range(-1.5_f32..1.5_f32)).max(0.5)
            } else {
                perf.max_speed_mps
            };
            let move_dist = (speed * dt).min(distance);
            velocity.0 = direction * speed;
            transform.translation += direction * move_dist;
            if distance > 0.1 {
                transform.look_at(target, Vec3::Y);
            }
        }
    }
}

/// Python 4A: each tick, +5 m "maneuver penalty" per drone that sees a DAA threat (no steering).
fn python4a_route_penalty_system(
    reactive_cfg: Option<Res<crate::daidalus::ReactiveDronesConfig>>,
    query: Query<(&crate::agents::Drone, &Transform)>,
    mut metrics: ResMut<crate::core::logger::SimMetrics>,
) {
    if reactive_cfg.map(|c| c.0) != Some(crate::AvoidanceMode::Python4a) {
        return;
    }

    const DAA_H: f32 = 25.0;
    const DAA_V: f32 = 12.0;
    let cell = 50.0_f32;

    let airborne: Vec<(String, Vec3)> = query
        .iter()
        .filter(|(_, t)| t.translation.y >= 5.0)
        .map(|(d, t)| (d.id.clone(), t.translation))
        .collect();

    let mut grid: HashMap<(i32, i32), Vec<usize>> = HashMap::new();
    for (i, (_, pos)) in airborne.iter().enumerate() {
        let cx = (pos.x / cell).floor() as i32;
        let cz = (pos.z / cell).floor() as i32;
        grid.entry((cx, cz)).or_default().push(i);
    }

    let neighbors = [
        (0, 0),
        (1, 0),
        (-1, 0),
        (0, 1),
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
        (0, -1),
    ];

    let mut penalized: HashSet<String> = HashSet::new();
    for (&(cx, cz), indices) in grid.iter() {
        for &(dx, dz) in &neighbors {
            let Some(other_indices) = grid.get(&(cx + dx, cz + dz)) else {
                continue;
            };
            for &i in indices {
                for &j in other_indices {
                    if i == j {
                        continue;
                    }
                    let (_, pa) = &airborne[i];
                    let (_, pb) = &airborne[j];
                    let dh = ((pa.x - pb.x).powi(2) + (pa.z - pb.z).powi(2)).sqrt();
                    let dv = (pa.y - pb.y).abs();
                    if dh < DAA_H && dv < DAA_V {
                        penalized.insert(airborne[i].0.clone());
                        penalized.insert(airborne[j].0.clone());
                    }
                }
            }
        }
    }

    metrics.total_real_distance += 5.0 * penalized.len() as f64;
}

fn physics_step(_time: Res<Time>, mut _query: Query<&mut Transform, With<RigidBody>>) {
    // Custom physics stepping logic if needed, 
    // otherwise Rapier handles it automatically via its plugin.
    // This is just a placeholder for explicit control.
}
