use bevy::prelude::*;
use rumqttc::{MqttOptions, Client, QoS};
use std::time::Duration;
use std::thread;

pub struct CommsPlugin;

impl Plugin for CommsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, setup_mqtt);
    }
}

fn setup_mqtt() {
    // Basic MQTT setup (Non-blocking or running in a separate thread recommended for Bevy)
    thread::spawn(move || {
        let mut mqttoptions = MqttOptions::new("hpm_utm_agent", "localhost", 1883);
        mqttoptions.set_keep_alive(Duration::from_secs(5));

        let (mut client, mut connection) = Client::new(mqttoptions, 10);
        
        // Example subscription
        client.subscribe("utm/directives", QoS::AtMostOnce).unwrap();

        for notification in connection.iter() {
            // In a real app, use a channel to send events back to Bevy main thread
            println!("Notification = {:?}", notification);
        }
    });
}
