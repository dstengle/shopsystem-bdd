"""Handlers of batches' batch summary (r102, r104, b580), each in world_four's chain: the Then that the batch brief the
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


@four("GivenDoes", "has", *BOTH)
def batch_has_summary(step):
    """The batch has the batch summary: what `work batch merged` returns of it (measure batch's figures)."""
    (k1, batch), (k2, summary) = parts(step)
    if (k1, k2) != ("batch", "batch summary"):
        return False
    step.context.setdefault("summary_of", {})[summary] = batch


@four("ThenPrints", "`work`", *BOTH)
def returns_summary(step):
    """`work batch merged` printed the batch summary of the batch: its heading naming the batch, then each figure under
    its name, cost in dollars, tokens a number or `unknown`."""
    if F.kind(step.nps[0])[0] != "batch summary":
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    assert step.names[-1] in step.context.get("summary_of", {}), (step.text, "no batch has the batch summary")
    out = done.stdout
    assert "batch summary of batch-" in out, (step.text, out)
    said = out.split("batch summary of batch-", 1)[1]
    assert figures(said) == list(FIGURES), (step.text, out)
    cost = re.search(r"^- cost: (\S+)$", said, re.MULTILINE).group(1)
    assert re.fullmatch(r"\$\d+\.\d\d|unknown", cost), (step.text, cost)
    for kind in ("output tokens", "new input tokens", "cache-read tokens"):
        value = re.search(r"^- %s: (\S+)$" % kind, said, re.MULTILINE).group(1)
        assert re.fullmatch(r"\d+|unknown", value), (step.text, kind, value)
