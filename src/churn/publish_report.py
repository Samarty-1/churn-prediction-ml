"""Generate public prose and tables exclusively from recorded experiment artifacts."""

import json


def number(value, places=3):
    return "unavailable" if value is None else f"{value:,.{places}f}"


def measured(metric, places=3):
    lo, hi = metric["ci95"]
    return f"{number(metric['value'], places)} [{number(lo, places)}, {number(hi, places)}]"


def render_results(root):
    development = json.loads((root / "results/development_evaluation.json").read_text())
    phase = "holdout" if (root / "results/holdout_evaluation.json").exists() else "development"
    result = json.loads((root / f"results/{phase}_evaluation.json").read_text())
    cleaning = json.loads((root / "results/cleaning_summary.json").read_text())
    snapshots = json.loads((root / "results/development_summary.json").read_text())
    placebo = json.loads((root / "results/placebo_evaluation.json").read_text())
    pooled = result["groups"]["pooled"]
    champion = development["champion"]
    best = max(
        ("recency", "rfm", "bgnbd"),
        key=lambda m: pooled["methods"][m]["metrics"]["profit"]["value"],
    )
    diff = pooled["comparisons"][champion][best]
    headline = (
        "ML superiority established" if result.get("success") else "ML superiority not established"
    )
    headline += (
        f": {champion} versus {best}, {phase} profit-proxy difference "
        f"GBP {number(diff['difference_gbp'], 2)} "
        f"(95% CI {number(diff['ci95'][0], 2)} to {number(diff['ci95'][1], 2)})."
    )
    table, ranking = [], []
    for method, record in pooled["methods"].items():
        m = record["metrics"]
        table.append(
            f"| {method} | {number(m['pr_auc']['value'])} | {number(m['roc_auc']['value'])} | "
            f"{number(m['brier']['value'])} | {measured(m['profit'], 2)} |"
        )
        ranking.append(
            f"| {method} | {measured(m['precision_top_10'])} | {measured(m['lift_top_10'])} | "
            f"{measured(m['precision_top_20'])} | {measured(m['lift_top_20'])} |"
        )
    cleaning_table = "\n".join(
        f"| {r['step']} | {r['rows']:,} | {r['signed_amount_gbp']} |" for r in cleaning["waterfall"]
    )
    paired = "\n".join(
        f"| {b} | {number(v['difference_gbp'], 2)} | "
        f"[{number(v['ci95'][0], 2)}, {number(v['ci95'][1], 2)}] | "
        f"[{number(v['ci_familywise95'][0], 2)}, {number(v['ci_familywise95'][1], 2)}] |"
        for b, v in pooled["comparisons"][champion].items()
        if b != "constant"
    )
    pm = placebo["groups"]["pooled"]["methods"][champion]["metrics"]
    pp = placebo["groups"]["pooled"]["comparisons"][champion]["constant"]
    assumptions = snapshots["primary_assumptions"]
    cutoff_table = "\n".join(
        f"| {t} | {g['methods'][champion]['rows']:,} | "
        f"{number(g['methods'][champion]['metrics']['base_rate']['value'], 6)} |"
        for t, g in result["groups"].items()
        if t != "pooled"
    )
    status = (
        "The approved holdout was opened once after a code/data/model freeze. No tuning followed."
        if phase == "holdout"
        else "Development results only; the holdout remains sealed."
    )
    text = f"""# churn-prediction-ml

**{headline}**

{status} The reported values are hypothetical retention policy values, not measured
treatment profit. The simple customer-base model is a serious comparator; an ML
win is not assumed. Non-significance does not prove equivalence.

## Why the old project was circular

The original generated customer labels from a hand-written logistic formula, then
trained models to rediscover it. The winning model and contract-risk insight were
built into the data generator. That version is preserved as `v0-synthetic`.

## Real data, reconciled

[UCI Online Retail II](https://doi.org/10.24432/C5CG6D) supplies
{cleaning["raw_rows"]:,} invoice lines. The identified sales population contains
{cleaning["customers"]:,} customers and {cleaning["orders"]:,} invoices.
Each raw row appears exactly once in this cleaning waterfall; the final row is retained.

| Disposition | Rows | Exact signed GBP |
|---|---:|---:|
{cleaning_table}

Missing IDs remove GBP {cleaning["missing_customer_sale_revenue_gbp"]} of otherwise
valid gross product sales. Cancellations are retained separately for historical
features; they are never counted as purchases. Source prices retain their precision:
{cleaning["positive_price_rounds_to_zero_rows"]} lines worth GBP
{cleaning["positive_price_rounds_to_zero_amount_gbp"]} would become zero-price rows
if rounded to pennies first. [Rules and provenance](docs/DATA.md).

## Evaluation fixed before modelling

[Preregistration](docs/PREREGISTRATION.md) defines monthly midnight cutoffs on the
ninth, a trailing-year eligible population, and zero purchases in the following
90 days as the label. Features use only transactions at or before the cutoff.
Deleting all future sales and cancellations left all features identical at every
development cutoff. Category breadth is a fixed keyword proxy, not a genuine taxonomy.

There are {len(snapshots["cutoffs"])} development cutoffs and
{sum(r["role"] == "backtest" for r in snapshots["cutoffs"])} evaluated rolling origins.
Training labels must mature before each validation/test cutoff, including inner CV
and calibration. Hyperparameters, Platt/isotonic calibration and recency thresholds
are selected on training history only. The final models use only development
labels matured before the first held-out cutoff; no earlier holdout month trains a later one.

The registered held-out dates are {", ".join(snapshots["sealed_cutoffs"])}.
The guard rejects access outside the one-use audited session. It is a procedural
evaluation seal over public data, not protection against deliberate source-code edits.

| {phase.title()} cutoff | Eligible customers | Churn base rate |
|---|---:|---:|
{cutoff_table}

## Models versus baselines

PR-AUC means average precision. Profit brackets are customer-bootstrap 95% CIs;
all per-cutoff and pooled metric CIs are in [the result file](results/{phase}_evaluation.json).

| Method | PR-AUC | ROC-AUC | Brier | Profit proxy GBP [95% CI] |
|---|---:|---:|---:|---:|
{chr(10).join(table)}

The selected ML candidate is **{champion}**. Paired comparisons use the same sampled
customers across methods; every sampled customer carries all their cutoff rows.
There are {result["bootstrap_draws"]:,} bootstrap draws. The three baseline comparisons
also receive a familywise-95% correction. Every adjusted lower bound must exceed
zero to establish the preregistered ML superiority claim.

| Baseline | ML minus baseline GBP | Paired 95% CI | Familywise-95% interval |
|---|---:|---:|---:|
{paired}

| Method | Precision top 10% [CI] | Lift top 10% [CI] | Precision top 20% [CI] | Lift top 20% [CI] |
|---|---:|---:|---:|---:|
{chr(10).join(ranking)}

![Probability reliability](reports/figures/{phase}_reliability.png)

BG/NBD uses a verified conditional probability of zero purchases in the prediction
window. Probability alive is also retained in local predictions; it is not
interchangeable with that churn probability. All methods share the same value proxy.
Every candidate, calibration attempt, optimizer warning and failed fit is retained
in [the trial ledger](docs/TRIALS.md). Development model selection is optimistic.

## Who gets an offer?

Assumptions: save rate {assumptions["save_rate"]:.0%}, cost GBP
{assumptions["offer_cost_gbp"]} per contact, and margin {assumptions["margin"]:.0%} of
trailing {assumptions["value_window_days"]}-day sales net of observed product cancellations,
floored at zero. Rank by `P(churn) × save_rate × value − offer_cost`; choose the
profit-maximizing prefix, allowing no contacts. Risk-ranking metrics are separate
from value-aware contact selection. Do not select contacts using test outcomes.

For evaluation, freeze the contacts and replace predicted churn with observed
churn in the payoff calculation. Comparing models' own predicted profits would
reward overconfidence. This outcome-based profit proxy is still conditional on
assumed retention effectiveness, not measured uplift.

![Profit curve](reports/figures/{phase}_profit_curve.png)
![Sensitivity](reports/figures/{phase}_sensitivity.png)

The full [sensitivity grid](results/{phase}_sensitivity.json) varies save rate and
offer cost for every method. It cannot replace the preregistered primary cell.

## Placebo and explanations

The single within-cutoff label shuffle produced {champion} PR-AUC
{measured(pm["pr_auc"])}, versus a base rate of {number(pm["base_rate"]["value"])}.
Top-decile lift was {measured(pm["lift_top_10"])}; the predictive advantage vanished.
Its profit-proxy difference versus constant risk was GBP {number(pp["difference_gbp"], 2)}
(95% CI {number(pp["ci95"][0], 2)} to {number(pp["ci95"][1], 2)}).
The placebo was not repeatedly reshuffled to obtain a desired answer.

![SHAP global importance](reports/figures/{phase}_shap.png)

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
"""
    card = f"""# Model card

{headline}

## Intended use

Research comparison of next-window purchase inactivity and hypothetical retention
targeting. Not a deployed churn service. Recommended business use is experiment
design; no individual should be contacted solely on this retrospective study.

## Data and population

UCI Online Retail II, a historical UK gift wholesaler with many B2B customers.
Cleaning retained {cleaning["customers"]:,} identified customers. Eligible at a cutoff
means an identified product sale in the prior year. Anonymous transactions are
excluded. First observed purchase is not necessarily acquisition.

## Evaluation

{status} Candidate: {champion}. Main comparator: {best}.
Paired difference: GBP {number(diff["difference_gbp"], 2)}; 95% CI
[{number(diff["ci95"][0], 2)}, {number(diff["ci95"][1], 2)}].
Complete metrics with customer-bootstrap CIs:

| Method | PR-AUC [95% CI] | ROC-AUC [95% CI] | Brier [95% CI] |
|---|---:|---:|---:|
"""
    for method, record in pooled["methods"].items():
        m = record["metrics"]
        card += f"| {method} | {measured(m['pr_auc'])} | {measured(m['roc_auc'])} | {measured(m['brier'])} |\n"
    card += """
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
"""
    return text, card


