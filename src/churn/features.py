"""Cutoff-local predictors. No fitted transforms and no outcome access."""

from pathlib import Path

from churn.holdout import require_development

FEATURE_COLUMNS = (
    "recency_days",
    "frequency_365",
    "monetary_365",
    "purchase_days_365",
    "basket_units_mean",
    "basket_lines_mean",
    "product_breadth",
    "category_breadth_proxy",
    "sales_90",
    "sales_prior_90",
    "frequency_90",
    "frequency_prior_90",
    "gap_mean_days",
    "gap_std_days",
    "overdue_ratio",
    "sales_trend_difference",
    "sales_trend_ratio",
    "frequency_trend_difference",
    "frequency_trend_ratio",
    "cancellation_invoices_365",
    "cancellation_amount_365",
    "cancellation_amount_90",
    "cancellation_rate",
    "cancellation_amount_ratio",
    "tenure_days",
    "country",
    "days_to_christmas",
    "acquisition_left_censored",
    "bg_repeat_days",
    "bg_recency_days",
    "bg_age_days",
    "customer_value",
)
SQL = Path(__file__).resolve().parents[2] / "sql/features/01_snapshot.sql"


def build_features(connection, cutoff):
    cutoff = require_development(cutoff)  # Must precede all data access.
    connection.execute(
        "CREATE OR REPLACE TEMP TABLE snapshot_clock AS SELECT ?::TIMESTAMP cutoff", [cutoff]
    )
    connection.execute(
        "CREATE OR REPLACE TEMP TABLE sale_history AS SELECT * FROM sales WHERE invoice_date <= ?",
        [cutoff],
    )
    connection.execute(
        "CREATE OR REPLACE TEMP TABLE cancellation_history AS "
        "SELECT * FROM cancellations WHERE invoice_date <= ?",
        [cutoff],
    )
    table = connection.execute(SQL.read_text()).fetch_arrow_table()
    if set(table.column_names) != {"customer_id", *FEATURE_COLUMNS}:
        raise ValueError("Feature schema differs from the preregistered allowlist")
    return table.select(["customer_id", *FEATURE_COLUMNS])
