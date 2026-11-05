"""Training-background SHAP for the selected ML model's uncalibrated log odds."""

import json

import joblib
import numpy as np
import pandas as pd
import shap

from churn.backtest import write_json
from churn.features import FEATURE_COLUMNS
from churn.holdout import DEVELOPMENT_CUTOFFS, HORIZON
from churn.models import SEED
from churn.snapshots import read_snapshot


def explain_frame(fitted, train, frame):
    pipeline = fitted.model
    pre, estimator = pipeline.named_steps["pre"], pipeline.named_steps["estimator"]
    values = pre.transform(frame[list(FEATURE_COLUMNS)])
    names = pre.get_feature_names_out()
    if fitted.method == "logistic":
        rng = np.random.default_rng(SEED)
        selected = rng.choice(len(train), size=min(100, len(train)), replace=False)
        background = pre.transform(train.iloc[selected][list(FEATURE_COLUMNS)])
        explainer = shap.LinearExplainer(estimator, background)
    else:
        # Path-dependent TreeSHAP uses leaf counts from training, never test backgrounds.
        explainer = shap.TreeExplainer(
            estimator, feature_perturbation="tree_path_dependent", model_output="raw"
        )
    explanation = explainer(values)
    contributions = np.asarray(explanation.values)
    if contributions.ndim != 2:
        raise ValueError("Unexpected SHAP output shape")
    raw = (
        pipeline.decision_function(frame[list(FEATURE_COLUMNS)])
        if fitted.method == "logistic"
        else estimator.booster_.predict(values, raw_score=True)
    )
    if not np.allclose(explanation.base_values + contributions.sum(axis=1), raw, atol=1e-5):
        raise ValueError("SHAP additivity check failed")
    names = [name.replace("numeric__", "").replace("country__", "") for name in names]
    reasons = []
    for row in contributions:
        top = np.argsort(-np.abs(row), kind="stable")[:3]
        reasons.append("; ".join(f"{names[j]} ({row[j]:+.3f} log-odds)" for j in top))
    return reasons, dict(zip(names, np.abs(contributions).sum(axis=0).tolist(), strict=True))


def explain_development(root):
    summary = json.loads((root / "results/development_evaluation.json").read_text())
    champion = summary["champion"]
    predictions = pd.read_parquet(root / "data/predictions/development.parquet")
    selected = predictions[predictions.method == champion].copy()
    global_sum, total = {}, 0
    outputs = []
    for cutoff, group in selected.groupby("cutoff", sort=True):
        t = pd.Timestamp(cutoff).to_pydatetime()
        frame = read_snapshot(root, t).to_pandas()
        train = pd.concat(
            [read_snapshot(root, c).to_pandas() for c in DEVELOPMENT_CUTOFFS if c + HORIZON <= t],
            ignore_index=True,
        )
        fitted = joblib.load(root / f"models/development/{cutoff}_{champion}.joblib")
        reasons, importance = explain_frame(fitted, train, frame)
        explanations = pd.DataFrame(
            {
                "customer_id": frame.customer_id,
                "reasons": reasons,
                "recency_days": frame.recency_days,
            }
        )
        outputs.append(group.merge(explanations, on="customer_id", validate="one_to_one"))
        for name, value in importance.items():
            global_sum[name] = global_sum.get(name, 0) + value
        total += len(frame)
    pd.concat(outputs, ignore_index=True).to_parquet(
        root / "data/predictions/development_explained.parquet", index=False
    )
    write_json(
        root / "results/shap_development.json",
        {
            "model": champion,
            "output": "uncalibrated log odds",
            "rows": total,
            "mean_absolute_shap": {
                k: v / total for k, v in sorted(global_sum.items(), key=lambda kv: -kv[1])
            },
        },
    )
