# Implementation notes recorded before Phase 3 fitting

The user approved Phase 3 and requested completion on 2026-11-06 (local time).
The original preregistration remains unchanged. These details resolve implementation
ambiguities rather than add model/feature searches:

- Raw recency is not a probability. When no forward calibration sample exists,
  its probability output uses training prevalence, while the threshold flag still
  selects customers by recency. This fallback is logged, not interpreted as calibration.
- The diagnostic constant predictor is never calibrated.
- Bootstrap ranking metrics condition on the original per-cutoff top-fraction
  membership, as profit conditions on frozen decisions. No bootstrap re-selection
  of contacts or model parameters occurs. Customer weights carry all their rows.
- The single placebo reuses each original outer fold's selected ML hyperparameters,
  while refitting on the shuffled training labels and recalibrating forward-only.
  It does not conduct a new hyperparameter search on shuffled outcomes.
- BG/NBD optimization uses three deterministic starts and positive parameters,
  with log-parameter bounds [-10, 15] to prevent numeric overflow. All starts and
  convergence messages are in the trial audit. Failed optimizers are never silently
  replaced by another baseline.
- CI files record unavailable single-class metrics explicitly. All plotted and
  displayed rounding is presentation only; machine-readable results retain precision.
- Streamlit was upgraded before fitting because the initially attempted version
  required an older Arrow release than the frozen ingestion environment. Arrow
  remains pinned to its Phase 1 version; pip check must pass.

The user separately authorized one-time unsealing after results are frozen and
reported; the exact approval is recorded in HOLDOUT_APPROVAL.json. The exclusive
receipt is consumed even if evaluation fails, preventing automatic repeat attempts.
GitHub publishing remains outside the authorization given so far.
