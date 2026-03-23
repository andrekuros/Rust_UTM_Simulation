use bevy::prelude::*;
use cxx::UniquePtr;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::f32::consts::{FRAC_PI_2, PI, TAU};

#[cxx::bridge]
pub mod ffi {
    #[derive(Debug, Clone, Copy)]
    pub struct DaidalusCppTune {
        /// &gt; 0: override `setDistanceFilter` after DO_365B (metres).
        pub distance_filter_m: f32,
        /// &gt; 0: override lookahead time (seconds).
        pub lookahead_s: f32,
        /// &gt; 0: override horizontal NMAC distance (metres).
        pub horizontal_nmac_m: f32,
    }

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
        fn new_daidalus(tune: &DaidalusCppTune) -> UniquePtr<DaidalusWrapper>;

        fn evaluate_pair(
            self: Pin<&mut DaidalusWrapper>,
            pos_a: &Vec3F,
            vel_a: &Vec3F,
            pos_b: &Vec3F,
            vel_b: &Vec3F,
        ) -> DaidalusResult;

        fn evaluate_multi(
            self: Pin<&mut DaidalusWrapper>,
            pos_o: &Vec3F,
            vel_o: &Vec3F,
            traffic_pos: &[Vec3F],
            traffic_vel: &[Vec3F],
        ) -> DaidalusResult;
    }
}

/// How pairwise DAIDALUS evaluations are aggregated for each ownship.
#[derive(
    Resource, Clone, Copy, Debug, Default, Serialize, Deserialize, PartialEq, Eq,
)]
#[serde(rename_all = "snake_case")]
pub enum DaaIntruderEvalMode {
    /// One C++ solve per intruder (legacy); reactive layer picks max `alert_level`.
    #[default]
    Pairwise,
    /// One C++ solve per ownship with all nearby intruders as traffic; combined bands/alerts.
    Multi,
}

/// Runtime tuning for DAIDALUS C++ core + Rust reactive layer (from `sim_config.json`).
#[derive(Resource, Clone, Copy, Debug, Serialize, Deserialize)]
#[serde(default)]
pub struct DaidalusTuneConfig {
    /// Lateral virtual target distance (m).
    pub evasion_offset_m: f32,
    /// Hold reactive target before allowing a new maneuver (s).
    pub evasion_duration_s: f32,
    /// 0 = lower edge of DAIDALUS NONE band; 1 = midpoint between min/max safe headings.
    pub heading_blend: f32,
    /// Blend safe horizontal direction with bearing to next waypoint (0..1).
    pub track_mix: f32,
    /// Minimum DAIDALUS alert level that triggers reactive steering.
    pub min_alert_level: i32,
    /// If &gt; 0, passed to C++ `setDistanceFilter` (m).
    pub cpp_distance_filter_m: f32,
    /// If &gt; 0, passed to C++ `setLookaheadTime` (s).
    pub cpp_lookahead_s: f32,
    /// If &gt; 0, passed to C++ `setHorizontalNMAC` (m).
    pub cpp_horizontal_nmac_m: f32,
    /// Max horizontal distance (XZ) from the remaining flight-plan polyline for a reactive
    /// avoidance target. Matches the spirit of Python2’s fixed lateral step, but keeps
    /// DAIDALUS-based headings from “walking” arbitrarily far from the route. `0` = no clamp.
    pub max_cross_track_m: f32,
    /// Horizontal distance (m) to the **last** mission waypoint while the active target **is** that
    /// waypoint (final leg only): below this, Daidalus reactive steering is disabled so aircraft
    /// can complete landing instead of orbiting with a partner at the same hub. `0` = disable.
    #[serde(default = "default_final_approach_no_reactive_radius_m")]
    pub final_approach_no_reactive_radius_m: f32,
    /// `pairwise` = one DAIDALUS solve per neighbor; `multi` = one solve per ownship with all
    /// intruders in range (combined horizontal bands via `alertLevelAllTraffic`).
    #[serde(default)]
    pub daa_intruder_eval_mode: DaaIntruderEvalMode,
}

fn default_final_approach_no_reactive_radius_m() -> f32 {
    120.0
}

impl Default for DaidalusTuneConfig {
    fn default() -> Self {
        Self {
            evasion_offset_m: 200.0,
            evasion_duration_s: 6.0,
            heading_blend: 0.5,
            track_mix: 0.25,
            min_alert_level: 1,
            cpp_distance_filter_m: 0.0,
            cpp_lookahead_s: 0.0,
            cpp_horizontal_nmac_m: 0.0,
            max_cross_track_m: 350.0,
            final_approach_no_reactive_radius_m: 120.0,
            daa_intruder_eval_mode: DaaIntruderEvalMode::Pairwise,
        }
    }
}

