"""Handlers of batches' scenarios of a task's dependents and of a task whose change touches a feature (r203-r205,
b889), each taking only a step of a scenario of one of its groups (`mine`), first in its key's chain.

g203: `work batch start` on batches_world's world with no seam (batches_handlers_applied's), the item i1 `ready` with a
line its applied workspace finds broken (applied's `BROKEN`, the rule catalogue written), so the batches service
reopens it; each other item the scenario names `ready` with a passing line of its own (`LINES`), a dependency on i1 of
those the Givens say have one; the Thens read each item's status and the batch's plan.

g204: over batches_world's batch, the item the dependent depends on made `in-batch` before the batch is made, and
amended (batches_handlers_amend's When: its lines reworded on main); the dependent's task branch is read for its own
lines beside the amended ones, which batches_handlers_amend's Then after it reads.

g205: over batches_world's batch, the running task's branch is given one more commit after the world's, citing its
item, that touches `features/work-queue.feature` (the kept change touching a feature); `work batch done` is run on the
task (batches_handlers_parked's When) and the Then reads the kept change's short sha in what it printed."""
import re
import sys
from pathlib import Path

import backlog_items
import backlog_lines

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
GROUPS = {"g203", "g204", "g205"}
FEATURE = "features/work-queue.feature"
# Passing lines of the other items g203 names, no two sharing a condition and a trigger (v15n), nor one with i1's
# broken line or the world's own item's (batches_handlers_applied's BROKEN and PASS).
LINES = (("While an initiative is `proposed`, when the person runs `work tidy` on the initiative, `work` shall exit "
          "successfully."),
         ("While an initiative is `started`, when the person runs `work tidy` on the initiative, `work` shall exit "
          "successfully."),
         ("While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set "
          "the status of the initiative to `abandoned`."))


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


def _applied():
    """batches_handlers_applied, which the handlers' glob loaded under a name of its own."""
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and Path(m.__file__).name == "batches_handlers_applied.py")


@first("GivenDoesNot", "has")
def given_has_not(step):
    """`the item i4 does not have the dependency d3`: the item is written with no dependency; the dependency is the
    world's own item's (backlog_world's)."""
    if not mine(step):
        return False
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("item", "dependency"):
        return False


@first("WhenRuns", "`work reopen`")
def reopens(step):
    """`the batches service reopens the item i1`: `work batch start` run, every item the scenario names `ready`, i1's
    line one its applied workspace finds broken."""
    if not mine(step):
        return False
    R, A = sys.modules["shop_readiness_world"], _applied()
    R.codify(step)
    step.context["delivery"] = T.DELIVERY + "\n[review]\nsize = 5000\n"
    step.context["own_line"] = A.PASS     # the world's own item's line, sharing no trigger with the others
    names = sorted(set(re.findall(r"\bthe item (i\d+)\b", " ".join(W.scenario_texts(step)))) - {step.names[-1]})
    for name, line in zip(names, LINES):
        B.write_item(step, name, status="ready")
        R.give_lines(step, name, line, capability=A.CAP)
    B.write_item(step, step.names[-1], status="ready")
    catalogue = step.repo / "grammar" / "rules.md"
    catalogue.parent.mkdir(parents=True, exist_ok=True)
    catalogue.write_text("# The rule catalogue\n")
    R.give_lines(step, step.names[-1], A.BROKEN[A.CODES[0]], capability=A.CAP)
    T.before_start(step)
    T.prepare(step)
    T.run_batch(step, "start")


def _row(step, name):
    """(the plan's task id, its branch) of the item `name`'s task in `batch-1`'s plan, or (None, None)."""
    return _applied()._row(step, name)


@first("ThenDoes", "reopen")
@first("ThenDoesNot", "reopen")
def then_reopens(step):
    """`the batches service reopens the item i2`: given back `shaped`, no task of it in the batch's plan; `does not
    reopen`: `in-batch`, a task of it in the plan."""
    if not mine(step) or "result" not in step.context:
        return False
    done, name = step.context["result"], step.names[-1]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    status = B.status_of(step, B.ident(name))
    if step.template == "ThenDoes":
        assert status == "shaped" and _row(step, name) == (None, None), (step.text, status, done.stdout)
    else:
        assert status == "in-batch" and _row(step, name)[0], (step.text, status, done.stdout)


def _blocker_in_batch(step):
    """Before the batch is made (g204): each item a dependency is on, of an item of the batch, `in-batch` too."""
    if not mine(step) or "g204" not in _tags(step):
        return
    for dep in step.context.get("deps", {}).values():
        if dep.get("on") and B.status_of(step, B.ident(dep["on"])) != "in-batch":
            B.write_item(step, dep["on"], status="in-batch")


T.BEFORE_BATCH.append(_blocker_in_batch)


def _tags(step):
    return set(sys.modules["vocab"].vocab4.requested.scenario(step.request.node).tags)


@first("ThenDoes", "has")
def then_has_own(step):
    """`the workspace w1 has the specification s1` (g204): the dependent's task branch still holds each of its own
    lines; then batches_handlers_amend's handler reads the amended item's lines there (the chain goes on)."""
    if not mine(step) or "g204" not in _tags(step):
        return False
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("worktree", "specification"):
        return False
    task = step.context["workspace_of"][n1]
    item = backlog_items.find(step.repo, B.ident(step.context["given"]["task"][task]["item"]))
    branch = T.task_row(step, task)[1]
    for block in backlog_lines.read(item, item.name):
        spec = T.git(step, "show", "%s:spec/capabilities/%s.md" % (branch, block.capability))
        for rid, text in [r for g in block.groups for r in g.requirements]:
            assert "[%s] %s" % (rid, text) in spec, (step.text, "the dependent's own line", rid, spec[-800:])
    return False


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
    for found in step.context["given"]["task"].values():
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
