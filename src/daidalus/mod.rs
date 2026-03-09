use bevy::prelude::*;
use cxx::UniquePtr;
use std::pin::Pin;

#[cxx::bridge]
pub mod ffi {
    #[derive(Debug, Clone)]
    pub struct DaidalusResult {
        pub alert_level: i32,
        pub time_to_violation: f32,
        pub min_safe_heading: f32,
        pub max_safe_heading: f32,
    }

    pub struct Vec3F {
        pub x: f32,
        pub y: f32,
        pub z: f32,
    }

    unsafe extern "C++" {
        include!("daidalus/include/daidalus_bridge.h");
        type DaidalusWrapper;
        fn new_daidalus() -> UniquePtr<DaidalusWrapper>;
        
        fn evaluate_pair(
            self: Pin<&mut DaidalusWrapper>, 
            pos_a: &Vec3F, vel_a: &Vec3F,
            pos_b: &Vec3F, vel_b: &Vec3F
        ) -> DaidalusResult;
    }
}

#[derive(Debug, Clone)]
pub struct CollisionAlert {
    pub drone_a: String,
    pub drone_b: String,
    pub distance: f32,
    pub alert_level: i32,
    pub time_to_violation: f32,
    pub min_safe_heading: f32,
    pub max_safe_heading: f32,
}

#[derive(Resource, Default)]
pub struct ActiveCollisions {
    pub alerts: Vec<CollisionAlert>,
}

#[derive(Resource)]
pub struct SafetyConfig {
    pub collision_threshold: f32,
}
pub struct DaidalusBridge {
    pub inner: UniquePtr<ffi::DaidalusWrapper>,
}

impl Default for DaidalusBridge {
    fn default() -> Self {
        Self::new()
    }
}

impl DaidalusBridge {
    pub fn new() -> Self {
        Self { 
            inner: ffi::new_daidalus() 
        }
    }
}

pub struct DaidalusPlugin;

impl Plugin for DaidalusPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<ActiveCollisions>()
           .add_systems(Update, (daidalus_monitoring_system, reactive_avoidance_system));
    }
}

fn daidalus_monitoring_system(
    query: Query<(&crate::agents::Drone, &Transform, &crate::agents::Velocity)>,
    safety: Res<SafetyConfig>,
    metadata: Res<crate::ScenarioMetadata>,
    mut active_collisions: ResMut<ActiveCollisions>,
) {
    let mut bridge = DaidalusBridge::new();
    let agents: Vec<(String, Vec3, Vec3)> = query.iter()
        .map(|(drone, transform, velocity)| (drone.id.clone(), transform.translation, velocity.0))
        .collect();

    let cell_size = 250.0_f32;
    let mut grid: std::collections::HashMap<(i32, i32, i32), Vec<usize>> = std::collections::HashMap::new();

    for (i, (_, pos, _)) in agents.iter().enumerate() {
        let cx = (pos.x / cell_size).floor() as i32;
        let cy = (pos.y / cell_size).floor() as i32;
        let cz = (pos.z / cell_size).floor() as i32;
        grid.entry((cx, cy, cz)).or_default().push(i);
    }

    let mut alerts = Vec::new();
    
    let mut check_pair = |idx_a: usize, idx_b: usize| {
        let (id_a, pos_a, vel_a) = &agents[idx_a];
        let (id_b, pos_b, vel_b) = &agents[idx_b];
        
        let both_in_zone = metadata.departure_landing_zones.iter().any(|z| z.contains_pos(*pos_a) && z.contains_pos(*pos_b));
        if both_in_zone { return; }

        let dist = pos_a.distance(*pos_b);
        let daidalus_evaluation_radius = 250.0;
        
        if dist < daidalus_evaluation_radius {
            let res = bridge.inner.pin_mut().evaluate_pair(
                &ffi::Vec3F { x: pos_a.x, y: pos_a.y, z: pos_a.z },
                &ffi::Vec3F { x: vel_a.x, y: vel_a.y, z: vel_a.z },
                &ffi::Vec3F { x: pos_b.x, y: pos_b.y, z: pos_b.z },
                &ffi::Vec3F { x: vel_b.x, y: vel_b.y, z: vel_b.z }
            );

            // only physically log the alert if DAIDALUS triggers a warning, or they just physically breached the raw critical spherical bounding box
            if res.alert_level > 0 || dist < safety.collision_threshold {
                alerts.push(CollisionAlert {
                    drone_a: id_a.clone(),
                    drone_b: id_b.clone(),
                    distance: dist,
                    alert_level: res.alert_level,
                    time_to_violation: res.time_to_violation,
                    min_safe_heading: res.min_safe_heading,
                    max_safe_heading: res.max_safe_heading,
                });
            }
        }
    };

    for (&(cx, cy, cz), cell_indices) in grid.iter() {
        // Internal cell pairs
        for i in 0..cell_indices.len() {
            for j in (i + 1)..cell_indices.len() {
                check_pair(cell_indices[i], cell_indices[j]);
            }
        }

        // Half of 26 neighbors to avoid double-counting
        let neighbors = [
            (1, 0, 0), (1, 1, 0), (1, -1, 0),
            (0, 1, 0),
            (0, 0, 1), (1, 0, 1), (-1, 0, 1),
            (0, 1, 1), (1, 1, 1), (-1, 1, 1),
            (0, -1, 1), (1, -1, 1), (-1, -1, 1),
        ];
        for &(dx, dy, dz) in &neighbors {
            if let Some(neighbor_indices) = grid.get(&(cx + dx, cy + dy, cz + dz)) {
                for &idx_a in cell_indices {
                    for &idx_b in neighbor_indices {
                        check_pair(idx_a, idx_b);
                    }
                }
            }
        }
    }

    active_collisions.alerts = alerts;
}

