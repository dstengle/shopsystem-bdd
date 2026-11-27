"""The laid lines' scenarios run by `work batch start` before the lay is committed (b488, batches r97): an item one
of whose requirements retires no requirement id and has a scenario that already passes on the lay goes back to
`shaped`, naming the scenario, since a strict expected failure that passes would fail every task's tests until the
item is built.

`[batch] tests` (batch_tasks' `run_tests`) is run in the batch's worktree, non-strict, every test file but the
scenario tests of the laid capabilities left out (batch_reach's `laid`), and the pytest plugin `work_items` keeps only
the unbuilt scenarios of the laid ids (`$SHOPSYSTEM_LAID`) and writes each that passes to `$SHOPSYSTEM_LAID_REPORT`.
A line that retires an id is not checked: a reworded line's scenario may pass already."""
import tempfile
from pathlib import Path

import backlog_items
import backlog_lines
import backlog_retires
import batch_reach
import batch_tasks

LAID, REPORT = "SHOPSYSTEM_LAID", "SHOPSYSTEM_LAID_REPORT"      # work_items'


def fresh(item):
    """The item's requirement ids `<capability>#r<n>` that retire no id: those no `retires:` pair of any block names
    (a line of another capability's block paired as `<cap>#r<n>`, b882), none of a block with a `retired:` line and
    no pairs to tell them by."""
    blocks = backlog_lines.read(item, backlog_items.rel_of(item.name))
    retiring = backlog_retires.retiring(blocks)
    found = []
    for block in blocks:
        if block.retired and not block.retires:
            continue
        found += ["%s#%s" % (block.capability, r) for g in block.groups for r, _ in g.requirements
                  if "%s#%s" % (block.capability, r) not in retiring]
    return found


def passed(root, tree, ids):
    """(its ids, its title) of each unbuilt scenario of `ids` that passes in `tree`."""
    with tempfile.TemporaryDirectory() as scratch:
        report = Path(scratch) / "passed"
        unreached = batch_reach.laid(tree, {i.split("#")[0] for i in ids})
        batch_tasks.run_tests(root, tree, strict=False, unreached=unreached,
                              extra={LAID: "\n".join(ids), REPORT: str(report)})
        lines = report.read_text(encoding="utf-8").splitlines() if report.is_file() else []
    return [(set(found.split(", ")), title) for found, title in (line.split("\t", 1) for line in lines)]


def passing(root, tree, picked):
    """(item, reasons) of each picked item a requirement of which, retiring none, has a scenario that passes in the
    laid worktree `tree`, each reason naming the requirement and the scenario."""
    ids = {item.name: fresh(item) for item in picked}
    wanted = sorted({i for found in ids.values() for i in found})
    if not wanted:
        return []
    scenarios = passed(root, tree, wanted)
    found = []
    for item in picked:
        reasons = ['%s: its scenario "%s" passes on the lay, before the item is built' % (rid, title)
                   for rids, title in scenarios for rid in ids[item.name] if rid in rids]
        if reasons:
            found.append((item, list(dict.fromkeys(reasons))))
    return found
