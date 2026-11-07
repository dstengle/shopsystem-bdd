"""The `pr-reviewer` agent (workflow simplification plan 5, Task 5, D2, D9, D24): the one review of a batch's pull
request, from the brief `work batch brief` wrote. Its pinned sentences hold pr-review r3, r4, r6 and r8, and its tools
keep it to reading: its findings travel as its reply, which the batch session saves (plan 7 review, B1)."""
import re

import batch_findings
import pytest
from test_agents import AGENTS, definition

PATH = AGENTS / "pr-reviewer.md"


def text():
    return " ".join(PATH.read_text().split())


def has(sentence):
    assert " ".join(sentence.split()) in text(), sentence


@pytest.mark.requirement("pr-review#r3")
def test_r3_the_reviewer_reads_the_items_lines_and_only_the_batchs_commits():
    has("Read every requirement the brief's `## Items` gives and every commit its `## Commits` lists, with their "
        "change in `change.diff`; read no other commit.")
    has("You have no shell: a commit the brief does not give is outside the batch, and you do not read it.")
    assert definition(PATH)["tools"] == ["Read", "Glob", "Grep"]


@pytest.mark.requirement("pr-review#r4")
def test_r4_the_reviewer_reads_every_judgement_decision():
    has("Read every design-decision the brief's `## Judgement decisions` lists, and check the change against each.")


@pytest.mark.requirement("pr-review#r6")
def test_r6_the_re_review_reads_every_commit_for_each_finding():
    has("On a re-review, read every commit the brief lists under each finding of `## Earlier findings`, and write "
        "`fixed` or `not fixed: <why>` for each.")
    has("On a re-review, a new finding is `fix now` only when the fix's own change is wrong.")


def example():
    """The first fenced block after the findings file's heading."""
    body = PATH.read_text().split("## The findings file", 1)[1]
    return re.search(r"```[a-z]*\n(.*?)```", body, re.DOTALL).group(1)


@pytest.mark.requirement("pr-review#r9")
def test_r9_each_finding_is_graded_and_written_to_the_findings_file():
    has("Give every finding a grade (`Critical`, `Important` or `Minor`) and a triage (`fix now`, `observation` or "
        "`drop`), and give them in the findings file's content, your reply.")
    verdict, found, earlier = batch_findings.parse_findings(example(), "pr-reviewer.md", {"b1"}, {"b1"}, {"f1"})
    assert verdict and found and earlier == {"f1": "fixed"}
    assert all(f.grade in batch_findings.GRADES for f in found)


def test_the_reviewer_changes_nothing_and_starts_no_agent():
    one = definition(PATH)
    assert not {"Write", "Edit", "NotebookEdit", "Agent", "Task", "Bash"} & set(one["tools"])
    assert one["model"] == "opus" and one["name"] == "pr-reviewer"


def test_the_reviewer_reads_each_commits_own_patch():
    """Review S4."""
    has("Each commit's own change is the patch its line names (`patch: <path>`): read it to see what that commit "
        "did, and `change.diff` for the range's net change.")


def test_a_run_failing_at_the_base_already_is_no_fix_now_finding():
    """Review S5."""
    has("**The runs**: a check that exited other than 0 at `Head:` and 0 at the base (`Exit code: 1 (base: 0)`) is a "
        "finding, with the lines of its output that show why; one that exited other than 0 at the base too is not "
        "the batch's, and is at most an `observation`.")


def test_the_findings_travel_as_the_reply():
    """Plan 7 review, B1 and the rulings' Q1: the harness refuses a subagent's Write of a findings file, so the reply is
    the findings file's content, which the batch session saves byte for byte."""
    has("Your final reply is the findings file's content and nothing else, starting at `## Verdict`.")
    assert "Write it in exactly this form" not in text()
