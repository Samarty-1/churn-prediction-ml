import json
from pathlib import Path

from churn.report import render_readme


def test_readme_matches_results_exactly():
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root / "results/cleaning_summary.json").read_text())
    assert (root / "README.md").read_text(encoding="utf-8") == render_readme(report)
