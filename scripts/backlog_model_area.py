"""The area an item's model lines go to (b387): a capability's `area:` in its file, or, for a capability new to the
context that a block of the item makes (`work line --capability`, b317), its block's `area:`, else its own name; and the model
file of an area that `spec/model/` does not hold yet, made by the lay (`made`, with the new capability's purpose as the
area's, of kind `port` when the block makes it a driven port, b701) and removed again by the unlay when nothing but
what it made is left, the areas it imports aside (`unmade`)."""
import re
from pathlib import Path

from backlog_items import Refused
from plumbing import shop_files

IMPORTS = re.compile(r"^imports:\s*\[.*\]\s*$", re.MULTILINE)


def _area(block):
    """A new capability's area: its block's `area:` when it has one, else its own name."""
    from backlog_section import NEW_FIELDS
    return dict(zip(NEW_FIELDS, block.new)).get("area") or block.capability


def new_block(blocks, capability):
    """The item's block that makes the capability `capability`, or None."""
    return next((b for b in blocks if getattr(b, "new", None) and b.capability == capability), None)


def area_block(blocks, area):
    """The item's block that makes a capability of the area `area`, or None."""
    return next((b for b in blocks if getattr(b, "new", None) and _area(b) == area), None)


def area_of(root, capability, blocks=()):
    """The area of `capability`: its own name when a block of the item makes it, else its file's `area:` (refused
    when the file has none, or there is no such codified capability)."""
    if new_block(blocks, capability) is not None:
        return _area(new_block(blocks, capability))
    from backlog_section import capability_file
    data, _ = shop_files.frontmatter(capability_file(root, capability).read_text())
    if not data.get("area"):
        raise Refused("work line: the capability %s names no area: its model lines have nowhere to go" % capability)
    return str(data["area"])


def model_path(root, area):
    return Path(root) / "spec" / "model" / ("%s.md" % area)


def skeleton(root, area, purpose, kind="core"):
    """The model file of a new area: its frontmatter (its kind), title, purpose and an empty ```model block."""
    title = area.replace("-", " ").capitalize()
    return ("---\nid: model/%s/%s\narea: %s\nkind: %s\nimports: []\n---\n\n# %s\n\n## Purpose\n\n%s\n\n```model\n```\n"
            % (shop_files.context_path(root), area, area, kind, title, purpose))


def _field(blocks, area, name, default=""):
    from backlog_section import NEW_FIELDS
    block = area_block(blocks, area)
    return dict(zip(NEW_FIELDS, block.new)).get(name) or default if block is not None else default


def purpose_of(blocks, area):
    return _field(blocks, area, "purpose")


def kind_of(blocks, area):
    """The kind of the area a block of the item makes: `port` of a driven port (b701), else core."""
    return _field(blocks, area, "kind", "core")


def _skeleton(root, area, blocks):
    return skeleton(root, area, purpose_of(blocks, area), kind_of(blocks, area))


def made(root, area, blocks):
    """The model file of `area` made when there is none and a block of the item makes the capability of that name;
    True when it was made."""
    path = model_path(root, area)
    if path.is_file() or area_block(blocks, area) is None:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_skeleton(root, area, blocks))
    return True


def unmade(root, area, blocks):
    """The model file `made` made removed when it holds nothing more than it did then, the areas it imports aside
    (backlog_port's, b701); True when it was removed."""
    path = model_path(root, area)
    if path.is_file() and area_block(blocks, area) is not None and \
            IMPORTS.sub("imports: []", path.read_text(), count=1) == _skeleton(root, area, blocks):
        path.unlink()
        return True
    return False
