use rand::Rng;
use serde::{Deserialize, Serialize};
use std::fs::File;
use std::io::Write;
use std::path::Path;

#[derive(Serialize, Deserialize)]
struct ScenarioData {
    drones: Vec<DroneConfig>,
    obstacles: Vec<ObstacleConfig>,
}

#[derive(Serialize, Deserialize)]
struct DroneConfig {
    id: String,
    performance: DronePerformance,
    flight_plan: DroneFlightPlanConfig,
    #[serde(default)]
    pub departure_time_s: f32,
}

#[derive(Serialize, Deserialize, Clone)]
struct DronePerformance {
    pub mass_kg: f32,
    pub max_speed_mps: f32,
    pub battery_discharge_rate: f32, 
}

#[derive(Serialize, Deserialize)]
struct DroneFlightPlanConfig {
    waypoints: Vec<[f32; 3]>,
    current_waypoint_index: usize,
}

#[derive(Serialize, Deserialize)]
struct ObstacleConfig {
    id: String,
    geometry_type: String, // "Cylinder", "Box"
    dimensions: [f32; 3],
    position: [f32; 3],
}

#[derive(Serialize, Deserialize)]
struct SimulationConfigJSON {
    duration: f32,
    collision_threshold: f32,
    show_progress_bar: Option<bool>,
}

#[derive(Serialize, Deserialize)]
struct ScenarioGenerationConfigJSON {
    num_drones: usize,
    area_size: f32,
    time_window: f32,
    min_speed: f32,
    max_speed: f32,
    flight_levels: Vec<f32>,
    departures: Vec<[f32; 2]>,
    landings: Vec<[f32; 2]>,
}

#[derive(Serialize, Deserialize, Clone)]
struct NoFlyZoneJSON {
    id: String,
    geometry_type: String, // "Cylinder"
    position: [f32; 3],    // [x, y, z] Wait, cylinder is usually just x,z base and height. Let's say position is base center.
    radius: f32,
    height: f32,
}

#[derive(Serialize, Deserialize)]
struct SimConfigRoot {
    simulation: SimulationConfigJSON,
    scenario: ScenarioGenerationConfigJSON,
    no_fly_zones: Vec<NoFlyZoneJSON>,
}

// Math helper for ray-cylinder intersection to detect NFZ violations
fn line_intersects_cylinder(
    p1: [f32; 3], 
    p2: [f32; 3], 
    cyl_pos: [f32; 3], 
    cyl_radius: f32, 
    cyl_height: f32
) -> bool {
    // Project to 2D (XZ plane) for radius check
    let x1 = p1[0];
    let z1 = p1[2];
    let x2 = p2[0];
    let z2 = p2[2];
    
    let cx = cyl_pos[0];
    let cz = cyl_pos[2];

    // Check if line segment intersects circle in 2D
    // line segment from (x1,z1) to (x2,z2), circle at (cx,cz) radius R
    let dx = x2 - x1;
    let dz = z2 - z1;
    let fx = x1 - cx;
    let fz = z1 - cz;

    let a = dx*dx + dz*dz;
    let b = 2.0 * (fx*dx + fz*dz);
    let c = (fx*fx + fz*fz) - cyl_radius*cyl_radius;

    let mut discriminant = b*b - 4.0*a*c;

    if discriminant >= 0.0 {
        discriminant = discriminant.sqrt();
        let t1 = (-b - discriminant) / (2.0 * a);
        let t2 = (-b + discriminant) / (2.0 * a);

        if (t1 >= 0.0 && t1 <= 1.0) || (t2 >= 0.0 && t2 <= 1.0) {
            // Intersects in 2D. Now check height (Y).
            // A simple check: if both points are above or below the cylinder entirely.
            // Assuming cylinder goes from Y=0 to Y=height
            let min_y = p1[1].min(p2[1]);
            let max_y = p1[1].max(p2[1]);
            
            let cyl_min_y = cyl_pos[1];
            let cyl_max_y = cyl_pos[1] + cyl_height;

            if max_y >= cyl_min_y && min_y <= cyl_max_y {
                return true;
            }
        }
    }
    false
}

fn line_intersects_box_2d(
    p1: [f32; 3], 
    p2: [f32; 3], 
    box_pos: [f32; 3], 
    box_dim: [f32; 3]
) -> bool {
    let min_x = box_pos[0] - box_dim[0] / 2.0;
    let max_x = box_pos[0] + box_dim[0] / 2.0;
    let min_z = box_pos[2] - box_dim[2] / 2.0;
    let max_z = box_pos[2] + box_dim[2] / 2.0;

    let dir_x = p2[0] - p1[0];
    let dir_z = p2[2] - p1[2];
    
    let p = [-dir_x, dir_x, -dir_z, dir_z];
    let q = [
        p1[0] - min_x,
        max_x - p1[0],
        p1[2] - min_z,
        max_z - p1[2]
    ];
    
    let mut u1 = 0.0f32;
    let mut u2 = 1.0f32;
    
    for i in 0..4 {
        if p[i] == 0.0 {
            if q[i] < 0.0 {
                return false;
            }
        } else {
            let t = q[i] / p[i];
            if p[i] < 0.0 && u1 < t {
                u1 = t;
            } else if p[i] > 0.0 && u2 > t {
                u2 = t;
            }
        }
    }
    
    if u1 > u2 {
        false
    } else {
        true
    }
}


