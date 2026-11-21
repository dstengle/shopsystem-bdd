"""Handlers of features/batches.feature in grammar 4 (b240, b158): the Givens of the batches, tasks, commits, pull
requests, review folders, scenarios and requirements batches_world.py builds, said with has, holds, cites, passes and
fails, each in world_four's chain beside the backlog's (backlog_handlers4.py), over the world functions of
batches_handlers*.py."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def _module(stem):
    """A handler module of the glob, by its file's stem."""
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


@four("GivenDoes", "holds", *BOTH)
def holds_given(step):
    """A batch holds an item (in it, `in-batch` unless a Given says otherwise); a git branch holds a requirement (the
    world lays the item's lines on the batch's branch); an item holds a universal condition (its `U1`, which `model
    logic` reads, beside a passing line, b203); an item holds a capability (a new one, `shelf`, b317)."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) == ("batch", "item"):
        T.given(step, "batch", n1)
        T.given(step, "item", n2)["batch"] = n1
        if not B.item_rel(step.context, n2):
            B.write_item(step, n2)
        if T.status_of(step, n2) == "idea":
            B.write_item(step, n2, status="in-batch")
    elif (k1, k2) == ("item", "capability"):          # b317: a new capability, its block with the passing line
        new_capability(step, n1, n2)
    elif (k1, k2) == ("item", "universal condition"):
        sys.modules["shop_readiness_world"].give_universal(step, n1, sys.modules["shop_readiness_world"].TRANSLATED_U)
    elif (k1, k2) == ("worktree", "commit"):           # a task's workspace holds its kept change (the reword)
        has_given(step, ("git branch", n1), ("commit", n2))
    elif (k1, k2) not in (("git branch", "requirement"), ("worktree", "requirement")):
        return False


NEW = ("shelf", "a person shelving things", "Things kept on a shelf, each found by its name.")


def new_capability(step, item, name):
    """The item's one block a capability new to the world's spec (`work line --capability`), its one group the
    passing line under g1, r1; spec/index.md given the empty `## Composition` `migrate init` writes (b391)."""
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    index = step.repo / "spec" / "index.md"
    if "\n## Composition" not in index.read_text():
        index.write_text(index.read_text().rstrip("\n") + "\n\n## Composition\n")
    capability, narrator, purpose = NEW
    step.context.setdefault("new_capability", {})[name] = capability
    lines = ("### %s\n\nnarrator: %s\ngroup: service\npurpose: %s\n\n#### [g1] Shelving\n- [r1] %s"
             % (capability, narrator, purpose, R.PASSING))
    B.write_item(step, item, sections={"Requirements": lines})


@four("GivenDoes", "has", *BOTH)
def has_given(step, *given):
    (k1, n1), (k2, n2) = given or parts(step)
    if k1 == "batch" and k2 in ("pull request", "review folder", "task"):
        T.given(step, "batch", n1)
        T.given(step, k2, n2)["batch"] = n1
    elif (k1, k2) == ("item", "task"):
        T.given(step, "task", n2).update(item=n1, batch=T.given(step, "item", n1).get("batch", "b1"))
    elif (k1, k2) == ("item", "scenario"):
        step.context.setdefault("scenario_of", {})[n2] = n1
    elif (k1, k2) == ("item", "requirement"):
        step.context.setdefault("proposed", {})[n2] = n1
    elif (k1, k2) == ("git branch", "commit"):
        task = step.context["git_branches"][n1]["task"]
        T.given(step, "task", task).setdefault("item", T.OWN_IN)
        T.given(step, "commit", n2)["item"] = step.context["given"]["task"][task]["item"]
    elif (k1, k2) == ("task", "worktree"):            # the task's workspace, the branch its kept changes are on
        step.context.setdefault("git_branches", {}).setdefault(n2, {})["task"] = n1
    elif (k1, k2) not in (("batch", "git branch"), ("batch", "worktree"), ("batch", "batch plan")):    # its plan, b416
        return False


@four("GivenDoesNot", "has", *BOTH)
def has_not_given(step):
    """`the batch b1 does not have the review folder r3` (a counter-example, b273): a review folder of another batch,
    which the world makes beside the batch's (`make_review_folders`)."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("batch", "review folder"):
        return False
    T.given(step, "review folder", n2)["batch"] = ("not", n1)


@four("GivenDoesNot", "exist", *BOTH)
def universal_absent(step):
    """`` `universal` does not exist``: the world's codified spec, which has no spec/universal.md (b203)."""
    if step.subject != "`universal`":
        return False
    sys.modules["shop_readiness_world"].codify(step)
    (step.repo / "spec" / "universal.md").unlink(missing_ok=True)


@four("GivenK", "universal condition", *BOTH)
@four("GivenK", "worktree", *BOTH)
def given_worktree(step):
    """The task's worktree, which the world makes for a running task."""


@four("GivenDoes", "cite", *BOTH)
def cites_given(step):
    """A commit cites the item (a commit of the item's branch), or cites no item (its message has no `Item:` line)."""
    commit = parts(step)[0][1]
    if step.nps[0] == "no item":
        T.given(step, "commit", commit)["uncited"] = True
    else:
        T.given(step, "commit", commit)["item"] = parts(step)[1][1]


@four("GivenDoes", "pass", *BOTH)
@four("GivenDoesNot", "pass", *BOTH)
@four("GivenDoes", "fail", *BOTH)
def passes_given(step):
    """An item passes the readiness bar (the lines `work batch start` gives a ready item) or does not (a line that
    does not parse); a scenario of an item fails or passes in the worktree of the task (the batch's tests)."""
    k, name = parts(step)[0]
    if k == "chore":           # batches_handlers_chore's (b316)
        return False
    if k == "item":
        if step.template == "GivenDoesNot":
            sys.modules["shop_readiness_world"].give_lines(step, name, sys.modules["shop_readiness_world"].FAILING)
    elif name not in step.context.get("scenario_of", {}):     # a scenario of a capability (batches_handlers_reach)
        return False
    else:
        item = step.context["scenario_of"][name]
        step.context["failing" if step.term == "fail" else "passing"] = item


@four("WhenRuns", "`work batch park`", *BOTH)
def batch_park(step):
    item = step.names[-1]
    batch = T.given(step, "item", item).get("batch", "b1")
    T.prepare(step)
    T.ensure_batch(step)
    T.run_batch(step, "park", T.batch_name(step, batch), B.ident(item), "--question",
                _module("batches_handlers_more").QUESTION)


@four("WhenHappens", "merge", *BOTH)
def merges(step):
    return _module("batches_handlers_more").merges_pull_request(step)


@four("ThenDoes", "set", *BOTH)
@four("ThenDoesNot", "set", *BOTH)
def sets(step):
    """The plan's status of the batch, or the task's row, is (is not) the value."""
    np = step.nps[0]
    if not np.startswith("the status of the "):
        return False
    k, name = F.kind(np[len("the status of the "):])
    if k not in ("batch", "task"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    got = T.plan_field(step, name, "status") if k == "batch" else T.task_row(step, name)[0]
    wanted = step.text.rsplit(" to ", 1)[1].strip("`")
    assert (got != wanted) if step.template == "ThenDoesNot" else (got == wanted), (step.text, got)
