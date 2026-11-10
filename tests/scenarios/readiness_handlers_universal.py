"""Handlers of features/readiness.feature for `work line --recodify universal` and `work line --universal --retires`
(b220, r17-r19): spec/universal.md switched to the new language on an item, its `### universal` block written with
`language: codified-2`; a new universal condition that replaces a live one of spec/universal.md, the old id under the
block's `retired:`, or refused when the condition it retires is nonexistent. Each handler returns False on a step of
another command, so the step goes on to the other handlers."""
import importlib.util
import re
import sys
from pathlib import Path


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

RECODIFY = "`work line --recodify universal`"
RETIRES = "`work line --universal --retires`"
ITEM = "i1"
LIVE = "universal#U1"               # the live condition of the spec/universal.md written here
NONEXISTENT = "universal#U9"        # an id spec/universal.md does not hold
CONDITION = "`work` shall commit every transition and push it."
UNIVERSAL = ("---\nid: capability/ex.com/prod/ctx/universal\ntitle: Universal conditions\ngroup: guarantees\n"
             "language: codified-1\nretired: []\n---\n\n# Universal conditions\n\n## Behaviour\n\n"
             "- [U1] `work` shall commit every transition.\n")


def _spec(step):
    """The fixture's codified spec, with a spec/universal.md of one live condition U1 in the old language."""
    R.codify(step)
    (step.repo / "spec" / "universal.md").write_text(UNIVERSAL)


@local("GivenK_C", "universal condition")
def given_nonexistent(step):
    """`the universal condition u1 is nonexistent`: the id the run retires is one spec/universal.md does not hold."""
    if not step.text.endswith(" is nonexistent"):
        return False
    step.context.setdefault("retires", {})[step.names[0]] = NONEXISTENT
    step.context.setdefault("says", {})[step.names[0]] = NONEXISTENT


@local("WhenRuns", "item")
def recodify(step):
    """`work line <item> --recodify universal` on the item (shaped, no lines yet)."""
    if step.term != RECODIFY:
        return False
    _spec(step)
    B.write_item(step, step.names[0], status="shaped")
    step.context["recodified"] = step.names[0]
    B.run_work(step, "line", B.ident(step.names[0]), "--recodify", "universal", **R.NO_INPUT)


def retire(step):
    """`work line <item> --universal <condition> --retires universal#U<n>` on the item i1 (shaped, no lines yet): the
    id a Given kept for the condition the step names, else the live U1."""
    if step.term != RETIRES:
        return False
    _spec(step)
    item = step.names[0] if step.kind == "item" else ITEM
    B.write_item(step, item, status="shaped")
    retired = step.context.get("retires", {}).get(step.names[0], LIVE)
    step.context["retiring"] = retired
    B.run_work(step, "line", B.ident(item), "--universal", CONDITION, "--retires", retired, **R.NO_INPUT)


local("WhenRuns", "item")(retire)
local("WhenRuns", "universal condition")(retire)


def _block(step):
    """The item's `### universal` block as the run wrote it."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    held = (step.repo / B.bind_written(step, ITEM)).read_text().split("\n## Requirements\n", 1)[1]
    assert "\n### universal\n" in "\n" + held, held
    return held.split("### universal\n", 1)[1]


@local("ThenDoes", "language marker")
def writes_marker(step):
    """The run exited 0 and wrote the item's universal block with the new language's marker; spec/universal.md is
    unchanged."""
    if "recodified" not in step.context or step.term != "write":
        return False
    assert re.match(r"\nlanguage: codified-2$", _block(step), re.MULTILINE), _block(step)
    assert "language: codified-1" in (step.repo / "spec" / "universal.md").read_text()


@local("ThenDoes", "universal condition")
def writes_condition(step):
    """The run exited 0 and wrote the condition onto the item under a fresh U id, its block's `retired:` holding the
    id it retires, and printed the new id."""
    if "retiring" not in step.context or step.term != "write":
        return False
    block, old = _block(step), step.context["retiring"].split("#")[1]
    assert re.search(r"(?m)^retired: \[%s\]$" % old, block), block
    found = re.search(r"(?m)^- \[(U[1-9]\d*)\] %s$" % re.escape(CONDITION), block)
    assert found and found.group(1) != old, block
    assert "universal#%s" % found.group(1) in step.context["result"].stdout, step.context["result"].stdout
