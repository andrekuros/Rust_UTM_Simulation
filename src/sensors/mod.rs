use bevy::prelude::*;
use bevy_rapier3d::prelude::*;

#[derive(Debug, Clone)]
pub struct DetectionResult {
    pub entity_id: Entity,
    pub distance: f32,
    pub bearing: f32,
    pub confidence: f32,
}

pub trait Sensor: Send + Sync {
    /// Update sensor state based on time step, owner's transform, and optional physics context
    fn update(&mut self, dt: f32, drone_transform: &Transform, rapier_context: Option<&RapierContext>);
    
    /// meaningful method to get what the sensor sees
    fn produce_detections(&self) -> Vec<DetectionResult>;
}

#[derive(Component)]
pub struct SensorSuite {
    pub sensors: Vec<Box<dyn Sensor>>,
}

/// A basic acoustic sensor implementation
pub struct AcousticSensor {
    pub max_range: f32,
    pub noise_floor: f32,
}

impl Sensor for AcousticSensor {
    fn update(&mut self, _dt: f32, _drone_transform: &Transform, _rapier_context: Option<&RapierContext>) {
        // In a real implementation, this would query the spatial index
    }

    fn produce_detections(&self) -> Vec<DetectionResult> {
        // Placeholder
        vec![]
    }
}

pub struct RaycastSensor {
    pub max_range: f32,
    pub fov: f32, // Field of view (placeholder for future multiple-ray implementations)
    last_detections: Vec<DetectionResult>,
}

impl RaycastSensor {
    pub fn new(max_range: f32, fov: f32) -> Self {
        Self {
            max_range,
            fov,
            last_detections: Vec::new(),
        }
    }
}

impl Sensor for RaycastSensor {
    fn update(&mut self, _dt: f32, drone_transform: &Transform, rapier_context: Option<&RapierContext>) {
        self.last_detections.clear();
        
        let Some(ctx) = rapier_context else { return };
        
        let ray_pos = drone_transform.translation;
        let ray_dir = drone_transform.rotation * Vec3::NEG_Z; // Forward direction
        
        let max_toi = self.max_range;
        let solid = true;
        let query_filter = QueryFilter::default();

        if let Some((entity, toi)) = ctx.cast_ray(ray_pos, ray_dir, max_toi, solid, query_filter) {
            self.last_detections.push(DetectionResult {
                entity_id: entity,
                distance: toi,
                bearing: 0.0, // Simplified: dead-ahead
                confidence: 1.0,
            });
        }
    }

    fn produce_detections(&self) -> Vec<DetectionResult> {
        self.last_detections.clone()
    }
}

pub struct SensorsPlugin;

impl Plugin for SensorsPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Update, sensor_update_system);
    }
}

fn sensor_update_system(
    time: Res<Time>,
    rapier_context: Option<Res<RapierContext>>,
    mut query: Query<(&Transform, &mut SensorSuite)>,
) {
    let dt = time.delta_seconds();
    let ctx = rapier_context.as_deref();

    for (transform, mut suite) in query.iter_mut() {
        for sensor in suite.sensors.iter_mut() {
            sensor.update(dt, transform, ctx);
        }
    }
}
