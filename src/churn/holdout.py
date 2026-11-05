"""Fail-closed evaluation seal. No unsealing mechanism exists in Phase 2."""

import json
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import date, datetime, time, timedelta, timezone

_ACTIVE = ContextVar("holdout_evaluation_session", default=False)

CUTOFFS = tuple(
    datetime(year, month, 9)
    for year in (2010, 2011)
    for month in range(1, 13)
    if (2010, 6) <= (year, month) <= (2011, 9)
)
DEVELOPMENT_CUTOFFS = CUTOFFS[:-3]
SEALED_CUTOFFS = CUTOFFS[-3:]
OBSERVATION_END = datetime(2011, 12, 9)
HORIZON = timedelta(days=90)


class HoldoutSealedError(PermissionError):
    pass


def require_development(cutoff: str | date | datetime) -> datetime:
    if isinstance(cutoff, str):
        cutoff = datetime.fromisoformat(cutoff)
    elif not isinstance(cutoff, datetime) and isinstance(cutoff, date):
        cutoff = datetime.combine(cutoff, time())
    if not isinstance(cutoff, datetime) or cutoff.tzinfo is not None:
        raise ValueError("Cutoff must be a naive registered midnight")
    # Reject sealed dates and their later aliases before any data access.
    if cutoff >= SEALED_CUTOFFS[0]:
        raise HoldoutSealedError("Holdout sealed; explicit Phase 4 approval is required")
    if cutoff not in DEVELOPMENT_CUTOFFS:
        raise ValueError("Unregistered development cutoff")
    return cutoff


def matured_training_cutoffs(test_cutoff) -> tuple[datetime, ...]:
    test_cutoff = require_development(test_cutoff)
    return tuple(t for t in DEVELOPMENT_CUTOFFS if t + HORIZON <= test_cutoff)


def development_origins() -> tuple[datetime, ...]:
    return tuple(t for t in DEVELOPMENT_CUTOFFS if len(matured_training_cutoffs(t)) >= 3)


def require_evaluation_cutoff(cutoff):
    try:
        return require_development(cutoff)
    except HoldoutSealedError:
        parsed = datetime.fromisoformat(cutoff) if isinstance(cutoff, str) else cutoff
        if _ACTIVE.get() and parsed in SEALED_CUTOFFS:
            return parsed
        raise


@contextmanager
def one_time_session(root, freeze_digest):
    approval = json.loads((root / "docs/HOLDOUT_APPROVAL.json").read_text())
    if approval.get("approved") is not True or not approval.get("user_statement"):
        raise HoldoutSealedError("Explicit approval has not been recorded")
    path = root / "results/holdout_receipt.json"
    receipt = {
        "status": "started",
        "freeze_sha256": freeze_digest,
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "approval": approval,
    }
    # Exclusive create consumes the permission even if evaluation crashes.
    with path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, indent=2)
    token = _ACTIVE.set(True)
    try:
        yield receipt
    except BaseException as error:
        receipt.update(status="failed", error=repr(error))
        raise
    else:
        receipt["status"] = "complete"
    finally:
        _ACTIVE.reset(token)
        receipt["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        path.write_text(json.dumps(receipt, indent=2, default=str) + "\n", encoding="utf-8")
