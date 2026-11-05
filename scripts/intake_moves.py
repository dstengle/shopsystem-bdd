"""Intake (capability intake; workflow simplification plan 3, D10-D12): a request of this context taken in as an item
(`work intake`), and the item side of `work outcome` on a request an item was taken in from. The request files are
the ones workqueue_request.py keeps; `work intake` changes nothing in the request."""
import re
from pathlib import Path

import backlog_lines
import workqueue
import workqueue_lines
import workqueue_request
from backlog_items import (
    Item,
    Refused,
    commit,
    items,
    label,
    next_name,
    one_line,
    rel_of,
    render,
)
from backlog_moves import CLOSED, add_note, text_line
from workqueue_request import _entries, _numbered, _with_entries, _with_field, field

TAKES = ("open", "awaiting-upstream")      # the upstream's turn
OUTCOMES = ("accepted", "rewritten", "refused", "question", "withdrawn")    # the glossary's `line outcome`


def provenance_of(root, asker):
    """`own` for this context's own asker, `product` for the product, `peer` for any other bounded context (D10)."""
    if asker == "internal" or asker in workqueue_request.own_askers(root):
        return "own"
    return "product" if (asker or "").startswith("product/") else "peer"


def linked(root, request):
    """The item taken in from `request`, or None."""
    return next((i for i in items(root) if i.request == request), None)


def title_of(text):
    found = re.search(r"(?m)^# (\S.*)$", text)
    return found.group(1).strip() if found else ""


def named(request, text):
    """How `work` names a request: `q<n> "<its title>"` (design goal 10)."""
    return '%s "%s"' % (request, title_of(text))


def intake(root, request):
    """Write the `shaped` item request `request` is taken in as, and commit it alone (D10): titled by the request's
    heading, asked by its asker, its provenance read off the asker. A request already taken in, and one that is not in
    the upstream's turn, and this context's own request to its upstream (taken in there), are refused."""
    text = workqueue.read(workqueue_request.path_of(root, request), root)
    had = linked(root, request)
    if had is not None:
        raise Refused("work intake: %s was taken in already, as %s" % (named(request, text), label(had)))
    asker, upstreams = field(text, "asker"), workqueue_request.upstreams(root)
    if upstreams and asker in workqueue_request.own_askers(root) and field(text, "source") is None:
        raise Refused("work intake: %s is a request to the upstream %s; it is taken in there"
                      % (named(request, text), upstreams[0]))
    status = field(text, "status")
    if status not in TAKES:
        raise Refused("work intake: %s is %s; work intake takes a request that is open or awaiting-upstream"
                      % (named(request, text), status))
    if field(text, "turn") != "upstream":
        raise Refused("work intake: %s is in the asker's turn; work intake takes a request in the upstream's turn"
                      % named(request, text))
    name = next_name(root)
    item = Item(name=name, ident="item/%s/%s" % (workqueue.context_path(root), name),
                title=one_line(title_of(text), "request's title"), status="shaped",
                provenance=provenance_of(root, asker), request=request, asked_by=asker,
                sections={"Notes": "taken in from request %s" % named(request, text)})
    commit(root, item, "work intake: %s -> %s shaped" % (named(request, text), label(item)))
    return item


def handles(args):
    """Whether `work outcome` is intake's: one of its options given (`--line` is `text`, `line` the line's number),
    or an item taken in from the request. A malformed backlog is refused, not read as no item."""
    if any(getattr(args, k, None) is not None for k in ("into", "group", "reason", "text")):
        return True
    return linked(args.root, args.request) is not None


def _refusals(root, ident, text, number, word, item, into, group, reason, line):
    """Refuse, before anything is written, an outcome intake does not take (D12); the old refusals first."""
    workqueue_request._refuse_upstream_part(root, text, ident, "the line outcomes")
    if word not in OUTCOMES:
        raise Refused("work outcome: %s is not a line outcome; give one of %s" % (word, ", ".join(OUTCOMES)))
    if field(text, "turn") == "asker":
        raise Refused("%s is in the asker's turn; the upstream writes a line outcome only in its own turn" % ident)
    if str(number) not in {e.split(". ", 1)[0] for e in _entries(text, "Lines")}:
        raise Refused("work outcome: %s has no line %d" % (named(ident, text), number))
    if (into is not None or group is not None) and (item is None or word != "accepted"):
        raise Refused("work outcome: --into and --group write an accepted line into the item taken in from the "
                      "request; give them with accepted, on a request taken in with `work intake`")
    if line is not None and word != "rewritten":
        raise Refused("work outcome: --line is a counter-proposal; give it with rewritten")
    if item is not None and item.status in CLOSED:
        raise Refused("work outcome: %s, taken in from %s, is %s" % (label(item), named(ident, text), item.status))
    if item is not None and word == "accepted" and into is None:
        raise Refused("work outcome: an accepted line of %s goes into a capability of %s: give --into <capability>"
                      % (named(ident, text), label(item)))
    if item is not None and word == "refused" and reason is None:
        raise Refused("work outcome: a refused line of %s is written with its reason: give --reason" % named(ident, text))


def outcome(root, ident, number, word, into=None, group=None, reason=None, line=None):
    """`work outcome` on a request taken in as an item, or with one of intake's options (D12): the line outcome, a
    reason under `## Reasons`, a counter-proposal appended to `## Lines` with the turn passed to the asker, and, on a
    request taken in, the accepted line written into the item and a note; one commit of the request and the item."""
    path = workqueue_request.path_of(root, ident)
    text = workqueue.read(path, root)
    item = linked(root, ident)
    reason = text_line(reason, "reason") if reason is not None else None
    _refusals(root, ident, text, number, word, item, into, group, reason, line)
    after = _with_entries(text, "Outcomes", _numbered(_entries(text, "Outcomes"), number, word))
    note = "line %d of request %s %s" % (number, ident, word)
    if line is not None:
        line = text_line(line, "counter-proposal")
        try:
            workqueue_lines.check(root, [line])
        except Refused as refused:
            said, head = str(refused), "line 1 does not parse in the upstream's requirement grammar: "
            if not said.startswith(head):
                raise
            raise Refused("work outcome: the counter-proposal does not parse in this context's requirement grammar: "
                          + said[len(head):]) from None
        lines = _entries(text, "Lines")
        at = max(int(e.split(".", 1)[0]) for e in lines) + 1
        after = _with_entries(after, "Lines", lines + ["%d. %s" % (at, line)])
        # a rewritten line is never settled, so `work turn` from the upstream sets awaiting-asker (requests r17)
        after = _with_field(_with_field(after, "status", "awaiting-asker"), "turn", "asker")
        reason = reason or "rewritten as line %d" % at
        note += " as line %d" % at
    if reason is not None:
        after = _with_entries(after, "Reasons", _numbered(_entries(after, "Reasons"), number, reason))
    if item is not None and word == "accepted":
        written = dict(e.split(". ", 1) for e in _entries(text, "Lines"))[str(number)]
        note += " into %s" % backlog_lines.add_line_to(root, item, into, written, group, command="work outcome")
    if reason is not None and line is None:
        note += ": %s" % reason
    rels = [str(path.relative_to(root))]
    message = "work outcome: %s line %d %s" % (ident, number, word)
    if item is not None:
        add_note(item, note)
        rels.append(rel_of(item.name))
        message += " -> %s" % label(item)

    def write():
        path.write_text(after)
        if item is not None:
            (Path(root) / rel_of(item.name)).write_text(render(item))
    workqueue.committed(root, rels, message, write)

