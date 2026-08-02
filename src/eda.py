"""Exploratory data analysis: generates and saves figures to reports/figures/."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "reports" / "figures"


def run_eda(df: pd.DataFrame) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Churn class balance
    fig, ax = plt.subplots(figsize=(5, 4))
    df["churn"].value_counts().rename({0: "Stayed", 1: "Churned"}).plot(
        kind="bar", color=["#4C72B0", "#DD8452"], ax=ax
    )
    ax.set_title("Churn Class Balance")
    ax.set_ylabel("Number of Customers")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "class_balance.png", dpi=150)
    plt.close(fig)

    # 2. Correlation heatmap (numeric features)
    numeric_cols = ["tenure_months", "monthly_charges", "total_charges", "num_support_calls", "churn"]
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(df[numeric_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Correlation Heatmap")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "correlation_heatmap.png", dpi=150)
    plt.close(fig)

    # 3. Tenure vs churn
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x="churn", y="tenure_months", hue="churn", palette=["#4C72B0", "#DD8452"], legend=False, ax=ax)
    ax.set_xticks([0, 1], ["Stayed", "Churned"])
    ax.set_title("Tenure vs Churn")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "tenure_vs_churn.png", dpi=150)
    plt.close(fig)

    # 4. Contract type churn rate
    fig, ax = plt.subplots(figsize=(6, 4))
    rate = df.groupby("contract_type")["churn"].mean().sort_values(ascending=False)
    rate.plot(kind="bar", color="#55A868", ax=ax)
    ax.set_title("Churn Rate by Contract Type")
    ax.set_ylabel("Churn Rate")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "churn_rate_by_contract.png", dpi=150)
    plt.close(fig)

    # 5. Monthly charges distribution by churn
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.kdeplot(data=df, x="monthly_charges", hue="churn", fill=True, common_norm=False,
                palette={0: "#4C72B0", 1: "#DD8452"}, ax=ax)
    ax.set_title("Monthly Charges Distribution by Churn")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "monthly_charges_dist.png", dpi=150)
    plt.close(fig)

    print(f"Saved 5 figures to {FIG_DIR}")


if __name__ == "__main__":
    data_path = ROOT / "data" / "churn_data.csv"
    df = pd.read_csv(data_path)
    run_eda(df)
