CREATE OR REPLACE TABLE contract_failures AS
SELECT 'raw_required_fields' AS contract, count(*) AS failures FROM raw_lines
WHERE invoice IS NULL OR stock_code IS NULL OR quantity IS NULL OR price IS NULL
   OR invoice_date IS NULL OR source_row IS NULL OR source_sheet IS NULL
UNION ALL
SELECT 'raw_source_uniqueness', count(*) FROM (
    SELECT source_sheet, source_row FROM raw_lines GROUP BY ALL HAVING count(*) > 1
)
UNION ALL
SELECT 'sales_positive_identified', count(*) FROM sales
WHERE quantity <= 0 OR price <= 0 OR line_amount <= 0 OR customer_id IS NULL
UNION ALL
SELECT 'sales_exact_uniqueness', count(*) FROM (
    SELECT invoice, stock_code, description, quantity, invoice_date, price, customer_id,
           country FROM sales GROUP BY ALL HAVING count(*) > 1
)
UNION ALL
SELECT 'date_bounds', count(*) FROM raw_lines
WHERE invoice_date < TIMESTAMP '2009-12-01' OR invoice_date >= TIMESTAMP '2011-12-10'
UNION ALL
SELECT 'row_reconciliation', abs(
    (SELECT count(*) FROM raw_lines) - (SELECT count(*) FROM classified)
);
