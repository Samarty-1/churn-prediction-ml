import json

import pytest

from churn.holdout import (
    SEALED_CUTOFFS,
    HoldoutSealedError,
    one_time_session,
    require_evaluation_cutoff,
)


def approve_fixture(root):
    (root / "docs").mkdir()
    (root / "results").mkdir()
    (root / "docs/HOLDOUT_APPROVAL.json").write_text(
        json.dumps({"approved": True, "user_statement": "Fixture authorization only"})
    )


def test_one_time_access_is_scoped_and_cannot_be_repeated(tmp_path):
    approve_fixture(tmp_path)
    with pytest.raises(HoldoutSealedError):
        require_evaluation_cutoff(SEALED_CUTOFFS[0])
    with one_time_session(tmp_path, "fixture-freeze"):
        assert require_evaluation_cutoff(SEALED_CUTOFFS[0]) == SEALED_CUTOFFS[0]
        with pytest.raises(HoldoutSealedError):
            require_evaluation_cutoff("2011-07-10")
    with pytest.raises(HoldoutSealedError):
        require_evaluation_cutoff(SEALED_CUTOFFS[0])
    with pytest.raises(FileExistsError), one_time_session(tmp_path, "fixture-freeze"):
        pass
    assert (
        json.loads((tmp_path / "results/holdout_receipt.json").read_text())["status"] == "complete"
    )


def test_failed_evaluation_consumes_permission(tmp_path):
    approve_fixture(tmp_path)
    with pytest.raises(RuntimeError), one_time_session(tmp_path, "fixture-freeze"):
        raise RuntimeError("deliberate fixture failure")
    with pytest.raises(FileExistsError), one_time_session(tmp_path, "fixture-freeze"):
        pass
    assert json.loads((tmp_path / "results/holdout_receipt.json").read_text())["status"] == "failed"


def test_no_recorded_approval_rejects_access(tmp_path):
    approve_fixture(tmp_path)
    (tmp_path / "docs/HOLDOUT_APPROVAL.json").write_text('{"approved": false}')
    with pytest.raises(HoldoutSealedError), one_time_session(tmp_path, "fixture-freeze"):
        pass
    assert not (tmp_path / "results/holdout_receipt.json").exists()
