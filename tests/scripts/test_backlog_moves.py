"""backlog r2, r3, r9-r14, r16: the moves of an item's status, each one commit, a move from another status refused
naming it, and `work withdraw` and `work answer` on a work-item as before (workflow simplification plan 2, Task 2)."""
import subprocess

import backlog_items
import backlog_moves
import pytest
import spec_lexicon
from backlog_testing import REPO, git, state, work, write_item

MOVES = sorted((command, before, after) for command, row in backlog_moves.TRANSITIONS.items()
               for before, after in row.items())
REFUSED = sorted((command, status) for command, row in backlog_moves.TRANSITIONS.items()
                 for status in backlog_items.STATUSES if status not in row)


def args_of(command):
    """The command line of `work <verb> b1`, with the text it takes."""
    verb = command.split()[1]
    return [verb, "b1"] + {"refuse": ["out of scope"], "answer": ["The first"]}.get(verb, [])


@pytest.mark.parametrize("command, before, after", MOVES)
def test_each_move_follows_its_row(backlog_repo, command, before, after):
    write_item(backlog_repo, "b1", status=before)
    done = work(backlog_repo, *args_of(command))
    assert done.returncode == 0, done.stderr
    assert 'b1 "Fix the parser"' in done.stdout
    assert backlog_items.find(backlog_repo, "b1").status == after
    assert git(backlog_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    assert git(backlog_repo, "log", "-1", "--format=%s").strip() == '%s: b1 "Fix the parser" %s -> %s' % (
        command, before, after)


@pytest.mark.parametrize("command, status", REFUSED)
def test_a_move_from_another_status_is_refused_naming_it(backlog_repo, command, status):
    write_item(backlog_repo, "b1", status=status)
    before = state(backlog_repo)
    done = work(backlog_repo, *args_of(command))
    assert done.returncode == 1, done.stdout
    assert 'b1 "Fix the parser" is %s' % status in done.stderr, done.stderr
    assert state(backlog_repo) == before


def test_the_moves_are_the_glossary_transitions():
    status = next(t for t in spec_lexicon.read(REPO).of("attribute") if t.term == "status" and t.kinds == ("item",))
    ours = {"`%s`" % c for c in backlog_moves.TRANSITIONS}
    glossary = {(by.strip("`"), before.strip("`"), after.strip("`")) for before, after, by in status.transitions
                if by in ours}
    assert glossary == set(MOVES)


def test_answer_moves_the_question_under_answers(backlog_repo):
    write_item(backlog_repo, "b1", status="needs-input", body="\n## Question\n\nWhich?\n")
    done = work(backlog_repo, "answer", "b1", "The first")
    assert done.returncode == 0, done.stderr
    item = backlog_items.find(backlog_repo, "b1")
    assert "Question" not in item.sections and item.status == "shaped"
    assert item.sections["Answers"] == "- Q: Which?\n  A: The first"


def test_a_second_answer_is_added_under_the_first(backlog_repo):
    write_item(backlog_repo, "b1", status="needs-input",
               body="\n## Question\n\nAnd now?\n\n## Answers\n\n- Q: Which?\n  A: The first\n")
    assert work(backlog_repo, "answer", "b1", "Now").returncode == 0
    assert backlog_items.find(backlog_repo, "b1").sections["Answers"] == (
        "- Q: Which?\n  A: The first\n- Q: And now?\n  A: Now")


def test_refuse_writes_the_reason(backlog_repo):
    write_item(backlog_repo, "b1")
    assert work(backlog_repo, "refuse", "b1", "out of scope").returncode == 0
    assert backlog_items.find(backlog_repo, "b1").sections["Refused"] == "out of scope"


def test_shape_keeps_its_note(backlog_repo):
    write_item(backlog_repo, "b1")
    assert work(backlog_repo, "shape", "b1", "--note", "the lines are drafted").returncode == 0
    assert backlog_items.find(backlog_repo, "b1").sections["Notes"] == "the lines are drafted"


@pytest.mark.parametrize("verb, text", [("refuse", ""), ("refuse", "a\nb"), ("answer", ""), ("answer", "a\nb")])
def test_an_empty_or_multi_line_text_is_refused(backlog_repo, verb, text):
    write_item(backlog_repo, "b1", status="needs-input" if verb == "answer" else "idea")
    before = state(backlog_repo)
    done = work(backlog_repo, verb, "b1", text)
    assert done.returncode == 1 and done.stderr.startswith("work: "), done.stderr
    assert state(backlog_repo) == before


@pytest.mark.parametrize("flag", ["--change", "--accept"])
def test_an_item_answer_refuses_the_reviewer_flags(backlog_repo, flag):
    write_item(backlog_repo, "b1", status="needs-input")
    before = state(backlog_repo)
    done = work(backlog_repo, "answer", "b1", "x", flag)
    assert done.returncode == 1 and flag in done.stderr, done.stderr
    assert state(backlog_repo) == before


def test_a_move_of_an_item_there_is_not_is_refused(backlog_repo):
    done = work(backlog_repo, "shape", "b9")
    assert done.returncode == 1 and "there is no item b9" in done.stderr


def test_work_withdraw_on_a_work_item_is_unchanged(backlog_repo):
    path = backlog_repo / ".shop/work/i1/w1.md"
    path.parent.mkdir(parents=True)
    path.write_text("---\nid: work-item/x/w1\nkind: work-item\nstatus: withdrawn\n---\n\n# w1\n")
    git(backlog_repo, "add", "-A")
    git(backlog_repo, "commit", "-qm", "w1")
    before = state(backlog_repo)
    done = work(backlog_repo, "withdraw", "w1")
    assert done.returncode == 1 and "withdrawn" in done.stderr, done.stderr
    assert state(backlog_repo) == before


def test_work_answer_on_a_work_item_is_unchanged(backlog_repo):
    done = work(backlog_repo, "answer", "w3", "x", "--change")
    assert done.returncode == 1 and "w3" in done.stderr and "item" not in done.stderr.replace("work-item", ""), \
        done.stderr
    assert subprocess.run(["git", "status", "--porcelain"], cwd=backlog_repo, capture_output=True,
                          text=True).stdout == ""
