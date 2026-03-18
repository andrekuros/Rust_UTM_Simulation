use bevy::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct Drone {
    pub id: String,
}

#[derive(Serialize, Deserialize, Component, Debug, Clone, Default)]
pub struct Velocity(pub Vec3);

/// Vehicle type for Daidalus and performance (rotorcraft vs fixed-wing).
#[derive(Serialize, Deserialize, Component, Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum AircraftKind {
    #[default]
    Rotorcraft,
    FixedWing,
}

#[derive(Serialize, Deserialize, Component, Debug, Clone)]
pub struct DronePerformance {
    pub mass_kg: f32,
    pub max_speed_mps: f32,
    #[serde(default)]
    pub min_speed_mps: f32,
    #[serde(default = "default_vertical_speed")]
    pub max_vertical_speed_mps: f32,
    #[serde(default = "default_turn_rate")]
    pub max_turn_rate_deg_s: f32,
    pub battery_discharge_rate: f32,
}

fn default_vertical_speed() -> f32 { 5.0 }
fn default_turn_rate() -> f32 { 45.0 }

impl DronePerformance {
    /// Default rotorcraft-like params for Daidalus bands.
    pub fn default_rotorcraft() -> Self {
        Self {
            mass_kg: 1.5,
            max_speed_mps: 25.0,
            min_speed_mps: 0.0,
            max_vertical_speed_mps: 5.0,
            max_turn_rate_deg_s: 45.0,
            battery_discharge_rate: 10.0,
        }
    }
    /// Fixed-wing with different turn rate and min speed.
    pub fn default_fixed_wing() -> Self {
        Self {
            mass_kg: 5.0,
            max_speed_mps: 30.0,
            min_speed_mps: 12.0,
            max_vertical_speed_mps: 3.0,
            max_turn_rate_deg_s: 15.0,
            battery_discharge_rate: 50.0,
        }
    }
}

#[derive(Serialize, Deserialize, Component, Debug, Clone)]
pub struct FlightPlan {
    pub waypoints: Vec<Vec3>,
    pub current_waypoint_index: usize,
}

/// Marks when this drone becomes active (departure time). Movement runs only after sim time >= this.
#[derive(Component, Debug, Clone)]
pub struct DepartureTime(pub f32);

/// Short-term avoidance target injected by reactive system (overrides waypoint until reached).
#[derive(Component, Debug, Clone, Default)]
pub struct ReactiveAvoidance {
    pub target: Option<Vec3>,
    pub until_time: f32,
}

#[derive(Component, Debug, Clone, Serialize, Deserialize)]
pub struct Obstacle {
    pub id: String,
    pub geometry_type: String, // "Cylinder", "Box"
    pub dimensions: Vec3,
}

/// Current phase of flight, inferred from altitude and velocity.
#[derive(Component, Debug, Clone, Serialize, Deserialize, Default, PartialEq, Eq)]
pub enum FlightState {
    #[default]
    Idle,
    Takeoff,
    Cruise,
    Landing,
    Completed,
}

impl std::fmt::Display for FlightState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            FlightState::Idle => write!(f, "idle"),
            FlightState::Takeoff => write!(f, "takeoff"),
            FlightState::Cruise => write!(f, "cruise"),
            FlightState::Landing => write!(f, "landing"),
            FlightState::Completed => write!(f, "completed"),
        }
    }
}

/// Rectangular departure/landing zone (XZ plane). Collision alerts disabled when both aircraft are inside.
#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct RectZone {
    pub name: String,
    /// Min X, Min Z
    pub min: [f32; 2],
    /// Max X, Max Z
    pub max: [f32; 2],
    #[serde(default)]
    pub height_max: Option<f32>,
}

impl RectZone {
    pub fn contains_xz(&self, x: f32, z: f32) -> bool {
        x >= self.min[0] && x <= self.max[0] && z >= self.min[1] && z <= self.max[1]
    }
    pub fn contains_pos(&self, pos: Vec3) -> bool {
        if !self.contains_xz(pos.x, pos.z) {
            return false;
        }
        if let Some(h) = self.height_max {
            if pos.y > h {
                return false;
            }
        }
        true
    }
}
