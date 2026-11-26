"""A driven port an item makes (b701, batches r151): a new capability's block that says `kind: port` (`work line
--capability <c> --area <a> --port`) laid as an area of kind port, its model file made by the lay even with no model
lines (backlog_model_area's skeleton writes the kind), importing each area whose layer has a word the item's lines
of the port or its model lines of the port say, and imported in turn by the model file of each area a capability
block of the item is in whose lines say a word of the port's layer, so the lay raises no v_m1 (`lay`); taken out
again by the unlay, each import the lay added out (the model file at the batch's base, else as git last held it, not
holding it), the imports of a port spec/model/ held already put back as that version held them (f1), and the model
file the lay made removed when nothing else is left in it (`unlay`). A word is said when
it, one of its forms or its plural stands whole in the text, as backlog_area_move_lay reads a moved word's users."""
import re
from pathlib import Path

import backlog_area_move_lay as laid
import backlog_area_move_unlay
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


def lay(into, blocks, files):
    """Each driven port the item makes laid over `into/spec` after its model lines, each path changed added to
    `files`."""
    made = ports(blocks)
    for port in made:
        if backlog_model_area.made(into, port, blocks):
            files.append(laid._rel("model", port))
    for port in made:
        said = _text(into, port, blocks)
        _imports(into, port, [a for a in _areas(into) if a not in (port, SHARED) and _says(said, a, into)], files)
        users = {_area(into, b, blocks) for b in blocks} - {None, port}
        for area in sorted(a for a in users if backlog_model.model_path(into, a).is_file()):
            if _says(_text(into, area, blocks), port, into):
                _imports(into, area, [port], files)


def unlay(into, blocks, files, base=None):
    """The reverse of `lay`, after the model lines are out (backlog_model's unlay)."""
    made = ports(blocks)
    if not made:
        return
    backlog_area_move_unlay._imports(into, set(made), base, files)
    for port in made:
        rel = laid._rel("model", port)
        path = backlog_model.model_path(into, port)
        was = backlog_area_move_unlay.held(path, base) if path.is_file() else None
        if was is not None and laid._imported(path.read_text()) != laid._imported(was):   # a port spec/model/ held (f1)
            path.write_text(laid._with_imports(path.read_text(), laid._imported(was)))
            files.append(rel)
        if backlog_model_area.unmade(into, port, blocks) and rel not in files:
            files.append(rel)
