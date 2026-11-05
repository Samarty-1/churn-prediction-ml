"""Standalone figures and sensitivity artifacts from saved predictions."""

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from churn.backtest import write_json
from churn.decision import decide, outcome_profit


def figures(root, phase="development"):
    result = json.loads((root / f"results/{phase}_evaluation.json").read_text())
    development = json.loads((root / "results/development_evaluation.json").read_text())
    champion = development["champion"]
    predictions = pd.read_parquet(root / f"data/predictions/{phase}.parquet")
    out = root / "reports/figures"
    out.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(8, 5))
    for method in predictions.method.unique():
        points = [r for r in result["reliability"] if r["method"] == method]
        ax.plot(
            [r["mean_probability"] for r in points],
            [r["observed_churn"] for r in points],
            marker="o",
            label=method,
        )
    ax.plot([0, 1], [0, 1], "k--", alpha=0.4)
    ax.set(
        xlabel="Predicted 90-day inactivity",
        ylabel="Observed fraction",
        title=f"{phase.title()} reliability",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / f"{phase}_reliability.png", dpi=160)
    plt.close(fig)
    latest = sorted(predictions.cutoff.unique())[-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    curves = {}
    for method, frame in predictions[predictions.cutoff == latest].groupby("method"):
        decision = decide(
            frame.probability,
            frame.customer_value,
            frame.customer_id,
            eligible=frame.policy_eligible,
        )
        curves[method] = {"optimal_n": decision["optimal_n"], "curve": decision["curve"].tolist()}
        ax.plot(np.arange(len(decision["curve"])), decision["curve"], label=method)
        ax.scatter(decision["optimal_n"], decision["predicted_profit"], s=25)
    ax.set(
        xlabel="Customers contacted",
        ylabel="Predicted hypothetical profit (GBP)",
        title=f"{latest}: fixed save-rate and cost assumptions",
    )
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / f"{phase}_profit_curve.png", dpi=160)
    plt.close(fig)
    write_json(root / f"results/{phase}_profit_curves.json", {"cutoff": latest, "methods": curves})
    grid = []
    for rate in (0.02, 0.05, 0.10, 0.20, 0.30):
        for cost in (1, 2, 5, 10, 20):
            for method, all_rows in predictions.groupby("method"):
                expected, observed, contacts = 0.0, 0.0, 0
                for _, frame in all_rows.groupby("cutoff"):
                    decision = decide(
                        frame.probability,
                        frame.customer_value,
                        frame.customer_id,
                        eligible=frame.policy_eligible,
                        save_rate=rate,
                        offer_cost=cost,
                    )
                    expected += decision["predicted_profit"]
                    contacts += decision["optimal_n"]
                    observed += float(
                        outcome_profit(
                            frame.churn,
                            frame.customer_value,
                            decision["contact"],
                            save_rate=rate,
                            offer_cost=cost,
                        ).sum()
                    )
                grid.append(
                    {
                        "save_rate": rate,
                        "offer_cost": cost,
                        "method": method,
                        "predicted_profit": expected,
                        "outcome_profit_proxy": observed,
                        "contacts": contacts,
                    }
                )
    write_json(root / f"results/{phase}_sensitivity.json", grid)
    selected = pd.DataFrame([r for r in grid if r["method"] == champion])
    matrix = selected.pivot(index="save_rate", columns="offer_cost", values="outcome_profit_proxy")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(5), matrix.columns)
    ax.set_yticks(range(5), [f"{r:.0%}" for r in matrix.index])
    ax.set(
        xlabel="Offer cost (GBP)",
        ylabel="Assumed save rate",
        title=f"{champion}: outcome-based profit proxy",
    )
    fig.colorbar(im, ax=ax, label="GBP; pooled campaign replays")
    fig.tight_layout()
    fig.savefig(out / f"{phase}_sensitivity.png", dpi=160)
    plt.close(fig)
    shap_path = root / f"results/shap_{phase}.json"
    if shap_path.exists():
        values = json.loads(shap_path.read_text())["mean_absolute_shap"]
        top = list(values.items())[:12][::-1]
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.barh([k for k, v in top], [v for k, v in top], color="#237a8c")
        ax.set(
            xlabel="Mean absolute SHAP (uncalibrated log odds)",
            title=f"{champion}: global associations",
        )
        fig.tight_layout()
        fig.savefig(out / f"{phase}_shap.png", dpi=160)
        plt.close(fig)
