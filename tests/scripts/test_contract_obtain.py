"""contract_obtain: an upstream's contract kept under provider/ (b587, checking r81), obtained again over a contract
kept there already (review f1): the upstream's bytes written again and committed, the same bytes left as they are; a gh
failure the bounded context unreachable and an id out of the context id form refused (b591)."""
import shutil
import subprocess
from pathlib import Path

import contract_obtain
import pytest
from batch_testing import gh_env
from shop_refused import Refused

FIXTURE = Path(__file__).parent / "fixtures" / "domain-model"
UPSTREAM = "bounded-context/example.org/fixture/inventory"
KEPT = "provider/example.org/fixture/inventory/1.2.0/contract.toml"
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


def test_a_gh_failure_on_the_repository_is_the_bounded_context_unreachable(tmp_path, monkeypatch):
    """A repository GitHub does not answer for is never reported as one with no contract (b591, checking r89)."""
    repo = _context(tmp_path, monkeypatch)
    monkeypatch.setenv("STUB_GH_FAIL", "api repos/ex/inventory")
    with pytest.raises(Refused) as refused:
        contract_obtain.obtain(repo, UPSTREAM)
    assert refused.value.reason == "bounded context unreachable"
    assert not (repo / "provider").exists()


def test_an_id_that_would_leave_provider_is_out_of_the_context_id_form(tmp_path, monkeypatch):
    """An id whose path climbs out of provider/ is refused before anything is read (b591, checking r88)."""
    repo = _context(tmp_path, monkeypatch)
    with pytest.raises(Refused) as refused:
        contract_obtain.obtain(repo, "bounded-context/example.org/../../outside")
    assert refused.value.reason == "id not in the context id form"
    assert not (repo / "provider").exists()


SERVE = '''import json, sys
from pathlib import Path
where = next(a for a in sys.argv[1:] if a.startswith("repos/"))
repo, _, path = where[len("repos/"):].partition("/contents")
found = Path(%r) / repo / path.strip("/")
if found.is_dir():
    sys.stdout.write(json.dumps([{"name": p.name, "type": "dir"} for p in found.iterdir() if p.is_dir()]))
elif found.is_file():
    sys.stdout.buffer.write(found.read_bytes())
else:
    sys.stderr.write("gh: Not Found (HTTP 404)\\n")
    sys.exit(1)
'''


def test_a_crlf_contract_is_kept_byte_for_byte(tmp_path, monkeypatch, capsys):
    """b594: a contract with CRLF line ends kept as the upstream's bytes, and obtained again left as it is."""
    repo = _context(tmp_path, monkeypatch)
    repos = tmp_path / "outside" / "gh-repos"
    crlf = CONTRACT.replace("\n", "\r\n").encode()
    (repos / "ex" / "inventory" / ".shop" / "contracts" / "1.2.0" / "contract.toml").write_bytes(crlf)
    serve = tmp_path / "serve_gh.py"
    serve.write_text(SERVE % str(repos))
    monkeypatch.setenv("SHOPSYSTEM_WORK_GH", "python3 %s" % serve)
    assert contract_obtain.obtain(repo, UPSTREAM) == 0
    assert (repo / KEPT).read_bytes() == crlf
    assert _git(repo, "status", "--porcelain") == ""
    head = _git(repo, "rev-parse", "HEAD")
    assert contract_obtain.obtain(repo, UPSTREAM, "1.2.0") == 0
    assert _git(repo, "rev-parse", "HEAD") == head
    assert "kept already %s" % KEPT in capsys.readouterr().out
