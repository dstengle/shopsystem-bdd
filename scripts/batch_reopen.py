"""`work batch reopen <batch> --finding <file>` (reviews r11, r12, b69): a batch awaiting its merge taken back to
building with the person's finding on its pull request, kept as a review.

Under the lock: the batch is `awaiting-merge` on its base (else refused, naming the batch); the file is a findings
file (batch_findings' form: `## Verdict`, `## Findings` with at least one `fix now` finding on an item in-batch). The
review `.shop/batches/<n>/review-<k>.md` is recorded from it at the batch branch's head, its result `fix-now`; the
pull request goes back to a draft (`gh pr ready --undo`, as a clean review made it ready, design-decision 0100), and
the batch is `building`, committed on the base with the record. The person's comment is on the pull request already:
nothing is posted."""
from pathlib import Path

import backlog_items
import batch_findings
import batch_plan
from batch_findings import Review
from batch_git import current_branch, git, locked
from plumbing import batch_gh, shop_files
from plumbing.shop_files import Refused

COMMAND = "work batch reopen"


def _batch(root, name):
    batch = batch_plan.find(root, name)
    branch = current_branch(root)
    if branch != batch.base:
        raise Refused("%s: %s is built from %s; run it on %s, not %s" % (
            COMMAND, batch.name, batch.base, batch.base, branch or "a detached HEAD"))
    if batch.status != "awaiting-merge":
        raise Refused("%s: %s is %s; %s takes a batch that is awaiting-merge" % (
            COMMAND, batch.name, batch.status, COMMAND))
    return batch


def _findings(root, batch, path):
    if not Path(path).is_file():
        raise Refused("%s: %s: no findings file %s" % (COMMAND, batch.name, path))
    items = {t.item: backlog_items.find(root, t.item) for t in batch.tasks}
    in_batch = {n for n, i in items.items() if i.status == "in-batch"}
    before = batch_findings.open_findings(root, batch.name)
    try:
        verdict, found, earlier = batch_findings.parse_findings(
            Path(path).read_text(encoding="utf-8", errors="replace"), str(path), set(items), in_batch,
            {f.fid for f in before})
    except Refused as refused:
        raise Refused("%s: %s: %s" % (COMMAND, batch.name, refused)) from None
    if not any(f.triage == "fix now" for f in found):
        raise Refused("%s: %s: %s has no fix now finding, which a reopened batch is built back to fix" % (
            COMMAND, batch.name, path))
    return verdict, found, earlier


def reopen(root, name, path):
    """The person's finding kept as the batch's next review, the batch `building` (r11); refused unless the batch is
    `awaiting-merge` (r12)."""
    with locked(root):
        batch = _batch(root, name)
        verdict, found, earlier = _findings(root, batch, path)
        done = batch_findings.reviews(root, batch.name)
        k = len(done) + 1
        for m, finding in enumerate(found, batch_findings.next_fid(root, batch.name)):
            finding.fid = "f%d" % m
        head = git(root, "rev-parse", batch.branch).stdout.strip()
        review = Review(number=k, batch=batch.name,
                        ident="review/%s/%s/review-%d" % (shop_files.context_path(root), batch.name, k),
                        pull_request=batch.pull_request, head=head,
                        range="%s..%s" % (done[-1].head if done else batch.forked_from, head),
                        result="fix-now", verdict=verdict, findings=found, earlier=earlier)
        text = batch_findings.render(review)
        if batch.pull_request:
            batch_gh.gh(root, "pr", "ready", "--undo", batch.pull_request, command=COMMAND)
        batch.status = "building"
        batch_plan.commit(root, batch, [], "%s: %s review %d -> building; open %s" % (
            COMMAND, batch.name, k, ", ".join(f.fid for f in found if f.triage == "fix now")),
            files={batch_findings.rel_of(batch.name, k): text})
        return review
