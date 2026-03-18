import os
import time
import math
import json
import random
import multiprocessing
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point as ShapelyPoint

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Resultados_Cenario1")

# --- CONFIGURAÇÕES DO CENÁRIO 1 ---
SCENARIO_ID = 1
SIMULATION_HOURS = 8
MACPROXY_RADIUS_M = 20.0
MACPROXY_ALT_M = 10.0

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
        self.cruise_altitude = random.uniform(30.0, 50.0) 
        self.idle_timer = random.uniform(0, 120)

    def update_kinematics(self, dt):
        if self.state == "IDLE":
            self.idle_timer -= dt
            if self.idle_timer <= 0:
                self.target_lat, self.target_lon = get_random_point_in_sjc()
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
            else:
                bearing = calculate_bearing(self.lat, self.lon, self.target_lat, self.target_lon)
                distance_to_move = self.speed_ms * dt
                self.lat, self.lon = move_point_fast(self.lat, self.lon, distance_to_move, bearing)

        elif self.state == "LANDING":
            self.alt -= self.vertical_speed * dt
            if self.alt <= 0.0:
                self.alt = 0.0
                self.state = "IDLE"
                self.idle_timer = 300.0 

def run_scenario_scale(num_drones):
    print(f"[{num_drones:03} Drones] Iniciando simulação de Baseline (Voo Cego)...")
    drones = [DroneOriginal(f"DRN_{i}") for i in range(num_drones)]
    total_ticks = SIMULATION_HOURS * 3600
    dt = 1.0 
    
    metrics = {"macproxy_unicos": 0, "historico_macproxy": set(), "log_detalhado": []}
    flight_data = [] 

    for tick in range(total_ticks):
        frame = {"tick": tick, "drones": []}
        
        for d in drones:
            d.update_kinematics(dt)
            if tick % 1 == 0: 
                frame["drones"].append({"id": d.drone_id, "lat": d.lat, "lon": d.lon, "alt": round(d.alt,2), "state": d.state})
                
        if tick % 1 == 0:
            flight_data.append(frame)

        # OTIMIZAÇÃO: Grade Espacial (Spatial Hashing)
        grid = defaultdict(list)
        for d in drones:
            if d.alt >= 5.0: 
                gy, gx = int(d.lat * 1000), int(d.lon * 1000)
                grid[(gy, gx)].append(d)

        for d1 in drones:
            if d1.alt < 5.0: continue
            gy, gx = int(d1.lat * 1000), int(d1.lon * 1000)
            
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    for d2 in grid[(gy + dy, gx + dx)]:
                        if d1.drone_id < d2.drone_id: 
                            dist_h = fast_distance_m(d1.lat, d1.lon, d2.lat, d2.lon)
                            dist_v = abs(d1.alt - d2.alt)
                            
                            pair_id = (d1.drone_id, d2.drone_id)
                            
                            if dist_h < MACPROXY_RADIUS_M and dist_v < MACPROXY_ALT_M:
                                if pair_id not in metrics["historico_macproxy"]:
                                    metrics["historico_macproxy"].add(pair_id)
                                    metrics["macproxy_unicos"] += 1
                                    metrics["log_detalhado"].append({
                                        "tick": tick,
                                        "hora_simulada": round(tick / 3600, 2),
                                        "envolvidos": pair_id,
                                        "coordenada": {"lat": round(d1.lat, 5), "lon": round(d1.lon, 5), "alt": round(d1.alt, 2)}
                                    })
                            elif dist_h > 40.0:
                                if pair_id in metrics["historico_macproxy"]:
                                    metrics["historico_macproxy"].remove(pair_id)

    print(f"[FIM {num_drones:03} DRONES] Concluído. Ocorrências MACproxy: {metrics['macproxy_unicos']}")

    critical_start, critical_end = 0, 600 
    if metrics["log_detalhado"]:
        blocos_5min = [log["tick"] // 300 for log in metrics["log_detalhado"]]
        pior_bloco = Counter(blocos_5min).most_common(1)[0][0]
        critical_start = max(0, (pior_bloco * 300) - 120)
        critical_end = min(total_ticks, (pior_bloco * 300) + 180)

    clip_critico = [f for f in flight_data if critical_start <= f["tick"] <= critical_end]
    
    return {
        "num_drones": num_drones,
        "macproxy": metrics["macproxy_unicos"],
        "log_detalhado": metrics["log_detalhado"],
        "clip_critico": clip_critico
    }

def gerar_grafico_baseline(resultados):
    resultados.sort(key=lambda x: x["num_drones"])
    
    x_drones = [r["num_drones"] for r in resultados]
    y_macproxy = [r["macproxy"] for r in resultados]
    
    plt.figure(figsize=(12, 6)) # Levemente mais largo para acomodar 30 pontos
    plt.plot(x_drones, y_macproxy, marker='o', color='red', linewidth=2, markersize=5)
    
    plt.title("Baseline de Caos: Ocorrências de MACproxy (Sem DAA/xTM)", fontsize=12)
    plt.xlabel("Quantidade de Drones Simultâneos", fontsize=11)
    plt.ylabel("Falhas Críticas de Separação (MACproxy) em 8 Horas", fontsize=11)
    
    # Adicionando grid em ambos os eixos para facilitar a leitura de alta resolução
    plt.xticks(x_drones[::2], rotation=45) # Exibe rótulos a cada 10 drones no eixo X para não embolar
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Adiciona os rótulos de dados de forma intercalada ou espaçada para não sobrepor
    for x, y in zip(x_drones, y_macproxy): 
        if x % 10 == 0: # Imprime o rótulo numérico a cada 10 drones para o gráfico ficar limpo
            plt.text(x, y + max(y_macproxy)*0.02, f"{y}", ha='center', va='bottom', fontsize=8)
        
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "grafico_macproxy_cenario1.png"), dpi=300)
    plt.close()
    print("[+] Gráfico de MACproxy do Baseline gerado com sucesso.")

