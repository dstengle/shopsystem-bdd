"""An item amended with the review finding it fixes (batches r125, b600), over batches_world's batch: a review of
the batch (`.shop/batches/<n>/review-1.md`, recorded at the batch branch's head) holding each review finding the
scenario names as a `fix now` finding on the in-batch item, and batches_handlers_amend's `work batch amend` run
with `--finding f<m>`, the finding's number in that review. The Thens read the amend's commit on the item's task
branch, which `work batch review` checks (batch_fix): kept, citing the item, and for the finding (`Finding: f<m>`)."""
import sys

import batch_findings
import shop_files

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")


@four("GivenDoes", "has", *BOTH)
def has_review(step):
    """`the batch b1 has the review r1`."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("batch", "review"):
        return False
    T.given(step, "batch", n1)
    T.given(step, "review", n2)["batch"] = n1


@four("GivenDoes", "holds", *BOTH)
def holds_finding(step):
    """`the review r1 holds the review finding r2`: one of its findings, numbered in the order the Givens say them."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("review", "review finding"):
        return False
    held = T.given(step, "review finding", n2)
    held["review"] = n1
    held["fid"] = "f%d" % len(step.context["given"]["review finding"])


def fids(step):
    """{review finding: f<m>} of the scenario's review findings."""
    return {n: f["fid"] for n, f in step.context.get("given", {}).get("review finding", {}).items() if "fid" in f}


def recorded(step, name):
    """The batch's review (T.AFTER_BATCH): each review finding a `fix now` finding on the batch's in-batch item, at
    the batch branch's head, committed on the base."""
    reviews = [r for r, f in step.context["given"].get("review", {}).items() if f.get("batch") == name]
    if not reviews:
        return
    n = T.batch_name(step, name)
    item = next(B.ident(i) for i, f in step.context["given"]["item"].items()
                if f.get("batch") == name and T.status_of(step, i) == "in-batch")
    head = T.git(step, "rev-parse", n).strip()
    plan = step.repo / T.plan_rel(step, name)
    findings = [batch_findings.Finding(fid=f["fid"], grade="Important", triage="fix now", title="the finding %s" % r,
                                       item=item, where="src/%s.txt" % item, body="What the review found.")
                for r, f in step.context["given"].get("review finding", {}).items() if f.get("review") in reviews]
    review = batch_findings.Review(
        number=1, batch=n, ident="review/%s/%s/review-1" % (shop_files.context_path(step.repo), n),
        pull_request=T.URL % 1, head=head, range="%s..%s" % (W.field(plan, "forked_from"), head), result="fix-now" if findings else "clean",
        verdict="A fix is due." if findings else "Nothing to fix.", findings=findings)
    (step.repo / batch_findings.rel_of(n, 1)).write_text(batch_findings.render(review))
    T.git(step, "add", "-A")
    T.git(step, "commit", "-q", "-m", "%s: review 1 -> building" % n)


T.AFTER_BATCH.append(recorded)


def _amended(step):
    done = step.context.get("result")
    return bool(fids(step)) and done is not None and "amend" in done.args


def _task_head(step):
    """The amend's commit: the head of the amended item's task branch."""
    task = next(t for t, f in step.context["given"]["task"].items() if f["item"] in step.context["given"]["item"])
    return T.task_row(step, task)[1]


@four("ThenDoes", "commit", *BOTH)
@four("ThenDoes", "write", *BOTH)
def keeps_change(step):
    """`the batches service keeps the kept change k1`: the amend exited 0, and its commit on the item's task branch
    cites the item."""
    if not _amended(step) or not step.nps or F.kind(step.nps[-1])[0] != "commit":
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branch = _task_head(step)
    message = T.git(step, "log", "-1", "--format=%B", branch)
    item = branch.rsplit("-", 1)[1]
    assert "Item: %s" % item in message.splitlines(), (step.text, branch, message)
    step.context.setdefault("kept", {})[step.names[-1]] = T.git(step, "rev-parse", branch).strip()


@four("ThenDoes", "for", *BOTH)
def change_for(step):
    """`the kept change k1 is for the review finding r2`: its message's trailers cite the finding (`Finding: f<m>`),
    as batch_fix reads them."""
    if len(step.names) != 2 or step.names[0] not in step.context.get("kept", {}):
        return False
    change, finding = step.names
    sha = step.context["kept"][change]
    cited = T.git(step, "log", "-1", "--format=%(trailers:key=Finding,valueonly)", sha).split()
    assert fids(step)[finding] in cited, (step.text, sha, T.git(step, "log", "-1", "--format=%B", sha))
