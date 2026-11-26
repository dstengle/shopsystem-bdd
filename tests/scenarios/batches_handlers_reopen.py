"""Handlers of a batch reopened with the person's finding (reviews r11, r12, b69): over batches_world's batch (one
`awaiting-merge` made so by batches_handlers_base_merge, with its clean review 1), each review finding the scenario
names written as a `fix now` finding on an in-batch item of the batch into a findings file beside the repository, and
`work batch reopen <batch> --finding <file>` run. The Thens, first in their chains, read the review the run committed
on the base: kept in the batch's folder, holding the finding."""
import sys

import backlog_items
import batch_findings
from plumbing import shop_files
from vocab import handler

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
parts = F.parts
first = next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith(
    "/batches_handlers_base_merge.py")).first     # loaded before this module: the glob is sorted


def title(name):
    return "the person's finding %s" % name


def findings_file(step, batch):
    """The findings file of the scenario's review findings, each `fix now` on an in-batch item of the batch."""
    items = [i for i, f in step.context["given"]["item"].items() if f.get("batch") == batch]
    item = next(B.ident(i) for i in items if backlog_items.find(step.repo, B.ident(i)).status == "in-batch")
    found = "\n\n".join("### Important fix now: %s\n- item: %s\n- where: src/%s.txt\nWhat the person found on the "
                        "pull request, and the fix." % (title(n), item, item)
                        for n in step.context["given"].get("review finding", {}))
    path = T.outside(step) / "person-findings.md"
    path.write_text("## Verdict\n\nThe person's comment on the pull request.\n\n## Findings\n\n%s\n" % found)
    return path


@handler("WhenRuns", "`work batch reopen`")
def batch_reopen(step):
    T.prepare(step)
    T.ensure_batch(step)
    batch = next(n for n in step.names if n in step.context["given"]["batch"])
    step.context["reopened"] = batch
    T.run_batch(step, "reopen", T.batch_name(step, batch), "--finding", str(findings_file(step, batch)))


def _review(step, name):
    return step.context.setdefault("reviews_kept", {}).get(name)


@first("ThenDoes", "keep")
@first("ThenDoes", "write")
def keeps_review(step):
    """`the batches service keeps the review r2`: the run exited 0 and its commit on the base added a review of the
    reopened batch."""
    if "reopened" not in step.context or len(parts(step)) < 2 or parts(step)[1][0] != "review":
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    added = T.git(step, "show", "--name-only", "--diff-filter=A", "--format=", "HEAD").split()
    batch = T.batch_name(step, step.context["reopened"])
    hits = [rel for rel in added if rel.startswith(".shop/batches/%s/review-" % batch.split("-")[1])]
    assert hits, (step.text, added)
    step.context.setdefault("reviews_kept", {})[parts(step)[1][1]] = hits[0]


@first("ThenDoes", "has")
def has_review(step):
    """`the batch b1 has the review r2`: the review kept is the batch's."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("batch", "review") or not _review(step, n2):
        return False
    rel = _review(step, n2)
    review = batch_findings.parse(shop_files.read(step.repo / rel, step.repo), rel)
    assert review.batch == T.batch_name(step, n1), (step.text, review.batch)
    assert rel == batch_findings.rel_of(review.batch, review.number), (step.text, rel)


@first("ThenDoes", "holds")
def holds_finding(step):
    """`the review r2 holds the review finding r1`: the review kept holds the finding as a `fix now` one."""
    (k1, n1), (k2, n2) = parts(step)
    if (k1, k2) != ("review", "review finding") or not _review(step, n1):
        return False
    rel = _review(step, n1)
    review = batch_findings.parse(shop_files.read(step.repo / rel, step.repo), rel)
    assert any(f.title == title(n2) and f.triage == "fix now" for f in review.findings), (step.text, review.findings)
