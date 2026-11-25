"""contract_obtain: an upstream's contract kept under provider/ (b587, checking r81), obtained again over a contract
kept there already (review f1): the upstream's bytes written again and committed, the same bytes left as they are."""
import shutil
import subprocess
from pathlib import Path

import contract_obtain
from batch_testing import gh_env

FIXTURE = Path(__file__).parent / "fixtures" / "domain-model"
UPSTREAM = "bounded-context/example.org/fixture/inventory"
KEPT = "provider/inventory/1.2.0/contract.toml"
CONTRACT = 'context = "%s"\nversion = "1.2.0"\nstatus = "published"\n' % UPSTREAM


def _git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


def _context(tmp_path, monkeypatch):
    repo, where = tmp_path / "repo", tmp_path / "outside"
    where.mkdir()
    shutil.copytree(FIXTURE / "spec", repo / "spec")
    index = repo / "spec" / "index.md"
    index.write_text(index.read_text().rstrip("\n") + "\n\n## Upstreams\n\n- %s: github: ex/inventory\n" % UPSTREAM)
    hosted = where / "gh-repos" / "ex" / "inventory" / ".shop" / "contracts" / "1.2.0" / "contract.toml"
    hosted.parent.mkdir(parents=True)
    hosted.write_text(CONTRACT)
    _git(repo.parent, "init", "-q", "-b", "main", str(repo))
    _git(repo, "config", "user.name", "t")
    _git(repo, "config", "user.email", "t@example.org")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")
    for key, value in gh_env(where).items():
        monkeypatch.setenv(key, value)
    return repo


def test_obtaining_again_writes_the_upstreams_contract_over_another(tmp_path, monkeypatch, capsys):
    repo = _context(tmp_path, monkeypatch)
    target = repo / KEPT
    target.parent.mkdir(parents=True)
    target.write_text("another contract\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "another")
    assert contract_obtain.obtain(repo, UPSTREAM) == 0
    assert target.read_text() == CONTRACT
    assert KEPT in _git(repo, "show", "--name-only", "--format=", "HEAD").split()
    assert _git(repo, "status", "--porcelain") == ""
    assert "obtained %s" % KEPT in capsys.readouterr().out


def test_obtaining_the_same_contract_again_changes_nothing(tmp_path, monkeypatch, capsys):
    repo = _context(tmp_path, monkeypatch)
    assert contract_obtain.obtain(repo, UPSTREAM) == 0
    head = _git(repo, "rev-parse", "HEAD")
    assert contract_obtain.obtain(repo, UPSTREAM) == 0
    assert _git(repo, "rev-parse", "HEAD") == head
    assert "kept already %s" % KEPT in capsys.readouterr().out
