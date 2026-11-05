# Preregistration: retail inactivity and retention targeting

Status: written before any model fitting or development metrics. Phase 2 review
is required before Phase 3. Profit assumptions below were explicitly approved
by the user in this session. Any later change requires a dated amendment and
trial-ledger entry; no changes after holdout unsealing.

## Question, population and time

Predict zero purchases during the next 90 days, not permanent contractual churn.
Source: UCI Online Retail II; staging rules and limitations are in DATA.md.
Monthly cutoffs are the ninth at 00:00:00 in the dataset's naive local clock,
2010-06-09 through 2011-09-09 inclusive (16 cutoffs). This anchors the requested
last cutoff and gives the earliest cutoff at least six calendar months of history.
No timezone or intraday timestamp is inferred from the source.

Eligible customers have at least one identified positive product sale in
(T - 365 days, T]. Churn = 1 exactly when no such sale occurs in (T, T + 90 days].
A purchase exactly at T belongs to history; exactly at T + 90 days prevents
churn. Require documented observation coverage through the entire outcome window.
Zero-price transactions do not count. The 17 positive-price fractional-penny
lines identified in staging do count under the frozen positive-price rule.
Do not silently reclassify these using later model performance.

July, August and September 2011 are the last three cutoffs and the sealed holdout.
Do not compute their populations, features, labels, base rates or predictions
before explicit unsealing approval. Full raw data was inspected for cleaning;
this is a procedural evaluation seal, not secrecy of the public source data.
The code rejects every non-development cutoff before querying data or reading
a snapshot. There is no unseal CLI or boolean bypass in Phase 2. Phase 4 must add
an explicit one-use, audited evaluation transaction after approval and freeze
code, dependencies, source hashes, parameters, policy and preregistration first.

Development cutoffs end 2011-06-09. Report populations and base rates for each;
report holdout base rates only at the one approved evaluation. Repeated customer
snapshots are allowed: the use case forecasts existing customers, not unseen IDs.
Customer ID, cutoff, label-window end and churn are never model predictors.

## Features, all observed at or before T

Feature code filters both sales and cancellations to T before aggregation.
No full-data quantiles, product dictionary, imputation, scaling, country pooling
or outcome-informed transformation is allowed. Fixed keyword categories below
are declared here before outcome inspection; genuine product categories are absent.

- Trailing 365-day recency (fractional days), distinct invoice frequency, monetary
  sales, distinct purchase days; counts use (T - window, T].
- Mean and sample standard deviation of gaps between distinct purchase dates in
  that year. Multiple same-day invoices represent one purchase occasion for gaps
  and BG/NBD. Mean is null with fewer than two dates; standard deviation is null
  with fewer than three dates. Overdue ratio = recency / mean gap, null if undefined.
- Sales and invoice counts in the latest 90 days and preceding 90 days, their
  differences and ratios. A zero prior denominator gives null, not infinity.
- Trailing-year product cancellation invoice count divided by sale plus cancellation
  invoice counts; cancellation absolute amount / gross sale amount is a separate
  unbounded ratio. No future matching or netting against original orders.
- Mean units and lines per sale invoice; product breadth and heuristic category
  breadth in the trailing year. Keywords, first match wins: CHRISTMAS/XMAS;
  MUG/CUP/PLATE/BOWL; CANDLE/CUSHION/LANTERN; NECKLACE/BRACELET/EARRING;
  BAG/PURSE; PEN/PENCIL/NOTEBOOK; TOY/GAME/DOLL; otherwise OTHER. Case-insensitive
  substring rules are a coarse description proxy, not a validated taxonomy.
- Observed tenure since first sale, latest sale country (ties: invoice, stock code,
  country lexically), and calendar days until Christmas (zero on Christmas Day).
- First sale in the source's opening month is flagged as potentially left-censored.
  Observed acquisition is not true acquisition. No invented pre-source history.
- BG/NBD inputs from all history through T: repeat purchase-day count, days from
  first to last purchase date, days from first purchase date to T.
- Trailing 90-day sale and absolute product cancellation amounts, and customer
  value = max(0, 0.30 * (sales - cancellations)). Margin and future value are proxies.

