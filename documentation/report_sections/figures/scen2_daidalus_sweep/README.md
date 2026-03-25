# Scenario 2 sweep figures (report)

PNG files consumed by `documentation/report_sections/scen2_daidalus_sweep_section.tex`:

- `fig_scen2_macproxy_vs_n.png`
- `fig_scen2_daa_alert_pairs_vs_n.png`
- `fig_scen2_completion_ratio_vs_n.png`
- `fig_scen2_route_inefficiency_vs_n.png`
- `fig_scen2_wall_seconds_vs_n.png`
- `fig_scen2_realtime_x_vs_n.png`

## Regenerate

From the repository root (requires `matplotlib`):

```text
python documentation/report_sections/figures/scen2_daidalus_sweep/build_figures.py
```

Defaults: read `experiments/xtm_primordial_rust/results/scen2_daidalus_sweep/run_20260324_210239Z/runs/`, write PNGs here, **exclude fleet sizes with N > 1000** (`--max-n 1000`) so plots only include the four complete variants.

Optional: `--run-dir <path_to_sweep_run>` if you analyze a different timestamped folder.

Raw sweep aggregates (if present) also live next to that run: `aggregate.csv`, `aggregate.json`, and `figures/*.png` from `run_scen2_daidalus_sweep.py`.
