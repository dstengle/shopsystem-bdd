"""`work line --reword` and `--remove` (b14): an item's own line given a new text under its id, or taken out with its
group when it was the last line and with the id it retires; a line the item does not hold refused, changing
nothing."""
import backlog_items
import backlog_lines
from backlog_section import Block, Group
from backlog_testing import git, work, write_item

LINE = ("While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall set the "
        "status of the initiative to `started` and commit the initiative.")
OTHER = ("While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set "
         "the status of the initiative to `abandoned`.")


def blocks(repo, name="b1"):
    return backlog_lines.read(backlog_items.find(repo, name), backlog_items.rel_of(name))


def test_reword_keeps_the_id_and_group_and_commits_the_item(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", LINE).returncode == 0
    done = work(ready_repo, "line", "b1", "--reword", "work-queue#r5", OTHER)
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": work-queue#r5 reworded\n'
    assert blocks(ready_repo) == [Block("work-queue", [], [Group("g4", "Fix the parser", [("r5", OTHER)])])]
    assert git(ready_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]


def test_remove_takes_the_line_its_group_and_the_id_it_retires(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", LINE).returncode == 0
    assert work(ready_repo, "line", "b1", "--in", "g4", "--into", "work-queue", OTHER).returncode == 0
    assert work(ready_repo, "line", "b1", "--retires", "work-queue#r1", "--group", "Retire the start",
                LINE).returncode == 0     # a group of its own: a plain line would join g4 (drafting#r65)
    assert work(ready_repo, "line", "b1", "--remove", "work-queue#r5").returncode == 0
    assert blocks(ready_repo) == [Block("work-queue", [], [Group("g4", "Fix the parser", [("r6", OTHER)]),
                                                           Group("g5", "Retire the start", [("r7", LINE)])], (),
                                        ("r1",), retires=(("r7", "r1"),))]
    done = work(ready_repo, "line", "b1", "--remove", "work-queue#r7")
    assert done.returncode == 0 and done.stdout == 'b1 "Fix the parser": work-queue#r7 removed\n', done.stderr
    assert blocks(ready_repo) == [Block("work-queue", [], [Group("g4", "Fix the parser", [("r6", OTHER)])])]
    assert work(ready_repo, "line", "b1", "--remove", "work-queue#r6").returncode == 0
    assert blocks(ready_repo) == []


def test_a_line_the_item_does_not_hold_is_refused_changing_nothing(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", LINE).returncode == 0
    head = git(ready_repo, "rev-parse", "HEAD")
    for args in (("--reword", "work-queue#r1", OTHER), ("--remove", "work-queue#r1"), ("--remove", "other#r5"),
                 ("--remove", "work-queue#g4")):
        done = work(ready_repo, "line", "b1", *args)
        assert done.returncode == 1 and args[1] in done.stderr, (args, done.stderr)
    for args in (("--reword", "work-queue#r5"), ("--remove", "work-queue#r5", OTHER),
                 ("--remove", "work-queue#r5", "--into", "work-queue")):
        assert work(ready_repo, "line", "b1", *args).returncode == 1, args
    assert git(ready_repo, "rev-parse", "HEAD") == head
