#!/usr/bin/env python3
"""
Serve the UTM viewer (viewer/index.html) and JSON + telemetry from experiment results.

  cd /path/to/Rust_models && python3 viewer/results_server.py
  Open the printed URL (default port 8765; auto-fallback if that port is blocked on Windows).

API:
  GET /api/runs
      Lists ``simulation_telemetry.ndjson`` files under allowed roots, **grouped by experiment**
      (first directory under ``experiments/``, e.g. ``encounter_battery``, ``xtm_primordial_rust``).
      Response includes ``experiments`` (list of {id, path, run_count, runs}) and ``runs`` (flat,
      newest first) for backward compatibility.

  GET /api/telemetry?path=<repo-relative path to .ndjson>
      Streams the file (only under allowed results roots).

Env:
  VIEWER_PORT   (default 8765; server tries alternate ports if bind fails)
  VIEWER_HOST   (default 127.0.0.1)
  VIEWER_RESULTS_GLOBS  optional colon-separated directories under the repo root to scan.
      If unset, scans **all of** ``experiments/`` (every sub-project with telemetry).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _allowed_roots(repo: Path) -> list[Path]:
    raw = os.environ.get("VIEWER_RESULTS_GLOBS", "").strip()
    if not raw:
        return [repo / "experiments" ]
    roots: list[Path] = []
    for part in raw.split(":"):
        p = (repo / part.strip()).resolve()
        if p.is_dir():
            roots.append(p)
    return roots if roots else [repo / "experiments" ]


def _is_under(path: Path, roots: list[Path]) -> bool:
    rp = path.resolve()
    for r in roots:
        try:
            rp.relative_to(r.resolve())
            return True
        except ValueError:
            continue
    return False


def _experiment_id(rel: Path) -> str:
    """First directory under ``experiments/``, or first path component if not under experiments."""
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "experiments":
        return parts[1]
    return parts[0] if parts else "other"


def _scan_runs(repo: Path, roots: list[Path]) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for base in roots:
        if not base.is_dir():
            continue
        for f in base.rglob("simulation_telemetry.ndjson"):
            try:
                rel = f.relative_to(repo)
            except ValueError:
                continue
            key = str(rel).replace("\\", "/")
            if key in seen:
                continue
            seen.add(key)
            st = f.stat()
            parent = f.parent
            exp_id = _experiment_id(rel)
            label = str(parent.relative_to(base)).replace("\\", "/") if parent != base else parent.name
            out.append(
                {
                    "telemetry_path": key,
                    "experiment": exp_id,
                    "folder": str(parent.relative_to(repo)).replace("\\", "/"),
                    "label": label,
                    "mtime": st.st_mtime,
                    "size_bytes": st.st_size,
                }
            )
    out.sort(key=lambda x: -x["mtime"])
    return out


def _group_by_experiment(repo: Path, runs: list[dict]) -> list[dict]:
    """Stable groups sorted by experiment id; runs within each group by newest first."""
    buckets: dict[str, list[dict]] = {}
    for r in runs:
        eid = r.get("experiment") or "other"
        buckets.setdefault(eid, []).append(r)
    groups: list[dict] = []
    for eid in sorted(buckets.keys()):
        br = buckets[eid]
        br.sort(key=lambda x: -x["mtime"])
        exp_path = str(Path("experiments") / eid).replace("\\", "/")
        groups.append(
            {
                "id": eid,
                "path": exp_path,
                "run_count": len(br),
                "runs": br,
            }
        )
    return groups


class Handler(SimpleHTTPRequestHandler):
    repo = _repo_root()
    viewer_dir = Path(__file__).resolve().parent
    allowed_roots = _allowed_roots(repo)

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), fmt % args))

    def _send_json(self, obj: dict, status: int = 200) -> None:
        data = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _send_file(self, path: Path, content_type: str) -> None:
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        path_only = urllib.parse.unquote(parsed.path)

        if path_only == "/api/runs":
            runs = _scan_runs(self.repo, self.allowed_roots)
            experiments = _group_by_experiment(self.repo, runs)
            self._send_json(
                {
                    "repo_root": str(self.repo),
                    "runs": runs,
                    "experiments": experiments,
                    "experiment_count": len(experiments),
                }
            )
            return

        if path_only == "/api/telemetry":
            qs = urllib.parse.parse_qs(parsed.query)
            rel = (qs.get("path") or [""])[0].strip()
            if not rel or ".." in rel:
                self._send_json({"error": "invalid path"}, 400)
                return
            target = (self.repo / rel).resolve()
            if not _is_under(target, self.allowed_roots):
                self._send_json({"error": "path not under allowed results roots"}, 403)
                return
            if not target.is_file() or target.suffix.lower() not in (".ndjson",):
                self._send_json({"error": "not a telemetry file"}, 404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "application/x-ndjson; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(target, "rb") as f:
                shutil.copyfileobj(f, self.wfile)
            return

        # Static viewer
        if path_only in ("/", "/index.html"):
            self._send_file(self.viewer_dir / "index.html", "text/html; charset=utf-8")
            return

        # Other files from viewer/ (e.g. future assets)
        if path_only.startswith("/"):
            rel_static = path_only.lstrip("/")
            candidate = (self.viewer_dir / rel_static).resolve()
            try:
                candidate.relative_to(self.viewer_dir.resolve())
            except ValueError:
                self.send_error(404)
                return
            if candidate.is_file():
                # minimal types
                ct = "application/octet-stream"
                if candidate.suffix == ".js":
                    ct = "text/javascript; charset=utf-8"
                elif candidate.suffix == ".css":
                    ct = "text/css; charset=utf-8"
                self._send_file(candidate, ct)
                return

        self.send_error(404)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()


def _bind_http_server(host: str, preferred: int) -> tuple[HTTPServer, int, OSError | None]:
    """Bind HTTPServer; try fallbacks if the port is busy or forbidden (common on Windows)."""
    candidates: list[int] = [preferred]
    for p in (8780, 8800, 8888, 9000):
        if p not in candidates:
            candidates.append(p)
    first_err: OSError | None = None
    for p in candidates:
        try:
            httpd = HTTPServer((host, p), Handler)
            err_for_note = first_err if p != preferred else None
            return httpd, p, err_for_note
        except OSError as e:
            if first_err is None:
                first_err = e
            continue
    try:
        httpd = HTTPServer((host, 0), Handler)
        return httpd, httpd.server_address[1], first_err
    except OSError:
        raise first_err from None


def main() -> None:
    host = os.environ.get("VIEWER_HOST", "127.0.0.1")
    port = int(os.environ.get("VIEWER_PORT", "8765"))
    repo = _repo_root()
    Handler.repo = repo
    Handler.allowed_roots = _allowed_roots(repo)
    httpd, bound, bind_err = _bind_http_server(host, port)
    if bound != port and bind_err is not None:
        print(
            f"Note: {host}:{port} unavailable ({bind_err}); using {bound}. "
            "Override with VIEWER_PORT, or inspect reserved ranges: "
            "`netsh interface ipv4 show excludedportrange protocol=tcp`",
            flush=True,
        )
    roots = [str(r.relative_to(repo)) for r in Handler.allowed_roots if r.is_dir()]
    print(f"Repo: {repo}")
    print(f"Scanning: {roots or '(none — create experiments/)'}")
    print(f"Viewer: http://{host}:{bound}/")
    print("API: GET /api/runs (grouped by experiments/)  |  GET /api/telemetry?path=<repo-relative>")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
