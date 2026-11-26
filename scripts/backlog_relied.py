"""The core lines a port line of an item supports (b705; drafting r86, r87, items r71): `work line <item> --into <cap>
[--group <title> | --in g<n>] <line> --relied-on-by <cap>#r<n>[,...]`, the line written as `work line` writes it,
and `work line <item> --into <cap> --in g<n> --relied-on-by <ids>`, the group's last line; each id a live requirement
of its capability or one of the item's own lines, else refused naming it, the item unchanged. The ids kept under the
line as `Relied on by: <ids>` in the item's block (backlog_section reads it, backlog_section_render's `laid_group`
writes it, so the lay writes it into the capability file as spec_read reads it), one commit of the item; the item's
own ids carried to their new ids by `renumbered` (backlog_renumber). With `--retires <cap>#r<n>` and a line
(b759, drafting r88) the id checked and kept under the block's `retired:` with the line's pair under `retires:`, as
`work line --retires` keeps it, in the same commit."""
import re

import spec_read
from backlog_items import Refused, commit, find, label

HEAD = "Relied on by:"
IDENT = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*#r[1-9]\d*$")


def add_arguments(p):
    p.add_argument("--relied-on-by", dest="relied_on_by", action="extend", metavar="CAP#rN[,...]",
                   type=lambda v: [t.strip() for t in v.split(",") if t.strip()],
                   help="the requirements `<capability>#r<n>` the port line supports, kept as its `Relied on by:` "
                        "line: the requirement line given with --into, or the last line of the group --in names")


def given(args):
    return getattr(args, "relied_on_by", None) is not None


def ids_of(line):
    """The ids of a `Relied on by:` line, in its order."""
    return tuple(t.strip() for t in line[len(HEAD):].strip().rstrip(".").split(",") if t.strip())


def line_of(ids):
    return "%s %s" % (HEAD, ", ".join(ids))


def _live(root, capability):
    """The requirement ids of the capability as spec/ holds it; none when it holds no such codified capability."""
    from backlog_section import capability_file
    try:
        path = capability_file(root, capability)
    except Refused:
        return set()
    return {r.id for g in spec_read.capability(path).groups for r in g.requirements}


def check(root, blocks, ids):
    """Refused, naming the id, unless each is `<cap>#r<n>` of a live requirement or one of the item's own lines."""
    from backlog_section import ids as own
    held = set(own(blocks))
    for ident in ids:
        if not IDENT.match(ident) or (ident not in held and ident.split("#")[1] not in _live(root, ident.split("#")[0])):
            raise Refused("work line: no requirement has the requirement id %s" % ident)


def _with(group, rid, ids):
    """`group` with the ids under its requirement `rid`, after any it supports already."""
    had = dict(group.relied)
    had[rid] = tuple(dict.fromkeys(had.get(rid, ()) + tuple(ids)))
    return group._replace(relied=tuple(had.items()))


def supported_by(group, line):
    """`group` with the ids of a `Relied on by:` line under its last requirement, as backlog_section reads it."""
    return _with(group, group.requirements[-1][0], ids_of(line))


def supported(blocks, capability, rid, ids):
    """`blocks` with the ids under the requirement `rid` of the capability's block."""
    block = next(b for b in blocks if b.capability == capability)
    for k, group in enumerate(block.groups):
        if any(r == rid for r, _ in group.requirements):
            block.groups[k] = _with(group, rid, ids)
            return blocks
    raise Refused("work line: the item holds no requirement %s#%s" % (capability, rid))


def cmd(args):
    """`work line <item> --relied-on-by ...`: one commit of the item; what it printed."""
    import backlog_lines
    import backlog_retires
    from backlog_section import SECTION, read, render
    item = find(args.root, args.name)
    if args.into is None:
        raise Refused("work line: --relied-on-by takes --into <capability> with a requirement line or --in g<n>")
    capability = args.into
    retires = getattr(args, "retires", None)
    if retires is not None and args.text is None:
        raise Refused("work line: --retires with --relied-on-by takes a requirement line")
    if args.text is not None:
        old = retires and backlog_retires.check(args.root, item, retires, capability)[1]
        rid = backlog_lines.add_line_to(args.root, item, capability, args.text, args.group, args.in_group).split("#")[1]
        if old:
            backlog_retires.with_retired(item, capability, old, rid)
        blocks = read(item, "the item %s" % item.name)
    elif args.in_group is not None:
        blocks = read(item, "the item %s" % item.name)
        group = next((g for b in blocks if b.capability == capability for g in b.groups if g.id == args.in_group), None)
        if group is None or not group.requirements:
            raise Refused("work line: %s has no group %s in %s" % (label(item), args.in_group, capability))
        rid = group.requirements[-1][0]
    else:
        raise Refused("work line: --relied-on-by takes a requirement line or --in g<n>")
    check(args.root, blocks, args.relied_on_by)
    item.sections[SECTION] = render(supported(blocks, capability, rid, args.relied_on_by))
    said = "%s#%s relied on by %s%s" % (capability, rid, ", ".join(args.relied_on_by),
                                       ", retires %s" % retires if retires else "")
    commit(args.root, item, "work line: %s %s" % (label(item), said))
    print("%s: %s" % (label(item), said))
    if retires:
        import decision_amend
        for line in decision_amend.enforcing(args.root, retires):    # drafting r28, as --retires names them
            print(line)
    return 0


def renumbered(groups, pairs):
    """`groups` with each id their `Relied on by:` lines name carried to the new id `pairs` moved it to."""
    moved = dict(pairs)
    return [g._replace(relied=tuple((r, tuple(moved.get(i, i) for i in ids)) for r, ids in g.relied))
            for g in groups]
