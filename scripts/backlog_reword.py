"""`work line --reword` and `work line --remove` (capability readiness, b14): one of an item's own requirement lines
given a new text, keeping its id and group, or taken out of the item's `## Requirements`, its group with it when it
was the group's last line (its given block too), and, for a line `work line --retires` wrote, the id it retires out
of its block's `retired:`, read off the block's `retires:` pairs (b323), never git history; an id no pair names (as
`--no-line` retires one) is kept. Each commits only the item. A live requirement of a capability is no line of an item:
it is refused, naming its id, as is any id the item holds no line of (requirements-retired-never-edited)."""
import re

from backlog_items import Refused, commit, find, label, one_line
from backlog_section import SECTION, read, render, takes

IDENT = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)#(r[1-9]\d*)$")


def _found(item, ident, flag):
    """The item's blocks, and the block, group and requirement `<cap>#r<n>` names in them; refused, naming the id,
    when it is no line of the item."""
    takes(item)
    match = IDENT.match(ident or "")
    if not match:
        raise Refused("work line: %s takes `<capability>#r<n>`, not %s" % (flag, ident))
    capability, rid = match.groups()
    blocks = read(item, "the item %s" % item.name)
    for b, block in enumerate(blocks):
        for g, group in enumerate(block.groups):
            if block.capability == capability and any(r == rid for r, _ in group.requirements):
                return blocks, b, g, rid
    raise Refused("work line: %s is no requirement line of %s; %s takes a line of the item's own, and a live "
                  "requirement is replaced by --retires" % (ident, label(item), flag))


def reword(root, name, ident, text):
    """`work line --reword <cap>#r<n> <line>`: the item's line of that id given the text `text`, committed."""
    item = find(root, name)
    blocks, b, g, rid = _found(item, ident, "--reword")
    text = one_line(text, "line")
    if text.startswith("#"):
        raise Refused("work line: %s: the line starts with #, which would read as a heading" % label(item))
    group = blocks[b].groups[g]
    group.requirements[:] = [(r, text if r == rid else old) for r, old in group.requirements]
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s rewords %s" % (label(item), ident))
    return item


def remove(root, name, ident):
    """`work line --remove <cap>#r<n>`: the item's line of that id taken out, its group too when it was the last line,
    and the id the line retires (its pair under `retires:`) out of the block's `retired:`; a block left empty goes too,
    but never a new capability's declaration (its narrator, group and purpose: b448); committed. A bare `<cap>` takes
    the item's whole block of the capability out with its model lines (backlog_retract, b450)."""
    if ident and "#" not in ident:
        import backlog_retract
        return backlog_retract.retract(root, name, ident)
    item = find(root, name)
    blocks, b, g, rid = _found(item, ident, "--remove")
    block = blocks[b]
    group = block.groups[g]
    group.requirements[:] = [(r, t) for r, t in group.requirements if r != rid]
    if not group.requirements:
        del block.groups[g]
    retiring = {old for line, old in block.retires if line == rid}
    if retiring:
        blocks[b] = block = block._replace(retired=tuple(r for r in block.retired if r not in retiring),
                                           retires=tuple(p for p in block.retires if p[0] != rid))
    if not (block.groups or block.terms or block.relations or block.retired or block.language or block.new):
        del blocks[b]
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s removes %s" % (label(item), ident))
    return item
