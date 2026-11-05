import json
from datetime import datetime

import pyarrow.parquet as pq
import pytest

from churn.ingest import HEADERS, SHEETS, ingest, land_workbook
from churn.staging import run_staging


class Sheet:
    def __init__(self, title, rows, headers=HEADERS):
        self.title = title
        self.rows = [headers, *rows]

    def iter_rows(self, *, values_only):
        assert values_only
        return iter(self.rows)


class Book:
    sheetnames = list(SHEETS)

    def __init__(self, rows, headers=HEADERS):
        self.sheets = [Sheet(title, rows, headers) for title in SHEETS]
        self.closed = False

    def __iter__(self):
        return iter(self.sheets)

    def close(self):
        self.closed = True


def test_import_keeps_lineage_precision_and_missing_customer(monkeypatch, tmp_path):
    line = [100, "00123", 123, 2, datetime(2010, 12, 2), 1.255, None, "UK"]
    book = Book([line, line])
    monkeypatch.setattr("churn.ingest.openpyxl.load_workbook", lambda *a, **k: book)
    target = tmp_path / "raw/lines.parquet"
    assert land_workbook(tmp_path / "unused.xlsx", target) == dict.fromkeys(SHEETS, 2)
    rows = pq.read_table(target).to_pylist()
    assert len(rows) == 4  # Import must not clean or deduplicate.
    assert [r["source_row"] for r in rows] == [2, 3, 2, 3]
    assert rows[0]["stock_code"] == "00123"
    assert rows[0]["description"] == "123"
    assert str(rows[0]["price"]) == "1.255"
    assert rows[0]["customer_id"] is None
    assert book.closed


def test_changed_archive_is_rejected(tmp_path):
    (tmp_path / "data/raw").mkdir(parents=True)
    (tmp_path / "results").mkdir()
    (tmp_path / "data/raw/online-retail-ii.zip").write_bytes(b"changed")
    (tmp_path / "results/ingest_manifest.json").write_text(
        json.dumps({"archive_sha256": "expected-original-digest"})
    )
    with pytest.raises(ValueError, match="Archive differs"):
        ingest(tmp_path)


def test_changed_parquet_is_rejected_before_staging(tmp_path):
    (tmp_path / "results").mkdir()
    parquet = tmp_path / "lines.parquet"
    parquet.write_bytes(b"changed")
    (tmp_path / "results/ingest_manifest.json").write_text(
        json.dumps({"parquet_sha256": "expected-original-digest"})
    )
    with pytest.raises(ValueError, match="Raw Parquet differs"):
        run_staging(tmp_path, parquet)


def test_schema_change_fails_without_publishing_parquet(monkeypatch, tmp_path):
    book = Book([], headers=("wrong",))
    monkeypatch.setattr("churn.ingest.openpyxl.load_workbook", lambda *a, **k: book)
    target = tmp_path / "lines.parquet"
    with pytest.raises(ValueError, match="Unexpected columns"):
        land_workbook(tmp_path / "unused.xlsx", target)
    assert not target.exists()
    assert not target.with_suffix(".partial").exists()
    assert book.closed
