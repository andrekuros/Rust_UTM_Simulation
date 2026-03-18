import os
import time
import math
import json
import random
import sys
import matplotlib.pyplot as plt
from collections import Counter
from shapely.geometry import Polygon, Point as ShapelyPoint

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Resultados_Cenario2")

# --- CONFIGURAÇÕES DO CENÁRIO 2 ---
SCENARIO_ID = 2
SCENARIO_NAME = "INICIO ALEATORIO - COM DAA - SEM xTM - SEM EVTOL"
SIMULATION_HOURS = 8

COLLISION_RADIUS_M = 20.0
COLLISION_ALT_M = 10.0
DAA_RADIUS_H = 150.0  
DAA_RADIUS_V = 30.0   
MAX_MISSION_DISTANCE_M = 12000.0 

# Condições de Saturação (Auto-Stop)
MAX_INEFICIENCIA_ACEITAVEL = 10.0 
MAX_COLISOES_ACEITAVEIS = 50      

SJC_GEOFENCE_COORDS = [
    (-23.1500, -45.9700), (-23.1300, -45.7500),
    (-23.2800, -45.7500), (-23.2800, -45.9700)
]
sjc_polygon = Polygon(SJC_GEOFENCE_COORDS)

def get_random_point_in_sjc():
    min_lat, min_lon, max_lat, max_lon = sjc_polygon.bounds
    while True:
        p_lat = random.uniform(min_lat, max_lat)
        p_lon = random.uniform(min_lon, max_lon)
        if sjc_polygon.contains(ShapelyPoint(p_lat, p_lon)):
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

class DroneOriginal:
    def __init__(self, drone_id):
        self.drone_id = drone_id
        self.lat, self.lon = get_random_point_in_sjc()
        self.alt = 0.0
        self.state = "IDLE"
        self.target_lat = None
        self.target_lon = None
        self.speed_ms = 15.3 
        self.vertical_speed = 3.0 
        
        # CORREÇÃO 1: Restaurada a dispersão de altitude para uso real do volume do espaço aéreo
        self.cruise_altitude = random.uniform(30.0, 50.0) 
        
        self.idle_timer = random.uniform(0, 120)
        self.evasion_timer = 0.0 
        self.current_bearing = 0.0
        self.evasion_heading = 0.0 # Armazena a proa de fuga durante o timer
        self.distancia_ideal_missao = 0.0
        self.distancia_real_missao = 0.0

    def update_kinematics(self, dt, all_drones, metrics, tick):
        if self.state == "IDLE":
            self.idle_timer -= dt
            if self.idle_timer <= 0:
                while True:
                    t_lat, t_lon = get_random_point_in_sjc()
                    dist = fast_distance_m(self.lat, self.lon, t_lat, t_lon)
                    if dist <= MAX_MISSION_DISTANCE_M:
                        self.target_lat, self.target_lon = t_lat, t_lon
                        self.distancia_ideal_missao = dist
                        self.distancia_real_missao = 0.0
                        break
                self.state = "TAKEOFF"
            return

        if self.state == "TAKEOFF":
            self.alt += self.vertical_speed * dt
            if self.alt >= self.cruise_altitude:
                self.alt = self.cruise_altitude
                self.state = "CRUISE"

        elif self.state == "CRUISE":
            dist_to_target = fast_distance_m(self.lat, self.lon, self.target_lat, self.target_lon)
            
            if dist_to_target < (self.speed_ms * dt):
                self.lat, self.lon = self.target_lat, self.target_lon
                self.state = "LANDING"
                metrics["missoes_concluidas"] += 1
                metrics["distancia_ideal_total"] += self.distancia_ideal_missao
                metrics["distancia_real_total"] += self.distancia_real_missao
                return

            base_bearing = calculate_bearing(self.lat, self.lon, self.target_lat, self.target_lon)
            
            # --- LÓGICA DAA CORRIGIDA ---
            threat_detected = False
            closest_threat = None
            min_threat_dist = float('inf')

            # CORREÇÃO 2: Escaneia todas as ameaças sem interromper no primeiro encontro (sem break)
            for other in all_drones:
                if other.drone_id != self.drone_id and other.alt > 5.0:
                    if abs(self.lat - other.lat) > 0.002 or abs(self.lon - other.lon) > 0.002: continue
                    
                    dist_h = fast_distance_m(self.lat, self.lon, other.lat, other.lon)
                    dist_v = abs(self.alt - other.alt)
                    
                    if dist_h < DAA_RADIUS_H and dist_v < DAA_RADIUS_V:
                        threat_detected = True
                        
                        # Log da ocorrência
                        pair_id = tuple(sorted([self.drone_id, other.drone_id]))
                        if pair_id not in metrics["historico_ocorrencias"]:
                            metrics["historico_ocorrencias"].add(pair_id)
                            metrics["ocorrencias_unicas"] += 1
                            metrics["log_ocorrencias"].append(tick)
                            
                        # Identifica a ameaça mais imediata
                        if dist_h < min_threat_dist:
                            min_threat_dist = dist_h
                            closest_threat = other

            # CORREÇÃO 3: Cálculo vetorial de repulsão baseado na posição da ameaça
            if threat_detected and closest_threat:
                self.evasion_timer = 8.0
                bearing_to_threat = calculate_bearing(self.lat, self.lon, closest_threat.lat, closest_threat.lon)
                # Desvia 90 graus em relação à ameaça (tangencial), não em relação ao alvo final
                self.evasion_heading = (bearing_to_threat + 90.0) % 360
                self.current_bearing = self.evasion_heading
            elif self.evasion_timer > 0:
                self.evasion_timer -= dt
                self.current_bearing = self.evasion_heading
            else:
                self.current_bearing = base_bearing

            distance_to_move = self.speed_ms * dt
            self.distancia_real_missao += distance_to_move
            self.lat, self.lon = move_point_fast(self.lat, self.lon, distance_to_move, self.current_bearing)

        elif self.state == "LANDING":
            self.alt -= self.vertical_speed * dt
            if self.alt <= 0.0:
                self.alt = 0.0
                self.state = "IDLE"
                self.idle_timer = 300.0 

