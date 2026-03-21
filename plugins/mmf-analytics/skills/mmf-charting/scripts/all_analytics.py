#!/usr/bin/env python3
"""
all_analytics.py — Run the full MMF analytics suite: cross-fund, summary, deep-dives, top issuers.
This is the master script that calls all other chart scripts.

Usage:
    python3 all_analytics.py [--db PATH] [--out DIR] [--days N]

Prints PNG:<path> for every chart saved.
"""

import sys
import subprocess
from pathlib import Path

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
from chart_utils import base_parser, ensure_out

SCRIPTS = [
    "cross_fund_charts.py",
    "summary_charts.py",
    "fund_deep_dive.py",
    "top_issuers.py",
    "heatmap_chart.py",
]


def main():
    p = base_parser("Run the full MMF analytics suite")
    args = p.parse_args()
    ensure_out(args.out)

    scripts_dir = Path(__file__).parent
    total_pngs = 0

    for script in SCRIPTS:
        script_path = str(scripts_dir / script)
        print(f"\n{'='*55}")
        print(f"  Running {script}...")
        print(f"{'='*55}")

        result = subprocess.run(
            [sys.executable, script_path,
             "--db", args.db, "--out", args.out, "--days", str(args.days)],
            capture_output=False,
        )
        if result.returncode != 0:
            print(f"[WARNING] {script} exited with code {result.returncode}", file=sys.stderr)

    print(f"\n{'='*55}")
    print(f"  Full MMF analytics complete — check {args.out}")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
