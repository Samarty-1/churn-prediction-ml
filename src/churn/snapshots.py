"""Build/read development snapshots only; audit real-data temporal invariance."""

import hashlib
import json
import math
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq

from churn.features import FEATURE_COLUMNS, build_features
from churn.holdout import (
    DEVELOPMENT_CUTOFFS,
    HORIZON,
    SEALED_CUTOFFS,
    development_origins,
    matured_training_cutoffs,
    require_development,
)
from churn.ingest import sha256
from churn.labels import build_labels

SNAPSHOT_CODE = (
    "src/churn/features.py",
    "src/churn/labels.py",
    "src/churn/holdout.py",
    "src/churn/snapshots.py",
    "sql/features/01_snapshot.sql",
)


def text_digest(path: Path) -> str:
    """Canonical newlines keep source fingerprints stable across Git platforms."""
    return hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def snapshot_path(root: Path, cutoff) -> Path:
    cutoff = require_development(cutoff)
    return root / "data/development" / f"{cutoff.date().isoformat()}.parquet"


def read_snapshot(root: Path, cutoff):
    cutoff = require_development(cutoff)
    path = snapshot_path(root, cutoff)
    manifest = json.loads((root / "results/development_summary.json").read_text())
    if text_digest(root / "docs/PREREGISTRATION.md") != manifest["preregistration_sha256"]:
        raise ValueError("Preregistration changed; rebuild and review snapshots")
    for name, digest in manifest["code_sha256"].items():
        if text_digest(root / name) != digest:
            raise ValueError("Snapshot code changed; rebuild and review snapshots")
    registered = {r["cutoff"]: r for r in manifest["cutoffs"]}
    if sha256(path) != registered[cutoff.date().isoformat()]["snapshot_sha256"]:
        raise ValueError("Snapshot digest mismatch")
    table = pq.read_table(path)
    if set(table["cutoff"].to_pylist()) != {cutoff}:
        raise ValueError("Snapshot cutoff mismatch")
    if set(table["label_end"].to_pylist()) != {cutoff + HORIZON}:
        raise ValueError("Snapshot label-window mismatch")
    return table


def build_development(root: Path) -> dict:
    prereg = root / "docs/PREREGISTRATION.md"
    if not prereg.exists():
        raise ValueError("Write preregistration before constructing evaluation snapshots")
    destination = root / "data/development"
    destination.mkdir(parents=True, exist_ok=True)
    rows = []
    with duckdb.connect() as con:
        for table in ("sales", "cancellations"):
            con.read_parquet(str(root / f"data/processed/{table}.parquet")).create_view(table)
        for cutoff in DEVELOPMENT_CUTOFFS:
            features = build_features(con, cutoff)
            labels = build_labels(con, cutoff)
            if not features["customer_id"].equals(labels["customer_id"]):
                raise ValueError("Feature and label populations differ")
            # Physically exclude all future records, then rebuild from the truncated sources.
            with duckdb.connect() as truncated:
                for table in ("sales", "cancellations"):
                    past = con.execute(
                        f"SELECT * FROM {table} WHERE invoice_date <= ?", [cutoff]
                    ).fetch_arrow_table()
                    truncated.register(table, past)
                recomputed = build_features(truncated, cutoff)
            if not features.equals(recomputed):
                raise ValueError(f"Future-deletion leakage test failed at {cutoff}")
            count = features.num_rows
            if count == 0 or len(set(features["customer_id"].to_pylist())) != count:
                raise ValueError("Invalid snapshot customer population")
            for name in FEATURE_COLUMNS:
                if name != "country" and any(
                    value is not None and not math.isfinite(value)
                    for value in features[name].to_pylist()
                ):
                    raise ValueError(f"Nonfinite feature: {name}")
            snapshot = features.append_column("churn", labels["churn"])
            snapshot = snapshot.append_column("cutoff", pa.array([cutoff] * count))
            snapshot = snapshot.append_column("label_end", pa.array([cutoff + HORIZON] * count))
            path = snapshot_path(root, cutoff)
            temporary = path.with_suffix(".partial")
            pq.write_table(snapshot, temporary, compression="zstd")
            temporary.replace(path)
            churned = sum(labels["churn"].to_pylist())
            rows.append(
                {
                    "cutoff": cutoff.date().isoformat(),
                    "customers": count,
                    "churned": churned,
                    "churn_rate": churned / count,
                    "feature_columns": len(features.column_names) - 1,
                    "feature_null_counts": {
                        name: features[name].null_count for name in FEATURE_COLUMNS
                    },
                    "future_deletion_identical": True,
                    "snapshot_sha256": sha256(path),
                    "matured_training_cutoffs": [
                        t.date().isoformat() for t in matured_training_cutoffs(cutoff)
                    ],
                    "role": "backtest" if cutoff in development_origins() else "warmup",
                }
            )
            print(f"Validated development snapshot {cutoff.date()}: {count} customers", flush=True)
    report = {
        "phase": 2,
        "holdout_status": "sealed",
        "holdout_access_supported": False,
        "sealed_cutoffs": [t.date().isoformat() for t in SEALED_CUTOFFS],
        "preregistration_sha256": text_digest(prereg),
        "code_sha256": {name: text_digest(root / name) for name in SNAPSHOT_CODE},
        "feature_allowlist": list(FEATURE_COLUMNS),
        "primary_assumptions": {
            "save_rate": 0.10,
            "offer_cost_gbp": 5,
            "margin": 0.30,
            "value_window_days": 90,
        },
        "source_sha256": {
            t: sha256(root / f"data/processed/{t}.parquet") for t in ("sales", "cancellations")
        },
        "cutoffs": rows,
    }
    (root / "results/development_summary.json").write_text(json.dumps(report, indent=2) + "\n")
    return report
