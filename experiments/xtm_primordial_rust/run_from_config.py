#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def _daa_intruder_eval_mode_from_genome(genome: dict) -> str:
    v = str(genome.get("daa_intruder_eval_mode", "pairwise")).strip().lower()
    return v if v in ("pairwise", "multi") else "pairwise"


def _resolve_daa_intruder_eval_mode(genome: dict, cfg: dict) -> str:
    """
    Priority:
    1) run config: daa_intruder_eval_mode (if valid pairwise|multi)
    2) genome: daa_intruder_eval_mode
    3) default: pairwise
    """
    v_cfg = cfg.get("daa_intruder_eval_mode")
    if v_cfg is not None:
        v = str(v_cfg).strip().lower()
        if v in ("pairwise", "multi"):
            return v
    return _daa_intruder_eval_mode_from_genome(genome)


def _resolve_daa_action_mode(cfg: dict) -> str:
    v = str(cfg.get("daa_action_mode", "safe_band")).strip().lower()
    return v if v in ("safe_band", "preferred_horizontal_resolution", "discrete_action") else "safe_band"


def _resolve_daa_trigger_mode(cfg: dict) -> str:
    v = str(cfg.get("daa_trigger_mode", "alert_level")).strip().lower()
    return v if v in ("alert_level", "ttv") else "alert_level"


def _resolve_float(cfg: dict, key: str, default: float) -> float:
    try:
        return float(cfg.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def _mission_complete_proximity_m(cfg: dict) -> float:
    """Horizontal metres to last waypoint for mission complete (0 = require all waypoints / landing)."""
    return max(0.0, _resolve_float(cfg, "mission_complete_proximity_m", 0.0))


def _resolve_no_daidalus_avoidance_mode(cfg: dict) -> str:
    """
    Baseline (no_daidalus) tactical mode:
    - explicit override via `no_daidalus_avoidance_mode`
    - else scenario-based Python parity default
    """
    v = cfg.get("no_daidalus_avoidance_mode")
    if v is not None:
        s = str(v).strip()
        valid = {"None", "Fixed", "Python2", "Python4a", "Python4b"}
        if s in valid:
            return s
    scen = str(cfg.get("scenario", "2")).strip().lower()
    if scen == "2":
        return "Python2"
    if scen == "4a":
        return "Python4a"
    if scen in {"4b", "4c"}:
        return "Python4b"
    return "None"


def _build_daidalus_sim_config(
    *,
    genome: dict,
    cfg: dict,
    duration_s: float,
    cpp_distance_filter_m: float,
    log_interval_s: float,
    show_progress_bar: bool,
    physics_hz: float,
    log_level: str,
) -> dict:
    return {
        "simulation": {
            "duration": float(duration_s),
            "collision_threshold": 20.0,
            "show_progress_bar": bool(show_progress_bar),
            "avoidance_mode": "Daidalus",
            "scenario_file": "config/scenario_dynamic.json",
            "enable_mqtt": False,
            "log_level": str(log_level).strip().lower(),
            "log_interval_s": float(log_interval_s),
            "physics_hz": float(physics_hz),
            "daa_interval_s": float(genome["daa_interval_s"]),
            "daidalus_tune": {
                "evasion_offset_m": float(genome["evasion_offset_m"]),
                "evasion_duration_s": float(genome["evasion_duration_s"]),
                "heading_blend": float(genome["heading_blend"]),
                "track_mix": float(genome["track_mix"]),
                "min_alert_level": int(genome["min_alert_level"]),
                "cpp_distance_filter_m": float(cpp_distance_filter_m),
                "cpp_lookahead_s": float(genome["cpp_lookahead_s"]),
                "cpp_horizontal_nmac_m": float(genome["cpp_horizontal_nmac_m"]),
                "max_cross_track_m": float(genome.get("max_cross_track_m", 350.0)),
                "final_approach_no_reactive_radius_m": float(
                    genome.get("final_approach_no_reactive_radius_m", 0.0)
                ),
                "daa_intruder_eval_mode": _resolve_daa_intruder_eval_mode(genome, cfg),
                "action_mode": _resolve_daa_action_mode(cfg),
                "trigger_mode": _resolve_daa_trigger_mode(cfg),
                "ttv_threshold_s": _resolve_float(cfg, "daa_ttv_threshold_s", 10.0),
                "discrete_turn_deg": _resolve_float(cfg, "daa_discrete_turn_deg", 60.0),
                "discrete_hold_s": _resolve_float(cfg, "daa_discrete_hold_s", 3.0),
            },
            "route_ideal_distance_mode": "chord",
            "route_metrics_timing": "mission_complete",
            "mission_complete_proximity_m": _mission_complete_proximity_m(cfg),
        }
    }


def _bin_paths() -> tuple[Path, Path]:
    sim = REPO / "target" / "release" / "hpm_utm_simulator"
    gen = REPO / "sjc_scenario_gen.py"
    if sys.platform == "win32":
        sim_exe = sim.with_suffix(".exe")
        if sim_exe.exists():
            sim = sim_exe
    return sim, gen


def _ensure_scenario_cache(
    *,
    cache_dir: Path,
    scenario: str,
    num_drones: int,
    seed: int,
    physics_hz: float,
    log_level: str,
    log_interval_s: float,
) -> None:
    scen_path = cache_dir / "config" / "scenario_dynamic.json"
    meta_path = cache_dir / "cache_meta.json"
    expected_meta = {
        "scenario": str(scenario),
        "num_drones": int(num_drones),
        "seed": int(seed),
        "physics_hz": float(physics_hz),
        "log_level": str(log_level),
        "log_interval_s": float(log_interval_s),
    }
    if scen_path.exists() and meta_path.exists():
        try:
            cached_meta = _load_json(meta_path)
        except Exception:
            cached_meta = None
        if cached_meta == expected_meta:
            return
        shutil.rmtree(cache_dir, ignore_errors=True)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(REPO / "sjc_scenario_gen.py"),
        "--scenario",
        scenario,
        "--num_drones",
        str(num_drones),
        "--seed",
        str(seed),
        "--output_dir",
        str(cache_dir),
        "--log_level",
        log_level,
        "--log_interval",
        str(log_interval_s),
        "--physics_hz",
        str(physics_hz),
    ]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"sjc_scenario_gen failed:\n{p.stderr or p.stdout}")
    _write_json(meta_path, expected_meta)


