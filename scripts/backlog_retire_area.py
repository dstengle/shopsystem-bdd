"""An area an item retires (b898, drafting r114-r118, applying r48-r50): an area that holds nothing.

`work line <item> --retire-area <area>` keeps `- area `<area>`` in the item's `### retirements` block (backlog_retire),
refused naming the area when the domain model holds no `spec/model/<area>.md`, naming the model line when its model
fence declares one, naming the term when its layer holds an entry, and naming the requirement `<cap>#r<n>` when a
capability of the area (its `area:`, else its own name) holds a live one (`retire_area`). The lay (`lay`) takes out
the area's model file and its layer, the area out of every other model file's `imports:`, and `area:` and
`specifies:` out of each capability of the area, which holds only retired ids; the Composition is written again by
the apply (spec_composition)."""
import re
from pathlib import Path

from backlog_items import Refused
from plumbing import shop_files

FIELD = re.compile(r"(?m)^(area|specifies):[^\n]*\n")


def capabilities(root, area):
    """The capability files of `area`: their `area:`, else their own name."""
    return [p for p in sorted((Path(root) / "spec" / "capabilities").glob("*.md"))
            if str(shop_files.frontmatter(p.read_text())[0].get("area") or p.stem) == area]


def _held(root, area):
    """The first thing the area holds, as (reason, name, message), or None when it holds nothing."""
    import backlog_model
    import spec_read
    import spec_vocabulary
    path = backlog_model.model_path(root, area)
    lines, start, end = backlog_model._fence(path.read_text(), path.name)
    found = backlog_model.chunks(lines[start:end])
    if found:
        return "area holding a model line", "model line:%s" % found[0][0], "the model line %s" % found[0][0]
    term = next((e.term for e in spec_vocabulary.entries(root) if e.layer == area), None)
    if term is not None:
        return "area holding a term", "term:%s" % term, "the term %s" % term
    for cap in capabilities(root, area):
        rid = next((m.group(1) for _, line in spec_read.numbered(cap.read_text(), "Behaviour")
                    for m in [spec_read.REQ.match(line)] if m), None)
        if rid is not None:
            ident = "%s#%s" % (cap.stem, rid)
            return "area holding a requirement", "requirement:%s" % ident, "the requirement %s" % ident
    return None


def retire_area(root, name, area):
    """`--retire-area`: the retirement of the area `area`, which holds nothing, kept in the item."""
    import backlog_model
    from backlog_items import one_line
    from backlog_retire import Retirement, _kept, _opened
    item, blocks = _opened(root, name)
    area = one_line(area, "area").strip()
    if not backlog_model.model_path(root, area).is_file():
        raise Refused("work line: the domain model holds no area %s" % area, reason="area not in the domain model",
                      names=["area:%s" % area])
    held = _held(root, area)
    if held is not None:
        raise Refused("work line: the area %s holds %s; it is retired once it holds nothing" % (area, held[2]),
                      reason=held[0], names=[held[1]])
    return _kept(root, item, blocks, Retirement("area", area, area))


def lay(into, area, files):
    """The area `area` taken out of `into/spec`, each path changed added to `files`."""
    import backlog_area_move_lay as laid
    import backlog_model
    model = backlog_model.model_path(into, area)
    if not model.is_file():
        raise Refused("the domain model holds no area %s to retire" % area)
    model.unlink()
    files.append(laid._rel("model", area))
    layer = backlog_model.vocabulary_path(into, area)
    if layer.is_file():
        layer.unlink()
        files.append(laid._rel("vocabulary", area))
    for path in sorted(model.parent.glob("*.md")):
        text = path.read_text()
        if area in laid._imported(text):
            path.write_text(laid._with_imports(text, [n for n in laid._imported(text) if n != area]))
            files.append(laid._rel("model", path.stem))
    for path in capabilities(into, area):
        text = path.read_text()
        end = text.find("\n---\n", 4)
        head = FIELD.sub("", text[:end + 1])
        if head != text[:end + 1]:
            path.write_text(head + text[end + 1:])
            files.append(path.relative_to(into).as_posix())
