import argparse
import json
from pathlib import Path

from churn.ingest import ingest
from churn.report import write_readme
from churn.staging import run_staging


def main():
    parser = argparse.ArgumentParser(description="Retail churn research: Phase 1 only")
    parser.add_argument("command", choices=["run-all", "stage"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "sql/staging/01_classify.sql").exists():
        parser.error("Run from the repository root or supply --root")
    parquet = ingest(root) if args.command == "run-all" else root / "data/raw/lines.parquet"
    print(json.dumps(run_staging(root, parquet), indent=2))
    write_readme(root)
    print("PHASE 1 COMPLETE. Stop for review; no labels, models or holdout evaluation executed.")