def _base_perf(kind: str, fast: bool = False) -> dict:
    if kind == "fixed":
        return {
            "mass_kg": 12.0 if not fast else 9.0,
            "max_speed_mps": 28.0 if not fast else 34.0,
            "min_speed_mps": 12.0,
            "max_vertical_speed_mps": 2.5,
            "max_turn_rate_deg_s": 18.0 if not fast else 22.0,
            "battery_discharge_rate": 30.0,
        }
    return {
        "mass_kg": 1.5 if not fast else 1.8,
        "max_speed_mps": 18.0 if not fast else 24.0,
        "min_speed_mps": 0.0,
        "max_vertical_speed_mps": 4.0,
        "max_turn_rate_deg_s": 45.0 if not fast else 50.0,
        "battery_discharge_rate": 12.0,
    }


def _mk_drone(drone_id: str, start: tuple[float, float], end: tuple[float, float], *, alt: float, departure_s: float, kind: str, fast: bool = False) -> dict:
    aircraft_kind = "FixedWing" if kind == "fixed" else "Rotorcraft"
    return {
        "id": drone_id,
        "performance": _base_perf(kind, fast=fast),
        "aircraft_kind": aircraft_kind,
        "departure_time_s": float(departure_s),
        "flight_plan": {
            "waypoints": [
                [float(start[0]), 0.0, float(start[1])],
                [float(start[0]), float(alt), float(start[1])],
                [float(end[0]), float(alt), float(end[1])],
                [float(end[0]), 0.0, float(end[1])],
            ],
            "current_waypoint_index": 0,
        },
    }


