"""Ordered comparison (b240, construct #6; the CNL 4 design, call 9): an attribute whose entry says `Order:` compared with
a value, read by `model logic` exactly over the values the lines name and the gaps between them, and written by
`features generate` as a Given of one value on the right side of every value the line names, which the codified-2
world's handler records."""
import pathlib
import subprocess
import sys

import features_vocab4
import pytest
import spec_context
import spec_lf_order
import spec_rgl_steps
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain
import vocab

FEATURES = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"
FILE = "While the version of a file is %s, when the person runs `work start`, `work` shall %s the file."
STAGE = "While the priority of a stage is %s, when the person runs `work start`, `work` shall %s the stage."


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def codes(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    ctx = spec_context.load(tmp_path)
    assert not ctx.refused, ctx.refused
    return [f.code for f in spec_solve.run(tmp_path, capability="thing")]


@pytest.mark.parametrize("first, second, clash", [
    ("before `2.0.0`", "after `1.0.0`", True),                 # the gap between them
    ("before `2.0.0`", "not before `2.0.0`", False),
    ("after `1.0.0`", "before `1.0.1`", True),                 # 1.0.0.1: an order by number has every gap
    ("after `2.0.0`", "before `3.0.0`", True),
    ("after `1.0.0` and before `3.0.0`", "`2.0.0`", True),
    ("after `1.0.0` and before `2.0.0`", "`1.0.0`", False),
    ("after `1.0.0` and before `2.0.0`", "`3.0.0`", False),
    ("after `1.0.0` and before `2.0.0`", "`1.0.1`", True),     # a value no entry lists
    ("after `1.9.0`", "before `1.10.0`", True),                # number by number, not as text
    ("after `1.10.0`", "before `1.9.0`", False),
])
def test_two_comparisons_by_number_clash_only_where_a_value_meets_both(tmp_path, first, second, clash):
    found = codes(tmp_path, FILE % (first, "print"), FILE % (second, "not print"))
    assert ("L1" in found) == clash, found


@pytest.mark.parametrize("first, second, clash", [
    ("after `low`", "before `high`", False),                   # nothing is listed between low and high
    ("after `low`", "before `urgent`", True),
    ("after `low`", "`high`", True),
    ("after `low`", "`low`", False),
    ("not after `low`", "before `high`", True),
])
def test_an_order_as_listed_has_only_its_values(tmp_path, first, second, clash):
    found = codes(tmp_path, STAGE % (first, "end"), STAGE % (second, "not end"))
    assert ("L1" in found) == clash, found


def test_a_comparison_is_a_fact_and_the_entry_gives_its_points(tmp_path):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", [FILE % ("not before `2.0.0`", "print")])
    ctx = spec_context.load(tmp_path)
    facts = [f for s in ctx.statements for f in ctx.facts[s.id]]
    assert any(f.startswith('ccmp("thing#r1",x1,') and ",before,(2,0,0,0,0,0),neg)." in f for f in facts), facts
    assert any(f.startswith("dense(") for f in ctx.domain) and any(f.startswith("vkey(") for f in ctx.domain)


def test_the_point_of_a_value():
    entry = type("T", (), {"order": "by number", "values": ("`1.0.0`",)})
    assert spec_lf_order.key(entry, "`1.10.0`") > spec_lf_order.key(entry, "`1.9.2`")
    assert spec_lf_order.key(entry, "`banana`") is None
    listed = type("T", (), {"order": "as listed", "values": ("`low`", "`high`")})
    assert spec_lf_order.key(listed, "`high`") > spec_lf_order.key(listed, "`low`")


def generated(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines), "c1")
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=tmp_path, capture_output=True,
                          text=True)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    text = (tmp_path / "features" / "c1.feature").read_text()
    return [line.strip().split(" ", 1)[1] for line in text.splitlines() if line.strip().startswith(("Given", "And"))]


@pytest.mark.parametrize("said, value", [
    ("after `1.0.0` and before `3.0.0`", "`2.0.0`"),
    ("before `2.0.0`", "`1.0.0`"),
    ("after `3.0.0`", "`3.0.1`"),
    ("after `2.0.0` and before `2.0.1`", "`2.0.0.1`"),
    ("not before `2.0.0`", "`2.0.0`"),
])
def test_the_given_is_one_value_on_the_right_side_of_every_point(tmp_path, said, value):
    assert "the version of the file f1 is %s" % value in generated(tmp_path, FILE % (said, "print"))


def test_a_value_no_entry_lists_reads_back_and_is_recorded(tmp_path):
    steps = generated(tmp_path, FILE % ("after `3.0.0`", "print"), STAGE % ("after `low`", "end"))
    assert "the priority of the stage s1 is `high`" in steps
    gram = spec_rgl_steps.load(tmp_path)[1]
    vocab.load_handlers(pathlib.Path(__file__).resolve().parents[1] / "scenarios")
    context = {}
    for text in ("the file f1 is `3.0.1`", "the priority of the stage s1 is `high`"):
        call = features_vocab4.step(tmp_path, "given", text)
        assert spec_rgl_steps.text(gram, call.tree) == text
        assert call.template == "GivenK_A"
        call.fixtures = lambda name: {"context": context}[name]
        vocab.lookup(call.template, call.term)(call)
    assert context["values"] == {("f1", "version"): "`3.0.1`", ("s1", "priority"): "`high`"}
