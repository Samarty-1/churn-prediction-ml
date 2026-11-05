import json
from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest


def test_app_sliders_change_optimal_contacts_without_training(tmp_path, monkeypatch):
    (tmp_path / "results").mkdir()
    (tmp_path / "data/predictions").mkdir(parents=True)
    (tmp_path / "results/development_evaluation.json").write_text(
        json.dumps({"champion": "lightgbm"})
    )
    pd.DataFrame(
        {
            "customer_id": ["A", "B"],
            "cutoff": ["2011-06-09"] * 2,
            "probability": [0.9, 0.2],
            "customer_value": [100, 100],
            "policy_eligible": [True, True],
            "reasons": ["recency (+1)", "recency (-1)"],
        }
    ).to_parquet(tmp_path / "data/predictions/development_explained.parquet")
    monkeypatch.setenv("CHURN_APP_ROOT", str(tmp_path))
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app/streamlit_app.py"))
    app.run(timeout=30)
    assert not app.exception
    assert app.metric[0].value == "1"
    app.slider[0].set_value(0.0).run()
    assert not app.exception
    assert app.metric[0].value == "0"
    assert app.selectbox[0].options == ["development"]
