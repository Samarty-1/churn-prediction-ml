-- Adapted from Samarty-1/retail-sql-analytics/sql/staging/01_stg_lines.sql.
-- Preserve source order, exact raw values and fractional-penny prices.
CREATE OR REPLACE TABLE classified AS
WITH numbered AS (
    SELECT *, row_number() OVER (
        PARTITION BY source_sheet, invoice, stock_code, description, quantity,
                     invoice_date, price, customer_id, country
        ORDER BY source_row
    ) AS copy_no FROM raw_lines
)
SELECT *, quantity * price AS line_amount,
    CASE
        WHEN source_sheet = 'Year 2009-2010'
             AND invoice_date >= TIMESTAMP '2010-12-01'
             AND invoice_date < TIMESTAMP '2010-12-10' THEN 'sheet_overlap'
        WHEN copy_no > 1 THEN 'exact_duplicate'
        WHEN upper(trim(invoice)) LIKE 'A%' THEN 'bad_debt_adjustment'
        WHEN upper(trim(stock_code)) IN
             ('POST','DOT','M','C2','C3','D','S','B','BANK CHARGES','AMAZONFEE','CRUK','GIFT')
             OR upper(trim(stock_code)) LIKE 'ADJUST%'
             OR upper(trim(stock_code)) LIKE 'TEST%'
             OR upper(trim(stock_code)) LIKE 'GIFT_%' THEN 'non_product'
        WHEN upper(trim(invoice)) LIKE 'C%' THEN 'cancellation'
        WHEN quantity <= 0 OR price <= 0 THEN 'stock_adjustment'
        WHEN customer_id IS NULL THEN 'missing_customer'
        ELSE 'sale'
    END AS disposition
FROM numbered;

CREATE OR REPLACE TABLE sales AS
SELECT * EXCLUDE (copy_no, disposition) FROM classified WHERE disposition = 'sale';

-- Retain product cancellations for future features, filtered to invoice_date <= cutoff.
CREATE OR REPLACE TABLE cancellations AS
SELECT * EXCLUDE (copy_no, disposition) FROM classified WHERE disposition = 'cancellation';
