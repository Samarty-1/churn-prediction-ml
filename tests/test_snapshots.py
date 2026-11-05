from datetime import datetime, timedelta
from decimal import Decimal
from math import sqrt

import duckdb
import pyarrow as pa
import pytest

from churn.features import FEATURE_COLUMNS, build_features
from churn.holdout import (
    CUTOFFS,
    DEVELOPMENT_CUTOFFS,
    HORIZON,
    SEALED_CUTOFFS,
    HoldoutSealedError,
    development_origins,
    matured_training_cutoffs,
    require_development,
)
from churn.ingest import SCHEMA
from churn.labels import build_labels
from churn.snapshots import read_snapshot, snapshot_path

T = datetime(2010, 6, 9)
SALE_SCHEMA = SCHEMA.append(pa.field("line_amount", pa.decimal128(18, 3)))


def line(
    customer, days, invoice, *, quantity=1, price="10", stock="1", description="MUG", country="UK"
):
    return {
        "customer_id": customer,
        "invoice_date": T + timedelta(days=days),
        "invoice": invoice,
        "quantity": quantity,
        "price": Decimal(price),
        "line_amount": quantity * Decimal(price),
        "stock_code": stock,
        "description": description,
        "country": country,
        "source_sheet": "fixture",
        "source_row": int(invoice.lstrip("C") or 0),
    }


def connect(sales, cancellations=()):
    con = duckdb.connect()
    con.register("sales", pa.Table.from_pylist(sales, schema=SALE_SCHEMA))
    con.register("cancellations", pa.Table.from_pylist(list(cancellations), schema=SALE_SCHEMA))
    return con


def test_known_labels_and_exact_window_boundaries():
    sales = [
        line("at_cutoff", 0, "1"),
        line("future_at_end", -1, "2"),
        line("future_at_end", 90, "3"),
        line("after_end", -1, "4"),
        line("after_end", 90 + 1 / 86400, "5"),
        line("expired", -365, "6"),
        line("expired", 1, "7"),
        line("eligible_boundary", -365 + 1 / 86400, "8"),
        line("future_only", 1, "9"),
        line("return_only_future", -1, "10"),
    ]
    returns = [line("return_only_future", 2, "C11", quantity=-1)]
    with connect(sales, returns) as con:
        observed = {r["customer_id"]: r["churn"] for r in build_labels(con, T).to_pylist()}
        assert observed == {
            "at_cutoff": 1,
            "future_at_end": 0,
            "after_end": 1,
            "eligible_boundary": 1,
            "return_only_future": 1,
        }
        assert set(build_features(con, T)["customer_id"].to_pylist()) == set(observed)
        with pytest.raises(ValueError, match="not fully observed"):
            build_labels(con, T, observation_end=T + HORIZON - timedelta(seconds=1))


def test_known_feature_values_and_missing_gaps():
    sales = [
        line("A", -120, "1", quantity=2),
        line("A", -60, "2", price="20", stock="2", description="BAG", country="FR"),
        line("A", -30, "3", quantity=3, price="5"),
        line("A", 0, "4", price="1", stock="3", description="XMAS", country="FR"),
        line("B", -1, "5"),
    ]
    with connect(sales, [line("A", -10, "C6", quantity=-1, price="5")]) as con:
        a, b = build_features(con, T).to_pylist()
        expected = {
            "frequency_365": 4,
            "monetary_365": 56,
            "purchase_days_365": 4,
            "recency_days": 0,
            "basket_units_mean": 1.75,
            "basket_lines_mean": 1,
            "product_breadth": 3,
            "category_breadth_proxy": 3,
            "sales_90": 36,
            "sales_prior_90": 20,
            "frequency_90": 3,
            "frequency_prior_90": 1,
            "gap_mean_days": 40,
            "gap_std_days": sqrt(300),
            "overdue_ratio": 0,
            "sales_trend_difference": 16,
            "sales_trend_ratio": 1.8,
            "frequency_trend_difference": 2,
            "frequency_trend_ratio": 3,
            "cancellation_invoices_365": 1,
            "cancellation_amount_365": 5,
            "cancellation_amount_90": 5,
            "cancellation_rate": 0.2,
            "cancellation_amount_ratio": 5 / 56,
            "tenure_days": 120,
            "days_to_christmas": (datetime(2010, 12, 25) - T).days,
            "acquisition_left_censored": 0,
            "bg_repeat_days": 3,
            "bg_recency_days": 120,
            "bg_age_days": 120,
            "customer_value": 9.3,
        }
        assert set(expected) | {"country"} == set(FEATURE_COLUMNS)
        for name, value in expected.items():
            assert a[name] == pytest.approx(value), name
        assert a["country"] == "FR"
        assert b["gap_mean_days"] is None
        assert b["gap_std_days"] is None
        assert b["overdue_ratio"] is None
        assert b["sales_trend_ratio"] is None


def test_delete_future_leaves_all_features_identical():
    past = [line("A", -100, "1"), line("A", -1, "2"), line("B", 0, "3")]
    returns = [line("A", -1, "C4", quantity=-1)]
    future = [
        line("A", 1, "5", quantity=99999, country="FUTURE", description="TOY"),
        line("C", 2, "6"),
    ]
    future_returns = [line("B", 1, "C7", quantity=-99999)]
    with (
        connect(past + future, returns + future_returns) as full,
        connect(past, returns) as truncated,
    ):
        assert build_features(full, T).equals(build_features(truncated, T))


def test_same_day_invoices_not_zero_length_gaps_and_value_floor():
    sales = [line("A", -2, "1"), line("A", -2, "2"), line("A", -1, "3")]
    with connect(sales, [line("A", 0, "C4", quantity=-100)]) as con:
        a = build_features(con, T).to_pylist()[0]
        assert a["frequency_365"] == 3
        assert a["purchase_days_365"] == 2
        assert a["gap_mean_days"] == 1
        assert a["gap_std_days"] is None
        assert a["bg_repeat_days"] == 1
        assert a["customer_value"] == 0


@pytest.mark.parametrize("cutoff", SEALED_CUTOFFS)
def test_holdout_rejected_before_any_database_or_file_access(cutoff, tmp_path):
    class NoAccess:
        def execute(self, *args, **kwargs):
            pytest.fail("Guard allowed data access")

    for function in (build_features, build_labels):
        with pytest.raises(HoldoutSealedError):
            function(NoAccess(), cutoff)
    with pytest.raises(HoldoutSealedError):
        read_snapshot(tmp_path / "does-not-exist", cutoff)
    with pytest.raises(HoldoutSealedError):
        snapshot_path(tmp_path, cutoff)


def test_guard_rejects_aliases_unregistered_dates_and_timezone():
    for value in ("2011-07-09", "2011-07-09T12:00:00", "2012-01-01"):
        with pytest.raises(HoldoutSealedError):
            require_development(value)
    for value in ("2010-06-08", "2010-06-09T01:00:00", "2010-06-09T00:00:00+00:00"):
        with pytest.raises(ValueError):
            require_development(value)


def test_rolling_schedule_purges_unmatured_labels():
    assert len(CUTOFFS) == 16
    assert len(DEVELOPMENT_CUTOFFS) == 13
    assert development_origins()[0] == datetime(2010, 11, 9)
    assert development_origins()[-1] == datetime(2011, 6, 9)
    assert len(development_origins()) == 8
    for test in DEVELOPMENT_CUTOFFS:
        for train in matured_training_cutoffs(test):
            assert train + HORIZON <= test
    assert datetime(2010, 9, 9) not in matured_training_cutoffs(datetime(2010, 11, 9))
