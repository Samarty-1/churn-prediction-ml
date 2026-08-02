"""CLI to run the trained churn model on new customer data.

Usage:
    python -m src.predict --input path/to/customers.csv --output path/to/predictions.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from src.preprocessing import FEATURE_COLUMNS
from src.train import MODEL_PATH


def predict(input_path: Path, output_path: Path) -> pd.DataFrame:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"No trained model found at {MODEL_PATH}. Run `python -m src.train` first.")

    pipeline = joblib.load(MODEL_PATH)
    df = pd.read_csv(input_path)
    missing = set(FEATURE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Input file is missing required columns: {sorted(missing)}")

    X = df[FEATURE_COLUMNS]
    df["churn_prediction"] = pipeline.predict(X)
    df["churn_probability"] = pipeline.predict_proba(X)[:, 1].round(4)
    df.to_csv(output_path, index=False)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict customer churn from a CSV of customer records.")
    parser.add_argument("--input", required=True, type=Path, help="CSV file with customer feature columns")
    parser.add_argument("--output", required=True, type=Path, help="Where to write predictions CSV")
    args = parser.parse_args()

    result = predict(args.input, args.output)
    print(f"Wrote {len(result)} predictions to {args.output}")
    print(f"Predicted churn rate: {result['churn_prediction'].mean():.2%}")


if __name__ == "__main__":
    main()
