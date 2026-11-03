"""`work run`'s drafting of a formulated capability-proposal's work-items (supervision r72) under the GF conversion's
design §13: `accepts` from the proposal's lists, and the retiring of a removed requirement from its `removes`, whose
check is the whole suite (a removed requirement has no scenario left to run)."""
import pathlib
import subprocess
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import supervise_worker  # noqa: F401  (supervise_faults is loaded through it, as supervise loads it)
import workqueue
from supervise_draft import Drafts


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


class Stub(Drafts):
    def __init__(self, root):
        self.root, self.initiative, self.dir = root, "i1", root / ".shop" / "work" / "i1"

    def waits(self, proposal):
        return False

    def rel(self, path):
        return path.relative_to(self.root).as_posix()


@pytest.fixture
def run(tmp_path):
    root = tmp_path / "repo"
    (root / "spec").mkdir(parents=True)
    (root / "spec" / "index.md").write_text("---\nid: bounded-context/example.org/fixture/draft\n---\n")
    work = root / ".shop" / "work" / "i1"
    work.mkdir(parents=True)
    (work / "initiative.md").write_text("---\nid: initiative/example.org/fixture/draft/i1\nkind: initiative\n"
                                        "status: started\n---\n")
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "t")
    git(root, "config", "user.email", "t@t")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    return Stub(root)


def proposal(run, name, status="formulated", adds=(), changes=(), removes=()):
    (run.dir / (name + ".md")).write_text(
        "---\nid: capability-proposal/example.org/fixture/draft/i1-%s\nkind: capability-proposal\nstatus: %s\n"
        "adds: [%s]\nchanges: [%s]\nremoves: [%s]\n---\n" % (name, status, ", ".join(adds), ", ".join(changes),
                                                              ", ".join(removes)))


def items(run):
    return {name: (data, workqueue.read(run.dir / (name + ".md"), run.root)) for name, data in run.nodes("work-item")}


def test_a_proposal_that_adds_and_removes_drafts_one_work_item_accepting_the_adds_and_retiring_the_removes(run):
    proposal(run, "thing", adds=["thing#r5"], removes=["thing#r3"])
    assert run.draft_proposals()
    (data, text), = items(run).values()
    assert data["accepts"] == ["thing#r5"] and data["under"] == "thing"
    assert "## Retires" in text and "(thing @r3)" in text


def test_a_proposal_that_only_removes_drafts_a_retire_work_item_whose_check_is_the_whole_suite(run):
    proposal(run, "thing", removes=["thing#r2", "thing#r3"])
    assert run.draft_proposals()
    (data, text), = items(run).values()
    assert data["accepts"] == [] and "retire" in text.split("\n# ", 1)[1].splitlines()[0]
    assert "(thing @r2)" in text and "(thing @r3)" in text


def test_drafting_again_drafts_nothing_more(run):
    proposal(run, "thing", adds=["thing#r5"], removes=["thing#r3"])
    proposal(run, "other", removes=["other#r1"])
    assert run.draft_proposals()
    assert not run.draft_proposals()
    assert len(items(run)) == 2


def test_a_proposal_not_yet_formulated_drafts_nothing(run):
    proposal(run, "thing", status="approved", adds=["thing#r5"], removes=["thing#r3"])
    assert not run.draft_proposals() and items(run) == {}


def test_a_term_id_drafts_no_work_item(run):
    proposal(run, "thing", adds=["term/frobnicate"])
    assert not run.draft_proposals()
