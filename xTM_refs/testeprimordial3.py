import os
import time
import math
import json
import random
import heapq
from collections import defaultdict
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, Point as ShapelyPoint

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Resultados_Cenario3")

# --- CONFIGURAÇÕES DO CENÁRIO 3 ---
SCENARIO_ID = 3
SIMULATION_HOURS = 8

XTM_SEPARATION_H = 30.0 
XTM_SEPARATION_V = 15.0 
MAX_MISSION_DISTANCE_M = 12000.0 

# NOVO LIMITE BASEADO EM REGRAS REAIS DO ATFM (SLOT DE DECOLAGEM)
MAX_ATRASO_MEDIO_MINUTOS = 5.0  

SJC_GEOFENCE_COORDS = [
    (-23.1500, -45.9700), (-23.1300, -45.7500),
    (-23.2800, -45.7500), (-23.2800, -45.9700)
]
sjc_polygon = Polygon(SJC_GEOFENCE_COORDS)

RESTRICTED_COORDS = [
    (-23.207232, -45.886221), (-23.246663, -45.860730), 
    (-23.221120, -45.839731), (-23.192784, -45.867164)
]
restricted_polygon = Polygon(RESTRICTED_COORDS)

AVOIDANCE_CORNERS = [
    (-23.204232, -45.889221), (-23.249663, -45.863730), 
    (-23.224120, -45.836731), (-23.189784, -45.864164)  
]

def get_random_point_in_sjc():
    min_lat, min_lon, max_lat, max_lon = sjc_polygon.bounds
    while True:
        p_lat = random.uniform(min_lat, max_lat)
        p_lon = random.uniform(min_lon, max_lon)
        pt = ShapelyPoint(p_lat, p_lon)
        if sjc_polygon.contains(pt) and not restricted_polygon.contains(pt):
            return p_lat, p_lon

def fast_distance_m(lat1, lon1, lat2, lon2):
    R = 6371000.0
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    x = (lon2_rad - lon1_rad) * math.cos((lat1_rad + lat2_rad) / 2)
    y = (lat2_rad - lat1_rad)
    return R * math.sqrt(x*x + y*y)

def move_point_fast(lat, lon, distance_m, bearing_deg):
    R = 6371000.0
    lat_rad, lon_rad = math.radians(lat), math.radians(lon)
    bearing_rad = math.radians(bearing_deg)
    new_lat_rad = math.asin(math.sin(lat_rad) * math.cos(distance_m / R) +
                            math.cos(lat_rad) * math.sin(distance_m / R) * math.cos(bearing_rad))
    new_lon_rad = lon_rad + math.atan2(math.sin(bearing_rad) * math.sin(distance_m / R) * math.cos(lat_rad),
                                       math.cos(distance_m / R) - math.sin(lat_rad) * math.sin(new_lat_rad))
    return math.degrees(new_lat_rad), math.degrees(new_lon_rad)

def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    d_lon = lon2_rad - lon1_rad
    x = math.sin(d_lon) * math.cos(lat2_rad)
    y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(d_lon))
    return (math.degrees(math.atan2(x, y)) + 360) % 360

def route_around_restricted_area(start_lat, start_lon, end_lat, end_lon):
    line = LineString([(start_lat, start_lon), (end_lat, end_lon)])
    if not line.crosses(restricted_polygon):
        return [(end_lat, end_lon)] 
    
    nodes = [(start_lat, start_lon), (end_lat, end_lon)] + AVOIDANCE_CORNERS
    graph = defaultdict(list)
    
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            seg = LineString([nodes[i], nodes[j]])
            if not seg.crosses(restricted_polygon):
                dist = fast_distance_m(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1])
                graph[i].append((dist, j))
                graph[j].append((dist, i))
                
    pq = [(0, 0, [])] 
    visited = set()
    
    while pq:
        cost, curr, path = heapq.heappop(pq)
        if curr in visited: continue
        visited.add(curr)
        
        new_path = path + [nodes[curr]]
        if curr == 1: 
            return new_path[1:] 
            
        for w, neighbor in graph[curr]:
            if neighbor not in visited:
                heapq.heappush(pq, (cost + w, neighbor, new_path))
                
    return [(end_lat, end_lon)] 

