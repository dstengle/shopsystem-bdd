"""supervision r131, r132: a researcher's file set is its output; an empty one says no file is to change and is given,
while a result with no file set at all gives none."""
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import supervise_outputs


def test_an_empty_researcher_file_set_is_given():
    assert supervise_outputs.missing("researcher", {"fileset": []}) is None


def test_a_researcher_result_with_no_file_set_misses_it():
    assert supervise_outputs.missing("researcher", {"summary": "done"}) == "the researcher's file set"


def test_a_planner_file_set_must_name_a_file():
    assert supervise_outputs.missing("planner", {"plan": "p", "fileset": []}) == "the planner's file set"
