"""Handlers of features/readiness.feature for `work line --recodify` (CNL 4's I19, r16): the fixture's codified-1
capability `work-queue` switched to the new language on an item, its block written with `language: codified-2`.
Each handler returns False on a step of another command, so the step goes on to the other handlers."""
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

COMMAND = "`work line --recodify`"
CAPABILITY = "work-queue"       # the fixture's capability, codified-1


@local("WhenRuns", "item")
def recodify(step):
    """`work line <item> --recodify work-queue` on the item (shaped, no lines yet)."""
    if step.term != COMMAND:
        return False
    R.codify(step)
    B.write_item(step, step.names[0], status="shaped")
    step.context["recodified"] = (step.names[0], CAPABILITY)
    B.run_work(step, "line", B.ident(step.names[0]), "--recodify", CAPABILITY, **R.NO_INPUT)


@local("ThenDoes", "capability")
def writes_capability(step):
    """The run exited 0 and wrote the capability's block onto the item, its marker the new language's."""
    if "recodified" not in step.context or step.term != "write":
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    item, capability = step.context["recodified"]
    held = (step.repo / B.bind_written(step, item)).read_text().split("\n## Requirements\n", 1)[1]
    assert re.search(r"(?m)^### %s\n\nlanguage: codified-2$" % re.escape(capability), held), held
    assert "codified-1" in (step.repo / "spec" / "capabilities" / ("%s.md" % capability)).read_text()
