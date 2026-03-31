#!/usr/bin/env python3
"""
Shared helper to build `sim_config.json` for runs that enable the NASA
DAIDALUS arm in the Rust simulator.

This is a lightweight reimplementation tailored for the current repo
state, providing the `build_daidalus_sim_config` function expected by:

- `experiments/xtm_primordial_rust/run_primordial_matrix.py`
- `experiments/xtm_primordial_rust/run_scen4b_full_log.py`
- `experiments/daidalus_ga/*.py` (if used)
"""

from __future__ import annotations

from typing import Dict, Any


def _get_float(genome: Dict[str, Any], key: str, default: float) -> float:
    try:
        return float(genome.get(key, default))
    except (TypeError, ValueError):
        return float(default)


def _get_int(genome: Dict[str, Any], key: str, default: int) -> int:
    try:
        return int(genome.get(key, default))
    except (TypeError, ValueError):
        return int(default)


def build_daidalus_sim_config(
    genome: Dict[str, Any],
    duration_s: float,
    *,
    cpp_distance_filter_m: float,
    log_interval_s: float,
    show_progress_bar: bool,
    physics_hz: float,
    log_level: str,
) -> Dict[str, Any]:
    """
    Return a `sim_config.json`-style dictionary enabling DAIDALUS
    with tuning parameters sourced from a GA `genome` dict.

    The signature matches the call sites in the experiment scripts.
    """

    sim: Dict[str, Any] = {
        "duration": float(duration_s),
        "collision_threshold": 20.0,
        "show_progress_bar": bool(show_progress_bar),
        "avoidance_mode": "Daidalus",
        "scenario_file": "config/scenario_dynamic.json",
        "enable_mqtt": False,
        "log_level": str(log_level),
        "log_interval_s": float(log_interval_s),
        "physics_hz": float(physics_hz),
        # DAIDALUS evaluation interval; fall back to 1 Hz if genome missing field.
        "daa_interval_s": _get_float(genome, "daa_interval_s", 1.0),
        # Route metrics parity with xTM primordial experiments.
        "route_ideal_distance_mode": "chord",
        "route_metrics_timing": "mission_complete",
    }

    tune: Dict[str, Any] = {
        "evasion_offset_m": _get_float(genome, "evasion_offset_m", 200.0),
        "evasion_duration_s": _get_float(genome, "evasion_duration_s", 6.0),
        "heading_blend": _get_float(genome, "heading_blend", 0.5),
        "track_mix": _get_float(genome, "track_mix", 0.25),
        "min_alert_level": _get_int(genome, "min_alert_level", 1),
        "cpp_distance_filter_m": float(cpp_distance_filter_m),
        "cpp_lookahead_s": _get_float(genome, "cpp_lookahead_s", 0.0),
        "cpp_horizontal_nmac_m": _get_float(genome, "cpp_horizontal_nmac_m", 0.0),
        "max_cross_track_m": _get_float(genome, "max_cross_track_m", 350.0),
        "final_approach_no_reactive_radius_m": _get_float(
            genome, "final_approach_no_reactive_radius_m", 120.0
        ),
        "daa_intruder_eval_mode": genome.get("daa_intruder_eval_mode", "pairwise"),
        "action_mode": genome.get("action_mode", "safe_band"),
        "trigger_mode": genome.get("trigger_mode", "alert_level"),
        "ttv_threshold_s": _get_float(genome, "ttv_threshold_s", 10.0),
        "discrete_turn_deg": _get_float(genome, "discrete_turn_deg", 60.0),
        "discrete_hold_s": _get_float(genome, "discrete_hold_s", 3.0),
    }

    return {"simulation": sim, "simulation_daidalus": {"daidalus_tune": tune}}

