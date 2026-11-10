"""Identity and distinctness (b240, construct #2), the grammar and the form: "another K", "a different K", "two Ks"
and "the same K" parse with one meaning and round-trip; "two Ks" restricts each of the two, a referent made inside a
box of its restriction made again for the second; `distinct` in the check's facts and read by the steps (phase 9,
with test_spec_distinct_check.py)."""
import pathlib
import re
import sys

import pytest
import spec_context
import spec_grammar4
import spec_lf
import spec_rgl_steps
import spec_steps4

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
SECTION = re.compile(r'^### "another K".*?(?=^### |^## )', re.MULTILINE | re.DOTALL)
BLOCK = re.compile(r"^```reading\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def twins():
    return [b.split("\n", 1)[0] for b in BLOCK.findall(SECTION.search((REPO / "grammar" / "language.md").read_text()
                                                                       ).group(0))
            if "\nrefused: " not in b]


def form(line):
    return spec_lf.form(spec_grammar4.load(FIXTURE)[0], spec_grammar4.parse(FIXTURE, line).tree)


def test_the_section_has_its_twins():
    assert len(twins()) >= 7


@pytest.mark.parametrize("line", twins())
def test_each_twin_parses_and_linearises_back(line):
    p = spec_grammar4.parse(FIXTURE, line)
    assert p.tree, p.refusal
    assert spec_grammar4.linearise(FIXTURE, p.tree) == line


def test_two_ks_restricted_by_a_box_make_the_box_again_for_the_second():
    shown = spec_lf.show(form("While two sessions that follow no stage have a worktree, when the person runs "
                              "`work start`, `work` shall exit successfully."))
    assert "not [x2: stage]\n      follow(subject: x1, object: x2)" in shown
    assert "not [x4: stage]\n      follow(subject: x3, object: x4)" in shown
    assert "distinct(x3, x1)" in shown and "of(x5, x1)" in shown and "of(x5, x3)" in shown


def test_the_same_k_of_x_is_the_image_of_x():
    shown = spec_lf.show(form("When a session ends a stage, `work` shall print the same worktree of the session."))
    assert "response [x4: worktree]\n    of(x4, x1)" in shown


@pytest.mark.parametrize("line", twins())
def test_the_check_and_the_steps_read_distinct(line):
    found, why = spec_context.Four(FIXTURE).facts("thing#r1", line)
    assert why is None and any(f.startswith('distinct("thing#r1",') for f in found[1]), why
    steps = spec_rgl_steps.load(FIXTURE)[0]
    assert spec_steps4.cases(steps, [("thing#r1", spec_lf.form(steps, spec_grammar4.parse(FIXTURE, line).tree))])
