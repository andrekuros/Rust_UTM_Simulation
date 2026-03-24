#!/usr/bin/env python3
"""
Scenario 2 — Daidalus action-mode scalability sweep (24 runs).

For each N in {50, 100, 200, 500, 1000, 2000}:
  - Shared scenario cache per N (one sjc_scenario_gen call).
  - no_daidalus (Python2 baseline from scenario 2).
  - daidalus × (safe_band | preferred_horizontal_resolution | discrete_action).

Fixed: scenario=2, duration_s=3600 (1 h sim), physics_hz=10, seed=42.
Default log_level=metrics (no NDJSON flood).

WARNINGS:
  - N=1000/2000 × 3600 s × 10 Hz can take very long wall time and high RAM.
  - Scenario 2 has no xTM in sjc_scenario_gen; mean authorization delay in
    generation_metrics is 0 — not a Daidalus effect.
  - daa_alert_pairs mixes geometric shell (no_daidalus) vs DAIDALUS bands — compare trends carefully.

Usage:
  python experiments/xtm_primordial_rust/run_scen2_daidalus_sweep.py \\
    --output-dir experiments/xtm_primordial_rust/results/scen2_sweep_demo

  python .../run_scen2_daidalus_sweep.py --skip-runs --aggregate-from <existing_run_dir>
    (rebuild aggregate + figures from prior run)
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PRIMORDIAL_DIR = Path(__file__).resolve().parent


def _load_run_from_config():
    path = PRIMORDIAL_DIR / "run_from_config.py"
    spec = importlib.util.spec_from_file_location("_rfc_sweep", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


RFC = _load_run_from_config()

DRONE_COUNTS = (50, 100, 200, 500, 1000, 2000)

VARIANTS = (
    ("no_daidalus_python2", "no_daidalus", None),
    ("daidalus_safe_band", "daidalus", "safe_band"),
    ("daidalus_preferred_horizontal_resolution", "daidalus", "preferred_horizontal_resolution"),
    ("daidalus_discrete_action", "daidalus", "discrete_action"),
)


def _default_base_cfg(
    *,
    seed: int,
    genome_path: str,
    log_level: str,
    log_interval_s: float,
    cpp_distance_filter_m: float,
) -> dict:
    return {
        "experiment_type": "standard",
        "scenario": "2",
        "duration_s": 3600.0,
        "physics_hz": 10.0,
        "seed": seed,
        "show_progress_bar": True,
        "log_level": log_level,
        "log_interval_s": log_interval_s,
        "cpp_distance_filter_m": cpp_distance_filter_m,
        "daa_intruder_eval_mode": "multi",
        "daa_action_mode": "safe_band",
        "daa_trigger_mode": "alert_level",
        "daa_ttv_threshold_s": 10.0,
        "daa_discrete_turn_deg": 60.0,
        "daa_discrete_hold_s": 3.0,
        "route_ideal_distance_mode": "chord",
        "route_metrics_timing": "mission_complete",
        "mission_complete_proximity_m": 0.0,
        "no_daidalus_avoidance_mode": None,
        "genome_path": genome_path,
        "mode": "both",
        "output_dir": "",
    }


def _load_genome(path: Path) -> dict:
    raw = RFC._load_json(path)
    g = raw.get("best_genome") if isinstance(raw.get("best_genome"), dict) else raw
    if not isinstance(g, dict):
        raise ValueError(f"No genome dict in {path}")
    return g


def _run_variant(
    *,
    num_drones: int,
    variant_id: str,
    arm: str,
    daa_action_mode: str | None,
    cache_dir: Path,
    arm_dir: Path,
    cfg: dict,
    genome: dict | None,
    sim_bin: Path,
) -> dict:
    c = dict(cfg)
    c["num_drones"] = int(num_drones)
    if daa_action_mode is not None:
        c["daa_action_mode"] = daa_action_mode
    t0 = time.perf_counter()
    res = RFC._run_arm(
        arm=arm,
        arm_dir=arm_dir,
        cache_dir=cache_dir,
        sim_bin=sim_bin,
        cfg=c,
        genome=genome,
    )
    res["variant_id"] = variant_id
    res["num_drones"] = num_drones
    res["daa_action_mode"] = daa_action_mode or ""
    wall_extra = time.perf_counter() - t0
    res["wall_seconds_script"] = round(wall_extra, 3)
    RFC._write_json(arm_dir / "sweep_cell.json", {"cfg": c, "result": {k: res[k] for k in res if k != "metrics"}})
    return res


def _daa_pairs_scalar(v) -> int | str:
    if v is None:
        return ""
    if isinstance(v, list):
        return len(v)
    return v


def _row_from_result(res: dict) -> dict:
    m = res.get("metrics") or {}
    ts = m.get("total_scheduled_missions")
    co = m.get("completed_missions")
    ratio = None
    try:
        if ts is not None and float(ts) > 0 and co is not None:
            ratio = float(co) / float(ts)
    except (TypeError, ValueError):
        ratio = None
    return {
        "variant_id": res.get("variant_id", ""),
        "arm": res.get("arm", ""),
        "daa_action_mode": res.get("daa_action_mode", ""),
        "num_drones": res.get("num_drones", ""),
        "rc": res.get("rc", ""),
        "wall_seconds": res.get("wall_seconds", ""),
        "realtime_x": res.get("realtime_x", ""),
        "macproxy_count": m.get("macproxy_count", ""),
        "daa_alert_pairs": _daa_pairs_scalar(m.get("daa_alert_pairs")),
        "completed_missions": co,
        "total_scheduled_missions": ts,
        "completion_ratio": ratio,
        "incomplete_missions_total": m.get("incomplete_missions_total", ""),
        "route_inefficiency_pct": m.get("route_inefficiency_pct", ""),
        "telemetry_bytes": res.get("telemetry_bytes", ""),
    }


def _write_aggregate_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    keys = list(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def _write_aggregate_json(path: Path, rows: list[dict], meta: dict) -> None:
    RFC._write_json(path, {"meta": meta, "rows": rows})


def _collect_rows_from_run_dir(run_dir: Path) -> list[dict]:
    rows = []
    runs = run_dir / "runs"
    if not runs.is_dir():
        return rows
    for cell in sorted(runs.iterdir()):
        if not cell.is_dir():
            continue
        sj = cell / "sweep_cell.json"
        sm = cell / "sim_metrics.json"
        if sj.exists():
            data = RFC._load_json(sj)
            res = dict(data.get("result", {}))
            if sm.exists():
                res["metrics"] = RFC._load_json(sm)
            rows.append(_row_from_result(res))
        elif sm.exists():
            m = RFC._load_json(sm)
            parts = cell.name.rsplit("_n", 1)
            variant_id = cell.name
            n = ""
            if len(parts) == 2 and parts[1].isdigit():
                variant_id = parts[0]
                n = int(parts[1])
            rows.append(
                _row_from_result(
                    {
                        "variant_id": variant_id,
                        "arm": "unknown",
                        "daa_action_mode": "",
                        "num_drones": n,
                        "rc": "",
                        "wall_seconds": "",
                        "realtime_x": "",
                        "metrics": m,
                        "telemetry_bytes": 0,
                    }
                )
            )
    rows.sort(key=lambda r: (int(r["num_drones"] or 0), str(r["variant_id"])))
    return rows


def _plot_figures(run_dir: Path, rows: list[dict], skip: bool) -> None:
    if skip:
        print("Skipping plots (--skip-plots).")
        return
    if not rows:
        print("No rows to plot.")
        return
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping figures. pip install matplotlib", file=sys.stderr)
        return

    fig_dir = run_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    by_var: dict[str, list[tuple[int, dict]]] = {}
    for r in rows:
        vid = str(r.get("variant_id", ""))
        try:
            n = int(r["num_drones"])
        except (TypeError, ValueError):
            continue
        by_var.setdefault(vid, []).append((n, r))
    for vid in by_var:
        by_var[vid].sort(key=lambda x: x[0])

    order = [v[0] for v in VARIANTS]
    colors = ["#333333", "#1f77b4", "#ff7f0e", "#2ca02c"]
    markers = ["o", "s", "^", "D"]

    def _series(metric_key: str, ylabel: str, fname: str, ylog: bool = False):
        plt.figure(figsize=(9, 5.5))
        for i, vid in enumerate(order):
            pts = by_var.get(vid, [])
            if not pts:
                continue
            xs = [p[0] for p in pts]
            ys = []
            for _, row in pts:
                v = row.get(metric_key)
                try:
                    ys.append(float(v) if v not in ("", None) else float("nan"))
                except (TypeError, ValueError):
                    ys.append(float("nan"))
            lbl = vid.replace("_", " ")
            plt.plot(
                xs,
                ys,
                marker=markers[i % len(markers)],
                color=colors[i % len(colors)],
                label=lbl,
                linewidth=2,
            )
        plt.xlabel("Number of drones (N)")
        plt.ylabel(ylabel)
        plt.title(f"{ylabel} vs fleet size (scenario 2, 1 h sim, 10 Hz)")
        plt.legend(loc="best", fontsize=8)
        plt.grid(True, alpha=0.3)
        if ylog:
            plt.yscale("log")
        plt.tight_layout()
        plt.savefig(fig_dir / fname, dpi=150)
        plt.close()

    _series("macproxy_count", "MACproxy count (cumulative unique)", "macproxy_vs_N.png")
    _series(
        "daa_alert_pairs",
        "DAA alert pairs (set size at end; geometric vs DAIDALUS)",
        "daa_alert_pairs_vs_N.png",
    )
    _series("completion_ratio", "Completion ratio (completed / scheduled)", "completion_ratio_vs_N.png")
    _series("route_inefficiency_pct", "Route inefficiency (%)", "route_inefficiency_vs_N.png")
    _series("wall_seconds", "Wall time (s)", "wall_seconds_vs_N.png", ylog=True)
    _series("realtime_x", "Sim speed (sim_s / wall_s)", "realtime_x_vs_N.png")

    print(f"Figures written to {fig_dir}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Scenario 2 Daidalus action-mode sweep")
    ap.add_argument(
        "--output-dir",
        default=str(REPO / "experiments" / "xtm_primordial_rust" / "results" / "scen2_daidalus_sweep"),
        help="Base directory; creates timestamped run folder inside",
    )
    ap.add_argument("--run-id", default="", help="Subfolder name (default: UTC timestamp)")
    ap.add_argument("--genome-path", default=str(REPO / "experiments" / "daidalus_ga" / "best_genome.json"))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--log-level", default="metrics", choices=["metrics", "compact", "full"])
    ap.add_argument("--log-interval-s", type=float, default=5.0)
    ap.add_argument("--cpp-distance-filter-m", type=float, default=250.0)
    ap.add_argument("--skip-plots", action="store_true")
    ap.add_argument("--skip-runs", action="store_true", help="Only aggregate + plots from existing run")
    ap.add_argument(
        "--aggregate-from",
        default="",
        help="With --skip-runs, path to existing run directory containing runs/",
    )
    args = ap.parse_args()

    run_id = args.run_id.strip() or datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%SZ")
    if args.skip_runs and args.aggregate_from:
        run_dir = Path(args.aggregate_from).resolve()
    else:
        run_dir = Path(args.output_dir).resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    sim_bin, _ = RFC._bin_paths()
    if not args.skip_runs and not sim_bin.exists():
        print(f"Missing simulator: {sim_bin} (cargo build --release)", file=sys.stderr)
        return 1

    base_cfg = _default_base_cfg(
        seed=args.seed,
        genome_path=str(Path(args.genome_path).resolve()),
        log_level=args.log_level,
        log_interval_s=args.log_interval_s,
        cpp_distance_filter_m=args.cpp_distance_filter_m,
    )

    genome = _load_genome(Path(args.genome_path).resolve()) if Path(args.genome_path).exists() else None
    if not args.skip_runs and genome is None:
        print("Genome required for daidalus arms.", file=sys.stderr)
        return 1

    print("=" * 72)
    print("Scenario 2 Daidalus action-mode sweep")
    print("=" * 72)
    print(f"  run_dir:    {run_dir}")
    print(f"  N:          {list(DRONE_COUNTS)}")
    print(f"  variants:   {len(VARIANTS)} per N  =>  {len(DRONE_COUNTS) * len(VARIANTS)} runs")
    print(f"  sim time:   3600 s   physics: 10 Hz")
    print(f"  log_level:  {args.log_level}")
    print("  NOTE: Large N may take a long time and high RAM.")
    print("=" * 72)

    all_results: list[dict] = []
    rows: list[dict] = []

    if not args.skip_runs:
        for n in DRONE_COUNTS:
            cache_dir = run_dir / "scenario_cache" / f"n{n}"
            RFC._ensure_scenario_cache(
                cache_dir=cache_dir,
                scenario="2",
                num_drones=n,
                seed=args.seed,
                physics_hz=10.0,
                log_level=args.log_level,
                log_interval_s=args.log_interval_s,
            )
            for variant_id, arm, daa_mode in VARIANTS:
                arm_dir = run_dir / "runs" / f"{variant_id}_n{n}"
                arm_dir.mkdir(parents=True, exist_ok=True)
                print(f"\n>>> {variant_id}  N={n}  arm={arm}", flush=True)
                res = _run_variant(
                    num_drones=n,
                    variant_id=variant_id,
                    arm=arm,
                    daa_action_mode=daa_mode,
                    cache_dir=cache_dir,
                    arm_dir=arm_dir,
                    cfg=base_cfg,
                    genome=genome if arm == "daidalus" else None,
                    sim_bin=sim_bin,
                )
                all_results.append(res)
                rows.append(_row_from_result(res))
                print(
                    f"    rc={res['rc']}  wall={res['wall_seconds']}s  mac={res.get('metrics', {}).get('macproxy_count')}  done={res.get('metrics', {}).get('completed_missions')}",
                    flush=True,
                )
    else:
        rows = _collect_rows_from_run_dir(run_dir)
        print(f"Loaded {len(rows)} rows from {run_dir / 'runs'}")

    meta = {
        "run_id": run_id,
        "scenario": "2",
        "duration_s": 3600,
        "physics_hz": 10,
        "seed": args.seed,
        "drone_counts": list(DRONE_COUNTS),
        "variants": [v[0] for v in VARIANTS],
        "genome_path": str(Path(args.genome_path).resolve()),
        "log_level": args.log_level,
        "repo": str(REPO),
    }
    try:
        meta["git_rev"] = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        meta["git_rev"] = None

    agg_csv = run_dir / "aggregate.csv"
    agg_json = run_dir / "aggregate.json"
    _write_aggregate_csv(agg_csv, rows)
    _write_aggregate_json(agg_json, rows, meta)
    print(f"\nWrote {agg_csv}")
    print(f"Wrote {agg_json}")

    _plot_figures(run_dir, rows, args.skip_plots)

    bad = sum(1 for r in rows if str(r.get("rc")) not in ("0", "None", ""))
    if bad:
        print(f"\nWarning: {bad} runs with non-zero rc.", file=sys.stderr)
    return 0 if bad == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
