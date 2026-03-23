#!/usr/bin/env python3
"""
Genetic algorithm to search DAIDALUS + reactive steering parameters.

Uses the same scenario file for every evaluation; only `sim_config.json` changes
(`daidalus_tune`, `daa_interval_s`, `avoidance_mode` forced to Daidalus).

Example:
  python optimize_daidalus_ga.py --generations 12 --population 16 --duration 900 \\
      --num_drones 50 --seed 42 --workers 8 --skip_build

  # xTM + Daidalus (same traffic as 4a/4b generator, mode forced to Daidalus):
  python optimize_daidalus_ga.py --scenario 4a --num_drones 100 --workers 6 --skip_build

Fitness (maximize): missions completed, penalize MACproxy, excess inefficiency, DAA pair churn.

Note: child stdout/stderr are discarded (DEVNULL). Capturing them would risk a full-pipe deadlock
if the binary is verbose (parent waits, child blocks on write → stuck, ~0% CPU).

Each eval copies only `scenario_dynamic.json` (+ optional `generation_metrics.json`) into a fresh
temp dir — not the whole template tree — to avoid filesystem lock / I/O stalls when many jobs run.

Task Manager "Python (N)" counts every Python process on the system (IDE, extensions, etc.). This
script uses one interpreter + threads; each genome evaluation runs `target/release/hpm_utm_simulator`
(Rust) as a subprocess — look for that name for CPU usage, not a 1:1 match with `--workers`.

RTF (real-time factor) printed per eval is simulated_duration / wall_clock (e.g. 1200s sim in 30s
→ RTF≈40×). There is no guarantee of "100×"; it depends on N, DAA cost, physics_hz, and hardware.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import copy
import json
import os
import random
import shutil
import signal
import statistics
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
BIN_SIM = os.path.join(REPO_ROOT, "target", "release", "hpm_utm_simulator")
SCENARIO_GEN = os.path.join(REPO_ROOT, "sjc_scenario_gen.py")

# Search bounds [low, high] — cpp_* use 0 to mean “leave DO_365B default” in C++.
BOUNDS_F = {
    "evasion_offset_m": (45.0, 260.0),
    "evasion_duration_s": (0.6, 12.0),
    "heading_blend": (0.0, 1.0),
    "track_mix": (0.0, 0.9),
    "cpp_distance_filter_m": (0.0, 5500.0),
    "cpp_lookahead_s": (0.0, 360.0),
    "cpp_horizontal_nmac_m": (0.0, 40.0),
    "daa_interval_s": (0.5, 2.5),
}
BOUNDS_I = {
    "min_alert_level": (1, 3),
}


def random_genome(rng: random.Random) -> Dict[str, Any]:
    g: Dict[str, Any] = {}
    for k, (lo, hi) in BOUNDS_F.items():
        g[k] = lo + rng.random() * (hi - lo)
    for k, (lo, hi) in BOUNDS_I.items():
        g[k] = rng.randint(lo, hi)
    return g


def clip_genome(g: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(g)
    for k, (lo, hi) in BOUNDS_F.items():
        out[k] = max(lo, min(hi, float(out[k])))
    for k, (lo, hi) in BOUNDS_I.items():
        out[k] = max(lo, min(hi, int(round(out[k]))))
    return out


def mutate(g: Dict[str, Any], rng: random.Random, rate: float = 0.2, sigma: float = 0.12) -> Dict[str, Any]:
    out = clip_genome(g)
    for k, (lo, hi) in BOUNDS_F.items():
        if rng.random() < rate:
            span = hi - lo
            out[k] = float(out[k]) + rng.gauss(0, sigma * span)
    for k, (lo, hi) in BOUNDS_I.items():
        if rng.random() < rate * 0.5:
            out[k] = rng.randint(lo, hi)
    return clip_genome(out)


def crossover(a: Dict[str, Any], b: Dict[str, Any], rng: random.Random) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    c1, c2 = {}, {}
    for k in a:
        if rng.random() < 0.5:
            c1[k], c2[k] = a[k], b[k]
        else:
            c1[k], c2[k] = b[k], a[k]
    return clip_genome(c1), clip_genome(c2)


def apply_genome_to_config(base: Dict[str, Any], genome: Dict[str, Any]) -> Dict[str, Any]:
    cfg = copy.deepcopy(base)
    sim = cfg.setdefault("simulation", {})
    sim["avoidance_mode"] = "Daidalus"
    sim["daa_interval_s"] = float(genome["daa_interval_s"])
    _dm = str(genome.get("daa_intruder_eval_mode", "pairwise")).strip().lower()
    daa_mode = _dm if _dm in ("pairwise", "multi") else "pairwise"
    sim["daidalus_tune"] = {
        "evasion_offset_m": float(genome["evasion_offset_m"]),
        "evasion_duration_s": float(genome["evasion_duration_s"]),
        "heading_blend": float(genome["heading_blend"]),
        "track_mix": float(genome["track_mix"]),
        "min_alert_level": int(genome["min_alert_level"]),
        "cpp_distance_filter_m": float(genome["cpp_distance_filter_m"]),
        "cpp_lookahead_s": float(genome["cpp_lookahead_s"]),
        "cpp_horizontal_nmac_m": float(genome["cpp_horizontal_nmac_m"]),
        "daa_intruder_eval_mode": daa_mode,
    }
    return cfg


def fitness_from_metrics(m: Dict[str, Any]) -> float:
    """Higher is better."""
    done = float(m.get("completed_missions", 0))
    mac = float(m.get("macproxy_count", 0))
    ineff = float(m.get("route_inefficiency_pct", 0.0))
    pairs = float(m.get("daa_alert_pairs", 0))
    pen_ineff = max(0.0, ineff)
    return (
        done * 1.0
        - 100.0 * mac
        - 0.35 * pen_ineff
        - 0.012 * pairs
    )


def _materialize_minimal_run_dir(template_dir: str, merged_cfg: Dict[str, Any], tmp: str) -> None:
    """Only files the simulator needs; avoids full copytree of large scenario JSON N times in parallel."""
    os.makedirs(os.path.join(tmp, "config"), exist_ok=True)
    scen_src = os.path.join(template_dir, "config", "scenario_dynamic.json")
    if not os.path.isfile(scen_src):
        raise FileNotFoundError(scen_src)
    shutil.copy2(scen_src, os.path.join(tmp, "config", "scenario_dynamic.json"))
    gen_src = os.path.join(template_dir, "generation_metrics.json")
    if os.path.isfile(gen_src):
        shutil.copy2(gen_src, os.path.join(tmp, "generation_metrics.json"))
    with open(os.path.join(tmp, "config", "sim_config.json"), "w") as f:
        json.dump(merged_cfg, f, indent=2)


def _sim_child_env() -> Dict[str, str]:
    """One heavy thread per process so `--workers N` can use ~N cores without oversubscription."""
    env = os.environ.copy()
    for k, v in (
        ("RAYON_NUM_THREADS", "1"),
        ("OMP_NUM_THREADS", "1"),
        ("OPENBLAS_NUM_THREADS", "1"),
        ("MKL_NUM_THREADS", "1"),
        ("NUMEXPR_NUM_THREADS", "1"),
    ):
        env.setdefault(k, v)
    return env


def _run_simulator_hard_timeout(exe: str, cwd: str, timeout_s: float) -> int:
    """Run simulator; on timeout SIGKILL the whole process group (handles hung native code)."""
    proc = subprocess.Popen(
        [exe],
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env=_sim_child_env(),
    )
    try:
        return int(proc.wait(timeout=timeout_s))
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, OSError):
            try:
                proc.kill()
            except ProcessLookupError:
                pass
        try:
            proc.wait(timeout=30)
        except subprocess.TimeoutExpired:
            pass
        return -1


def evaluate_genome(
    template_dir: str,
    genome: Dict[str, Any],
    base_cfg: Dict[str, Any],
    bin_sim: str | None = None,
    subprocess_timeout_s: float = 300.0,
) -> Tuple[float, Dict[str, Any]]:
    """Write minimal run dir, run simulator with hard wall timeout, return (fitness, metrics)."""
    exe = bin_sim or BIN_SIM
    merged = apply_genome_to_config(copy.deepcopy(base_cfg), genome)
    with tempfile.TemporaryDirectory(prefix="ga_daa_") as tmp:
        try:
            _materialize_minimal_run_dir(template_dir, merged, tmp)
        except OSError as e:
            return -1e9, {"error": f"materialize: {e}"}
        rc = _run_simulator_hard_timeout(exe, tmp, float(subprocess_timeout_s))
        if rc != 0:
            err = "timeout (killed)" if rc == -1 else f"exit {rc}"
            return -1e9, {"error": err}
        mp = os.path.join(tmp, "sim_metrics.json")
        if not os.path.isfile(mp):
            return -1e9, {"error": "no sim_metrics.json"}
        with open(mp) as f:
            metrics = json.load(f)
        return fitness_from_metrics(metrics), metrics


def _genome_line(g: Dict[str, Any]) -> str:
    """One-line view of the tunable genes (for evolution visibility)."""
    return (
        f"off={g['evasion_offset_m']:.0f}m evdur={g['evasion_duration_s']:.1f}s "
        f"hblend={g['heading_blend']:.2f} tmix={g['track_mix']:.2f} "
        f"lvl={g['min_alert_level']} daa_ival={g['daa_interval_s']:.2f}s "
        f"cpp_df={g['cpp_distance_filter_m']:.0f} la={g['cpp_lookahead_s']:.0f} nmac={g['cpp_horizontal_nmac_m']:.0f}"
    )


def _sim_rtf(sim_duration_s: float, wall_s: float) -> float:
    """Simulated seconds per wall second (higher = faster). NaN if wall invalid."""
    if wall_s <= 0:
        return float("nan")
    return float(sim_duration_s) / float(wall_s)


def _pbar(done: int, total: int, width: int = 24) -> str:
    if total <= 0:
        return "[]"
    fill = int(width * done / total)
    fill = min(width, max(0, fill))
    return "[" + "=" * fill + "-" * (width - fill) + f"] {done}/{total}"


def tournament_select(pop: List[Dict], fit: List[float], rng: random.Random, k: int = 3) -> Dict[str, Any]:
    idxs = [rng.randrange(len(pop)) for _ in range(k)]
    best_i = max(idxs, key=lambda i: fit[i])
    return copy.deepcopy(pop[best_i])


def _patch_sim_config_for_ga(cfg_path: str, duration: float) -> None:
    with open(cfg_path) as f:
        cfg = json.load(f)
    sim = cfg.setdefault("simulation", {})
    sim["duration"] = float(duration)
    sim["show_progress_bar"] = False
    sim["avoidance_mode"] = "Daidalus"
    sim.setdefault("daa_interval_s", 1.0)
    # Match Python xTM route metrics (chord ideal; fold totals at mission complete).
    sim.setdefault("route_ideal_distance_mode", "chord")
    sim.setdefault("route_metrics_timing", "mission_complete")
    sim.setdefault(
        "daidalus_tune",
        {
            "evasion_offset_m": 200.0,
            "evasion_duration_s": 6.0,
            "heading_blend": 0.5,
            "track_mix": 0.25,
            "min_alert_level": 1,
            "cpp_distance_filter_m": 0.0,
            "cpp_lookahead_s": 0.0,
            "cpp_horizontal_nmac_m": 0.0,
        },
    )
    with open(cfg_path, "w") as f:
        json.dump(cfg, f, indent=2)


def prepare_template(args) -> str:
    """Return a directory to copy for each eval (never mutates user's --template_dir)."""
    if getattr(args, "template_dir", None):
        user_src = os.path.abspath(args.template_dir)
        if not os.path.isdir(os.path.join(user_src, "config")):
            print(f"Invalid --template_dir (missing config/): {user_src}", file=sys.stderr)
            sys.exit(1)
        cache = os.path.join(REPO_ROOT, "experiments", "daidalus_ga", "template_cache")
        if os.path.isdir(cache):
            shutil.rmtree(cache)
        shutil.copytree(user_src, cache)
        _patch_sim_config_for_ga(os.path.join(cache, "config", "sim_config.json"), args.duration)
        return cache

    out = os.path.join(REPO_ROOT, "experiments", "daidalus_ga", "template_run")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            SCENARIO_GEN,
            "--scenario",
            str(args.scenario),
            "--num_drones",
            str(args.num_drones),
            "--output_dir",
            out,
            "--seed",
            str(args.seed),
            "--log_level",
            "metrics",
            "--log_interval",
            str(args.log_interval),
        ],
        check=True,
        cwd=REPO_ROOT,
    )
    _patch_sim_config_for_ga(os.path.join(out, "config", "sim_config.json"), args.duration)
    return out


