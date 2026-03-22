#!/usr/bin/env python3
"""
Random search over Daidalus tune parameters using the scenario suite objective.

Each **trial** evaluates one genome on all suite scenarios **in parallel** (up to `--workers`).

  python3 experiments/daidalus_ga/run_daidalus_optimization.py \\
    --trials 12 --workers 16 --suite fast --seed 42

Writes `optimization_run_<timestamp>.json` in this directory.

**Checkpoint:** ``--checkpoint path.json`` saves after every trial (RNG state + rows). Resume if the
file exists unless ``--fresh``.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_GA_DIR = os.path.dirname(os.path.abspath(__file__))
if _GA_DIR not in sys.path:
    sys.path.insert(0, _GA_DIR)

from evaluate_genome_suite import (  # noqa: E402
    BIN,
    evaluate_genome_suite_parallel,
)
from objective_and_suites import (  # noqa: E402
    DEFAULT_SEARCH_BOUNDS,
    suite_by_name,
)

RANDOM_CKPT_FORMAT = "daidalus_random_checkpoint_v1"


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


def _load_base_genome(path: str) -> dict:
    with open(path) as f:
        raw = json.load(f)
    return raw["genome"] if isinstance(raw.get("genome"), dict) else raw


def sample_genome(rng: random.Random, base: dict, bounds: dict) -> dict:
    g = {**base}
    for k, (lo, hi) in bounds.items():
        if k == "min_alert_level":
            g[k] = float(int(rng.randint(int(lo), int(hi))))
        else:
            g[k] = lo + rng.random() * (hi - lo)
    return g


def main() -> int:
    ap = argparse.ArgumentParser(description="Parallel random search for Daidalus genome")
    ap.add_argument("--base-genome", default=os.path.join(_GA_DIR, "best_genome.json"))
    ap.add_argument("--trials", type=int, default=8)
    ap.add_argument("--workers", type=int, default=min(16, (os.cpu_count() or 8)))
    ap.add_argument("--suite", default="fast", help="fast | core | full")
    ap.add_argument("--aggregate", default="mean", choices=("mean", "max", "sum"))
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument(
        "--checkpoint",
        default=None,
        metavar="PATH",
        help="Save after each trial; resume if file exists (unless --fresh)",
    )
    ap.add_argument("--fresh", action="store_true", help="Ignore existing checkpoint")
    args = ap.parse_args()

    if not os.path.isfile(BIN):
        print(f"Build release binary first: {BIN}", file=sys.stderr)
        return 1

    base = _load_base_genome(args.base_genome)
    bounds = DEFAULT_SEARCH_BOUNDS

    suite = suite_by_name(args.suite)
    cfg = {k: v for k, v in vars(args).items()}

    ckpt_path = args.checkpoint
    if ckpt_path and os.path.isfile(ckpt_path) and not args.fresh:
        with open(ckpt_path) as f:
            ck = json.load(f)
        if ck.get("format") != RANDOM_CKPT_FORMAT:
            print(f"Checkpoint {ckpt_path!r}: bad format", file=sys.stderr)
            return 1
        if ck.get("suite") != args.suite:
            print(
                f"Checkpoint suite {ck.get('suite')!r} != CLI {args.suite!r}",
                file=sys.stderr,
            )
            return 1
        if int(ck.get("trials_target", -1)) != args.trials:
            print(
                f"Checkpoint trials_target {ck.get('trials_target')} != --trials {args.trials}",
                file=sys.stderr,
            )
            return 1
        rng = random.Random()
        rng.setstate(_detuplify(ck["rng_state"]))  # type: ignore[arg-type]
        out_rows: list[dict] = list(ck.get("rows") or [])
        best_j = float(ck.get("best_J", float("inf")))
        best_genome = ck.get("best_genome")
        start_trial = len(out_rows)
        print(
            f"Resumed from {ckpt_path!r} trials_done={start_trial}/{args.trials}",
            flush=True,
        )
    else:
        rng = random.Random(args.seed)
        out_rows = []
        best_j = float("inf")
        best_genome = None
        start_trial = 0

    print(
        f"trials={args.trials} workers={args.workers} suite={args.suite} "
        f"scenarios={len(suite)} aggregate={args.aggregate} seed={args.seed}",
        flush=True,
    )

    if start_trial >= args.trials:
        print("Checkpoint: all trials already done; writing summary only.", flush=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(_GA_DIR, f"optimization_run_{stamp}.json")
        payload = {
            "created_utc": stamp,
            "trials": args.trials,
            "workers": args.workers,
            "suite": args.suite,
            "aggregate": args.aggregate,
            "seed": args.seed,
            "best_J": best_j,
            "best_genome": best_genome,
            "rows": out_rows,
            "checkpoint": ckpt_path,
        }
        with open(out_path, "w") as f:
            json.dump(payload, f, indent=2)
        print(f"\nWrote {out_path}", flush=True)
        return 0

    for t in range(start_trial, args.trials):
        genome = sample_genome(rng, base, bounds)
        J, ordered = evaluate_genome_suite_parallel(
            genome,
            suite,
            max_workers=args.workers,
            aggregate=args.aggregate,
        )
        row = {
            "trial": t,
            "J": J,
            "genome": genome,
            "per_scenario": [
                {
                    "name": r.get("name"),
                    "j": r.get("j"),
                    "rc": r.get("rc"),
                    "error": r.get("error"),
                    "macproxy_count": (r.get("sm") or {}).get("macproxy_count"),
                    "route_inefficiency_pct": (r.get("sm") or {}).get("route_inefficiency_pct"),
                }
                for r in ordered
            ],
        }
        out_rows.append(row)
        print(f"  trial {t + 1}/{args.trials}  J={J:.6g}", flush=True)
        if J < best_j:
            best_j = J
            best_genome = genome
            print(f"    *** new best J={best_j:.6g}", flush=True)

        if ckpt_path:
            _atomic_write_json(
                ckpt_path,
                {
                    "format": RANDOM_CKPT_FORMAT,
                    "suite": args.suite,
                    "config": cfg,
                    "trials_target": args.trials,
                    "rows": out_rows,
                    "best_J": best_j,
                    "best_genome": best_genome,
                    "rng_state": _tuplify_for_json(rng.getstate()),
                },
            )

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(_GA_DIR, f"optimization_run_{stamp}.json")
    payload = {
        "created_utc": stamp,
        "trials": args.trials,
        "workers": args.workers,
        "suite": args.suite,
        "aggregate": args.aggregate,
        "seed": args.seed,
        "best_J": best_j,
        "best_genome": best_genome,
        "rows": out_rows,
        "checkpoint": ckpt_path,
    }
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nWrote {out_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
