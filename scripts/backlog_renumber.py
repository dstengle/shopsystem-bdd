"""An item's ids renumbered past its capabilities', `spec/universal.md`'s and the items' picked before it (plan 4, D8),
split out of backlog_lines, which gives `renumber` to its callers: each group, requirement and universal condition id
that collides the next free in file order, the `retires:` pairs and the `serves:` pairs of the item's own groups
(backlog_serves, b641), the ids of its `Relied on by:` lines (backlog_relied, b705) and its `request_lines` (b6) carried to the new ids."""
import re

import backlog_forms
import backlog_relied
import backlog_serves
from backlog_section import SECTION, Blocks, Group, read, render


def _number(ident):
    return int(ident[1:])


def _fresh(old, capability, used, seen, pairs):
    """`old`, or the next id above every one `seen` when it is `used`, the pair noted in `pairs`."""
    if old not in used:
        used.add(old)
        return old
    new = "%s%d" % (old[0], max(_number(i) for i in seen if i[0] == old[0]) + 1)
    seen.add(new)
    used.add(new)
    pairs.append(("%s#%s" % (capability, old), "%s#%s" % (capability, new)))
    return new


def renumber(root, item, taken):
    """New group, requirement and universal ids for the item's wherever they collide with its capability in `spec/`
    (groups, requirements, `retired:`), with `spec/universal.md`'s, or with `taken` ({capability, or "universal":
    ids} of the items picked before it), each the next free in file order (plan 4, D8). `taken` gains the item's ids;
    the item's `## Requirements` is rewritten, its model, adapter, pack, moves, imports and retirements blocks kept (b378, b660, b672), and its
    `request_lines` keyed by the new ids (b6). The (`<cap>#<old>`, `<cap>#<new>`) pairs."""
    from backlog_lines import _spec_of  # backlog_lines imports this module
    blocks, pairs = read(item, "the item %s" % item.name), []
    out = Blocks(upstreams=blocks.upstreams, universal_language=blocks.universal_language,
                 universal_retired=blocks.universal_retired, models=blocks.models,
                 adapters=blocks.adapters, packs=blocks.packs, moves=blocks.moves,
                 imports=blocks.imports, retirements=blocks.retirements)
    for block in blocks:
        cap = _spec_of(root, block.capability, blocks)
        used = {g.id for g in cap.groups} | {r.id for g in cap.groups for r in g.requirements}
        used |= {r for r in cap.retired if re.fullmatch(r"[gr][1-9]\d*", r)} | taken.get(block.capability, set())
        seen = used | {g.id for g in block.groups} | {r for g in block.groups for r, _ in g.requirements}

        groups = []
        for g in block.groups:
            gid = _fresh(g.id, block.capability, used, seen, pairs)
            fresh = [(r, _fresh(r, block.capability, used, seen, pairs), text) for r, text in g.requirements]
            keys = {r: n for r, n, _ in fresh}
            groups.append(Group(gid, g.title, [(n, text) for _, n, text in fresh], g.given,
                                tuple((keys.get(r, r), ids) for r, ids in g.relied)))
        moved = {o.split("#")[1]: n.split("#")[1] for o, n in pairs if o.startswith(block.capability + "#r")}
        out.append(block._replace(groups=groups, retires=tuple((moved.get(r, r), old) for r, old in block.retires),
                                  serves=backlog_serves.renumbered(block, pairs)))
        taken.setdefault(block.capability, set()).update(
            {g.id for g in groups} | {r for g in groups for r, _ in g.requirements})
    if blocks.universal:
        used = backlog_forms.universal_ids(root) | taken.get("universal", set())
        seen = used | {u for u, _ in blocks.universal}
        out.universal = [(_fresh(u, "universal", used, seen, pairs), text) for u, text in blocks.universal]
        taken.setdefault("universal", set()).update(u for u, _ in out.universal)
    if pairs:
        moved = dict(pairs)
        out[:] = [b._replace(groups=backlog_relied.renumbered(b.groups, pairs),    # b705
                             retires=tuple((moved.get(r, r) if "#" in r else r, old) for r, old in b.retires))
                  for b in out]         # a line of another capability's, `<cap>#r<n>` (b882)
        item.sections[SECTION] = render(out)
        item.request_lines = {moved.get(i, i): n for i, n in item.request_lines.items()}
    return pairs
