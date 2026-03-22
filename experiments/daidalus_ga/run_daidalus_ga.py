#!/usr/bin/env python3
"""
Genetic algorithm for Daidalus `daidalus_tune` parameters.

**Optimized parameters** — see `objective_and_suites.GENOME_KEYS` and module docstring:
evasion offset/duration, heading_blend, track_mix, cpp_* gates, daa_interval_s,
min_alert_level, max_cross_track_m, final_approach_no_reactive_radius_m.

Default suite is **`fast`** (encounter scenarios only, no large `sjc_scenario_gen` run).

Parallelism:
  - `--pop-parallel` processes evaluate **different individuals** at once (each runs the full suite).
  - `--scenario-workers` parallelizes **scenarios within one process** only when `--pop-parallel` is 1.
  - When `--pop-parallel` > 1, scenarios run **sequentially** inside each worker (avoids nested process pools).

  Example (16 cores): `--pop-parallel 4` → up to 4 simulator processes; pair with `--pop-parallel 1 --scenario-workers 16` if you prefer one genome at a time with parallel scenarios.

  python3 experiments/daidalus_ga/run_daidalus_ga.py \\
    --generations 12 --population 16 --suite fast --seed 42 \\
    --pop-parallel 3 --scenario-workers 5

**Checkpoints:** pass ``--checkpoint path.json`` to atomically save after each generation
(``next_gen``, population, RNG state, history, best). If the file already exists, the run
resumes unless you pass ``--fresh``. On completion, ``ga_run_<timestamp>.json`` is still written.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import random
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_GA_DIR = os.path.dirname(os.path.abspath(__file__))
if _GA_DIR not in sys.path:
    sys.path.insert(0, _GA_DIR)

from evaluate_genome_suite import (  # noqa: E402
    BIN,
    evaluate_genome_suite_parallel,
    evaluate_genome_suite_sequential,
)
from objective_and_suites import (  # noqa: E402
    DEFAULT_SEARCH_BOUNDS,
    GENOME_KEYS,
    suite_by_name,
)

CHECKPOINT_FORMAT = "daidalus_ga_checkpoint_v1"


def _tuplify_for_json(obj: object) -> object:
    if isinstance(obj, tuple):
        return {"__tuple__": [_tuplify_for_json(x) for x in obj]}
    if isinstance(obj, list):
        return [_tuplify_for_json(x) for x in obj]
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    raise TypeError(f"checkpoint JSON cannot encode {type(obj)!r}")


def _detuplify(obj: object) -> object:
    if isinstance(obj, dict) and "__tuple__" in obj:
        return tuple(_detuplify(x) for x in obj["__tuple__"])
    if isinstance(obj, list):
        return [_detuplify(x) for x in obj]
    return obj


def _atomic_write_json(path: str, payload: dict) -> None:
    d = os.path.dirname(os.path.abspath(path))
    if d:
        os.makedirs(d, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(payload, f, indent=2)
    os.replace(tmp, path)


def _save_ga_checkpoint(
    path: str,
    *,
    next_gen: int,
    population: list[dict],
    rng: random.Random,
    history: list[dict],
    best_j: float,
    best_genome: dict | None,
    config: dict,
    suite_name: str,
) -> None:
    _atomic_write_json(
        path,
        {
            "format": CHECKPOINT_FORMAT,
            "suite": suite_name,
            "config": config,
            "next_gen": next_gen,
            "population": population,
            "history": history,
            "best_J": best_j,
            "best_genome": best_genome,
            "rng_state": _tuplify_for_json(rng.getstate()),
        },
    )


def _load_ga_checkpoint(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _load_base_genome(path: str) -> dict:
    with open(path) as f:
        raw = json.load(f)
    return raw["genome"] if isinstance(raw.get("genome"), dict) else raw


def random_genome(rng: random.Random, base: dict) -> dict:
    g = dict(base)
    for k in GENOME_KEYS:
        lo, hi = DEFAULT_SEARCH_BOUNDS[k]
        if k == "min_alert_level":
            g[k] = float(rng.randint(int(lo), int(hi)))
        else:
            g[k] = lo + rng.random() * (hi - lo)
    return g


def crossover(rng: random.Random, a: dict, b: dict) -> dict:
    c = {}
    for k in GENOME_KEYS:
        if k == "min_alert_level":
            c[k] = float(rng.choice([int(a[k]), int(b[k])]))
        else:
            if rng.random() < 0.5:
                c[k] = a[k]
            else:
                c[k] = b[k]
            if rng.random() < 0.3:
                c[k] = (a[k] + b[k]) * 0.5
    return c


def mutate(rng: random.Random, g: dict, sigma: float) -> dict:
    out = dict(g)
    for k in GENOME_KEYS:
        if rng.random() > 0.25:
            continue
        lo, hi = DEFAULT_SEARCH_BOUNDS[k]
        span = hi - lo
        if k == "min_alert_level":
            out[k] = float(max(int(lo), min(int(hi), int(round(out[k] + rng.randint(-1, 1))))))
        else:
            out[k] = out[k] + rng.gauss(0.0, sigma * span)
            out[k] = max(lo, min(hi, out[k]))
    return out


def tournament_select(rng: random.Random, pop: list[dict], fitness: list[float], k: int) -> dict:
    idxs = rng.sample(range(len(pop)), k=min(k, len(pop)))
    best_i = min(idxs, key=lambda i: fitness[i])
    return copy.deepcopy(pop[best_i])


def _fitness_payload(payload: dict) -> tuple[int, float]:
    """Worker: returns (index, J). Always sequential scenarios — no nested process pools."""
    i = int(payload["index"])
    genome = payload["genome"]
    suite = payload["suite"]
    agg = payload["aggregate"]
    J, _ = evaluate_genome_suite_sequential(genome, suite, aggregate=agg)
    return i, J


def evaluate_population(
    population: list[dict],
    suite: list,
    *,
    pop_parallel: int,
    scenario_workers: int,
    aggregate: str,
) -> list[float]:
    """Return fitness list (lower better).

    If ``pop_parallel > 1``, individuals are evaluated in parallel with **sequential** scenarios
    only (nested ProcessPoolExecutor + scenario-parallel would oversubscribe CPUs).

    If ``pop_parallel == 1`` and ``scenario_workers > 1``, scenarios run in parallel inside one process.
    """
    if pop_parallel <= 1:
        out: list[float] = []
        for g in population:
            if scenario_workers > 1:
                J, _ = evaluate_genome_suite_parallel(
                    g, suite, max_workers=scenario_workers, aggregate=aggregate
                )
            else:
                J, _ = evaluate_genome_suite_sequential(g, suite, aggregate=aggregate)
            out.append(J)
        return out

    payloads = [
        {
            "index": i,
            "genome": g,
            "suite": suite,
            "aggregate": aggregate,
        }
        for i, g in enumerate(population)
    ]
    workers = max(1, min(pop_parallel, len(population)))
    results: list[float | None] = [None] * len(population)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(_fitness_payload, p): p["index"] for p in payloads}
        for fut in as_completed(futs):
            i, J = fut.result()
            results[i] = J
    return [x if x is not None else float("inf") for x in results]


def main() -> int:
    ap = argparse.ArgumentParser(description="GA for Daidalus tune parameters")
    ap.add_argument("--base-genome", default=os.path.join(_GA_DIR, "best_genome.json"))
    ap.add_argument("--population", type=int, default=16)
    ap.add_argument("--generations", type=int, default=12)
    ap.add_argument("--mutation-sigma", type=float, default=0.12, help="Gaussian mut. vs bound width")
    ap.add_argument("--tournament", type=int, default=3)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--suite", default="fast", help="fast | core | full")
    ap.add_argument("--aggregate", default="mean", choices=("mean", "max", "sum"))
    ap.add_argument(
        "--pop-parallel",
        type=int,
        default=3,
        help="Evaluate this many individuals at once (separate processes)",
    )
    ap.add_argument(
        "--scenario-workers",
        type=int,
        default=5,
        help="Parallel scenarios per individual when --pop-parallel is 1; ignored when pop-parallel>1",
    )
    ap.add_argument(
        "--checkpoint",
        default=None,
        metavar="PATH",
        help="Save after each generation; resume if file exists (use --fresh to restart)",
    )
    ap.add_argument(
        "--fresh",
        action="store_true",
        help="Ignore existing checkpoint file and overwrite it on first save",
    )
    args = ap.parse_args()

    if not os.path.isfile(BIN):
        print(f"Build release binary first: {BIN}", file=sys.stderr)
        return 1

    base = _load_base_genome(args.base_genome)
    suite = suite_by_name(args.suite)
    sw = max(1, min(args.scenario_workers, len(suite)))
    cfg = {k: v for k, v in vars(args).items()}

    ckpt_path = args.checkpoint
    resumed = False
    if ckpt_path and os.path.isfile(ckpt_path) and not args.fresh:
        ck = _load_ga_checkpoint(ckpt_path)
        if ck.get("format") != CHECKPOINT_FORMAT:
            print(f"Checkpoint {ckpt_path!r}: bad format", file=sys.stderr)
            return 1
        if ck.get("suite") != args.suite:
            print(
                f"Checkpoint suite {ck.get('suite')!r} != CLI {args.suite!r} "
                f"(use matching --suite or --fresh)",
                file=sys.stderr,
            )
            return 1
        if len(ck.get("population") or []) != args.population:
            print(
                f"Checkpoint population size != --population {args.population} (use --fresh)",
                file=sys.stderr,
            )
            return 1
        rng = random.Random()
        rng.setstate(_detuplify(ck["rng_state"]))  # type: ignore[arg-type]
        next_gen = int(ck["next_gen"])
        population = ck["population"]
        history = list(ck.get("history") or [])
        best_j = float(ck.get("best_J", float("inf")))
        best_ever = ck.get("best_genome")
        if isinstance(best_ever, dict):
            best_ever = copy.deepcopy(best_ever)
        else:
            best_ever = None
        resumed = True
        print(f"Resumed from checkpoint {ckpt_path!r} next_gen={next_gen}/{args.generations}", flush=True)
    else:
        rng = random.Random(args.seed)
        next_gen = 0
        population = [random_genome(rng, base) for _ in range(args.population)]
        best_ever = None
        best_j = float("inf")
        history = []

    if next_gen >= args.generations:
        print("Checkpoint reports all generations done; writing final summary only.", flush=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(_GA_DIR, f"ga_run_{stamp}.json")
        out = {
            "created_utc": stamp,
            "best_J": best_j,
            "best_genome": best_ever,
            "config": cfg,
            "history": history,
            "resumed_from_checkpoint": ckpt_path,
        }
        with open(out_path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nWrote {out_path}", flush=True)
        return 0

    print(
        f"GA pop={args.population} gen={args.generations} suite={args.suite} "
        f"n_scen={len(suite)} pop_parallel={args.pop_parallel} scenario_workers={sw}"
        f"{' (resumed)' if resumed else ''}",
        flush=True,
    )

    for gen in range(next_gen, args.generations):
        fit = evaluate_population(
            population,
            suite,
            pop_parallel=args.pop_parallel,
            scenario_workers=sw,
            aggregate=args.aggregate,
        )
        gen_best_i = min(range(len(fit)), key=lambda i: fit[i])
        gen_best_j = fit[gen_best_i]
        if gen_best_j < best_j:
            best_j = gen_best_j
            best_ever = copy.deepcopy(population[gen_best_i])
            print(f"  gen {gen + 1}/{args.generations}  best J={best_j:.6g}  (overall best)", flush=True)
        else:
            print(
                f"  gen {gen + 1}/{args.generations}  best J={gen_best_j:.6g}  overall={best_j:.6g}",
                flush=True,
            )
        history.append(
            {
                "generation": gen,
                "best_J": gen_best_j,
                "mean_J": sum(fit) / len(fit) if fit else None,
            }
        )

        if gen == args.generations - 1:
            if ckpt_path:
                _save_ga_checkpoint(
                    ckpt_path,
                    next_gen=args.generations,
                    population=population,
                    rng=rng,
                    history=history,
                    best_j=best_j,
                    best_genome=best_ever,
                    config=cfg,
                    suite_name=args.suite,
                )
            break

        sorted_idx = sorted(range(len(fit)), key=lambda i: fit[i])
        elite = copy.deepcopy(population[sorted_idx[0]])
        next_pop: list[dict] = [elite]
        while len(next_pop) < args.population:
            p1 = tournament_select(rng, population, fit, args.tournament)
            p2 = tournament_select(rng, population, fit, args.tournament)
            child = crossover(rng, p1, p2)
            child = mutate(rng, child, args.mutation_sigma)
            next_pop.append(child)
        population = next_pop

        if ckpt_path:
            _save_ga_checkpoint(
                ckpt_path,
                next_gen=gen + 1,
                population=population,
                rng=rng,
                history=history,
                best_j=best_j,
                best_genome=best_ever,
                config=cfg,
                suite_name=args.suite,
            )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(_GA_DIR, f"ga_run_{stamp}.json")
    out = {
        "created_utc": stamp,
        "best_J": best_j,
        "best_genome": best_ever,
        "config": cfg,
        "history": history,
        "checkpoint": ckpt_path,
    }
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