#[derive(Resource)]
pub struct ReactiveDronesConfig(pub crate::AvoidanceMode);

fn reactive_avoidance_system(
    time: Res<Time>,
    reactive_cfg: Option<Res<ReactiveDronesConfig>>,
    active_collisions: Res<ActiveCollisions>,
    mut query: Query<(&crate::agents::Drone, &Transform, &mut crate::agents::ReactiveAvoidance, &crate::agents::FlightPlan)>,
) {
    let mode = reactive_cfg.map(|c| c.0).unwrap_or(crate::AvoidanceMode::None);
    if mode == crate::AvoidanceMode::None {
        return;
    }
    let now = time.elapsed_seconds();
    for (drone, transform, mut avoidance, _plan) in query.iter_mut() {
        if avoidance.until_time > 0.0 && now < avoidance.until_time {
            continue;
        }
        if avoidance.until_time > 0.0 && now >= avoidance.until_time {
            avoidance.target = None;
            avoidance.until_time = 0.0;
        }
        let in_alert = active_collisions.alerts.iter()
            .find(|a| (a.drone_a == drone.id || a.drone_b == drone.id) && a.alert_level > 0);
        
        if let Some(alert) = in_alert {
            let pos = transform.translation;
            let offset = match mode {
                crate::AvoidanceMode::Fixed => {
                    Vec3::new(1.0, 0.0, 1.0).normalize() * 200.0
                },
                crate::AvoidanceMode::Daidalus => {
                    if alert.min_safe_heading == 0.0 && alert.max_safe_heading == 0.0 {
                        Vec3::new(15.0, 10.0, 15.0) // tiny fallback jitter if totally gridlocked
                    } else {
                        let h = alert.min_safe_heading;
                        Vec3::new(h.sin(), 0.0, -h.cos()) * 200.0
                    }
                },
                crate::AvoidanceMode::None => Vec3::ZERO,
            };

            if offset != Vec3::ZERO {
                avoidance.target = Some(pos + offset);
                avoidance.until_time = now + 0.5; // Short burst evaluation to prevent overcoasting
            }
        }
    }
}