def _build_encounter_case(case_name: str, mixed_fleet: bool) -> list[dict]:
    c = str(case_name).strip().lower()
    if c == "head_on_2":
        return [
            _mk_drone("E1_A", (-900, 0), (900, 0), alt=60, departure_s=0, kind="rotor"),
            _mk_drone("E1_B", (900, 0), (-900, 0), alt=60, departure_s=0, kind="fixed" if mixed_fleet else "rotor"),
        ]
    if c == "cross_90_2":
        return [
            _mk_drone("E2_A", (-900, 0), (900, 0), alt=60, departure_s=0, kind="rotor"),
            _mk_drone("E2_B", (0, -900), (0, 900), alt=60, departure_s=0, kind="fixed" if mixed_fleet else "rotor"),
        ]
    if c == "oblique_45_2":
        return [
            _mk_drone("E3_A", (-900, -300), (900, 300), alt=60, departure_s=0, kind="rotor"),
            _mk_drone("E3_B", (900, -300), (-900, 300), alt=60, departure_s=0, kind="fixed" if mixed_fleet else "rotor"),
        ]
    if c == "overtake_2":
        return [
            _mk_drone("E4_A", (-900, 0), (900, 0), alt=60, departure_s=0, kind="rotor", fast=False),
            _mk_drone("E4_B", (-1200, 0), (900, 0), alt=60, departure_s=8, kind="fixed" if mixed_fleet else "rotor", fast=True),
        ]
    if c == "cross_90_3":
        return [
            _mk_drone("E5_A", (-900, 0), (900, 0), alt=60, departure_s=0, kind="rotor"),
            _mk_drone("E5_B", (0, -900), (0, 900), alt=60, departure_s=0, kind="fixed" if mixed_fleet else "rotor"),
            _mk_drone("E5_C", (900, 140), (-900, 140), alt=60, departure_s=0, kind="rotor"),
        ]
    if c == "merge_3":
        return [
            _mk_drone("E6_A", (-900, -220), (900, 0), alt=65, departure_s=0, kind="rotor"),
            _mk_drone("E6_B", (-900, 220), (900, 0), alt=65, departure_s=0, kind="fixed" if mixed_fleet else "rotor"),
            _mk_drone("E6_C", (0, -900), (900, 0), alt=65, departure_s=0, kind="rotor"),
        ]
    if c == "box_4":
        return [
            _mk_drone("E7_N", (0, -900), (0, 900), alt=70, departure_s=0, kind="rotor"),
            _mk_drone("E7_S", (0, 900), (0, -900), alt=70, departure_s=0, kind="fixed" if mixed_fleet else "rotor"),
            _mk_drone("E7_W", (-900, 0), (900, 0), alt=70, departure_s=0, kind="rotor"),
            _mk_drone("E7_E", (900, 0), (-900, 0), alt=70, departure_s=0, kind="fixed" if mixed_fleet else "rotor"),
        ]
    raise ValueError(f"Unknown encounter_case: {case_name}")


def _ensure_encounter_cache(*, cache_dir: Path, cfg: dict, case_name: str) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)
    scen_dir = cache_dir / "config"
    scen_dir.mkdir(parents=True, exist_ok=True)
    mixed = bool(cfg.get("encounter_mixed_fleet", True))
    drones = _build_encounter_case(case_name, mixed_fleet=mixed)
    scenario_data = {
        "drones": drones,
        "obstacles": [],
        "departure_landing_zones": [],
    }
    _write_json(scen_dir / "scenario_dynamic.json", scenario_data)
    sim_cfg = {
        "simulation": {
            "duration": float(cfg["duration_s"]),
            "collision_threshold": 20.0,
            "show_progress_bar": bool(cfg["show_progress_bar"]),
            "avoidance_mode": "None",
            "scenario_file": "config/scenario_dynamic.json",
            "enable_mqtt": False,
            "log_level": str(cfg["log_level"]).strip().lower(),
            "log_interval_s": float(cfg["log_interval_s"]),
            "physics_hz": float(cfg["physics_hz"]),
            "daa_interval_s": 1.0,
            "route_ideal_distance_mode": str(cfg["route_ideal_distance_mode"]),
            "route_metrics_timing": str(cfg["route_metrics_timing"]),
            "mission_complete_proximity_m": _mission_complete_proximity_m(cfg),
        }
    }
    _write_json(scen_dir / "sim_config.json", sim_cfg)


def _build_baseline_cfg(base_sim: dict, cfg: dict) -> dict:
    out = json.loads(json.dumps(base_sim))
    sim = out.setdefault("simulation", {})
    sim["duration"] = float(cfg["duration_s"])
    sim["physics_hz"] = float(cfg["physics_hz"])
    sim["log_level"] = str(cfg["log_level"])
    sim["log_interval_s"] = float(cfg["log_interval_s"])
    sim["show_progress_bar"] = bool(cfg["show_progress_bar"])
    sim["route_ideal_distance_mode"] = str(cfg["route_ideal_distance_mode"])
    sim["route_metrics_timing"] = str(cfg["route_metrics_timing"])
    sim["mission_complete_proximity_m"] = _mission_complete_proximity_m(cfg)
    sim["avoidance_mode"] = _resolve_no_daidalus_avoidance_mode(cfg)
    return out


def _build_daidalus_cfg(cfg: dict, genome: dict) -> dict:
    out = _build_daidalus_sim_config(
        genome=genome,
        cfg=cfg,
        duration_s=float(cfg["duration_s"]),
        cpp_distance_filter_m=float(cfg["cpp_distance_filter_m"]),
        log_interval_s=float(cfg["log_interval_s"]),
        show_progress_bar=bool(cfg["show_progress_bar"]),
        physics_hz=float(cfg["physics_hz"]),
        log_level=str(cfg["log_level"]),
    )
    sim = out.setdefault("simulation", {})
    sim["route_ideal_distance_mode"] = str(cfg["route_ideal_distance_mode"])
    sim["route_metrics_timing"] = str(cfg["route_metrics_timing"])
    return out


