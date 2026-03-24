//! Route distance accounting for `sim_metrics.json` (parity with Python xTM scripts).
//!
//! **Route inefficiency** matches `testeprimordial*.py`:  
//! `route_inefficiency_pct = (total_real - total_ideal) / total_ideal * 100` when `total_ideal > 0`.
//! Ideal length depends on [`RouteIdealDistanceMode`]: `chord` ≈ Python direct start→goal distance;
//! `polyline` = sum of waypoint legs (NFZ detours in the plan count toward ideal).

use bevy::prelude::*;
use serde::{Deserialize, Serialize};

/// How **ideal** mission distance is defined (affects `route_inefficiency_pct`).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RouteIdealDistanceMode {
    /// Sum of straight segments along the full flight-plan polyline (NFZ detours count in the ideal).
    #[default]
    Polyline,
    /// Single chord from first waypoint to last — same idea as `testeprimordial4b.py`
    /// `distancia_ideal_missao` (direct line; NFZ routing is “extra” in real path only).
    Chord,
}

/// When ideal/real distances are folded into global `sim_metrics` totals.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RouteMetricsTiming {
    /// Legacy: add ideal at spawn; integrate real every frame into global totals.
    #[default]
    Spawn,
    /// Python-style: add ideal+real only when a mission completes at landing (despawn).
    MissionComplete,
}

#[derive(Resource, Clone, Copy)]
pub struct RouteMetricsConfig {
    pub ideal_mode: RouteIdealDistanceMode,
    pub timing: RouteMetricsTiming,
}

impl Default for RouteMetricsConfig {
    fn default() -> Self {
        Self {
            ideal_mode: RouteIdealDistanceMode::Polyline,
            timing: RouteMetricsTiming::Spawn,
        }
    }
}

/// Per-drone accumulators when [`RouteMetricsTiming::MissionComplete`] is active.
#[derive(Component, Debug, Clone)]
pub struct MissionRouteMetrics {
    pub ideal_m: f64,
    pub real_m: f64,
    pub last_pos: Option<Vec3>,
}

/// Ideal distance (metres) for a waypoint list according to `mode`.
pub fn ideal_distance_m(waypoints: &[Vec3], mode: RouteIdealDistanceMode) -> f32 {
    match mode {
        RouteIdealDistanceMode::Polyline => waypoints
            .windows(2)
            .map(|w| w[0].distance(w[1]))
            .sum(),
        RouteIdealDistanceMode::Chord => {
            if waypoints.len() < 2 {
                0.0
            } else {
                waypoints.first().unwrap().distance(*waypoints.last().unwrap())
            }
        }
    }
}

/// When `radius_m > 0`, a drone on the **final leg** completes the mission if horizontal (XZ)
/// distance to the **last waypoint** is ≤ `radius_m` (avoids orbiting near the pad when turn rate
/// blocks the 1 m capture). `0` = legacy: must advance through all waypoints (including ground).
#[derive(Resource, Clone, Copy)]
pub struct MissionCompleteProximityConfig {
    pub radius_m: f32,
}

impl Default for MissionCompleteProximityConfig {
    fn default() -> Self {
        Self { radius_m: 0.0 }
    }
}
