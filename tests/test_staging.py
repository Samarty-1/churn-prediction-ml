from datetime import datetime
from decimal import Decimal
from pathlib import Path

import duckdb
import pyarrow as pa
import pytest

from churn.ingest import SCHEMA
from churn.staging import stage

SQL = Path(__file__).resolve().parents[1] / "sql/staging"


def row(**changes):
    values = dict(
        invoice="100",
        stock_code="12345",
        description="GIFT PRODUCT",
        quantity=2,
        invoice_date=datetime(2010, 12, 2),
        price=Decimal("1.255"),
        customer_id="123",
        country="United Kingdom",
        source_sheet="Year 2010-2011",
        source_row=2,
    )
    values.update(changes)
    return values


def connect(rows):
    connection = duckdb.connect()
    connection.register("raw_lines", pa.Table.from_pylist(rows, schema=SCHEMA))
    return connection


def test_overlap_and_duplicates_keep_first_later_sheet_copy():
    with connect([row(source_sheet="Year 2009-2010"), row(source_row=3), row()]) as con:
        report = stage(con, SQL)
        assert con.execute(
            "SELECT source_sheet, source_row, line_amount FROM sales"
        ).fetchall() == [("Year 2010-2011", 2, Decimal("2.510"))]
        counts = {item["step"]: item["rows"] for item in report["waterfall"]}
        assert counts["sheet_overlap"] == 1
        assert counts["exact_duplicate"] == 1
        assert counts["sale"] == 1


@pytest.mark.parametrize(
    "stock",
    [
        "POST",
        "DOT",
        "M",
        "C2",
        "C3",
        "D",
        "S",
        "B",
        "BANK CHARGES",
        "AMAZONFEE",
        "CRUK",
        "GIFT",
        "ADJUST1",
        "TEST1",
        "GIFT_0001",
    ],
)
def test_non_product_codes(stock):
    with connect([row(stock_code=stock)]) as con:
        stage(con, SQL)
        assert con.execute("SELECT disposition FROM classified").fetchone()[0] == "non_product"
        assert con.execute("SELECT count(*) FROM sales").fetchone()[0] == 0


@pytest.mark.parametrize(
    "changes,expected",
    [
        ({"invoice": "A123"}, "bad_debt_adjustment"),
        ({"invoice": "C123", "quantity": -2}, "cancellation"),
        ({"price": Decimal("0")}, "stock_adjustment"),
        ({"price": Decimal("-1")}, "stock_adjustment"),
        ({"quantity": -2}, "stock_adjustment"),
        ({"quantity": 0}, "stock_adjustment"),
        ({"customer_id": None}, "missing_customer"),
    ],
)
def test_exclusions(changes, expected):
    with connect([row(**changes)]) as con:
        stage(con, SQL)
        assert con.execute("SELECT disposition FROM classified").fetchone()[0] == expected
        assert con.execute("SELECT count(*) FROM sales").fetchone()[0] == 0
        assert con.execute("SELECT count(*) FROM cancellations").fetchone()[0] == (
            1 if expected == "cancellation" else 0
        )


def test_revenue_loss_and_waterfall_reconcile():
    with connect(
        [row(), row(source_row=3, customer_id=None), row(source_row=4, invoice="C100", quantity=-1)]
    ) as con:
        report = stage(con, SQL)
        assert report["missing_customer_sale_revenue_gbp"] == "2.510"
        assert report["eligible_product_sale_revenue_gbp"] == "5.020"
        assert sum(item["rows"] for item in report["waterfall"]) == report["raw_rows"]
        assert not any(report["contracts"].values())


@pytest.mark.parametrize(
    "rows",
    [
        [row(invoice_date=datetime(2012, 1, 1))],
        [row(invoice=None)],
        [row(), row(invoice="101")],
    ],
)
def test_contract_rejects_corrupt_input(rows):
    with connect(rows) as con, pytest.raises(ValueError, match="Data contract failed"):
        stage(con, SQL)


def test_full_source_contract_rejects_fixture():
    with connect([row()]) as con, pytest.raises(ValueError, match="Data contract failed"):
        stage(con, SQL, full_data=True)


def test_overlap_date_boundaries():
    with connect(
        [
            row(source_sheet="Year 2009-2010", invoice_date=datetime(2010, 11, 30)),
            row(
                source_sheet="Year 2009-2010",
                source_row=3,
                invoice_date=datetime(2010, 12, 9, 23, 59),
            ),
            row(source_sheet="Year 2009-2010", source_row=4, invoice_date=datetime(2010, 12, 10)),
        ]
    ) as con:
        stage(con, SQL)
        assert con.execute("SELECT source_row FROM sales ORDER BY source_row").fetchall() == [
            (2,),
            (4,),
        ]