def _run_arm(*, arm: str, arm_dir: Path, cache_dir: Path, sim_bin: Path, cfg: dict, genome: dict | None) -> dict:
    (arm_dir / "config").mkdir(parents=True, exist_ok=True)
    shutil.copy2(cache_dir / "config" / "scenario_dynamic.json", arm_dir / "config" / "scenario_dynamic.json")
    base_sim = _load_json(cache_dir / "config" / "sim_config.json")

    if arm == "no_daidalus":
        sim_cfg = _build_baseline_cfg(base_sim, cfg)
    else:
        if genome is None:
            raise ValueError("genome is required for daidalus arm")
        sim_cfg = _build_daidalus_cfg(cfg, genome)

    _write_json(arm_dir / "config" / "sim_config.json", sim_cfg)

    t0 = time.perf_counter()
    # Stream simulator stdout/stderr directly so Bevy progress bar is visible live.
    p = subprocess.Popen([str(sim_bin)], cwd=arm_dir)
    rc = p.wait()
    wall_s = time.perf_counter() - t0

    sm_path = arm_dir / "sim_metrics.json"
    metrics = _load_json(sm_path) if sm_path.exists() else None
    sim_s = float(cfg["duration_s"])
    rt_x = (sim_s / wall_s) if wall_s > 0 else None
    tel = arm_dir / "simulation_telemetry.ndjson"

    return {
        "arm": arm,
        "rc": rc,
        "wall_seconds": round(wall_s, 3),
        "sim_seconds": sim_s,
        "realtime_x": round(rt_x, 4) if rt_x is not None else None,
        "running_speed_x": round(rt_x, 4) if rt_x is not None else None,
        "telemetry_bytes": tel.stat().st_size if tel.exists() else 0,
        "metrics": metrics,
        "stderr_tail": "",
    }


def _authorization_delay_context(
    *,
    generation_metrics: dict,
    generation_metrics_path: Path | None,
    scenario: str,
    duration_s: float,
    experiment_type: str,
) -> dict:
    """
    Explains why mean_authorization_delay_* does not change with Rust duration_s and how it
    differs from testeprimordial4.py runtime averaging.
    """
    exp = str(experiment_type).strip().lower()
    has_file = generation_metrics_path is not None and generation_metrics_path.exists()
    if exp == "encounter_suite":
        return {
            "source": "not_applicable (encounter_suite has no sjc_scenario_gen / generation_metrics.json)",
            "generation_metrics_path": None,
            "field_used": None,
            "how_computed": "Hand-built encounter scenarios omit xTM pre-planning; study_metrics auth delay is null.",
            "planning_horizon_s": None,
            "planning_horizon_note": None,
            "rust_sim_duration_s": float(duration_s),
            "independent_of_rust_sim_duration": True,
            "scenario_has_xtm_in_generator": False,
            "scenarios_1_and_2_note": None,
            "python_testeprimordial4_comparison": (
                "Python xTM delay is runtime metric_delays; this encounter path does not compute it."
            ),
        }
    scen = str(scenario).strip().lower()
    no_xtm = scen in {"1", "2"}
    return {
        "source": "generation_metrics.json (written by sjc_scenario_gen.py)"
        if has_file
        else "unavailable (missing generation_metrics.json after standard cache build)",
        "generation_metrics_path": str(generation_metrics_path.resolve())
        if has_file
        else None,
        "field_used": "mean_xtm_delay_s -> copied to study_metrics as mean_authorization_delay_s",
        "how_computed": (
            "While building scenario_dynamic.json, generate_missions() simulates xTM tube "
            "clearance like testeprimordial3/4: +15 s delay accounting per failed attempt, "
            "one retry per simulation second (start_tick += 1); mean_xtm_delay_s is the mean "
            "of those per-mission deferrals over the generator planning loop."
        ),
        "planning_horizon_s": 28800.0,
        "planning_horizon_note": (
            "Fixed SIM_DURATION in sjc_scenario_gen.py (8 h virtual time), not your run config duration_s."
        ),
        "rust_sim_duration_s": float(duration_s),
        "independent_of_rust_sim_duration": True,
        "scenario_has_xtm_in_generator": not no_xtm,
        "scenarios_1_and_2_note": (
            "No xTM reservation in the generator; mean_xtm_delay_s is 0. Python scen 2 also has no xTM."
        )
        if no_xtm
        else None,
        "python_testeprimordial4_comparison": (
            "Python computes atraso_medio from xtm.metric_delays during the full Python simulation "
            "(runtime). This pipeline pre-computes delays at scenario generation; the Rust binary "
            "does not re-simulate xTM or accumulate authorization wait."
        ),
    }


