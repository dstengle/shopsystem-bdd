"""`work request` parses each line in the upstream's requirement grammar when the upstream's index is codified (the
GF conversion's design §13, §13.4), and refuses an upstream whose spec is not codified, naming `migrate upgrade`; a
refusal writes nothing."""
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT / "tests"))
import toolchain
import workqueue
import workqueue_request

GLOSSARY = ROOT / "tests" / "scripts" / "fixtures" / "glossary" / "spec" / "index.md"
GOOD = "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `started`."
BAD = "When the person runs `work start` on an initiative that is `drafted`, `work` shall set its status to `started`."
LEGACY = "**When** `work list` is run, `work` shall print each request with its status."
UNCODIFIED = "---\nid: capability/example.org/fixture/glossary/old\nnarrator: the person\n---\n\n## Behaviour\n\n- [r1] x\n"


def git(repo, *args):
    return subprocess.run(["git", "-c", "user.name=T", "-c", "user.email=t@example.com", *args], cwd=repo,
                          capture_output=True, text=True, check=True).stdout


def make(tmp_path, index):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text(index)
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.name", "T")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-q", "-m", "init")
    return tmp_path


@pytest.fixture
def codified(tmp_path):
    toolchain.require()
    return make(tmp_path, GLOSSARY.read_text())


@pytest.fixture
def legacy(tmp_path):
    return make(tmp_path, "---\nid: bounded-context/ex.com/prod/ctx\n---\n\n# ctx\n")


def lines(repo, *text):
    path = repo / "lines.md"
    path.write_text("".join(t + "\n" for t in text))
    return str(path)


def written(repo):
    return sorted((repo / ".shop/work/requests").glob("q*.md")) if (repo / ".shop/work/requests").is_dir() else []


def test_lines_that_parse_are_written(codified):
    name = workqueue_request.request(codified, "t", "internal", lines(codified, GOOD), ["observation/o1"], None)
    assert GOOD in (codified / ".shop/work/requests" / (name + ".md")).read_text()


def test_a_line_that_does_not_parse_is_refused_naming_it_and_nothing_is_written(codified):
    with pytest.raises(workqueue.Refused) as refused:
        workqueue_request.request(codified, "t", "internal", lines(codified, GOOD, BAD), ["observation/o1"], None)
    text = str(refused.value)
    assert "line 2" in text and "`drafted`" in text and BAD in text
    assert "parsed up to" in text, text
    assert written(codified) == []


def test_the_command_exits_1_and_writes_no_file(codified):
    r = subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(codified), "request", "t",
                        "--from", "internal", "--lines", lines(codified, BAD), "--source", "observation/o1"],
                       capture_output=True, text=True)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "line 1" in r.stderr and "`drafted`" in r.stderr
    assert written(codified) == []


def test_an_upstream_whose_index_is_not_codified_is_refused_naming_migrate_upgrade(legacy):
    with pytest.raises(workqueue.Refused) as refused:
        workqueue_request.request(legacy, "t", "internal", lines(legacy, LEGACY), ["observation/o1"], None)
    assert "spec/index.md is not codified: run `migrate upgrade`" in str(refused.value)
    assert written(legacy) == []


def test_an_upstream_with_an_uncodified_capability_is_refused_naming_it(codified):
    (codified / "spec/capabilities").mkdir()
    (codified / "spec/capabilities/old.md").write_text(UNCODIFIED)
    with pytest.raises(workqueue.Refused) as refused:
        workqueue_request.request(codified, "t", "internal", lines(codified, GOOD), ["observation/o1"], None)
    assert "spec/capabilities/old.md is not codified: run `migrate upgrade`" in str(refused.value)
    assert written(codified) == []


def test_no_grammar_tools_refuses_naming_tools_install(codified, monkeypatch):
    import spec_grammar
    monkeypatch.setattr(spec_grammar, "gf_binary", lambda: None)
    monkeypatch.setattr(spec_grammar, "_loaded", {})
    monkeypatch.setenv("XDG_CACHE_HOME", str(codified / "empty-cache"))
    with pytest.raises(workqueue.Refused, match="tools install"):
        workqueue_request.request(codified, "t", "internal", lines(codified, GOOD), ["observation/o1"], None)
    assert written(codified) == []
    shutil.rmtree(codified / "empty-cache", ignore_errors=True)
