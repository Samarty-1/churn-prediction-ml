# Model card

ML superiority not established: lightgbm versus bgnbd, development profit-proxy difference GBP -7,316.42 (95% CI -8,413.80 to -6,322.93).

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

Development results only; the holdout remains sealed. Candidate: lightgbm. Main comparator: bgnbd.
Paired difference: GBP -7,316.42; 95% CI
[-8,413.80, -6,322.93].
Complete metrics with customer-bootstrap CIs:

| Method | PR-AUC [95% CI] | ROC-AUC [95% CI] | Brier [95% CI] |
|---|---:|---:|---:|
| bgnbd | 0.817 [0.807, 0.826] | 0.757 [0.747, 0.768] | 0.194 [0.191, 0.198] |
| constant | 0.631 [0.619, 0.642] | 0.487 [0.480, 0.494] | 0.248 [0.247, 0.248] |
| lightgbm | 0.788 [0.779, 0.798] | 0.718 [0.708, 0.729] | 0.211 [0.208, 0.215] |
| logistic | 0.761 [0.751, 0.772] | 0.673 [0.663, 0.683] | 0.227 [0.224, 0.231] |
| recency | 0.768 [0.758, 0.779] | 0.659 [0.650, 0.668] | 0.223 [0.221, 0.225] |
| rfm | 0.786 [0.776, 0.796] | 0.712 [0.702, 0.722] | 0.209 [0.206, 0.213] |

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
