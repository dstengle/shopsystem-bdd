"""What the plugin's hooks tell a session about the repository's initiatives (migration-tools r32-r34).

The SessionStart hook adds `work status`'s text for each initiative neither done nor abandoned (`work_text`); the
PreCompact hook (`migrate compacting`) appends `compacted`, with the time, to the ledger of each of them and tells the
session to write its hand-off with `work note` and end. Both exit 0: a hook's failure must not stop a session.
"""
import sys
import time
from pathlib import Path

import workqueue
import workqueue_status
from migrate_write import top_level


def open_root(root):
    """`root` when it holds .shop/work/ with an initiative neither done nor abandoned, else None."""
    if not (Path(root) / workqueue.WORK).is_dir():
        return None
    return root if workqueue_status.open_names(root) else None


def work_text(root):
    """What `work status` prints at `root` for each open initiative; '' when there is none."""
    return workqueue_status.open_text(root) if open_root(root) else ""


def compacting(root):
    """Append `compacted` to the ledger of each open initiative, commit them, and return what the session is told."""
    names = workqueue_status.open_names(root) if open_root(root) else []
    if not names:
        return ""
    rels = ["%s/%s/ledger.md" % (workqueue.WORK, name) for name in names]
    line = ("- %s: compacted\n" % time.strftime("%Y-%m-%d %H:%M")).encode()

    def write():
        for rel in rels:
            workqueue.append(Path(root) / rel, line)

    workqueue.committed(root, rels, "compacted: " + ", ".join(names), write)
    return ("This session is about to be compacted. Do not go on from a summary: for each of %s, write your hand-off "
            "with `work note <initiative> \"<hand-off>\"` (python3 %s note), and then end this session instead of being "
            "compacted.\n" % (", ".join(names), Path(__file__).resolve().parent / "work"))


def run():
    """`migrate compacting`: the PreCompact hook, always exit 0."""
    root = top_level(Path.cwd())
    if root is not None:
        try:
            sys.stdout.write(compacting(root))
        except workqueue.Refused:
            pass
    return 0
