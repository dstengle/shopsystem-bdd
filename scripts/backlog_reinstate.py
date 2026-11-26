"""A retirement or an import taken back out of an item (b688, drafting r79-r84).

`work line <item> --reinstate-model "<element header>"` takes the item's retirement of that model line out of its
`### retirements` block (backlog_retire), refused naming the model line when the item does not retire it;
`--reinstate-term "<word>"` (or `"<word> → <element>"`) the retirement of that term, refused naming the term; and
`--remove-import <pack>` the pack out of its `### imports` block (backlog_import), refused naming the pack when the
item does not import it. Each one commit of the item."""
from backlog_items import Refused, commit, find, label, one_line

FLAGS = ("reinstate_model", "reinstate_term", "remove_import")


def add_arguments(p):
    """`work line`'s options that take a retirement or an import back out of an item."""
    p.add_argument("--reinstate-model", metavar="HEADER", help="an element header the item retires (`object tag`), "
                   "its retirement taken out of the item")
    p.add_argument("--reinstate-term", metavar="TERM", help="a vocabulary entry the item retires (its word, or "
                   "`<word> → <element>`), its retirement taken out of the item")
    p.add_argument("--remove-import", metavar="PACK", help="a pack the item imports, its import taken out of the item")


def given(args):
    """True when the run is one of this module's."""
    return any(getattr(args, k, None) is not None for k in FLAGS)


def _term(what, term):
    """True when the retired entry `what` (`<word> → <element>`) is the term `term`, by its word or whole."""
    word, _, ref = what.partition(" → ")
    asked, _, element = term.partition("→")
    return word == asked.strip() and (not element.strip() or " ".join(element.split()) == ref)


def _opened(root, name):
    from backlog_section import read, takes
    item = find(root, name)
    takes(item)
    return item, read(item, "the item %s" % item.name)


def _kept(root, item, blocks, message):
    from backlog_section import SECTION
    from backlog_section import render as rendered
    item.sections[SECTION] = rendered(blocks)
    commit(root, item, "work line: %s %s" % (label(item), message))
    return item


def reinstate(root, name, kind, what):
    """The item's retirement of the model line or the term `what` taken out of it and committed."""
    item, blocks = _opened(root, name)
    what = one_line(what, kind).strip()
    match = (lambda r: r.what == what) if kind == "model line" else (lambda r: _term(r.what, what))
    found = [r for r in blocks.retirements if r.kind == kind and match(r)]
    if not found:
        raise Refused("work line: %s retires no %s %s" % (label(item), kind, what),
                      reason="%s not retired by the item" % kind, names=["%s:%s" % (kind, what)])
    blocks.retirements = [r for r in blocks.retirements if r not in found]
    return _kept(root, item, blocks, "no longer retires the %s %s" % (kind, found[0].what))


def remove_import(root, name, pack):
    """The item's import of the pack `pack` taken out of it and committed."""
    item, blocks = _opened(root, name)
    pack = one_line(pack, "pack").strip()
    if pack not in blocks.imports:
        raise Refused("work line: %s imports no pack %s" % (label(item), pack),
                      reason="pack not imported by the item", names=["pack:%s" % pack])
    blocks.imports.remove(pack)
    return _kept(root, item, blocks, "no longer imports the pack %s" % pack)


def cmd(args):
    """`work line` with `--reinstate-model`, `--reinstate-term` or `--remove-import`, alone; what was done, printed."""
    from backlog_cli import PIECES
    flags = [k for k in FLAGS if getattr(args, k, None) is not None]
    others = [k for k in PIECES + ("retires", "reword", "remove", "group", "in_group", "into")
              if getattr(args, k, None) is not None]
    if len(flags) != 1 or others:
        raise Refused("work line: --reinstate-model, --reinstate-term and --remove-import each alone")
    if flags[0] == "remove_import":
        item = remove_import(args.root, args.name, args.remove_import)
        print("%s: no longer imports the pack %s" % (label(item), args.remove_import))
        return 0
    kind = "model line" if flags[0] == "reinstate_model" else "term"
    item = reinstate(args.root, args.name, kind, getattr(args, flags[0]))
    print("%s: no longer retires the %s %s" % (label(item), kind, getattr(args, flags[0])))
    return 0
