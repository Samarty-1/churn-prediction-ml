# Model card

ML superiority not established: lightgbm versus bgnbd, holdout profit-proxy difference GBP -11.21 (95% CI -319.00 to 293.59).

## Intended use

Research comparison of next-window purchase inactivity and hypothetical retention
targeting. Not a deployed churn service. Recommended business use is experiment
design; no individual should be contacted solely on this retrospective study.

## Data and population

UCI Online Retail II, a historical UK gift wholesaler with many B2B customers.
Cleaning retained 5,852 identified customers. Eligible at a cutoff
means an identified product sale in the prior year. Anonymous transactions are
excluded. First observed purchase is not necessarily acquisition.

## Evaluation

The approved holdout was opened once after a code/data/model freeze. No tuning followed. Candidate: lightgbm. Main comparator: bgnbd.
Paired difference: GBP -11.21; 95% CI
[-319.00, 293.59].
Complete metrics with customer-bootstrap CIs:

| Method | PR-AUC [95% CI] | ROC-AUC [95% CI] | Brier [95% CI] |
|---|---:|---:|---:|
| bgnbd | 0.774 [0.757, 0.790] | 0.781 [0.769, 0.793] | 0.194 [0.188, 0.199] |
| constant | 0.550 [0.537, 0.564] | 0.500 [0.500, 0.500] | 0.248 [0.246, 0.250] |
| lightgbm | 0.784 [0.770, 0.799] | 0.791 [0.780, 0.802] | 0.197 [0.192, 0.202] |
| logistic | 0.757 [0.742, 0.773] | 0.774 [0.762, 0.786] | 0.233 [0.226, 0.239] |
| recency | 0.724 [0.707, 0.741] | 0.721 [0.709, 0.733] | 0.221 [0.216, 0.226] |
| rfm | 0.750 [0.735, 0.764] | 0.768 [0.756, 0.779] | 0.219 [0.213, 0.225] |

## Failures and limitations

Gift seasonality, B2B buying cycles, historical drift, incomplete acquisition
history, customer-ID omissions, bulk reversals and unmeasured margin can invalidate
the policy. Fixed keyword categories may misclassify products. Calibrators have
limited early forward history; fallbacks and optimizer outcomes are logged.
The same buyer may appear across overlapping windows; reported replay profit is
not a promise of additive campaign revenue. Customer-bootstrap CIs do not quantify
treatment uncertainty or distribution shift. The data has no intervention; save
rate and offer cost are assumptions and causal uplift is unknown.

SHAP explains raw model log odds, not calibrated treatment benefit. Risk ranking
is not equivalent to value-aware contact ranking. Use a randomized retention test,
recent data and monitoring before deployment. Do not reuse these customer IDs for
marketing outreach. No fairness or geographic generalization claim is made.

## Governance

Preregistration and trial ledger precede the sealed evaluation. Code, models,
dependencies, source hashes and approval are recorded in the freeze/receipt.
No post-holdout model selection or retuning is permitted. Data and binaries are
ignored by Git. The app performs scenario calculations over saved predictions.