class xTMCentral:
    def __init__(self):
        self.reservations = {}
        self.metric_delays = []

    def request_flight_plan(self, drone_id, start_tick, start_lat, start_lon, waypoints, cruise_alt, speed_ms, vertical_speed):
        proposed_trajectory = []
        current_tick = start_tick
        c_lat, c_lon = start_lat, start_lon
        c_alt = 0.0
        total_real_dist = 0.0
        
        while c_alt < cruise_alt:
            c_alt = min(c_alt + vertical_speed, cruise_alt)
            proposed_trajectory.append((current_tick, c_lat, c_lon, c_alt, "TAKEOFF"))
            current_tick += 1
            
        for wp in waypoints:
            t_lat, t_lon = wp
            dist_to_wp = fast_distance_m(c_lat, c_lon, t_lat, t_lon)
            while dist_to_wp > speed_ms:
                bearing = calculate_bearing(c_lat, c_lon, t_lat, t_lon)
                c_lat, c_lon = move_point_fast(c_lat, c_lon, speed_ms, bearing)
                total_real_dist += speed_ms
                proposed_trajectory.append((current_tick, c_lat, c_lon, c_alt, "CRUISE"))
                current_tick += 1
                dist_to_wp = fast_distance_m(c_lat, c_lon, t_lat, t_lon)
            
            total_real_dist += dist_to_wp
            c_lat, c_lon = t_lat, t_lon
            proposed_trajectory.append((current_tick, c_lat, c_lon, c_alt, "CRUISE"))
            current_tick += 1
            
        while c_alt > 0:
            c_alt = max(c_alt - vertical_speed, 0.0)
            proposed_trajectory.append((current_tick, c_lat, c_lon, c_alt, "LANDING"))
            current_tick += 1

        for pt in proposed_trajectory:
            t, lat, lon, alt, _ = pt
            if t in self.reservations:
                grid_y, grid_x = int(lat * 1000), int(lon * 1000)
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        cell = (grid_y + dy, grid_x + dx)
                        if cell in self.reservations[t]:
                            for res_id, r_lat, r_lon, r_alt in self.reservations[t][cell]:
                                if res_id != drone_id:
                                    dh = fast_distance_m(lat, lon, r_lat, r_lon)
                                    dv = abs(alt - r_alt)
                                    if dh < XTM_SEPARATION_H and dv < XTM_SEPARATION_V:
                                        return False, [], 0.0 

        for pt in proposed_trajectory:
            t, lat, lon, alt, _ = pt
            if t not in self.reservations: self.reservations[t] = {}
            grid_y, grid_x = int(lat * 1000), int(lon * 1000)
            cell = (grid_y, grid_x)
            if cell not in self.reservations[t]: self.reservations[t][cell] = []
            self.reservations[t][cell].append((drone_id, lat, lon, alt))
            
        return True, proposed_trajectory, total_real_dist

class DroneXTM:
    def __init__(self, drone_id):
        self.drone_id = drone_id
        self.lat, self.lon = get_random_point_in_sjc()
        self.alt = 0.0
        self.state = "IDLE"
        self.trajectory = []
        self.speed_ms = 15.3 
        self.vertical_speed = 3.0 
        self.cruise_altitude = random.uniform(30.0, 50.0)
        self.idle_timer = random.uniform(0, 120)
        
        self.delay_acumulado = 0.0
        self.distancia_ideal_missao = 0.0
        self.distancia_real_missao = 0.0

    def update(self, dt, xtm, metrics, tick):
        if self.state == "IDLE":
            self.idle_timer -= dt
            if self.idle_timer <= 0:
                while True:
                    t_lat, t_lon = get_random_point_in_sjc()
                    dist = fast_distance_m(self.lat, self.lon, t_lat, t_lon)
                    if dist <= MAX_MISSION_DISTANCE_M:
                        self.distancia_ideal_missao = dist
                        waypoints = route_around_restricted_area(self.lat, self.lon, t_lat, t_lon)
                        self.delay_acumulado = 0.0
                        self.state = "AWAITING_XTM_CLEARANCE"
                        self._pending_waypoints = waypoints
                        break
            return

        if self.state == "AWAITING_XTM_CLEARANCE":
            approved, trajectory, real_dist = xtm.request_flight_plan(self.drone_id, tick, self.lat, self.lon, self._pending_waypoints, self.cruise_altitude, self.speed_ms, self.vertical_speed)
            if approved:
                xtm.metric_delays.append(self.delay_acumulado)
                self.trajectory = trajectory
                self.distancia_real_missao = real_dist
                self.state = "FLYING" 
            else:
                self.delay_acumulado += 15.0 
            return

        if self.state == "FLYING":
            if self.trajectory:
                _, self.lat, self.lon, self.alt, self.state_display = self.trajectory.pop(0)
            else:
                self.state = "IDLE"
                self.state_display = "IDLE"
                self.idle_timer = 300.0 
                metrics["missoes_concluidas"] += 1
                metrics["distancia_ideal_total"] += self.distancia_ideal_missao
                metrics["distancia_real_total"] += self.distancia_real_missao

