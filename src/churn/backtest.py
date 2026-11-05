"""Nested expanding-origin experiment with an append-only trial audit."""

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score

from churn.decision import decide, outcome_profit
from churn.evaluate import reliability, summarize
from churn.holdout import DEVELOPMENT_CUTOFFS, HORIZON, development_origins
from churn.models import (
    CONFIGS,
    METHODS,
    Fitted,
    calibrated,
    choose_calibration,
    empty_oof,
    fit_base,
    raw_score,
)
from churn.snapshots import read_snapshot


def write_json(path, value):
    path.write_text(
        json.dumps(value, indent=2, allow_nan=False, default=str) + "\n", encoding="utf-8"
    )


class Experiment:
    def __init__(self, root: Path, *, placebo=False):
        self.root, self.placebo = root, placebo
        self.frames = {t: read_snapshot(root, t).to_pandas() for t in DEVELOPMENT_CUTOFFS}
        if placebo:
            rng = np.random.default_rng(20261106)
            for frame in self.frames.values():
                frame["churn"] = rng.permutation(frame.churn.to_numpy())
        self.cache = {}
        self.log = root / "results/trials.jsonl"
        self.run_name = "placebo" if placebo else "development"

    def record(self, **entry):
        entry = {"run": self.run_name, **entry}
        with self.log.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(entry, default=str, allow_nan=False) + "\n")

    def fit(self, method, config, train, context):
        try:
            model, warnings = fit_base(method, config, train)
            self.record(
                event="fit",
                method=method,
                config=config,
                context=context,
                train_cutoffs=sorted(str(t) for t in train.cutoff.unique()),
                rows=len(train),
                warnings=warnings,
                status="ok",
                optimizer=getattr(model, "attempts", None),
            )
            return model
        except Exception as error:
            self.record(
                event="fit",
                method=method,
                config=config,
                context=context,
                status="failed",
                error=repr(error),
            )
            raise

    def forward(self, method, config, available):
        parts = []
        for validation in available:
            earlier = tuple(t for t in available if t + HORIZON <= validation)
            if not earlier:
                continue
            key = (method, json.dumps(config, sort_keys=True), validation, earlier)
            if key not in self.cache:
                train = pd.concat([self.frames[t] for t in earlier], ignore_index=True)
                model = self.fit(method, config, train, f"inner:{validation.date()}")
                frame = self.frames[validation]
                part = frame[
                    [
                        "customer_id",
                        "churn",
                        "cutoff",
                        "label_end",
                        "customer_value",
                        "recency_days",
                    ]
                ].copy()
                part["score"] = raw_score(method, model, frame)
                part["native"] = model.predict(frame) if method == "recency" else part.score
                self.cache[key] = part
            parts.append(self.cache[key])
        return pd.concat(parts, ignore_index=True) if parts else empty_oof()

    def selected_fit(self, method, available, context, forced_config=None):
        candidates = []
        for config in [forced_config] if forced_config is not None else CONFIGS[method]:
            oof = self.forward(method, config, available)
            score = float(average_precision_score(oof.churn, oof.score)) if len(oof) else None
            candidates.append((config, oof, score))
            self.record(
                event="candidate",
                method=method,
                config=config,
                context=context,
                inner_average_precision=score,
                validation_rows=len(oof),
            )
        chosen = max(candidates, key=lambda c: c[2] if c[2] is not None else -1)
        config, oof, _ = chosen
        calibrator, kind, calibration_trials = choose_calibration(oof)
        if method == "constant":
            calibrator, kind = None, "native"
        self.record(
            event="calibration",
            method=method,
            context=context,
            selected=kind,
            candidates=calibration_trials,
        )
        k = 30
        if method == "recency" and len(oof):
            # Threshold tuning uses chronological calibration, never future OOF outcomes.
            forward_prob = np.empty(len(oof))
            for t in sorted(oof.cutoff.unique()):
                earlier = oof[oof.label_end <= t]
                valid = oof.cutoff == t
                mapping, name, _ = choose_calibration(earlier)
                forward_prob[valid] = (
                    calibrated(mapping, name, oof.loc[valid, "score"])
                    if mapping is not None
                    else oof.loc[valid, "native"]
                )
            options = []
            for threshold in (30, 60, 90, 120, 180, 270):
                decision = decide(
                    forward_prob,
                    oof.customer_value,
                    oof.customer_id,
                    eligible=oof.recency_days.to_numpy() > threshold,
                )
                profit = float(
                    outcome_profit(oof.churn, oof.customer_value, decision["contact"]).sum()
                )
                options.append((threshold, profit))
                self.record(
                    event="threshold",
                    method=method,
                    context=context,
                    k=threshold,
                    inner_profit=profit,
                )
            k = max(options, key=lambda option: option[1])[0]
        train = pd.concat([self.frames[t] for t in available], ignore_index=True)
        model = self.fit(method, config, train, context)
        fitted = Fitted(method, config, model, calibrator, kind, k)
        return fitted, train


