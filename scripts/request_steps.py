"""The steps of a request's conversation that are not a line outcome (capability requests, r29-r31): the
upstream's offer (`work offer`), and the asker's answer to it, that an offered capability fits (`work fits`) or the
lines it proposes (`work propose`). Each step is written into this side's record and committed; the offer and the fit
are posted on the issue (request_post), the proposed lines with the asker's turn (`work turn`).

An offer quotes the capabilities it names, whole, and the glossary of spec/index.md, for the asker to write its lines
in this context's terms; the record keeps the offer under `## Offer`, each line quoted (`> `)."""
import re
from pathlib import Path

import backlog_lines
import request_moves
import request_post
import shop_files
from backlog_items import one_line
from request_text import entries, field, with_entries, with_field
from shop_files import Refused

LIMIT = 60000       # GitHub's limit on a comment is 65536 characters


def with_offer(text, offer):
    """The record with `offer` under `## Offer`, quoted."""
    section = "## Offer\n%s\n" % request_post.quoted(offer)
    if re.search(r"(?m)^## Offer\n", text):
        return re.sub(r"(?ms)^## Offer\n.*?(?=^## |\Z)", lambda _: section, text, count=1)
    return text.replace("\n## Lines\n", "\n%s\n## Lines\n" % section, 1) if "\n## Lines\n" in text else \
        text.rstrip("\n") + "\n\n" + section


def offer_text(root, capabilities, note):
    """The offer: the note, each named capability's file whole, and the glossary."""
    parts = [note.strip()] if note and note.strip() else []
    for name in capabilities:
        parts.append("Capability %s:\n\n%s" % (name, backlog_lines.capability_file(root, name).read_text().strip()))
    index = Path(root) / "spec" / "index.md"
    glossary = re.search(r"(?ms)^## Glossary\s*$.*?(?=^## |\Z)", index.read_text() if index.is_file() else "")
    if glossary:
        parts.append(glossary.group(0).strip())
    parts.append("Does any of this serve the request? If one serves it, say so with `work fits`; if not, propose "
                 "lines in these terms with `work propose`.")
    return "\n\n".join(parts)


def _change(root, ident, message, edit):
    path = request_moves.path_of(root, ident)
    after = edit(shop_files.read(path, root))
    shop_files.committed(root, [str(path.relative_to(root))], "work %s: %s" % (message, ident),
                         lambda: path.write_text(after))


def _in_turn(text, ident, side, status, command):
    if field(text, "turn") != side or field(text, "status") not in status:
        raise Refused("%s: %s is %s in the %s's turn; %s takes a request that is %s" % (
            command, ident, field(text, "status"), field(text, "turn"), command, " or ".join(status)))


def offer(root, ident, capabilities, note=None):
    """`work offer` (r29): the upstream's offer on an open request posted, the request `awaiting-asker` in the
    asker's turn."""
    def edit(text):
        request_moves.refuse_upstream_part(root, text, ident, "the offer")
        _in_turn(text, ident, "upstream", ("open",), "work offer")
        said = offer_text(root, capabilities, note)
        if len(said) > LIMIT:
            raise Refused("work offer: the offer is %d characters, over GitHub's limit: offer fewer capabilities"
                          % len(said))
        after = with_field(with_field(with_offer(text, said), "status", "awaiting-asker"), "turn", "asker")
        return request_post.post(root, after, "offer", None, "work offer", fields={"offer": said})
    _change(root, ident, "offer", edit)


def refuse_asker_part(root, text, ident, part):
    if not request_post.is_asker(root, text):
        raise Refused("%s is a request of %s to this context; its asker writes %s" % (ident, field(text, "asker"),
                                                                                     part))


def fits(root, ident, serves):
    """`work fits` (r30): the asker says what of the offer serves it, the requirement ids `serves`; the request
    delivered with them as its resolution, posted, and its issue closed."""
    if not serves:
        raise Refused("work fits: name the requirement that serves the request: give --serves <capability>#r<n>")

    def edit(text):
        refuse_asker_part(root, text, ident, "that an offer fits")
        _in_turn(text, ident, "asker", ("awaiting-asker",), "work fits")
        held = ["%d. %s" % (n, one_line(s, "requirement")) for n, s in enumerate(serves, 1)]
        after = with_field(with_entries(text, "Resolution", held), "status", "delivered")
        return request_post.post(root, after, "fits", {"Resolution": request_post.numbered(after, "Resolution")},
                                 "work fits", close=True)
    _change(root, ident, "fits", edit)


def propose(root, ident, lines):
    """`work propose` (r31): the asker's lines appended to the request's `## Lines`, numbered on; posted with the
    asker's turn. They are the asker's words in the upstream's terms; the upstream parses them."""
    if not lines:
        raise Refused("work propose: give each line with --line <text>")

    def edit(text):
        refuse_asker_part(root, text, ident, "its lines")
        _in_turn(text, ident, "asker", ("awaiting-asker",), "work propose")
        held = entries(text, "Lines")
        at = max([int(e.split(".", 1)[0]) for e in held if e.split(".", 1)[0].isdigit()], default=0)
        new = ["%d. %s" % (at + k, one_line(line, "line")) for k, line in enumerate(lines, 1)]
        return with_entries(text, "Lines", held + new)
    _change(root, ident, "propose", edit)
