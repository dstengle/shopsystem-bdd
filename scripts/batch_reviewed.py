"""`work batch reviewed` (capability pr-review r5, r7; workflow simplification plan 5, D10, D12, D13): the findings
file `pr-reviewer` wrote for the batch's next review, recorded.

Under the lock: the batch is `in-review` on its base, the findings file is there and the batch branch is still at the
brief's `Head:`; the file parses against the batch's items and its open findings. The record
`.shop/batches/<n>/review-<k>.md` is rendered in the review's scratch directory and posted on the pull request
(`gh pr comment --body-file`); a clean review marks the pull request ready (`gh pr ready`). Last, the batch is
`building` while a finding is open, else `awaiting-merge`, committed on the base with the record. A gh that fails is
refused with nothing committed."""
import backlog_items
import batch_brief
import batch_findings
import batch_gh
import batch_plan
import workqueue
from batch_findings import Review
from batch_git import current_branch, git, locked
from workqueue import Refused

COMMAND = "work batch reviewed"


def _batch(root, name):
    batch = batch_plan.find(root, name)
    branch = current_branch(root)
    if branch != batch.base:
        raise Refused("%s: %s is built from %s; run it on %s, not %s" % (
            COMMAND, batch.name, batch.base, batch.base, branch or "a detached HEAD"))
    if batch.status != "in-review":
        raise Refused("%s: %s is %s; %s takes a batch that is in-review, after work batch brief and pr-reviewer" % (
            COMMAND, batch.name, batch.status, COMMAND))
    return batch


def _label(root, finding):
    try:
        return backlog_items.label(backlog_items.find(root, finding.item))
    except Refused:
        return finding.item


def _open_after(review, before):
    still = [f for f in before if review.earlier.get(f.fid) != "fixed"]
    return still + [f for f in review.findings if f.triage == "fix now"]


def reviewed(root, name):
    """The review recorded (D12)."""
    with locked(root):
        batch = _batch(root, name)
        done = batch_findings.reviews(root, batch.name)
        k = len(done) + 1
        where = batch_findings.scratch(root, batch.name, k)
        path = where / "findings.md"
        if not path.is_file():
            raise Refused("%s: %s has no findings file %s; run work batch brief %s, then the pr-reviewer agent on "
                          "its brief %s" % (COMMAND, batch.name, path, batch.name, where / "brief.md"))
        head = git(root, "rev-parse", batch.branch).stdout.strip()
        if not (where / "brief.md").is_file() or batch_brief.head_of(where / "brief.md") != head:
            raise Refused("%s: %s: the batch branch moved since the brief; run work batch brief %s again" % (
                COMMAND, batch.name, batch.name))
        items = {t.item: backlog_items.find(root, t.item) for t in batch.tasks}
        before = batch_findings.open_findings(root, batch.name)
        verdict, found, earlier = batch_findings.parse_findings(
            path.read_text(encoding="utf-8", errors="replace"), str(path), set(items), {n for n, i in items.items() if i.status == "in-batch"}, {f.fid for f in before})
        first = batch_findings.next_fid(root, batch.name)
        for m, finding in enumerate(found, first):
            finding.fid = "f%d" % m
        review = Review(number=k, batch=batch.name,
                        ident="review/%s/%s/review-%d" % (workqueue.context_path(root), batch.name, k),
                        pull_request=batch.pull_request, head=head,
                        range="%s..%s" % (done[-1].head if done else batch.forked_from, head),
                        result="fix-now", verdict=verdict, findings=found, earlier=earlier)
        still = _open_after(review, before)
        review.result = "fix-now" if still else "clean"
        text, body = batch_findings.render(review), where / ("review-%d.md" % k)
        body.write_text(text, encoding="utf-8")
        batch_gh.gh(root, "pr", "comment", batch.pull_request, "--body-file", str(body),
                    command=COMMAND)
        if not still:
            batch_gh.gh(root, "pr", "ready", batch.pull_request, command=COMMAND)
        batch.status = "building" if still else "awaiting-merge"
        said = "; open %s" % ", ".join("%s %s" % (f.fid, _label(root, f)) for f in still) if still else ""
        batch_plan.commit(root, batch, [], "%s: %s review %d -> %s%s" % (COMMAND, batch.name, k, batch.status, said),
                          files={batch_findings.rel_of(batch.name, k): text})
        return review


def said(root, review):
    """What `work batch reviewed` prints (D12), right after it: the findings still open."""
    still = batch_findings.open_findings(root, review.batch)
    fix = sum(f.triage == "fix now" for f in review.findings)
    if not still:
        return "%s review %d: %d findings -> awaiting-merge; the pull request %s is ready for the person's merge" % (
            review.batch, review.number, len(review.findings), review.pull_request)
    lines = ["%s review %d: %d findings, %d fix now -> building" % (review.batch, review.number, len(review.findings),
                                                                    fix)]
    lines += ["  open %s %s %s %s: %s" % (f.fid, f.grade, _label(root, f), f.where or "-", f.title) for f in still]
    return "\n".join(lines)


def status_line(root, batch):
    """`reviews: none`, or `reviews: <k>, last <result>; open f3 b2 "..."` (D15)."""
    done = batch_findings.reviews(root, batch.name)
    if not done:
        return "reviews: none"
    still = batch_findings.open_findings(root, batch.name)
    return "reviews: %d, last %s%s" % (len(done), done[-1].result, "; open %s" % ", ".join(
        "%s %s" % (f.fid, _label(root, f)) for f in still) if still else "")


def as_json(root, batch):
    return {"reviews": [{"review": r.number, "result": r.result, "findings": [f.fid for f in r.findings]}
                        for r in batch_findings.reviews(root, batch.name)],
            "open": [f.fid for f in batch_findings.open_findings(root, batch.name)]}
