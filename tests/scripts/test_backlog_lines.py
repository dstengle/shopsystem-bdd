"""An item's requirement lines (workflow simplification plan 3, Task 1, D2-D5): the `## Requirements` block of an
item's file read and written, `work line` giving a new line the next ids of its capability, and the block laid over a
copy of `spec/`."""
import shutil

import backlog_items
import backlog_lines
import pytest
import spec_read
from backlog_lines import Block, Group
from backlog_testing import git, state, work, write_item

from conftest import GENERATE_SPEC

ABANDON = ("When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to "
           "`abandoned`.")
FROBNICATE = "When the person runs `work start` on an initiative that is `proposed`, `work` shall frobnicate the initiative."
DONE = "When the person runs `work start` on an initiative that is `proposed`, `work` shall set its status to `done`."
TERM = "- **frobnicate** (event): Forms: frobnicates, frobnicated. Frame: `work` frobnicates initiative."


def blocks(repo, name="b1"):
    item = backlog_items.find(repo, name)
    return backlog_lines.read(item, backlog_items.rel_of(name))


def test_line_writes_the_next_ids_and_commits_only_the_item(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON)
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": work-queue#r5\n'
    assert blocks(ready_repo) == [Block("work-queue", [], [Group("g4", "Fix the parser", [("r5", ABANDON)])])]
    assert git(ready_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    assert git(ready_repo, "log", "-1", "--format=%s").strip() == 'work line: b1 "Fix the parser" work-queue#r5'


def test_a_second_line_in_the_group_takes_the_next_requirement_id(ready_repo):
    write_item(ready_repo, "b1", status="idea")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON).returncode == 0
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--in", "g4", DONE)
    assert done.returncode == 0 and done.stdout.endswith("work-queue#r6\n"), done.stderr
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--group", "Another", FROBNICATE)
    assert done.returncode == 0 and done.stdout.endswith("work-queue#r7\n"), done.stderr
    assert blocks(ready_repo) == [Block("work-queue", [], [
        Group("g4", "Fix the parser", [("r5", ABANDON), ("r6", DONE)]), Group("g5", "Another", [("r7", FROBNICATE)])])]
    assert backlog_lines.ids(blocks(ready_repo)) == ["work-queue#r5", "work-queue#r6", "work-queue#r7"]


def test_ids_skip_the_retired(ready_repo):
    path = ready_repo / "spec" / "capabilities" / "work-queue.md"
    text = path.read_text().replace("retired: []", "retired: [r9]")
    text = text.replace("shall print every work-item whose status is not `green` or `withdrawn`.\n",
                        "shall print every work-item whose status is not `green` or `withdrawn`.\n"
                        "- [r8] When the person runs `work list`, `work` shall exit successfully.\n")
    path.write_text(text)
    git(ready_repo, "commit", "-qam", "r8 and a retired r9")
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON)
    assert done.returncode == 0, done.stderr
    assert done.stdout.endswith("work-queue#r10\n")


def test_line_refuses_a_capability_that_is_not_codified(ready_repo):
    shutil.copy(GENERATE_SPEC / "capabilities" / "legacy.md", ready_repo / "spec" / "capabilities" / "legacy.md")
    write_item(ready_repo, "b1", status="shaped")
    before = state(ready_repo)
    for capability in ("nothing", "legacy"):
        done = work(ready_repo, "line", "b1", "--into", capability, ABANDON)
        assert done.returncode == 1, done.stdout
        assert "no codified capability %s" % capability in done.stderr, done.stderr
        assert state(ready_repo) == before


@pytest.mark.parametrize("status", ["ready", "withdrawn"])
def test_line_refuses_an_item_that_is_not_idea_or_shaped(ready_repo, status):
    write_item(ready_repo, "b1", status=status)
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON)
    assert done.returncode == 1
    assert 'b1 "Fix the parser" is %s' % status in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_line_refuses_an_unknown_group_and_text_with_a_line_break(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--in", "g4", ABANDON)
    assert done.returncode == 1 and "g4" in done.stderr, done.stderr
    done = work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON + "\nmore")
    assert done.returncode == 1 and "line break" in done.stderr, done.stderr
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "# " + ABANDON)
    assert done.returncode == 1 and 'work line: b1 "' in done.stderr and "starts with #" in done.stderr, (
        done.stderr)
    assert state(ready_repo) == before


