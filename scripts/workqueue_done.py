"""An initiative done (work-queue r23): the condition over its work-items and the requests this context asked naming it,
and the rewrite of its initiative.md that a command's commit carries.

An initiative qualifies when it has a work-item, every work-item is green or withdrawn, every capability-proposal is
formulated, withdrawn or merged, and every request kept under
.shop/work/requests/ that this context asked and that names the initiative (in its part_of or source) is delivered.
"""
import re
from pathlib import Path

import workqueue

CLOSED_PROPOSAL = ("formulated", "withdrawn", "merged")


def _named(data):
    """The ids a request's part_of and source name."""
    ids = []
    for key in ("part_of", "source"):
        value = data.get(key)
        ids += value if isinstance(value, list) else [value]
    return {i for i in ids if isinstance(i, str)}


def _holds(root, directory, ident, over):
    """The condition for the initiative in `directory` with id `ident`, the statuses in `over` (name -> status) put in
    place of those kept."""
    context = workqueue.context_path(root)
    statuses = []
    for path in sorted(directory.glob("*.md")):
        data, _ = workqueue.frontmatter(workqueue.read(path, root))
        if data.get("kind") == "work-item":
            statuses.append(over.get(path.stem, data.get("status")))
        elif data.get("kind") == "capability-proposal" and data.get("status") not in CLOSED_PROPOSAL:
            return False     # a proposal still open has lines not yet delivered (observation 2026-10-27-done-with-proposal-open)
    if "green" not in statuses or any(s not in ("green", "withdrawn") for s in statuses):
        return False
    for path in sorted((Path(root) / workqueue.WORK / "requests").glob("*.md")):
        data, _ = workqueue.frontmatter(workqueue.read(path, root))
        mine = data.get("asker") in ("internal", context)
        if data.get("kind") == "request" and mine and ident in _named(data) and over.get(path.stem, data.get("status")) != "delivered":
            return False
    return True


def holds(root, directory, ident):
    """Whether the condition holds now for the initiative in `directory` with id `ident` (the part of `work run`'s done
    that the command's is too, r105)."""
    return _holds(root, directory, ident, {})


def becomes(root, directory, over):
    """Whether initiative.md of `directory` is not done, the condition does not hold now and holds with `over` made."""
    path = directory / "initiative.md"
    if not path.is_file():
        return False
    data, _ = workqueue.frontmatter(workqueue.read(path, root))
    ident = data.get("id")
    return data.get("status") != "done" and not _holds(root, directory, ident, {}) and _holds(root, directory, ident, over)


def mark(directory, root, status="done"):
    """Set the status of the initiative.md of `directory` to `status`, done when none is given."""
    path = directory / "initiative.md"
    text = workqueue.read(path, root)
    end = text.find("\n---", 4)
    path.write_text(re.sub(r"(?m)^status:.*$", "status: " + status, text[:end], count=1) + text[end:])


def naming(root, request):
    """The directories of the initiatives the request `request` (its stem) names."""
    path = Path(root) / workqueue.WORK / "requests" / (request + ".md")
    named = _named(workqueue.frontmatter(workqueue.read(path, root))[0])
    found = []
    for ini in sorted((Path(root) / workqueue.WORK).glob("*/initiative.md")):
        if workqueue.frontmatter(workqueue.read(ini, root))[0].get("id") in named:
            found.append(ini.parent)
    return found
