"""A batch submitted after an amendment its task built (reviews r15, b600, b874), over batches_world's batch: once the
batch is made (T.AFTER_BATCH), the item the amendment cites is given a new line (`AMENDED`, a group of its own) on
main, and `work batch amend`'s apply (batch_amend's `relay`) is made of it on the item's task branch, its workspace,
one commit citing the item with its `Applied:` line; the task branch then builds it (its ids out of `unbuilt:`).
The scenario of the amended line that succeeds in the task's workspace is the one `[batch] tests` runs at the
review, in the batch's worktree, strict: the review passes only when the merge leaves the built line out of
`unbuilt:` on the batch branch."""
import sys

import backlog_items
import batch_amend

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def first(template, term):
    """`four`, the handler put first in its key's chain, before batches_handlers4's of a commit that cites."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


TITLE = "The amended line of %s"


def _tags(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return set(found.tags) if found is not None else set()


def _parked():
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/batches_handlers_parked.py"))


@four("GivenK", "amendment", *BOTH)
def given_amendment(step):
    """The amendment, made once the batch is."""


@first("GivenDoes", "cite")
def amendment_cites(step):
    """`the amendment a1 cites the item i1`: the item it lays again."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("amendment", "item"):
        return False
    step.context.setdefault("amendments", {})[n1] = n2


@four("GivenDoes", "holds", *BOTH)
def holds_amendment(step):
    """`the worktree w1 holds the amendment a1`: a task's workspace, its branch holding the amend's apply (b874);
    under a scenario of a task's only kept change an amendment (b698), nothing built after it."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("worktree", "amendment"):
        return False
    if (step.context.get("git_branches", {}).get(n1) or {}).get("task") and "r15" not in _tags(step):
        step.context.setdefault("unbuilt_amendments", set()).add(n2)
        T.given(step, "item", step.context["amendments"][n2])["unbuilt"] = True     # no build commit before the lay


def _relaid(step, branch, base, new, item, build=False):
    """The amend's apply of `new` on `branch`, its paths put back as `base` holds them, one commit citing the item;
    with `build`, a second commit taking the item's ids out of `unbuilt:`, as its task builds them."""
    tree = T.outside(step) / ("amend-%s" % branch)
    T.git(step, "worktree", "add", "-q", str(tree), branch)
    changed, _ = batch_amend.relay(tree, new, base)
    T.git(step, "add", "-A", "--", *changed, cwd=tree)
    T.git(step, "commit", "-q", "-m", "%s: amended\n\nApplied: %s\nItem: %s" % (branch, base, item), cwd=tree)
    if build:
        T.built(tree, new)
        T.git(step, "add", "-A", cwd=tree)
        T.git(step, "commit", "-q", "-m", "build the amended line of %s\n\nItem: %s" % (item, item), cwd=tree)
    T.git(step, "worktree", "remove", "--force", str(tree))


def amended(step, name):
    """The batch's amendment (T.AFTER_BATCH): each item an amendment cites given a new line on main, applied on its
    task branch, built there."""
    unbuilt = {step.context["amendments"][a] for a in step.context.get("unbuilt_amendments", ())}
    for item in dict.fromkeys(step.context.get("amendments", {}).values()):
        if T.given(step, "item", item).get("batch") != name:
            continue
        b = B.ident(item)
        fields = step.context["item_fields"][item]
        lines = fields["sections"]["Requirements"] + "\n\n#### [g80] %s\n- [r80] %s" % (TITLE % item, T.R().PASSING)
        B.write_item(step, item, sections=dict(fields["sections"], Requirements=lines))
        T.git(step, "add", "-A")
        T.git(step, "commit", "-q", "-m", "work line: %s amended" % b)
        new = backlog_items.find(step.repo, b)
        n = T.batch_name(step, name)
        _relaid(step, "%s-%s" % (n, b), T.git(step, "rev-parse", n).strip(), new, b, build=item not in unbuilt)


T.AFTER_BATCH.append(amended)


@four("WhenRuns", "`work batch review`", *BOTH)
def review_runs_amended(step):
    """Under `work batch review` of an amended batch: `[batch] tests` the amended line's scenario, run in the batch's
    worktree; the review itself is batches_handlers_more's."""
    amended_items = list(dict.fromkeys(step.context.get("amendments", {}).values()))
    if not amended_items or "prepared" in step.context:
        return False
    feature = step.repo / ".shop" / "worktrees" / "batch-1" / "features" / "work-queue.feature"
    step.context["delivery"] = _parked().bound_tests(step, feature, TITLE % amended_items[0])
    return False

