use bevy::prelude::*;
use crate::daidalus::DaidalusBridge;

pub struct NegotiationPlugin;

impl Plugin for NegotiationPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, negotiation_system);
    }
}

fn negotiation_system() {
    // Negotiation logic will be connected to the new evaluate_pair API later.
}

pub fn calculate_utility_cost(battery_usage: f32, time_to_arrival: f32) -> f32 {
    // Utility = w1 * Battery + w2 * Time
    let w1 = 0.6;
    let w2 = 0.4;
    (w1 * battery_usage) + (w2 * time_to_arrival)
}