fn main() {
    let mut config_file = File::open("config/sim_config.json").expect("Failed to open sim_config.json");
    let mut config_data = String::new();
    std::io::Read::read_to_string(&mut config_file, &mut config_data).unwrap();
    let root_config: SimConfigRoot = serde_json::from_str(&config_data).unwrap();
    let config = root_config.scenario;
    let nfzs = root_config.no_fly_zones;

    let mut rng = rand::thread_rng();
    let mut scenario = ScenarioData {
        drones: Vec::new(),
        obstacles: Vec::new(), // generate random obstacles if needed
    };

    for nfz in &nfzs {
        scenario.obstacles.push(ObstacleConfig {
            id: nfz.id.clone(),
            geometry_type: nfz.geometry_type.clone(),
            dimensions: [nfz.radius, nfz.height, nfz.radius],
            position: nfz.position,
        });
    }

    // Generate CBD (Dense, tall skyscrapers in the center)
    for i in 0..60 {
        let r = rng.gen_range(0.0..800.0);
        let theta = rng.gen_range(0.0..std::f32::consts::TAU);
        let x = r * theta.cos();
        let z = r * theta.sin();
        
        let width = rng.gen_range(40.0..90.0);
        let depth = rng.gen_range(40.0..90.0);
        let height = rng.gen_range(200.0..600.0);
        
        scenario.obstacles.push(ObstacleConfig {
            id: format!("CBD_{:03}", i),
            geometry_type: "Box".to_string(),
            dimensions: [width, height, depth],
            position: [x, height / 2.0, z],
        });
    }

    // Generate Suburbs (Sparse, lower buildings outside the center)
    for i in 0..80 {
        let r = rng.gen_range(800.0..2500.0);
        let theta = rng.gen_range(0.0..std::f32::consts::TAU);
        let x = r * theta.cos();
        let z = r * theta.sin();
        
        let width = rng.gen_range(60.0..150.0);
        let depth = rng.gen_range(60.0..150.0);
        let height = rng.gen_range(40.0..120.0);
        
        scenario.obstacles.push(ObstacleConfig {
            id: format!("SUB_{:03}", i),
            geometry_type: "Box".to_string(),
            dimensions: [width, height, depth],
            position: [x, height / 2.0, z],
        });
    }

    // Define multiple asymmetric hubs (10 departure/landing points)
    let hubs = vec![
        [0.0, -2200.0],
        [2200.0, -2200.0],
        [-2200.0, -2200.0],
        [2200.0, 2200.0],
        [-2200.0, 2200.0],
        [0.0, 2200.0],
        [2400.0, 0.0],
        [-2400.0, 0.0],
        [1800.0, -500.0],
        [-1800.0, 500.0],
    ];

    for i in 0..config.num_drones {
        let mut dep_idx = rng.gen_range(0..hubs.len());
        let mut land_idx = rng.gen_range(0..hubs.len());
        while dep_idx == land_idx {
            land_idx = rng.gen_range(0..hubs.len());
        }
        
        let departure = hubs[dep_idx];
        let landing = hubs[land_idx];
        let flight_level = config.flight_levels[rng.gen_range(0..config.flight_levels.len())];
        let speed = rng.gen_range(config.min_speed..config.max_speed);
        let dep_time = rng.gen_range(0.0..config.time_window);

        let p_start = [departure[0], flight_level, departure[1]];
        let p_end = [landing[0], flight_level, landing[1]];
        
        let mut waypoints = vec![p_start];

        let mut avoidance_points = Vec::new();
        for obs in &scenario.obstacles {
            let intersect = if obs.geometry_type == "Cylinder" {
                line_intersects_cylinder(p_start, p_end, obs.position, obs.dimensions[0], obs.dimensions[1])
            } else if obs.geometry_type == "Box" {
                line_intersects_box_2d(p_start, p_end, obs.position, obs.dimensions)
            } else {
                false
            };

            if intersect {
                let mid_x = (p_start[0] + p_end[0]) / 2.0;
                let mid_z = (p_start[2] + p_end[2]) / 2.0;
                
                let dx = p_end[0] - p_start[0];
                let dz = p_end[2] - p_start[2];
                let length = (dx*dx + dz*dz).sqrt();
                if length > 0.0 {
                    let nx = -dz / length;
                    let nz = dx / length;
                    
                    let offset = if obs.geometry_type == "Cylinder" { obs.dimensions[0] } else { obs.dimensions[0] + obs.dimensions[2] } + 100.0;
                    avoidance_points.push([
                        mid_x + nx * offset,
                        flight_level,
                        mid_z + nz * offset
                    ]);
                }
            }
        }
        
        waypoints.extend(avoidance_points);
        waypoints.push(p_end);
        waypoints.push([landing[0], 0.0, landing[1]]);

        let drone = DroneConfig {
            id: format!("UAV_{:05}", i),
            performance: DronePerformance {
                mass_kg: 1.5,
                max_speed_mps: speed,
                battery_discharge_rate: 10.0,
            },
            flight_plan: DroneFlightPlanConfig {
                waypoints,
                current_waypoint_index: 0, 
            },
            departure_time_s: dep_time,
        };
        scenario.drones.push(drone);
    }
    
    let json = serde_json::to_string_pretty(&scenario).unwrap();
    let path = Path::new("config/scenario_dynamic.json");
    let mut file = File::create(path).unwrap();
    file.write_all(json.as_bytes()).unwrap();

    println!("Successfully generated scenario to config/scenario_dynamic.json with {} drones.", config.num_drones);
}
