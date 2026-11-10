"""Value sets and a value's absence (b240, construct #4): "is one of `a` or `b`" a case a value, "is not `a` or `b`"
none of them, "has no T" a fact no listed value meets, and "every K of x is one of ...", read by `model logic` and
written by `features generate` as Givens, which the codified-2 world's handler records; each twin of the construct
in grammar/language.md translates to the check's facts and to steps."""
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
LINE = "While a line %s, when the person runs `work start`, `work` shall %s the line."
STAGE = "While a stage is `open` and %s, when the person runs `work start`, `work` shall %s the stage."
SECTION = re.compile(r'^### "is one of.*?(?=^### |^## )', re.MULTILINE | re.DOTALL)
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
    ("is one of `proposed` or `accepted`", "is `accepted`", True),
    ("is one of `proposed` or `accepted`", "is `refused`", False),
    ("is not `accepted` or `refused`", "is `accepted`", False),
    ("is not `accepted` or `refused`", "is `withdrawn`", True),
    ("has no outcome", "is `accepted`", False),                         # absent: no listed value
    ("has no outcome", "is not `accepted`", True),
    ("has no outcome", "is not `accepted`, `refused` or `withdrawn`", True),     # none of them
    ("is one of `accepted` or `refused`", "has no outcome", False),
])
def test_a_set_is_its_values_and_an_absence_no_value(tmp_path, first, second, clash):
    found = codes(tmp_path, LINE % (first, "print"), LINE % (second, "not print"))
    assert ("L1" in found) == clash, found


@pytest.mark.parametrize("second, clash", [
    ("a line of the stage is `accepted`", True),
    ("a line of the stage is `proposed`", False),
    ("a line of the stage has no outcome", False),
    ("a line of the stage is not `accepted`", True),
])
def test_every_line_of_a_stage_is_one_of_its_values(tmp_path, second, clash):
    every = "every line of the stage is one of `accepted` or `refused`"
    found = codes(tmp_path, STAGE % (every, "end"), STAGE % (second, "not end"))
    assert ("L1" in found) == clash, found


def test_an_absence_is_its_own_fact_and_neither_l3_nor_l4(tmp_path):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", [LINE % ("has no outcome", "print")])
    ctx = spec_context.load(tmp_path)
    facts = [f for s in ctx.statements for f in ctx.facts[s.id]]
    assert any(f.startswith('cond("thing#r1",x1,') and f.endswith(",absent,pos).") for f in facts), facts
    assert [f.code for f in spec_solve.run(tmp_path, capability="thing")] == []


def test_a_finding_says_the_absence(tmp_path):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", [LINE % ("has no outcome", "print"),
                                                          LINE % ("is not `accepted`", "not print")])
    done = subprocess.run([sys.executable, str(REPO / "scripts" / "model"), "--root", str(tmp_path), "logic"],
                          capture_output=True, text=True)
    assert "with a line that has no outcome and is not `accepted`," in done.stdout, done.stdout + done.stderr


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
    return [line.strip().split(" ", 1)[1] for line in text.splitlines() if line.strip().startswith(("Given", "And"))]


def test_a_set_is_a_scenario_a_value_and_none_of_them_each_value_negated(tmp_path):
    steps = generated(tmp_path, LINE % ("is one of `proposed` or `accepted`", "print"))
    assert "the line l1 is `proposed`" in steps and "the line l1 is `accepted`" in steps
    steps = generated(tmp_path, LINE % ("is not `accepted` or `refused`", "print"))
    assert "the line l1 is not `accepted`" in steps and "the line l1 is not `refused`" in steps


def test_has_no_reads_back_and_is_recorded(tmp_path):
    steps = generated(tmp_path, LINE % ("has no outcome", "print"))
    assert "the line l1 has no outcome" in steps
    gram = spec_rgl_steps.load(tmp_path)[1]
    vocab.load_handlers(pathlib.Path(__file__).resolve().parents[1] / "scenarios")
    context = {"values": {("l1", "outcome"): "`proposed`"}}
    for text in ("the line l1 is not `refused`", "the line l1 has no outcome"):
        call = features_vocab4.step(tmp_path, "given", text)
        assert spec_rgl_steps.text(gram, call.tree) == text
        assert call.template == "GivenK_A"
        call.fixtures = lambda name: {"context": context}[name]
        vocab.lookup(call.template, call.term)(call)
    assert context["values"] == {("l1", "outcome"): None}