impl DaidalusTuneConfig {
    pub fn cpp_ffi(&self) -> ffi::DaidalusCppTune {
        ffi::DaidalusCppTune {
            distance_filter_m: self.cpp_distance_filter_m,
            lookahead_s: self.cpp_lookahead_s,
            horizontal_nmac_m: self.cpp_horizontal_nmac_m,
        }
    }
}

#[derive(Debug, Clone)]
pub struct CollisionAlert {
    pub drone_a: String,
    pub drone_b: String,
    /// Empty = legacy / symmetric (both aircraft may use the same band data).
    /// Otherwise DAIDALUS bands are for this aircraft as **ownship** vs the other as traffic.
    pub ownship_id: String,
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
        Self::new_with_cpp_tune(&ffi::DaidalusCppTune {
            distance_filter_m: 0.0,
            lookahead_s: 0.0,
            horizontal_nmac_m: 0.0,
        })
    }
}

impl DaidalusBridge {
    pub fn new_with_cpp_tune(tune: &ffi::DaidalusCppTune) -> Self {
        Self {
            inner: ffi::new_daidalus(tune),
        }
    }
}

#[derive(Resource)]
pub struct ReactiveDronesConfig(pub crate::AvoidanceMode);

/// When true, cruise horizontal speed gets ±1.5 m/s each tick (Python scenario 4B).
#[derive(Resource)]
pub struct Python4bWind(pub bool);

#[derive(Resource)]
pub struct DaaIntervalConfig(pub f32);

impl Default for DaaIntervalConfig {
    fn default() -> Self {
        Self(5.0)
    }
}

/// When both aircraft are in the same terminal volume, DAA / collision alerts are skipped.
/// - `radius_m: None` — legacy: both must lie inside the same rectangular [`crate::agents::RectZone`].
/// - `radius_m: Some(r)` — both within `r` metres horizontally of the **same** hub centre
///   (zone XZ centroid or a `landing_points` entry) and **both** with `y` in `[0, height_max_m]`.
#[derive(Resource, Clone, Copy, Debug)]
pub struct LandingCollisionIgnoreConfig {
    pub radius_m: Option<f32>,
    pub height_max_m: f32,
}

impl Default for LandingCollisionIgnoreConfig {
    fn default() -> Self {
        Self {
            radius_m: None,
            height_max_m: 400.0,
        }
    }
}

/// Horizontal distance in the XZ plane from a column at `(cx, cz)`.
fn horizontal_dist_to_column(pos: Vec3, cx: f32, cz: f32) -> f32 {
    let dx = pos.x - cx;
    let dz = pos.z - cz;
    (dx * dx + dz * dz).sqrt()
}

fn legacy_both_in_rect_zone(
    metadata: &crate::ScenarioMetadata,
    pos_a: Vec3,
    pos_b: Vec3,
) -> bool {
    metadata
        .departure_landing_zones
        .iter()
        .any(|z| z.contains_pos(pos_a) && z.contains_pos(pos_b))
}

/// Terminal airspace: ignore pairwise DAA / MACproxy when both drones are in the same volume.
pub fn landing_collision_pair_ignored(
    metadata: &crate::ScenarioMetadata,
    pos_a: Vec3,
    pos_b: Vec3,
    cfg: &LandingCollisionIgnoreConfig,
) -> bool {
    if let Some(radius) = cfg.radius_m {
        let y_max = cfg.height_max_m;
        if pos_a.y < 0.0 || pos_b.y < 0.0 || pos_a.y > y_max || pos_b.y > y_max {
            return false;
        }
        for zone in &metadata.departure_landing_zones {
            let cx = (zone.min[0] + zone.max[0]) * 0.5;
            let cz = (zone.min[1] + zone.max[1]) * 0.5;
            let da = horizontal_dist_to_column(pos_a, cx, cz);
            let db = horizontal_dist_to_column(pos_b, cx, cz);
            if da <= radius && db <= radius {
                return true;
            }
        }
        for lp in &metadata.landing_points {
            let cx = lp[0];
            let cz = lp[2];
            let da = horizontal_dist_to_column(pos_a, cx, cz);
            let db = horizontal_dist_to_column(pos_b, cx, cz);
            if da <= radius && db <= radius {
                return true;
            }
        }
        false
    } else {
        legacy_both_in_rect_zone(metadata, pos_a, pos_b)
    }
}

#[derive(Resource)]
struct DaaTimer(Timer);

impl Default for DaaTimer {
    fn default() -> Self {
        Self(Timer::from_seconds(5.0, TimerMode::Repeating))
    }
}

pub struct DaidalusPlugin;

impl Plugin for DaidalusPlugin {
    fn build(&self, app: &mut App) {
        app.init_resource::<ActiveCollisions>()
            .init_resource::<DaidalusTuneConfig>()
            .init_resource::<DaaIntervalConfig>()
            .init_resource::<DaaTimer>()
            .add_systems(Startup, init_daa_timer)
            .add_systems(Update, (daa_monitoring_system, reactive_avoidance_system));
    }
}

