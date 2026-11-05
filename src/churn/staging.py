"""SQL staging, fail-closed contracts, and an exhaustive cleaning waterfall."""

import json
from pathlib import Path

import duckdb

from churn.ingest import sha256

ORDER = [
    "sheet_overlap",
    "exact_duplicate",
    "bad_debt_adjustment",
    "non_product",
    "cancellation",
    "stock_adjustment",
    "missing_customer",
    "sale",
]
FIELDS = "invoice, stock_code, description, quantity, invoice_date, price, customer_id, country"


def stage(connection, sql_dir: Path, *, full_data: bool = False) -> dict:
    connection.execute((sql_dir / "01_classify.sql").read_text())
    connection.execute((sql_dir / "02_contracts.sql").read_text())
    checks = dict(connection.execute("SELECT * FROM contract_failures").fetchall())
    if full_data:
        # Validate the overlap as a multiset BEFORE dropping it, including duplicates.
        a = f"SELECT {FIELDS} FROM raw_lines WHERE source_sheet = 'Year 2009-2010'"
        b = f"SELECT {FIELDS} FROM raw_lines WHERE source_sheet = 'Year 2010-2011'"
        window = " AND invoice_date >= '2010-12-01' AND invoice_date < '2010-12-10'"
        mismatch = connection.execute(
            f"SELECT count(*) FROM (({a + window} EXCEPT ALL {b + window}) "
            f"UNION ALL ({b + window} EXCEPT ALL {a + window}))"
        ).fetchone()[0]
        checks["overlap_multiset_equality"] = mismatch
        counts = dict(
            connection.execute(
                "SELECT source_sheet, count(*) FROM raw_lines GROUP BY source_sheet"
            ).fetchall()
        )
        checks["source_sheet_counts"] = int(
            counts
            != {
                "Year 2009-2010": 525461,
                "Year 2010-2011": 541910,
            }
        )
        overlap = connection.execute(
            "SELECT count(*) FROM classified WHERE disposition = 'sheet_overlap'"
        ).fetchone()[0]
        checks["overlap_count"] = abs(overlap - 22523)
        dates = connection.execute(
            "SELECT min(invoice_date)::date, max(invoice_date)::date FROM raw_lines"
        ).fetchone()
        checks["date_coverage"] = int(tuple(map(str, dates)) != ("2009-12-01", "2011-12-09"))
    if any(checks.values()):
        raise ValueError(f"Data contract failed: {checks}")
    grouped = {
        kind: (count, amount)
        for kind, count, amount in connection.execute(
            "SELECT disposition, count(*), sum(line_amount) FROM classified GROUP BY disposition"
        ).fetchall()
    }
    remaining = connection.execute("SELECT count(*) FROM raw_lines").fetchone()[0]
    raw_count = remaining
    waterfall = []
    for kind in ORDER:
        count, amount = grouped.get(kind, (0, 0))
        if kind != "sale":
            remaining -= count
        waterfall.append(
            {
                "step": kind,
                "rows": count,
                "signed_amount_gbp": str(amount),
                "remaining_sale_candidates": remaining,
            }
        )
    missing = grouped.get("missing_customer", (0, 0))[1]
    retained = grouped.get("sale", (0, 0))[1]
    if remaining != grouped.get("sale", (0, 0))[0]:
        raise ValueError("Waterfall reconciliation failed")
    return {
        "raw_rows": raw_count,
        "waterfall": waterfall,
        "contracts": checks,
        "missing_customer_sale_revenue_gbp": str(missing),
        "eligible_product_sale_revenue_gbp": str(missing + retained),
        "retained_sale_revenue_gbp": str(retained),
        "positive_price_rounds_to_zero_rows": connection.execute(
            "SELECT count(*) FROM sales WHERE price::decimal(18, 2) = 0"
        ).fetchone()[0],
        "positive_price_rounds_to_zero_amount_gbp": str(
            connection.execute(
                "SELECT coalesce(sum(line_amount), 0) FROM sales WHERE price::decimal(18, 2) = 0"
            ).fetchone()[0]
        ),
        "customers": connection.execute("SELECT count(DISTINCT customer_id) FROM sales").fetchone()[
            0
        ],
        "orders": connection.execute("SELECT count(DISTINCT invoice) FROM sales").fetchone()[0],
        "sale_date_range": list(
            map(
                str,
                connection.execute(
                    "SELECT min(invoice_date), max(invoice_date) FROM sales"
                ).fetchone(),
            )
        ),
        "amount_note": "Exact GBP decimal amounts; no price or line rounding. Not net revenue.",
    }


def run_staging(root: Path, parquet: Path) -> dict:
    manifest = json.loads((root / "results/ingest_manifest.json").read_text())
    if sha256(parquet) != manifest["parquet_sha256"]:
        raise ValueError("Raw Parquet differs from the ingestion manifest")
    with duckdb.connect() as connection:
        connection.read_parquet(str(parquet)).create_view("raw_lines")
        report = stage(connection, root / "sql/staging", full_data=True)
        processed = root / "data/processed"
        processed.mkdir(parents=True, exist_ok=True)
        for table in ("sales", "cancellations"):
            connection.table(table).write_parquet(str(processed / f"{table}.parquet"))
    (root / "results").mkdir(exist_ok=True)
    (root / "results/cleaning_summary.json").write_text(json.dumps(report, indent=2) + "\n")
    return report