def test_term_writes_a_term_bullet(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--term", TERM)
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": a term of work-queue\n'
    assert blocks(ready_repo) == [Block("work-queue", [TERM], [])]
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--term", "- frobnicate")
    assert done.returncode == 1 and "- frobnicate" in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_render_round_trips_and_malformed_blocks_are_refused():
    b = [Block("work-queue", [TERM], [Group("g4", "One", [("r5", ABANDON), ("r6", DONE)]), Group("g5", "Two", [])]),
         Block("supervision", [], [Group("g9", "Three", [("r20", FROBNICATE)])])]
    text = backlog_lines.render(b)
    assert text.startswith("### work-queue\n\n%s\n\n#### [g4] One\n- [r5] " % TERM)
    item = backlog_items.Item("b1", "item/x/b1", "T", "shaped", "own", sections={"Requirements": text})
    assert backlog_lines.read(item, "b1.md") == b
    for bad in ("### work-queue\n- [r5] %s" % ABANDON,
                "### work-queue\n#### [g4] One\n- [r5] %s\n- [r5] %s" % (ABANDON, DONE),
                "a stray line"):
        item.sections["Requirements"] = bad
        with pytest.raises(backlog_items.Refused, match="b1.md: Requirements: "):
            backlog_lines.read(item, "b1.md")


def test_lay_puts_the_block_into_a_copy_of_spec(ready_repo, tmp_path):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", "--term", TERM).returncode == 0
    assert work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON).returncode == 0
    live = (ready_repo / "spec" / "capabilities" / "work-queue.md").read_bytes()
    into = tmp_path / "copy"
    assert backlog_lines.lay(ready_repo, backlog_items.find(ready_repo, "b1"), into) == ["work-queue"]
    cap = spec_read.capability(into / "spec" / "capabilities" / "work-queue.md")
    assert cap.problems == []
    g4 = next(g for g in cap.groups if g.id == "g4")
    assert [r.id for r in g4.requirements] == ["r5"]
    copied = (into / "spec" / "capabilities" / "work-queue.md").read_text()
    assert TERM in copied.split("## Terms", 1)[1].split("## Behaviour", 1)[0]
    assert (ready_repo / "spec" / "capabilities" / "work-queue.md").read_bytes() == live
    assert git(ready_repo, "status", "--porcelain", "--", "spec") == ""


def test_a_line_after_a_double_dash_is_the_line(ready_repo):
    """plan-3 review M9: `work line b1 --into CAP -- TEXT`, for a text that starts with `-`."""
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--", "-x " + ABANDON)
    assert done.returncode == 0, done.stderr
    assert [r for b in blocks(ready_repo) for g in b.groups for r in g.requirements] == [("r5", "-x " + ABANDON)]


def ready_lines(repo, name, text, title="Fix the parser"):
    write_item(repo, name, title=title, status="ready",
               body="\n## Requirements\n\n### work-queue\n\n#### [g4] %s\n- [r5] %s\n" % (title, text))
    return backlog_items.find(repo, name)


def test_renumber_moves_past_spec_and_taken(ready_repo):
    """plan 4, Task 2, D8: an item's ids moved past its capability's and those of the items picked before it."""
    item = ready_lines(ready_repo, "b1", ABANDON)
    taken = {}
    assert backlog_lines.renumber(ready_repo, item, taken) == []
    assert backlog_lines.ids(backlog_lines.read(item, "b1")) == ["work-queue#r5"]
    taken = {"work-queue": {"g4", "r5"}}
    assert backlog_lines.renumber(ready_repo, item, taken) == [("work-queue#g4", "work-queue#g5"),
                                                               ("work-queue#r5", "work-queue#r6")]
    assert backlog_lines.read(item, "b1")[0].groups[0].id == "g5"
    assert taken == {"work-queue": {"g4", "r5", "g5", "r6"}}
    path = ready_repo / "spec" / "capabilities" / "work-queue.md"
    text = path.read_text().replace("retired: []", "retired: [r7]").replace(
        "\n## Not yet", "\n### [g9] more\n- [r6] %s\n\n## Not yet" % DONE)
    path.write_text(text)
    item = ready_lines(ready_repo, "b2", ABANDON)
    assert backlog_lines.renumber(ready_repo, item, {"work-queue": {"r5"}}) == [("work-queue#r5", "work-queue#r8")]


def test_lay_with_others_lays_both(ready_repo, tmp_path):
    first = ready_lines(ready_repo, "b1", ABANDON)
    second = ready_lines(ready_repo, "b2", DONE)
    backlog_lines.renumber(ready_repo, second, {"work-queue": {"g4", "r5"}})
    live = (ready_repo / "spec" / "capabilities" / "work-queue.md").read_bytes()
    backlog_lines.lay(ready_repo, second, tmp_path / "copy", others=[first])
    cap = spec_read.capability(tmp_path / "copy" / "spec" / "capabilities" / "work-queue.md")
    assert cap.problems == [] and {"g4", "g5"} <= {g.id for g in cap.groups}
    assert (ready_repo / "spec" / "capabilities" / "work-queue.md").read_bytes() == live
