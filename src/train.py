"""Train and compare candidate models, then persist the best pipeline."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split

from src.preprocessing import build_pipeline, split_features_target

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "best_model.joblib"
METRICS_PATH = ROOT / "reports" / "model_comparison.json"
RANDOM_STATE = 42

CANDIDATE_MODELS = {
    "logistic_regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    "random_forest": RandomForestClassifier(n_estimators=300, random_state=RANDOM_STATE),
    "gradient_boosting": GradientBoostingClassifier(random_state=RANDOM_STATE),
}

SCORING = ["accuracy", "precision", "recall", "f1", "roc_auc"]


def train_and_compare(df: pd.DataFrame):
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    results = {}
    fitted_pipelines = {}

    for name, model in CANDIDATE_MODELS.items():
        pipeline = build_pipeline(model)
        cv_scores = cross_validate(pipeline, X_train, y_train, cv=cv, scoring=SCORING)
        results[name] = {metric: float(cv_scores[f"test_{metric}"].mean()) for metric in SCORING}
        pipeline.fit(X_train, y_train)
        fitted_pipelines[name] = pipeline

    best_name = max(results, key=lambda n: results[n]["roc_auc"])
    best_pipeline = fitted_pipelines[best_name]

    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = {
        "cv_results": results,
        "best_model": best_name,
        "test_set_size": len(X_test),
        "train_set_size": len(X_train),
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    return best_name, best_pipeline, results, (X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    data_path = ROOT / "data" / "churn_data.csv"
    df = pd.read_csv(data_path)
    best_name, best_pipeline, results, split = train_and_compare(df)

    print("5-fold CV results (mean):")
    for name, metrics in results.items():
        print(f"  {name}: " + ", ".join(f"{k}={v:.3f}" for k, v in metrics.items()))
    print(f"\nBest model by ROC-AUC: {best_name}")
    print(f"Saved to {MODEL_PATH}")
