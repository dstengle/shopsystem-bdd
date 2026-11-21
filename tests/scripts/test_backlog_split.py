"""`work retitle` and `work split` (b459): a title replaced under the item's id; lines moved to a new item that derives
from the old one, with their group, given block and the id they retire; refusals changing nothing."""
import backlog_items
from backlog_testing import git, state, work, write_item

SECTION = """
## Requirements

### notes
retired: [r1]
retires: [r8 r1]

#### [g3] Two lines
- [r7] The first line.
- [r8] The second line.

```given
the file `a` holds "1"
```
"""


def test_retitle_keeps_the_id_and_commits_only_the_item(backlog_repo):
    write_item(backlog_repo, "b1", status="ready")
    done = work(backlog_repo, "retitle", "b1", "Parse every file")
    assert done.returncode == 0 and done.stdout == 'b1 "Parse every file"\n', done.stderr
    assert backlog_items.find(backlog_repo, "b1").title == "Parse every file"
    assert git(backlog_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]


def test_retitle_of_a_closed_item_is_refused_naming_it(backlog_repo):
    write_item(backlog_repo, "b1", status="delivered")
    before = state(backlog_repo)
    done = work(backlog_repo, "retitle", "b1", "Parse every file")
    assert done.returncode == 1 and 'b1 "Fix the parser"' in done.stderr
    assert state(backlog_repo) == before


def test_split_moves_the_line_with_its_group_given_and_retirement(backlog_repo):
    write_item(backlog_repo, "b1", status="shaped", value="high-value", body=SECTION)
    done = work(backlog_repo, "split", "b1", "--requirement", "notes#r8")
    assert done.returncode == 0, done.stderr
    old, new = backlog_items.find(backlog_repo, "b1"), backlog_items.find(backlog_repo, "b2")
    assert "r8" not in old.sections["Requirements"] and "retired" not in old.sections["Requirements"]
    assert "- [r7] The first line." in old.sections["Requirements"]
    assert new.sections["Requirements"] == ('### notes\n\nretired: [r1]\nretires: [r8 r1]\n\n#### [g3] Two lines\n'
                                            '- [r8] The second line.\n\n```given\nthe file `a` holds "1"\n```')
    assert (new.derives_from, new.status, new.value) == ("b1", "shaped", "high-value")
    assert sorted(git(backlog_repo, "show", "--name-only", "--format=", "HEAD").split()) == [
        ".shop/backlog/b1.md", ".shop/backlog/b2.md"]


def test_split_refuses_a_line_the_item_does_not_hold_and_an_item_past_shaped(backlog_repo):
    write_item(backlog_repo, "b1", status="shaped", body=SECTION)
    write_item(backlog_repo, "b3", status="ready", body=SECTION)
    before = state(backlog_repo)
    done = work(backlog_repo, "split", "b1", "--requirement", "notes#r9")
    assert done.returncode == 1 and "notes#r9" in done.stderr
    done = work(backlog_repo, "split", "b3", "--requirement", "notes#r8")
    assert done.returncode == 1 and 'b3 "Fix the parser"' in done.stderr
    assert state(backlog_repo) == before
