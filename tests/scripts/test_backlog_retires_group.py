"""Two items retiring the lines of one group (b755, laying r5): the second lay takes the group out whole; unlaying
either item puts the group back holding only that item's own line, the other's still retired, and unlaying the other
after it gives the file back as it was."""
import subprocess

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


def committed(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    path = tmp_path / "queue.md"
    path.write_text(TEXT)
    subprocess.run(["git", "-C", str(tmp_path), "add", "queue.md"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "q"],
                   check=True)
    return path


def test_unlaying_one_item_puts_back_only_its_own_line(tmp_path):
    path = committed(tmp_path)
    laid = backlog_retires.lay(backlog_retires.lay(TEXT, "queue", ["r1"], "b1"), "queue", ["r2"], "b2")
    assert "### [g1]" not in laid and "retired: [r1, g1, r2]" in laid
    back = backlog_retires.unlay(path, laid, ["r1"])
    assert "### [g1] One\nRestates: r3@0.29.\n- [r1] " in back and "- [r2] " not in back
    assert "retired: [r2]" in back and "## Dropped" not in back
    assert backlog_retires.unlay(path, back, ["r2"]) == TEXT


def test_unlaying_the_item_whose_lay_took_the_group_out_keeps_the_other_s_line_out(tmp_path):
    path = committed(tmp_path)
    laid = backlog_retires.lay(backlog_retires.lay(TEXT, "queue", ["r1"], "b1"), "queue", ["r2"], "b2")
    back = backlog_retires.unlay(path, laid, ["r2"])
    assert "### [g1] One\nRestates: r3@0.29.\n- [r2] " in back and "- [r1] " not in back
    assert "retired: [r1]" in back and "## Dropped" not in back
    assert backlog_retires.unlay(path, back, ["r1"]) == TEXT
