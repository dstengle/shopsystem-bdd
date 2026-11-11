"""The 0.31.0 upgrade step "the workflow simplified" (plan 9, D13; migration-tools g24). `plan` computes every change
and writes none:
- when `.shop/work/` exists, `.shop/work/FROZEN.md` holds `FROZEN_TEXT`: the queue of plugin 0.30 is frozen;
- each request of `.shop/work/requests/` that is not closed and whose asker is neither `internal` nor this context
  moves to `.shop/requests/`, its name and id unchanged (D8); a peer's negotiation in flight goes on;
- when `spec/decisions/` exists, `spec/decisions/index.md` is rewritten as `model decisions` writes it (plan-6 M5);
- `notes`: each initiative neither done nor abandoned, each proposal never applied, each internal request not closed,
  and each request moved, by id and title;
- `failures`: a request file whose frontmatter does not read (a destination that exists is `migrate_upgrade`'s
  `move_failures`).
Nothing is deleted, and nothing else under `.shop/work/` changes."""
import re
from pathlib import Path

import model_report
from migrate_upgrade_ids import Changes
from model_parse import frontmatter
from request_text import FROZEN, REQUESTS
from shop_files import Refused, context_path

WORK = Path(".shop/work")
MARKER = WORK / "FROZEN.md"
FROZEN_TEXT = ("# Frozen\n\nThe request, initiative and work-item queue of plugin 0.30, frozen by `migrate upgrade` 0.31.0. "
               "Nothing writes here and `model check` reads nothing here but the `source` of its initiatives and "
               "requests. Items are in `.shop/backlog/`, batches in `.shop/batches/` and live requests in "
               "`.shop/requests/`.\n")
OPEN = ("open", "awaiting-asker", "awaiting-upstream", "accepted")
CLOSED_INITIATIVE = ("done", "abandoned")
APPLIED = ("formulated", "approved", "merged", "withdrawn")
PROPOSALS = ("capability-proposal", "glossary-proposal")
EARLIER = "left for a session to write: %s/" % WORK.as_posix()   # an earlier step's note on the queue this one freezes


def superseded(note):
    """Whether an earlier step's note (0.30.0's proposal "in 0.29 lines") asks for a write into the queue this step
    freezes: in the same upgrade it is dropped, since `FROZEN.md` says nothing writes there (plan-9 review S5)."""
    return note.startswith(EARLIER)


def title(data, body):
    """A file's `title`, else its first `# ` heading, else nothing."""
    heading = re.search(r"^# (.+)$", body, re.MULTILINE)
    return str(data.get("title") or (heading.group(1).strip() if heading else ""))


def number_of(name):
    return [int(w) if w.isdigit() else w for w in re.split(r"(\d+)", name)]


def own_asker(root):
    try:
        return "bounded-context/" + context_path(root)
    except Refused:
        return None


def initiatives(root, notes):
    for path in sorted((root / WORK).glob("*/initiative.md"), key=lambda p: number_of(p.parent.name)):
        data, body = frontmatter(path.read_text())
        if data.get("status") in CLOSED_INITIATIVE:
            continue
        match = re.match(r"i\d+", path.parent.name)
        ident = str(data.get("id", "")).rsplit("/", 1)[-1] or (match.group(0) if match else path.parent.name)
        notes.append('open initiative %s "%s" is frozen: shape what is still wanted as an item (work idea)'
                     % (ident, title(data, body)))
    for path in sorted((root / WORK).glob("*/*.md"), key=lambda p: (number_of(p.parent.name), p.name)):
        data, _ = frontmatter(path.read_text())
        if data.get("kind") in PROPOSALS and data.get("status") not in APPLIED:
            notes.append("the lines of proposal %s were never applied: shape an item with them if still wanted"
                         % path.relative_to(root).as_posix())


def requests(root, changes):
    own = own_asker(root)
    for path in sorted((root / FROZEN).glob("q*.md"), key=lambda p: number_of(p.stem)):
        rel = path.relative_to(root).as_posix()
        data, body = frontmatter(path.read_text())
        if not data.get("status") or not data.get("asker"):
            changes.failures.append("could not read the frontmatter of %s: it gives no status or no asker" % rel)
            continue
        if data["status"] not in OPEN:
            continue
        if data["asker"] in ("internal", own):
            changes.notes.append('internal request %s "%s" is frozen: enter it as an item if still wanted'
                                 % (path.stem, title(data, body)))
        else:
            changes.moves.append((rel, (REQUESTS / path.name).as_posix()))
            changes.notes.append("moved request %s to %s/" % (path.stem, REQUESTS.as_posix()))


def plan(root):
    root = Path(root)
    changes = Changes()
    changes.notes = []
    if (root / WORK).is_dir():
        changes.texts[MARKER.as_posix()] = FROZEN_TEXT
        initiatives(root, changes.notes)
        requests(root, changes)
    if (root / "spec/decisions").is_dir():
        changes.texts["spec/decisions/index.md"] = model_report.render_decisions(root)
    return changes
