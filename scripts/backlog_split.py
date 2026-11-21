"""`work retitle` and `work split` (b459): an open item given a new title under its own id (items#r48, r49), and
requirement lines of an idea or a shaped item moved to a new item that derives from it (items#r50-r52). Each is one
commit of the item files it writes (backlog.retitle, backlog.split)."""
import re
from dataclasses import replace
from pathlib import Path

import shop_files
from backlog_items import Refused, find, label, next_name, one_line, rel_of, render
from backlog_section import SECTION, read, takes
from backlog_section import render as render_section

CLOSED = ("delivered", "refused", "withdrawn")
SPLITS = ("idea", "shaped")
IDENT = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)#(r[1-9]\d*)$")


def retitle(root, name, title):
    """The item `name` titled `title`, its id kept (items#r48); a closed item refused, naming it (items#r49)."""
    item = find(root, name)
    if item.status in CLOSED:
        raise Refused("work retitle: %s is %s; a closed item keeps its title" % (label(item), item.status))
    title = one_line(title, "title")
    if title.startswith("#"):
        raise Refused("work retitle: %s: the title starts with #, which would read as a heading" % label(item))
    before = label(item)
    item.title = title
    _commit(root, [item], "work retitle: %s -> \"%s\"" % (before, title))
    return item


def _chosen(item, idents):
    """{(capability, r<n>)} of `idents`, each a requirement line of the item; refused naming the first that is not
    (items#r51) or that does not read `<capability>#r<n>`."""
    if not idents:
        raise Refused("work split: %s: name a requirement line to split off with --requirement" % label(item))
    blocks, chosen = read(item, rel_of(item.name)), set()
    held = {(b.capability, r) for b in blocks for g in b.groups for r, _ in g.requirements}
    for ident in idents:
        match = IDENT.match(ident)
        if not match:
            raise Refused("work split: --requirement takes `<capability>#r<n>`, not %s" % ident)
        if match.groups() not in held:
            raise Refused("work split: %s is no requirement line of %s" % (ident, label(item)))
        chosen.add(match.groups())
    return blocks, chosen


def _apart(block, chosen):
    """(the block less the chosen lines, the block of them): each group's chosen lines, with its id, title and given
    block, go; the `retires:` pair of a chosen line and the id it retires go with it."""
    def lines(group, keep):
        return [(r, t) for r, t in group.requirements if ((block.capability, r) in chosen) != keep]
    stays = [g._replace(requirements=lines(g, True)) for g in block.groups]
    goes = [g._replace(requirements=lines(g, False)) for g in block.groups]
    moved = {r for g in goes for r, _ in g.requirements}
    pairs = tuple(p for p in block.retires if p[0] in moved)
    retired = {old for _, old in pairs}
    left = block._replace(groups=[g for g in stays if g.requirements], retires=tuple(
        p for p in block.retires if p[0] not in moved), retired=tuple(r for r in block.retired if r not in retired))
    out = block._replace(groups=[g for g in goes if g.requirements], terms=(), relations=(), new=None,
                         retires=pairs, retired=tuple(r for r in block.retired if r in retired))
    return left, out


def split(root, name, idents):
    """The chosen requirement lines of the idea or shaped item `name` moved to a new item that derives from it, with
    its status, provenance, ratings, dependencies and request (items#r50); an item in another state refused, naming it
    (items#r52), and a line the item does not hold refused, naming it (items#r51). One commit of both items."""
    item = find(root, name)
    takes(item, "work split", SPLITS)
    blocks, chosen = _chosen(item, idents)
    kept, moved = type(blocks)(), type(blocks)()
    for block in blocks:
        left, out = _apart(block, chosen)
        if left.groups or left.terms or left.relations or left.retired or left.language or left.new:
            kept.append(left)
        if out.groups:
            moved.append(out)
    for attr in ("universal", "upstreams", "models", "adapters", "packs"):
        setattr(kept, attr, getattr(blocks, attr))
    kept.universal_language, kept.universal_retired = blocks.universal_language, blocks.universal_retired
    said = sorted("%s#%s" % pair for pair in chosen)
    new = next_name(root)
    part = replace(item, name=new, ident="%s/%s" % (item.ident.rsplit("/", 1)[0], new),
                   title="%s (split from %s)" % (item.title, item.name), derives_from=item.name,
                   request_lines={k: v for k, v in item.request_lines.items() if k in said},
                   sections={"Notes": "Split from %s: %s." % (label(item), ", ".join(said)),
                             SECTION: render_section(moved)})
    item.request_lines = {k: v for k, v in item.request_lines.items() if k not in said}
    item.sections[SECTION] = render_section(kept)
    _commit(root, [item, part], "work split: %s -> %s, %s" % (label(item), new, ", ".join(said)))
    return item, part


def _commit(root, items, message):
    rels = [rel_of(i.name) for i in items]

    def write():
        for each, rel in zip(items, rels):
            path = Path(root) / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render(each), encoding="utf-8")
    shop_files.committed(root, rels, message, write)


def add_parsers(sub):
    p = sub.add_parser("retitle", help="give an item that is not closed a new title, keeping its id")
    p.add_argument("name")
    p.add_argument("title")
    p = sub.add_parser("split", help="move requirement lines of an item that is idea or shaped to a new item that "
                       "derives from it")
    p.add_argument("name")
    p.add_argument("--requirement", action="append", default=[], metavar="CAPABILITY#rN",
                   help="a requirement line of the item to move (repeatable)")


def cmd_retitle(args):
    print(label(retitle(args.root, args.name, args.title)))
    return 0


def cmd_split(args):
    item, part = split(args.root, args.name, args.requirement)
    print("%s split from %s" % (label(part), label(item)))
    return 0


COMMANDS = {"retitle": cmd_retitle, "split": cmd_split}
