# xTM primordial (Rust) — Daidalus vs baseline

- Output: `/home/suporte/Conceptio_Services/Rust_models/experiments/xtm_primordial_rust/results/run_20260322_183259`
- Duration (s): **28800.0**, drones: **50**, seed **42**
- Genome: `/home/suporte/Conceptio_Services/Rust_models/experiments/daidalus_ga/best_genome.json`


| Scen | Python analogue                              | macproxy (no DAID) | macproxy (DAID) | Δ macproxy | ineff % (no)       | ineff % (DAID)     | Δ DAA pairs |
| ---- | -------------------------------------------- | ------------------ | --------------- | ---------- | ------------------ | ------------------ | ----------- |
| 1    | testeprimordial1 — blind baseline            | 29                 | 150             | 121.0      | 0.8031856136552152 | 13.124273285855054 | 770.0       |
| 2    | testeprimordial2 — geometric DAA, no xTM     | 0                  | 87              | 87.0       | 1.7956086961329227 | 8.264704894591507  | 299.0       |
| 3    | testeprimordial3 — xTM tubes, no tactical DA | 2                  | 1924            | 1922.0     | 2.9869222918519713 | 27.72497918288638  | 1418.0      |
| 4a   | testeprimordial4 — xTM + DAA (4A-style)      | 6                  | 1053            | 1047.0     | 2.8532697654276284 | 39.91094543938651  | 1313.0      |
| 4b   | testeprimordial4b — xTM + DAA + wind-style ( | 0                  | 2577            | 2577.0     | 2.9359654607866372 | 45.937563122395815 | 1616.0      |


