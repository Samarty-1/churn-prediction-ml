import json
from pathlib import Path

from churn.publish_report import render_results
from churn.report import render_readme

ROOT = Path(__file__).resolve().parents[1]


def test_readme_matches_results_exactly():
    """The committed README must be exactly what the generator produces from results."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if (ROOT / "results/development_evaluation.json").exists():
        expected, card = render_results(ROOT)
        assert (ROOT / "docs/MODEL_CARD.md").read_text(encoding="utf-8") == card
    else:
        report = json.loads((ROOT / "results/cleaning_summary.json").read_text())
        development = json.loads((ROOT / "results/development_summary.json").read_text())
        expected = render_readme(report, development)
    assert readme == expected
