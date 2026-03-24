#!/usr/bin/env python3
"""
Rust equivalents of ``xTM_refs/testeprimordial1.py`` … ``testeprimordial4b.py`` via ``sjc_scenario_gen.py``.

For each SJC scenario (``1`` = blind baseline, ``2`` = geometric DAA, ``3`` = xTM tubes,
``4a`` / ``4b`` = xTM + tighter DAA / wind-style), runs the **same** generated traffic twice:

- **no_daidalus** — avoidance mode from ``sjc_scenario_gen.SCENARIO_AVOIDANCE`` (None / Python2 / …).
- **daidalus** — ``avoidance_mode: Daidalus`` + ``daidalus_tune`` from ``experiments/daidalus_ga/best_genome.json``
  (``cpp_distance_filter_m`` forced to **0** for sparse cruise; see ``daidalus_sim_config_shared``).

Environment (optional):

- ``PRIMORDIAL_DURATION_S`` — default ``28800`` (8 h, matches Python). Use ``600`` or ``120`` for smoke tests.
- ``PRIMORDIAL_NUM_DRONES`` — default ``50``.
- ``PRIMORDIAL_SEED`` — default ``42``.
- ``PRIMORDIAL_PHYSICS_HZ`` — default ``1.0`` (parity with Python 1 Hz feel).
- ``PRIMORDIAL_WORKERS`` — parallel processes (default ``min(8, cpu_count)``).
- ``PRIMORDIAL_GENOME`` — path to genome JSON (default: ``experiments/daidalus_ga/best_genome.json``).

Writes under ``experiments/xtm_primordial_rust/results/<run_id>/`` and ``analysis_summary.json``.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ENC = os.path.join(REPO, "experiments", "encounter_battery")
_GA = os.path.join(REPO, "experiments", "daidalus_ga")
if _ENC not in sys.path:
    sys.path.insert(0, _ENC)
from daidalus_sim_config_shared import build_daidalus_sim_config  # noqa: E402

_BIN = os.path.join(REPO, "target", "release", "hpm_utm_simulator")
BIN = _BIN + (".exe" if sys.platform == "win32" and not _BIN.endswith(".exe") else "")
SJC_GEN = os.path.join(REPO, "sjc_scenario_gen.py")
SCENARIOS = ("1", "2", "3", "4a", "4b", "4c")
MODES = ("no_daidalus", "daidalus")


def _load_genome(path: str) -> dict:
    with open(path) as f:
        raw = json.load(f)
    g = raw.get("best_genome") if isinstance(raw.get("best_genome"), dict) else raw
    if not isinstance(g, dict):
        raise ValueError(f"No genome dict in {path}")
    return g


def _scenario_cache_dir(
    out_base: str, scenario: str, num_drones: int, seed: int, physics_hz: float
) -> str:
    return os.path.join(
        out_base,
        "_scenario_cache",
        f"scen{scenario}_n{num_drones}_s{seed}_ph{physics_hz}",
    )


def _ensure_scenario_generated(
    cache_dir: str,
    scenario: str,
    num_drones: int,
    seed: int,
    physics_hz: float,
) -> str:
    scen_path = os.path.join(cache_dir, "config", "scenario_dynamic.json")
    if os.path.isfile(scen_path):
        return cache_dir
    os.makedirs(cache_dir, exist_ok=True)
    cmd = [
        sys.executable,
        SJC_GEN,
        "--scenario",
        scenario,
        "--num_drones",
        str(num_drones),
        "--seed",
        str(seed),
        "--output_dir",
        cache_dir,
        "--log_level",
        "metrics",
        "--log_interval",
        "5.0",
        "--physics_hz",
        str(physics_hz),
    ]
    p = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"sjc_scenario_gen failed: {p.stderr or p.stdout}")
    if not os.path.isfile(scen_path):
        raise FileNotFoundError(f"Missing {scen_path} after generation")
    return cache_dir


def _read_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _write_json(path: str, obj: dict) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)


def _patch_baseline_config(
    base_sim: dict, duration_s: float, physics_hz: float, log_interval_s: float
) -> dict:
    cfg = json.loads(json.dumps(base_sim))
    sim = cfg.setdefault("simulation", {})
    sim["duration"] = float(duration_s)
    sim["physics_hz"] = float(physics_hz)
    sim["log_interval_s"] = float(log_interval_s)
    sim["log_level"] = "metrics"
    sim["show_progress_bar"] = False
    sim["route_ideal_distance_mode"] = "chord"
    sim["route_metrics_timing"] = "mission_complete"
    return cfg


def _run_single_job(payload: dict) -> dict:
    """Process-pool worker."""
    tag = payload["tag"]
    work = payload["work_dir"]
    genome = payload["genome"]
    mode = payload["mode"]
    duration_s = float(payload["duration_s"])
    physics_hz = float(payload["physics_hz"])
    bin_path = payload["bin_path"]
    cache_dir = payload["cache_dir"]

    result: dict = {
        "tag": tag,
        "mode": mode,
        "scenario": str(payload["scenario"]),
        "rc": -1,
        "error": None,
        "sim_metrics": None,
        "work_dir": work,
    }
    try:
        os.makedirs(os.path.join(work, "config"), exist_ok=True)
        shutil.copy2(
            os.path.join(cache_dir, "config", "scenario_dynamic.json"),
            os.path.join(work, "config", "scenario_dynamic.json"),
        )
        base_cfg_path = os.path.join(cache_dir, "config", "sim_config.json")
        base_sim = _read_json(base_cfg_path)

        if mode == "no_daidalus":
            cfg = _patch_baseline_config(base_sim, duration_s, physics_hz, 5.0)
        else:
            cfg = build_daidalus_sim_config(
                genome,
                duration_s,
                cpp_distance_filter_m=0.0,
                log_interval_s=5.0,
                show_progress_bar=False,
                physics_hz=physics_hz,
                log_level="metrics",
            )
            # Keep metric semantics aligned with Python and baseline arm.
            cfg.setdefault("simulation", {})["route_ideal_distance_mode"] = "chord"
            cfg["simulation"]["route_metrics_timing"] = "mission_complete"
        with open(os.path.join(work, "config", "sim_config.json"), "w") as f:
            json.dump(cfg, f, indent=2)

        timeout_s = max(600, int(duration_s * 4) + 300)
        proc = subprocess.run(
            [bin_path],
            cwd=work,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        result["rc"] = proc.returncode
        result["stderr_tail"] = (proc.stderr or "")[-4000:]
        sm_path = os.path.join(work, "sim_metrics.json")
        if os.path.isfile(sm_path):
            result["sim_metrics"] = _read_json(sm_path)
        if proc.returncode != 0:
            result["error"] = f"exit {proc.returncode}"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
        result["traceback"] = traceback.format_exc()
    return result


def _metrics_subset(m: dict | None) -> dict:
    if not m:
        return {}
    keys = (
        "macproxy_count",
        "macproxy_active_pairs",
        "daa_alert_pairs",
        "total_scheduled_missions",
        "completed_missions",
        "incomplete_missions_total",
        "route_inefficiency_pct",
        "total_real_distance_m",
        "total_ideal_distance_m",
    )
    return {k: m.get(k) for k in keys if k in m}


def run_analysis(results: list[dict]) -> dict:
    by_scen: dict[str, dict] = {}
    for r in results:
        s = str(r.get("scenario", ""))
        mode = r.get("mode")
        if s not in by_scen:
            by_scen[s] = {}
        by_scen[s][mode] = r

    comparisons: list[dict] = []
    for s in SCENARIOS:
        pair = by_scen.get(s, {})
        nd = pair.get("no_daidalus")
        da = pair.get("daidalus")
        if not nd or not da:
            comparisons.append({"scenario": s, "error": "missing arm"})
            continue
        m0 = nd.get("sim_metrics") or {}
        m1 = da.get("sim_metrics") or {}
        comparisons.append(
            {
                "scenario": s,
                "python_reference": {
                    "1": "testeprimordial1 — blind baseline",
                    "2": "testeprimordial2 — geometric DAA, no xTM",
                    "3": "testeprimordial3 — xTM tubes, no tactical DAA in generator",
                    "4a": "testeprimordial4 — xTM + DAA (4A-style)",
                    "4b": "testeprimordial4b — xTM + DAA + wind-style (4B)",
                    "4c": "new 4C — mixed-fleet xTM + DAA + wind-style",
                }.get(s, s),
                "no_daidalus": _metrics_subset(m0),
                "daidalus": _metrics_subset(m1),
                "delta_daidalus_minus_baseline": {
                    "macproxy_count": _num(m1.get("macproxy_count"))
                    - _num(m0.get("macproxy_count")),
                    "route_inefficiency_pct": _num(m1.get("route_inefficiency_pct"))
                    - _num(m0.get("route_inefficiency_pct")),
                    "completed_missions": _num(m1.get("completed_missions"))
                    - _num(m0.get("completed_missions")),
                    "daa_alert_pairs": _num(m1.get("daa_alert_pairs"))
                    - _num(m0.get("daa_alert_pairs")),
                },
            }
        )
    return {"comparisons": comparisons, "by_scenario_keys": list(by_scen.keys())}


def _num(x) -> float:
    if x is None:
        return 0.0
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="xTM primordial Rust matrix (SJC gen vs Daidalus)")
    ap.add_argument(
        "--genome",
        default=os.path.join(_GA, "best_genome.json"),
        help="Genome JSON (with best_genome wrapper ok)",
    )
    ap.add_argument("--out", default=None, help="Output directory (default: results/<stamp>)")
    ap.add_argument("--workers", type=int, default=None)
    args = ap.parse_args()

    if not os.path.isfile(BIN):
        print(f"Build release binary first: {BIN}", file=sys.stderr)
        return 1
    if not os.path.isfile(SJC_GEN):
        print(f"Missing {SJC_GEN}", file=sys.stderr)
        return 1

    duration_s = float(os.environ.get("PRIMORDIAL_DURATION_S", "28800"))
    num_drones = int(os.environ.get("PRIMORDIAL_NUM_DRONES", "50"))
    seed = int(os.environ.get("PRIMORDIAL_SEED", "42"))
    physics_hz = float(os.environ.get("PRIMORDIAL_PHYSICS_HZ", "1.0"))
    workers = args.workers or int(os.environ.get("PRIMORDIAL_WORKERS", "0")) or min(
        8, (os.cpu_count() or 4)
    )
    genome_path = os.environ.get("PRIMORDIAL_GENOME", args.genome)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_base = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "results", f"run_{stamp}"
    )
    os.makedirs(out_base, exist_ok=True)

    genome = _load_genome(genome_path)

    meta = {
        "created_utc": stamp,
        "duration_s": duration_s,
        "num_drones": num_drones,
        "seed": seed,
        "physics_hz": physics_hz,
        "genome_path": os.path.abspath(genome_path),
        "scenarios": list(SCENARIOS),
        "modes": list(MODES),
        "workers": workers,
    }
    _write_json(os.path.join(out_base, "run_meta.json"), meta)

    print(
        f"out={out_base}\n"
        f"duration_s={duration_s} num_drones={num_drones} seed={seed} "
        f"physics_hz={physics_hz} workers={workers}",
        flush=True,
    )

    jobs: list[dict] = []
    for scenario in SCENARIOS:
        cache_dir = _scenario_cache_dir(out_base, scenario, num_drones, seed, physics_hz)
        _ensure_scenario_generated(cache_dir, scenario, num_drones, seed, physics_hz)
        for mode in MODES:
            tag = f"scen{scenario}_n{num_drones}_s{seed}_{mode}"
            work = os.path.join(out_base, tag)
            jobs.append(
                {
                    "tag": tag,
                    "work_dir": work,
                    "genome": genome,
                    "mode": mode,
                    "scenario": scenario,
                    "duration_s": duration_s,
                    "physics_hz": physics_hz,
                    "bin_path": BIN,
                    "cache_dir": cache_dir,
                }
            )

    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_run_single_job, j): j["tag"] for j in jobs}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            err = r.get("error")
            sm = r.get("sim_metrics")
            print(
                f"  [{r.get('tag')}] rc={r.get('rc')} "
                f"macproxy={sm.get('macproxy_count') if sm else 'n/a'} "
                f"{'ERR ' + err if err else 'ok'}",
                flush=True,
            )

    analysis = run_analysis(results)
    analysis["run_meta"] = meta
    analysis["raw_results"] = [
        {
            "tag": r.get("tag"),
            "scenario": r.get("scenario"),
            "mode": r.get("mode"),
            "rc": r.get("rc"),
            "error": r.get("error"),
            "metrics": _metrics_subset(r.get("sim_metrics")),
        }
        for r in results
    ]
    _write_json(os.path.join(out_base, "analysis_summary.json"), analysis)

    # Markdown report
    lines = [
        "# xTM primordial (Rust) — Daidalus vs baseline",
        "",
        f"- Output: `{out_base}`",
        f"- Duration (s): **{duration_s}**, drones: **{num_drones}**, seed **{seed}**",
        f"- Genome: `{genome_path}`",
        "",
        "| Scen | Python analogue | macproxy (no DAID) | macproxy (DAID) | Δ macproxy | ineff % (no) | ineff % (DAID) | Δ DAA pairs |",
        "|------|-----------------|--------------------|-----------------|------------|--------------|----------------|-------------|",
    ]
    for c in analysis["comparisons"]:
        if c.get("error"):
            lines.append(f"| {c.get('scenario')} | — | — | — | — | — | — | — |")
            continue
        d = c.get("delta_daidalus_minus_baseline") or {}
        nd = c.get("no_daidalus") or {}
        da = c.get("daidalus") or {}
        ref = (c.get("python_reference") or "").replace("|", "/")[:44]
        lines.append(
            f"| {c.get('scenario')} | {ref} | {nd.get('macproxy_count')} | {da.get('macproxy_count')} | "
            f"{d.get('macproxy_count')} | {nd.get('route_inefficiency_pct')} | "
            f"{da.get('route_inefficiency_pct')} | {d.get('daa_alert_pairs')} |"
        )
    lines.append("")
    report_md = "\n".join(lines)
    with open(os.path.join(out_base, "REPORT.md"), "w") as f:
        f.write(report_md)
    print("\n" + report_md, flush=True)
    print(f"\nWrote {out_base}/analysis_summary.json and REPORT.md", flush=True)

    final_md = _build_final_analysis_md(meta, analysis, results)
    with open(os.path.join(out_base, "FINAL_ANALYSIS.md"), "w", encoding="utf-8") as f:
        f.write(final_md)
    print(f"Wrote {out_base}/FINAL_ANALYSIS.md", flush=True)
    return 0 if all(r.get("rc") == 0 for r in results) else 2


def _build_final_analysis_md(meta: dict, analysis: dict, results: list[dict]) -> str:
    """Narrative summary for overnight runs (paired with analysis_summary.json)."""
    lines: list[str] = [
        "# Primordial matrix — final analysis (Daidalus vs baseline)",
        "",
        "## Run configuration",
        "",
        f"- **UTC stamp**: `{meta.get('created_utc')}`",
        f"- **Simulation duration (s)**: {meta.get('duration_s')}",
        f"- **Drones**: {meta.get('num_drones')}, **seed**: {meta.get('seed')}",
        f"- **physics_hz**: {meta.get('physics_hz')}",
        f"- **Parallel workers**: {meta.get('workers')}",
        f"- **Genome**: `{meta.get('genome_path')}` (includes `daidalus_tune`, e.g. `daa_intruder_eval_mode`).",
        f"- **Daidalus arm**: `build_daidalus_sim_config` with **cpp_distance_filter_m = 0** (wide-area traffic).",
        f"- **Baseline arm**: avoidance from `sjc_scenario_gen` only; `log_level: metrics`.",
        "",
        "## Job outcomes",
        "",
    ]
    ok = sum(1 for r in results if r.get("rc") == 0 and not r.get("error"))
    bad = [r for r in results if r.get("rc") != 0 or r.get("error")]
    lines.append(f"- **Succeeded**: {ok} / {len(results)}")
    if bad:
        lines.append("- **Failed or errors**:")
        for r in bad:
            lines.append(
                f"  - `{r.get('tag')}`: rc={r.get('rc')}, {r.get('error') or 'no error string'}"
            )
    else:
        lines.append("- All subprocesses exited 0.")
    lines.extend(["", "## Scenario-by-scenario comparison", ""])

    for c in analysis.get("comparisons") or []:
        if c.get("error"):
            lines.append(f"### Scenario {c.get('scenario')} — **incomplete** ({c.get('error')})")
            lines.append("")
            continue
        s = c.get("scenario")
        ref = c.get("python_reference") or ""
        nd = c.get("no_daidalus") or {}
        da = c.get("daidalus") or {}
        d = c.get("delta_daidalus_minus_baseline") or {}
        lines.append(f"### Scenario {s}")
        lines.append(f"*{ref}*")
        lines.append("")
        lines.append("| Metric | Baseline (no NASA DAIDALUS) | + Daidalus (Rust) | Δ (Daidalus − baseline) |")
        lines.append("|--------|-----------------------------|---------------------|-------------------------|")
        lines.append(
            f"| MACproxy count | {nd.get('macproxy_count')} | {da.get('macproxy_count')} | **{d.get('macproxy_count')}** |"
        )
        lines.append(
            f"| Route inefficiency % | {nd.get('route_inefficiency_pct')} | {da.get('route_inefficiency_pct')} | **{d.get('route_inefficiency_pct')}** |"
        )
        lines.append(
            f"| Completed missions | {nd.get('completed_missions')} | {da.get('completed_missions')} | **{d.get('completed_missions')}** |"
        )
        lines.append(
            f"| DAA alert pairs (Rust metric) | {nd.get('daa_alert_pairs')} | {da.get('daa_alert_pairs')} | **{d.get('daa_alert_pairs')}** |"
        )
        lines.append("")

        mac_d = _num(d.get("macproxy_count"))
        ineff_d = _num(d.get("route_inefficiency_pct"))
        done_d = _num(d.get("completed_missions"))
        blurb: list[str] = []
        if mac_d < 0:
            blurb.append("MACproxy **decreased** with Daidalus (fewer near-NMAC proximity events).")
        elif mac_d > 0:
            blurb.append(
                "MACproxy **increased** with Daidalus — can indicate more conservative separation "
                "detection or different trajectories; interpret with inefficiency and completions."
            )
        else:
            blurb.append("MACproxy unchanged.")
        if ineff_d > 0:
            blurb.append("Route inefficiency **rose** (more path length vs chord ideal, often from lateral avoidance).")
        elif ineff_d < 0:
            blurb.append("Route inefficiency **fell**.")
        if done_d < 0:
            blurb.append("**Fewer** missions completed within the horizon (possible delays or timeouts).")
        elif done_d > 0:
            blurb.append("**More** missions completed.")
        lines.append("**Interpretation:** " + " ".join(blurb))
        lines.append("")

    lines.extend(
        [
            "## Overall notes",
            "",
            "- **MACproxy** and **route_inefficiency_pct** use Rust `sim_metrics.json` at exit; "
            "baseline uses `route_metrics_timing: mission_complete` (totals when missions finish).",
            "- Daidalus arm uses the **current** `best_genome.json` reactive tuning (evasion, "
            "`min_alert_level`, `daa_intruder_eval_mode`, etc.).",
            "- This matrix does **not** re-run Python xTM; it compares two Rust configurations on "
            "the **same** `sjc_scenario_gen` instance per scenario.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
