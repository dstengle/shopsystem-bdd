"""`work line --remove <capability>` (b450): an item's block of a capability taken out of its `## Requirements`, with
the item's model block of the capability's area (its `### <area> model`, backlog_model) when no other block of the
item goes to that area; committed. And the other items that hold a capability new to the context (`holders`), each
with the batch it is in, which `work line --capability` and `--into` name when they refuse that capability."""
from backlog_items import Refused, commit, find, items, label
from backlog_model_area import area_of, new_block
from backlog_section import SECTION, read, render, takes

GONE = ("delivered", "refused", "withdrawn")


def _area(root, capability, blocks):
    """The area the capability's model lines go to, or None when it names none."""
    try:
        return area_of(root, capability, blocks)
    except Refused:
        return None


def retract(root, name, capability):
    """The item's block of `capability` and, unless another block of the item shares its area, its model block taken
    out and committed; the item. Refused, naming the capability, when the item holds no block of it."""
    item = find(root, name)
    takes(item)
    blocks = read(item, "the item %s" % item.name)
    block = next((b for b in blocks if b.capability == capability), None)
    if block is None:
        raise Refused("work line: %s holds no block of the capability %s" % (label(item), capability))
    area = _area(root, capability, blocks)
    blocks.remove(block)
    if area is not None and all(_area(root, b.capability, blocks) != area for b in blocks):
        blocks.models[:] = [m for m in blocks.models if m.area != area]
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s removes the capability %s" % (label(item), capability))
    return item


def holders(root, capability, besides=None):
    """Each item but `besides`, not delivered, refused or withdrawn, whose block makes `capability`, said as its label
    and, when it is in a batch, `in <batch>`; none where the backlog cannot be read (a copy of spec/ alone)."""
    try:
        found = [i for i in items(root) if i.name != besides and i.status not in GONE
                 and new_block(read(i, "the item %s" % i.name), capability) is not None]
    except Refused:
        return []
    import batch_plan
    said = []
    for item in found:
        batch = batch_plan.of_item(root, item.name) if item.status == "in-batch" else None
        said.append(label(item) + (" in %s" % batch.name if batch is not None else ""))
    return said
