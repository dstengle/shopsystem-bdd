"""A driven port an item makes (b701, batches r151): a new capability's block that says `kind: port` (`work line
--capability <c> --area <a> --port`) laid as an area of kind port, its model file made by the lay even with no model
lines (backlog_model_area's skeleton writes the kind), importing each area whose layer has a word the item's lines
of the port or its model lines of the port say, and imported in turn by the model file of each area a capability
block of the item is in whose lines say a word of the port's layer, so the lay raises no v_m1 (`lay`). Every other
area the item makes is laid alike (b830: `areas`), its model file made only when it imports an area. A word is said when
it, one of its forms or its plural stands whole in the text, as backlog_area_move_lay reads a moved word's users."""
import re
from pathlib import Path

import backlog_area_move_lay as laid
import backlog_model
import backlog_model_area
from backlog_items import Refused
from backlog_section import laid_group

SHARED = "shared"


def ports(blocks):
    """The areas the item's blocks make driven ports, in their order."""
    from backlog_section import NEW_FIELDS
    return list(dict.fromkeys(backlog_model_area._area(b) for b in blocks
                              if getattr(b, "new", None) and dict(zip(NEW_FIELDS, b.new)).get("kind") == "port"))


def _area(into, block, blocks):
    try:
        return backlog_model_area.area_of(into, block.capability, blocks)
    except Refused:          # a capability of no area: its lines read no area's layer
        return None


def _text(into, area, blocks):
    """What the item says in `area`: the lines of its blocks of capabilities in the area and its model lines there."""
    lines = [laid_group(g) for b in blocks if _area(into, b, blocks) == area for g in b.groups]
    lines += [x for m in getattr(blocks, "models", ()) if m.area == area for x in m.lines]
    return "\n".join(lines)


def _says(text, area, into):
    """Whether `text` says a word of the layer of `area`."""
    words = laid._words(laid._all(into, area))
    if not words or not text:
        return False
    return bool(re.search(r"(?i)\b(?:%s)\b" % "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)),
                          text))


def _areas(into):
    return sorted(p.stem for p in (Path(into) / "spec" / "model").glob("*.md"))


def _imports(into, area, names, files):
    path = backlog_model.model_path(into, area)
    text = path.read_text()
    have = laid._imported(text)
    new = [n for n in names if n not in have and n != area]
    if new:
        path.write_text(laid._with_imports(text, have + new))
        files.append(laid._rel("model", area))


def areas(blocks):
    """The areas the item's blocks make (b830), its driven ports first, in their order."""
    made = [backlog_model_area._area(b) for b in blocks if getattr(b, "new", None)]
    return list(dict.fromkeys(ports(blocks) + made))


def _needed(into, area, blocks):
    """The areas whose layer the item says a word of in `area`, the area itself and the shared layer aside."""
    said = _text(into, area, blocks)
    return [a for a in _areas(into) if a not in (area, SHARED) and _says(said, a, into)]


def lay(into, blocks, files):
    """Each area the item makes laid over `into/spec` after its model lines, each path changed added to `files`: a
    driven port's model file made, and each made area importing the areas whose words its lines say, a core area's
    model file made only when it imports one (b830), and imported by each other area of the item that says its
    words."""
    made = ports(blocks)
    for port in made:
        if backlog_model_area.made(into, port, blocks):
            files.append(laid._rel("model", port))
    for area in areas(blocks):
        needed = _needed(into, area, blocks)
        if needed and backlog_model_area.made(into, area, blocks):
            files.append(laid._rel("model", area))
        if backlog_model.model_path(into, area).is_file():
            _imports(into, area, needed, files)
        users = {_area(into, b, blocks) for b in blocks} - {None, area}
        for user in sorted(a for a in users if backlog_model.model_path(into, a).is_file()):
            if _says(_text(into, user, blocks), area, into):
                _imports(into, user, [area], files)
