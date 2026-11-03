"""The formulate round as a script (the GF conversion's design §13): `features generate` for each capability of the
approved proposal, `features generate --check`, `model check` with no new row, the feature files committed, and no
session. A capability that is not codified, a generation that fails or a new row is the round's fault."""
import json
import pathlib
import shutil
import subprocess
import sys
import threading

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import supervise_worker  # noqa: F401  (supervise_faults is loaded through it, as supervise loads it)
import supervise_formulate
import toolchain
from supervise_faults import Fault

FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures" / "generate"


def git(root, *args):
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout


@pytest.fixture
def repo(tmp_path):
    toolchain.require()
    root = tmp_path / "repo"
    shutil.copytree(FIXTURES / "repo", root)
    shutil.copytree(FIXTURES / "broken" / "spec" / "capabilities", root / "spec" / "capabilities", dirs_exist_ok=True)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.name", "t")
    git(root, "config", "user.email", "t@t")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "spec")
    return root


def generated(root, name):
    done = subprocess.run([sys.executable, str(SCRIPTS / "features"), "generate", "--root", str(root), "--preview",
                           str(root / "spec" / "capabilities" / ("%s.md" % name))], capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return done.stdout


def test_the_capabilities_of_a_proposal_are_those_its_lists_name_in_order():
    lists = {"adds": ["work-queue#r5", "term/frobnicate"], "changes": ["review#r1"], "removes": ["work-queue#r2"]}
    assert supervise_formulate.capabilities(lists) == ["work-queue", "review"]


def test_a_codified_service_capability_is_generated_checked_and_committed(repo):
    result = supervise_formulate.script(repo, "work-queue", ["work-queue"])
    assert (repo / "features" / "work-queue.feature").read_text() == generated(repo, "work-queue")
    assert result["generated"] == ["features/work-queue.feature"] and result["status"] == "DONE"
    assert git(repo, "status", "--porcelain") == ""
    assert "features: work-queue generated from work-queue" in git(repo, "log", "-1", "--format=%s")
    assert result["commit"] == git(repo, "rev-parse", "HEAD").strip()


def test_a_guarantees_capability_has_no_feature_and_nothing_is_committed(repo):
    head = git(repo, "rev-parse", "HEAD")
    result = supervise_formulate.script(repo, "review", ["review"])
    assert result["generated"] == [] and not (repo / "features").exists() and git(repo, "rev-parse", "HEAD") == head


def test_an_uncodified_capability_is_the_rounds_fault_naming_migrate_upgrade(repo):
    with pytest.raises(Fault) as fault:
        supervise_formulate.script(repo, "legacy", ["legacy"])
    assert "spec/capabilities/legacy.md is not codified: run `migrate upgrade`" in str(fault.value)
    assert not (repo / "features").exists()


def test_a_generation_that_fails_is_the_rounds_fault_naming_the_requirement(repo):
    with pytest.raises(Fault) as fault:
        supervise_formulate.script(repo, "thing", ["thing"])
    assert "thing#r2" in str(fault.value) and git(repo, "status", "--porcelain") == ""


def test_a_new_model_check_row_is_the_rounds_fault_and_nothing_is_committed(repo, monkeypatch):
    seen = iter([set(), {("v_s1", "features/work-queue.feature:a scenario")}])
    monkeypatch.setattr(supervise_formulate, "rows", lambda root: next(seen))
    head = git(repo, "rev-parse", "HEAD")
    with pytest.raises(Fault) as fault:
        supervise_formulate.script(repo, "work-queue", ["work-queue"])
    assert "model check" in str(fault.value) and "v_s1" in str(fault.value)
    assert git(repo, "rev-parse", "HEAD") == head and git(repo, "status", "--porcelain") == ""


def test_model_check_rows_are_rule_and_row_pairs():
    text = ("v_s3  a group or requirement has no scenario  (2)\n    capability/x#g1\n    capability/x#g2\n"
            "file: spec/a.md: wrong\n3 violations, 0 warnings, 0 unresolved references, 1 file problems\n")
    assert supervise_formulate.parse_rows(text) == {("v_s3", "capability/x#g1"), ("v_s3", "capability/x#g2"),
                                                    ("file", "file: spec/a.md: wrong")}


class Stub(supervise_formulate.Formulate):
    """The part of a run the formulate round uses."""

    def __init__(self, root):
        self.root, self.initiative, self.dir = root, "i1", root / ".shop" / "work" / "i1"
        self.lock, self.own = threading.RLock(), set()
        self.dir.mkdir(parents=True)
        (self.dir / "work-queue.md").write_text("---\nkind: capability-proposal\nstatus: approved\nadds: [work-queue#r1]\n"
                                                "changes: []\nremoves: []\n---\n")

    def rel(self, path):
        return path.relative_to(self.root).as_posix()

    def run_dir(self, name, stage):
        return "1-formulate", self.dir / "runs" / name / "1-formulate"


def test_the_round_gives_a_result_in_its_stage_directory_and_starts_no_session(repo):
    run = Stub(repo)
    data, failure = run.formulate_script("work-queue", repo, "1-formulate")
    kept = repo / ".shop/work/i1/runs/work-queue/1-formulate"
    assert failure is None and json.loads((kept / "result.json").read_text()) == data
    assert data["generated"] == ["features/work-queue.feature"] and not (kept / "session.json").exists()
    assert run.rel(kept) in run.own
