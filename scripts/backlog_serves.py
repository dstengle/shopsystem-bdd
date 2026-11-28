"""A requirement group dedicated to a job on an item (decision 0140, b641; drafting r71, batches r124): `work line
<item> --serves <capability>#g<n> <job>`, a live group of the capability or one of the item's own, and `work line
<item> --into <capability> [--group <title>] --serves <job> <line>` (or the line before --serves), the group the line
goes into (one argument, the job, read when the line follows it or --into is given: `_read`, b839), the requirement it
added printed before the pair (drafting r93, b799); a job the product does not hold, while its product file is kept,
refused naming the job (drafting r92, b799), a job held when the product holds one of its name, given by its name or
its id, as `spec check` reads it, and a product file not of the product form checking nothing and named (drafting r96,
r97, b803); each the pair
(g<n>, job) under the `serves: [g<n> <job>, ...]` line of the item's block of the capability (backlog_section),
one commit of the item. Laid by `lay` into the group's `serves: <job>, ...` line under its heading in the capability
file (spec_read reads it, `spec check` its serves fact); a pair a live group serves already, or another open item holds, refused; the pairs
of the item's own groups carried to their new ids by `renumbered` (backlog_renumber)."""
import re
import sys
from pathlib import Path

import product_store
import spec_read
from backlog_items import Refused, commit, find, items, label
from model_product import name_of

GROUP = re.compile(r"^(?P<cap>[a-z0-9]+(?:-[a-z0-9]+)*)#(?P<g>g[1-9]\d*)$")


def add_arguments(p):
    p.add_argument("--serves", nargs="+", action="extend", metavar="CAP#gN JOB",
                   help="the requirement group `<capability>#g<n>` (a live one, or the item's own) and the job it "
                        "serves, written into the item's block of the capability; with --into and a requirement line "
                        "(before or after it), the job alone, which the group the line goes into serves")


def given(args):
    return getattr(args, "serves", None) is not None


def _job(root, job):
    """The job and what is said of the product, refused when it is not a job's name or id, and, while the product
    exists (its product file is kept), when the product does not hold it (drafting r92): the reason `job outside the
    product`, naming the job. A job is held when the product holds a job of its name, by its name or its id, as `spec
    check` reads it (model_product's `name_of`, drafting r97); a product file not of the product form, which `spec
    check` only warns of, checks nothing and is said, naming the file (drafting r96, b803)."""
    if not spec_read.JOB.match(job):
        raise Refused("work line: --serves: %r is not a job's name or id" % job)
    if not (Path(root) / product_store.REL).is_file():
        return job, None
    try:
        jobs = product_store.read(root)["jobs"]
    except Refused as why:
        return job, "work line: --serves: %s; the job %s not checked against the product" % (
            str(why).replace("{names}", product_store.REL), job)
    if name_of(job) not in {name_of(j) for j in jobs}:
        raise Refused("work line: --serves: the product holds no job %s" % job, reason="job outside the product",
                      names=["job:%s" % job])
    return job, None


def _groups(root, capability, block):
    """The ids of the capability's live groups and of the item's own groups of it."""
    from backlog_section import capability_file
    own = {g.id for g in block.groups} if block is not None else set()
    if block is not None and block.new:
        return own
    return own | {g.id for g in spec_read.capability(capability_file(root, capability)).groups}


def _holder(root, item, capability, gid, job):
    """Another open item whose block of the capability holds the pair (gid, job), or None."""
    from backlog_retract import GONE
    from backlog_section import read
    for other in items(root):
        if other.name != item.name and other.status not in GONE and any(
                b.capability == capability and (gid, job) in b.serves for b in read(other, "the item %s" % other.name)):
            return other
    return None


