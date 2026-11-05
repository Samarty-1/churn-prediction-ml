# churn-prediction-ml

**ML superiority not established: lightgbm versus bgnbd, holdout profit-proxy difference GBP -11.21 (95% CI -319.00 to 293.59).**

The approved holdout was opened once after a code/data/model freeze. No tuning followed. The reported values are hypothetical retention policy values, not measured
treatment profit. The simple customer-base model is a serious comparator; an ML
win is not assumed. Non-significance does not prove equivalence.

## Why the old project was circular

The original generated customer labels from a hand-written logistic formula, then
trained models to rediscover it. The winning model and contract-risk insight were
built into the data generator. That version is preserved as `v0-synthetic`.

## Real data, reconciled

[UCI Online Retail II](https://doi.org/10.24432/C5CG6D) supplies
1,067,371 invoice lines. The identified sales population contains
5,852 customers and 36,594 invoices.
Each raw row appears exactly once in this cleaning waterfall; the final row is retained.

| Disposition | Rows | Exact signed GBP |
|---|---:|---:|
| sheet_overlap | 22,523 | 377488.450 |
| exact_duplicate | 11,812 | 54228.420 |
| bad_debt_adjustment | 6 | -147614.080 |
| non_product | 5,795 | 75748.711 |
| cancellation | 17,915 | -716462.570 |
| stock_adjustment | 5,963 | 0.000 |
| missing_customer | 226,761 | 2575278.900 |
| sale | 776,596 | 17068582.737 |

Missing IDs remove GBP 2575278.900 of otherwise
valid gross product sales. Cancellations are retained separately for historical
features; they are never counted as purchases. Source prices retain their precision:
17 lines worth GBP
0.017 would become zero-price rows
if rounded to pennies first. [Rules and provenance](docs/DATA.md).

## Evaluation fixed before modelling

[Preregistration](docs/PREREGISTRATION.md) defines monthly midnight cutoffs on the
ninth, a trailing-year eligible population, and zero purchases in the following
90 days as the label. Features use only transactions at or before the cutoff.
Deleting all future sales and cancellations left all features identical at every
development cutoff. Category breadth is a fixed keyword proxy, not a genuine taxonomy.

There are 13 development cutoffs and
8 evaluated rolling origins.
Training labels must mature before each validation/test cutoff, including inner CV
and calibration. Hyperparameters, Platt/isotonic calibration and recency thresholds
are selected on training history only. The final models use only development
labels matured before the first held-out cutoff; no earlier holdout month trains a later one.

The registered held-out dates are 2011-07-09, 2011-08-09, 2011-09-09.
The guard rejects access outside the one-use audited session. It is a procedural
evaluation seal over public data, not protection against deliberate source-code edits.

| Holdout cutoff | Eligible customers | Churn base rate |
|---|---:|---:|
| 2011-07-09 | 4,312 | 0.602505 |
| 2011-08-09 | 4,339 | 0.552892 |
| 2011-09-09 | 4,313 | 0.495015 |

## Models versus baselines

PR-AUC means average precision. Profit brackets are customer-bootstrap 95% CIs;
all per-cutoff and pooled metric CIs are in [the result file](results/holdout_evaluation.json).

| Method | PR-AUC | ROC-AUC | Brier | Profit proxy GBP [95% CI] |
|---|---:|---:|---:|---:|
| bgnbd | 0.774 | 0.781 | 0.194 | 7,692.31 [3,687.07, 13,438.79] |
| constant | 0.550 | 0.500 | 0.248 | 5,005.55 [924.23, 10,849.12] |
| lightgbm | 0.784 | 0.791 | 0.197 | 7,681.10 [3,661.88, 13,475.65] |
| logistic | 0.757 | 0.774 | 0.233 | 5,289.03 [1,219.60, 11,185.37] |
| recency | 0.724 | 0.721 | 0.221 | 4,032.96 [1,767.26, 7,046.24] |
| rfm | 0.750 | 0.768 | 0.219 | 5,308.71 [1,213.34, 11,131.67] |

The selected ML candidate is **lightgbm**. Paired comparisons use the same sampled
customers across methods; every sampled customer carries all their cutoff rows.
There are 2,000 bootstrap draws. The three baseline comparisons
also receive a familywise-95% correction. Every adjusted lower bound must exceed
zero to establish the preregistered ML superiority claim.

| Baseline | ML minus baseline GBP | Paired 95% CI | Familywise-95% interval |
|---|---:|---:|---:|
| recency | 3,648.14 | [1,520.73, 6,613.24] | [1,221.62, 7,370.91] |
| rfm | 2,372.39 | [1,999.23, 2,740.85] | [1,897.12, 2,830.79] |
| bgnbd | -11.21 | [-319.00, 293.59] | [-372.14, 383.56] |

| Method | Precision top 10% [CI] | Lift top 10% [CI] | Precision top 20% [CI] | Lift top 20% [CI] |
|---|---:|---:|---:|---:|
| bgnbd | 0.823 [0.793, 0.850] | 1.496 [1.439, 1.551] | 0.831 [0.810, 0.850] | 1.510 [1.466, 1.552] |
| constant | 0.524 [0.484, 0.565] | 0.952 [0.884, 1.023] | 0.535 [0.507, 0.563] | 0.973 [0.929, 1.019] |
| lightgbm | 0.839 [0.812, 0.863] | 1.525 [1.473, 1.574] | 0.831 [0.812, 0.849] | 1.511 [1.471, 1.552] |
| logistic | 0.800 [0.769, 0.828] | 1.454 [1.394, 1.507] | 0.807 [0.785, 0.827] | 1.467 [1.423, 1.510] |
| recency | 0.773 [0.742, 0.805] | 1.406 [1.346, 1.463] | 0.773 [0.750, 0.795] | 1.404 [1.360, 1.446] |
| rfm | 0.820 [0.791, 0.846] | 1.490 [1.435, 1.542] | 0.811 [0.791, 0.831] | 1.475 [1.433, 1.516] |

![Probability reliability](reports/figures/holdout_reliability.png)

BG/NBD uses a verified conditional probability of zero purchases in the prediction
window. Probability alive is also retained in local predictions; it is not
interchangeable with that churn probability. All methods share the same value proxy.
Every candidate, calibration attempt, optimizer warning and failed fit is retained
in [the trial ledger](docs/TRIALS.md). Development model selection is optimistic.

## Who gets an offer?

Assumptions: save rate 10%, cost GBP
5 per contact, and margin 30% of
trailing 90-day sales net of observed product cancellations,
floored at zero. Rank by `P(churn) × save_rate × value − offer_cost`; choose the
profit-maximizing prefix, allowing no contacts. Risk-ranking metrics are separate
from value-aware contact selection. Do not select contacts using test outcomes.

For evaluation, freeze the contacts and replace predicted churn with observed
churn in the payoff calculation. Comparing models' own predicted profits would
reward overconfidence. This outcome-based profit proxy is still conditional on
assumed retention effectiveness, not measured uplift.

![Profit curve](reports/figures/holdout_profit_curve.png)
![Sensitivity](reports/figures/holdout_sensitivity.png)

The full [sensitivity grid](results/holdout_sensitivity.json) varies save rate and
offer cost for every method. It cannot replace the preregistered primary cell.

## Placebo and explanations

The single within-cutoff label shuffle produced lightgbm PR-AUC
0.627 [0.620, 0.634], versus a base rate of 0.636.
Top-decile lift was 1.017 [0.993, 1.040]; the predictive advantage vanished.
Its profit-proxy difference versus constant risk was GBP -253.61
(95% CI -475.90 to -50.09).
The placebo was not repeatedly reshuffled to obtain a desired answer.

![SHAP global importance](reports/figures/holdout_shap.png)

SHAP explains uncalibrated model log odds with training-only background information.
It describes associations, not causes or offer responsiveness. Local per-customer
reasons appear in the Streamlit app, alongside risk, value and contact decisions.

## Limits that matter

- Historical UK gift wholesaler, many B2B buyers, strong seasonality and Christmas
  effects. A nonpurchase window is not permanent churn or a subscription cancellation.
- Anonymous buyers are excluded. Acquisition before the source begins is unknown.
  Exact repeated lines may include genuine purchases; cancellations lack original-order links.
- Billing reversals and extreme orders can distort trailing value. Margin and
  save rate are assumptions. **There are no treatment data; real uplift is unknown.**
- Monthly windows overlap. Pooled profits are sums of independent campaign replays,
  not an additive quarterly cash forecast. Repeated-offer fatigue is unmeasured.
- Customer bootstrap uncertainty does not cover regime shifts, new retailers,
  treatment effectiveness or development-selection optimism. Use a randomized
  retention trial before deploying any contact policy.

## Reproduce and explore

```powershell
py -3.11 -m venv .venv
.venv/Scripts/python.exe -m pip install -c requirements-lock.txt -e '.[dev]'
.venv/Scripts/python.exe -m churn run-all
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m ruff check .
.venv/Scripts/python.exe -m streamlit run app/streamlit_app.py
```

`run-all` builds missing development artifacts and reports. Once the holdout receipt
exists, it preserves the recorded one-time evaluation and refuses another unsealing.
Frozen model binaries and customer-level data are local, ignored artifacts; retain
them to reproduce the exact released app and holdout figures. A fresh clone can
rebuild development results, but cannot recover ignored holdout artifacts from Git.
The committed freeze manifests, aggregate results and receipt remain auditable.
The app reads results only; sliders never retrain models or open the seal.

CI runs lint, dependency checks and fixture tests without downloading UCI data.
The README and model card are generated from result files and tested for exact agreement.
See [model card](docs/MODEL_CARD.md), [freeze](results/freeze.json), and
[holdout receipt](results/holdout_receipt.json). No data or model binaries are committed.

Code: [MIT](LICENSE). Data: UCI CC BY 4.0.
