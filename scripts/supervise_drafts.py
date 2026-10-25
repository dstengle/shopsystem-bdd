"""The requirement ids other initiatives' kept drafts add (capability supervision r102): what an integrate round is told,
so that its drafts take other ids. Standard library only."""
import re
from pathlib import Path

import workqueue

ID = re.compile(r"^\s*-?\s*\[r(\d+)\]", re.MULTILINE)


def ids_in(path):
    """The requirement ids `[r<n>]` that the capability file `path` holds; none when there is no such file."""
    return set(ID.findall(path.read_text())) if path.is_file() else set()


def last_integrate(runs):
    """The directory of the highest-numbered `<k>-integrate` stage under `runs`, else None."""
    stages = [p for p in runs.glob("*-integrate") if p.is_dir() and p.name.split("-")[0].isdigit()]
    return max(stages, key=lambda p: int(p.name.split("-")[0]), default=None)


def added_by_others(root, initiative):
    """`<capability>#r<n>` for each id that another initiative's kept drafts (those of its last integrate round) hold and
    spec/capabilities/<capability>.md in the checkout `root` does not, whatever that initiative's proposals' status."""
    found = []
    for path in sorted((Path(root) / workqueue.WORK).glob("i*/initiative.md")):
        other = path.parent.name
        stage = last_integrate(path.parent / "runs" / other) if other != initiative else None
        for draft in sorted(stage.glob("drafts/spec/capabilities/*.md")) if stage else []:
            held = ids_in(Path(root) / "spec" / "capabilities" / draft.name)
            found += ["%s#r%s" % (draft.stem, n) for n in sorted(ids_in(draft) - held, key=int)
                      if "%s#r%s" % (draft.stem, n) not in found]
    return found
