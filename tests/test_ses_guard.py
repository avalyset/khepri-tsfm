"""issue.py shared-machine guard (DEVIATIONS D-10), on temporary directories only.

Nothing under /Volumes/Vault/sjel-eller-speil is read: SES_DIR is pointed at tmp_path.
"""

import importlib
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture
def issue(tmp_path, monkeypatch):
    monkeypatch.setenv("V", str(tmp_path / "V"))
    sys.path.insert(0, ROOT)
    mod = importlib.import_module("issue")
    mod = importlib.reload(mod)
    monkeypatch.setattr(mod, "SES_DIR", str(tmp_path / "ses"))
    monkeypatch.setattr(mod, "PROSP", str(tmp_path / "prosp"))
    monkeypatch.setattr(mod, "LOGF", str(tmp_path / "prosp" / "issue_log.jsonl"))
    (tmp_path / "ses").mkdir()
    return mod


def status(tmp_path, line):
    (tmp_path / "ses" / "STATUS_SES.txt").write_text("2026-11-02T00:00:00Z x\n" + line + "\n")


def test_running_is_active(issue, tmp_path):
    status(tmp_path, "2026-11-02T00:41:17Z MODELL google/gemma-3-4b-it: gjenopptar")
    assert issue.ses_active().startswith("SES-S1 går")


def test_paused_is_idle(issue, tmp_path):
    status(tmp_path, "2026-11-02T06:38:29Z PAUSET (ren stopp) i google/gemma-3-4b-it")
    assert issue.ses_active() is None


def test_no_status_file_is_idle(issue):
    assert issue.ses_active() is None


def test_live_las_is_active(issue, tmp_path):
    status(tmp_path, "2026-11-02T06:38:29Z PAUSET")
    (tmp_path / "ses" / "LAS").write_text(str(os.getpid()))
    assert "levende prosess" in issue.ses_active()


def test_dead_las_is_idle(issue, tmp_path):
    status(tmp_path, "2026-11-02T06:38:29Z PAUSET")
    (tmp_path / "ses" / "LAS").write_text("999999")
    assert issue.ses_active() is None


def test_main_logs_lost_and_does_nothing_else(issue, tmp_path, monkeypatch):
    status(tmp_path, "2026-11-02T00:41:17Z MODELL x: gjenopptar")
    monkeypatch.setattr(issue, "vault_ok", lambda: True)
    monkeypatch.setattr(issue, "take_lock", lambda *a, **k: pytest.fail("lock must not be taken"))
    monkeypatch.setattr(issue, "build_raw", lambda *a, **k: pytest.fail("no fetch when SES is active"))
    issue.main()
    rec = json.loads((tmp_path / "prosp" / "issue_log.jsonl").read_text().splitlines()[-1])
    assert rec["status"] == "tapt: SES aktiv"
    assert not list((tmp_path / "prosp").glob("PROSP_*.parquet"))