def dedicate(root, item, capability, gid, job):
    """The pair (gid, job) under the item's block of the capability; nothing committed. Refused, naming the group,
    when neither the capability nor the item holds it; and, naming the group and the job, when the capability's live
    group serves the job already or another open item holds the pair."""
    from backlog_lines import block_of
    from backlog_section import SECTION, capability_file, read, render, takes
    takes(item)
    blocks = read(item, "the item %s" % item.name)
    found = next((b for b in blocks if b.capability == capability), None)
    if gid not in _groups(root, capability, found):
        raise Refused("work line: there is no requirement group %s#%s in the capability or in %s"
                      % (capability, gid, label(item)))
    own = {g.id for g in found.groups} if found is not None else set()
    if gid not in own and any(g.id == gid and job in g.serves
                              for g in spec_read.capability(capability_file(root, capability)).groups):
        raise Refused("work line: the requirement group %s#%s serves the job %s already" % (capability, gid, job))
    other = _holder(root, item, capability, gid, job)
    if other is not None:
        raise Refused("work line: %s dedicates the requirement group %s#%s to the job %s already"
                      % (label(other), capability, gid, job))
    block = block_of(blocks, capability)
    if (gid, job) not in block.serves:
        blocks[blocks.index(block)] = block._replace(serves=tuple(block.serves) + ((gid, job),))
    item.sections[SECTION] = render(blocks)


def _read(args):
    """The words `--serves` took, read as the CLI adapter means them (b839): two, `<capability>#g<n> <job>`, only when
    the first has the group form; else one, the job, when a line follows or --into is given, a second word, which
    argparse's nargs='+' takes from the line's place, the requirement line itself."""
    words = list(args.serves)
    if words and not GROUP.match(words[0]) and (args.into is not None or len(words) > 1):
        if len(words) > 2 or (len(words) == 2 and args.text is not None):
            raise Refused("work line: --serves takes one job beside a requirement line, not %s" % " ".join(words[1:]))
        if len(words) == 2:
            args.text = words[1]
        args.serves = words[:1]


def cmd(args):
    """`work line <item> --serves ...`: one commit of the item; what it printed."""
    item, added = find(args.root, args.name), None
    _read(args)
    if len(args.serves) == 2 and args.text is None:
        m = GROUP.match(args.serves[0])
        if not m:
            raise Refused("work line: --serves: %r is not a requirement group <capability>#g<n>" % args.serves[0])
        capability, gid = m.group("cap"), m.group("g")
        job, notice = _job(args.root, args.serves[1])
    elif len(args.serves) == 1 and args.text is not None and args.into is not None:
        import backlog_lines
        from backlog_section import read
        job, notice = _job(args.root, args.serves[0])
        capability = args.into
        rid = backlog_lines.add_line_to(args.root, item, capability, args.text, args.group, args.in_group).split("#")[1]
        block = next(b for b in read(item, "the item %s" % item.name) if b.capability == capability)
        gid = next(g.id for g in block.groups if any(r == rid for r, _ in g.requirements))
        added = "%s#%s %s" % (capability, rid, args.text)
    else:
        raise Refused("work line: --serves takes a requirement group <capability>#g<n> and a job, or a job beside "
                      "a requirement line and --into")
    dedicate(args.root, item, capability, gid, job)
    if notice is not None:  # a product not of the product form named, as spec check's w_unformed_product names it
        print(notice, file=sys.stderr)
    commit(args.root, item, "work line: %s %s#%s serves %s" % (label(item), capability, gid, job))
    if added is not None:   # the requirement the line added, named with its group and the job (drafting r93)
        print("%s: %s" % (label(item), added))
    print("%s: %s#%s serves %s" % (label(item), capability, gid, job))
    return 0


def renumbered(block, pairs):
    """The block's pairs, each of the item's own groups under the id `pairs` moved it to."""
    own = {g.id for g in block.groups}
    moved = {o.split("#")[1]: n.split("#")[1] for o, n in pairs if o.startswith(block.capability + "#g")}
    return tuple((moved.get(g, g) if g in own else g, job) for g, job in block.serves)


def _heading(text, gid):
    found = re.search(r"(?m)^### \[%s\] .*$" % gid, text)
    if found is None:
        raise Refused("there is no requirement group %s to serve a job in the capability" % gid)
    return found.end()


def lay(text, serves):
    """`text`, a capability file's, with each pair's job on its group's `serves:` line, made under its heading."""
    for gid, job in serves:
        at = _heading(text, gid)
        rest = text[at + 1:]
        line = rest.split("\n", 1)[0]
        if line.startswith(spec_read.SERVES):
            jobs = spec_read.jobs_of(line)
            new = line if job in jobs else "%s %s" % (spec_read.SERVES, ", ".join(jobs + [job]))
            text = text[:at + 1] + new + rest[len(line):]
        else:
            text = text[:at] + "\n%s %s" % (spec_read.SERVES, job) + text[at:]
    return text
