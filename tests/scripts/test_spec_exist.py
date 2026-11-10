"""Existence (b240, construct #7): "x exists" a one-place state of every thing, "x does not exist" its negation and
"no K exists" R3's "no K", read by `model logic` as the fluent `crel(R, exists, x, none, Pol)` and `rnone`, and
written by `features generate` as a Given that reads back; each twin of the construct in grammar/language.md
translates to the check's facts and to steps."""
import pathlib
import re
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

REPO = pathlib.Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "scripts" / "fixtures" / "codified-2"
LINE = "While %s, when the person runs `work start`, `work` shall %s."
OK, ERROR = "exit successfully", "exit with an error naming `work start`"
SECTION = re.compile(r'^### "X exists".*?(?=^### |^## )', re.MULTILINE | re.DOTALL)
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
    ("the `a` file exists", "the `a` file exists", True),
    ("the `a` file exists", "the `a` file does not exist", False),
    ("the `a` file exists", "the `b` file does not exist", True),
    ("no file exists", "the `a` file exists", False),
    ("no file exists", "a file exists", False),
    ("no file exists", "the `a` file does not exist", True),
    ("a file exists", "the `a` file does not exist", True),       # two files, one there and one not
])
def test_existence_is_a_state_of_its_thing(tmp_path, first, second, clash):
    found = codes(tmp_path, LINE % (first, OK), LINE % (second, ERROR))
    assert ("L1" in found) == clash, found


def test_existence_is_the_one_place_fluent_and_no_k_its_rnone(tmp_path):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", [LINE % ("the `a` file exists", OK),
                                                          LINE % ("no file exists", ERROR)])
    ctx = spec_context.load(tmp_path)
    facts = [f for s in ctx.statements for f in ctx.facts[s.id]]
    assert 'crel("thing#r1",exists,x1,none,pos).' in facts, facts
    assert any(f.startswith('rnone("thing#r2",exists,kind(') and f.endswith("),none).") for f in facts), facts


def twins():
    return [b.split("\n", 1)[0] for b in BLOCK.findall(SECTION.search((REPO / "grammar" / "language.md").read_text()
                                                                       ).group(0))
            if "\nrefused: " not in b]


def test_the_section_has_its_twins():
    assert len(twins()) >= 6


@pytest.mark.parametrize("line", twins())
def test_each_twin_translates_to_facts_and_to_steps(line):
    found, why = spec_context.Four(FIXTURE, True).facts("thing#r1", line)
    assert why is None and found[1], why
    steps = spec_rgl_steps.load(FIXTURE)[0]
    assert spec_steps4.cases(steps, [("thing#r1", spec_lf.form(steps, spec_grammar4.parse(FIXTURE, line).tree))])


@pytest.mark.parametrize("line, given, template", [
    ("the `a` file exists", "the `a` file exists", "GivenDoes"),
    ("the `a` file does not exist", "the `a` file does not exist", "GivenDoesNot"),
    ("no file exists", "no file exists", "GivenDoes"),
    ("a file exists", "the file f1 exists", "GivenDoes"),
])
def test_the_given_says_existence_and_reads_back(line, given, template):
    steps, gram = spec_rgl_steps.load(FIXTURE)
    form = spec_lf.form(steps, spec_grammar4.parse(FIXTURE, LINE % (line, OK)).tree)
    said = [spec_rgl_steps.text(gram, t) for k, t in spec_steps4.read(steps, [("thing#r1", form)]) if k == "given"]
    assert given in said, said
    call = features_vocab4.step(FIXTURE, "given", given)
    assert (call.template, call.term) == (template, "exist")
