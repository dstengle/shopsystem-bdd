"""The Then that states an order (b285, decision 0093): a step of a feature `features generate` wrote of an order,
"`work` prints every file, ordered by version, in ascending order", is taken by world_order's `then`, which
world_fallbacks registers as a `local` handler of ThenPrints whose `order` is set; it checks what the tool printed
against the values codified2_handlers_values recorded of the members, and fails on output out of that order."""
import pathlib
import re
import subprocess
import sys
from types import SimpleNamespace

import features_vocab4
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_world
import toolchain
import vocab

FEATURES = pathlib.Path(__file__).resolve().parents[2] / "scripts" / "features"
EVERY = "When the person runs `work start`, `work` shall print every file, ordered by version, in %s order."
KEYWORDS = {"Given": "given", "When": "when", "Then": "then"}


@pytest.fixture(scope="module", autouse=True)
def tools():
    toolchain.require()


def scenario(tmp_path, direction):
    """The generated scenario's steps of an order, each read as its Call with the scenario's fixtures."""
    codified2_world.context(tmp_path, "ex.com/prod/ctx", [EVERY % direction], "c1")
    done = subprocess.run([sys.executable, str(FEATURES), "generate", "c1"], cwd=tmp_path, capture_output=True,
                          text=True)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    text = (tmp_path / "features" / "c1.feature").read_text()
    vocab.load_handlers(pathlib.Path(__file__).resolve().parents[1] / "scenarios")
    context, calls, keyword = {}, [], None
    request = SimpleNamespace(node=SimpleNamespace(function=None, name="test_c1", nodeid="c1.feature"))   # no feature's
    for word, said in re.findall(r"^\s*(Given|When|Then|And) (.*)$", text, re.MULTILINE):
        keyword = KEYWORDS.get(word, keyword)
        call = features_vocab4.step(tmp_path, keyword, said)
        call.fixtures = lambda name: {"context": context, "repo": tmp_path, "request": request}[name]
        calls.append(call)
    return context, calls


def run(tmp_path, direction, printed):
    """The scenario's Givens recorded, `printed` its command's output, and its order's Then run."""
    context, calls = scenario(tmp_path, direction)
    for call in calls:
        if call.keyword == "given" and call.template == "GivenK_A":
            vocab.lookup(call.template, call.term)(call)
    context["result"] = SimpleNamespace(returncode=0, stdout=printed, stderr="")
    then = next(c for c in calls if c.order)
    assert sys.modules["shop_work_queue_world"].LOCAL[("ThenPrints", None)](then) is not False
    return context


def test_the_order_then_passes_on_output_in_its_order(tmp_path):
    values = run(tmp_path, "ascending", "f3\nf1\nf2\n")["values"]
    assert values == {("f1", "version"): "`2.0.0`", ("f2", "version"): "`2.5.0`", ("f3", "version"): "`1.0.0`"}
    run(tmp_path, "descending", "f2 f1 f3")


@pytest.mark.parametrize("direction, printed", [("ascending", "f1 f2 f3"), ("descending", "f3 f1 f2"),
                                                ("ascending", "f3 f1")])
def test_the_order_then_fails_on_output_out_of_its_order(tmp_path, direction, printed):
    with pytest.raises(AssertionError, match=r"is not printed|are not in %s order" % direction):
        run(tmp_path, direction, printed)
