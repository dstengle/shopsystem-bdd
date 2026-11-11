"""A codified-2 capability's scenarios (b240 phase 13, from batch-33's b153 and b154): `features vocab --check` reads
a codified-2 feature's steps in the step grammar 4, its `unbuilt:` ids are marked as a codified-1 file's are, a Given
of example data reads as such and not as a holds condition, the step grammar is loaded once for a state of the
context and a step's parse is kept on disk, and pytest-bdd runs a codified-2 feature's scenarios through their
handlers, by the conftest's vocabulary and by `bind_all`."""
import pathlib
import subprocess
import sys

import features_vocab4
import pytest
import spec_parse_cache
import spec_rgl_steps
import spec_unbuilt

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world as C
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FEATURES = REPO / "scripts" / "features"
LINES = ["When a session ends a stage, `work` shall print the stage.",
         "When the person runs `work start`, `work` shall exit with an error naming `work start` and change nothing."]


def world(repo, unbuilt=()):
    toolchain.require()
    C.context(repo, "ex.com/prod/ctx", LINES, "c1")
    if unbuilt:
        cap = repo / "spec" / "capabilities" / "c1.md"
        cap.write_text(spec_unbuilt.with_unbuilt(cap.read_text(), unbuilt))
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=repo, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr
    return repo


def vocab_check(repo, tests):
    return subprocess.run([sys.executable, str(FEATURES), "vocab", "--check", "--tests", str(tests)], cwd=repo,
                          capture_output=True, text=True, timeout=600)


def test_features_vocab_check_reads_a_codified2_feature_in_the_step_grammar_4(tmp_path):
    repo = world(tmp_path / "ctx")
    (tmp_path / "none").mkdir()
    done = vocab_check(repo, tmp_path / "none")
    assert done.returncode == 1
    assert "does not parse" not in done.stdout, done.stdout
    assert "the session s1 ends the stage s2 | no handler for WhenHappens end" in done.stdout


def test_a_scenario_of_an_unbuilt_id_of_a_codified2_capability_needs_no_handler(tmp_path):
    repo = world(tmp_path / "ctx", ["r1", "r2"])
    (tmp_path / "none").mkdir()
    assert spec_unbuilt.unbuilt(repo) == {"c1": {"r1", "r2"}} and spec_unbuilt.problems(repo) == []
    done = vocab_check(repo, tmp_path / "none")
    assert (done.returncode, done.stdout.strip()) == (0, "every step has one handler"), done.stdout


def test_a_given_of_example_data_is_not_read_as_a_holds_condition_on_a_code(tmp_path):
    """b154: a file is in a worktree, so "the worktree `w` holds "x"" also reads as the worktree holding a file
    coded "x"; under Given it is example data."""
    repo = world(tmp_path)
    text = 'the worktree `w` holds "x"'
    assert len(spec_rgl_steps.trees(repo, text)) == 2
    call = features_vocab4.step(repo, "given", text)
    assert (call.template, call.term, call.names, call.quoted) == ("GivenCode", "worktree", ["`w`"], ['"x"'])


def test_the_step_grammar_is_loaded_once_for_a_state_of_the_context(tmp_path, monkeypatch):
    repo = world(tmp_path)
    calls, real = [], spec_rgl_steps.modules
    monkeypatch.setattr(spec_rgl_steps, "modules", lambda vocab: calls.append(1) or real(vocab))
    first = spec_rgl_steps.load(repo)
    assert spec_rgl_steps.load(repo)[1] is first[1] and len(calls) <= 1


def test_a_step_parse_is_kept_on_disk(tmp_path, monkeypatch):
    repo = world(tmp_path / "ctx")
    monkeypatch.setattr(spec_parse_cache, "_base", lambda: tmp_path / "parse")
    good, bad = "the session s1 ends the stage s2", "the session s1 sings the stage s2"
    first = spec_rgl_steps.trees(repo, good)
    with pytest.raises(spec_rgl_steps.StepError) as refused:
        spec_rgl_steps.trees(repo, bad)

    def no_gf(*_):
        raise AssertionError("a cached step ran GF")
    monkeypatch.setattr(spec_rgl_steps, "_parse", no_gf)
    assert spec_rgl_steps.trees(repo, good) == first
    with pytest.raises(spec_rgl_steps.StepError) as again:
        spec_rgl_steps.trees(repo, bad)
    assert str(again.value) == str(refused.value)


CONFTEST = '''import sys
sys.path.insert(0, %(scenarios)r)
sys.path.insert(0, %(scripts)r)
import vocab
ROOT = %(root)r
vocab.install(globals(), ROOT, %(here)r)
'''
HANDLERS = '''from pathlib import Path
from vocab import handler
SEEN = Path(%(seen)r)


def seen(step):
    with SEEN.open("a") as out:
        out.write("%%s %%s\\n" %% (step.template, step.term))


for key in (("GivenK", "session"), ("GivenK", "stage"), ("WhenHappens", "end"), ("ThenPrints", "`work`"), ("WhenRuns", "`work start`"),
            ("ThenExitsErr", "`work`"), ("ThenChangesNothing", "`work`")):
    handler(*key)(seen)
'''
TEST = '''from pytest_bdd import scenarios
%(bind)s
scenarios(%(feature)r)
'''


@pytest.mark.parametrize("bind", ["", "from work_queue_world import bind_all\nbind_all(globals(), %r)"])
def test_pytest_bdd_runs_a_codified2_feature_through_its_handlers(tmp_path, bind):
    repo = world(tmp_path / "ctx")
    tests, seen = tmp_path / "t", tmp_path / "seen.txt"
    tests.mkdir()
    names = {"scenarios": str(REPO / "tests" / "scenarios"), "scripts": str(REPO / "scripts"), "root": str(repo),
             "here": str(tests), "seen": str(seen), "feature": str(repo / "features" / "c1.feature")}
    (tests / "conftest.py").write_text(CONFTEST % names)
    (tests / "c1_handlers.py").write_text(HANDLERS % names)
    (tests / "test_c1.py").write_text(TEST % dict(names, bind=bind % str(repo) if bind else ""))
    done = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-n", "0", "-c",
                           "/dev/null", "--rootdir", str(tests), str(tests)], cwd=tests, capture_output=True,
                          text=True, timeout=600)
    assert "2 passed" in done.stdout, done.stdout[-3000:] + done.stderr[-2000:]
    assert sorted(seen.read_text().splitlines()) == sorted(["GivenK session", "GivenK stage", "WhenHappens end",
                                                            "ThenPrints `work`",
                                                            "WhenRuns `work start`", "ThenExitsErr `work`",
                                                            "ThenChangesNothing `work`"])