def _study_metrics_by_arm(results: list[dict], generation_metrics: dict | None = None) -> dict:
    """Per-arm study row. mean_authorization_delay_* comes from generation_metrics (see authorization_delay_context)."""
    gen = generation_metrics or {}
    mean_delay_s = gen.get("mean_xtm_delay_s")
    try:
        mean_delay_min = float(mean_delay_s) / 60.0 if mean_delay_s is not None else None
    except (TypeError, ValueError):
        mean_delay_min = None
    out: dict[str, dict] = {}
    for r in results:
        m = r.get("metrics") or {}
        out[r["arm"]] = {
            "mean_authorization_delay_s": mean_delay_s,
            "mean_authorization_delay_min": mean_delay_min,
            "completed_missions": m.get("completed_missions"),
            "total_scheduled_missions": m.get("total_scheduled_missions"),
            "incomplete_missions_total": m.get("incomplete_missions_total"),
            "macproxy_count": m.get("macproxy_count"),
            "daa_alert_pairs": m.get("daa_alert_pairs"),
            "route_inefficiency_pct": m.get("route_inefficiency_pct"),
            "total_real_distance_m": m.get("total_real_distance_m"),
            "total_ideal_distance_m": m.get("total_ideal_distance_m"),
            "running_speed_x": r.get("running_speed_x"),
            "wall_seconds": r.get("wall_seconds"),
            "telemetry_bytes": r.get("telemetry_bytes"),
            "rc": r.get("rc"),
        }
    return out


def _delta_if_both(study_by_arm: dict) -> dict | None:
    nd = study_by_arm.get("no_daidalus")
    da = study_by_arm.get("daidalus")
    if not nd or not da:
        return None

    def num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    def delta(k):
        a = num(da.get(k))
        b = num(nd.get(k))
        if a is None or b is None:
            return None
        return a - b

    return {
        "daidalus_minus_no_daidalus": {
            "mean_authorization_delay_s": delta("mean_authorization_delay_s"),
            "mean_authorization_delay_min": delta("mean_authorization_delay_min"),
            "completed_missions": delta("completed_missions"),
            "incomplete_missions_total": delta("incomplete_missions_total"),
            "macproxy_count": delta("macproxy_count"),
            "daa_alert_pairs": delta("daa_alert_pairs"),
            "route_inefficiency_pct": delta("route_inefficiency_pct"),
            "running_speed_x": delta("running_speed_x"),
            "wall_seconds": delta("wall_seconds"),
        }
    }


def _fmt_num(v, nd=3):
    try:
        return f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return "n/a"


def _fmt_int(v):
    try:
        return str(int(v))
    except (TypeError, ValueError):
        return "n/a"


def _print_kv_block(title: str, rows: list[tuple[str, str]]) -> None:
    print(f"\n{title}")
    width = max((len(k) for k, _ in rows), default=0)
    for k, v in rows:
        print(f"  {k.ljust(width)} : {v}")


def _print_compact_table(headers: list[str], rows: list[list[str]]) -> None:
    all_rows = [headers] + rows
    widths = [max(len(r[i]) for r in all_rows) for i in range(len(headers))]
    fmt = "  " + " | ".join("{:<" + str(w) + "}" for w in widths)
    sep = "  " + "-+-".join("-" * w for w in widths)
    print(fmt.format(*headers))
    print(sep)
    for r in rows:
        print(fmt.format(*r))


