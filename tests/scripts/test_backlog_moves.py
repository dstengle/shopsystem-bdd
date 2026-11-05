"""backlog r2, r3, r9-r14, r16: the moves of an item's status, each one commit, a move from another status refused
naming it (workflow simplification plan 2, Task 2)."""

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


# `work ready` moves only an item that passes the bar: test_readiness_bar.py's test_ready_readies_a_passing_item.
@pytest.mark.parametrize("command, before, after", [m for m in MOVES if m[0] != "work ready"])
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


def test_a_move_of_an_item_there_is_not_is_refused(backlog_repo):
    done = work(backlog_repo, "shape", "b9")
    assert done.returncode == 1 and "there is no item b9" in done.stderr


def test_drop_removes_a_dependency(backlog_repo):
    """plan 4, D27: `work depend B --drop A`."""
    write_item(backlog_repo, "b1", title="First")
    write_item(backlog_repo, "b2", title="Second", depends_on="b1")
    head = git(backlog_repo, "rev-parse", "HEAD").strip()
    done = work(backlog_repo, "depend", "b2", "--drop", "b1")
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b2 "Second" no longer depends on b1 "First"\n'
    assert backlog_items.find(backlog_repo, "b2").depends_on == ()
    assert len(git(backlog_repo, "rev-list", "%s..HEAD" % head).split()) == 1


def test_drop_of_a_missing_item(backlog_repo):
    write_item(backlog_repo, "b2", title="Second", depends_on="b9")
    done = work(backlog_repo, "depend", "b2", "--drop", "b9")
    assert done.returncode == 0 and done.stdout == 'b2 "Second" no longer depends on b9 (missing)\n', done.stderr


def test_drop_refuses_one_it_lacks(backlog_repo):
    write_item(backlog_repo, "b1", title="First")
    write_item(backlog_repo, "b2", title="Second")
    before = state(backlog_repo)
    done = work(backlog_repo, "depend", "b2", "--drop", "b1")
    assert done.returncode == 1 and 'b2 "Second" does not depend on b1' in done.stderr, done.stderr
    assert state(backlog_repo) == before


@pytest.mark.parametrize("flags", [(), ("--on", "b1", "--drop", "b1")])
def test_depend_takes_on_or_drop(backlog_repo, flags):
    write_item(backlog_repo, "b1")
    write_item(backlog_repo, "b2")
    assert work(backlog_repo, "depend", "b2", *flags).returncode == 2