def main():
    ap = argparse.ArgumentParser(description="GA for DAIDALUS tune + reactive params")
    ap.add_argument("--scenario", default="2", help="sjc_scenario_gen scenario id (1,2,3,4a,4b)")
    ap.add_argument(
        "--template_dir",
        default=None,
        help="Reuse existing run directory (must contain config/ + scenario); skips sjc_scenario_gen",
    )
    ap.add_argument("--num_drones", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--duration", type=float, default=900.0, help="Sim horizon (s) per eval")
    ap.add_argument("--population", type=int, default=16)
    ap.add_argument("--generations", type=int, default=10)
    ap.add_argument("--log_interval", type=float, default=5.0)
    ap.add_argument("--skip_build", action="store_true")
    ap.add_argument("--elite", type=int, default=2, help="Elitism count")
    ap.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Parallel evaluations per generation (1 = sequential). Uses threads; each eval is a separate subprocess with its own cwd.",
    )
    ap.add_argument(
        "--eval-timeout",
        type=float,
        default=None,
        metavar="SEC",
        help="Wall-clock cap per simulator run (default: min(600, max(120, 2*sim_duration+60)))",
    )
    ap.add_argument(
        "--verbose",
        action="store_true",
        help="Reserved for extra debug; per-eval lines are on by default (see --no-progress).",
    )
    ap.add_argument(
        "--no-progress",
        action="store_true",
        help="Disable per-eval lines (ASCII bar + timings + genes); keep generation summaries only",
    )
    args = ap.parse_args()

    if not args.skip_build:
        subprocess.run(["cargo", "build", "--release", "--bin", "hpm_utm_simulator"], cwd=REPO_ROOT, check=True)
    if not os.path.isfile(BIN_SIM):
        print(f"Missing {BIN_SIM}; build first.", file=sys.stderr)
        sys.exit(1)

    rng = random.Random(args.seed + 999)
    template_dir = prepare_template(args)
    eval_timeout = args.eval_timeout
    if eval_timeout is None:
        # Cap so one bad/hung C++ eval cannot stall the whole GA for tens of minutes.
        d = float(args.duration)
        eval_timeout = min(600.0, max(120.0, 2.0 * d + 60.0))
    print(
        f"Template: {template_dir} (scenario {args.scenario}, N={args.num_drones}, "
        f"duration={args.duration}s, workers={args.workers}, eval_timeout={eval_timeout:.0f}s)"
    )
    print(
        f"Each eval runs `{os.path.basename(BIN_SIM)}` (Rust). "
        f"RTF = sim_duration/wall_time (higher = faster). "
        f"Task Manager 'Python (N)' is not the number of simulations.",
        flush=True,
    )

    with open(os.path.join(template_dir, "config", "sim_config.json")) as f:
        base_cfg = json.load(f)

    pop = [random_genome(rng) for _ in range(args.population)]
    fit: List[float] = []
    metrics_log: List[Dict[str, Any]] = []
    show_eval = (not args.no_progress) or args.verbose
    t_run0 = time.perf_counter()

    for gen in range(args.generations):
        fit.clear()
        metrics_log.clear()
        t_gen0 = time.perf_counter()
        print(
            f"\n=== Generation {gen + 1}/{args.generations} "
            f"| {time.strftime('%H:%M:%S')} "
            f"| elapsed={time.perf_counter() - t_run0:.0f}s ===",
            flush=True,
        )
        if args.workers > 1:
            conc = min(args.workers, len(pop))
            print(
                f"  Concurrent evals: {conc} process(es) at a time "
                f"({len(pop)} total this generation; completion order is finish time, not index)",
                flush=True,
            )

        sim_s = float(args.duration)
        gen_wall_times: List[float] = []

        if args.workers <= 1:
            for gi, g in enumerate(pop):
                t0 = time.perf_counter()
                f, m = evaluate_genome(
                    template_dir,
                    g,
                    base_cfg,
                    subprocess_timeout_s=float(eval_timeout),
                )
                dt = time.perf_counter() - t0
                gen_wall_times.append(dt)
                fit.append(f)
                metrics_log.append(m)
                if show_eval:
                    done = gi + 1
                    cm = m.get("completed_missions", "?")
                    rtf = _sim_rtf(sim_s, dt)
                    print(
                        f"  {_pbar(done, len(pop))}  #{gi}  "
                        f"fit={f:8.3f}  wall={dt:5.2f}s  rtf={rtf:5.1f}x  "
                        f"done_missions={cm}  {_genome_line(g)}",
                        flush=True,
                    )
        else:
            slot: List[Optional[Tuple[float, Dict[str, Any]]]] = [None] * len(pop)

            def _thread_eval(i: int, genome: Dict[str, Any]) -> Tuple[int, float, Dict[str, Any], float]:
                t0 = time.perf_counter()
                f, m = evaluate_genome(
                    template_dir,
                    copy.deepcopy(genome),
                    base_cfg,
                    BIN_SIM,
                    float(eval_timeout),
                )
                dt = time.perf_counter() - t0
                return i, f, m, dt

            done = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
                futs = [ex.submit(_thread_eval, i, pop[i]) for i in range(len(pop))]
                for fu in concurrent.futures.as_completed(futs):
                    i, f, m, dt = fu.result()
                    slot[i] = (f, m)
                    gen_wall_times.append(dt)
                    done += 1
                    if show_eval:
                        cm = m.get("completed_missions", "?")
                        rtf = _sim_rtf(sim_s, dt)
                        print(
                            f"  {_pbar(done, len(pop))}  idx={i:2d}  "
                            f"fit={f:8.3f}  wall={dt:5.2f}s  rtf={rtf:5.1f}x  "
                            f"done_missions={cm}  {_genome_line(pop[i])}",
                            flush=True,
                        )
            for i in range(len(pop)):
                pair = slot[i]
                assert pair is not None
                fit.append(pair[0])
                metrics_log.append(pair[1])

        ranked = sorted(range(len(pop)), key=lambda i: fit[i], reverse=True)
        best_i = ranked[0]
        worst_i = ranked[-1]
        bm = metrics_log[best_i]
        ineff = bm.get("route_inefficiency_pct")
        ineff_s = f"{float(ineff):.2f}%" if isinstance(ineff, (int, float)) else "n/a"
        gen_wall = time.perf_counter() - t_gen0
        mean_f = statistics.mean(fit) if fit else 0.0
        try:
            stdev_f = statistics.stdev(fit) if len(fit) > 1 else 0.0
        except statistics.StatisticsError:
            stdev_f = 0.0

        print(
            f"--- Gen {gen + 1} summary ({gen_wall:.1f}s) --- "
            f"best={fit[best_i]:.3f}  worst={fit[worst_i]:.3f}  "
            f"mean={mean_f:.3f}  stdev={stdev_f:.3f}",
            flush=True,
        )
        if gen_wall_times:
            rtfs = [_sim_rtf(sim_s, w) for w in gen_wall_times]
            print(
                f"  RTF (sim/wall per eval): mean={statistics.mean(rtfs):.1f}x  "
                f"min={min(rtfs):.1f}x  max={max(rtfs):.1f}x  "
                f"(sim {sim_s:g}s each; higher RTF = faster run)",
                flush=True,
            )
        print(
            f"  metrics: missions={bm.get('completed_missions')}  "
            f"macproxy={bm.get('macproxy_count')}  ineff={ineff_s}  "
            f"daa_pairs={bm.get('daa_alert_pairs')}",
            flush=True,
        )
        print(f"  best genome: {_genome_line(pop[best_i])}", flush=True)

        if gen == args.generations - 1:
            break

        elite_n = min(args.elite, len(pop))
        new_pop = [copy.deepcopy(pop[ranked[i]]) for i in range(elite_n)]
        while len(new_pop) < args.population:
            p1 = tournament_select(pop, fit, rng)
            p2 = tournament_select(pop, fit, rng)
            c1, c2 = crossover(p1, p2, rng)
            c1 = mutate(c1, rng)
            c2 = mutate(c2, rng)
            new_pop.append(c1)
            if len(new_pop) < args.population:
                new_pop.append(c2)
        pop = new_pop[: args.population]

    best_i = max(range(len(pop)), key=lambda i: fit[i])
    champion = clip_genome(pop[best_i])
    out_dir = os.path.join(REPO_ROOT, "experiments", "daidalus_ga")
    os.makedirs(out_dir, exist_ok=True)
    best_path = os.path.join(out_dir, "best_genome.json")
    with open(best_path, "w") as f:
        json.dump(
            {
                "fitness": fit[best_i],
                "genome": champion,
                "metrics": metrics_log[best_i],
                "scenario": args.scenario,
                "num_drones": args.num_drones,
                "duration_s": args.duration,
                "workers": args.workers,
                "template_dir": args.template_dir,
            },
            f,
            indent=2,
        )
    cfg_fragment = apply_genome_to_config({"simulation": {}}, champion)
    with open(os.path.join(out_dir, "best_sim_config_fragment.json"), "w") as f:
        json.dump(cfg_fragment, f, indent=2)

    print(f"\nChampion genome saved to {best_path}")
    print("Merge `best_sim_config_fragment.json` into your run's `config/sim_config.json`.")


if __name__ == "__main__":
    main()
