"""Single source for Daidalus `simulation` JSON used by mixed_20 and related runners.

`run_mixed_20_encounters.py` works with **genome** `cpp_distance_filter_m` (~200) because every
pair is laid out in a small arena — intruders stay inside the C++ distance filter.

`sjc_scenario_gen` missions are **sparse** on long legs: with the same 200 m filter, DAIDALUS
often sees no intruder until the terminal area, so avoidance *looks* like it only happens near
departure/landing. For generated traffic use **`cpp_distance_filter_m=0`** (library default /
no filter) unless you intentionally match the genome for dense tests.

All scripts that compare “mixed_20 vs random” should use this builder so only `cpp_distance_filter_m`
(and duration / log_interval) differ on purpose.
"""

from __future__ import annotations


def _daa_intruder_eval_mode_from_genome(genome: dict) -> str:
    v = str(genome.get("daa_intruder_eval_mode", "pairwise")).strip().lower()
    return v if v in ("pairwise", "multi") else "pairwise"


def build_daidalus_sim_config(
    genome: dict,
    duration_s: float,
    *,
    cpp_distance_filter_m: float,
    log_interval_s: float = 1.0,
    show_progress_bar: bool = True,
    physics_hz: float = 10.0,
    log_level: str = "full",
) -> dict:
    return {
        "simulation": {
            "duration": float(duration_s),
            "collision_threshold": 20.0,
            "show_progress_bar": show_progress_bar,
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
                "daa_intruder_eval_mode": _daa_intruder_eval_mode_from_genome(genome),
            },
            "route_ideal_distance_mode": "chord",
            # `spawn` = ideal at spawn + integrate real each tick. Encounter / time-capped runs
            # often never land, so `mission_complete` leaves total_ideal/real at 0. Full pad-to-pad
            # sweeps that need “only finished missions” can override to `mission_complete`.
            "route_metrics_timing": "spawn",
        }
    }
