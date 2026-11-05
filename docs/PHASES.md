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

Current code implements only Phase 1. No labels or evaluation snapshots exist;
no holdout results have been computed. Raw and staged invoices include the full
source date range for cleaning validation. The evaluation access guard will be
implemented before any cutoff-level labels or models are created.

Before modelling, resolve the truncated portions of the task in the preregistration:
monthly cutoff anchor, success criterion, cost assumptions and value horizon.
Training labels must have matured by each test cutoff (a past cutoff alone is
insufficient when its outcome window extends into the test period).

Future output conventions: `results/` for machine-readable results and
`reports/figures/` for plots. A pipeline command must never bypass approval gates.
