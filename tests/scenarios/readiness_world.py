"""The scenario repository of features/readiness.feature and features/intake.feature (not a handler module, so the
glob does not load it): the codified spec of tests/scripts/fixtures/generate/repo/ written over the repository's
`spec/` (plan 3, D17), an item given requirement lines, and `work` run with no input. readiness_handlers.py and
intake_handlers.py load it by path as `shop_readiness_world`."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "generate" / "repo" / "spec"
# A line that passes the bar in the fixture's spec, and one that does not parse there (`frobnicate` is no word of it).
PASSING = ("When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to "
           "`abandoned`.")
FAILING = ("When the person runs `work start` on an initiative that is `proposed`, `work` shall frobnicate the "
           "initiative.")
# What `work` must answer with no person there: no stdin, and a ceiling on the run (D16).
NO_INPUT = {"stdin": subprocess.DEVNULL, "timeout": 120}


def B():
    return sys.modules["shop_backlog_world"]


def codify(step):
    """D17's spec over the repository's `spec/`, once: the fixture less its uncodified `legacy.md`, its index naming
    the context `ex.com/prod/ctx`."""
    if step.context.get("codified"):
        return
    spec = step.repo / "spec"
    shutil.copytree(SPEC, spec, dirs_exist_ok=True)
    (spec / "capabilities" / "legacy.md").unlink()
    index = spec / "index.md"
    index.write_text(re.sub(r"(?m)^id: .*$", "id: bounded-context/ex.com/prod/ctx", index.read_text(), count=1))
    step.context["codified"] = True


def block(title, text):
    return "### work-queue\n\n#### [g4] %s\n- [r5] %s" % (title, text)


def give_lines(step, name, text):
    """The item `name` given the one requirement line `text`, as `work-queue#r5` in a group `g4`."""
    codify(step)
    fields = step.context.get("item_fields", {}).get(name, {})
    B().write_item(step, name, sections={"Requirements": block(fields.get("title", "Title of %s" % name), text)})