def _run_one_case(*, cfg_path: Path, cfg: dict, out_dir: Path, sim_bin: Path, case_label: str) -> tuple[list[dict], dict, dict | None]:
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = out_dir / "_scenario_cache"
    if str(cfg.get("experiment_type", "standard")).strip().lower() == "encounter_suite":
        _ensure_encounter_cache(
            cache_dir=cache_dir,
            cfg=cfg,
            case_name=str(cfg["encounter_case"]),
        )
    else:
        _ensure_scenario_cache(
            cache_dir=cache_dir,
            scenario=str(cfg["scenario"]),
            num_drones=int(cfg["num_drones"]),
            seed=int(cfg["seed"]),
            physics_hz=float(cfg["physics_hz"]),
            log_level=str(cfg["log_level"]),
            log_interval_s=float(cfg["log_interval_s"]),
        )
    generation_metrics: dict = {}
    gm_path = cache_dir / "generation_metrics.json"
    if gm_path.exists():
        generation_metrics = _load_json(gm_path)

    mode = str(cfg["mode"]).strip().lower()
    if mode not in {"both", "no_daidalus", "daidalus"}:
        raise ValueError("mode must be one of: both, no_daidalus, daidalus")

    arms = ["no_daidalus", "daidalus"] if mode == "both" else [mode]
    genome = None
    if "daidalus" in arms:
        genome = _load_json(Path(cfg["genome_path"]).resolve())
        if isinstance(genome.get("best_genome"), dict):
            genome = genome["best_genome"]

    print(f"\n[{case_label}]")
    results = []
    for arm in arms:
        print(f"\nRunning {arm}...", flush=True)
        arm_dir = out_dir / arm
        res = _run_arm(
            arm=arm,
            arm_dir=arm_dir,
            cache_dir=cache_dir,
            sim_bin=sim_bin,
            cfg=cfg,
            genome=genome,
        )
        results.append(res)
        print(f"  done rc={res['rc']} wall={res['wall_seconds']}s x={res['realtime_x']} telemetry={res['telemetry_bytes']} B", flush=True)

    speed_by_arm = {
        r["arm"]: r.get("running_speed_x")
        for r in results
    }
    speed_ratio = None
    if "no_daidalus" in speed_by_arm and "daidalus" in speed_by_arm:
        no_x = speed_by_arm["no_daidalus"]
        da_x = speed_by_arm["daidalus"]
        if isinstance(no_x, (int, float)) and no_x not in (0, 0.0):
            speed_ratio = round(float(da_x) / float(no_x), 6) if da_x is not None else None

    summary = {
        "config_path": str(cfg_path),
        "output_dir": str(out_dir),
        "config_used": cfg,
        "speed_summary": {
            "running_speed_x_by_arm": speed_by_arm,
            "daidalus_vs_no_daidalus_speed_ratio": speed_ratio,
        },
        "study_metrics": _study_metrics_by_arm(results, generation_metrics),
        "authorization_delay_context": _authorization_delay_context(
            generation_metrics=generation_metrics,
            generation_metrics_path=gm_path,
            scenario=str(cfg.get("scenario", "")),
            duration_s=float(cfg.get("duration_s", 0.0)),
            experiment_type=str(cfg.get("experiment_type", "standard")),
        ),
        "results": results,
    }
    delta_block = _delta_if_both(summary["study_metrics"])
    if delta_block is not None:
        summary["study_deltas"] = delta_block
    _write_json(out_dir / "summary.json", summary)
    return results, summary, delta_block


