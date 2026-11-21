"""The steps of a request's conversation that are not a line outcome (capability requests, r29-r31): the
upstream's offer (`work offer`), and the asker's answer to it, that an offered capability fits (`work fits`) or the
lines it proposes (`work propose`). Each step is written into this side's record and committed; the offer and the fit
are posted on the issue (request_post), the proposed lines with the asker's turn (`work turn`).

An offer quotes each capability it names by its groups, each a title over its requirements (no frontmatter, prose,
terms or given blocks), and of the imported packs, the glossary and the capabilities' `## Terms` only the entries those
requirements mention (b40), for the asker to write its lines in this context's terms; the record keeps the offer under
`## Offer`, each line quoted (`> `)."""
import re

import backlog_lines
import request_moves
import request_post
import shop_files
import spec_packs
import spec_read
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


def _spellings(term):
    """The words a line mentions `term` by: its own, its plural or forms, and its values."""
    words = {term.term, term.term + "s", term.term + "es", term.plural, *term.forms, *term.values}
    return [w for w in words if w]


def mentions(text, word):
    return re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(word), text, re.IGNORECASE) is not None


def mentioned(root, lines):
    """The term entries, over every layer (packs, glossary, capabilities' `## Terms`), that `lines` mention, each
    once, a later layer's entry of a word in place of an earlier one's."""
    text, found = "\n".join(lines), {}
    for _, term in spec_packs.layers(root):
        if any(mentions(text, w) for w in _spellings(term)):
            found[(term.term, term.label)] = "- **%s**%s: %s" % (
                term.term, " (%s)" % term.label if term.label else "", term.text)
    return list(found.values())


def offer_text(root, capabilities, note):
    """The offer: the note, each named capability's groups and requirements, and the terms they mention."""
    parts, lines = ([note.strip()] if note and note.strip() else []), []
    for name in capabilities:
        cap = spec_read.capability(backlog_lines.capability_file(root, name))
        block = ["Capability %s:" % name]
        for group in cap.groups:
            block.append("\n### [%s] %s" % (group.id, group.title))
            block += ["- [%s] %s" % (r.id, r.text) for r in group.requirements]
            lines += [r.text for r in group.requirements]
        parts.append("\n".join(block))
    terms = mentioned(root, lines)
    if terms:
        parts.append("Terms they use:\n\n" + "\n".join(terms))
    parts.append("Does any of this serve the request? If one serves it, say so with `work fits`; if not, propose "
                 "lines in these terms with `work propose`.")
    return "\n\n".join(parts)


def change(root, ident, message, edit, posting=None):
    """The record as `edit` makes it committed, then what `posting` makes of it posted (request_post.committed)."""
    path = request_moves.path_of(root, ident)
    after = edit(shop_files.read(path, root))
    request_post.committed(root, path, "work %s: %s" % (message, ident), after, posting(after) if posting else None)


def in_turn(text, ident, side, status, command):
    if field(text, "turn") != side or field(text, "status") not in status:
        raise Refused("%s: %s is %s in the %s's turn; %s takes a request that is %s" % (
            command, ident, field(text, "status"), field(text, "turn"), command, " or ".join(status)))


def offer(root, ident, capabilities, note=None):
    """`work offer` (r29): the upstream's offer on an open request posted, the request `awaiting-asker` in the
    asker's turn."""
    said = {}

    def edit(text):
        request_moves.refuse_upstream_part(root, text, ident, "the offer")
        in_turn(text, ident, "upstream", ("open",), "work offer")
        said["offer"] = offer_text(root, capabilities, note)
        if len(said["offer"]) > LIMIT:
            raise Refused("work offer: the offer is %d characters, over GitHub's limit: offer fewer capabilities"
                          % len(said["offer"]))
        return with_field(with_field(with_offer(text, said["offer"]), "status", "awaiting-asker"), "turn", "asker")
    change(root, ident, "offer", edit, lambda after: request_post.posting(
        after, "offer", None, "work offer", fields=said))


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
        in_turn(text, ident, "asker", ("awaiting-asker",), "work fits")
        held = ["%d. %s" % (n, one_line(s, "requirement")) for n, s in enumerate(serves, 1)]
        return with_field(with_entries(text, "Resolution", held), "status", "delivered")
    change(root, ident, "fits", edit, lambda after: request_post.posting(
        after, "fits", {"Resolution": request_post.numbered(after, "Resolution")}, "work fits", close=True))


def propose(root, ident, lines):
    """`work propose` (r31): the asker's lines appended to the request's `## Lines`, numbered on; posted with the
    asker's turn. They are the asker's words in the upstream's terms; the upstream parses them."""
    if not lines:
        raise Refused("work propose: give each line with --line <text>")

    def edit(text):
        refuse_asker_part(root, text, ident, "its lines")
        in_turn(text, ident, "asker", ("awaiting-asker",), "work propose")
        held = entries(text, "Lines")
        at = max([int(e.split(".", 1)[0]) for e in held if e.split(".", 1)[0].isdigit()], default=0)
        new = ["%d. %s" % (at + k, one_line(line, "line")) for k, line in enumerate(lines, 1)]
        return with_entries(text, "Lines", held + new)
    change(root, ident, "propose", edit)
