"""A retired group's `Restates:` ids (b333): laying a retire that removes a group writes each 0.29 id it restated, and
that no group left restates, under the capability's `## Dropped` as `r<n>@0.29: retired with <cap>#r<m> by b<k>.`, so
`model restates` still finds it covered."""

import backlog_retires
import spec_read

TEXT = """---
id: capability/ex/ctx/queue
language: codified-2
retired: []
---

# Queue

## Behaviour

### [g1] One
Restates: r3@0.29, other#r9@0.29.
- [r1] When the person runs `work start`, `work` shall exit successfully.

### [g2] Two
Restates: r4@0.29.
- [r2] When the person runs `work stop`, `work` shall exit successfully.

### [g3] Three
Restates: r4@0.29.
- [r5] When the person runs `work list`, `work` shall exit successfully.
"""


def test_a_removed_groups_restated_ids_are_dropped_by_the_item():
    text = backlog_retires.lay(TEXT, "queue", ["r1"], "b7")
    assert "### [g1]" not in text
    assert text.endswith("## Dropped\n- r3@0.29: retired with queue#r1 by b7.\n"
                         "- other#r9@0.29: retired with queue#r1 by b7.\n")
    assert "retired: [g1, r1]" in text


def test_an_id_another_group_still_restates_is_not_dropped():
    text = backlog_retires.lay(TEXT, "queue", ["r2"], "b7")
    assert "## Dropped" not in text


def test_a_dropped_section_there_already_takes_the_entry_at_its_end():
    with_section = TEXT + "\n## Dropped\n- r8@0.29: retired with queue#r1 in 0.31.0 (old).\n\n## Notes\nkept\n"
    text = backlog_retires.lay(with_section, "queue", ["r1"], "b7")
    assert ("## Dropped\n- r8@0.29: retired with queue#r1 in 0.31.0 (old).\n- r3@0.29: retired with queue#r1 by b7.\n"
            "- other#r9@0.29: retired with queue#r1 by b7.\n\n## Notes\nkept\n") in text


def test_the_dropped_entries_read_and_cover_the_ids(tmp_path):
    path = tmp_path / "queue.md"
    path.write_text(backlog_retires.lay(TEXT, "queue", ["r1"], "b7"))
    found = spec_read.capability(path)
    assert not found.problems
    assert ("queue", 3, "retired with queue#r1 by b7.") in found.dropped