fn init_daa_timer(cfg: Res<DaaIntervalConfig>, mut timer: ResMut<DaaTimer>) {
    timer
        .0
        .set_duration(std::time::Duration::from_secs_f32(cfg.0));
    timer.0.reset();
    println!("DAA evaluation interval: {}s", cfg.0);
}

/// Horizontal bearing (radians), 0 = north. North = −Z when +Z is south (SJC projection).
fn bearing_xz(from: Vec3, to: Vec3) -> f32 {
    let dx = to.x - from.x;
    let dz = to.z - from.z;
    dx.atan2(-dz)
}

fn horizontal_dist(a: Vec3, b: Vec3) -> f32 {
    let dx = a.x - b.x;
    let dz = a.z - b.z;
    (dx * dx + dz * dz).sqrt()
}

fn legacy_geom_alerts(
    agents: &[(String, Vec3)],
    metadata: &crate::ScenarioMetadata,
    daa_h: f32,
    daa_v: f32,
    landing_ignore: &LandingCollisionIgnoreConfig,
) -> Vec<CollisionAlert> {
    let cell = 250.0_f32;
    let mut grid: std::collections::HashMap<(i32, i32, i32), Vec<usize>> =
        std::collections::HashMap::new();

    for (i, (_, pos)) in agents.iter().enumerate() {
        let cx = (pos.x / cell).floor() as i32;
        let cy = (pos.y / cell).floor() as i32;
        let cz = (pos.z / cell).floor() as i32;
        grid.entry((cx, cy, cz)).or_default().push(i);
    }

    let mut pairs: Vec<(usize, usize)> = Vec::new();
    for (&(cx, cy, cz), cell_indices) in grid.iter() {
        for i in 0..cell_indices.len() {
            for j in (i + 1)..cell_indices.len() {
                pairs.push((cell_indices[i], cell_indices[j]));
            }
        }
        let neighbors = [
            (1, 0, 0),
            (1, 1, 0),
            (1, -1, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (-1, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (0, -1, 1),
            (1, -1, 1),
            (-1, -1, 1),
        ];
        for &(dx, dy, dz) in &neighbors {
            if let Some(neighbor_indices) = grid.get(&(cx + dx, cy + dy, cz + dz)) {
                for &idx_a in cell_indices {
                    for &idx_b in neighbor_indices {
                        pairs.push((idx_a, idx_b));
                    }
                }
            }
        }
    }

    let mut alerts = Vec::new();
    let mut seen_pairs: HashSet<(String, String)> = HashSet::new();
    for (idx_a, idx_b) in pairs {
        let (id_a, pos_a) = &agents[idx_a];
        let (id_b, pos_b) = &agents[idx_b];
        let key = if id_a < id_b {
            (id_a.clone(), id_b.clone())
        } else {
            (id_b.clone(), id_a.clone())
        };
        if !seen_pairs.insert(key) {
            continue;
        }

        if landing_collision_pair_ignored(metadata, *pos_a, *pos_b, landing_ignore) {
            continue;
        }

        let dh = horizontal_dist(*pos_a, *pos_b);
        let dv = (pos_a.y - pos_b.y).abs();
        if dh >= daa_h || dv >= daa_v {
            continue;
        }

        let dist = pos_a.distance(*pos_b);
        alerts.push(CollisionAlert {
            drone_a: id_a.clone(),
            drone_b: id_b.clone(),
            ownship_id: String::new(),
            distance: dist,
            alert_level: 1,
            time_to_violation: 0.0,
            min_safe_heading: 0.0,
            max_safe_heading: 0.0,
        });
    }
    alerts
}

const MAX_MULTI_INTRUDERS: usize = 32;

fn run_daidalus_evaluation(
    agents: &[(String, Vec3, Vec3)],
    metadata: &crate::ScenarioMetadata,
    threshold: f32,
    cpp_tune: &ffi::DaidalusCppTune,
    landing_ignore: &LandingCollisionIgnoreConfig,
    eval_mode: DaaIntruderEvalMode,
) -> Vec<CollisionAlert> {
    let mut bridge = DaidalusBridge::new_with_cpp_tune(cpp_tune);
    let cell_size = 250.0_f32;
    let mut grid: std::collections::HashMap<(i32, i32, i32), Vec<usize>> =
        std::collections::HashMap::new();

    for (i, (_, pos, _)) in agents.iter().enumerate() {
        let cx = (pos.x / cell_size).floor() as i32;
        let cy = (pos.y / cell_size).floor() as i32;
        let cz = (pos.z / cell_size).floor() as i32;
        grid.entry((cx, cy, cz)).or_default().push(i);
    }

    let mut pairs: Vec<(usize, usize)> = Vec::new();
    for (&(cx, cy, cz), cell_indices) in grid.iter() {
        for i in 0..cell_indices.len() {
            for j in (i + 1)..cell_indices.len() {
                pairs.push((cell_indices[i], cell_indices[j]));
            }
        }
        let neighbors = [
            (1, 0, 0),
            (1, 1, 0),
            (1, -1, 0),
            (0, 1, 0),
            (0, 0, 1),
            (1, 0, 1),
            (-1, 0, 1),
            (0, 1, 1),
            (1, 1, 1),
            (-1, 1, 1),
            (0, -1, 1),
            (1, -1, 1),
            (-1, -1, 1),
        ];
        for &(dx, dy, dz) in &neighbors {
            if let Some(neighbor_indices) = grid.get(&(cx + dx, cy + dy, cz + dz)) {
                for &idx_a in cell_indices {
                    for &idx_b in neighbor_indices {
                        pairs.push((idx_a, idx_b));
                    }
                }
            }
        }
    }

    let mut seen_pairs: HashSet<(usize, usize)> = HashSet::new();
    let mut valid_pairs: Vec<(usize, usize)> = Vec::new();
    for (idx_a, idx_b) in pairs {
        let (_, pos_a, _) = &agents[idx_a];
        let (_, pos_b, _) = &agents[idx_b];

        if landing_collision_pair_ignored(metadata, *pos_a, *pos_b, landing_ignore) {
            continue;
        }

        let dist = pos_a.distance(*pos_b);
        if dist >= 250.0 {
            continue;
        }

        let key = if idx_a < idx_b {
            (idx_a, idx_b)
        } else {
            (idx_b, idx_a)
        };
        if !seen_pairs.insert(key) {
            continue;
        }
        valid_pairs.push(key);
    }

    let mut alerts = Vec::new();

    match eval_mode {
        DaaIntruderEvalMode::Pairwise => {
            for (idx_a, idx_b) in valid_pairs {
                let (id_a, pos_a, vel_a) = &agents[idx_a];
                let (id_b, pos_b, vel_b) = &agents[idx_b];
                let dist = pos_a.distance(*pos_b);

                let res_a = bridge.inner.pin_mut().evaluate_pair(
                    &ffi::Vec3F {
                        x: pos_a.x,
                        y: pos_a.y,
                        z: pos_a.z,
                    },
                    &ffi::Vec3F {
                        x: vel_a.x,
                        y: vel_a.y,
                        z: vel_a.z,
                    },
                    &ffi::Vec3F {
                        x: pos_b.x,
                        y: pos_b.y,
                        z: pos_b.z,
                    },
                    &ffi::Vec3F {
                        x: vel_b.x,
                        y: vel_b.y,
                        z: vel_b.z,
                    },
                );

                let res_b = bridge.inner.pin_mut().evaluate_pair(
                    &ffi::Vec3F {
                        x: pos_b.x,
                        y: pos_b.y,
                        z: pos_b.z,
                    },
                    &ffi::Vec3F {
                        x: vel_b.x,
                        y: vel_b.y,
                        z: vel_b.z,
                    },
                    &ffi::Vec3F {
                        x: pos_a.x,
                        y: pos_a.y,
                        z: pos_a.z,
                    },
                    &ffi::Vec3F {
                        x: vel_a.x,
                        y: vel_a.y,
                        z: vel_a.z,
                    },
                );

                // DAIDALUS can alert one ownship and not the other for the same geometry. Emit *both*
                // perspectives whenever the pair is active, so reactive steering is not one-sided when
                // `dist` is above `collision_threshold` but still inside the pair envelope.
                let pair_active =
                    res_a.alert_level > 0 || res_b.alert_level > 0 || dist < threshold;
                if pair_active {
                    alerts.push(CollisionAlert {
                        drone_a: id_a.clone(),
                        drone_b: id_b.clone(),
                        ownship_id: id_a.clone(),
                        distance: dist,
                        alert_level: res_a.alert_level,
                        time_to_violation: res_a.time_to_violation,
                        min_safe_heading: res_a.min_safe_heading,
                        max_safe_heading: res_a.max_safe_heading,
                    });
                    alerts.push(CollisionAlert {
                        drone_a: id_a.clone(),
                        drone_b: id_b.clone(),
                        ownship_id: id_b.clone(),
                        distance: dist,
                        alert_level: res_b.alert_level,
                        time_to_violation: res_b.time_to_violation,
                        min_safe_heading: res_b.min_safe_heading,
                        max_safe_heading: res_b.max_safe_heading,
                    });
                }
            }
        }
        DaaIntruderEvalMode::Multi => {
            let n = agents.len();
            let mut neigh: Vec<Vec<usize>> = vec![Vec::new(); n];
            for &(idx_a, idx_b) in &valid_pairs {
                neigh[idx_a].push(idx_b);
                neigh[idx_b].push(idx_a);
            }

            for i in 0..n {
                if neigh[i].is_empty() {
                    continue;
                }
                let (id_i, pos_i, vel_i) = &agents[i];
                let mut js: Vec<usize> = std::mem::take(&mut neigh[i]);
                js.sort_by(|&a, &b| {
                    let da = pos_i.distance(agents[a].1);
                    let db = pos_i.distance(agents[b].1);
                    da.partial_cmp(&db).unwrap_or(std::cmp::Ordering::Equal)
                });
                js.truncate(MAX_MULTI_INTRUDERS);
                let mut traffic_pos: Vec<ffi::Vec3F> = Vec::with_capacity(js.len());
                let mut traffic_vel: Vec<ffi::Vec3F> = Vec::with_capacity(js.len());
                for &j in &js {
                    let (_, p, v) = &agents[j];
                    traffic_pos.push(ffi::Vec3F {
                        x: p.x,
                        y: p.y,
                        z: p.z,
                    });
                    traffic_vel.push(ffi::Vec3F {
                        x: v.x,
                        y: v.y,
                        z: v.z,
                    });
                }

                let res = bridge.inner.pin_mut().evaluate_multi(
                    &ffi::Vec3F {
                        x: pos_i.x,
                        y: pos_i.y,
                        z: pos_i.z,
                    },
                    &ffi::Vec3F {
                        x: vel_i.x,
                        y: vel_i.y,
                        z: vel_i.z,
                    },
                    &traffic_pos,
                    &traffic_vel,
                );

                let closest_j = js[0];
                let closest_dist = pos_i.distance(agents[closest_j].1);
                let id_closest = agents[closest_j].0.clone();
                let any_close = js
                    .iter()
                    .any(|&j| pos_i.distance(agents[j].1) < threshold);
                let pair_active = res.alert_level > 0 || any_close;
                if pair_active {
                    alerts.push(CollisionAlert {
                        drone_a: id_i.clone(),
                        drone_b: id_closest,
                        ownship_id: id_i.clone(),
                        distance: closest_dist,
                        alert_level: res.alert_level,
                        time_to_violation: res.time_to_violation,
                        min_safe_heading: res.min_safe_heading,
                        max_safe_heading: res.max_safe_heading,
                    });
                }
            }
        }
    }

    alerts
}

fn daa_monitoring_system(
    time: Res<Time>,
    reactive_cfg: Option<Res<ReactiveDronesConfig>>,
    mut timer: ResMut<DaaTimer>,
    query: Query<(&crate::agents::Drone, &Transform, &crate::agents::Velocity)>,
    safety: Res<SafetyConfig>,
    metadata: Res<crate::ScenarioMetadata>,
    mut active_collisions: ResMut<ActiveCollisions>,
    daidalus_tune: Res<DaidalusTuneConfig>,
    landing_ignore: Res<LandingCollisionIgnoreConfig>,
) {
    let mode = reactive_cfg
        .as_ref()
        .map(|c| c.0)
        .unwrap_or(crate::AvoidanceMode::None);

    if mode == crate::AvoidanceMode::None {
        active_collisions.alerts.clear();
        return;
    }

    if !timer.0.tick(time.delta()).just_finished() {
        return;
    }

    let threshold = safety.collision_threshold;

    match mode {
        crate::AvoidanceMode::Fixed | crate::AvoidanceMode::Daidalus => {
            let agents: Vec<(String, Vec3, Vec3)> = query
                .iter()
                .filter(|(_, transform, _)| transform.translation.y >= 5.0)
                .map(|(drone, transform, velocity)| {
                    (
                        drone.id.clone(),
                        transform.translation,
                        velocity.0,
                    )
                })
                .collect();
            let cpp = daidalus_tune.cpp_ffi();
            active_collisions.alerts = run_daidalus_evaluation(
                &agents,
                &metadata,
                threshold,
                &cpp,
                &landing_ignore,
                daidalus_tune.daa_intruder_eval_mode,
            );
        }
        crate::AvoidanceMode::Python2 => {
            let agents: Vec<(String, Vec3)> = query
                .iter()
                .filter(|(_, transform, _)| transform.translation.y >= 5.0)
                .map(|(drone, transform, _)| (drone.id.clone(), transform.translation))
                .collect();
            active_collisions.alerts = legacy_geom_alerts(
                &agents,
                &metadata,
                150.0,
                30.0,
                &landing_ignore,
            );
        }
        crate::AvoidanceMode::Python4a | crate::AvoidanceMode::Python4b => {
            let agents: Vec<(String, Vec3)> = query
                .iter()
                .filter(|(_, transform, _)| transform.translation.y >= 5.0)
                .map(|(drone, transform, _)| (drone.id.clone(), transform.translation))
                .collect();
            active_collisions.alerts = legacy_geom_alerts(
                &agents,
                &metadata,
                25.0,
                12.0,
                &landing_ignore,
            );
        }
        crate::AvoidanceMode::None => {}
    }
}

/// Closest point on segment AB to point P in the XZ plane (Y from `p`).
fn closest_point_on_segment_xz(p: Vec3, a: Vec3, b: Vec3) -> Vec3 {
    let abx = b.x - a.x;
    let abz = b.z - a.z;
    let apx = p.x - a.x;
    let apz = p.z - a.z;
    let ab_len_sq = abx * abx + abz * abz;
    let t = if ab_len_sq < 1e-6 {
        0.0
    } else {
        (apx * abx + apz * abz) / ab_len_sq
    }
    .clamp(0.0, 1.0);
    Vec3::new(a.x + abx * t, p.y, a.z + abz * t)
}

/// Pull `candidate` horizontally toward the **active mission leg** if farther than `max_m` (XZ).
///
/// The active leg is `(waypoints[i-1], waypoints[i])` where `i == current_waypoint_index` (the
/// waypoint the drone is flying toward). This matches “stay near the segment you are on”.
///
/// **Why not** `[i .. end]` polylines: for SJC-style plans, when `i` points at the cruise endpoint,
/// `i..end-1` is only the **descent** segment, which shares one (x,z) — degenerate in XZ — and
/// clamps all evasion onto the pad column, killing en-route avoidance. Two-waypoint missions
/// often had `i == len-1`, so the polyline range was empty and clamp was a no-op — masking the bug.
fn clamp_to_active_route_leg_xz(
    candidate: Vec3,
    plan: &crate::agents::FlightPlan,
    max_m: f32,
) -> Vec3 {
    if max_m <= 0.0 || plan.waypoints.len() < 2 {
        return candidate;
    }
    let i = plan.current_waypoint_index;
    if i == 0 || i >= plan.waypoints.len() {
        return candidate;
    }
    let a = plan.waypoints[i - 1];
    let b = plan.waypoints[i];
    let abx = b.x - a.x;
    let abz = b.z - a.z;
    if abx * abx + abz * abz < 1e-4 {
        // Pure-vertical leg in XZ: no meaningful horizontal corridor (climb/descent column).
        return candidate;
    }
    let on = closest_point_on_segment_xz(candidate, a, b);
    let dx = candidate.x - on.x;
    let dz = candidate.z - on.z;
    let h = (dx * dx + dz * dz).sqrt();
    if h <= max_m || h < 1e-4 {
        candidate
    } else {
        Vec3::new(
            on.x + dx / h * max_m,
            candidate.y,
            on.z + dz / h * max_m,
        )
    }
}

/// Horizontal distance in XZ from `pos` to the flight plan’s last waypoint (typically over the pad).
fn horizontal_dist_to_last_waypoint_xz(pos: Vec3, plan: &crate::agents::FlightPlan) -> Option<f32> {
    plan.waypoints.last().map(|wp| {
        let dx = pos.x - wp.x;
        let dz = pos.z - wp.z;
        (dx * dx + dz * dz).sqrt()
    })
}

fn closest_threat_pos(
    self_id: &str,
    self_pos: Vec3,
    others: &[(String, Vec3)],
    daa_h: f32,
    daa_v: f32,
) -> Option<Vec3> {
    let mut best: Option<(f32, Vec3)> = None;
    for (oid, opos) in others {
        if oid == self_id {
            continue;
        }
        if opos.y <= 5.0 {
            continue;
        }
        let dh = horizontal_dist(self_pos, *opos);
        let dv = (self_pos.y - opos.y).abs();
        if dh < daa_h && dv < daa_v {
            let replace = match best {
                None => true,
                Some((bd, _)) => dh < bd,
            };
            if replace {
                best = Some((dh, *opos));
            }
        }
    }
    best.map(|(_, p)| p)
}

fn reactive_avoidance_system(
    time: Res<Time>,
    reactive_cfg: Option<Res<ReactiveDronesConfig>>,
    active_collisions: Res<ActiveCollisions>,
    daidalus_tune: Res<DaidalusTuneConfig>,
    mut query: Query<(
        &crate::agents::Drone,
        &Transform,
        &mut crate::agents::ReactiveAvoidance,
        &crate::agents::FlightPlan,
        &crate::agents::FlightState,
        &crate::agents::Velocity,
    )>,
) {
    let mode = reactive_cfg
        .map(|c| c.0)
        .unwrap_or(crate::AvoidanceMode::None);
    if mode == crate::AvoidanceMode::None || mode == crate::AvoidanceMode::Python4a {
        return;
    }

    let now = time.elapsed_seconds();

    if matches!(
        mode,
        crate::AvoidanceMode::Python2 | crate::AvoidanceMode::Python4b
    ) {
        let agents: Vec<(String, Vec3)> = query
            .iter()
            .map(|(d, t, _, _, _, _)| (d.id.clone(), t.translation))
            .collect();

        let (daa_h, daa_v, evade_s) = match mode {
            crate::AvoidanceMode::Python2 => (150.0_f32, 30.0_f32, 8.0_f32),
            crate::AvoidanceMode::Python4b => (25.0_f32, 12.0_f32, 3.0_f32),
            _ => unreachable!(),
        };

        for (drone, transform, mut avoidance, plan, _state, _vel) in query.iter_mut() {
            let pos = transform.translation;
            if pos.y < 5.0 {
                continue;
            }

            if let Some(threat_pos) =
                closest_threat_pos(&drone.id, pos, &agents, daa_h, daa_v)
            {
                let dir = if mode == crate::AvoidanceMode::Python2 {
                    let b_threat = bearing_xz(pos, threat_pos);
                    let evasion = b_threat + FRAC_PI_2;
                    Vec3::new(evasion.sin(), 0.0, -evasion.cos())
                } else {
                    let wp = plan
                        .waypoints
                        .get(plan.current_waypoint_index)
                        .copied()
                        .unwrap_or(pos + Vec3::Z);
                    let base = bearing_xz(pos, wp);
                    let b_threat = bearing_xz(pos, threat_pos);
                    let diff = (b_threat - base).rem_euclid(TAU);
                    let evasion = if diff < PI {
                        base - (60.0_f32.to_radians())
                    } else {
                        base + (60.0_f32.to_radians())
                    };
                    Vec3::new(evasion.sin(), 0.0, -evasion.cos())
                };

                avoidance.target = Some(pos + dir.normalize() * 200.0);
                avoidance.until_time = now + evade_s;
            }
        }
        return;
    }

    let tune = *daidalus_tune;
    let positions: HashMap<String, Vec3> = query
        .iter()
        .map(|(d, t, _, _, _, _)| (d.id.clone(), t.translation))
        .collect();

    for (drone, transform, mut avoidance, plan, _state, vel) in query.iter_mut() {
        let pos = transform.translation;

        // Avoid fighting the same landing point: disable lateral Daidalus targets only on the
        // final leg when horizontally near the **last** waypoint. (Distance to the last waypoint
        // alone is not enough: on an earlier leg you can pass near that XY while still navigating
        // to a different waypoint.) Do not use `FlightState::Landing` — that state is set for any
        // descent (vy < -0.5), which would disable avoidance for most of the mission.
        if mode == crate::AvoidanceMode::Daidalus {
            let on_last_leg = !plan.waypoints.is_empty()
                && plan.current_waypoint_index == plan.waypoints.len() - 1;
            let on_final = tune.final_approach_no_reactive_radius_m > 0.0
                && on_last_leg
                && horizontal_dist_to_last_waypoint_xz(pos, plan)
                    .map(|d| d <= tune.final_approach_no_reactive_radius_m)
                    .unwrap_or(false);
            if on_final {
                avoidance.target = None;
                avoidance.until_time = 0.0;
                continue;
            }
        }

        if avoidance.until_time > 0.0 && now < avoidance.until_time {
            continue;
        }
        if avoidance.until_time > 0.0 && now >= avoidance.until_time {
            avoidance.target = None;
            avoidance.until_time = 0.0;
        }
        let in_alert = active_collisions
            .alerts
            .iter()
            .filter(|a| {
                let involved = a.drone_a == drone.id || a.drone_b == drone.id;
                let ownship_ok = a.ownship_id.is_empty() || a.ownship_id == drone.id;
                if !involved || !ownship_ok {
                    return false;
                }
                if a.alert_level >= tune.min_alert_level {
                    return true;
                }
                // Pair was only admitted when close or when either side had a DAIDALUS alert; the
                // other ownship may still be alert_level 0 — still steer (fallback heading path).
                (mode == crate::AvoidanceMode::Daidalus || mode == crate::AvoidanceMode::Fixed)
                    && a.alert_level == 0
            })
            .max_by_key(|a| a.alert_level);

        if let Some(alert) = in_alert {
            let offset = match mode {
                crate::AvoidanceMode::Fixed => Vec3::new(1.0, 0.0, 1.0).normalize() * 200.0,
                crate::AvoidanceMode::Daidalus => {
                    // Horizontal-only offset (legacy fallback had Y≠0 and caused runaway climb).
                    if alert.min_safe_heading == 0.0 && alert.max_safe_heading == 0.0 {
                        // C++ leaves bands at 0 when alert_level==0; we still emit pairs for
                        // dist < collision_threshold. Same world-space (1,0,1) for both aircraft
                        // does not separate them — step horizontally **away from the intruder**.
                        let other_id = if alert.drone_a == drone.id {
                            alert.drone_b.as_str()
                        } else {
                            alert.drone_a.as_str()
                        };
                        let away = positions
                            .get(other_id)
                            .map(|op| {
                                let mut v = pos - *op;
                                v.y = 0.0;
                                v
                            })
                            .unwrap_or(Vec3::ZERO);
                        if away.length_squared() > 4.0 {
                            away.normalize() * tune.evasion_offset_m
                        } else {
                            let mut v = vel.0;
                            v.y = 0.0;
                            if v.length_squared() > 1e-2 {
                                Vec3::new(-v.z, 0.0, v.x).normalize() * tune.evasion_offset_m
                            } else {
                                Vec3::new(1.0, 0.0, 1.0).normalize() * tune.evasion_offset_m
                            }
                        }
                    } else {
                        let b = tune.heading_blend.clamp(0.0, 1.0);
                        let lo = alert.min_safe_heading;
                        let hi = alert.max_safe_heading;
                        // Circular midpoint of the safe arc (arithmetic mean breaks near ±π wrap).
                        let s = lo.sin() + hi.sin();
                        let c = lo.cos() + hi.cos();
                        let mid = s.atan2(c);
                        let h = lo * (1.0 - b) + mid * b;
                        let dir_safe = Vec3::new(h.sin(), 0.0, -h.cos());
                        let wp = plan
                            .waypoints
                            .get(plan.current_waypoint_index)
                            .copied()
                            .unwrap_or(pos + Vec3::Z);
                        let mut to_wp = wp - pos;
                        to_wp.y = 0.0;
                        let dir_wp = if to_wp.length_squared() < 1e-6 {
                            dir_safe
                        } else {
                            to_wp.normalize()
                        };
                        // When DAIDALUS "safe" heading ≈ track to waypoint, track_mix pulls the
                        // virtual target onto the original leg → velocity stays straight (alerts fire
                        // but no visible lateral maneuver). Tighten blend when close; if still
                        // collinear with route, force a horizontal sidestep toward dir_safe.
                        let m_base = tune.track_mix.clamp(0.0, 1.0);
                        let m_dist = (alert.distance / 220.0_f32).clamp(0.0, 1.0);
                        // Previous: large distance → large m → strong pull toward waypoint even when
                        // that leg crosses the intruder (jagged last-second turns). Cap route blend
                        // when alerts are serious or geometry is already tight.
                        let severity = if alert.alert_level >= 3 {
                            0.1
                        } else if alert.alert_level >= 2 {
                            0.22
                        } else if alert.alert_level >= 1 {
                            0.45
                        } else if alert.distance < 85.0 {
                            0.55
                        } else {
                            1.0
                        };
                        let m = m_base * m_dist * severity;
                        let blended = dir_safe * (1.0 - m) + dir_wp * m;
                        let mut dir = if blended.length_squared() < 1e-6 {
                            dir_safe
                        } else {
                            blended.normalize()
                        };
                        let align_xz = dir.x * dir_wp.x + dir.z * dir_wp.z;
                        if align_xz.abs() > 0.88 {
                            let mut right = Vec3::new(-dir_wp.z, 0.0, dir_wp.x);
                            if right.length_squared() < 1e-6 {
                                right = Vec3::new(1.0, 0.0, 0.0);
                            } else {
                                right = right.normalize();
                            }
                            let left = -right;
                            dir = if dir_safe.dot(right) >= dir_safe.dot(left) {
                                right
                            } else {
                                left
                            };
                        }
                        dir * tune.evasion_offset_m
                    }
                }
                crate::AvoidanceMode::None
                | crate::AvoidanceMode::Python2
                |                 crate::AvoidanceMode::Python4a
                | crate::AvoidanceMode::Python4b => Vec3::ZERO,
            };

            if offset != Vec3::ZERO {
                let mut offset = offset;
                if mode == crate::AvoidanceMode::Daidalus {
                    offset.y = 0.0;
                }
                let mut target = pos + offset;
                if mode == crate::AvoidanceMode::Daidalus {
                    target.y = pos.y;
                }
                if mode == crate::AvoidanceMode::Daidalus && tune.max_cross_track_m > 0.0 {
                    target = clamp_to_active_route_leg_xz(target, plan, tune.max_cross_track_m);
                    target.y = pos.y;
                }
                avoidance.target = Some(target);
                let dur = if mode == crate::AvoidanceMode::Daidalus {
                    tune.evasion_duration_s.max(0.1)
                } else {
                    0.5
                };
                avoidance.until_time = now + dur;
            }
        }
    }
}