def run_scenario_scale(num_drones):
    print(f"\n[{num_drones:04} Drones] Iniciando simulação xTM...")
    start_sim_time = time.time()
    
    xtm_central = xTMCentral()
    drones = [DroneXTM(f"DRN_{i}") for i in range(num_drones)]
    total_ticks = SIMULATION_HOURS * 3600
    dt = 1.0 
    
    metrics = { "missoes_concluidas": 0, "distancia_ideal_total": 0.0, "distancia_real_total": 0.0 }
    flight_data = [] 

    gravar_inicio = 3600
    gravar_fim = 3900

    for tick in range(total_ticks):
        if gravar_inicio <= tick <= gravar_fim:
            frame = {"tick": tick, "drones": []}
            for d in drones:
                if d.state != "IDLE" and d.state != "AWAITING_XTM_CLEARANCE":
                    frame["drones"].append({"id": d.drone_id, "lat": d.lat, "lon": d.lon, "alt": round(d.alt,2), "state": d.state_display})
            flight_data.append(frame)

        for d in drones:
            d.update(dt, xtm_central, metrics, tick)
            
        if tick > 0 and tick % 7200 == 0: print(f"  -> {tick//3600}h simuladas...")

    ineficiencia_pct = 0.0
    if metrics["distancia_ideal_total"] > 0:
        ineficiencia_pct = ((metrics["distancia_real_total"] - metrics["distancia_ideal_total"]) / metrics["distancia_ideal_total"]) * 100

    atraso_medio = sum(xtm_central.metric_delays) / len(xtm_central.metric_delays) if xtm_central.metric_delays else 0
    atraso_medio_min = atraso_medio / 60.0

    tempo_execucao = time.time() - start_sim_time
    print(f"[FIM {num_drones:04} DRONES] Concluído em {tempo_execucao:.1f}s | Atraso Médio: {atraso_medio_min:.1f} min | Ineficiência: {ineficiencia_pct:.1f}%")

    return {
        "num_drones": num_drones, 
        "atraso_medio_min": atraso_medio_min,
        "ineficiencia_pct": ineficiencia_pct,
        "clip_critico": flight_data
    }

def gerar_relatorios(resultados):
    print("\n--- SALVANDO DADOS DO xTM ---")
    log_geral = {}
    for res in resultados:
        log_geral[f"{res['num_drones']}_drones"] = {
            "atraso_medio_minutos": res["atraso_medio_min"],
            "ineficiencia_pct": res["ineficiencia_pct"]
        }
        
    caminho_log = os.path.join(OUTPUT_DIR, "log_consolidado_cenario3.json")
    with open(caminho_log, "w") as f:
        json.dump(log_geral, f, indent=4)

    x_drones = [r["num_drones"] for r in resultados]
    y_atraso = [r["atraso_medio_min"] for r in resultados]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_drones, y_atraso, marker='o', color='darkorange', linewidth=2, markersize=6)
    plt.axhline(y=MAX_ATRASO_MEDIO_MINUTOS, color='r', linestyle='--', label=f"Limite Crítico de Slot ATFM ({MAX_ATRASO_MEDIO_MINUTOS} min)")
    plt.title("Saturação de Solo: Atraso Médio de Decolagem por Geometria xTM", fontsize=12)
    plt.xlabel("Quantidade de Drones Simultâneos", fontsize=11)
    plt.ylabel("Tempo Médio de Espera (Minutos)", fontsize=11)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    for x, y in zip(x_drones, y_atraso): plt.text(x, y + 0.1, f"{y:.1f}m", ha='center', va='bottom', fontsize=8)
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_atraso_solo_xtm.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    if len(resultados) > 0:
        res_inicio = resultados[0] 
        res_meio = resultados[len(resultados)//2] 
        res_fim = resultados[-1] 

        for nome, res in [("Inicio", res_inicio), ("Intermediario", res_meio), ("Saturado", res_fim)]:
            caminho_pb = os.path.join(OUTPUT_DIR, f"playback_cenario3_{nome}_{res['num_drones']}drones.json")
            with open(caminho_pb, "w") as f: 
                json.dump(res["clip_critico"], f)
            
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"==================================================")
    print(f" MOTOR DE BUSCA DE SATURAÇÃO - CENÁRIO 3 (xTM)")
    print(f" Teste escalando de 100 em 100 até limite ATFM (5 min)")
    print(f"==================================================\n")
    
    resultados = []
    num_drones = 100
    step = 100
    try:
        while True:
            res = run_scenario_scale(num_drones)
            resultados.append(res)
            if res["atraso_medio_min"] >= MAX_ATRASO_MEDIO_MINUTOS:
                print(f"\n[!!!] SATURAÇÃO LOGÍSTICA ATINGIDA! Limite de Slot ATFM (> 5 min) ultrapassado no solo. [!!!]")
                break
            num_drones += step
    except KeyboardInterrupt:
        pass
    
    gerar_relatorios(resultados)