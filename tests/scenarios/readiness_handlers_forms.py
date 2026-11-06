"""Handlers of features/readiness.feature for the pieces `work line` writes beside an item's lines (b43, r5-r11): a
relation row (`--relation`), a universal condition (`--universal`), an upstream entry (`--upstream`) and a given block
(`--given`), each written onto an item that has a group of lines in the codified spec readiness_world.py writes, or
refused when the piece a Given made malformed. The flag is the one `GivenFeat` keeps (world_run); what `work` wrote is
read back off the item's file."""
import importlib.util
import re
import sys
from pathlib import Path

from vocab import handler


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
local = W.local

# flag: (kind of its piece, a well-formed piece, a malformed one) in the fixture's spec (kinds initiative, work-item).
PIECES = {
    "--relation": ("relation row", "| initiative | holds | work-item | many |", "| initiative | holds | frobnicator |"),
    "--universal": ("universal condition", "`work` shall commit every transition.", None),
    "--upstream": ("upstream entry", "bounded-context/ex.com/prod/up: the upstream, github: ex/up",
                   "the upstream, github: ex/up"),
    "--given": ("given block", "the file `notes.md` holds:\n  The first line.\n  The second line.",
                "an initiative i1 that is `proposed`"),
}
ITEM = "i1"
INTO = {"--relation": ["--into", "work-queue"], "--given": ["--into", "work-queue", "--given", "g4"]}


def _flag(step):
    found = [f for f in step.context.get("flags", []) if f in PIECES]
    assert len(found) == 1, ("no one flag of work line was given", step.context.get("flags"))
    return found[0]


def given_piece(step):
    """`a relation row r1`: the scenario's piece, well-formed until a Given makes it malformed."""
    step.context.setdefault("pieces", {})[step.names[0]] = True


def given_malformed(step):
    assert step.text.endswith(" is malformed"), step.text
    step.context.setdefault("pieces", {})[step.names[0]] = False


for _kind in ("relation row", "upstream entry", "given block"):
    handler("GivenK", _kind)(given_piece)
    handler("GivenK_C", _kind)(given_malformed)


@handler("WhenRuns", "`work line`")
def work_line(step):
    """`work line` on the item i1 (given a group g4 of lines first), with the flag's piece: the malformed one when a
    Given made the piece the step names malformed, whose refusal must name it."""
    flag = _flag(step)
    kind, good, bad = PIECES[flag]
    name = step.names[0]
    item = name if step.kind == "item" else ITEM
    R.give_lines(step, item, R.PASSING)
    text = good if step.context.get("pieces", {}).get(name, True) else bad
    if text is bad:
        step.context.setdefault("says", {})[name] = text.splitlines()[0]
    step.context["piece"] = (kind, text)
    args = INTO.get(flag, []) + ([] if flag == "--given" else [flag])
    B.run_work(step, "line", B.ident(item), *args, text, **R.NO_INPUT)


def written(step):
    """The piece the run wrote is in the item's file the run changed, in its `## Requirements`."""
    kind, text = step.context["piece"]
    assert kind == step.kind, (kind, step.text)
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    rel = B.bind_written(step, ITEM)
    held = (step.repo / rel).read_text().split("\n## Requirements\n", 1)[1]
    if kind == "universal condition":
        assert re.search(r"(?m)^- \[U[1-9]\d*\] %s$" % re.escape(text), held), held
    elif kind == "upstream entry":
        assert re.search(r"(?m)^- %s$" % re.escape(text), held), held
    else:
        assert all(re.search(r"(?m)^%s$" % re.escape(line), held)
                   for line in text.splitlines()), (text, held)


for _kind in ("relation row", "universal condition", "upstream entry", "given block"):
    local("ThenDoes", _kind)(written)
