# Source and staging contract

Source: [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii),
Daqing Chen, DOI `10.24432/C5CG6D`. The data is licensed CC BY 4.0, separately
from this repository's MIT code license. Download URL and SHA-256 digests are
recorded in `results/ingest_manifest.json`. Raw archives, workbook and Parquet
are local ignored artifacts. No customer-level data is committed.

The import streams the original workbook with openpyxl and lands typed Arrow
Parquet. Source sheet and Excel row number preserve lineage and first-copy
semantics. Invoice IDs, descriptions and stock codes retain their source values.
Prices use exact three-decimal GBP values, with a hard failure for greater
precision; line amounts are not rounded to pennies before aggregation.

SQL adapts the rules from
[retail-sql-analytics staging](https://github.com/Samarty-1/retail-sql-analytics/blob/main/sql/staging/01_stg_lines.sql).
The exclusion order in `sql/staging/01_classify.sql` defines a mutually exclusive
waterfall: overlap, exact duplicates, bad-debt entries, non-product codes,
cancellations, stock adjustments, missing customer IDs, retained sales.
Thus a cancellation of a postage fee is counted as non-product, not twice.
The original SQL `GIFT_%` pattern is preserved (SQL underscore is a wildcard).
Nonpositive quantities and prices are excluded even if not explicitly cancelled.

Before overlap removal, a full-data contract checks both directions of a multiset
comparison of the overlapping windows. The later sheet wins; within each sheet,
exact duplicates keep the earliest Excel row. Distinct lines on the same invoice
are legitimate and are not collapsed by invoice/product alone.

Missing-customer revenue loss is computed from otherwise valid positive product
sales after all earlier exclusions. It is gross product-sales revenue, not net
of returns, not margin, and not the sum of every raw unidentified transaction.
Signed amounts are retained in the waterfall for complete reconciliation.

`sales.parquet` contains identified positive product sales. `cancellations.parquet`
retains deduplicated product cancellations for later return-rate features,
including missing IDs which later features must filter. A cancellation is not
automatically matched to an earlier invoice. No netting or future-informed
customer filtering occurs in staging.

Contracts verify source counts and date coverage, overlap equality and size,
required fields, source-row uniqueness, sales exact-line uniqueness, positive
sales amounts and row reconciliation. Failures abort before output export.
The small fixtures exercise cleaning rules without downloading UCI data.
