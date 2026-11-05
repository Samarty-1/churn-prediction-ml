"""Registered estimators and chronological probability calibration."""

import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from churn.baselines import BGNBD, RFM, Recency
from churn.features import FEATURE_COLUMNS

SEED = 20261105
CONFIGS = {
    "logistic": [{"C": c} for c in (0.01, 0.1, 1.0)],
    "lightgbm": [
        {"num_leaves": n, "min_child_samples": m}
        for n, m in ((7, 50), (15, 50), (15, 100), (31, 100))
    ],
    "recency": [{}],
    "rfm": [{}],
    "bgnbd": [{}],
    "constant": [{}],
}
METHODS = tuple(CONFIGS)


def fit_base(method, config, train):
    if method in ("recency", "constant"):
        return Recency().fit(train), []
    if method == "rfm":
        return RFM().fit(train), []
    if method == "bgnbd":
        return BGNBD().fit(train), []
    numeric = [c for c in FEATURE_COLUMNS if c != "country"]
    steps = [
        ("impute", SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True))
    ]
    if method == "logistic":
        steps.append(("scale", StandardScaler()))
    pre = ColumnTransformer(
        [
            ("numeric", Pipeline(steps), numeric),
            ("country", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["country"]),
        ],
        sparse_threshold=0,
    )
    estimator = (
        LogisticRegression(**config, max_iter=2000, random_state=SEED)
        if method == "logistic"
        else LGBMClassifier(
            **config,
            n_estimators=200,
            learning_rate=0.05,
            reg_lambda=1,
            random_state=SEED,
            deterministic=True,
            force_col_wise=True,
            n_jobs=1,
            verbosity=-1,
        )
    )
    pipeline = Pipeline([("pre", pre), ("estimator", estimator)])
    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter("always")
        pipeline.fit(train[list(FEATURE_COLUMNS)], train.churn)
    return pipeline, sorted(set(str(w.message) for w in recorded))


def raw_score(method, model, frame):
    if method == "recency":
        return frame.recency_days.to_numpy(float)
    if method in ("rfm", "bgnbd", "constant"):
        return model.predict(frame)
    return model.predict_proba(frame[list(FEATURE_COLUMNS)])[:, 1]


def fit_calibrator(kind, score, y):
    if kind == "platt":
        return LogisticRegression(C=1e6, max_iter=2000).fit(np.asarray(score).reshape(-1, 1), y)
    return IsotonicRegression(out_of_bounds="clip").fit(score, y)


def calibrated(calibrator, kind, score):
    if kind == "platt":
        return calibrator.predict_proba(np.asarray(score).reshape(-1, 1))[:, 1]
    return calibrator.predict(score)


def eligible_calibration(kind, frame):
    return len(frame) >= (1000 if kind == "isotonic" else 100) and frame.churn.nunique() == 2


def choose_calibration(oof):
    if oof.empty:
        return None, "native", [{"reason": "no forward predictions"}]
    records = []
    for kind in ("platt", "isotonic"):
        actual, predicted = [], []
        for t in sorted(oof.cutoff.unique()):
            earlier = oof[oof.label_end <= t]
            valid = oof[oof.cutoff == t]
            if eligible_calibration(kind, earlier):
                model = fit_calibrator(kind, earlier.score, earlier.churn)
                actual.extend(valid.churn)
                predicted.extend(calibrated(model, kind, valid.score))
        records.append(
            {
                "kind": kind,
                "validation_rows": len(actual),
                "brier": float(brier_score_loss(actual, predicted)) if actual else None,
            }
        )
    usable = [r for r in records if r["brier"] is not None and eligible_calibration(r["kind"], oof)]
    kind = min(usable, key=lambda r: r["brier"])["kind"] if usable else "platt"
    if not eligible_calibration(kind, oof):
        return None, "native", records
    return fit_calibrator(kind, oof.score, oof.churn), kind, records


@dataclass
class Fitted:
    method: str
    config: dict
    model: object
    calibrator: object = None
    calibration: str = "native"
    recency_k: int = 30

    def predict(self, frame):
        score = raw_score(self.method, self.model, frame)
        if self.calibrator is not None:
            return calibrated(self.calibrator, self.calibration, score)
        if self.method == "recency":
            return self.model.predict(frame)
        return score

    def contact_eligible(self, frame):
        return (
            frame.recency_days.to_numpy() > self.recency_k
            if self.method == "recency"
            else np.ones(len(frame), bool)
        )


def empty_oof():
    return pd.DataFrame(
        columns=[
            "score",
            "churn",
            "cutoff",
            "label_end",
            "customer_id",
            "customer_value",
            "recency_days",
        ]
    )
