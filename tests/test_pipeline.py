import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score

from src.data import generate_churn_data
from src.preprocessing import FEATURE_COLUMNS, TARGET_COLUMN, build_pipeline, split_features_target
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


@pytest.fixture(scope="module")
def df():
    return generate_churn_data(n_customers=500, seed=1)


def test_generate_churn_data_shape(df):
    assert len(df) == 500
    assert set(FEATURE_COLUMNS + [TARGET_COLUMN, "customer_id"]).issubset(df.columns)


def test_churn_is_binary_and_imbalanced(df):
    assert set(df["churn"].unique()) <= {0, 1}
    churn_rate = df["churn"].mean()
    assert 0.05 < churn_rate < 0.6


def test_no_missing_values(df):
    assert df[FEATURE_COLUMNS].isna().sum().sum() == 0


def test_generation_is_deterministic():
    df1 = generate_churn_data(n_customers=100, seed=7)
    df2 = generate_churn_data(n_customers=100, seed=7)
    pd.testing.assert_frame_equal(df1, df2)


def test_split_features_target_shapes(df):
    X, y = split_features_target(df)
    assert list(X.columns) == FEATURE_COLUMNS
    assert len(X) == len(y) == len(df)


def test_pipeline_fits_and_beats_random_baseline(df):
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=0
    )
    pipeline = build_pipeline(LogisticRegression(max_iter=1000, random_state=0))
    pipeline.fit(X_train, y_train)
    proba = pipeline.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, proba)
    assert auc > 0.6  # meaningfully better than a random classifier (0.5)
