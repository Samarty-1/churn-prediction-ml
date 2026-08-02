"""Synthetic telecom customer-churn dataset.

Real churn datasets (e.g. IBM Telco) require a network download, which isn't
reproducible in every environment. This generator instead simulates a
realistic customer base with a defined (noisy) relationship between customer
attributes and churn, so the dataset behaves like a real one: imbalanced
classes, correlated features, and signal that a model can actually learn.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

RANDOM_SEED = 42

CONTRACT_TYPES = ["Month-to-month", "One year", "Two year"]
INTERNET_SERVICES = ["DSL", "Fiber optic", "No"]
PAYMENT_METHODS = ["Electronic check", "Mailed check", "Bank transfer", "Credit card"]


def generate_churn_data(n_customers: int = 2000, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Generate a synthetic customer-churn dataset with n_customers rows."""
    rng = np.random.default_rng(seed)

    tenure_months = rng.integers(0, 73, size=n_customers)
    senior_citizen = rng.binomial(1, 0.16, size=n_customers)
    partner = rng.binomial(1, 0.48, size=n_customers)
    dependents = rng.binomial(1, 0.30, size=n_customers)

    contract_type = rng.choice(CONTRACT_TYPES, size=n_customers, p=[0.55, 0.24, 0.21])
    internet_service = rng.choice(INTERNET_SERVICES, size=n_customers, p=[0.35, 0.44, 0.21])
    payment_method = rng.choice(PAYMENT_METHODS, size=n_customers, p=[0.34, 0.23, 0.22, 0.21])
    tech_support = rng.binomial(1, 0.29, size=n_customers)
    paperless_billing = rng.binomial(1, 0.59, size=n_customers)

    base_charge = np.where(
        internet_service == "Fiber optic", rng.normal(85, 12, n_customers),
        np.where(internet_service == "DSL", rng.normal(55, 10, n_customers), rng.normal(25, 5, n_customers)),
    )
    monthly_charges = np.clip(base_charge, 18, 120).round(2)
    total_charges = (monthly_charges * tenure_months + rng.normal(0, 50, n_customers)).clip(min=0).round(2)
    num_support_calls = rng.poisson(1.5, size=n_customers)

    # Ground-truth churn probability via a logistic function of the features,
    # so the dataset carries real, learnable signal plus noise.
    contract_risk = np.select(
        [contract_type == "Month-to-month", contract_type == "One year", contract_type == "Two year"],
        [1.1, -0.4, -1.3],
    )
    payment_risk = np.where(payment_method == "Electronic check", 0.5, -0.15)

    logit = (
        -1.1
        + contract_risk
        + payment_risk
        - 0.045 * tenure_months
        + 0.018 * monthly_charges
        + 0.22 * num_support_calls
        - 0.55 * tech_support
        - 0.35 * partner
        - 0.25 * dependents
        + 0.30 * senior_citizen
        + rng.normal(0, 0.6, n_customers)
    )
    churn_prob = 1 / (1 + np.exp(-logit))
    churn = (rng.random(n_customers) < churn_prob).astype(int)

    df = pd.DataFrame({
        "customer_id": [f"CUST-{i:05d}" for i in range(n_customers)],
        "tenure_months": tenure_months,
        "senior_citizen": senior_citizen,
        "partner": partner,
        "dependents": dependents,
        "contract_type": contract_type,
        "internet_service": internet_service,
        "payment_method": payment_method,
        "tech_support": tech_support,
        "paperless_billing": paperless_billing,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "num_support_calls": num_support_calls,
        "churn": churn,
    })
    return df


if __name__ == "__main__":
    from pathlib import Path

    df = generate_churn_data()
    out_path = Path(__file__).resolve().parent.parent / "data" / "churn_data.csv"
    out_path.parent.mkdir(exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    print(f"Churn rate: {df['churn'].mean():.2%}")
