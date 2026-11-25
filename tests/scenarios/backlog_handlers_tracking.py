"""items' suspended item (r58, b578): `work suspend` run on the item the step names with the world's question, and
the Thens of the question kept on the item: under its `## Question`, the item `needs-input`. `work allocate`,
`work deliver` and `work restore` are backlog_handlers4's `run_on_item`."""
import re
import sys

F = sys.modules["shop_world_four"]
four, parts = F.four, F.parts
B, W = sys.modules["shop_backlog_world"], sys.modules["shop_work_queue_world"]

BOTH = ("backlog", "batches")


def _item(step):
    return re.search(r"\bthe item (i\d+)", step.text).group(1)


@four("WhenRuns", "`work suspend`", *BOTH)
def work_suspend(step):
    B.run_work(step, "suspend", B.ident(_item(step)), "--question", B.QUESTION)
    step.context["suspended"] = _item(step)


def _kept(step, item):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    text = B.item_file(step, item).read_text()
    assert "\n## Question\n\n%s\n" % B.QUESTION in text, (step.text, text)
    assert W.field(B.item_file(step, item), "status") == "needs-input", step.text


@four("ThenDoes", "on", *BOTH)
def question_on(step):
    """`the question q1 is on the item i1`: the item the run suspended holds the question."""
    (k1, _), (k2, item) = parts(step)
    if (k1, k2) != ("question", "item") or "suspended" not in step.context:
        return False
    _kept(step, item)


@four("ThenDoes", "write", *BOTH)
def keeps_question(step):
    """The run kept the question: on the item it suspended."""
    if parts(step)[1][0] != "question" or "suspended" not in step.context:
        return False
    _kept(step, step.context["suspended"])
    B.in_commits(step, B.item_rel(step.context, step.context["suspended"]))
