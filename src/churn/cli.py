"""Command-line entry point: `python -m churn <command>`.

- run-all: download, stage and build development snapshots; run the development
  backtest only if its results are missing; regenerate reports. Never opens the holdout.
- stage / build-development: rerun cleaning SQL or development snapshots only.
- backtest: rerun the development backtest, placebo, explanations and figures.
- report: regenerate README, model card and trial ledger from saved results.
- holdout: freeze, then open the sealed holdout once (needs recorded approval).
"""

import argparse
import json
from pathlib import Path

COMMANDS = ["run-all", "stage", "build-development", "backtest", "report", "holdout"]


def publish(root: Path):
    """Write the public README, model card and ledger from whatever results exist."""
    if (root / "results/development_evaluation.json").exists():
        from churn.publish_report import write_ledger, write_public_report

        write_public_report(root)
        write_ledger(root)
    else:
        from churn.report import write_readme

        write_readme(root)


def development_backtest(root: Path):
    from churn.backtest import run_backtest
    from churn.explain import explain_development
    from churn.plots import figures

    result = run_backtest(root)
    run_backtest(root, placebo=True, champion=result["champion"])
    explain_development(root)
    figures(root, "development")


def holdout(root: Path):
    from churn.holdout_run import evaluate_once, prepare_freeze
    from churn.plots import figures

    if not (root / "results/freeze.json").exists():
        prepare_freeze(root)
    result = evaluate_once(root)
    figures(root, "holdout")
    return result


def main():
    parser = argparse.ArgumentParser(description="Retail churn research pipeline")
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "sql/staging/01_classify.sql").exists():
        parser.error("Run from the repository root or supply --root")

    if args.command in ("run-all", "stage", "build-development"):
        from churn.ingest import ingest
        from churn.snapshots import build_development
        from churn.staging import run_staging

        if args.command != "build-development":
            parquet = ingest(root) if args.command == "run-all" else root / "data/raw/lines.parquet"
            print(json.dumps(run_staging(root, parquet), indent=2))
        if args.command != "stage":
            print(json.dumps(build_development(root), indent=2))

    evaluated = (root / "results/development_evaluation.json").exists()
    if args.command == "backtest" or (args.command == "run-all" and not evaluated):
        development_backtest(root)
    if args.command == "holdout":
        result = holdout(root)
        print(f"Holdout evaluated once. Preregistered success: {result['success']}")

    publish(root)
    print("Reports regenerated from saved results. The holdout is never opened by run-all.")