if __name__ == "__main__":
    # Teste de 5 a 150, passo 5
    escalas = list(range(5, 151, 5)) 
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Iniciando simulações... Os resultados serão salvos na pasta: {OUTPUT_DIR}")
    start_time = time.time()
    
    with multiprocessing.Pool(processes=8) as pool:
        resultados = pool.map(run_scenario_scale, escalas)
        
    print(f"\nTempo total real de processamento: {time.time() - start_time:.2f} segundos")
    print("\n--- SALVANDO DADOS ORGANIZADOS ---")
    
    log_geral = {}
    for res in resultados:
        log_geral[f"{res['num_drones']}_drones"] = {
            "total_macproxy": res["macproxy"],
            "detalhes": res["log_detalhado"]
        }
        
    caminho_log = os.path.join(OUTPUT_DIR, "log_consolidado_macproxy.json")
    with open(caminho_log, "w") as f:
        json.dump(log_geral, f, indent=4)
    print(f"[+] Log único consolidado salvo com sucesso.")
    
    gerar_grafico_baseline(resultados)
    
    print("\n[+] Selecionando Playbacks representativos (Baixa, Média e Alta Densidade):")
    
    # Reajuste dos recortes de densidade para o limite de 150 drones
    baixa_densidade = [r for r in resultados if r["num_drones"] <= 50]
    media_densidade = [r for r in resultados if 50 < r["num_drones"] <= 100]
    alta_densidade  = [r for r in resultados if r["num_drones"] > 100]
    
    casos_selecionados = []
    if baixa_densidade: casos_selecionados.append(max(baixa_densidade, key=lambda x: x["macproxy"]))
    if media_densidade: casos_selecionados.append(max(media_densidade, key=lambda x: x["macproxy"]))
    if alta_densidade: casos_selecionados.append(max(alta_densidade, key=lambda x: x["macproxy"]))

    for res in casos_selecionados:
        categoria = "Baixa" if res["num_drones"] <= 50 else ("Média" if res["num_drones"] <= 100 else "Alta")
        nome_arquivo = f"playback_{categoria.lower()}_densidade_{res['num_drones']}drones.json"
        caminho_pb = os.path.join(OUTPUT_DIR, nome_arquivo)
        
        with open(caminho_pb, "w") as f:
            json.dump(res["clip_critico"], f)
        print(f"    -> Categoria {categoria} ({res['num_drones']} drones): salvo como {nome_arquivo} ({res['macproxy']} MACproxies)")
        
    print("\n--- FINALIZADO COM SUCESSO ---")