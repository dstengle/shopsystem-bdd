"""The number of Ks (b240, construct #3): "the number of Ks that P" printed, an object of its own restricted as the Ks
it counts, and compared with a number, R7's count in a condition, read by `model logic` (two counts of one set of
things that no number meets both of never fire together) and written by `features generate` (the Ks it needs, or
the Given of a comparison with a parameter, which the codified-2 world's handler records); each twin of the
construct in grammar/language.md translates to the check's facts and to steps."""
import pathlib
import re
import subprocess
import sys

import features_vocab4
import pytest
import spec_context
import spec_grammar4
import spec_lf
import spec_rgl_steps
import spec_solve
import spec_steps4

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain
import vocab

REPO = pathlib.Path(__file__).resolve().parents[2]
FEATURES = REPO / "scripts" / "features"
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
PRINT = "When a session ends a stage, `work` shall %s the number of %s."
STAGE = "While a stage is `open` and the number of lines of the stage is %s, when the person runs `work start`, " \
        "`work` shall %s the stage."
SECTION = re.compile(r'^### "the number of Ks.*?(?=^### |^## )', re.MULTILINE | re.DOTALL)
BLOCK = re.compile(r"^```reading\n(.*?)\n```$", re.MULTILINE | re.DOTALL)


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def codes(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    ctx = spec_context.load(tmp_path)
    assert not ctx.refused, ctx.refused
    return [f.code for f in spec_solve.run(tmp_path, capability="thing")]


@pytest.mark.parametrize("first, second, clash", [
    ("lines of the stage", "lines of the stage", True),
    ("lines of the stage", "sessions that follow the stage", False),
    ("lines of the stage", "lines of the stage whose outcome is `accepted`", False),
    ("lines of the stage whose outcome is `accepted`", "lines of the stage whose outcome is `refused`", False),
])
def test_a_printed_number_is_the_number_of_the_things_it_counts(tmp_path, first, second, clash):
    found = codes(tmp_path, PRINT % ("print", first), PRINT % ("not print", second))
    assert ("L1" in found) == clash, found


@pytest.mark.parametrize("first, second, clash", [
    ("more than three", "at most three", False),
    ("more than three", "less than `2`", False),
    ("`0`", "at least one", False),
    ("more than three", "at least two", True),
    ("at most three", "less than `2`", True),
    ("`0`", "less than `2`", True),
    ("more than `limit`", "at most three", True),        # a parameter's number is not known
])
def test_two_counts_of_one_set_that_no_number_meets_never_fire_together(tmp_path, first, second, clash):
    found = codes(tmp_path, STAGE % (first, "end"), STAGE % (second, "not end"))
    assert ("L1" in found) == clash, found


def test_counts_of_two_sets_are_not_compared(tmp_path):
    other = "While a stage is `open` and the number of lines of the stage whose outcome is `accepted` is at most " \
            "three, when the person runs `work start`, `work` shall not end the stage."
    assert "L1" in codes(tmp_path, STAGE % ("more than three", "end"), other)


def twins():
    return [b.split("\n", 1)[0] for b in BLOCK.findall(SECTION.search((REPO / "grammar" / "language.md").read_text()
                                                                       ).group(0))
            if "\nrefused: " not in b]


@pytest.mark.parametrize("line", twins())
def test_each_twin_translates_to_facts_and_to_steps(line):
    found, why = spec_context.Four(FIXTURE).facts("thing#r1", line)
    assert why is None and found[1], why
    steps = spec_rgl_steps.load(FIXTURE)[0]
    assert spec_steps4.cases(steps, [("thing#r1", spec_lf.form(steps, spec_grammar4.parse(FIXTURE, line).tree))])


def generated(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines), "c1")
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=tmp_path, capture_output=True,
                          text=True)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    text = (tmp_path / "features" / "c1.feature").read_text()
    return [line.strip().split(" ", 1)[1] for line in text.splitlines()
            if line.strip().startswith(("Given", "And", "Then"))]


def test_a_printed_number_brings_in_two_of_the_things_it_counts(tmp_path):
    steps = generated(tmp_path, PRINT % ("print", "lines of the stage whose outcome is `accepted`"))
    assert [s for s in steps if s.startswith("a line ")] == ["a line l1", "a line l2"]
    assert "the outcome of the line l2 is `accepted`" in steps
    assert steps[-1] == "`work` prints the number of lines of the stage s2 whose outcome is `accepted`"


def test_a_compared_number_brings_in_as_many_things_as_it_needs(tmp_path):
    steps = generated(tmp_path, STAGE % ("more than three", "end"))
    assert [s for s in steps if s.startswith("a line ")] == ["a line l1", "a line l2", "a line l3", "a line l4"]


def test_a_comparison_with_a_parameter_is_its_own_given_and_is_recorded(tmp_path):
    text = "the number of lines of the stage s1 is more than `limit`"
    assert text in generated(tmp_path, STAGE % ("more than `limit`", "end"))
    gram = spec_rgl_steps.load(tmp_path)[1]
    vocab.load_handlers(pathlib.Path(__file__).resolve().parents[1] / "scenarios")
    context = {}
    call = features_vocab4.step(tmp_path, "given", text)
    assert spec_rgl_steps.text(gram, call.tree) == text and call.template == "GivenCount"
    call.fixtures = lambda name: {"context": context}[name]
    vocab.lookup(call.template, call.term)(call)
    assert context["counts"] == {"the number of lines of the stage s1": "more than `limit`"}
