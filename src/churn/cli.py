import argparse
import json
from pathlib import Path

from churn.ingest import ingest
from churn.report import write_readme
from churn.snapshots import build_development
from churn.staging import run_staging


def main():
    parser = argparse.ArgumentParser(description="Retail churn research: phases 1 and 2")
    parser.add_argument("command", choices=["run-all", "stage", "build-development"])
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "sql/staging/01_classify.sql").exists():
        parser.error("Run from the repository root or supply --root")
    if args.command != "build-development":
        parquet = ingest(root) if args.command == "run-all" else root / "data/raw/lines.parquet"
        print(json.dumps(run_staging(root, parquet), indent=2))
    if args.command != "stage":
        print(json.dumps(build_development(root), indent=2))
    write_readme(root)
    print("STOP FOR REVIEW. No models fitted; holdout access remains sealed.")
