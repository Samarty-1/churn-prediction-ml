"""Freeze before unsealing, consume approval once, and report the result unchanged."""

import json

import duckdb
import joblib
import pandas as pd

from churn.backtest import Experiment, predictions_for, write_json
from churn.evaluate import reliability, summarize
from churn.explain import explain_frame
from churn.features import build_features
from churn.holdout import DEVELOPMENT_CUTOFFS, HORIZON, SEALED_CUTOFFS, one_time_session
from churn.ingest import sha256
from churn.labels import build_labels
from churn.models import METHODS
from churn.snapshots import text_digest

FROZEN_CODE = [
    f"src/churn/{name}.py"
    for name in (
        "baselines",
        "models",
        "decision",
        "evaluate",
        "features",
        "labels",
        "holdout",
        "holdout_run",
        "snapshots",
        "backtest",
        "explain",
    )
] + [
    "sql/features/01_snapshot.sql",
    "docs/PREREGISTRATION.md",
    "docs/IMPLEMENTATION_NOTES.md",
    "pyproject.toml",
    "requirements-lock.txt",
    "results/development_evaluation.json",
    "results/placebo_evaluation.json",
    "docs/HOLDOUT_APPROVAL.json",
]


def prepare_freeze(root):
    path = root / "results/freeze.json"
    if path.exists() or (root / "results/holdout_receipt.json").exists():
        raise FileExistsError("Freeze or holdout receipt already exists; no automatic overwrite")
    development = json.loads((root / "results/development_evaluation.json").read_text())
    experiment = Experiment(root)
    experiment.run_name = "final_fit_before_unseal"
    available = tuple(t for t in DEVELOPMENT_CUTOFFS if t + HORIZON <= SEALED_CUTOFFS[0])
    models_dir = root / "models/frozen"
    models_dir.mkdir(parents=True, exist_ok=True)
    fitted_details = {}
    for method in METHODS:
        fitted, train = experiment.selected_fit(method, available, "final_frozen_fit")
        joblib.dump(fitted, models_dir / f"{method}.joblib")
        fitted_details[method] = {
            "config": fitted.config,
            "calibration": fitted.calibration,
            "recency_k": fitted.recency_k,
        }
    train.to_parquet(models_dir / "training.parquet", index=False)
    files = {name: {"kind": "text", "sha256": text_digest(root / name)} for name in FROZEN_CODE}
    binaries = [
        *(f"models/frozen/{m}.joblib" for m in METHODS),
        "models/frozen/training.parquet",
        "data/processed/sales.parquet",
        "data/processed/cancellations.parquet",
    ]
    files.update({name: {"kind": "binary", "sha256": sha256(root / name)} for name in binaries})
    freeze = {
        "champion": development["champion"],
        "holdout_cutoffs": [str(t.date()) for t in SEALED_CUTOFFS],
        "training_cutoffs": [str(t.date()) for t in available],
        "models": fitted_details,
        "files": files,
    }
    write_json(path, freeze)
    return freeze


def verify_freeze(root):
    freeze = json.loads((root / "results/freeze.json").read_text())
    for name, expected in freeze["files"].items():
        actual = text_digest(root / name) if expected["kind"] == "text" else sha256(root / name)
        if actual != expected["sha256"]:
            raise ValueError(f"Frozen artifact changed: {name}")
    return freeze


def evaluate_once(root):
    if (root / "results/holdout_receipt.json").exists():
        raise FileExistsError("Holdout evaluation has already been attempted; no second unsealing")
    freeze = verify_freeze(root)
    parts, explained = [], []
    importance, total = {}, 0
    with one_time_session(root, sha256(root / "results/freeze.json")) as receipt:
        train = pd.read_parquet(root / "models/frozen/training.parquet")
        fitted = {m: joblib.load(root / f"models/frozen/{m}.joblib") for m in METHODS}
        with duckdb.connect() as con:
            for table in ("sales", "cancellations"):
                con.read_parquet(str(root / f"data/processed/{table}.parquet")).create_view(table)
            for cutoff in SEALED_CUTOFFS:
                features = build_features(con, cutoff)
                labels = build_labels(con, cutoff)
                if not features["customer_id"].equals(labels["customer_id"]):
                    raise ValueError("Holdout feature/label populations differ")
                frame = features.to_pandas()
                frame["churn"] = labels["churn"].to_numpy()
                frame["cutoff"] = pd.Timestamp(cutoff)
                for method, model in fitted.items():
                    output = predictions_for(model, frame)
                    parts.append(output)
                    if method == freeze["champion"]:
                        reasons, sums = explain_frame(model, train, frame)
                        output = output.copy()
                        output["reasons"] = reasons
                        output["recency_days"] = frame.recency_days.to_numpy()
                        explained.append(output)
                        for key, value in sums.items():
                            importance[key] = importance.get(key, 0) + value
                        total += len(frame)
                print(f"Evaluated sealed cutoff {cutoff.date()} once", flush=True)
        predictions = pd.concat(parts, ignore_index=True)
        target = root / "data/predictions"
        predictions.to_parquet(target / "holdout.parquet", index=False)
        pd.concat(explained, ignore_index=True).to_parquet(
            target / "holdout_explained.parquet", index=False
        )
        result = summarize(predictions)
        result["reliability"] = reliability(predictions)
        result["champion"] = freeze["champion"]
        pooled = result["groups"]["pooled"]
        comparison = pooled["comparisons"][freeze["champion"]]
        result["success"] = all(
            comparison[b]["ci_familywise95"][0] > 0 for b in ("recency", "rfm", "bgnbd")
        ) and (pooled["methods"][freeze["champion"]]["metrics"]["profit"]["value"] > 0)
        write_json(root / "results/holdout_evaluation.json", result)
        write_json(
            root / "results/shap_holdout.json",
            {
                "model": freeze["champion"],
                "output": "uncalibrated log odds",
                "rows": total,
                "mean_absolute_shap": {
                    k: v / total for k, v in sorted(importance.items(), key=lambda kv: -kv[1])
                },
            },
        )
        receipt["evaluation_sha256"] = sha256(root / "results/holdout_evaluation.json")
        receipt["predictions_sha256"] = sha256(target / "holdout.parquet")
        receipt["explained_sha256"] = sha256(target / "holdout_explained.parquet")
    return result
