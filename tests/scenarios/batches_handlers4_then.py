"""The Thens of features/batches.feature in grammar 4 (b240, b158), each in world_four's chain beside the backlog's,
over the checks of batches_handlers*.py: what `work batch` wrote, picked, printed, refused, named, published and
removed. A step of a kind that is not the batches' returns False."""
import sys

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def _module(stem):
    """A handler module of the glob, by its file's stem."""
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


def _more():
    return _module("batches_handlers_more")


def _first():
    return _module("batches_handlers")


@four("ThenDoes", "write", *BOTH)
def writes(step):
    k = parts(step)[1][0]
    if k == "batch":
        return _first().writes_batch(step)
    if k == "batch plan":
        return _first().writes_plan(step)
    return False


@four("ThenDoes", "remove", *BOTH)
@four("ThenDoesNot", "remove", *BOTH)
def removes(step):
    k = parts(step)[1][0]
    if k == "review folder":
        return _more().removes_review_folder(step)
    if k == "requirement":
        return _module("batches_handlers_parked").removes_requirement(step)
    return False


@four("ThenPrints", "`work`", *BOTH)
def prints(step):
    k = F.kind(step.nps[0])[0]
    if k == "item":
        return _first().prints_item(step)
    if k in ("task", "status of the task"):
        return _first().prints_task(step)
    if k == "batch brief":
        return _first().prints_brief(step)
    return False


@four("ThenDoes", "name", *BOTH)
def names(step):
    k = parts(step)[1][0]
    if k == "task":
        return _first().refused_naming_task(step)
    if k == "commit":
        return _first().refused_naming_commit(step)
    return False


@four("ThenDoes", "has", *BOTH)
def has_then(step):
    """The batch has the pull request (gh created it from the batch's branch), the batch plan (the run wrote and
    committed it)."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) == ("batch", "pull request"):
        call = _more().created(step)
        assert call[call.index("--head") + 1] == T.batch_name(step, n1), (step.text, call)
    elif (k1, k2) == ("batch", "batch plan"):
        step.context.setdefault("plans", {})[n2] = _first().plan_written(step)
    else:
        return False


@four("ThenDoes", "cite", *BOTH)
def cites(step):
    return _more().pull_request_cites(step)


@four("ThenDoesNot", "holds", *BOTH)
def holds_not(step):
    """The pull request does not hold the commit: the run exited 0, the commit is not reachable from the remote's
    batch branch, and its item's lines are not in that branch's spec (the lines commit laid them)."""
    (k1, _), (k2, commit) = parts(step)
    if (k1, k2) != ("pull request", "commit"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    call = _more().created(step)
    pushed = _more().remote_head(step, call[call.index("--head") + 1])
    sha = step.context["commits"][commit]
    assert pushed and sha not in T.git(step, "rev-list", pushed).split(), (step.text, sha)
    item = step.context["given"]["commit"][commit]["item"]
    spec = T.git(step, "show", "%s:%s" % (pushed, T.CAP))
    for group in step.context["laid"][item]:
        assert "### [%s] " % group not in spec, (step.text, group, spec)


@four("ThenDoes", "pick", *BOTH)
@four("ThenDoesNot", "pick", *BOTH)
def picks(step):
    """`work batch start` picked the item: it is `in-batch` in a plan the run wrote; or it exited 0 and the item is
    not `in-batch`."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    name = parts(step)[1][1]
    status = W.field(B.item_file(step, name), "status")
    if step.template == "ThenDoesNot":
        assert status != "in-batch", (step.text, status)
        return
    assert status == "in-batch", (step.text, status, done.stdout)
    plans = [rel for rel in B.changed(step) if rel.startswith(".shop/batches/") and rel.endswith("/plan.md")]
    assert plans and any(" %s " % B.ident(name) in (step.repo / rel).read_text() for rel in plans), (step.text, plans)


@four("ThenDoes", "holds", *BOTH)
def holds_item(step):
    """`the batch b2 holds the item i1` after a batch is opened (the reword of "`work` picks the item i1")."""
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("batch", "item"):
        return False
    picks(step)


@four("ThenDoes", "keep", *BOTH)
def keeps_lay(step):
    """`the batches service keeps the worktree w2` (the batch's workspace after a park) or `keeps the corpus c1` (after
    a batch is opened): the request was done; what it no longer holds is the next Then's."""
    if parts(step)[1][0] not in ("worktree", "corpus"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stderr)


@four("ThenDoesNot", "holds", *BOTH)
def holds_not_after(step):
    """`the worktree w2 does not hold the requirement r1`, `the corpus c1 does not hold the requirement r2`: the
    requirement removed, as the reword of "`work` removes the requirement r1" (the remove handlers')."""
    (k1, n1), (k2, name) = parts(step)
    if k1 not in ("worktree", "corpus") or k2 != "requirement":
        return False
    step.workspace = n1
    step.template, step.term, step.event = "ThenDoes", "remove", "remove"
    step.subject, step.nps, step.names = "`work`", ["the requirement %s" % name], [name]
    return F._chain(("ThenDoes", "remove"), frozenset(BOTH))(step)


@four("ThenDoes", "has", *BOTH)
@four("ThenDoes", "on", *BOTH)
def has_after(step):
    """`the batch b1 has the worktree w2` after a park (its workspace kept); `the comment e1 is on the request c1`, the
    entry a delivered item's context request was given (posted on its issue)."""
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) == ("batch", "worktree"):
        assert step.context["result"].returncode == 0, step.text
    elif (k1, k2) == ("comment", "request"):
        step.nps = [step.subject]
        return sys.modules["vocab"].lookup("ThenDoes", "post")(step)
    else:
        return False
