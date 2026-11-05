"""`work run`'s briefs under the GF conversion's design §13: no formulation-question text, request lines asked for as
codified requirements, and an intake given each line beside its normal form."""
import pathlib
import shutil
import sys

import pytest

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import supervise  # noqa: F401  (its import order settles the modules' circular imports)
import supervise_brief
import toolchain

FIXTURE = pathlib.Path(__file__).resolve().parent / "fixtures" / "generate" / "repo"


def test_the_briefs_hold_no_formulation_question_text():
    assert not hasattr(supervise_brief, "NOTHING_FORMULATED")


def test_request_lines_are_asked_for_as_codified_requirements_checked_with_model_parse():
    assert "strict form" not in supervise_brief.REQUEST_LINES
    assert "codified" in supervise_brief.REQUEST_LINES and "model parse" in supervise_brief.REQUEST_LINES


def test_the_integrate_brief_says_the_drafts_are_codified_and_checked():
    assert "codified" in supervise_brief.CODIFIED and "parses every drafted requirement" in supervise_brief.CODIFIED


@pytest.fixture
def repo(tmp_path):
    toolchain.require()
    root = tmp_path / "repo"
    shutil.copytree(FIXTURE, root)
    return root


def test_a_line_that_parses_is_given_its_normal_form(repo):
    line = "when the person runs  `work start` on an initiative that is `proposed` , `work` shall exit successfully."
    assert supervise_brief.normal_form(repo, line) == (
        "normal form: When the person runs `work start` on an initiative that is `proposed`, `work` shall exit "
        "successfully.")


def test_a_line_that_does_not_parse_says_so(repo):
    said = supervise_brief.normal_form(repo, "When the person runs `work start`, `work` shall frobnicate.")
    assert said.startswith("does not parse: ") and "frobnicate" in said


def test_a_context_whose_index_is_not_codified_gives_no_normal_form(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text("---\nid: bounded-context/a/b/c\n---\n")
    assert supervise_brief.normal_form(tmp_path, "The thing shall go.") is None
