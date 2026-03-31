#!/usr/bin/env python3
"""
Build figures for Scenario 4C mixed-fleet (eVTOL/UAM proxy) comparison.

Reads two consolidated analysis files:
    experiments/xtm_primordial_rust/results/run_200d_1h/analysis_summary.json
    experiments/xtm_primordial_rust/results/run_500d_1h/analysis_summary.json

and generates:
  1) N=200 bar charts (legacy names kept for LaTeX compatibility)
  2) density trend charts (N=200 vs N=500) for 4B and 4C, baseline and DAIDALUS.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[4]
RUN_200 = (
    ROOT / "experiments" / "xtm_primordial_rust" / "results" / "run_200d_1h" / "analysis_summary.json"
)
RUN_500 = (
    ROOT / "experiments" / "xtm_primordial_rust" / "results" / "run_500d_1h" / "analysis_summary.json"
)
OUT_DIR = Path(__file__).resolve().parent


def _load_analysis(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _extract_scen_metrics(analysis: dict, scen: str) -> tuple[dict, dict]:
    """
    Return (baseline, daidalus) metrics dicts for a given scenario id.
    """
    for comp in analysis.get("comparisons", []):
        if str(comp.get("scenario")) != str(scen):
            continue
        return comp.get("no_daidalus", {}), comp.get("daidalus", {})
    raise KeyError(f"Scenario {scen!r} not found in analysis_summary.json")


def _bar_plot(values, labels, title, ylabel, outfile, ylim=None):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 4))
    x = range(len(values))
    ax.bar(x, values, tick_label=labels)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    if ylim is not None:
        ax.set_ylim(0, ylim)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(OUT_DIR / outfile, dpi=150)
    plt.close(fig)


def _line_plot(x_vals, series, title, ylabel, outfile, log_y=False):
    """
    series: list[(label, list[float])]
    """
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for label, y_vals in series:
        ax.plot(x_vals, y_vals, marker="o", linewidth=2, label=label)
    ax.set_title(title)
    ax.set_xlabel("Physical drones (N)")
    ax.set_ylabel(ylabel)
    if log_y:
        ax.set_yscale("log")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(OUT_DIR / outfile, dpi=150)
    plt.close(fig)


def _completion_ratio(metrics: dict) -> float:
    total = float(metrics.get("total_scheduled_missions", 1.0))
    done = float(metrics.get("completed_missions", 0.0))
    return done / total if total > 0 else 0.0


def main() -> int:
    if not RUN_200.is_file():
        raise SystemExit(f"Missing analysis_summary.json at {RUN_200}")
    if not RUN_500.is_file():
        raise SystemExit(f"Missing analysis_summary.json at {RUN_500}")

    analysis_200 = _load_analysis(RUN_200)
    analysis_500 = _load_analysis(RUN_500)

    # Scenario labels: 4B = homogeneous, 4C = mixed fleet (eVTOL proxy)
    b4b_200, d4b_200 = _extract_scen_metrics(analysis_200, "4b")
    b4c_200, d4c_200 = _extract_scen_metrics(analysis_200, "4c")
    b4b_500, d4b_500 = _extract_scen_metrics(analysis_500, "4b")
    b4c_500, d4c_500 = _extract_scen_metrics(analysis_500, "4c")

    labels = [
        "4B base",
        "4B +DAA",
        "4C base",
        "4C +DAA",
    ]

    # --- N=200 bars (kept for existing LaTeX refs) ---
    mac_vals = [
        b4b_200.get("macproxy_count", 0),
        d4b_200.get("macproxy_count", 0),
        b4c_200.get("macproxy_count", 0),
        d4c_200.get("macproxy_count", 0),
    ]
    _bar_plot(
        mac_vals,
        labels,
        "MACproxy count (N=200, 1h)",
        "MACproxy (unique pairs)",
        "fig_scen4c_macproxy_vs_scen.png",
    )

    # DAA alert pairs
    daa_vals = [
        b4b_200.get("daa_alert_pairs", 0),
        d4b_200.get("daa_alert_pairs", 0),
        b4c_200.get("daa_alert_pairs", 0),
        d4c_200.get("daa_alert_pairs", 0),
    ]
    _bar_plot(
        daa_vals,
        labels,
        "DAA alert pairs (N=200, 1h)",
        "DAA alert pairs",
        "fig_scen4c_daa_alert_pairs_vs_scen.png",
    )

    # Completion ratio (completed / scheduled)
    comp_vals = []
    for m in (b4b_200, d4b_200, b4c_200, d4c_200):
        comp_vals.append(_completion_ratio(m))
    _bar_plot(
        comp_vals,
        labels,
        "Completion ratio (N=200, 1h)",
        "Completion ratio",
        "fig_scen4c_completion_ratio_vs_scen.png",
        ylim=1.0,
    )

    # Route inefficiency (%)
    ineff_vals = [
        b4b_200.get("route_inefficiency_pct", 0.0),
        d4b_200.get("route_inefficiency_pct", 0.0),
        b4c_200.get("route_inefficiency_pct", 0.0),
        d4c_200.get("route_inefficiency_pct", 0.0),
    ]
    _bar_plot(
        ineff_vals,
        labels,
        "Route inefficiency (N=200, 1h)",
        "Route inefficiency [%]",
        "fig_scen4c_route_inefficiency_vs_scen.png",
    )

    # --- Density trends (N=200 and N=500) ---
    x_vals = [200, 500]

    _line_plot(
        x_vals,
        [
            ("4B baseline", [b4b_200.get("macproxy_count", 0), b4b_500.get("macproxy_count", 0)]),
            ("4B +DAIDALUS", [d4b_200.get("macproxy_count", 0), d4b_500.get("macproxy_count", 0)]),
            ("4C baseline", [b4c_200.get("macproxy_count", 0), b4c_500.get("macproxy_count", 0)]),
            ("4C +DAIDALUS", [d4c_200.get("macproxy_count", 0), d4c_500.get("macproxy_count", 0)]),
        ],
        "MACproxy vs density (4B/4C, 1h)",
        "MACproxy (unique pairs)",
        "fig_scen4c_macproxy_vs_density.png",
        log_y=True,
    )

    _line_plot(
        x_vals,
        [
            ("4B baseline", [b4b_200.get("daa_alert_pairs", 0), b4b_500.get("daa_alert_pairs", 0)]),
            ("4B +DAIDALUS", [d4b_200.get("daa_alert_pairs", 0), d4b_500.get("daa_alert_pairs", 0)]),
            ("4C baseline", [b4c_200.get("daa_alert_pairs", 0), b4c_500.get("daa_alert_pairs", 0)]),
            ("4C +DAIDALUS", [d4c_200.get("daa_alert_pairs", 0), d4c_500.get("daa_alert_pairs", 0)]),
        ],
        "DAA alert pairs vs density (4B/4C, 1h)",
        "DAA alert pairs",
        "fig_scen4c_daa_alert_pairs_vs_density.png",
        log_y=True,
    )

    _line_plot(
        x_vals,
        [
            ("4B baseline", [_completion_ratio(b4b_200), _completion_ratio(b4b_500)]),
            ("4B +DAIDALUS", [_completion_ratio(d4b_200), _completion_ratio(d4b_500)]),
            ("4C baseline", [_completion_ratio(b4c_200), _completion_ratio(b4c_500)]),
            ("4C +DAIDALUS", [_completion_ratio(d4c_200), _completion_ratio(d4c_500)]),
        ],
        "Completion ratio vs density (4B/4C, 1h)",
        "Completion ratio",
        "fig_scen4c_completion_ratio_vs_density.png",
    )

    _line_plot(
        x_vals,
        [
            ("4B baseline", [b4b_200.get("route_inefficiency_pct", 0), b4b_500.get("route_inefficiency_pct", 0)]),
            ("4B +DAIDALUS", [d4b_200.get("route_inefficiency_pct", 0), d4b_500.get("route_inefficiency_pct", 0)]),
            ("4C baseline", [b4c_200.get("route_inefficiency_pct", 0), b4c_500.get("route_inefficiency_pct", 0)]),
            ("4C +DAIDALUS", [d4c_200.get("route_inefficiency_pct", 0), d4c_500.get("route_inefficiency_pct", 0)]),
        ],
        "Route inefficiency vs density (4B/4C, 1h)",
        "Route inefficiency [%]",
        "fig_scen4c_route_inefficiency_vs_density.png",
    )

    print(f"Figures written under {OUT_DIR} (N=200 bars + density trends)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

