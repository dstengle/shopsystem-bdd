"""Handlers of batches' scenarios of a task's dependents and of a task whose change touches a feature (r203-r205,
b889), each taking only a step of a scenario of one of its groups (`mine`), first in its key's chain.

g205: over batches_world's batch, the running task's branch is given one more commit after the world's, citing its
item, that touches `features/work-queue.feature` (the kept change touching a feature); `work batch done` is run on the
task (batches_handlers_parked's When) and the Then reads the kept change's short sha in what it printed."""
import sys
from pathlib import Path

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
GROUPS = {"g203", "g204", "g205"}
FEATURE = "features/work-queue.feature"


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "batches" and bool(GROUPS & set(found.tags))


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, "batches")(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


@first("GivenK", "feature")
def given_feature(step):
    """A feature: the capability's feature the items' lines are in, `features/work-queue.feature`."""
    if not mine(step):
        return False


@first("GivenDoes", "touch")
def given_touches(step):
    """`the kept change k1 touches the feature f1`: a commit the world adds to the running task's branch."""
    if not mine(step):
        return False
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("commit", "feature"):
        return False
    step.context.setdefault("touching", []).append(n1)


@first("GivenDoes", "holds")
def given_holds(step):
    """`the workspace w1 holds the kept change k1`: the commit is on the branch of the task's worktree."""
    if not mine(step):
        return False
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("worktree", "commit"):
        return False


def _touching(step, name):
    """Once the batch is made: each kept change touching a feature committed on the running task's branch."""
    if not step.context.get("touching"):
        return
    n = T.batch_name(step, name)
    for task, found in step.context["given"]["task"].items():
        if found["status"] != "running" or found["batch"] != name:
            continue
        b = B.ident(found["item"])
        tree = T.outside(step) / ("touch-%s" % b)
        T.git(step, "worktree", "add", "-q", str(tree), "%s-%s" % (n, b))
        path = tree / FEATURE
        path.write_text(path.read_text() + "\n# edited by hand\n")
        T.git(step, "commit", "-q", "-am", "an edit of the feature\n\nItem: %s" % b, cwd=tree)
        sha = T.git(step, "rev-parse", "--short", "HEAD", cwd=tree).strip()
        T.git(step, "worktree", "remove", "--force", str(tree))
        for kept in step.context["touching"]:
            step.context.setdefault("says", {})[kept] = sha


T.AFTER_BATCH.append(_touching)


@first("ThenDoes", "name")
def then_names(step):
    """`the batches service names the kept change k1`: refused, its short sha in what `work batch done` printed."""
    if not mine(step) or parts(step)[-1][0] != "commit":
        return False
    done, said = step.context["result"], step.context["says"][parts(step)[-1][1]]
    assert done.returncode == 1 and said in done.stderr, (step.text, said, done.stdout, done.stderr)
