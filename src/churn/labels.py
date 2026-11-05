"""Mature 90-day nonpurchase labels; labels never flow into feature construction."""

from churn.holdout import HORIZON, OBSERVATION_END, require_development


def build_labels(connection, cutoff, *, observation_end=OBSERVATION_END):
    cutoff = require_development(cutoff)
    if cutoff + HORIZON > observation_end:
        raise ValueError("Outcome window is not fully observed")
    return connection.execute(
        """
        WITH eligible AS (
            SELECT DISTINCT customer_id FROM sales
            WHERE invoice_date > ?::TIMESTAMP - INTERVAL 365 DAY AND invoice_date <= ?
        ), future AS (
            SELECT DISTINCT customer_id FROM sales WHERE invoice_date > ? AND invoice_date <= ?
        )
        SELECT e.customer_id, (f.customer_id IS NULL)::int AS churn
        FROM eligible e LEFT JOIN future f USING (customer_id) ORDER BY customer_id
        """,
        [cutoff, cutoff, cutoff, cutoff + HORIZON],
    ).fetch_arrow_table()
