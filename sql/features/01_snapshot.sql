-- Inputs are already restricted to invoice_date <= cutoff in features.py.
WITH eligible AS (
    SELECT DISTINCT customer_id FROM sale_history
    WHERE invoice_date > (SELECT cutoff FROM snapshot_clock) - INTERVAL 365 DAY
), recent AS (
    SELECT s.*, upper(coalesce(description, '')) AS text_description
    FROM sale_history s JOIN eligible USING (customer_id)
    WHERE invoice_date > (SELECT cutoff FROM snapshot_clock) - INTERVAL 365 DAY
), categorized AS (
    SELECT *, CASE
        WHEN regexp_matches(text_description, 'CHRISTMAS|XMAS') THEN 'CHRISTMAS'
        WHEN regexp_matches(text_description, 'MUG|CUP|PLATE|BOWL') THEN 'KITCHEN'
        WHEN regexp_matches(text_description, 'CANDLE|CUSHION|LANTERN') THEN 'HOME'
        WHEN regexp_matches(text_description, 'NECKLACE|BRACELET|EARRING') THEN 'JEWELRY'
        WHEN regexp_matches(text_description, 'BAG|PURSE') THEN 'BAGS'
        WHEN regexp_matches(text_description, 'PEN|PENCIL|NOTEBOOK') THEN 'STATIONERY'
        WHEN regexp_matches(text_description, 'TOY|GAME|DOLL') THEN 'TOYS'
        ELSE 'OTHER' END AS category_proxy
    FROM recent
), lifetime AS (
    SELECT customer_id, min(invoice_date) AS first_sale, max(invoice_date) AS last_sale,
        count(DISTINCT invoice_date::date) - 1 AS bg_repeat_days,
        date_diff('day', min(invoice_date)::date, max(invoice_date)::date) AS bg_recency_days,
        date_diff('day', min(invoice_date)::date,
                  (SELECT cutoff FROM snapshot_clock)::date) AS bg_age_days
    FROM sale_history JOIN eligible USING (customer_id) GROUP BY customer_id
), aggregate_sales AS (
    SELECT customer_id, count(DISTINCT invoice) AS frequency_365,
        sum(line_amount)::double AS monetary_365,
        count(DISTINCT invoice_date::date) AS purchase_days_365,
        sum(quantity)::double / count(DISTINCT invoice) AS basket_units_mean,
        count(*)::double / count(DISTINCT invoice) AS basket_lines_mean,
        count(DISTINCT stock_code) AS product_breadth,
        count(DISTINCT category_proxy) AS category_breadth_proxy,
        coalesce(sum(line_amount) FILTER (WHERE invoice_date >
            (SELECT cutoff FROM snapshot_clock) - INTERVAL 90 DAY), 0)::double AS sales_90,
        coalesce(sum(line_amount) FILTER (WHERE invoice_date >
            (SELECT cutoff FROM snapshot_clock) - INTERVAL 180 DAY AND invoice_date <=
            (SELECT cutoff FROM snapshot_clock) - INTERVAL 90 DAY), 0)::double AS sales_prior_90,
        count(DISTINCT invoice) FILTER (WHERE invoice_date >
            (SELECT cutoff FROM snapshot_clock) - INTERVAL 90 DAY) AS frequency_90,
        count(DISTINCT invoice) FILTER (WHERE invoice_date >
            (SELECT cutoff FROM snapshot_clock) - INTERVAL 180 DAY AND invoice_date <=
            (SELECT cutoff FROM snapshot_clock) - INTERVAL 90 DAY) AS frequency_prior_90
    FROM categorized GROUP BY customer_id
), purchase_dates AS (
    SELECT DISTINCT customer_id, invoice_date::date AS purchase_date FROM recent
), gaps AS (
    SELECT customer_id, date_diff('day', lag(purchase_date) OVER (
        PARTITION BY customer_id ORDER BY purchase_date), purchase_date) AS gap
    FROM purchase_dates
), gap_stats AS (
    SELECT customer_id, avg(gap) AS gap_mean_days, stddev_samp(gap) AS gap_std_days
    FROM gaps GROUP BY customer_id
), returns AS (
    SELECT customer_id, count(DISTINCT invoice) AS cancellation_invoices_365,
        sum(abs(line_amount))::double AS cancellation_amount_365,
        coalesce(sum(abs(line_amount)) FILTER (WHERE invoice_date >
            (SELECT cutoff FROM snapshot_clock) - INTERVAL 90 DAY), 0)::double
            AS cancellation_amount_90
    FROM cancellation_history
    WHERE invoice_date > (SELECT cutoff FROM snapshot_clock) - INTERVAL 365 DAY
    GROUP BY customer_id
), countries AS (
    SELECT customer_id, coalesce(country, 'UNKNOWN') AS country FROM sale_history
    QUALIFY row_number() OVER (PARTITION BY customer_id
        ORDER BY invoice_date DESC, invoice ASC, stock_code ASC, country ASC) = 1
)
SELECT customer_id,
    epoch((SELECT cutoff FROM snapshot_clock) - last_sale) / 86400.0 AS recency_days,
    a.* EXCLUDE(customer_id), gap_mean_days, gap_std_days,
    (epoch((SELECT cutoff FROM snapshot_clock) - last_sale) / 86400.0)
        / nullif(gap_mean_days, 0) AS overdue_ratio,
    sales_90 - sales_prior_90 AS sales_trend_difference,
    sales_90 / nullif(sales_prior_90, 0) AS sales_trend_ratio,
    frequency_90 - frequency_prior_90 AS frequency_trend_difference,
    frequency_90::double / nullif(frequency_prior_90, 0) AS frequency_trend_ratio,
    coalesce(cancellation_invoices_365, 0) AS cancellation_invoices_365,
    coalesce(cancellation_amount_365, 0) AS cancellation_amount_365,
    coalesce(cancellation_amount_90, 0) AS cancellation_amount_90,
    coalesce(cancellation_invoices_365, 0)::double /
        (frequency_365 + coalesce(cancellation_invoices_365, 0)) AS cancellation_rate,
    coalesce(cancellation_amount_365, 0) / monetary_365 AS cancellation_amount_ratio,
    epoch((SELECT cutoff FROM snapshot_clock) - first_sale) / 86400.0 AS tenure_days,
    country,
    date_diff('day', (SELECT cutoff FROM snapshot_clock)::date,
        CASE WHEN month((SELECT cutoff FROM snapshot_clock)) = 12
                   AND day((SELECT cutoff FROM snapshot_clock)) > 25
        THEN make_date(year((SELECT cutoff FROM snapshot_clock))::int + 1, 12, 25)
        ELSE make_date(year((SELECT cutoff FROM snapshot_clock))::int, 12, 25) END)
        AS days_to_christmas,
    (first_sale < TIMESTAMP '2010-01-01')::int AS acquisition_left_censored,
    bg_repeat_days, bg_recency_days, bg_age_days,
    greatest(0, 0.30 * (sales_90 - coalesce(cancellation_amount_90, 0))) AS customer_value
FROM aggregate_sales a
JOIN lifetime USING (customer_id)
JOIN gap_stats USING (customer_id)
JOIN countries USING (customer_id)
LEFT JOIN returns USING (customer_id)
ORDER BY customer_id;
