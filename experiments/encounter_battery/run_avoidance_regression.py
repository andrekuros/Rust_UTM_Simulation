#!/usr/bin/env python3
"""Regression: encounter battery (known-good 2-drone cases) vs sjc_scenario_gen random seeds.

Uses `daidalus_sim_config_shared.build_daidalus_sim_config` — same tune block as
`run_mixed_20_encounters.py` so only `cpp_distance_filter_m` and duration differ on purpose.

For each run, copies `simulation_telemetry.ndjson` and runs `analyze_telemetry_ndjson`
(alerts vs `has_reactive_target`). Writes `results/avoidance_regression/<run_id>/summary.json`.

Env:
  ENCOUNTER_DURATION_S (default 600) — default sim duration for encounters **without** `duration_s` in SCENARIOS;
    SJC-style cases in `run_encounter_experiments` set their own `duration_s` (320–420 s).
  RANDOM_DURATION_S (default 200),
  NUM_DRONES (50), SCENARIO (2), SEEDS (comma-separated, default 42-51),
  RANDOM_CPP_MODE=genome|zero  — random runs only (default **zero**: genome ~200 m hides sparse cruise traffic)
  LOG_INTERVAL_S (default 1.0, aligned with mixed_20)
  RUN_ENCOUNTERS=1 (default), RUN_RANDOM=1 (default), RUN_ID=optional folder name

Quick smoke: RANDOM_DURATION_S=45 SEEDS=42,43
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ENC_BATTERY = os.path.join(REPO, "experiments", "encounter_battery")
if _ENC_BATTERY not in sys.path:
    sys.path.insert(0, _ENC_BATTERY)
from daidalus_sim_config_shared import build_daidalus_sim_config  # noqa: E402

BIN = os.path.join(REPO, "target", "release", "hpm_utm_simulator")
SCENARIO_GEN = os.path.join(REPO, "sjc_scenario_gen.py")
OUT_BASE = os.path.join(REPO, "experiments", "encounter_battery", "results", "avoidance_regression")


def _load_encounter_module():
    p = os.path.join(REPO, "experiments", "encounter_battery", "run_encounter_experiments.py")
    spec = importlib.util.spec_from_file_location("encounter_experiments", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_analyze():
    p = os.path.join(REPO, "experiments", "analyze_telemetry_reactive.py")
    spec = importlib.util.spec_from_file_location("analyze_tr", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_sim_in_tmp(
    cfg: dict,
    scenario_path_or_writer: str | dict,
    timeout_s: int,
) -> tuple[int, dict]:
    """If scenario_path_or_writer is dict, write as scenario_dynamic content."""
    tmp = tempfile.mkdtemp(prefix="reg_avoid_")
    try:
        cfg_dir = os.path.join(tmp, "config")
        os.makedirs(cfg_dir)
        if isinstance(scenario_path_or_writer, dict):
            with open(os.path.join(cfg_dir, "scenario_dynamic.json"), "w") as f:
                json.dump(scenario_path_or_writer, f, indent=2)
        else:
            shutil.copy2(scenario_path_or_writer, os.path.join(cfg_dir, "scenario_dynamic.json"))
        with open(os.path.join(cfg_dir, "sim_config.json"), "w") as f:
            json.dump(cfg, f, indent=2)
        proc = subprocess.run([BIN], cwd=tmp, capture_output=True, text=True, timeout=timeout_s)
        sm_path = os.path.join(tmp, "sim_metrics.json")
        sm: dict = {}
        if os.path.isfile(sm_path):
            with open(sm_path) as f:
                sm = json.load(f)
        tel = os.path.join(tmp, "simulation_telemetry.ndjson")
        tel_text = None
        if os.path.isfile(tel):
            with open(tel) as f:
                tel_text = f.read()
        return proc.returncode, {
            "sim_metrics": sm,
            "telemetry_text": tel_text,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def write_telemetry(text: str | None, dest: str) -> None:
    if text:
        with open(dest, "w") as f:
            f.write(text)


def main() -> int:
    encounter_mod = _load_encounter_module()
    analyze_mod = _load_analyze()
    analyze_telemetry_ndjson = analyze_mod.analyze_telemetry_ndjson

    if not os.path.isfile(BIN):
        print(f"Missing {BIN} — run: cargo build --release", file=sys.stderr)
        return 1

    genome = encounter_mod.load_genome()
    enc_dur = float(os.environ.get("ENCOUNTER_DURATION_S", "600"))
    rand_dur = float(os.environ.get("RANDOM_DURATION_S", "200"))
    num_drones = int(os.environ.get("NUM_DRONES", "50"))
    scen_id = os.environ.get("SCENARIO", "2")
    seeds_str = os.environ.get("SEEDS", ",".join(str(s) for s in range(42, 52)))
    seeds = [int(x.strip()) for x in seeds_str.split(",") if x.strip()]
    log_interval_s = float(os.environ.get("LOG_INTERVAL_S", "1.0"))
    random_cpp_mode = os.environ.get("RANDOM_CPP_MODE", "zero").strip().lower()
    if random_cpp_mode not in ("genome", "zero"):
        print("RANDOM_CPP_MODE must be genome or zero", file=sys.stderr)
        return 1
    cpp_random = float(genome["cpp_distance_filter_m"]) if random_cpp_mode == "genome" else 0.0
    cpp_encounter = float(genome["cpp_distance_filter_m"])

    run_enc = os.environ.get("RUN_ENCOUNTERS", "1") not in ("0", "false", "no")
    run_rand = os.environ.get("RUN_RANDOM", "1") not in ("0", "false", "no")
    run_id = os.environ.get("RUN_ID") or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_root = os.path.join(OUT_BASE, run_id)
    os.makedirs(out_root, exist_ok=True)

    rows: list[dict] = []
    timeout_rand = int(rand_dur) + 600

    print("=== Avoidance regression ===", flush=True)
    print(f"out: {out_root}", flush=True)
    print(f"encounter cpp_distance_filter_m={cpp_encounter}  random mode={random_cpp_mode} -> {cpp_random}", flush=True)

    if run_enc:
        for name, spec in encounter_mod.SCENARIOS.items():
            case_dur = float(spec.get("duration_s", enc_dur))
            timeout_enc = int(case_dur) + 180
            cfg = build_daidalus_sim_config(
                genome,
                case_dur,
                cpp_distance_filter_m=cpp_encounter,
                log_interval_s=log_interval_s,
                show_progress_bar=False,
            )
            sub = os.path.join(out_root, f"encounter_{name}")
            os.makedirs(sub, exist_ok=True)
            scenario_data = {
                "drones": spec["drones"],
                "obstacles": [],
                "departure_landing_zones": [],
            }
            with open(os.path.join(sub, "sim_config_used.json"), "w") as f:
                json.dump(cfg, f, indent=2)
            print(f"--- encounter: {name} (duration_s={case_dur}) ---", flush=True)
            rc, bundle = run_sim_in_tmp(cfg, scenario_data, timeout_enc)
            write_telemetry(
                bundle.get("telemetry_text"),
                os.path.join(sub, "simulation_telemetry.ndjson"),
            )
            with open(os.path.join(sub, "run.log"), "w") as f:
                f.write(bundle.get("stdout") or "")
                if bundle.get("stderr"):
                    f.write("\n--- stderr ---\n" + bundle["stderr"])
            sm = bundle.get("sim_metrics") or {}
            with open(os.path.join(sub, "sim_metrics.json"), "w") as f:
                json.dump(sm, f, indent=2)
            tel_path = os.path.join(sub, "simulation_telemetry.ndjson")
            stats = analyze_telemetry_ndjson(tel_path)
            with open(os.path.join(sub, "telemetry_analysis.json"), "w") as f:
                json.dump(stats, f, indent=2)
            row = {
                "kind": "encounter",
                "name": name,
                "returncode": rc,
                "daa_alert_pairs": sm.get("daa_alert_pairs"),
                "cpp_distance_filter_m": cpp_encounter,
                **{k: stats[k] for k in ("telemetry_rows", "rows_with_ownship_alert", "alert_with_reactive", "alert_without_reactive", "fraction_alert_without_reactive", "missing_file")},
            }
            rows.append(row)
            print(
                f"  rc={rc} daa_pairs={sm.get('daa_alert_pairs')} "
                f"alert_rows={stats['rows_with_ownship_alert']} "
                f"reactive={stats['alert_with_reactive']} "
                f"alert_only={stats['alert_without_reactive']} "
                f"frac_no_reactive={stats['fraction_alert_without_reactive']}",
                flush=True,
            )

    if run_rand:
        for seed in seeds:
            sub = os.path.join(out_root, f"random_seed_{seed}_cpp_{random_cpp_mode}")
            os.makedirs(sub, exist_ok=True)
            cfg = build_daidalus_sim_config(
                genome,
                rand_dur,
                cpp_distance_filter_m=cpp_random,
                log_interval_s=log_interval_s,
                show_progress_bar=False,
            )
            with open(os.path.join(sub, "sim_config_used.json"), "w") as f:
                json.dump(cfg, f, indent=2)

            tmp = tempfile.mkdtemp(prefix=f"reg_gen_{seed}_")
            try:
                subprocess.run(
                    [
                        sys.executable,
                        SCENARIO_GEN,
                        "--scenario",
                        scen_id,
                        "--num_drones",
                        str(num_drones),
                        "--seed",
                        str(seed),
                        "--output_dir",
                        tmp,
                        "--log_level",
                        "full",
                        "--log_interval",
                        str(log_interval_s),
                        "--physics_hz",
                        "10.0",
                    ],
                    cwd=REPO,
                    check=True,
                )
                cfg_dir = os.path.join(tmp, "config")
                os.makedirs(cfg_dir, exist_ok=True)
                with open(os.path.join(cfg_dir, "sim_config.json"), "w") as f:
                    json.dump(cfg, f, indent=2)
                print(f"--- random seed={seed} scenario={scen_id} ---", flush=True)
                proc = subprocess.run([BIN], cwd=tmp, capture_output=True, text=True, timeout=timeout_rand)
                tel_tmp = os.path.join(tmp, "simulation_telemetry.ndjson")
                if os.path.isfile(tel_tmp):
                    shutil.copy2(tel_tmp, os.path.join(sub, "simulation_telemetry.ndjson"))
                sm_path = os.path.join(tmp, "sim_metrics.json")
                sm = {}
                if os.path.isfile(sm_path):
                    with open(sm_path) as f:
                        sm = json.load(f)
                with open(os.path.join(sub, "sim_metrics.json"), "w") as f:
                    json.dump(sm, f, indent=2)
                with open(os.path.join(sub, "run.log"), "w") as f:
                    f.write(proc.stdout or "")
                    if proc.stderr:
                        f.write("\n--- stderr ---\n" + proc.stderr)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)

            tel_path = os.path.join(sub, "simulation_telemetry.ndjson")
            stats = analyze_telemetry_ndjson(tel_path)
            with open(os.path.join(sub, "telemetry_analysis.json"), "w") as f:
                json.dump(stats, f, indent=2)
            row = {
                "kind": "random",
                "seed": seed,
                "scenario": scen_id,
                "returncode": proc.returncode,
                "daa_alert_pairs": sm.get("daa_alert_pairs"),
                "cpp_distance_filter_m": cpp_random,
                **{k: stats[k] for k in ("telemetry_rows", "rows_with_ownship_alert", "alert_with_reactive", "alert_without_reactive", "fraction_alert_without_reactive", "missing_file")},
            }
            rows.append(row)
            print(
                f"  rc={proc.returncode} daa_pairs={sm.get('daa_alert_pairs')} "
                f"alert_rows={stats['rows_with_ownship_alert']} "
                f"reactive={stats['alert_with_reactive']} "
                f"alert_only={stats['alert_without_reactive']} "
                f"frac_no_reactive={stats['fraction_alert_without_reactive']}",
                flush=True,
            )

    physics_hz = 10.0
    summary = {
        "run_id": run_id,
        "genome_source": getattr(encounter_mod, "BEST_GENOME", None),
        "log_interval_s": log_interval_s,
        "physics_hz": physics_hz,
        "genome_cpp_distance_filter_m": float(genome.get("cpp_distance_filter_m", 0.0)),
        "encounter_cpp_distance_filter_m": cpp_encounter if run_enc else None,
        "random_cpp_mode": random_cpp_mode if run_rand else None,
        "random_cpp_distance_filter_m": cpp_random if run_rand else None,
        "encounter_duration_s": enc_dur if run_enc else None,
        "random_duration_s": rand_dur if run_rand else None,
        "num_drones": num_drones if run_rand else None,
        "scenario": scen_id if run_rand else None,
        "seeds": seeds if run_rand else None,
        "rows": rows,
    }
    with open(os.path.join(out_root, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Table (alert_rows = telemetry rows with ownship collision_alerts) ===", flush=True)
    print(f"{'kind':<12} {'name/seed':<22} {'daa_pairs':>10} {'alert_rows':>10} {'reactive':>10} {'alert_only':>10} {'frac_nr':>8}", flush=True)
    for row in rows:
        label = row.get("name") or f"s{row.get('seed')}"
        fr = row.get("fraction_alert_without_reactive")
        frs = f"{fr:.3f}" if fr is not None else "n/a"
        print(
            f"{row['kind']:<12} {str(label):<22} {str(row.get('daa_alert_pairs')):>10} "
            f"{row['rows_with_ownship_alert']:>10} {row['alert_with_reactive']:>10} "
            f"{row['alert_without_reactive']:>10} {frs:>8}",
            flush=True,
        )

    bad_rc = [r for r in rows if r.get("returncode", 0) != 0]
    return 1 if bad_rc else 0


if __name__ == "__main__":
    sys.exit(main())
