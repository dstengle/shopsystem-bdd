"""The pull request review's findings file and its record `.shop/batches/<n>/review-<k>.md` (workflow simplification
plan 5, Task 1, D9, D10, D13, D22): the agent's file parsed and refused when ungraded or malformed, the record
round-tripped, and the open findings followed across the batch's reviews."""
import batch_findings
import batch_plan
import pytest
from backlog_testing import git, write_item
from batch_findings import Finding, Review
from workqueue import Refused

REL = "batch-1-review-2/findings.md"

EXAMPLE = """## Verdict

The batch builds both items; one finding to fix.

## Findings

### Important fix now: abandon leaves the initiative started
- item: b1
- where: scripts/work:12
The line says `abandoned`; the code writes `started`. Fix: set the status.

### Minor observation: the message could name the initiative
- item: -
- where: -
Reproduction: run it.

## Earlier findings
- f1: fixed
"""

FIRST = EXAMPLE.split("## Earlier findings")[0]


def parse(text, open_ids=("f1",), items=("b1", "b2"), in_batch=("b1", "b2")):
    return batch_findings.parse_findings(text, REL, set(items), set(in_batch), set(open_ids))


def test_a_findings_file_parses():
    verdict, findings, earlier = parse(EXAMPLE)
    assert verdict == "The batch builds both items; one finding to fix."
    assert findings == [
        Finding(None, "Important", "fix now", "abandon leaves the initiative started", "b1", "scripts/work:12",
                "The line says `abandoned`; the code writes `started`. Fix: set the status."),
        Finding(None, "Minor", "observation", "the message could name the initiative", None, None,
                "Reproduction: run it."),
    ]
    assert earlier == {"f1": "fixed"}


MALFORMED = {
    "no verdict": (EXAMPLE.replace("## Verdict\n\nThe batch builds both items; one finding to fix.\n\n", ""),
                   (), "## Verdict"),
    "empty verdict": (EXAMPLE.replace("The batch builds both items; one finding to fix.", ""), (), "## Verdict"),
    "grade": (FIRST.replace("### Important fix now", "### Major fix now"), (), "### Major fix now"),
    "triage": (FIRST.replace("### Important fix now", "### Important later"), (), "### Important later"),
    "fix now with no item": (FIRST.replace("- item: b1", "- item: -"), (), "- item: -"),
    "item outside the batch": (FIRST.replace("- item: b1", "- item: b9"), (), "- item: b9"),
    "fix now on a parked item": (FIRST.replace("- item: b1", "- item: b2"), ("b1",), "- item: b2"),
    "no title": (FIRST.replace(": abandon leaves the initiative started", ":"), (), "### Important fix now:"),
    "earlier on a first review": (EXAMPLE, (), "f1"),
    "an unknown section": (FIRST + "\n## Notes\n\nMore.\n", (), "## Notes"),
    "fix now with no text": (FIRST.replace("The line says `abandoned`; the code writes `started`. Fix: set the status.\n",
                                           ""), (), "abandon leaves the initiative started"),
}


@pytest.mark.parametrize("case", sorted(MALFORMED))
def test_malformed_findings_are_refused(case):
    text, in_batch, named = MALFORMED[case]
    with pytest.raises(Refused) as refused:
        parse(text, open_ids=(), in_batch=in_batch or ("b1", "b2"))
    said = str(refused.value)
    assert said.startswith(REL + ": ") and named in said, said


FENCED = """The diff:

```
## Behaviour
### [g1] Abandon
- [r5] An initiative is abandoned.
```

The heading is the spec's."""


def test_a_fenced_heading_is_the_findings_text():
    """Review S2: a `## ` or `### ` line inside a fenced block is text, in the file and in the record."""
    text = FIRST.replace("Fix: set the status.", "Fix: set the status.\n\n" + FENCED)
    _, findings, _ = parse(text, open_ids=())
    assert len(findings) == 2 and findings[0].body.endswith(FENCED)
    r = review(findings=[Finding("f2", "Important", "fix now", "t", "b1", None, FENCED)])
    assert batch_findings.parse(batch_findings.render(r), "x") == r


def test_none_is_no_findings():
    verdict, findings, earlier = parse("## Verdict\n\nClean.\n\n## Findings\n\nNone.\n", open_ids=())
    assert (verdict, findings, earlier) == ("Clean.", [], {})


