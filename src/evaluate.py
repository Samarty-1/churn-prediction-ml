"""Evaluate the persisted best model on the held-out test set and save plots."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

from src.preprocessing import CATEGORICAL_FEATURES, split_features_target
from src.train import METRICS_PATH, MODEL_PATH, ROOT, RANDOM_STATE
from sklearn.model_selection import train_test_split

FIG_DIR = ROOT / "reports" / "figures"


def evaluate(df: pd.DataFrame) -> dict:
    pipeline = joblib.load(MODEL_PATH)
    X, y = split_features_target(df)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    report = classification_report(y_test, y_pred, target_names=["Stayed", "Churned"], output_dict=True)
    auc = roc_auc_score(y_test, y_proba)

    # Confusion matrix
    fig, ax = plt.subplots(figsize=(5, 5))
    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm, display_labels=["Stayed", "Churned"]).plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title("Confusion Matrix (Test Set)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "confusion_matrix.png", dpi=150)
    plt.close(fig)

    # ROC curve
    fig, ax = plt.subplots(figsize=(5, 5))
    RocCurveDisplay.from_predictions(y_test, y_proba, ax=ax, name="Logistic Regression")
    ax.plot([0, 1], [0, 1], linestyle="--", color="grey")
    ax.set_title("ROC Curve (Test Set)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "roc_curve.png", dpi=150)
    plt.close(fig)

    # Feature importance (if supported by the model)
    model = pipeline.named_steps["model"]
    if hasattr(model, "feature_importances_"):
        preprocessor = pipeline.named_steps["preprocessor"]
        cat_names = list(preprocessor.named_transformers_["cat"].get_feature_names_out(CATEGORICAL_FEATURES))
        feature_names = (
            preprocessor.transformers_[0][2]
            + preprocessor.transformers_[1][2]
            + cat_names
        )
        importances = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=True)
        fig, ax = plt.subplots(figsize=(7, 6))
        importances.tail(15).plot(kind="barh", color="#55A868", ax=ax)
        ax.set_title(f"Top Feature Importances ({type(model).__name__})")
        fig.tight_layout()
        fig.savefig(FIG_DIR / "feature_importance.png", dpi=150)
        plt.close(fig)

    test_summary = {
        "test_roc_auc": float(auc),
        "classification_report": report,
    }

    if METRICS_PATH.exists():
        with open(METRICS_PATH) as f:
            existing = json.load(f)
    else:
        existing = {}
    existing["test_evaluation"] = test_summary
    with open(METRICS_PATH, "w") as f:
        json.dump(existing, f, indent=2)

    return test_summary


if __name__ == "__main__":
    data_path = ROOT / "data" / "churn_data.csv"
    df = pd.read_csv(data_path)
    summary = evaluate(df)
    print(f"Test ROC-AUC: {summary['test_roc_auc']:.3f}")
    print(json.dumps(summary["classification_report"], indent=2))
