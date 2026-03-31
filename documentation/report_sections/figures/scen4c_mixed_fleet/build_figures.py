#!/usr/bin/env python3
"""
Build figures for Scenario 4C mixed-fleet (eVTOL/UAM proxy) comparison.

Sources:
  - analysis_summary.json  (sim metrics: completion, inefficiency)
  - generation_metrics.json (xTM ground delay, per scenario cache)

Generates 5 PNGs matching the LaTeX includegraphics references:
  1. fig_scen4c_delay_vs_scen.png          (grouped bar: 4A/4B/4C delay at N=200 & N=500)
  2. fig_scen4c_completion_ratio_vs_scen.png (bar: 4B/4C × arm at N=200)
  3. fig_scen4c_route_inefficiency_vs_scen.png (bar: 4B/4C × arm at N=200)
  4. fig_scen4c_completion_ratio_vs_density.png (lines: N=200→500)
  5. fig_scen4c_route_inefficiency_vs_density.png (lines: N=200→500)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
RESULTS = ROOT / "experiments" / "xtm_primordial_rust" / "results"
RUN_200 = RESULTS / "run_200d_1h"
RUN_500 = RESULTS / "run_500d_1h"
OUT_DIR = Path(__file__).resolve().parent

plt.rcParams.update({
    "figure.figsize": (7.5, 4.5),
    "font.size": 11,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "legend.fontsize": 9,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
})

COLORS_4 = ["#555555", "#1f77b4", "#888888", "#ff7f0e"]
COLORS_DENSITY = ["#333333", "#1f77b4", "#ff7f0e", "#2ca02c"]
MARKERS = ["o", "s", "^", "D"]


def _load_json(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _gen_metrics(run_dir: Path, scen: str, n: int) -> dict:
    """Load generation_metrics.json from the scenario cache."""
    cache = run_dir / "_scenario_cache" / f"scen{scen}_n{n}_s42_ph1.0" / "generation_metrics.json"
    if not cache.is_file():
        raise FileNotFoundError(cache)
    return _load_json(cache)


def _extract_scen_metrics(analysis: dict, scen: str) -> tuple[dict, dict]:
    for comp in analysis.get("comparisons", []):
        if str(comp.get("scenario")) != str(scen):
            continue
        return comp.get("no_daidalus", {}), comp.get("daidalus", {})
    raise KeyError(f"Scenario {scen!r} not found in analysis_summary.json")


def _completion_ratio(m: dict) -> float:
    total = float(m.get("total_scheduled_missions", 1.0))
    done = float(m.get("completed_missions", 0.0))
    return done / total if total > 0 else 0.0


def _save(fig, name):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUT_DIR / name, dpi=150)
    plt.close(fig)


def main() -> int:
    a200 = _load_json(RUN_200 / "analysis_summary.json")
    a500 = _load_json(RUN_500 / "analysis_summary.json")

    # --- delay from generation_metrics ---
    delay = {}
    for scen in ("4a", "4b", "4c"):
        delay[(scen, 200)] = _gen_metrics(RUN_200, scen, 200)["mean_xtm_delay_s"]
        delay[(scen, 500)] = _gen_metrics(RUN_500, scen, 500)["mean_xtm_delay_s"]

    # --- sim metrics ---
    b4b_200, d4b_200 = _extract_scen_metrics(a200, "4b")
    b4c_200, d4c_200 = _extract_scen_metrics(a200, "4c")
    b4b_500, d4b_500 = _extract_scen_metrics(a500, "4b")
    b4c_500, d4c_500 = _extract_scen_metrics(a500, "4c")

    # ===== 1. Delay grouped-bar (4A / 4B / 4C at N=200 and N=500) =====
    scenarios = ["4A", "4B", "4C"]
    n_groups = len(scenarios)
    x = np.arange(n_groups)
    w = 0.32
    d200 = [delay[("4a", 200)], delay[("4b", 200)], delay[("4c", 200)]]
    d500 = [delay[("4a", 500)], delay[("4b", 500)], delay[("4c", 500)]]

    fig, ax = plt.subplots()
    ax.bar(x - w / 2, d200, w, label="N = 200", color="#1f77b4")
    ax.bar(x + w / 2, d500, w, label="N = 500", color="#ff7f0e")
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.set_ylabel("Mean xTM ground delay (s)")
    ax.set_title("Mean xTM authorisation delay by scenario and density")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    for i, (v2, v5) in enumerate(zip(d200, d500)):
        ax.text(i - w / 2, v2 + 3, f"{v2:.1f}", ha="center", fontsize=8)
        ax.text(i + w / 2, v5 + 3, f"{v5:.1f}", ha="center", fontsize=8)
    _save(fig, "fig_scen4c_delay_vs_scen.png")

    # ===== 2. Completion bar at N=200 =====
    labels_4 = ["4B base", "4B +DAA", "4C base", "4C +DAA"]
    comp_200 = [_completion_ratio(m) for m in (b4b_200, d4b_200, b4c_200, d4c_200)]
    fig, ax = plt.subplots()
    ax.bar(range(4), comp_200, color=COLORS_4, tick_label=labels_4)
    ax.set_ylabel("Completion ratio")
    ax.set_title("Completion ratio (N = 200, 1 h)")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _save(fig, "fig_scen4c_completion_ratio_vs_scen.png")

    # ===== 3. Inefficiency bar at N=200 =====
    ineff_200 = [m.get("route_inefficiency_pct", 0.0) for m in (b4b_200, d4b_200, b4c_200, d4c_200)]
    fig, ax = plt.subplots()
    ax.bar(range(4), ineff_200, color=COLORS_4, tick_label=labels_4)
    ax.set_ylabel("Route inefficiency (%)")
    ax.set_title("Route inefficiency (N = 200, 1 h)")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _save(fig, "fig_scen4c_route_inefficiency_vs_scen.png")

    # ===== 4. Completion vs density =====
    x_vals = [200, 500]
    series_comp = [
        ("4B baseline",  [_completion_ratio(b4b_200), _completion_ratio(b4b_500)]),
        ("4B +DAIDALUS", [_completion_ratio(d4b_200), _completion_ratio(d4b_500)]),
        ("4C baseline",  [_completion_ratio(b4c_200), _completion_ratio(b4c_500)]),
        ("4C +DAIDALUS", [_completion_ratio(d4c_200), _completion_ratio(d4c_500)]),
    ]
    fig, ax = plt.subplots()
    for i, (lbl, ys) in enumerate(series_comp):
        ax.plot(x_vals, ys, marker=MARKERS[i], color=COLORS_DENSITY[i], linewidth=2, label=lbl)
    ax.set_xlabel("Physical drones (N)")
    ax.set_ylabel("Completion ratio")
    ax.set_title("Completion ratio vs density (4B / 4C, 1 h)")
    ax.legend(loc="best")
    ax.grid(True, linestyle="--", alpha=0.4)
    _save(fig, "fig_scen4c_completion_ratio_vs_density.png")

    # ===== 5. Inefficiency vs density =====
    series_ineff = [
        ("4B baseline",  [b4b_200.get("route_inefficiency_pct", 0), b4b_500.get("route_inefficiency_pct", 0)]),
        ("4B +DAIDALUS", [d4b_200.get("route_inefficiency_pct", 0), d4b_500.get("route_inefficiency_pct", 0)]),
        ("4C baseline",  [b4c_200.get("route_inefficiency_pct", 0), b4c_500.get("route_inefficiency_pct", 0)]),
        ("4C +DAIDALUS", [d4c_200.get("route_inefficiency_pct", 0), d4c_500.get("route_inefficiency_pct", 0)]),
    ]
    fig, ax = plt.subplots()
    for i, (lbl, ys) in enumerate(series_ineff):
        ax.plot(x_vals, ys, marker=MARKERS[i], color=COLORS_DENSITY[i], linewidth=2, label=lbl)
    ax.set_xlabel("Physical drones (N)")
    ax.set_ylabel("Route inefficiency (%)")
    ax.set_title("Route inefficiency vs density (4B / 4C, 1 h)")
    ax.legend(loc="best")
    ax.grid(True, linestyle="--", alpha=0.4)
    _save(fig, "fig_scen4c_route_inefficiency_vs_density.png")

    print(f"Wrote 5 PNGs to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
