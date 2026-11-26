"""The scenario worlds' fallbacks (b748): a Given no test world reads fails, naming the scenario's node id and the
Given, so that a new line's scenario cannot pass in a default world that cannot fail. Each picker that fell back
silently is fed a step no world reads and must raise; an allowlisted step of each must not.

- feature_file_tools_capability's `prepare` with an empty spec/ and a fact no branch reads, and its `feature` with
  no example data (the example data's capability or feature file, written by a given block, is allowlisted);
- world_fallbacks' `given_recorded` with a GivenDoes of a verb outside its allowlist (a bare introduction of an
  allowlisted kind, and a named negative fact, are allowlisted);
- readiness_handlers_givens' `given_does` with a has it does not read (a has of a bar check it allowlists)."""
import pathlib
import sys
from types import SimpleNamespace

import pytest

SCENARIOS = pathlib.Path(__file__).resolve().parents[1] / "scenarios"
sys.path.insert(0, str(SCENARIOS.parent))
sys.path.insert(0, str(SCENARIOS))
import vocab

NODE = "tests/scenarios/test_x.py::test_a_scenario_no_world_reads"


def module(file):
    """The handler module of tests/scenarios/<file>, loaded as the scenarios load it."""
    vocab.load_handlers(SCENARIOS)
    return next(m for m in list(sys.modules.values()) if getattr(m, "__file__", None)
                and pathlib.Path(m.__file__).resolve() == (SCENARIOS / file).resolve())


def call(repo=None, **fields):
    base = {"template": "GivenDoes", "kind": None, "term": None, "attribute": None, "text": "", "subject": "",
            "nps": [], "names": [], "values": [], "context": {}, "repo": repo,
            "request": SimpleNamespace(node=SimpleNamespace(nodeid=NODE))}
    base.update(fields)
    return SimpleNamespace(**base)


def capability():
    return module("feature_file_tools_capability.py")


def test_prepare_with_a_fact_no_branch_reads_fails_naming_the_scenario(tmp_path):
    step = call(tmp_path, context={"ff": {"kinds": {"x1": "frobnicator"}, "values": {},
                                          "facts": [("frobnicate", "x1", "y1", True)]}})
    with pytest.raises(AssertionError, match="test_a_scenario_no_world_reads.*frobnicate"):
        capability().prepare(step)


def test_prepare_on_the_example_data_runs_on_no_name(tmp_path):
    (tmp_path / "spec" / "capabilities").mkdir(parents=True)
    (tmp_path / "spec" / "capabilities" / "shelf.md").write_text("# shelf\n")
    step = call(tmp_path, context={"ff": {"kinds": {}, "values": {}, "facts": [("frobnicate", "x1", "y1", True)]}})
    assert capability().prepare(step) == []


def test_feature_with_no_example_data_fails_naming_the_scenario(tmp_path):
    w = {"kinds": {"f1": "feature"}, "values": {}, "facts": []}
    with pytest.raises(AssertionError, match="test_a_scenario_no_world_reads.*f1"):
        capability().feature(call(tmp_path), w, "f1")


def test_feature_of_the_example_data_is_its_feature_file(tmp_path):
    (tmp_path / "features").mkdir()
    (tmp_path / "features" / "shelf.feature").write_text("Feature: shelf\n")
    w = {"kinds": {"f1": "feature"}, "values": {}, "facts": []}
    assert capability().feature(call(tmp_path), w, "f1") == "features/shelf.feature"


def test_given_recorded_of_a_verb_outside_the_allowlist_fails_naming_the_scenario():
    step = call(term="frobnicate", text="the test t1 frobnicates", subject="the test t1")
    with pytest.raises(AssertionError, match="test_a_scenario_no_world_reads.*the test t1 frobnicates"):
        module("world_fallbacks.py").given_recorded(step)


def test_given_recorded_of_an_unlisted_kind_fails():
    step = call(template="GivenK", kind="frobnicator", term="frobnicator", text="a frobnicator f1")
    with pytest.raises(AssertionError, match="a frobnicator f1"):
        module("world_fallbacks.py").given_recorded(step)


@pytest.mark.parametrize("fields", [
    {"template": "GivenK", "kind": "session", "term": "session", "text": "a session s1"},
    {"term": "for", "text": "no commit is for the review finding r2", "subject": "no commit"},
    {"template": "GivenDoesNot", "term": "contain", "subject": "the scenario title s7",
     "text": "the scenario title s7 does not contain the search text s1"}])
def test_given_recorded_of_the_allowlist_passes(fields):
    assert module("world_fallbacks.py").given_recorded(call(**fields)) is None


def test_given_recorded_of_a_positive_fact_of_a_negative_verb_fails():
    step = call(term="for", text="the request c1 is for the request c2", subject="the request c1",
                nps=["the request c2"])
    with pytest.raises(AssertionError, match="is for the request c2"):
        module("world_fallbacks.py").given_recorded(step)


def test_readiness_given_does_of_an_unread_has_fails_naming_the_scenario(monkeypatch):
    givens = module("readiness_handlers_givens.py")
    monkeypatch.setattr(givens.R, "mine", lambda step: True)
    step = call(term="has", text="the item i1 has the frobnicator f1", subject="the item i1",
                nps=["the frobnicator f1"], names=["i1", "f1"])
    with pytest.raises(AssertionError, match="test_a_scenario_no_world_reads.*the frobnicator f1"):
        givens.given_does(step)


def test_readiness_given_does_of_a_bar_check_has_passes(monkeypatch):
    givens = module("readiness_handlers_givens.py")
    monkeypatch.setattr(givens.R, "mine", lambda step: True)
    step = call(term="has", text="the readiness bar r1 has the bar check b1", subject="the readiness bar r1",
                nps=["the bar check b1"], names=["r1", "b1"])
    assert givens.given_does(step) is None
