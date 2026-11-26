"""A batch polled whose task branches conflict (batches r158, b710), over batches_handlers_branches' kept changes of
`src/shared.txt`: under a poll, a kept change that conflicts with another and cites no item is the kept change of an
item of its own (`i92`, in the batch), whose task is the first task no Given gives an item, so that it is the earlier
task and the item a kept change cites the later one. The Then `the batches service returns the file f1`, first in its
chain after batches_handlers_next's, reads the file off the batch step's `files`."""
import re
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
EARLIER = "i92"
PATH = "src/shared.txt"      # batches_handlers_branches' shared file


def earlier_item(step):
    """The uncited side of a conflict of kept changes given an item of its own, and that item the first free task."""
    shared = step.context.get("shared")
    if not step.context.get("polling") or not shared or not shared["conflicts"]:
        return
    commits = step.context["given"].setdefault("commit", {})
    pairs = list(shared["conflicts"].items())
    uncited = [c for pair in pairs for c in pair if not commits.get(c, {}).get("item")]
    if not uncited:
        return
    batch = next(iter(step.context["given"]["batch"]))
    B.write_item(step, EARLIER, title="an item whose change conflicts", status="in-batch")
    step.context["given"]["item"][EARLIER] = {"batch": batch}
    for commit in uncited:
        T.given(step, "commit", commit)["item"] = EARLIER
    text = " ".join(W.scenario_texts(step))
    tasks = step.context["given"]["task"]
    free = next((n for n in tasks if not n.startswith("_") and not re.search(
        r"\bthe item [a-z]+\d+ has the task %s\b" % n, text)), None)
    tasks[free or "_%s" % EARLIER] = dict(tasks.get(free, {}), batch=batch, item=EARLIER,
                                          status=tasks.get(free, {}).get("status", "done"))


T.BEFORE_BATCH.append(earlier_item)


@four("ThenPrints", "`work`", *BOTH)
def returns_file(step):
    """`the batches service returns the file f1`: the batch step's `files` hold the shared file's path."""
    kind = parts(step)[-1][0]
    if kind != "file" or "polled" not in step.context or "shared" not in step.context:
        return False
    content = step.context["polled"]["content"]
    assert PATH in (content.get("files") or []), (step.text, content)
