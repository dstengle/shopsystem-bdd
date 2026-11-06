"""More handlers of features/batches.feature (workflow simplification plan 4): `work batch resume` and a park (Task
4), over the world batches_handlers.py loads; see there."""
import json
import sys

from vocab import handler

W, B, T = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world"))
local = W.local
QUESTION = "Which reading holds?"


@handler("WhenRuns", "`work batch resume`")
def batch_resume(step):
    T.prepare(step)
    T.ensure_batch(step, resume=True)
    step.context["pending"] = [t for t in step.context["given"]["task"] if T.task_row(step, t)[0] == "pending"]
    T.run_batch(step, "resume", T.batch_name(step, step.names[-1]))


@handler("ThenDoes", "use")
def uses_plan(step):
    """The run named the batch's plan and every task of it, and each task that was pending is running in its
    worktree."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    batch = next(iter(step.context["given"]["batch"]))
    assert T.plan_rel(step, batch) in done.stdout, (step.text, done.stdout)
    for name in step.context["given"]["task"]:
        assert "\n%s " % T.task_id(step, name) in "\n" + done.stdout, (step.text, name, done.stdout)
    assert step.context["pending"], "no task was pending"
    for name in step.context["pending"]:
        status, branch = T.task_row(step, name)
        tree = step.repo / ".shop" / "worktrees" / ("%s-%s" % (T.batch_name(step, batch), T.task_id(step, name)))
        assert status == "running" and tree.is_dir(), (step.text, name, status, tree)
        assert T.git(step, "symbolic-ref", "--short", "HEAD", cwd=tree).strip() == branch


@handler("WhenHappens", "park")
def batch_parks(step):
    batch, item = step.names
    T.prepare(step)
    T.ensure_batch(step)
    T.run_batch(step, "park", T.batch_name(step, batch), B.ident(item), "--question", QUESTION)


@local("ThenDoes", "question")
def writes_question(step):
    """The last run gave an item's file a `## Question`; the question is that item's."""
    if step.term != "write" or not step.context.get("given"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    hits = [B.name_of(step.context, rel) for rel in filter(B.is_item_file, B.changed(step))
            if "\n## Question\n\n%s\n" % QUESTION in (step.repo / rel).read_text()]
    assert hits, (step.text, B.changed(step))
    step.context.setdefault("questions_written", {})[step.names[0]] = hits[0]


@local("ThenR", "question")
def question_on_item(step):
    question, item = step.names
    if step.term != "on" or question not in step.context.get("questions_written", {}):
        return False
    assert step.context["questions_written"][question] == item, (step.text, step.context["questions_written"])
    assert W.field(B.item_file(step, item), "status") == "needs-input", step.text


@handler("WhenRuns", "`work batch review`")
def batch_review(step):
    T.prepare(step)
    T.ensure_batch(step)
    T.run_batch(step, "review", T.batch_name(step, step.names[-1]))


@handler("GivenK", "commit")
def given_commit(step):
    T.given(step, "commit", step.names[0])


@handler("GivenK_C", "commit")
def given_uncited(step):
    assert step.text.endswith(" is uncited"), step.text
    T.given(step, "commit", step.names[0])["uncited"] = True


@handler("GivenK", "pull request")
def given_pull_request(step):
    T.given(step, "pull request", step.names[0])


def commit_of(step):
    commit, item = step.names
    T.given(step, "commit", commit)["item"] = item


def pull_request_of(step):
    pr, batch = step.names
    T.given(step, "batch", batch)
    T.given(step, "pull request", pr)["batch"] = batch


B.OF_GIVENS["commit"] = commit_of
B.OF_GIVENS["pull request"] = pull_request_of


def created(step):
    """The argv of the stand-in gh's last `pr create`."""
    calls = [c for c in T.gh_calls(step) if c[:2] == ["pr", "create"]]
    assert calls, ("no pull request was created", T.gh_calls(step))
    return calls[-1]


def remote_head(step, branch):
    found = T.git(step, "ls-remote", "origin", "refs/heads/%s" % branch).split()
    return found[0] if found else None


@handler("ThenDoes", "publish")
def publishes(step):
    """The run created a pull request through gh and pushed the batch's branch, as it is, to the remote."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    call = created(step)
    head = call[call.index("--head") + 1]
    assert remote_head(step, head) == T.git(step, "rev-parse", head).strip(), (step.text, head)
    step.context.setdefault("prs", {})[step.names[0]] = done.stdout.strip().splitlines()[-1]


@handler("ThenDoesNot", "publish")
def publishes_not(step):
    """The command exited 0, the commit is not reachable from the remote's batch branch, and the lines of its item are
    not in that branch's spec (plan 4 review, B1: the lines commit laid them)."""
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    sha = step.context["commits"][step.names[0]]
    pushed = remote_head(step, created(step)[created(step).index("--head") + 1])
    assert pushed and sha not in T.git(step, "rev-list", pushed).split(), (step.text, sha)
    item = step.context["given"]["commit"][step.names[0]]["item"]
    spec = T.git(step, "show", "%s:%s" % (pushed, T.CAP))
    for group in step.context["laid"][item]:
        assert "### [%s] " % group not in spec, (step.text, group, spec)


@local("ThenR", "pull request")
def pull_request_of_batch(step):
    if step.term != "of":
        return False
    call = created(step)
    assert call[call.index("--head") + 1] == T.batch_name(step, step.names[1]), (step.text, call)


@handler("ThenR", "cites")
def pull_request_cites(step):
    call = created(step)
    assert step.context["says"][step.names[1]] in call[call.index("--body") + 1], (step.text, call)


@local("WhenHappens", "pull request")
def merges_pull_request(step):
    """The person merges: `batch-<n>` merged into main with `--no-ff`, gh's state `MERGED` at that merge, then `work
    batch merged`. A local, not the registry's `merge`: supervision's fallback `WhenHappens` takes its own merges."""
    if step.term != "merge":
        return False
    T.prepare(step)
    T.ensure_batch(step)
    batch = next(f["batch"] for p, f in step.context["given"]["pull request"].items() if p == step.names[0])
    name = T.batch_name(step, batch)
    T.git(step, "merge", "-q", "--no-ff", name, "-m", "merge the pull request of %s" % name)
    oid = T.git(step, "rev-parse", "HEAD").strip()
    (T.outside(step) / "gh-state.json").write_text(json.dumps(
        {step.context["prs"][step.names[0]]: {"state": "MERGED", "mergeCommit": {"oid": oid}}}))
    T.run_batch(step, "merged", name)


@handler("WhenRuns", "`work batch abandon`")
def batch_abandon(step):
    T.prepare(step)
    T.ensure_batch(step)
    T.run_batch(step, "abandon", T.batch_name(step, step.names[-1]))


@handler("GivenK", "review folder")
def given_review_folder(step):
    T.given(step, "review folder", step.names[0])


def review_folder_of(step):
    folder, batch = step.names
    T.given(step, "batch", batch)
    T.given(step, "review folder", folder)["batch"] = batch


B.OF_GIVENS["review folder"] = review_folder_of


@local("ThenDoes", "review folder")
def removes_review_folder(step):
    """The run exited 0 and the review folder the world made for the batch is gone."""
    if step.term != "remove":
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stderr
    path = step.context["review_folders"][step.names[0]]
    assert not path.exists(), (step.text, sorted(p.name for p in path.iterdir()))