def main() -> int:
    ap = argparse.ArgumentParser(description="Run primordial scenario from one JSON config")
    ap.add_argument("--config", required=True, help="Path to run config JSON")
    args = ap.parse_args()

    cfg_path = Path(args.config).resolve()
    cfg = _load_json(cfg_path)

    defaults = {
        "experiment_type": "standard",  # standard | encounter_suite
        "scenario": "2",
        "num_drones": 50,
        "duration_s": 600.0,
        "seed": 42,
        "physics_hz": 1.0,
        "mode": "both",  # both | no_daidalus | daidalus
        "no_daidalus_avoidance_mode": None,
        "log_level": "full",
        "log_interval_s": 2.0,
        "show_progress_bar": True,
        "cpp_distance_filter_m": 0.0,
        "daa_intruder_eval_mode": None,
        "daa_action_mode": "safe_band",
        "daa_trigger_mode": "alert_level",
        "daa_ttv_threshold_s": 10.0,
        "daa_discrete_turn_deg": 60.0,
        "daa_discrete_hold_s": 3.0,
        "route_ideal_distance_mode": "chord",
        "route_metrics_timing": "mission_complete",
        "mission_complete_proximity_m": 0.0,
        "output_dir": str(REPO / "experiments" / "xtm_primordial_rust" / "results" / "run_from_config"),
        "genome_path": str(REPO / "experiments" / "daidalus_ga" / "best_genome.json"),
        "encounter_drone_counts": [],
        "encounter_cases": [],
        "encounter_mixed_fleet": True,
    }
    for k, v in defaults.items():
        cfg.setdefault(k, v)

    sim_bin, _ = _bin_paths()
    if not sim_bin.exists():
        print(f"Missing simulator binary: {sim_bin}", file=sys.stderr)
        return 1

    out_dir = Path(cfg["output_dir"]).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 72)
    print("Run From Config")
    print("=" * 72)
    _print_kv_block(
        "Config",
        [
            ("experiment_type", str(cfg["experiment_type"])),
            ("scenario", str(cfg["scenario"])),
            ("num_drones", str(cfg["num_drones"])),
            ("duration_s", str(cfg["duration_s"])),
            ("mode", str(cfg["mode"])),
            ("daa_action_mode", str(cfg["daa_action_mode"])),
            ("daa_trigger_mode", str(cfg["daa_trigger_mode"])),
            ("physics_hz", str(cfg["physics_hz"])),
            ("log_level", str(cfg["log_level"])),
            ("log_interval_s", str(cfg["log_interval_s"])),
            ("output_dir", str(out_dir)),
        ],
    )

    experiment_type = str(cfg.get("experiment_type", "standard")).strip().lower()
    if experiment_type not in {"standard", "encounter_suite"}:
        raise ValueError("experiment_type must be one of: standard, encounter_suite")

    if experiment_type == "encounter_suite":
        all_cases = [
            "head_on_2",
            "cross_90_2",
            "oblique_45_2",
            "overtake_2",
            "cross_90_3",
            "merge_3",
            "box_4",
        ]
        cases = cfg.get("encounter_cases") or all_cases
        cases = [str(c).strip().lower() for c in cases]
        bad = [c for c in cases if c not in all_cases]
        if bad:
            raise ValueError(f"Unknown encounter_cases: {bad}")
        encounter_rows = []
        encounter_cases_out = []
        exit_codes = []
        for case_name in cases:
            case_cfg = dict(cfg)
            case_cfg["encounter_case"] = case_name
            case_cfg["num_drones"] = len(_build_encounter_case(case_name, mixed_fleet=bool(cfg.get("encounter_mixed_fleet", True))))
            case_dir = out_dir / f"encounter_{case_name}"
            results, summary, _ = _run_one_case(
                cfg_path=cfg_path,
                cfg=case_cfg,
                out_dir=case_dir,
                sim_bin=sim_bin,
                case_label=f"encounter case: {case_name}",
            )
            exit_codes.extend([int(r.get("rc", 1)) for r in results])
            nd = (summary.get("study_metrics") or {}).get("no_daidalus", {})
            da = (summary.get("study_metrics") or {}).get("daidalus", {})
            encounter_rows.append(
                [
                    case_name,
                    str(case_cfg["num_drones"]),
                    _fmt_int(nd.get("macproxy_count")),
                    _fmt_int(da.get("macproxy_count")),
                    _fmt_num(nd.get("running_speed_x"), 3) + "x",
                    _fmt_num(da.get("running_speed_x"), 3) + "x",
                ]
            )
            encounter_cases_out.append(
                {
                    "case": case_name,
                    "num_drones": int(case_cfg["num_drones"]),
                    "output_dir": str(case_dir),
                    "summary_path": str(case_dir / "summary.json"),
                    "speed_summary": summary.get("speed_summary"),
                    "study_metrics": summary.get("study_metrics"),
                    "study_deltas": summary.get("study_deltas"),
                }
            )
        encounter_summary = {
            "config_path": str(cfg_path),
            "output_dir": str(out_dir),
            "config_used": cfg,
            "experiment_type": "encounter_suite",
            "cases": encounter_cases_out,
        }
        _write_json(out_dir / "summary_encounter_suite.json", encounter_summary)
        print("\n" + "=" * 72)
        print("Encounter Suite Summary")
        print("=" * 72)
        print(f"  summary_json: {out_dir / 'summary_encounter_suite.json'}")
        _print_compact_table(
            ["case", "drones", "mac_no_daa", "mac_daa", "x_no_daa", "x_daa"],
            encounter_rows,
        )
        return 0 if all(rc == 0 for rc in exit_codes) else 2

    encounter_counts = cfg.get("encounter_drone_counts") or []
    try:
        encounter_counts = [int(x) for x in encounter_counts]
    except (TypeError, ValueError):
        encounter_counts = []

    if encounter_counts:
        sweep_rows = []
        encounter_results = []
        exit_codes = []
        for n in encounter_counts:
            case_cfg = dict(cfg)
            case_cfg["num_drones"] = int(n)
            case_dir = out_dir / f"encounter_{int(n)}"
            results, summary, delta_block = _run_one_case(
                cfg_path=cfg_path,
                cfg=case_cfg,
                out_dir=case_dir,
                sim_bin=sim_bin,
                case_label=f"encounter {int(n)} drones",
            )
            encounter_results.append(
                {
                    "num_drones": int(n),
                    "output_dir": str(case_dir),
                    "summary_path": str(case_dir / "summary.json"),
                    "speed_summary": summary.get("speed_summary"),
                    "study_metrics": summary.get("study_metrics"),
                    "study_deltas": summary.get("study_deltas"),
                }
            )
            exit_codes.extend([int(r.get("rc", 1)) for r in results])
            nd = (summary.get("study_metrics") or {}).get("no_daidalus", {})
            da = (summary.get("study_metrics") or {}).get("daidalus", {})
            sweep_rows.append(
                [
                    str(int(n)),
                    _fmt_int(nd.get("macproxy_count")),
                    _fmt_int(da.get("macproxy_count")),
                    _fmt_num(nd.get("running_speed_x"), 3) + "x",
                    _fmt_num(da.get("running_speed_x"), 3) + "x",
                ]
            )
        encounter_summary = {
            "config_path": str(cfg_path),
            "output_dir": str(out_dir),
            "config_used": cfg,
            "encounter_drone_counts": [int(n) for n in encounter_counts],
            "cases": encounter_results,
        }
        _write_json(out_dir / "summary_encounter.json", encounter_summary)
        print("\n" + "=" * 72)
        print("Encounter Summary")
        print("=" * 72)
        print(f"  summary_json: {out_dir / 'summary_encounter.json'}")
        _print_compact_table(
            ["num_drones", "mac_no_daa", "mac_daa", "x_no_daa", "x_daa"],
            sweep_rows,
        )
        return 0 if all(rc == 0 for rc in exit_codes) else 2

    results, summary, delta_block = _run_one_case(
        cfg_path=cfg_path,
        cfg=cfg,
        out_dir=out_dir,
        sim_bin=sim_bin,
        case_label=f"single run ({int(cfg['num_drones'])} drones)",
    )
    speed_ratio = (summary.get("speed_summary") or {}).get("daidalus_vs_no_daidalus_speed_ratio")

    print("\n" + "=" * 72)
    print("Summary")
    print("=" * 72)
    print(f"  summary_json: {out_dir / 'summary.json'}")
    summary_rows = []
    for r in results:
        m = r.get("metrics") or {}
        summary_rows.append(
            [
                r["arm"],
                _fmt_int(r["rc"]),
                _fmt_int(m.get("completed_missions")),
                _fmt_int(m.get("macproxy_count")),
                _fmt_int(m.get("daa_alert_pairs")),
                _fmt_num(r.get("running_speed_x"), 3) + "x",
                _fmt_num(r.get("wall_seconds"), 3) + "s",
            ]
        )
    _print_compact_table(
        ["case", "rc", "done", "macproxy", "alerts", "x_realtime", "wall"],
        summary_rows,
    )
    if speed_ratio is not None:
        print(f"\n  speed_ratio(daidalus/no_daidalus): {_fmt_num(speed_ratio, 6)}")

    print("\nStudy metrics")
    study_rows = []
    for arm, m in summary["study_metrics"].items():
        study_rows.append(
            [
                arm,
                _fmt_num(m.get("mean_authorization_delay_min"), 3),
                f"{_fmt_int(m.get('completed_missions'))}/{_fmt_int(m.get('total_scheduled_missions'))}",
                _fmt_int(m.get("incomplete_missions_total")),
                _fmt_int(m.get("macproxy_count")),
                _fmt_int(m.get("daa_alert_pairs")),
                _fmt_num(m.get("route_inefficiency_pct"), 3),
                _fmt_num(m.get("running_speed_x"), 3) + "x",
            ]
        )
    _print_compact_table(
        [
            "case",
            "auth_delay_min",
            "done/scheduled",
            "incomplete",
            "macproxy",
            "alerts",
            "ineff_pct",
            "x_realtime",
        ],
        study_rows,
    )
    ad_ctx = summary.get("authorization_delay_context") or {}
    if ad_ctx.get("independent_of_rust_sim_duration") and ad_ctx.get("field_used"):
        print(
            "\n  Note: auth_delay_min is from scenario generation (sjc_scenario_gen), "
            "not measured during the Rust run — it does not change when you only change duration_s."
        )
    s12 = ad_ctx.get("scenarios_1_and_2_note")
    if s12:
        print(f"  Note: {s12}")
    if delta_block is not None:
        d = delta_block["daidalus_minus_no_daidalus"]
        print("\nDelta (daidalus - no_daidalus)")
        _print_compact_table(
            ["metric", "delta"],
            [
                ["completed_missions", _fmt_num(d.get("completed_missions"), 3)],
                ["incomplete_missions_total", _fmt_num(d.get("incomplete_missions_total"), 3)],
                ["mean_authorization_delay_s", _fmt_num(d.get("mean_authorization_delay_s"), 3)],
                ["mean_authorization_delay_min", _fmt_num(d.get("mean_authorization_delay_min"), 3)],
                ["macproxy_count", _fmt_num(d.get("macproxy_count"), 3)],
                ["daa_alert_pairs", _fmt_num(d.get("daa_alert_pairs"), 3)],
                ["route_inefficiency_pct", _fmt_num(d.get("route_inefficiency_pct"), 3)],
                ["running_speed_x", _fmt_num(d.get("running_speed_x"), 3)],
                ["wall_seconds", _fmt_num(d.get("wall_seconds"), 3)],
            ],
        )
    return 0 if all(r["rc"] == 0 for r in results) else 2


if __name__ == "__main__":
    sys.exit(main())

