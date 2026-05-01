#!/usr/bin/env python3
"""Rebuilds docs/data.json from countries/*.json + config + latest history diff.
Run after every weekly update."""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
COUNTRIES_DIR = ROOT / "countries"
CONFIG_PATH = ROOT / "config" / "countries.json"
HISTORY_DIR = ROOT / "history"
DOCS_DIR = ROOT / "docs"


def main() -> int:
    config = json.loads(CONFIG_PATH.read_text())
    countries = [json.loads(f.read_text()) for f in sorted(COUNTRIES_DIR.glob("*.json"))]
    diffs = sorted(HISTORY_DIR.glob("diff_*.json")) if HISTORY_DIR.exists() else []
    latest_diff = json.loads(diffs[-1].read_text()) if diffs else {"new": [], "updated": []}

    bundle = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "compliance_jobs": config["compliance_jobs"],
        "regions": config["regions"],
        "countries": countries,
        "latest_diff": latest_diff,
    }
    out = DOCS_DIR / "data.json"
    out.write_text(json.dumps(bundle, ensure_ascii=False, separators=(",", ":")))
    print(f"Wrote {out} ({out.stat().st_size:,} bytes, {len(countries)} countries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
