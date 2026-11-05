"""`work names` (capability conversation r4; workflow simplification plan 8, D8): one table of every item and every
batch with its name beside its id, items then batches by number, a batch named by the labels of its tasks' items; and
the SessionStart hook's `work names --hook`, the table under one line telling the session to name things by their
names, silent when there is nothing to name and never failing a session's start (design goal 10). Standard library
only."""
from pathlib import Path

import backlog_items
import batch_plan
from backlog_view import cell
from migrate_write import top_level
from shop_files import Refused

HOOK_LINE = ("The names of this repository's items and batches: tell the person each by its name beside its id "
             '(b3 "Fix the parser"), never by its id alone.')
EMPTY = "there is no item in .shop/backlog/ and no batch in .shop/batches/"


def rows(root):
    """(id, name, status) of every item and then every batch (D8)."""
    items = backlog_items.items(root)
    by_name = {i.name: i for i in items}
    out = [(i.name, i.title, i.status) for i in items]
    for batch in batch_plan.batches(root):
        names = [backlog_items.label(by_name[t.item]) if t.item in by_name else "%s (missing)" % t.item
                 for t in batch.tasks]
        out.append((batch.name, ", ".join(names), batch.status))
    return out


def table(root):
    """The table of rows(root), each cell escaped; EMPTY when there is no row."""
    found = rows(root)
    if not found:
        return EMPTY
    return "\n".join(["| id | name | status |", "|---|---|---|"] +
                     ["| %s | %s | %s |" % tuple(cell(c) for c in row) for row in found])


def hook_text(cwd):
    """What the SessionStart hook prints at the top level of the cwd's repository: HOOK_LINE and the table, nothing
    when there is nothing to name or no `.shop/`, `work names: <why>` for a refusal. Never raises."""
    try:
        root = top_level(cwd)
        if root is None or not (Path(root) / ".shop").is_dir() or not rows(root):
            return ""
        return "%s\n%s" % (HOOK_LINE, table(root))
    except Refused as why:
        return "work names: %s" % why
    except Exception:  # noqa: BLE001  (a hook never fails a session's start: D8)
        return ""