def run_scenario_scale(num_drones):
    print(f"\n[{num_drones:04} Drones] Iniciando simulação de 8 horas...")
    start_sim_time = time.time()
    
    drones = [DroneOriginal(f"DRN_{i}") for i in range(num_drones)]
    total_ticks = SIMULATION_HOURS * 3600
    dt = 1.0 
    
    metrics = {
        "colisoes_unicas": 0, "ocorrencias_unicas": 0,
        "historico_colisoes": set(), "historico_ocorrencias": set(),
        "log_detalhado_colisoes": [], "log_ocorrencias": [],
        "missoes_concluidas": 0, "distancia_ideal_total": 0.0, "distancia_real_total": 0.0
    }
    flight_data = [] 

    for tick in range(total_ticks):
        frame = {"tick": tick, "drones": []}
        for d in drones:
            d.update_kinematics(dt, drones, metrics, tick)
            if tick % 1 == 0: 
                frame["drones"].append({"id": d.drone_id, "lat": d.lat, "lon": d.lon, "alt": round(d.alt,2), "state": d.state})
        
        if tick % 1 == 0: flight_data.append(frame)

        for i in range(len(drones)):
            for j in range(i+1, len(drones)):
                d1, d2 = drones[i], drones[j]
                if d1.alt < 5.0 and d2.alt < 5.0: continue 
                if abs(d1.lat - d2.lat) > 0.0005 or abs(d1.lon - d2.lon) > 0.0005: continue

                dist_h = fast_distance_m(d1.lat, d1.lon, d2.lat, d2.lon)
                dist_v = abs(d1.alt - d2.alt)
                pair_id = tuple(sorted([d1.drone_id, d2.drone_id]))
                
                if dist_h < COLLISION_RADIUS_M and dist_v < COLLISION_ALT_M:
                    if pair_id not in metrics["historico_colisoes"]:
                        metrics["historico_colisoes"].add(pair_id)
                        metrics["colisoes_unicas"] += 1
                        metrics["log_detalhado_colisoes"].append({"tick": tick, "hora_simulada": round(tick / 3600, 2), "envolvidos": pair_id})
                elif dist_h > 160.0: 
                    if pair_id in metrics["historico_colisoes"]: metrics["historico_colisoes"].remove(pair_id)
                    if pair_id in metrics["historico_ocorrencias"]: metrics["historico_ocorrencias"].remove(pair_id)

        if tick > 0 and tick % 7200 == 0: 
            print(f"  -> {tick//3600}h simuladas...")

    ineficiencia_pct = 0.0
    if metrics["distancia_ideal_total"] > 0:
        ineficiencia_pct = ((metrics["distancia_real_total"] - metrics["distancia_ideal_total"]) / metrics["distancia_ideal_total"]) * 100

    tempo_execucao = time.time() - start_sim_time
    print(f"[FIM {num_drones:04} DRONES] Concluído em {tempo_execucao:.1f}s | Ineficiência: {ineficiencia_pct:.2f}% | Evasões: {metrics['ocorrencias_unicas']} | Colisões: {metrics['colisoes_unicas']}")

    critical_start, critical_end = 0, 600 
    if metrics["log_ocorrencias"]:
        blocos_5min = [t // 300 for t in metrics["log_ocorrencias"]]
        pior_bloco = Counter(blocos_5min).most_common(1)[0][0]
        critical_start = max(0, (pior_bloco * 300) - 120)
        critical_end = min(total_ticks, (pior_bloco * 300) + 180)

    clip_critico = [f for f in flight_data if critical_start <= f["tick"] <= critical_end]
    
    return {
        "num_drones": num_drones, 
        "colisoes": metrics["colisoes_unicas"],
        "ocorrencias": metrics["ocorrencias_unicas"],
        "ineficiencia_pct": ineficiencia_pct,
        "log_colisoes": metrics["log_detalhado_colisoes"], 
        "clip_critico": clip_critico
    }

def gerar_relatorios(resultados):
    print("\n--- SALVANDO DADOS ORGANIZADOS ---")
    
    log_geral = {}
    for res in resultados:
        log_geral[f"{res['num_drones']}_drones"] = {
            "ineficiencia_pct": res["ineficiencia_pct"],
            "total_ocorrencias_evitadas": res["ocorrencias"],
            "total_colisoes_falhas": res["colisoes"],
            "detalhes_colisoes": res["log_colisoes"]
        }
        
    caminho_log = os.path.join(OUTPUT_DIR, "log_consolidado_cenario2.json")
    with open(caminho_log, "w") as f:
        json.dump(log_geral, f, indent=4)

    x_drones = [r["num_drones"] for r in resultados]
    y_ineficiencia = [r["ineficiencia_pct"] for r in resultados]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x_drones, y_ineficiencia, marker='o', color='purple', linewidth=2, markersize=6)
    plt.axhline(y=MAX_INEFICIENCIA_ACEITAVEL, color='r', linestyle='--', label=f"Limiar de Colapso Logístico ({MAX_INEFICIENCIA_ACEITAVEL}%)")
    
    plt.title("Saturação do Espaço Aéreo: Ineficiência de Rota por DAA (Cenário 2)", fontsize=12)
    plt.xlabel("Quantidade de Drones Simultâneos", fontsize=11)
    plt.ylabel("Aumento Percentual da Rota Voada (%)", fontsize=11)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    for x, y in zip(x_drones, y_ineficiencia): 
        plt.text(x, y + (max(max(y_ineficiencia), MAX_INEFICIENCIA_ACEITAVEL)*0.02), f"{y:.1f}%", ha='center', va='bottom', fontsize=8)
        
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_ineficiencia_rota.png"), dpi=300, bbox_inches='tight')
    plt.close()
    
    if len(resultados) > 0:
        res_inicio = resultados[0] 
        res_meio = resultados[len(resultados)//2] 
        res_fim = resultados[-1] 

        selecionados = [("Inicio", res_inicio), ("Intermediario", res_meio), ("Saturado", res_fim)]

        for nome, res in selecionados:
            caminho_pb = os.path.join(OUTPUT_DIR, f"playback_cenario2_{nome}_{res['num_drones']}drones.json")
            with open(caminho_pb, "w") as f: 
                json.dump(res["clip_critico"], f)

    print("\n--- PROCESSO TOTALMENTE FINALIZADO ---")

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"==================================================")
    print(f" MOTOR DE BUSCA DE SATURAÇÃO - CENÁRIO 2")
    print(f" O teste vai escalar de 50 em 50 drones até quebrar.")
    print(f"==================================================\n")
    
    resultados = []
    num_drones = 50
    step = 50
    
    try:
        while True:
            res = run_scenario_scale(num_drones)
            resultados.append(res)
            
            if res["ineficiencia_pct"] >= MAX_INEFICIENCIA_ACEITAVEL:
                print(f"\n[!!!] SATURAÇÃO LOGÍSTICA ATINGIDA EM {num_drones} DRONES [!!!]")
                break
                
            if res["colisoes"] >= MAX_COLISOES_ACEITAVEIS:
                print(f"\n[!!!] SATURAÇÃO DE SEGURANÇA ATINGIDA EM {num_drones} DRONES [!!!]")
                break
                
            num_drones += step
            
    except KeyboardInterrupt:
        print("\n\n[!] Teste interrompido pelo usuário...")
    
    if len(resultados) > 0:
        gerar_relatorios(resultados)