The feature allowlist is explicit in features.py. Missing-value indicators and
training-fitted median imputation are used for numeric ML inputs. Scale numeric
inputs for logistic regression. Country one-hot encoding is fitted only on each
training fold, with unseen values ignored. No customer ID encoding.

Leakage acceptance test: deleting every sale and cancellation after T must leave
the complete sorted feature table identical. Test on an adversarial hand-built
fixture and on each development cutoff in the real dataset. Include history and
outcome boundary tests, missing gap tests and independently calculated feature values.

## Rolling evaluation and selection

For a test cutoff T, only snapshots with cutoff + 90 days <= T can train a model.
This maturation purge applies at every inner split and calibration split too.
Merely requiring a training cutoff < T leaks unresolved future outcomes.
Use expanding origins, never random splits. An origin needs at least three
mature training cutoffs; earlier cutoffs are warm-up and are still reported.
The registered development test origins are 2010-11-09 through 2011-06-09.

At each outer origin, inner validation uses matured expanding origins within the
training cutoffs, with at least one mature training cutoff per inner fold.
Where no inner fold exists, use the registered first configuration and Platt
calibration if enough forward predictions exist; otherwise use native probabilities
and flag calibration unavailable. Never use outer outcomes to fit a calibrator.
Select hyperparameters by pooled inner average precision; ties use list order.

Calibration uses chronological forward predictions within training data. Choose
between Platt and isotonic using later forward folds: fit on earlier matured
out-of-fold predictions, assess Brier on later folds, and refit the chosen map
on all available forward predictions. Isotonic requires at least 1,000 calibration
rows and both classes; Platt requires at least 100 and both classes. Without an
eligible calibration validation split, prefer Platt if eligible, otherwise native
probabilities with an explicit warning. Report which fallback each origin used.

One full feature set, no feature search in the primary protocol. Registered models:
- Logistic regression: L2, C in [0.01, 0.1, 1.0], no class weighting, max_iter 2000.
- LightGBM: binary objective, learning_rate 0.05, 200 trees; (num_leaves,
  min_child_samples) in [(7, 50), (15, 50), (15, 100), (31, 100)]; lambda_l2=1,
  no class weighting, no early stopping on outer data. Fix seed 20261105 and
  deterministic CPU settings. Exact modelling dependencies are pinned before fitting.

Baselines (identical populations, maturity rules and value assumptions):
- Recency: score recency, threshold k in [30, 60, 90, 120, 180, 270] days selected
  on inner training validation policy profit. For continuous ranking/calibration,
  fit the calibration map to recency; the binary flag remains separately reported.
- RFM: training-fitted terciles of recency, invoice frequency and monetary sales.
  Segment risk = (churn count + 1) / (segment count + 2), training data only;
  empty segments use the training population base rate. Boundary ties use the
  lower bin, not row order. Calibration follows the same training-only procedure.
- BG/NBD: fit the original likelihood with scipy, positive log-parameterization,
  deterministic multi-start optimization; check convergence and report failed fits.
  Use one customer history at the latest available training snapshot, not repeated
  customers as independent likelihood terms. Report probability alive separately.
  Alive is not a 90-day purchase probability. Use the model's conditional probability
  of zero purchases in 90 days for churn scoring, verified against numerical
  integration or simulation; calibration follows the same forward-only procedure.
  Use the common trailing-margin customer-value proxy; Gamma-Gamma is not a second
  hidden value model search. No substitution of 1 - alive for 90-day churn.
- A constant training-base-rate predictor and contact-nobody policy are diagnostic
  reference points, not replacements for the three required baselines.

Log every hyperparameter, calibration candidate, failure and optional amendment
in TRIALS.md with result file paths. Select one ML champion using pooled development
policy-profit proxy, then average precision, then logistic regression on a tie.
Development selection is optimistic; only the sealed evaluation is confirmatory.

At unsealing, fit one final frozen model per method using development snapshots
whose labels matured by 2011-07-09. Do not train on any holdout label, including
earlier holdout months. Apply frozen models and policies to all three holdouts.

## Decisions and profit: approved assumptions

