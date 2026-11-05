"""Prediction-only contact selection and outcome-based hypothetical policy value."""

import numpy as np


def decide(probability, value, customer_id, *, save_rate=0.10, offer_cost=5.0, eligible=None):
    p, v = np.asarray(probability, float), np.asarray(value, float)
    if p.shape != v.shape or p.ndim != 1 or len(customer_id) != len(p):
        raise ValueError("Mismatched decision vectors")
    if not (np.isfinite(p).all() and np.isfinite(v).all()):
        raise ValueError("Nonfinite decision inputs")
    if ((p < 0) | (p > 1) | (v < 0)).any() or not 0 <= save_rate <= 1 or offer_cost < 0:
        raise ValueError("Invalid probability, value or cost")
    eligible = np.ones(len(p), bool) if eligible is None else np.asarray(eligible, bool)
    gain = p * save_rate * v - offer_cost
    order = np.lexsort((np.asarray(customer_id, str), -gain))
    order = order[eligible[order]]
    curve = np.r_[0.0, np.cumsum(gain[order])]
    optimal_n = int(np.argmax(curve))
    contact = np.zeros(len(p), bool)
    contact[order[:optimal_n]] = True
    return {
        "contact": contact,
        "gain": gain,
        "order": order,
        "curve": curve,
        "optimal_n": optimal_n,
        "predicted_profit": float(curve[optimal_n]),
    }


def outcome_profit(churn, value, contact, *, save_rate=0.10, offer_cost=5.0):
    return np.asarray(contact, bool) * (
        np.asarray(churn) * save_rate * np.asarray(value) - offer_cost
    )
