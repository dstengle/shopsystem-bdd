"""An in-batch item amended (batches r81-r83, b460), over the world batches_world.py builds: the item's lines laid on
`batch-<n>` and its task's branch as `work batch start` laid them, then changed on main before the When as `work
line` changes them (each line reworded, or every line taken out when a Given says the item no longer holds its
requirement), committed, and `work batch amend` run; the Thens read the batch's or the task's branch."""
import re
import sys

import backlog_items
import backlog_lines

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


@four("GivenDoes", "holds", *BOTH)
def holds_requirement(step):
    """The item holds the requirement: one of its lines, which the world gives it when it builds the batch."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("item", "requirement"):
        return False
    step.context.setdefault("proposed", {})[n2] = n1


@four("GivenDoesNot", "holds", *BOTH)
def holds_no_requirement(step):
    """The item no longer holds the requirement the batch's workspace holds: its lines taken out before the When."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("item", "requirement"):
        return False
    step.context.setdefault("proposed", {})[n2] = n1
    step.context.setdefault("dropping", set()).add(n1)


def _change(step, name):
    """The item's lines changed on main and committed: every line taken out (its ids kept under `dropped` for the
    Thens), or each reworded to the world's other passing line (the new texts kept under `amended`)."""
    rel = B.item_rel(step.context, name)
    item = backlog_items.find(step.repo, B.ident(name))
    blocks = backlog_lines.read(item, item.name)
    if name in step.context.get("dropping", ()):
        ids = [i.split("#")[1] for i in backlog_lines.ids(blocks)]
        for requirement, owner in step.context.get("proposed", {}).items():
            if owner == name:
                step.context.setdefault("dropped", {})[requirement] = ids
        item.sections.pop(backlog_lines.SECTION)
    else:
        text = item.sections[backlog_lines.SECTION]
        for _, line in [r for b in blocks for g in b.groups for r in g.requirements]:
            other = T.SECOND if line != T.SECOND else T.R().PASSING
            text = text.replace(line, other)
        item.sections[backlog_lines.SECTION] = text
        step.context["amended"] = [(b.capability, r, t) for b in backlog_lines.read(item, item.name)
                                   for g in b.groups for r, t in g.requirements]
    (step.repo / rel).write_text(backlog_items.render(item))
    W.git(step.repo, "add", "--", rel)
    W.git(step.repo, "commit", "-q", "-m", "work line: %s changed" % item.name)


@four("WhenRuns", "`work batch amend`", *BOTH)
def amend(step):
    name = step.names[-1]
    T.prepare(step)
    T.ensure_batch(step)
    if T.status_of(step, name) == "in-batch":
        _change(step, name)
    T.run_batch(step, "amend", B.ident(name))


@four("ThenDoes", "has", *BOTH)
def task_has_workspace(step):
    """The task has the workspace: the run exited 0, and the workspace is the task's branch."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("task", "worktree") or "amended" not in step.context:
        return False
    assert step.context["result"].returncode == 0, (step.text, step.context["result"].stderr)
    step.context.setdefault("workspace_of", {})[n2] = n1


@four("ThenDoes", "holds", *BOTH)
def workspace_holds(step):
    """The workspace (the batch's branch, or the task's the step before named) holds the item's reworded line under its
    id in the capability, and lists the id as unbuilt."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("worktree", "requirement") or "amended" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    batch = T.batch_name(step, next(iter(step.context["given"]["batch"])))
    task = step.context.get("workspace_of", {}).get(n1)
    branch = T.task_row(step, task)[1] if task else batch
    for capability, rid, text in step.context["amended"]:
        spec = T.git(step, "show", "%s:spec/capabilities/%s.md" % (branch, capability))
        assert "[%s] %s" % (rid, text) in spec, (step.text, branch, rid, spec)
        unbuilt = re.search(r"(?m)^unbuilt: \[(.*)\]$", spec).group(1)
        assert rid in [i.strip() for i in unbuilt.split(",")], (step.text, branch, unbuilt)
