"""Handlers of batches' batch summary (r102, r103, b580), each in world_four's chain: the Then that the batch brief the
run wrote holds the batch summary form, its section naming each figure of a batch summary (`FIGURES`, the vocabulary
entry's own words, not batch_summary's table)."""
import re
import sys

W, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
FIGURES = ("cost", "output tokens", "new input tokens", "cache-read tokens", "wall time", "opening time",
           "building time", "test runs", "review time")


def _brief(step, name):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    rel = W.node_rel(step.context, name)
    assert rel, (step.text, "no batch brief was written")
    return (step.repo / rel).read_text()


def figures(text):
    """The figures named, one a line `- <name>: <value>`, of `text`."""
    return [m.group(1) for m in re.finditer(r"^- ([a-z -]+): ", text, re.MULTILINE)]


@four("ThenDoes", "holds", *BOTH)
def brief_holds_form(step):
    """The batch brief holds the batch summary form: its section, each figure under its name, the reply asking for
    it."""
    found = parts(step)
    if [k for k, _ in found] != ["batch brief", "batch summary form"]:
        return False
    text = _brief(step, found[0][1])
    assert "### The batch summary form" in text, (step.text, text)
    form = text.split("### The batch summary form", 1)[1]
    assert figures(form) == list(FIGURES), (step.text, form)
    reply = text.split("## What you reply", 1)[1]
    assert "batch summary" in reply.split("###", 1)[0], (step.text, reply)
