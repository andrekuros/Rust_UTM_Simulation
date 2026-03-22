#!/usr/bin/env python3
"""Summarize simulation_telemetry.ndjson: ownship DAA alerts vs reactive steering.

Each line (after the optional metadata line) should include `has_reactive_target` (newer builds).
Rows with collision_alerts but has_reactive_target false are "alert but no lateral virtual target".

Usage:
  python3 experiments/analyze_telemetry_reactive.py path/to/simulation_telemetry.ndjson
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any


def analyze_telemetry_ndjson(path: str) -> dict[str, Any]:
    """Return counts; empty/missing file returns zeros with missing_file=True."""
    out: dict[str, Any] = {
        "telemetry_rows": 0,
        "rows_with_ownship_alert": 0,
        "alert_with_reactive": 0,
        "alert_without_reactive": 0,
        "fraction_alert_without_reactive": None,
        "by_flight_state": {},
        "missing_file": True,
    }
    if not path or not os.path.isfile(path):
        return out

    out["missing_file"] = False
    n = 0
    n_alerts = 0
    n_ar = 0
    n_anr = 0
    by_state: dict[str, dict[str, int]] = {}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if "metadata" in row:
                continue
            n += 1
            alerts = row.get("collision_alerts") or []
            if not alerts:
                continue
            n_alerts += 1
            hr = bool(row.get("has_reactive_target", False))
            st = row.get("flight_state") or "unknown"
            by_state.setdefault(st, {"alert": 0, "alert_reactive": 0, "alert_no_reactive": 0})
            by_state[st]["alert"] += 1
            if hr:
                n_ar += 1
                by_state[st]["alert_reactive"] += 1
            else:
                n_anr += 1
                by_state[st]["alert_no_reactive"] += 1

    out["telemetry_rows"] = n
    out["rows_with_ownship_alert"] = n_alerts
    out["alert_with_reactive"] = n_ar
    out["alert_without_reactive"] = n_anr
    if n_alerts:
        out["fraction_alert_without_reactive"] = n_anr / n_alerts
    out["by_flight_state"] = by_state
    return out


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path:
        print("Usage: analyze_telemetry_reactive.py <simulation_telemetry.ndjson>", file=sys.stderr)
        return 1

    s = analyze_telemetry_ndjson(path)
    print(f"file: {path}")
    print(f"telemetry_rows: {s['telemetry_rows']}")
    print(f"rows_with_any_ownship_alert: {s['rows_with_ownship_alert']}")
    print(f"  with has_reactive_target=True:  {s['alert_with_reactive']}")
    print(f"  with has_reactive_target=False: {s['alert_without_reactive']}")
    if s["fraction_alert_without_reactive"] is not None:
        print(f"  fraction alert-without-reactive: {s['fraction_alert_without_reactive']:.3f}")
    print("by flight_state (ownship alerts):")
    for st, c in sorted(s["by_flight_state"].items()):
        print(
            f"  {st!r}: alerts={c['alert']}  reactive={c['alert_reactive']}  "
            f"alert_only={c['alert_no_reactive']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
