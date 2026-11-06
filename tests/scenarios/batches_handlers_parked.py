"""Handlers of features/batches.feature for a parked item (b47): a park takes the item's lines out of `batch-<n>`
(g17), and `work batch done` on another task is not held up by a parked item's failing scenario (g18), over the world
batches_handlers.py loads; see there."""
import sys

import backlog_items
import backlog_lines
from vocab import handler

W, B, T = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world"))
local = W.local


@handler("GivenR", "proposes")
def item_proposes(step):
    """The requirement is one of the item's lines: the world gives the item its lines when it builds the batch."""
    item, requirement = step.names
    step.context.setdefault("proposed", {})[requirement] = item


@local("ThenDoes", "requirement")
def removes_requirement(step):
    """The run exited 0, and the ids of the item that proposes the requirement are out of the batch branch's spec and
    its `unbuilt:`, where the lines commit laid them."""
    if step.term != "remove":
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    item = step.context["proposed"][step.names[0]]
    found = backlog_items.find(step.repo, B.ident(item))
    ids = [i.split("#")[1] for i in backlog_lines.ids(backlog_lines.read(found, found.name))]
    assert ids, (step.text, "the item has no lines")
    batch = T.batch_name(step, next(iter(step.context["given"]["batch"])))
    spec = T.git(step, "show", "%s:%s" % (batch, T.CAP))
    unbuilt = next(line for line in spec.splitlines() if line.startswith("unbuilt:"))
    for rid in ids:
        assert "[%s]" % rid not in spec and rid not in unbuilt.replace("[", " ").replace(",", " ").split(), (
            step.text, rid, spec)
