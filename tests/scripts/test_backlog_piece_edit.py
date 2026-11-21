"""`work line --remove-universal`, `--replace-universal`, `--remove-upstream`, `--replace-upstream`, `--remove-given`
and `--replace-given` (b48): an item's own universal condition, upstream entry or given block taken out or replaced,
one commit of the item; one the item does not hold, or a replacement that does not conform, refused, changing
nothing."""
import backlog_items
import backlog_lines
import pytest
from backlog_testing import git, state, work, write_item
from test_backlog_forms import ABANDON, GIVEN, UNIVERSAL, UPSTREAM

OTHER_UP = "bounded-context/ex.com/prod/other: another, github: ex/other"


@pytest.fixture
def held(ready_repo):
    """b1 holding a line of work-queue with a given block, a universal condition U<n> and two upstream entries."""
    write_item(ready_repo, "b1", status="shaped")
    for args in (("--into", "work-queue", ABANDON), ("--into", "work-queue", "--given", "g4", GIVEN),
                 ("--universal", UNIVERSAL), ("--upstream", UPSTREAM), ("--upstream", OTHER_UP)):
        assert work(ready_repo, "line", "b1", *args).returncode == 0
    return ready_repo


def _blocks(repo):
    return backlog_lines.read(backlog_items.find(repo, "b1"), "b1")


def _ident(repo):
    return _blocks(repo).universal[0][0]


def test_each_piece_goes_in_one_commit_of_the_item(held):
    ident = _ident(held)
    for args in (("--remove-universal", "universal#" + ident), ("--remove-upstream", "bounded-context/ex.com/prod/up"),
                 ("--remove-given", "work-queue#g4")):
        done = work(held, "line", "b1", *args)
        assert done.returncode == 0 and "removed" in done.stdout, done.stderr
        assert git(held, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    blocks = _blocks(held)
    assert blocks.universal == [] and blocks.upstreams == [OTHER_UP] and blocks[0].groups[0].given == ()


def test_a_replacement_keeps_its_place(held):
    ident = _ident(held)
    assert work(held, "line", "b1", "--replace-universal", ident, "`work` shall commit every move.").returncode == 0
    new_up = "bounded-context/ex.com/prod/up: the upstream, github: ex/up2"
    assert work(held, "line", "b1", "--replace-upstream", "bounded-context/ex.com/prod/up", new_up).returncode == 0
    new_given = "the file `notes.md` holds:\n  Another line."
    assert work(held, "line", "b1", "--replace-given", "work-queue#g4", new_given).returncode == 0
    blocks = _blocks(held)
    assert blocks.universal == [(ident, "`work` shall commit every move.")]
    assert blocks.upstreams == [new_up, OTHER_UP] and blocks[0].groups[0].given == tuple(new_given.split("\n"))


@pytest.mark.parametrize("args, said", [
    (("--remove-universal", "U99"), "universal condition U99"),
    (("--remove-upstream", "bounded-context/ex.com/prod/none"), "upstream entry bounded-context/ex.com/prod/none"),
    (("--remove-given", "work-queue#g9"), "given block work-queue#g9"),
    (("--replace-upstream", "bounded-context/ex.com/prod/up", OTHER_UP), "is an upstream already"),
    (("--replace-upstream", "bounded-context/ex.com/prod/up", "no id here"), "malformed"),
    (("--replace-given", "work-queue#g4", "not example data"), "malformed"),
    (("--replace-universal", "U1"), "takes the universal condition"),
    (("--remove-universal", "U1", "--universal", UNIVERSAL), "take one of them"),
])
def test_a_piece_not_held_or_malformed_is_refused(held, args, said):
    before = state(held)
    done = work(held, "line", "b1", *args)
    assert done.returncode == 1 and said in done.stderr and "usage:" not in done.stderr, done.stderr
    assert state(held) == before
