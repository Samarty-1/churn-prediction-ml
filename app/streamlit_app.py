"""Read-only scenario explorer; never fits models or unseals holdouts."""

import json
import os
from pathlib import Path

import pandas as pd
import streamlit as st

from churn.decision import decide

ROOT = Path(os.environ.get("CHURN_APP_ROOT", Path(__file__).resolve().parents[1]))
st.set_page_config(page_title="Retail retention decisions", layout="wide")
st.title("Who should receive a retention offer?")
st.caption("Historical gift-wholesaler data. A decision scenario, not measured treatment uplift.")
summary_path = ROOT / "results/development_evaluation.json"
if not summary_path.exists():
    st.info("Run the development evaluation to prepare the explorer.")
    st.stop()
summary = json.loads(summary_path.read_text())
phases = ["development"]
receipt_path = ROOT / "results/holdout_receipt.json"
if receipt_path.exists() and json.loads(receipt_path.read_text()).get("status") == "complete":
    phases.append("holdout")
phase = st.selectbox("Evaluation period", phases)
path = ROOT / f"data/predictions/{phase}_explained.parquet"
if not path.exists():
    st.info("Generate customer explanations to prepare this evaluation period.")
    st.stop()
data = pd.read_parquet(path)
cutoff = st.selectbox("Cutoff", sorted(data.cutoff.unique()))
save_rate = st.slider("Assumed save rate", 0.0, 0.50, 0.10, 0.01)
cost = st.slider("Offer cost per contact (GBP)", 0.0, 30.0, 5.0, 0.50)
frame = data[data.cutoff == cutoff].copy().reset_index(drop=True)
decision = decide(
    frame.probability,
    frame.customer_value,
    frame.customer_id,
    save_rate=save_rate,
    offer_cost=cost,
    eligible=frame.policy_eligible,
)
left, right = st.columns(2)
left.metric("Optimal contacts", decision["optimal_n"])
right.metric("Predicted hypothetical profit", f"GBP {decision['predicted_profit']:,.2f}")
st.line_chart(pd.DataFrame({"Predicted profit (GBP)": decision["curve"]}).rename_axis("Contacts"))
st.write(
    f"Model: **{summary['champion']}**. Value is trailing net product margin, floored at zero."
)
st.warning(
    "Save rate is an assumption. There are no retention treatments in these data, "
    "so real uplift is unknown."
)
frame["recommended_contact"] = decision["contact"]
frame["expected_gain_gbp"] = decision["gain"]
frame = frame.sort_values(["probability", "customer_id"], ascending=[False, True])
st.subheader("Ranked customer risk and reasons")
st.caption(
    "SHAP reasons explain the model's uncalibrated log odds. "
    "Positive contributions increase risk; they are not causes."
)
st.dataframe(
    frame[
        [
            "customer_id",
            "probability",
            "customer_value",
            "recommended_contact",
            "expected_gain_gbp",
            "reasons",
        ]
    ],
    hide_index=True,
    width="stretch",
)
st.caption(
    "Monthly outcome windows overlap. Pooled results are historical campaign replays, "
    "not additive quarterly revenue."
)
