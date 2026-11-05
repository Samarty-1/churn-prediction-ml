"""Download original UCI workbook and stream its rows to typed Parquet."""

import hashlib
import json
import shutil
import urllib.request
import zipfile
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import openpyxl
import pyarrow as pa
import pyarrow.parquet as pq

URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
SHEETS = {"Year 2009-2010": 525461, "Year 2010-2011": 541910}
HEADERS = (
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country",
)
SCHEMA = pa.schema(
    [
        ("invoice", pa.string()),
        ("stock_code", pa.string()),
        ("description", pa.string()),
        ("quantity", pa.int64()),
        ("invoice_date", pa.timestamp("us")),
        ("price", pa.decimal128(18, 3)),
        ("customer_id", pa.string()),
        ("country", pa.string()),
        ("source_sheet", pa.string()),
        ("source_row", pa.int64()),
    ]
)


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def land_workbook(workbook: Path, destination: Path) -> dict:
    book = openpyxl.load_workbook(workbook, read_only=True, data_only=True)
    counts = {}
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".partial")
    try:
        if book.sheetnames != list(SHEETS):
            raise ValueError(f"Unexpected sheets: {book.sheetnames}")
        with pq.ParquetWriter(temporary, SCHEMA, compression="zstd") as writer:
            for sheet in book:
                rows = sheet.iter_rows(values_only=True)
                if tuple(next(rows)) != HEADERS:
                    raise ValueError(f"Unexpected columns in {sheet.title}")
                batch = []
                count = 0
                for row_number, row in enumerate(rows, start=2):
                    invoice, stock, description, quantity, date, price, customer, country = row
                    if quantity is None or price is None or not isinstance(date, datetime):
                        raise ValueError(f"Malformed row {sheet.title}:{row_number}")
                    if quantity != int(quantity):
                        raise ValueError("Non-integral quantity")
                    exact_price = Decimal(str(price))
                    if exact_price != exact_price.quantize(Decimal("0.001")):
                        raise ValueError("Price needs more than three decimal places")
                    if customer is not None and customer != int(customer):
                        raise ValueError("Non-integral customer ID")
                    batch.append(
                        dict(
                            zip(
                                SCHEMA.names,
                                [
                                    str(invoice) if invoice is not None else None,
                                    str(stock) if stock is not None else None,
                                    description,
                                    int(quantity),
                                    date,
                                    exact_price,
                                    str(int(customer)) if customer is not None else None,
                                    country,
                                    sheet.title,
                                    row_number,
                                ],
                                strict=True,
                            )
                        )
                    )
                    count += 1
                    if len(batch) >= 20000:
                        writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))
                        batch.clear()
                if batch:
                    writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))
                counts[sheet.title] = count
                print(f"Landed {sheet.title}: {count} rows", flush=True)
        temporary.replace(destination)
    finally:
        book.close()
        temporary.unlink(missing_ok=True)
    return counts


def ingest(root: Path) -> Path:
    raw = root / "data/raw"
    raw.mkdir(parents=True, exist_ok=True)
    archive = raw / "online-retail-ii.zip"
    if not archive.exists():
        partial = archive.with_suffix(".partial")
        try:
            with urllib.request.urlopen(URL, timeout=120) as response, partial.open("wb") as out:
                shutil.copyfileobj(response, out)
            with zipfile.ZipFile(partial) as zipped:
                if zipped.testzip() is not None:
                    raise ValueError("Corrupt UCI archive")
            partial.replace(archive)
        finally:
            partial.unlink(missing_ok=True)
    workbook = raw / "online_retail_II.xlsx"
    with zipfile.ZipFile(archive) as zipped:
        members = [name for name in zipped.namelist() if name.endswith(".xlsx")]
        if len(members) != 1:
            raise ValueError("Expected exactly one workbook")
        with zipped.open(members[0]) as source, workbook.open("wb") as destination:
            shutil.copyfileobj(source, destination)
    parquet = raw / "lines.parquet"
    counts = land_workbook(workbook, parquet)
    if counts != SHEETS:
        raise ValueError(f"UCI row-count contract failed: {counts}")
    manifest = {
        "url": URL,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "archive_sha256": sha256(archive),
        "workbook_sha256": sha256(workbook),
        "parquet_sha256": sha256(parquet),
        "sheet_rows": counts,
    }
    results = root / "results"
    results.mkdir(exist_ok=True)
    (results / "ingest_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return parquet
