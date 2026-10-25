"""supervision's steps about the answers a work-item carries (r57) and the work-item branch `work run` keeps (r58)."""
import json

from pytest_bdd import given, parsers, then

from .supervision_then_workers import brief_lines
from .supervision_world import (
    calls,
    commit_all,
    git,
    item_text,
    starts,
    work_item_of,
    write,
)


@given(parsers.re(r'i1\'s work-item (?P<name>\w+) is (?P<status>[\w-]+), its ## Questions section with "(?P<q1>[^"]+)" and '
                  r'"(?P<q2>[^"]+)", and its Answers section with "(?P<a1>[^"]+)" and "(?P<a2>[^"]+)"$'))
def item_with_answers(repo, name, status, q1, q2, a1, a2):
    text = item_text(name, status) + "\n## Questions\n- %s\n- %s\n\n## Answers\n- %s\n- %s\n" % (q1, q2, a1, a2)
    write(repo, ".shop/work/i1/%s.md" % name, text)
    commit_all(repo, "%s with questions and answers" % name)


@then(parsers.re(r'each of w1\'s four briefs holds "(?P<q1>[^"]+)" with "(?P<a1>[^"]+)" and "(?P<q2>[^"]+)" with "(?P<a2>[^"]+)"$'))
def briefs_hold_answers(repo, context, q1, a1, q2, a2):
    started = [c for c in starts(repo) if work_item_of(c) == "w1"]
    assert len(started) == 4, (started, context["done"].stderr)
    for c in started:
        lines = c["brief"].splitlines()
        for q, a in ((q1, a1), (q2, a2)):
            at = [i for i, l in enumerate(lines) if q in l]
            assert at and any(a in l for l in lines[at[0]:at[0] + 3]), (q, a, c["brief"])


REVIEW = ".shop/work/i1/runs/w1/3-review"


@given(parsers.re(r'i1\'s work-item w1 was awaiting-answer on its reviewer\'s question "(?P<q>[^"]+)", the reviewer having '
                  r"written findings\.md beside its brief$"))
def reviewer_asked(repo, context, q):
    context["question"] = q
    write(repo, REVIEW + "/brief.md", "# review of w1\n")
    write(repo, REVIEW + "/findings.md", "The old reader is still called.\n")
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- %s\n" % q)
    commit_all(repo, "w1 awaiting-answer on its reviewer's question")


@given(parsers.re(r'the answer "(?P<a>[^"]+)" to "(?P<q>[^"]+)" returned w1 to ready$'))
def answer_returned_to_ready(repo, a, q):
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "ready") + "\n## Questions\n- %s\n\n## Answers\n- %s\n" % (q, a))
    steps = [("ready", "claimed"), ("claimed", "done"), ("done", "awaiting-answer"), ("awaiting-answer", "ready")]
    write(repo, ".shop/work/i1/log.jsonl", "".join(
        json.dumps({"time": "2026-10-19T10:0%d:00+00:00" % n, "work-item": "w1", "before": b, "after": a_,
                    "by": "work answer" if a_ == "ready" else "work run"}) + "\n" for n, (b, a_) in enumerate(steps)))
    commit_all(repo, "w1 returned to ready by an answer")


@then(parsers.re(r'the implementer of w1 was given the reviewer\'s findings\.md, and the question "(?P<q>[^"]+)" with the '
                 r'answer "(?P<a>[^"]+)"$'))
def implementer_given_findings(repo, context, q, a):
    started = [c for c in starts(repo) if work_item_of(c) == "w1" and c["agent"].endswith("bdd-implementer")]
    assert len(started) == 1, (started, context["done"].stderr)
    lines = started[0]["brief"].splitlines()
    assert any(l.strip().endswith("-review/findings.md") and "Read (paths" not in l and not l.startswith("- ") for l in lines), lines
    at = [i for i, l in enumerate(lines) if q in l]
    assert at and any(a in l for l in lines[at[0]:at[0] + 3]), (q, a, started[0]["brief"])


@given(parsers.re(r"i1's work-item (?P<name>\w+) is ready, and the branch work/(?P=name) was kept with a commit of (?P<path>\S+)$"))
def kept_branch(repo, plan, name, path):
    plan["bdd-implementer"] = {"watch": [path]}     # the stand-in records what the file holds in its worktree
    write(repo, ".shop/work/i1/%s.md" % name, item_text(name, "ready"))
    commit_all(repo, "%s ready" % name)
    git(repo, "checkout", "-q", "-b", "work/" + name)
    write(repo, path, "kept\n")
    commit_all(repo, "kept work on %s" % name)
    git(repo, "checkout", "-q", "main")


@then(parsers.re(r"the implementer of (?P<name>\w+) worked in a worktree on the branch work/(?P=name), with (?P<path>\S+) in it$"))
def implementer_on_kept(repo, context, name, path):
    seen = [c for c in calls(repo, ("seen",)) if c["agent"].endswith("bdd-implementer")]
    started = [c for c in starts(repo) if c["agent"].endswith("bdd-implementer")]
    assert len(started) == 1 and len(seen) == 1, (started, context["done"].stderr)
    assert brief_lines(started[0]["brief"]).get("Branch") == "work/" + name, started[0]["brief"]
    assert seen[0]["seen"][path] == "kept\n", seen
