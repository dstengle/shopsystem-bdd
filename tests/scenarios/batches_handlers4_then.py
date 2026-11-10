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
    if k == "question":
        return _more().writes_question(step)
    return False


@four("ThenDoes", "on", *BOTH)
def question_on(step):
    """The run wrote the question into the item's file, and the item is `needs-input`."""
    (k1, question), (k2, item) = parts(step)
    if (k1, k2) != ("question", "item") or not step.context.get("given"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    text = "\n## Question\n\n%s\n" % _more().QUESTION
    hits = [B.name_of(step.context, rel) for rel in filter(B.is_item_file, B.changed(step))
            if text in (step.repo / rel).read_text()]
    assert hits == [item], (step.text, hits)
    assert W.field(B.item_file(step, item), "status") == "needs-input", step.text
    step.context.setdefault("questions_written", {})[question] = item


@four("ThenDoes", "remove", *BOTH)
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