def predictions_for(fitted, frame):
    p = fitted.predict(frame)
    decision = decide(
        p, frame.customer_value, frame.customer_id, eligible=fitted.contact_eligible(frame)
    )
    output = frame[["customer_id", "cutoff", "churn", "customer_value"]].copy()
    output["cutoff"] = output.cutoff.dt.strftime("%Y-%m-%d")
    output["method"] = fitted.method
    output["probability"] = p
    output["contact"] = decision["contact"]
    output["predicted_gain"] = decision["gain"]
    output["profit"] = outcome_profit(frame.churn, frame.customer_value, decision["contact"])
    output["calibration"] = fitted.calibration
    output["policy_eligible"] = fitted.contact_eligible(frame)
    if fitted.method == "bgnbd":
        output["probability_alive"] = fitted.model.probability_alive(frame)
    return output


def run_backtest(root, *, placebo=False, champion=None):
    experiment = Experiment(root, placebo=placebo)
    parts = []
    methods = (champion, "constant") if placebo else METHODS
    for cutoff in development_origins():
        available = tuple(t for t in DEVELOPMENT_CUTOFFS if t + HORIZON <= cutoff)
        for method in methods:
            forced = None
            if placebo and method != "constant":
                original = joblib.load(root / f"models/development/{cutoff.date()}_{method}.joblib")
                forced = original.config
            fitted, _ = experiment.selected_fit(
                method, available, f"outer:{cutoff.date()}", forced_config=forced
            )
            output = predictions_for(fitted, experiment.frames[cutoff])
            parts.append(output)
            model_dir = root / "models" / experiment.run_name
            model_dir.mkdir(parents=True, exist_ok=True)
            joblib.dump(fitted, model_dir / f"{cutoff.date()}_{method}.joblib")
            experiment.record(
                event="outer_result",
                cutoff=str(cutoff.date()),
                method=method,
                average_precision=float(average_precision_score(output.churn, output.probability)),
                profit=float(output.profit.sum()),
                contacts=int(output.contact.sum()),
                config=fitted.config,
                calibration=fitted.calibration,
            )
            print(
                f"{experiment.run_name} {cutoff.date()} {method}: profit {output.profit.sum():.6f}",
                flush=True,
            )
    predictions = pd.concat(parts, ignore_index=True)
    target = root / "data/predictions"
    target.mkdir(parents=True, exist_ok=True)
    predictions.to_parquet(target / f"{experiment.run_name}.parquet", index=False)
    result = summarize(predictions)
    result["reliability"] = reliability(predictions)
    if not placebo:
        pooled = result["groups"]["pooled"]["methods"]
        result["champion"] = max(
            ("logistic", "lightgbm"),
            key=lambda m: (
                pooled[m]["metrics"]["profit"]["value"],
                pooled[m]["metrics"]["pr_auc"]["value"],
                m == "logistic",
            ),
        )
    write_json(root / f"results/{experiment.run_name}_evaluation.json", result)
    return result
