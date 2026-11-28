"""Two items retiring the lines of one group (b755): the second lay takes the group out whole."""

import backlog_retires

TEXT = """---
id: capability/ex/ctx/queue
language: codified-2
retired: []
---

# Queue

## Behaviour

### [g1] One
Restates: r3@0.29.
- [r1] When the person runs `work start`, `work` shall exit successfully.
- [r2] When the person runs `work stop`, `work` shall exit successfully.

### [g2] Two
- [r5] When the person runs `work list`, `work` shall exit successfully.
"""


def test_the_second_lay_takes_the_group_out_whole():
    laid = backlog_retires.lay(backlog_retires.lay(TEXT, "queue", ["r1"], "b1"), "queue", ["r2"], "b2")
    assert "### [g1]" not in laid and "retired: [r1, g1, r2]" in laid
