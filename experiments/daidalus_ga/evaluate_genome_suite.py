#!/usr/bin/env python3
"""
Evaluate one genome (Daidalus tune) across a **scenario suite** and print a scalar objective.

  python3 experiments/daidalus_ga/evaluate_genome_suite.py \\
    --genome experiments/daidalus_ga/best_genome.json \\
    --suite core

Env:
  BIN  path to hpm_utm_simulator (default: target/release/hpm_utm_simulator)
  SUITE_AGGREGATE  mean | max | sum  (default mean)
  DAIDALUS_EVAL_WORKERS  default max parallel scenarios (default 16)

Use `--parallel --workers 16` to run scenarios concurrently (same as `run_daidalus_optimization.py`).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_GA_DIR = os.path.dirname(os.path.abspath(__file__))
if _GA_DIR not in sys.path:
    sys.path.insert(0, _GA_DIR)
BIN = os.environ.get("BIN", os.path.join(REPO, "target", "release", "hpm_utm_simulator"))
_ENC_BATTERY = os.path.join(REPO, "experiments", "encounter_battery")
if _ENC_BATTERY not in sys.path:
    sys.path.insert(0, _ENC_BATTERY)
from daidalus_sim_config_shared import build_daidalus_sim_config  # noqa: E402

from objective_and_suites import (  # noqa: E402
    ObjectiveWeights,
    ScenarioSpec,
    aggregate_objectives,
    default_core_suite,
    default_fast_suite,
    default_full_suite,
    load_sim_metrics,
    scalar_objective,
    scenario_spec_from_dict,
    scenario_spec_to_dict,
    suite_by_name,
)


def _load_encounter_scenarios():
    p = os.path.join(REPO, "experiments", "encounter_battery", "run_encounter_experiments.py")
    spec = importlib.util.spec_from_file_location("enc", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.SCENARIOS


def run_encounter_case(
    genome: dict,
    spec: ScenarioSpec,
    scenarios_map: dict,
    timeout_s: int,
    *,
    bin_path: str | None = None,
) -> tuple[int, dict]:
    enc = scenarios_map.get(spec.encounter_key or "")
    if not enc:
        raise KeyError(spec.encounter_key)
    cpp = spec.cpp_distance_filter_m
    if cpp is None:
        cpp = float(genome["cpp_distance_filter_m"])
    cfg = build_daidalus_sim_config(
        genome,
        spec.duration_s,
        cpp_distance_filter_m=cpp,
        log_interval_s=2.0,
        show_progress_bar=False,
        log_level="metrics",
    )
    scenario_data = {
        "drones": enc["drones"],
        "obstacles": [],
        "departure_landing_zones": [],
    }
    tmp = tempfile.mkdtemp(prefix="eval_enc_")
    try:
        os.makedirs(os.path.join(tmp, "config"), exist_ok=True)
        with open(os.path.join(tmp, "config", "scenario_dynamic.json"), "w") as f:
            json.dump(scenario_data, f)
        with open(os.path.join(tmp, "config", "sim_config.json"), "w") as f:
            json.dump(cfg, f)
        exe = bin_path or BIN
        proc = subprocess.run([exe], cwd=tmp, capture_output=True, text=True, timeout=timeout_s)
        sm_path = os.path.join(tmp, "sim_metrics.json")
        sm: dict = {}
        if os.path.isfile(sm_path):
            sm = load_sim_metrics(sm_path)
        return proc.returncode, sm
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_sjc_gen_case(
    genome: dict,
    spec: ScenarioSpec,
    timeout_s: int,
    *,
    bin_path: str | None = None,
    repo_root: str | None = None,
    python_exe: str | None = None,
) -> tuple[int, dict]:
    if not spec.sjc:
        raise ValueError("sjc tuple required")
    scen_id, num_drones, seed = spec.sjc
    cpp = spec.cpp_distance_filter_m
    if cpp is None:
        cpp = float(genome["cpp_distance_filter_m"])
    cfg = build_daidalus_sim_config(
        genome,
        spec.duration_s,
        cpp_distance_filter_m=cpp,
        log_interval_s=2.0,
        show_progress_bar=False,
        log_level="metrics",
    )
    root = repo_root or REPO
    py = python_exe or sys.executable
    sjc_script = os.path.join(root, "sjc_scenario_gen.py")
    tmp = tempfile.mkdtemp(prefix="eval_sjc_")
    try:
        subprocess.run(
            [
                py,
                sjc_script,
                "--scenario",
                scen_id,
                "--num_drones",
                str(num_drones),
                "--seed",
                str(seed),
                "--output_dir",
                tmp,
                "--log_level",
                "metrics",
                "--log_interval",
                "2.0",
                "--physics_hz",
                "10.0",
            ],
            cwd=root,
            check=True,
        )
        cfg_dir = os.path.join(tmp, "config")
        os.makedirs(cfg_dir, exist_ok=True)
        with open(os.path.join(cfg_dir, "sim_config.json"), "w") as f:
            json.dump(cfg, f)
        exe = bin_path or BIN
        proc = subprocess.run([exe], cwd=tmp, capture_output=True, text=True, timeout=timeout_s)
        sm_path = os.path.join(tmp, "sim_metrics.json")
        sm: dict = {}
        if os.path.isfile(sm_path):
            sm = load_sim_metrics(sm_path)
        return proc.returncode, sm
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _mp_run_single_scenario(payload: dict) -> dict:
    """Module-level worker for `multiprocessing` (must be picklable)."""
    spec = scenario_spec_from_dict(payload["spec"])
    genome = payload["genome"]
    repo = payload["repo"]
    bin_path = payload["bin"]
    py = payload.get("python") or sys.executable
    w = ObjectiveWeights()
    scenarios_map = _load_encounter_scenarios()
    timeout_s = int(spec.duration_s) + 300
    try:
        if spec.encounter_key:
            rc, sm = run_encounter_case(
                genome, spec, scenarios_map, timeout_s, bin_path=bin_path
            )
        elif spec.sjc:
            rc, sm = run_sjc_gen_case(
                genome, spec, timeout_s, bin_path=bin_path, repo_root=repo, python_exe=py
            )
        else:
            return {"name": spec.name, "rc": -1, "sm": {}, "j": float("inf"), "error": "invalid spec"}
    except subprocess.TimeoutExpired:
        return {"name": spec.name, "rc": -1, "sm": {}, "j": float("inf"), "error": "timeout"}
    except Exception as e:
        return {"name": spec.name, "rc": -1, "sm": {}, "j": float("inf"), "error": str(e)}
    j = scalar_objective(sm, w, scenario_weight=spec.weight) if sm else float("inf")
    if rc != 0:
        j = float("inf")
    return {"name": spec.name, "rc": rc, "sm": sm, "j": j, "error": None}


def evaluate_genome_suite_parallel(
    genome: dict,
    suite: list[ScenarioSpec],
    *,
    max_workers: int = 16,
    aggregate: str = "mean",
) -> tuple[float, list[dict]]:
    """Run all scenarios in parallel; return (aggregate_J, per_scenario dicts)."""
    from concurrent.futures import ProcessPoolExecutor, as_completed

    payloads = [
        {
            "genome": genome,
            "spec": scenario_spec_to_dict(s),
            "repo": REPO,
            "bin": BIN,
            "python": sys.executable,
        }
        for s in suite
    ]
    workers = max(1, min(max_workers, len(suite)))
    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(_mp_run_single_scenario, p) for p in payloads]
        for fut in as_completed(futs):
            results.append(fut.result())
    by_name = {r["name"]: r for r in results}
    per_obj: list[tuple[str, float]] = []
    ordered: list[dict] = []
    for s in suite:
        r = by_name.get(s.name)
        if not r:
            per_obj.append((s.name, float("inf")))
            ordered.append({"name": s.name, "error": "missing"})
            continue
        per_obj.append((s.name, r["j"]))
        ordered.append(r)
    J = aggregate_objectives(per_obj, aggregate)
    return J, ordered


def evaluate_genome_suite_sequential(
    genome: dict,
    suite: list[ScenarioSpec],
    aggregate: str = "mean",
) -> tuple[float, list[tuple[str, float, dict]]]:
    """Run scenarios one after another (single process); returns aggregate J and per-scenario rows."""
    scenarios_map = _load_encounter_scenarios()
    w = ObjectiveWeights()
    per_obj: list[tuple[str, float]] = []
    rows: list[tuple[str, float, dict]] = []
    for spec in suite:
        timeout_s = int(spec.duration_s) + 300
        try:
            if spec.encounter_key:
                rc, sm = run_encounter_case(genome, spec, scenarios_map, timeout_s)
            elif spec.sjc:
                rc, sm = run_sjc_gen_case(genome, spec, timeout_s)
            else:
                raise ValueError(spec)
        except subprocess.TimeoutExpired:
            rc, sm = -1, {}
        j = scalar_objective(sm, w, scenario_weight=spec.weight) if sm else float("inf")
        if rc != 0:
            j = float("inf")
        per_obj.append((spec.name, j))
        rows.append((spec.name, j, sm))
    J = aggregate_objectives(per_obj, aggregate)
    return J, rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate Daidalus genome on scenario suite")
    ap.add_argument("--genome", default="", help="Path to JSON with {\"genome\": {...}} or flat tune")
    ap.add_argument("--suite", default="fast", help="fast | core | full")
    ap.add_argument("--aggregate", default=os.environ.get("SUITE_AGGREGATE", "mean"), choices=("mean", "max", "sum"))
    ap.add_argument("--list", action="store_true", help="Print scenario list and exit")
    ap.add_argument(
        "--parallel",
        action="store_true",
        help="Run scenarios in parallel (uses up to --workers processes)",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=int(os.environ.get("DAIDALUS_EVAL_WORKERS", "16")),
        help="Max parallel scenario processes (default 16)",
    )
    args = ap.parse_args()

    if args.suite == "fast":
        suite = default_fast_suite()
    elif args.suite == "core":
        suite = default_core_suite()
    elif args.suite == "full":
        suite = default_full_suite()
    else:
        try:
            suite = suite_by_name(args.suite)
        except ValueError:
            suite = default_fast_suite()

    if args.list:
        for s in suite:
            print(s.name, s.duration_s, s.encounter_key or s.sjc, s.tags)
        return 0

    if not args.genome:
        print("--genome is required unless --list", file=sys.stderr)
        return 2

    if not os.path.isfile(BIN):
        print(f"Missing binary {BIN}", file=sys.stderr)
        return 1

    with open(args.genome) as f:
        raw = json.load(f)
    genome = raw["genome"] if isinstance(raw.get("genome"), dict) else raw

    if args.parallel:
        J, ordered = evaluate_genome_suite_parallel(
            genome, suite, max_workers=args.workers, aggregate=args.aggregate
        )
        for r in ordered:
            sm = r.get("sm") or {}
            print(
                f"{r.get('name','?'):40} rc={r.get('rc', -1):3}  J={r.get('j'):.6g}  "
                f"mac={sm.get('macproxy_count')}  ineff={sm.get('route_inefficiency_pct')}  "
                f"daa={sm.get('daa_alert_pairs')}  "
                f"done={sm.get('completed_missions')}/{sm.get('total_scheduled_missions')}  "
                f"err={r.get('error')}",
                flush=True,
            )
    else:
        scenarios_map = _load_encounter_scenarios()
        w = ObjectiveWeights()
        per_obj: list[tuple[str, float]] = []

        for spec in suite:
            timeout_s = int(spec.duration_s) + 300
            try:
                if spec.encounter_key:
                    rc, sm = run_encounter_case(genome, spec, scenarios_map, timeout_s)
                elif spec.sjc:
                    rc, sm = run_sjc_gen_case(genome, spec, timeout_s)
                else:
                    raise ValueError(spec)
            except subprocess.TimeoutExpired:
                rc, sm = -1, {}
            j = scalar_objective(sm, w, scenario_weight=spec.weight) if sm else float("inf")
            if rc != 0:
                j = float("inf")
            per_obj.append((spec.name, j))
            print(
                f"{spec.name:40} rc={rc:3}  J={j:.6g}  mac={sm.get('macproxy_count')}  "
                f"ineff={sm.get('route_inefficiency_pct')}  daa={sm.get('daa_alert_pairs')}  "
                f"done={sm.get('completed_missions')}/{sm.get('total_scheduled_missions')}",
                flush=True,
            )

        J = aggregate_objectives(per_obj, args.aggregate)
    print(f"\naggregate ({args.aggregate}): {J:.6g}")
    return 0 if J < float("inf") else 1


if __name__ == "__main__":
    sys.exit(main())
