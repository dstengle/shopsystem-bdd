"""`work line --reword` and `work line --remove` (capability readiness, b14): one of an item's own requirement lines
given a new text, keeping its id and group, or taken out of the item's `## Requirements`, its group with it when it
was the group's last line (its given block too), and, for a line `work line --retires` wrote, the id it retires out
of its block's `retired:`, read off the block's `retires:` pairs (b323), never git history; an id no pair names (as
`--no-line` retires one) is kept. Each commits only the item. A live requirement of a capability is no line of an item:
`--reword` refuses it, naming its id, as it does any id the item holds no line of (requirements-retired-never-edited);
`--remove` of an id that is no line of the item but one its block retires reinstates it (b760, drafting r89, r90:
`_unretiring`; the item's own line that retired it kept, its pair out, b768), and refuses any other, naming it, as a requirement id not retired by the item."""
import re

from backlog_items import Refused, commit, find, label, one_line
from backlog_section import SECTION, read, render, takes

IDENT = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)#(r[1-9]\d*)$")


def _found(item, ident, flag, lineless=None):
    """The item's blocks, and the block, group and requirement `<cap>#r<n>` names in them; when it is no line of the
    item, what `lineless(item, blocks, capability, rid)` gives, else refused naming the id."""
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
    if lineless is not None:
        return lineless(item, blocks, capability, rid)
    raise Refused("work line: %s is no requirement line of %s; %s takes a line of the item's own, and a live "
                  "requirement is replaced by --retires" % (ident, label(item), flag))


def reword(root, name, ident, text):
    """`work line --reword <cap>#r<n> <line>`: the item's line of that id given the text `text`, committed; the item
    and whether it changed: a line the item holds with that text already is left as it is, nothing committed
    (drafting r107, b829)."""
    item = find(root, name)
    blocks, b, g, rid = _found(item, ident, "--reword")
    text = one_line(text, "line")
    if text.startswith("#"):
        raise Refused("work line: %s: the line starts with #, which would read as a heading" % label(item))
    group = blocks[b].groups[g]
    if dict(group.requirements)[rid] == text:
        return item, False
    group.requirements[:] = [(r, text if r == rid else old) for r, old in group.requirements]
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s rewords %s" % (label(item), ident))
    return item, True


def remove(root, name, ident):
    """`work line --remove <cap>#r<n>`: the item's line of that id taken out, its group too when it was the last line,
    and the id the line retires (its pair under `retires:`) out of the block's `retired:`; a block left empty goes too,
    but never a new capability's declaration (its narrator, group and purpose: b448); committed. A bare `<cap>` takes
    the item's whole block of the capability out with its model lines (backlog_retract, b450). An id that is no line
    of the item but one its block retires is reinstated (`_unretiring`, b760)."""
    if ident and "#" not in ident:
        import backlog_retract
        return backlog_retract.retract(root, name, ident)
    item = find(root, name)
    found = _found(item, ident, "--remove", _unretiring)
    if found is None:
        commit(root, item, "work line: %s reinstates %s" % (label(item), ident))
        return item
    blocks, b, g, rid = found
    block = blocks[b]
    group = block.groups[g]
    group.requirements[:] = [(r, t) for r, t in group.requirements if r != rid]
    if not group.requirements:
        del block.groups[g]
    retiring = {old for line, old in block.retires if line == rid}
    if retiring:
        blocks[b] = block._replace(retired=tuple(r for r in block.retired if r not in retiring),
                                   retires=tuple(p for p in block.retires if p[0] != rid))
    _written(item, blocks, b)
    commit(root, item, "work line: %s removes %s" % (label(item), ident))
    return item


def _written(item, blocks, b):
    """The item's section written from `blocks`, the block `b` out when nothing is left in it."""
    block = blocks[b]
    if not (block.groups or block.terms or block.relations or block.retired or block.language or block.new):
        del blocks[b]
    item.sections[SECTION] = render(blocks)


def _unretiring(item, blocks, capability, rid):
    """`work line --remove <cap>#r<n>` of an id that is no line of the item: reinstated (drafting.reinstate
    requirement, b760) when the item's block of the capability retires it, the id out of `retired:` and every pair
    naming it out of `retires:`, an item's own line of such a pair kept, retiring nothing (drafting r91, b768); the
    item's section written; None. Refused, naming the id, when no block retires it."""
    for b, block in enumerate(blocks):
        if block.capability == capability and rid in block.retired:
            blocks[b] = block._replace(retired=tuple(r for r in block.retired if r != rid),
                                       retires=tuple(p for p in block.retires if p[1] != rid))
            _written(item, blocks, b)
            return
    ident = "%s#%s" % (capability, rid)
    raise Refused("work line: %s neither holds a line of nor retires %s; --remove takes a line of the item's own or "
                  "an id it retires (requirement id not retired by the item)" % (label(item), ident),
                  reason="requirement id not retired by the item", names=["requirement id:%s" % ident])
