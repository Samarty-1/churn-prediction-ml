import numpy as np
import pandas as pd
import pytest
from scipy.integrate import quad
from scipy.stats import gamma
from sklearn.metrics import average_precision_score, roc_auc_score

from churn.baselines import BGNBD, RFM, bg_log_likelihood
from churn.decision import decide, outcome_profit
from churn.evaluate import Metrics, summarize
from churn.models import choose_calibration


def test_bg_zero_purchase_probability_against_numerical_integration():
    model = BGNBD()
    model.parameters = np.array([0.7, 30, 1.5, 3])
    frame = pd.DataFrame(
        {"bg_repeat_days": [0, 2, 10], "bg_recency_days": [0, 15, 50], "bg_age_days": [20, 50, 60]}
    )
    alive = model.probability_alive(frame)
    for i, row in frame.iterrows():
        integrated = quad(
            lambda rate: np.exp(-rate * 90)
            * gamma.pdf(rate, a=0.7 + row.bg_repeat_days, scale=1 / (30 + row.bg_age_days)),
            0,
            np.inf,
        )[0]
        assert model.predict(frame)[i] == pytest.approx(1 - alive[i] + alive[i] * integrated)
    assert alive[0] == 1
    assert model.predict(frame)[0] > 0  # Alive is not a purchase guarantee.


def test_bg_likelihood_zero_repeat_closed_form():
    result = bg_log_likelihood(
        [0.7, 30, 1.5, 3], np.array([0.0]), np.array([0.0]), np.array([20.0])
    )
    assert result[0] == pytest.approx(0.7 * np.log(30 / 50))


def test_decisions_choose_n_without_outcomes_and_allow_no_contact():
    choice = decide([0.9, 0.5, 0.1], [100, 100, 100], ["A", "B", "C"])
    assert choice["optimal_n"] == 1  # zero marginal gain does not justify another contact.
    assert choice["predicted_profit"] == pytest.approx(4)
    assert choice["contact"].tolist() == [True, False, False]
    assert outcome_profit([1, 1, 1], [100] * 3, choice["contact"]).sum() == 5
    assert decide([0.5], [0], ["A"])["optimal_n"] == 0
    with pytest.raises(ValueError):
        decide([1.1], [100], ["A"])


def test_decision_ties_and_eligibility():
    choice = decide([0.9, 0.9], [100, 100], ["B", "A"], eligible=[False, True])
    assert choice["order"].tolist() == [1]


def test_weighted_metrics_match_sklearn_including_probability_ties():
    frame = pd.DataFrame(
        {
            "customer_id": list("ABCDE"),
            "cutoff": ["T"] * 5,
            "churn": [1, 0, 1, 0, 1],
            "probability": [0.8, 0.8, 0.4, 0.3, 0.1],
            "profit": [2, -5, 0, 0, 0],
        }
    )
    weights = np.array([2, 1, 0, 3, 1])
    metrics = Metrics(frame).calculate(weights)
    assert metrics["pr_auc"] == pytest.approx(
        average_precision_score(frame.churn, frame.probability, sample_weight=weights)
    )
    assert metrics["roc_auc"] == pytest.approx(
        roc_auc_score(frame.churn, frame.probability, sample_weight=weights)
    )


def test_cluster_bootstrap_pairs_identical_policies_exactly():
    frame = pd.DataFrame(
        {
            "customer_id": ["A", "B", "A", "B"],
            "cutoff": ["T", "T", "U", "U"],
            "churn": [1, 0, 1, 0],
            "probability": [0.8, 0.2, 0.7, 0.3],
            "profit": [10, -5, 10, -5],
            "contact": [True] * 4,
            "predicted_gain": [3] * 4,
        }
    )
    both = pd.concat([frame.assign(method="logistic"), frame.assign(method="recency")])
    result = summarize(both, draws=30)
    diff = result["groups"]["pooled"]["comparisons"]["logistic"]["recency"]
    assert diff["ci95"] == [0, 0]
    assert result["bootstrap_unit"] == "customer"


def test_rfm_empty_segments_use_training_base_rate():
    frame = pd.DataFrame(
        {
            "recency_days": [1, 2, 3],
            "frequency_365": [1, 2, 3],
            "monetary_365": [1, 2, 3],
            "churn": [1, 0, 0],
        }
    )
    model = RFM().fit(frame)
    assert model.predict(
        pd.DataFrame({"recency_days": [100], "frequency_365": [0], "monetary_365": [0]})
    )[0] == pytest.approx(1 / 3)


def test_calibration_with_no_forward_history_is_explicit():
    calibrator, name, reason = choose_calibration(pd.DataFrame())
    assert calibrator is None and name == "native" and reason
