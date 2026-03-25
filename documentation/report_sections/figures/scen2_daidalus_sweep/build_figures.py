#!/usr/bin/env python3
"""
Regenerate report PNGs from a Scenario 2 Daidalus sweep run directory.

Uses only N <= max_n (default 1000) so incomplete high-N arms are excluded.
Run from repo root:
  python documentation/report_sections/figures/scen2_daidalus_sweep/build_figures.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
DEFAULT_RUN = REPO / "experiments" / "xtm_primordial_rust" / "results" / "scen2_daidalus_sweep" / "run_20260324_210239Z"
OUT_DIR = Path(__file__).resolve().parent

VARIANT_ORDER = [
    "no_daidalus_python2",
    "daidalus_safe_band",
    "daidalus_preferred_horizontal_resolution",
    "daidalus_discrete_action",
]


def _load_json(p: Path) -> dict:
    with p.open(encoding="utf-8") as f:
        return json.load(f)


def _daa_pairs_scalar(v):
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
        "num_drones": res.get("num_drones", ""),
        "wall_seconds": res.get("wall_seconds", ""),
        "realtime_x": res.get("realtime_x", ""),
        "macproxy_count": m.get("macproxy_count", ""),
        "daa_alert_pairs": _daa_pairs_scalar(m.get("daa_alert_pairs")),
        "completion_ratio": ratio,
        "route_inefficiency_pct": m.get("route_inefficiency_pct", ""),
    }


def collect_rows(run_dir: Path) -> list[dict]:
    rows: list[dict] = []
    runs = run_dir / "runs"
    if not runs.is_dir():
        return rows
    for cell in sorted(runs.iterdir()):
        if not cell.is_dir():
            continue
        sj = cell / "sweep_cell.json"
        sm = cell / "sim_metrics.json"
        if sj.exists():
            data = _load_json(sj)
            res = dict(data.get("result", {}))
            if sm.exists():
                res["metrics"] = _load_json(sm)
            rows.append(_row_from_result(res))
        elif sm.exists():
            m = _load_json(sm)
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
                        "num_drones": n,
                        "wall_seconds": "",
                        "realtime_x": "",
                        "metrics": m,
                    }
                )
            )
    rows.sort(key=lambda r: (int(r["num_drones"] or 0), str(r["variant_id"])))
    return rows


def plot_all(rows: list[dict], out_dir: Path, max_n: int) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "figure.figsize": (9.0, 5.5),
            "font.size": 11,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "legend.fontsize": 9,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
        }
    )

    filtered = []
    for r in rows:
        try:
            n = int(r["num_drones"])
        except (TypeError, ValueError):
            continue
        if n <= max_n:
            filtered.append(r)

    by_var: dict[str, list[tuple[int, dict]]] = {}
    for r in filtered:
        vid = str(r.get("variant_id", ""))
        try:
            n = int(r["num_drones"])
        except (TypeError, ValueError):
            continue
        by_var.setdefault(vid, []).append((n, r))
    for vid in by_var:
        by_var[vid].sort(key=lambda x: x[0])

    colors = ["#333333", "#1f77b4", "#ff7f0e", "#2ca02c"]
    markers = ["o", "s", "^", "D"]

    def _series(metric_key: str, ylabel: str, fname: str, ylog: bool = False) -> None:
        plt.figure()
        for i, vid in enumerate(VARIANT_ORDER):
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
        plt.title(f"{ylabel} vs fleet size (scenario 2, 1 h sim, 10 Hz; N <= {max_n})")
        plt.legend(loc="best")
        plt.grid(True, alpha=0.3)
        if ylog:
            plt.yscale("log")
        plt.tight_layout()
        plt.savefig(out_dir / fname, dpi=150)
        plt.close()

    _series("macproxy_count", "MACproxy count (cumulative unique)", "fig_scen2_macproxy_vs_n.png")
    _series(
        "daa_alert_pairs",
        "DAA alert pairs (set size at end; geometric vs DAIDALUS)",
        "fig_scen2_daa_alert_pairs_vs_n.png",
    )
    _series("completion_ratio", "Completion ratio (completed / scheduled)", "fig_scen2_completion_ratio_vs_n.png")
    _series("route_inefficiency_pct", "Route inefficiency (%)", "fig_scen2_route_inefficiency_vs_n.png")
    _series("wall_seconds", "Wall time (s)", "fig_scen2_wall_seconds_vs_n.png", ylog=True)
    _series("realtime_x", "Sim speed (sim_s / wall_s)", "fig_scen2_realtime_x_vs_n.png")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build scen2 sweep figures for LaTeX report")
    ap.add_argument("--run-dir", type=Path, default=DEFAULT_RUN, help="Sweep run directory (contains runs/)")
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR, help="Where to write PNGs")
    ap.add_argument("--max-n", type=int, default=1000, help="Exclude fleet sizes above this N")
    args = ap.parse_args()
    run_dir = args.run_dir.resolve()
    if not (run_dir / "runs").is_dir():
        print(f"Missing runs/ under {run_dir}", file=sys.stderr)
        return 1
    rows = collect_rows(run_dir)
    if not rows:
        print(f"No rows collected from {run_dir}", file=sys.stderr)
        return 1
    args.out_dir.mkdir(parents=True, exist_ok=True)
    plot_all(rows, args.out_dir, args.max_n)
    print(f"Wrote 6 PNGs to {args.out_dir} (N <= {args.max_n}, source {run_dir})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
