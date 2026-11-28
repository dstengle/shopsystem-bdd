"""reviews' batch submitted with its specification rebuilt from the base (r20, b874), each handler taking only a step of
g20's scenario (`mine`), first in its key's chain: over batches_world's batch, `work batch review` run (the When is
batches_handlers_more's). The batch's workspace is its branch `batch-<n>`; the Thens read it: a commit on it since
the batch's base citing the item whose change rebuilt the specification, and the capability file there holding each
line of the item, as the base now holds it, with every other item's."""
import sys
from pathlib import Path

import backlog_items
import backlog_lines

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "reviews" and "g20" in found.tags


def first(template, term):
    def mark(fn):
        four(template, term, "batches")(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def _branch(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    return T.batch_name(step, "b1")


@first("ThenDoes", "has")
def has(step):
    """`the batch b1 has the workspace w1`: its branch; `the workspace w1 has the specification s1`: the spec on it
    holds each line of the item i1 under its id."""
    if not mine(step) or "result" not in step.context:
        return False
    kinds = [k for k, _ in parts(step)]
    if kinds == ["batch", "worktree"]:
        _branch(step)
    elif kinds == ["worktree", "specification"]:
        branch, item = _branch(step), backlog_items.find(step.repo, B.ident("i1"))
        for block in backlog_lines.read(item, item.name):
            spec = T.git(step, "show", "%s:spec/capabilities/%s.md" % (branch, block.capability))
            for rid, text in [r for g in block.groups for r in g.requirements]:
                assert "[%s] %s" % (rid, text) in spec, (step.text, rid, spec[-600:])
    else:
        return False


@first("ThenDoes", "apply")
def applies(step):
    """`the batches service applies the item i1 to the specification s1`: a commit on the batch's branch since its base
    rebuilt its specification, citing the item."""
    if not mine(step) or "result" not in step.context:
        return False
    branch = _branch(step)
    forked = T.plan_field(step, "b1", "forked_from")
    log = T.git(step, "log", "--format=%s%x00%B%x1e", "%s..%s" % (forked, branch))
    rebuilt = [body for subject, _, body in (e.strip("\n").partition("\x00") for e in log.split("\x1e") if e.strip())
               if "specification rebuilt" in subject]
    assert rebuilt and "Item: %s" % B.ident("i1") in rebuilt[0].splitlines(), (step.text, log)
