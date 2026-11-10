"""Intake (capability intake; requests r38): the upstream's line outcomes of a request, `work outcome`. A request
of another context, or of this one, is answered on its issue; the item it becomes is written only when the person
accepts it (`work accept`, request_accept.py), so a session's `accepted` here is a proposal of acceptance, which
names the capability (and group) the line goes into under the request's `## Into`. The request files are the ones
request_moves.py keeps."""
import re

import backlog_lines
import request_lines
import request_moves
import request_post
import shop_files
from backlog_items import Refused
from backlog_moves import text_line
from request_text import COUNTERS, entries, field, numbered, turned, with_entries

OUTCOMES = ("accepted", "rewritten", "refused", "question", "withdrawn")    # the glossary's `line outcome`


def provenance_of(root, asker):
    """`own` for this context's own asker, `product` for the product, `peer` for any other bounded context (D10)."""
    if asker == "internal" or asker in request_moves.own_askers(root):
        return "own"
    return "product" if (asker or "").startswith("product/") else "peer"


def title_of(text):
    found = re.search(r"(?m)^# (\S.*)$", text)
    return found.group(1).strip() if found else ""


def named(request, text):
    """How `work` names a request: `q<n> "<its title>"` (design goal 10)."""
    return '%s "%s"' % (request, title_of(text))


def parsed(root, line, said):
    """Refuse `line` unless it parses in this context's requirement grammar (request_lines), with `said` before the
    refusal."""
    try:
        request_lines.check(root, [line])
    except Refused as refused:
        why, head = str(refused), "line 1 does not parse in the upstream's requirement grammar: "
        if not why.startswith(head):
            raise
        raise Refused("work outcome: %s does not parse in this context's requirement grammar: %s"
                      % (said, why[len(head):])) from None


def _refusals(root, ident, text, number, word, into, group, line, reason):
    """Refuse, before anything is written, an outcome intake does not take (D12); the old refusals first."""
    request_moves.refuse_upstream_part(root, text, ident, "the line outcomes")
    if word not in OUTCOMES:
        raise Refused("work outcome: %s is not a line outcome; give one of %s" % (word, ", ".join(OUTCOMES)))
    if field(text, "turn") == "asker":
        raise Refused("%s is in the asker's turn; the upstream writes a line outcome only in its own turn" % ident)
    lines = dict(e.split(". ", 1) for e in entries(text, "Lines") if ". " in e)
    if str(number) not in lines:
        raise Refused("work outcome: %s has no line %d" % (named(ident, text), number))
    if (into is not None or group is not None) and word != "accepted":
        raise Refused("work outcome: --into and --group name where an accepted line goes; give them with accepted")
    if line is not None and word != "rewritten":
        raise Refused("work outcome: --line is a counter-proposal; give it with rewritten")
    if word == "refused" and reason is None:
        raise Refused("work outcome: a refused line is written with its reason: give --reason <text>")
    if word == "rewritten" and line is None:
        raise Refused("work outcome: a rewritten line is written with its counter-proposal: give --line <text>")
    if word == "accepted":
        parsed(root, lines[str(number)], "line %d of %s, %s," % (number, named(ident, text), lines[str(number)]))
        if into is None:
            raise Refused("work outcome: an accepted line of %s goes into a capability of this context: give "
                          "--into <capability>" % named(ident, text))
        backlog_lines.capability_file(root, into)


def outcome(root, ident, number, word, into=None, group=None, reason=None, line=None):
    """`work outcome`: the line outcome, a reason under `## Reasons` (a refused line's is required, intake r8 and r9),
    an accepted line's capability (and group) under `## Into` (r38: a line that does not parse is not accepted), and a
    counter-proposal appended to `## Lines` with the turn passed to the asker and posted (intake r7); one commit of
    the request."""
    path = request_moves.path_of(root, ident)
    text = shop_files.read(path, root)
    reason = text_line(reason, "reason") if reason is not None else None
    into = text_line(into, "capability") if into is not None else None
    group = text_line(group, "group") if group is not None else None
    _refusals(root, ident, text, number, word, into, group, line, reason)
    after = with_entries(text, "Outcomes", numbered(entries(text, "Outcomes"), number, word))
    if into is not None:
        after = with_entries(after, "Into", numbered(entries(after, "Into"), number,
                                                     into + (" %s" % group if group else "")))
    if line is not None:
        line = text_line(line, "counter-proposal")
        parsed(root, line, "the counter-proposal")
        lines = entries(text, "Lines")
        at = max(int(e.split(".", 1)[0]) for e in lines) + 1
        after = with_entries(after, "Lines", lines + ["%d. %s" % (at, line)])
        after = with_entries(after, COUNTERS, numbered(entries(after, COUNTERS), number, str(at)))
        reason = reason or "rewritten as line %d" % at
    if reason is not None:
        after = with_entries(after, "Reasons", numbered(entries(after, "Reasons"), number, reason))
    posted = None
    if line is not None:
        # its counter-proposal has no outcome yet, so the turn passes to the asker (requests r35), posted once committed
        before, after = after, turned(after)
        posted = request_post.turn_posting(before, after, "work outcome")
    request_post.committed(root, path, "work outcome: %s line %d %s" % (ident, number, word), after, posted)