def write_public_report(root):
    readme, card = render_results(root)
    (root / "README.md").write_text(readme, encoding="utf-8")
    (root / "docs/MODEL_CARD.md").write_text(card, encoding="utf-8")


def write_ledger(root):
    records = [
        json.loads(line) for line in (root / "results/trials.jsonl").read_text().splitlines()
    ]
    lines = [
        "# Trial ledger",
        "",
        "Generated from the append-only [full audit](../results/trials.jsonl).",
        "Every fit, optimizer start, warning, candidate, calibration and threshold is retained there.",
        "No unsuccessful result is removed. Development selection is optimistic; the holdout is confirmatory.",
        "",
        "| Audit line | Run | Event | Method | Context | Configuration / result |",
        "|---:|---|---|---|---|---|",
    ]
    for index, record in enumerate(records, 1):
        detail = {
            k: v
            for k, v in record.items()
            if k not in ("run", "event", "method", "context", "train_cutoffs", "optimizer")
        }
        lines.append(
            f"| {index} | {record['run']} | {record['event']} | {record['method']} | "
            f"{record.get('context', record.get('cutoff', ''))} | "
            f"`{json.dumps(detail, sort_keys=True).replace('|', '/').replace('`', '')}` |"
        )
    (root / "docs/TRIALS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