RECORD = """---
id: review/ex.com/prod/ctx/batch-1/review-2
kind: review
batch: batch-1
pull_request: https://github.com/ex/ctx/pull/1
head: 4c1f00
range: 9a0e00..4c1f00
result: fix-now
---

# batch-1 review 2

## Verdict

One left.

## Findings

### f2 Important fix now: abandon leaves the initiative started
- item: b1
- where: scripts/work:12
The line says it.

## Earlier findings
- f1: fixed
"""


def review(number=2, findings=None, earlier=None, result="fix-now"):
    found = findings if findings is not None else [
        Finding("f2", "Important", "fix now", "abandon leaves the initiative started", "b1", "scripts/work:12",
                "The line says it.")]
    return Review(number=number, batch="batch-1", ident="review/ex.com/prod/ctx/batch-1/review-%d" % number,
                  pull_request="https://github.com/ex/ctx/pull/1", head="4c1f00", range="9a0e00..4c1f00",
                  result=result, verdict="One left.", findings=found,
                  earlier={"f1": "fixed"} if earlier is None else earlier)


def test_the_record_round_trips():
    r = review()
    assert batch_findings.render(r) == RECORD
    assert batch_findings.parse(RECORD, ".shop/batches/1/review-2.md") == r
    clean = review(1, findings=[], earlier={}, result="clean")
    assert batch_findings.parse(batch_findings.render(clean), "x") == clean
    assert batch_findings.rel_of("batch-1", 2) == ".shop/batches/1/review-2.md"


def finding(fid, triage, item):
    return Finding(fid, "Important", triage, "title %s" % fid, item, None, "text")


def records(root, second_f1):
    for name in ("b1", "b2"):
        write_item(root, name, title=name.upper(), status="in-batch", commit=False)
    one = review(1, [finding("f1", "fix now", "b1"), finding("f2", "observation", None)], {})
    two = review(2, [finding("f3", "fix now", "b2")], {"f1": second_f1})
    for r in (one, two):
        path = root / batch_findings.rel_of("batch-1", r.number)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(batch_findings.render(r))


def test_open_findings_follow_the_reviews(tmp_path):
    records(tmp_path, "fixed")
    assert [f.fid for f in batch_findings.open_findings(tmp_path, "batch-1")] == ["f3"]
    assert batch_findings.next_fid(tmp_path, "batch-1") == 4
    assert [r.number for r in batch_findings.reviews(tmp_path, "batch-1")] == [1, 2]
    records(tmp_path, "not fixed: still started")
    assert [f.fid for f in batch_findings.open_findings(tmp_path, "batch-1")] == ["f1", "f3"]
    write_item(tmp_path, "b2", title="B2", status="needs-input", commit=False)
    assert [f.fid for f in batch_findings.open_findings(tmp_path, "batch-1")] == ["f1"]
    assert batch_findings.next_fid(tmp_path, "batch-2") == 1


@pytest.mark.parametrize("status", ["merged", "abandoned"])
def test_a_closed_batch_has_no_open_finding(tmp_path, status):
    """Review M2: a closed batch's finding is not open, though its item is in-batch again in a later batch."""
    from test_batch_plan import batch
    records(tmp_path, "not fixed: still started")
    (tmp_path / batch_plan.rel_of("batch-1")).write_text(batch_plan.render(batch(status=status,
                                                                                   pull_request="https://x/pull/1")))
    assert batch_findings.open_findings(tmp_path, "batch-1") == []


def test_a_review_file_not_numbered_is_refused(tmp_path):
    path = tmp_path / ".shop/batches/1/review-x.md"
    path.parent.mkdir(parents=True)
    path.write_text(RECORD)
    with pytest.raises(Refused, match=r"\.shop/batches/1/review-x\.md"):
        batch_findings.reviews(tmp_path, "batch-1")


def test_commit_takes_files(backlog_repo):
    from test_batch_plan import batch
    b = batch()
    rel = batch_findings.rel_of("batch-1", 1)
    batch_plan.commit(backlog_repo, b, [], "with a review", files={rel: "the review\n"})
    shown = git(backlog_repo, "show", "--name-only", "--format=%s", "HEAD").split()
    assert shown == ["with", "a", "review", ".shop/batches/1/plan.md", rel]
    assert (backlog_repo / rel).read_text() == "the review\n"
