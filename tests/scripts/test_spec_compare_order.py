"""Comparisons and orders over a value order (b275): a typed attribute's points (`Type: number`, `time`, `text`), one
thing's value compared with another's read by `model logic` over the cells of the points a pair names, two orders of
one printing in opposite directions an L1, the Givens `features generate` writes of a comparison and of an order, and
world_order's sorted comparison of what a tool printed."""
import pathlib
import subprocess
import sys

import pytest
import spec_context
import spec_lf_order
import spec_solve

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain
import world_order

FEATURES = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"
PAIR = ("While the version of the `a` file is %s the version of a file, when a session writes the file, `work` shall "
        "%s the file.")
EVERY = "When the person runs `work start`, `work` shall print every file, ordered by version, in %s order."


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def codes(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines))
    ctx = spec_context.load(tmp_path)
    assert not ctx.refused, ctx.refused
    return [f.code for f in spec_solve.run(tmp_path, capability="thing")]


def entry(**fields):
    return type("T", (), {"order": "", "type": "", "values": (), **fields})


def test_the_point_of_a_typed_value():
    number, time, text = entry(type="number"), entry(type="time"), entry(type="text")
    assert spec_lf_order.key(number, "`-1.5`") < spec_lf_order.key(number, "`-1`") < spec_lf_order.key(number, "`0.25`")
    assert spec_lf_order.key(number, "`3.10`") < spec_lf_order.key(number, "`3.9`")     # a decimal, not a release
    assert spec_lf_order.key(time, "`2026-01-02`") > spec_lf_order.key(time, "`2026-01-01T23:59`")
    assert spec_lf_order.key(text, "`abc`") < spec_lf_order.key(text, "`abd`") < spec_lf_order.key(text, "`b`")
    assert spec_lf_order.key(number, "`soon`") is None and spec_lf_order.key(entry(), "`1`") is None


@pytest.mark.parametrize("first, second, clash", [
    ("after", "after", True),
    ("after", "before", False),         # the same two values: no value of either meets both
    ("not after", "after", False),
    ("not after", "before", True),
    ("before", "the same as", False),
    ("not before", "the same as", True),
])
def test_two_comparisons_of_the_same_two_values_clash_only_where_values_meet_both(tmp_path, first, second, clash):
    found = codes(tmp_path, PAIR % (first, "print"), PAIR % (second, "not print"))
    assert ("L1" in found) == clash, found


@pytest.mark.parametrize("first, second, clash", [("ascending", "descending", True), ("ascending", "ascending", False)])
def test_two_orders_of_one_printing_clash_in_opposite_directions(tmp_path, first, second, clash):
    found = codes(tmp_path, EVERY % first, EVERY % second)
    assert ("L1" in found) == clash, found


def generated(tmp_path, *lines):
    codified2_world.context(tmp_path, "ex.com/prod/ctx", list(lines), "c1")
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=tmp_path, capture_output=True,
                          text=True)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    return (tmp_path / "features" / "c1.feature").read_text()


def test_a_comparison_is_given_values_that_meet_it(tmp_path):
    text = generated(tmp_path, PAIR % ("after", "print"))
    assert "the version of the `a` file is `1.0.0`" in text and "the version of the file f1 is `0.0.0`" in text, text


def test_an_order_is_given_three_members_in_neither_order_and_a_then_of_it(tmp_path):
    text = generated(tmp_path, EVERY % "descending")
    assert "the version of the file f1 is `2.0.0`" in text and "the version of the file f3 is `1.0.0`" in text, text
    assert "Then `work` prints every file, ordered by version, in descending order" in text.replace("And ", "Then "), \
        text


def test_world_order_compares_the_output_sorted_and_lets_ties_pass():
    values = {"f1": 2, "f2": 3, "f3": 1}
    world_order.ordered("f3 f1 f2", values, "ascending")
    world_order.ordered("f2 f1 f3", values, "descending")
    with pytest.raises(AssertionError):
        world_order.ordered("f1 f2 f3", values, "ascending")
    with pytest.raises(AssertionError):
        world_order.ordered("f3 f1", values, "ascending")     # f2 not printed
    world_order.ordered("f2 f1", {"f1": 1, "f2": 1}, "ascending")
