"""Handlers of a batch awaiting its merge whose workspace holds a base merge, or none (reviews r9, r10, b492): a batch
`awaiting-merge` is made with its pull request and one clean review whose head is the batch branch's head, pushed to
`origin`; when its workspace holds a base merge, a change is committed on `main` after that review and merged into the
batch branch (`--no-ff`), as a driver merges the base by hand. The Thens read what `work batch review` did: the batch
branch pushed with the merge on it, the plan's pull request kept and no other created, and the refusal naming the
batch."""
import sys

import batch_findings
import shop_files

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


def first(template, term):
    """`four`, the handler put first in its key's chain, before the handlers that read a batch built from its tasks."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


@four("GivenK", "base merge", *BOTH)
def given_base_merge(step):
    """The base merge, made once the batch is."""


@four("GivenDoes", "holds", *BOTH)
def holds_base_merge(step):
    """`the worktree w1 holds the base merge b2` (the batch's workspace merged its base), or `holds no base merge`."""
    if parts(step)[0][0] != "worktree" or not step.nps[0].endswith("base merge") and "base merge " not in step.nps[0]:
        return False
    step.context["base_merge"] = not step.nps[0].startswith("no ")


def awaiting(step, name):
    """The batch `awaiting-merge` (T.AFTER_BATCH): its pull request, its clean review at the branch's head, pushed,
    and, when its workspace holds one, a base merge after that review."""
    if step.context["given"]["batch"][name].get("status") != "awaiting-merge":
        return
    n = T.batch_name(step, name)
    url = T.URL % 1
    head = T.git(step, "rev-parse", n).strip()
    plan = step.repo / T.plan_rel(step, name)
    plan.write_text(plan.read_text().replace("pull_request:\n", "pull_request: %s\n" % url))
    review = batch_findings.Review(
        number=1, batch=n, ident="review/%s/%s/review-1" % (shop_files.context_path(step.repo), n),
        pull_request=url, head=head, range="%s..%s" % (W.field(plan, "forked_from"), head), result="clean",
        verdict="Clean.")
    (step.repo / batch_findings.rel_of(n, 1)).write_text(batch_findings.render(review))
    T.git(step, "add", "-A")
    T.git(step, "commit", "-q", "-m", "%s: review 1 -> awaiting-merge" % n)
    T.git(step, "push", "-q", "origin", n)
    step.context.setdefault("awaiting", {})[name] = head
    if not step.context.get("base_merge"):
        return
    (step.repo / "src").mkdir(exist_ok=True)
    (step.repo / "src" / "base.txt").write_text("a change on the base after the review\n")
    T.git(step, "add", "-A")
    T.git(step, "commit", "-q", "-m", "a change on the base")
    tree = T.outside(step) / ("merge-%s" % n)
    T.git(step, "worktree", "add", "-q", str(tree), n)
    T.git(step, "merge", "-q", "--no-ff", "-m", "Merge main into %s" % n, "main", cwd=tree)
    step.context.setdefault("merged", {})[name] = T.git(step, "rev-parse", "HEAD", cwd=tree).strip()
    T.git(step, "worktree", "remove", "--force", str(tree))


T.AFTER_BATCH.append(awaiting)


def _resubmitted(step):
    return bool(step.context.get("awaiting"))


@first("ThenDoes", "keep")
@first("ThenDoes", "write")
def keeps_resubmitted(step):
    """`the batches service keeps the proposed change p1` (`` `work` writes the pull request p1 ``) of a batch submitted
    again: the run exited 0 and the remote's
    batch branch holds the base merge."""
    if not _resubmitted(step) or parts(step)[1][0] != "pull request":
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    for name, merge in step.context.get("merged", {}).items():
        pushed = T.git(step, "ls-remote", "origin", "refs/heads/%s" % T.batch_name(step, name)).split()
        assert pushed and merge in T.git(step, "rev-list", pushed[0]).split(), (step.text, merge, pushed)


@first("ThenDoes", "has")
def has_resubmitted(step):
    """`the batch b1 has the proposed change p1`: the plan keeps the pull request it had, and gh created no other."""
    (k1, n1), (k2, _) = parts(step)
    if not _resubmitted(step) or (k1, k2) != ("batch", "pull request"):
        return False
    assert T.plan_field(step, n1, "pull_request") == T.URL % 1, step.text
    assert not [c for c in T.gh_calls(step) if c[:2] == ["pr", "create"]], (step.text, T.gh_calls(step))


@first("ThenDoes", "name")
def names_batch(step):
    """`the batches service names the batch b1`: the run was refused, naming the batch."""
    (_, _), (k, name) = parts(step)
    if k != "batch":
        return False
    done = step.context["result"]
    assert done.returncode != 0, (step.text, done.stdout)
    assert T.batch_name(step, name) in done.stderr, (step.text, done.stderr)
