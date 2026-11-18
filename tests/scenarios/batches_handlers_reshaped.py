"""Handlers of features/batches.feature for a parked item reshaped after the park (b324, batches r45): "the git
branch g1 does not hold the requirement r1" of a requirement an item has. Once the world has made the batch
(batches_world's `make_batch`, the item's lines laid, every task's branch forked, the plan committed), the item's
lines are taken out of `batch-<n>` in one commit as `work batch park` takes them, and the item's line is reworded on
main under its id: a task's branch, forked before, still holds the line as it was laid."""
import sys

import backlog_items
import batch_start

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts


@four("GivenDoesNot", "holds", "backlog", "batches")
def branch_holds_not(step):
    """The requirement is not in the batch's branch: the item that has it is reshaped after the park."""
    (k1, _), (k2, requirement) = parts(step)
    if (k1, k2) != ("git branch", "requirement"):
        return False
    step.context.setdefault("not_held", []).append(requirement)


def reshape(step, name):
    """Each item of the batch `name` that has a requirement the branch does not hold: its lines taken out of the
    batch's branch (the park's commit), then its line reworded on main, its id kept."""
    proposed = step.context.get("proposed", {})
    items = [proposed[r] for r in step.context.get("not_held", ()) if r in proposed]
    items = [i for i in dict.fromkeys(items) if step.context["given"]["item"].get(i, {}).get("batch") == name]
    if not items:
        return
    n = T.batch_name(step, name)
    tree = T.outside(step) / ("park-%s" % n)
    T.git(step, "worktree", "add", "-q", str(tree), n)
    found = [backlog_items.find(step.repo, B.ident(i)) for i in items]
    changed = batch_start.unlay_lines(tree, found, "work batch park")
    T.git(step, "add", "--", *changed, cwd=tree)
    T.git(step, "commit", "-q", "-m", "%s: the requirement lines taken out\n%s" % (n, batch_start.cites(found)),
          cwd=tree)
    T.git(step, "worktree", "remove", "--force", str(tree))
    for item in items:
        fields = step.context["item_fields"][item]
        lines = fields["sections"]["Requirements"]
        reworded = lines.replace("`started`", "`proposed`")
        assert reworded != lines, (item, lines)
        B.write_item(step, item, sections=dict(fields["sections"], Requirements=reworded))
    W.init(step.repo)


T.AFTER_BATCH.append(reshape)
