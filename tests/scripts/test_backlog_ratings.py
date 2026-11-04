"""backlog r4, r5: `work rate` sets an item's ratings to the glossary's values, and `work depend` writes a dependency
in the item that needs it, refusing itself, a duplicate, an unknown item and a cycle (workflow simplification plan 2,
Task 3)."""
import backlog_items
import backlog_moves
import pytest
from backlog_testing import git, state, work, write_item


def test_rate_sets_each_given_rating(backlog_repo):
    write_item(backlog_repo, "b1")
    head = git(backlog_repo, "rev-parse", "HEAD")
    done = work(backlog_repo, "rate", "b1", "--value", "high-value", "--size", "small")
    assert done.returncode == 0, done.stderr
    item = backlog_items.find(backlog_repo, "b1")
    assert (item.value, item.size, item.urgency) == ("high-value", "small", None)
    assert git(backlog_repo, "rev-list", "--count", "%s..HEAD" % head.strip()).strip() == "1"
    assert git(backlog_repo, "log", "-1", "--format=%s").strip() == 'work rate: b1 "Fix the parser" value=high-value size=small'


@pytest.mark.parametrize("flag, value, allowed", [("--value", "high", "low-value, medium-value, high-value"),
                                                  ("--size", "high-value", "small, medium, large"),
                                                  ("--urgency", "small", "low-urgency, medium-urgency, high-urgency")])
def test_rate_refuses_a_value_of_another_attribute(backlog_repo, flag, value, allowed):
    write_item(backlog_repo, "b1")
    before = state(backlog_repo)
    done = work(backlog_repo, "rate", "b1", flag, value)
    assert done.returncode == 1 and allowed in done.stderr and done.stderr.startswith("work: "), done.stderr
    assert state(backlog_repo) == before


def test_rate_refuses_no_rating(backlog_repo):
    write_item(backlog_repo, "b1")
    before = state(backlog_repo)
    done = work(backlog_repo, "rate", "b1")
    assert done.returncode == 1 and 'b1 "Fix the parser"' in done.stderr, done.stderr
    assert state(backlog_repo) == before


@pytest.mark.parametrize("status", ["delivered", "refused", "withdrawn"])
def test_rate_refuses_a_closed_item(backlog_repo, status):
    write_item(backlog_repo, "b1", status=status)
    done = work(backlog_repo, "rate", "b1", "--size", "small")
    assert done.returncode == 1 and status in done.stderr, done.stderr


def test_depend_writes_the_dependency_in_the_needing_item(backlog_repo):
    b1 = write_item(backlog_repo, "b1")
    write_item(backlog_repo, "b2", title="Use the parser")
    text = b1.read_bytes()
    done = work(backlog_repo, "depend", "b2", "--on", "b1")
    assert done.returncode == 0, done.stderr
    assert backlog_items.find(backlog_repo, "b2").depends_on == ("b1",)
    assert b1.read_bytes() == text
    assert git(backlog_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b2.md"]
    assert git(backlog_repo, "log", "-1", "--format=%s").strip() == \
        'work depend: b2 "Use the parser" on b1 "Fix the parser"'


def test_depend_refuses_itself(backlog_repo):
    write_item(backlog_repo, "b1")
    before = state(backlog_repo)
    done = work(backlog_repo, "depend", "b1", "--on", "b1")
    assert done.returncode == 1 and 'b1 "Fix the parser"' in done.stderr, done.stderr
    assert state(backlog_repo) == before


def test_depend_refuses_a_cycle(backlog_repo):
    for n in (1, 2, 3):
        write_item(backlog_repo, "b%d" % n, title="T%d" % n)
    assert work(backlog_repo, "depend", "b1", "--on", "b2").returncode == 0
    assert work(backlog_repo, "depend", "b2", "--on", "b3").returncode == 0
    before = state(backlog_repo)
    done = work(backlog_repo, "depend", "b3", "--on", "b1")
    assert done.returncode == 1, done.stdout
    assert 'b3 "T3" -> b1 "T1" -> b2 "T2" -> b3 "T3"' in done.stderr, done.stderr
    assert state(backlog_repo) == before


def test_depend_refuses_an_unknown_item_and_a_duplicate(backlog_repo):
    write_item(backlog_repo, "b1")
    write_item(backlog_repo, "b2", depends_on="b1")
    before = state(backlog_repo)
    unknown = work(backlog_repo, "depend", "b2", "--on", "b7")
    assert unknown.returncode == 1 and "b7" in unknown.stderr, unknown.stderr
    twice = work(backlog_repo, "depend", "b2", "--on", "b1")
    assert twice.returncode == 1 and "already" in twice.stderr, twice.stderr
    assert state(backlog_repo) == before


def test_cycle_is_none_without_a_path_and_survives_a_hand_written_cycle(backlog_repo):
    write_item(backlog_repo, "b1", depends_on="b2")
    write_item(backlog_repo, "b2", depends_on="b1")
    write_item(backlog_repo, "b3")
    assert backlog_moves.cycle(backlog_repo, "b3", "b1") is None
    assert backlog_moves.cycle(backlog_repo, "b1", "b2") == ["b2", "b1"]