Primary save_rate = 0.10; offer_cost = GBP 5 for each contacted customer regardless
of response; margin = 0.30; customer value is trailing 90-day net product margin,
floored at zero as specified above. No additional discount, campaign capacity or
fixed campaign cost is assumed. These are explicit hypothetical business inputs.

For each customer g = P(churn) * save_rate * value - offer_cost. Rank descending
by g, ties by customer ID, and choose the prefix with maximal cumulative expected
profit, allowing N=0 and preferring smaller N on ties. Recency's chosen flag limits
its eligible contact set. Show the entire profit-vs-N curve, plus risk-ranked
top-10%/20% classification metrics separately; value ranking and risk ranking differ.

Do NOT compare models using the sum of their own predicted profits as evidence of
superiority: an overconfident model can win that circular comparison. The primary
evaluation uses the frozen contact decisions and observed churn Y:
sum(contact * (Y * save_rate * value - offer_cost)), reported per cutoff and pooled,
with paired between-policy differences. This is an outcome-based profit proxy,
not observed treatment profit. Report predicted profit beside the proxy to expose
miscalibration. Do not choose N using test outcomes.

Sensitivity grid: save_rate in [0.02, 0.05, 0.10, 0.20, 0.30], offer_cost in
[1, 2, 5, 10, 20] GBP, keeping the margin proxy fixed; each cell reoptimizes N using
predictions only. It is descriptive and cannot replace the primary assumption cell.
No treatment or offer exists in this dataset, so actual uplift and causal profit
are unknown. A randomized retention trial is required before deployment.

## Metrics, uncertainty and success criterion

Per origin and pooled: average precision (the registered PR-AUC definition),
ROC-AUC, Brier, precision and lift at ceil(0.10*n) and ceil(0.20*n), plus population
and churn base rate. ROC-AUC is unavailable for a single-class sample; record that
explicitly. Use deterministic customer-ID tie-breaking. Reliability curves use
ten equal-width probability bins, displaying counts and omitting empty bins.

Bootstrap unique customers, not rows, with replacement 2,000 times, seed 20261105;
carry each sampled customer's complete cutoff history and the same weights across
all compared policies. Decisions, models and N are frozen before resampling.
Report percentile 95% CIs. This captures customer sampling uncertainty, not new
retailers, time-regime changes, treatment uncertainty or model-selection uncertainty.

Confirmatory success: the selected ML policy must exceed EACH of recency, RFM and
BG/NBD on pooled holdout outcome-based profit proxy, with positive paired lower
confidence bounds. Alongside ordinary 95% intervals, use Bonferroni-adjusted
98.333333% two-sided intervals for each of the three comparisons (familywise 95%).
All three adjusted lower bounds must exceed zero, and ML must have positive profit
relative to contact nobody. Otherwise declare superiority unproven. If a simple
rule matches or wins, that is the README headline. Do not equate non-significance
with proven equivalence. Report absolute GBP totals and per-customer-cutoff values.

Placebo: one registered run with seed 20261106 shuffles labels independently within
each development cutoff, refits the same selected ML configuration and calibration
procedure, and evaluates against shuffled test labels. Report metrics and paired
policy edge; the model should lose its signal. Do not repeatedly reshuffle until a
desired result appears. A suspicious remaining edge requires investigation and a
ledger entry before any holdout evaluation, not selective deletion of the result.

SHAP: training-only background, global and per-customer explanations of fitted
model scores; identify whether raw score or calibrated probability is explained.
SHAP describes model associations, not causes or retention treatment effects.

## Known limitations and references

Gift wholesaler, B2B-heavy population, historical period and Christmas demand;
left-censored acquisition, many anonymous buyers, billing reversals and uncertain
customer value. A 90-day nonpurchase event can be normal seasonal behavior.
Feature deletion tests establish temporal invariance of feature construction,
not absence of every possible source of bias.

- Fader, Hardie & Lee, [BG/NBD original paper](https://www.brucehardie.com/papers/018/fader_et_al_mksc_05.pdf).
- scikit-learn, [calibration documentation](https://scikit-learn.org/stable/modules/calibration.html).
