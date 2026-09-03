"""Tests for scripts/install_cron_script_deps.py."""
import importlib.util
from pathlib import Path
import pytest

REPO = Path(__file__).parent.parent
SCRIPT = REPO / "scripts" / "install_cron_script_deps.py"


def _load_module():
    spec = importlib.util.spec_from_file_location(
        "install_cron_script_deps", str(SCRIPT)
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_dry_run_does_not_modify(tmp_path, monkeypatch):
    mod = _load_module()
    fake_can = tmp_path / "scripts"
    fake_can.mkdir()
    fake_repo = tmp_path / "repo" / "scripts"
    fake_repo.mkdir(parents=True)
    (fake_repo / "signal_queue.py").write_text("# signal_queue stub\n")
    (fake_can / "router.py").write_text("from signal_queue import X\n")
    monkeypatch.setattr(mod, "CANONICAL", fake_can)
    monkeypatch.setattr(mod, "REPO_SCRIPTS", fake_repo)

    original_router = (fake_can / "router.py").read_text()
    mod.patch(apply=False)
    # No new file created
    assert not (fake_can / "signal_queue.py").exists()
    assert (fake_can / "router.py").read_text() == original_router


def test_apply_copies_missing_sibling(tmp_path, monkeypatch):
    mod = _load_module()
    fake_can = tmp_path / "scripts"
    fake_can.mkdir()
    fake_repo = tmp_path / "repo" / "scripts"
    fake_repo.mkdir(parents=True)
    (fake_repo / "signal_queue.py").write_text("# signal_queue content\n")
    (fake_repo / "_paths.py").write_text("# _paths content\n")
    (fake_can / "router.py").write_text("from signal_queue import X\nfrom _paths import Y\n")
    monkeypatch.setattr(mod, "CANONICAL", fake_can)
    monkeypatch.setattr(mod, "REPO_SCRIPTS", fake_repo)

    mod.patch(apply=True)
    assert (fake_can / "signal_queue.py").exists()
    assert (fake_can / "_paths.py").exists()
    assert (fake_can / "signal_queue.py").read_text() == "# signal_queue content\n"


def test_skip_when_already_present(tmp_path, monkeypatch):
    mod = _load_module()
    fake_can = tmp_path / "scripts"
    fake_can.mkdir()
    fake_repo = tmp_path / "repo" / "scripts"
    fake_repo.mkdir(parents=True)
    (fake_repo / "signal_queue.py").write_text("# new content\n")
    (fake_can / "signal_queue.py").write_text("# existing content\n")
    (fake_can / "router.py").write_text("from signal_queue import X\n")
    monkeypatch.setattr(mod, "CANONICAL", fake_can)
    monkeypatch.setattr(mod, "REPO_SCRIPTS", fake_repo)

    mod.patch(apply=True)
    # Existing file is NOT overwritten
    assert (fake_can / "signal_queue.py").read_text() == "# existing content\n"


def test_skip_stdlib_imports(tmp_path, monkeypatch):
    mod = _load_module()
    fake_can = tmp_path / "scripts"
    fake_can.mkdir()
    fake_repo = tmp_path / "repo" / "scripts"
    fake_repo.mkdir(parents=True)
    (fake_can / "router.py").write_text("import os\nimport sys\nfrom pathlib import Path\n")
    monkeypatch.setattr(mod, "CANONICAL", fake_can)
    monkeypatch.setattr(mod, "REPO_SCRIPTS", fake_repo)

    mod.patch(apply=True)
    # No spurious files created from stdlib imports
    assert list(fake_can.iterdir()) == [fake_can / "router.py"]


def test_idempotent(tmp_path, monkeypatch):
    mod = _load_module()
    fake_can = tmp_path / "scripts"
    fake_can.mkdir()
    fake_repo = tmp_path / "repo" / "scripts"
    fake_repo.mkdir(parents=True)
    (fake_repo / "signal_queue.py").write_text("# signal_queue content\n")
    (fake_can / "router.py").write_text("from signal_queue import X\n")
    monkeypatch.setattr(mod, "CANONICAL", fake_can)
    monkeypatch.setattr(mod, "REPO_SCRIPTS", fake_repo)

    mod.patch(apply=True)
    # Second run is a no-op
    mod.patch(apply=True)
    assert (fake_can / "signal_queue.py").exists()
