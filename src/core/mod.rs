use bevy::prelude::*;
use bevy_rapier3d::prelude::*;

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
        app.add_systems(FixedUpdate, (physics_step, drone_movement_system));
    }
}

fn configure_physics_hz(hz: Res<PhysicsHz>, mut fixed_time: ResMut<Time<Fixed>>) {
    let rate = hz.0.max(0.1);
    *fixed_time = Time::<Fixed>::from_hz(rate);
    println!("Physics tick rate set to {} Hz (dt = {:.3}s)", rate, 1.0 / rate);
}

fn drone_movement_system(
    time: Res<Time>,
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
            let move_dist = (perf.max_speed_mps * dt).min(distance);
            velocity.0 = direction * perf.max_speed_mps;
            transform.translation += direction * move_dist;
            if distance > 0.1 {
                transform.look_at(target, Vec3::Y);
            }
        }
    }
}

fn physics_step(_time: Res<Time>, mut _query: Query<&mut Transform, With<RigidBody>>) {
    // Custom physics stepping logic if needed, 
    // otherwise Rapier handles it automatically via its plugin.
    // This is just a placeholder for explicit control.
}
