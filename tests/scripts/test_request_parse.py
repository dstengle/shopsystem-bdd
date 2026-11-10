"""The upstream parses each line of a request in its own requirement grammar when its index is codified (the GF
conversion's design §13, §13.4; requests r38: `work outcome accepted` refuses a line that does not parse), and refuses
when its spec is not codified, naming `migrate upgrade`; a refusal writes nothing."""
import pathlib
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT / "tests"))
import request_lines
import shop_files
import toolchain

GLOSSARY = ROOT / "tests" / "scripts" / "fixtures" / "glossary" / "spec" / "index.md"
GOOD = "While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall set the status of the initiative to `started`."
BAD = "While an initiative is `drafted`, when the person runs `work start` on the initiative, `work` shall set the status of the initiative to `started`."
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


def test_lines_that_parse_pass(codified):
    assert request_lines.check(codified, [GOOD]) is None


def test_a_line_that_does_not_parse_is_refused_naming_it(codified):
    with pytest.raises(shop_files.Refused) as refused:
        request_lines.check(codified, [GOOD, BAD])
    text = str(refused.value)
    assert "line 2" in text and "`drafted`" in text and BAD in text
    assert "parsed up to" in text, text


def test_work_outcome_accepted_exits_1_on_a_line_that_does_not_parse_and_writes_nothing(codified):
    """requests r38."""
    (codified / "spec/capabilities").mkdir()
    shutil.copyfile(GLOSSARY.parent / "capabilities" / "work-queue.md", codified / "spec/capabilities/work-queue.md")
    (codified / ".shop/requests").mkdir(parents=True)
    (codified / ".shop/requests/q1.md").write_text(
        "---\nid: request/ex.com/prod/ctx/q1\nkind: request\nasker: internal\nsource: [observation/o1]\n"
        "status: open\nturn: upstream\n---\n\n# t\n\n## Lines\n1. %s\n\n## Outcomes\n" % BAD)
    git(codified, "add", "-A")
    git(codified, "commit", "-q", "-m", "q1")
    before = (codified / ".shop/requests/q1.md").read_text()
    r = subprocess.run([sys.executable, str(SCRIPTS / "work"), "--root", str(codified), "outcome", "q1", "1",
                        "accepted", "--into", "work-queue"], capture_output=True, text=True)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "line 1 of q1" in r.stderr and "`drafted`" in r.stderr, r.stderr
    assert (codified / ".shop/requests/q1.md").read_text() == before


def test_an_upstream_whose_index_is_not_codified_is_refused_naming_migrate_upgrade(legacy):
    with pytest.raises(shop_files.Refused) as refused:
        request_lines.check(legacy, [LEGACY])
    assert "spec/index.md is not codified: run `migrate upgrade`" in str(refused.value)


def test_an_upstream_with_an_uncodified_capability_is_refused_naming_it(codified):
    (codified / "spec/capabilities").mkdir()
    (codified / "spec/capabilities/old.md").write_text(UNCODIFIED)
    with pytest.raises(shop_files.Refused) as refused:
        request_lines.check(codified, [GOOD])
    assert "spec/capabilities/old.md is not codified: run `migrate upgrade`" in str(refused.value)


def test_no_grammar_tools_refuses_naming_tools_install(codified, monkeypatch):
    import spec_grammar
    import tools_grammar
    monkeypatch.setattr(tools_grammar, "gf_binary", lambda environ=None: None)
    monkeypatch.setattr(spec_grammar, "_loaded", {})
    monkeypatch.setenv("XDG_CACHE_HOME", str(codified / "empty-cache"))
    with pytest.raises(shop_files.Refused, match="tools install"):
        request_lines.check(codified, [GOOD])
    shutil.rmtree(codified / "empty-cache", ignore_errors=True)
