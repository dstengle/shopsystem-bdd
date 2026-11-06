"""`work accept` (capability requests, r39, r40): the upstream's person accepts a request whose lines proposed are all
settled with one accepted, and the request becomes an item of the backlog. The item is written `shaped`, titled by the
request, asked by its asker, its provenance read off the asker (`own`, `product`, `peer`), with each accepted line in
its `## Requirements` under the capability (and group) its `work outcome accepted` named; the request is `accepted`,
in the upstream's turn. The request and the item are one commit, and the acceptance is posted on its issue after it
(b36)."""
import re
from pathlib import Path

import backlog_lines
import intake_moves
import request_moves
import request_post
import shop_files
from backlog_items import Item, label, next_name, one_line, rel_of, render
from request_text import SETTLED, countered, entries, field, with_field
from shop_files import Refused

TAKES = ("open", "awaiting-upstream")      # the upstream's turn


def proposed(text):
    """(number, text, line outcome or None, into or None) of each line proposed in the request: a line a
    counter-proposal took the place of is not."""
    gone = countered(text)
    numbered = {s: dict(e.split(". ", 1) for e in entries(text, s) if ". " in e) for s in ("Lines", "Outcomes", "Into")}
    return [(int(n), line, numbered["Outcomes"].get(n), numbered["Into"].get(n))
            for n, line in sorted(numbered["Lines"].items(), key=lambda e: int(e[0])) if n not in gone]


def _refusals(root, ident, text):
    request_moves.refuse_upstream_part(root, text, ident, "its acceptance")
    said = intake_moves.named(ident, text)
    if field(text, "status") not in TAKES or field(text, "turn") != "upstream":
        raise Refused("work accept: %s is %s in the %s's turn; work accept takes a request in the upstream's turn"
                      % (said, field(text, "status"), field(text, "turn")))
    lines = proposed(text)
    for number, line, word, _ in lines:
        if word not in SETTLED:
            raise Refused("work accept: line %d of request %s is %s, not settled: %s"
                          % (number, ident, word or "unanswered", line))
    accepted = [(n, line, into) for n, line, word, into in lines if word == "accepted"]
    if not accepted:
        raise Refused("work accept: %s has no accepted line" % said)
    for number, _, into in accepted:
        if not into:
            raise Refused("work accept: line %d of request %s names no capability it goes into: run `work outcome %s "
                          "%d accepted --into <capability>`" % (number, ident, ident, number))
    return accepted


def _write_lines(root, item, accepted):
    """Each accepted line into the item, under its capability; the lines of one capability with no group named share
    one new group, titled by the item."""
    shared = {}
    for _, line, into in accepted:
        capability, _, group = into.partition(" ")
        in_group = group if re.fullmatch(r"g[1-9]\d*", group) else None
        if not group and capability in shared:
            in_group = shared[capability]
        title = None if in_group is not None else (group or None)
        backlog_lines.add_line_to(root, item, capability, line, title, in_group, command="work accept")
        if not group and capability not in shared:
            block = next(b for b in backlog_lines.read(item, rel_of(item.name)) if b.capability == capability)
            shared[capability] = block.groups[-1].id


def accept(root, ident):
    """Write the item request `ident` becomes, set the request `accepted` and post the acceptance; return the item."""
    path = request_moves.path_of(root, ident)
    text = shop_files.read(path, root)
    accepted = _refusals(root, ident, text)
    asker = field(text, "asker")
    name = next_name(root)
    item = Item(name=name, ident="item/%s/%s" % (shop_files.context_path(root), name),
                title=one_line(intake_moves.title_of(text), "request's title"), status="shaped",
                provenance=intake_moves.provenance_of(root, asker), request=ident, asked_by=asker,
                sections={"Notes": "taken in from request %s" % intake_moves.named(ident, text)})
    _write_lines(root, item, accepted)
    after = with_field(text, "status", "accepted")

    def write():
        target = Path(root) / rel_of(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(item), encoding="utf-8")
    request_post.committed(root, path, "work accept: %s -> %s shaped" % (intake_moves.named(ident, text), label(item)),
                           after, request_post.posting(after, "accept", None, "work accept"), [rel_of(name)], write)
    return item
