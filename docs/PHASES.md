# Rebuild checkpoints

The original synthetic project is preserved by the local tag `v0-synthetic`.
All rebuild work is on `rebuild-real-data`; nothing is pushed without authorization.

- Phase 1: download, Parquet landing, SQL staging, data contracts and cleaning tests.
  Stop and show the cleaning summary.
- Phase 2: labels, features, deletion-of-future leakage test, preregistration and holdout guard.
  Stop for approval before modelling.
- Phase 3: rolling-origin development evaluation, baselines, models and trial ledger.
  Stop with results. Holdout remains sealed.
- Phase 4: explicit approval to unseal once; report the frozen evaluation regardless of result.
- Phase 5: decision interface, app, model card, generated README and CI.

Status (2026-11-06): Phases 1-3 are complete. The development backtest, baselines,
placebo, explanations and figures exist, and the trial ledger is generated from
`results/trials.jsonl`. One-time unsealing is approved (`docs/HOLDOUT_APPROVAL.json`)
but has not been used: no freeze manifest, holdout snapshots or holdout fits exist.
Commands: `python -m churn backtest` reruns Phase 3, `python -m churn report`
regenerates the README, model card and ledger, and `python -m churn holdout`
performs the single Phase 4 evaluation. `run-all` never opens the holdout.

Phase 2 notes, kept for the record: development snapshots and temporal
invariance audits are available.
The access guard blocks holdout feature, label and snapshot requests before data
access; no unseal option exists. Raw and staged invoices retain the full source
date range for cleaning. This is an evaluation guard, not raw-file encryption.

The previously truncated task details are specified in PREREGISTRATION.md.
The user approved the primary profit assumptions during Phase 2. The complete
preregistration still requires approval before modelling. Training label windows
must mature by each test cutoff, including during inner selection and calibration.

Future output conventions: `results/` for machine-readable results and
`reports/figures/` for plots. A pipeline command must never bypass approval gates.
