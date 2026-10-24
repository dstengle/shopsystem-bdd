"""`work note`: a dated line in an initiative's ledger (capability work-queue, r19-r21)."""
import datetime
from pathlib import Path

import workqueue
from workqueue import Refused
from workqueue_answer import LINE_BREAKS


def note(root, initiative, text):
    """Append `text` with today's date to .shop/work/<initiative>/ledger.md and commit that file on the current branch."""
    if any(c in text for c in LINE_BREAKS):
        raise Refused("the note has a line break in it; a note is one line")
    workqueue.entry(initiative, "initiative")
    directory = Path(root) / workqueue.WORK / initiative
    if not directory.is_dir():
        raise Refused("the initiative %s does not exist (no %s)" % (initiative, directory.relative_to(root)))
    ledger = directory / "ledger.md"
    line = "- %s: %s\n" % (datetime.date.today().isoformat(), text)
    workqueue.committed(root, [str(ledger.relative_to(root))], "work note: %s" % initiative,
                        lambda: workqueue.append(ledger, line.encode()))
