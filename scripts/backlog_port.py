"""A driven port an item makes (b701, batches r151): a new capability's block that says `kind: port` (`work line
--capability <c> --area <a> --port`) laid as an area of kind port, its model file made by the lay even with no model
lines (backlog_model_area's skeleton writes the kind), importing each area whose layer has a word the item's lines
of the port or its model lines of the port say, and imported in turn by the model file of each area a capability
block of the item is in whose lines say a word of the port's layer, so the lay raises no v_m1 (`lay`); taken out
again by the unlay, per item (b704): each import the item's lay would add, computed again from its blocks, taken out
unless the model file at the batch's base held it or a line left in the area (another item's, the spec's) or a line
of its model fence the base did not hold (another item's) still says a word of the imported layer, never reset to
the base, so a park keeps the imports another item laid on the same port and an amend (given the batch's base too)
takes out those its lines no longer need and keeps those the base held; and the model file the lay made removed when
nothing else is left in it (`unlay`). A word is said when
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


def _fenced(text, area):
    if text is None or "```model" not in text:
        return []
    lines, start, end = backlog_model._fence(text, laid._rel("model", area))
    return lines[start:end]


def _left(into, area, was):
    """What is left in `area` once the item's lines are out: the requirement lines of each capability of the area,
    and the lines of its model fence that the model file at the batch's base (`was`) did not hold, another item's
    model lines; none of the fence with no base, whose lines cannot be told apart."""
    lines = []
    for path in sorted((Path(into) / "spec" / "capabilities").glob("*.md")):
        try:
            if backlog_model_area.area_of(into, path.stem) != area:
                continue
        except Refused:
            continue
        lines += [x for x in path.read_text().split("\n") if x.startswith("- [r")]
    path = backlog_model.model_path(into, area)
    if was is not None:
        held = set(_fenced(was, area))
        lines += [x for x in _fenced(path.read_text(), area) if x not in held]
    return "\n".join(lines)


def _unimport(into, area, names, base, files):
    """Each of `names` out of the imports of `area`, unless the model file at `base` held it or what is left in the
    area says a word of its layer."""
    path = backlog_model.model_path(into, area)
    if not path.is_file() or not names:
        return
    text = path.read_text()
    have = laid._imported(text)
    was = backlog_area_move_unlay.held(path, base) if base else None
    before = laid._imported(was) if was is not None else []
    left = _left(into, area, was)
    kept = [n for n in have if n not in names or n in before or _says(left, n, into)]
    if kept != have:
        path.write_text(laid._with_imports(text, kept))
        files.append(laid._rel("model", area))


def unlay(into, blocks, files, base=None):
    """The reverse of `lay`, after the model lines are out (backlog_model's unlay), per item (b704)."""
    made = ports(blocks)
    for port in made:
        said = _text(into, port, blocks)
        _unimport(into, port, [a for a in _areas(into) if a not in (port, SHARED) and _says(said, a, into)], base,
                  files)
        users = {_area(into, b, blocks) for b in blocks} - {None, port}
        for area in sorted(users):
            if _says(_text(into, area, blocks), port, into):
                _unimport(into, area, [port], base, files)
    for port in made:
        rel = laid._rel("model", port)
        if backlog_model_area.unmade(into, port, blocks) and rel not in files:
            files.append(rel)
