"""The requirement ids other initiatives' kept drafts add (capability supervision r102): what an integrate round is told,
so that its drafts take other ids. Standard library only."""
import re
from pathlib import Path

import workqueue

ID = re.compile(r"^\s*-?\s*\[r(\d+)\]", re.MULTILINE)


def ids_in(path):
    """The requirement ids `[r<n>]` that the capability file `path` holds; none when there is no such file."""
    return set(ID.findall(path.read_text())) if path.is_file() else set()


def kept_drafts(runs):
    """The capability files in `runs`' kept drafts: `<k>-integrate/drafts/round-<m>/spec/capabilities/*.md`, every round
    of every integrate stage."""
    return sorted(runs.glob("*-integrate/drafts/round-*/spec/capabilities/*.md"))


def added_by_others(root, initiative):
    """`<capability>#r<n>` for each id that another initiative's kept drafts (every round of every integrate stage) hold and
    spec/capabilities/<capability>.md in the checkout `root` does not, whatever that initiative's proposals' status."""
    found = []
    for path in sorted((Path(root) / workqueue.WORK).glob("i*/initiative.md")):
        other = path.parent.name
        for draft in kept_drafts(path.parent / "runs" / other) if other != initiative else []:
            held = ids_in(Path(root) / "spec" / "capabilities" / draft.name)
            found += ["%s#r%s" % (draft.stem, n) for n in sorted(ids_in(draft) - held, key=int)
                      if "%s#r%s" % (draft.stem, n) not in found]
    return found
