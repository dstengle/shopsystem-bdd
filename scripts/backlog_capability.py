"""`work line --capability` (b317): a capability new to the context written in an item, as a block of its
`## Requirements` (`### <name>`, then its `narrator:`, `group:` and `purpose:`; backlog_section reads and writes it),
refused when `spec/capabilities/<name>.md` exists; with `--area`, its `area:` line after them (b645). Laid over a spec (`lay`), the block writes the capability file in
0.38's form (its id under the context's, its title, narrator, group, `area:` and `specifies:`, `language: codified-2`,
`retired: []`, `## Purpose`, `## Behaviour`, no empty section) and names it in its area's row of the one table
`| area | kind | capabilities |` under `spec/index.md`'s `## Composition` (b391; old tables `| capability | narrator |
group |` written in that form first, and put back as git held them by the unlay), before its lines, terms and rows go
into it as any block's do; taken out again (`unlay`), the file, its feature and the name are removed."""
import re
import subprocess
from pathlib import Path

from backlog_items import Refused, commit, find, label, one_line
from backlog_section import (
    CAP,
    INDEX,
    NEW_FIELDS,
    SECTION,
    UNIVERSAL,
    Block,
    read,
    render,
    takes,
)
from shop_files import context_path

GROUPS = ("service", "guarantees")
COMMAND = "work line --capability"
HEADER = "| area | kind | capabilities |\n|---|---|---|"


def path_of(root, capability):
    return Path(root) / "spec" / "capabilities" / ("%s.md" % capability)


def check(root, item, capability, group):
    """Refused, naming the capability, when its name is no capability name, its file exists in `spec/`, or the item
    holds a block for it already; naming the other item and its batch when another item holds one (b450); or when
    the group is neither service nor guarantees."""
    if not CAP.match("### %s" % capability) or capability in (UNIVERSAL, INDEX):
        raise Refused("%s: %s is no capability name: lowercase words joined by -" % (COMMAND, capability))
    if path_of(root, capability).exists():
        raise Refused("%s: the capability %s exists: spec/capabilities/%s.md" % (COMMAND, capability, capability))
    if any(b.capability == capability for b in read(item, "the item %s" % item.name)):
        raise Refused("%s: %s holds a block of the capability %s already" % (COMMAND, label(item), capability))
    others = __import__("backlog_retract").holders(root, capability, besides=item.name)
    if others:
        raise Refused("%s: the capability %s is new on %s already; its lines go into that item"
                      % (COMMAND, capability, ", ".join(others)))
    if group not in GROUPS:
        raise Refused("%s: the group %s is neither %s" % (COMMAND, group, " nor ".join(GROUPS)))


def add(root, name, capability, narrator, group, purpose, area=None):
    """The new capability's block written into the item `name` and committed, with its `area:` line when the person
    names the area (b645: an area of spec/model/ or a new one); the item."""
    item = find(root, name)
    takes(item, COMMAND)
    check(root, item, capability, group)
    if area is not None and (not CAP.match("### %s" % area) or area in (UNIVERSAL, INDEX)):
        raise Refused("%s: %s is no area name: lowercase words joined by -" % (COMMAND, area))
    new = (one_line(narrator, "narrator"), group, one_line(purpose, "purpose")) + ((area,) if area else ())
    blocks = read(item, "the item %s" % item.name)
    blocks.append(Block(capability, [], [], new=new))
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s a new capability %s" % (label(item), capability))
    return item


def add_arguments(p):
    """`work line`'s option of a new capability's area (b645)."""
    p.add_argument("--area", help="with --capability: the area the new capability is placed in, an area of "
                   "spec/model/ or a new one (default: the capability's own name)")


def cmd(args):
    """`work line <item> --capability <name> --narrator <who> [--group service|guarantees] [--area <area>]
    <purpose>`."""
    others = [k for k in ("into", "in_group", "retires", "reword", "remove", "term", "relation", "given", "universal",
                          "upstream", "recodify") if getattr(args, k) is not None] + (["no_line"] if args.no_line else [])
    if args.narrator is None or args.text is None or others:
        raise Refused("%s: takes --narrator and the capability's purpose, with --group service or guarantees "
                      "(default service), and no other piece" % COMMAND)
    item = add(args.root, args.name, args.capability, args.narrator, args.group or "service", args.text,
               getattr(args, "area", None))
    print("%s: a new capability %s" % (label(item), args.capability))
    return 0


def area(block):
    """The area of the model the capability's lines are read in: the block's own when it names one, else the
    capability's name."""
    return dict(zip(NEW_FIELDS, block.new)).get("area") or block.capability


def specifies(block):
    """What the capability is about: the service of its name, or the guarantees of its name."""
    fields = dict(zip(NEW_FIELDS, block.new))
    return ("service %s" if fields["group"] == "service" else "the %s guarantees") % block.capability


def text(root, block):
    """The capability file the block makes, in 0.38's form: its id under spec/index.md's `bounded-context/<path>`,
    its `area:` and `specifies:`, and no empty section (`## Terms` is made when a term is laid)."""
    path = context_path(root)
    fields = dict(zip(NEW_FIELDS, block.new))
    title = block.capability.replace("-", " ").capitalize()
    return ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: %s\ngroup: %s\narea: %s\nspecifies: %s\n"
            "language: codified-2\nretired: []\n---\n\n# %s\n\n## Purpose\n%s\n\n## Behaviour\n"
            % (path, block.capability, title, fields["narrator"], fields["group"], area(block), specifies(block),
               title, fields["purpose"]))


def _cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _composition(text):
    """The body's span of `## Composition` in spec/index.md's `text`, or None."""
    found = re.search(r"(?ms)^## Composition[ \t]*\n(.*?)(?=^## |\Z)", text)
    return found.span(1) if found else None


def _old(body):
    """Whether the Composition section's `body` holds the old tables `| capability | narrator | group |`."""
    rows = re.findall(r"(?m)^\|.*\|[ \t]*$", body)
    return bool(rows) and _cells(rows[0])[0] == "capability"


def _field(path, name):
    """The frontmatter field `name` of the file at `path`, or None."""
    head = re.match(r"(?s)---\n(.*?)\n---", path.read_text()) if path.exists() else None
    found = re.search(r"(?m)^%s:[ \t]*(\S.*?)[ \t]*$" % name, head.group(1)) if head else None
    return found.group(1) if found else None


AREA = re.compile(r"(?m)\A### (\S+) \(([^()\s]+)\)[ \t]*$")


def _converted(root, body, block):
    """The old tables' `body` written in the index form (b391, f1 of batch-51): its prose before the first heading
    or table kept, then one table `| area | kind | capabilities |`, a row for each area of the capabilities the old
    tables name whose file says `area:` (in the order they name them), its kind from spec/model/<area>.md's `kind`,
    else its `### <area> (<kind>)` heading's, else core, the new capability named last in its area's row; then every
    subsection that is no `### <area> (<kind>)` table (the Retired lists), verbatim."""
    areas, kinds = {}, {}
    names = re.findall(r"(?m)^\|[ \t]*`([^`|]+)`[ \t]*\|", body) + [block.capability]
    for name in names:
        where = area(block) if name == block.capability else _field(path_of(root, name), "area")
        if where and name not in areas.setdefault(where, []):
            areas[where].append(name)
    subsections = [m.group(0) for m in re.finditer(r"(?ms)^###[ \t].*?(?=^###[ \t]|\Z)", body)]
    kept = []
    for sub in subsections:
        heading = AREA.match(sub)
        if heading and _old(sub):
            kinds[heading.group(1)] = heading.group(2)
        else:
            kept.append(sub.rstrip("\n") + "\n")
    model = Path(root) / "spec" / "model"
    rows = ["| %s | %s | %s |" % (a, _field(model / ("%s.md" % a), "kind") or kinds.get(a, "core"), ", ".join(n))
            for a, n in areas.items()]
    lead = re.split(r"(?m)^(?:###|\|)", body, maxsplit=1)[0].rstrip("\n")
    return ((lead + "\n\n" if lead.strip() else "\n") + "\n".join(["%s\n%s\n" % (HEADER, "\n".join(rows))] + kept)
            + ("\n" if body.endswith("\n\n") else ""))


def _held(root, body, block):
    """The old tables' Composition body git last held in spec/index.md that `_converted` makes `body` of, or None."""
    def git(*args):
        return subprocess.run(["git", "-C", str(Path(root) / "spec"), *args], capture_output=True, text=True)
    log = git("log", "--format=%H", "--", "index.md")
    for sha in log.stdout.split() if log.returncode == 0 else ():
        text = git("show", "%s:./index.md" % sha).stdout
        span = _composition(text)
        old = text[span[0]:span[1]] if span else ""
        if _old(old) and _converted(root, old, block) == body:
            return old
    return None


def _with(body, block, root):
    """The Composition section's `body` with the capability named in its area's row of the table `| area | kind |
    capabilities |` (the row, and the table, made when missing); old tables `| capability | narrator | group |`
    written in the index form first (`_converted`)."""
    if _old(body):
        return _converted(root, body, block)
    rows = list(re.finditer(r"(?m)^\|.*\|[ \t]*$", body))
    if not rows:
        return body.rstrip("\n") + ("\n\n" if body.strip() else "\n") + "%s\n%s\n" % (HEADER, _row(block))
    for row in rows[2:]:
        cells = _cells(row.group(0))
        if cells[0] == area(block):
            names = [n for n in cells[2].split(",") if n.strip()] + [" %s" % block.capability]
            cells[2] = ",".join(names).strip()
            return body[:row.start()] + "| %s |" % " | ".join(cells) + body[row.end():]
    at = rows[-1].end()
    return body[:at] + "\n" + _row(block) + body[at:]


def _without(body, block, root):
    """The reverse of `_with`: the old tables git held put back when `_with` converted them and nothing else changed
    the section since (`_held`); else the capability out of its area's row, the row out when `_with` made it, the
    table out when no row is left."""
    held = _held(root, body, block)
    if held is not None:
        return held
    rows = list(re.finditer(r"(?m)^\|.*\|[ \t]*\n?", body))
    for row in rows[2:]:
        cells = _cells(row.group(0))
        if cells[0] != area(block) or block.capability not in [n.strip() for n in cells[2].split(",")]:
            continue
        if row.group(0).rstrip("\n") == _row(block):
            body = body[:row.start()] + body[row.end():]
            if len(rows) == 3:
                body = body.replace(HEADER + "\n", "", 1)
                body = re.sub(r"\n+\Z", "\n", body) if body.strip() else ""
            return body
        cells[2] = ", ".join(n.strip() for n in cells[2].split(",") if n.strip() != block.capability)
        return body[:row.start()] + "| %s |" % " | ".join(cells) + row.group(0)[len(row.group(0).rstrip("\n")):] \
            + body[row.end():]
    return body


def _row(block):
    return "| %s | core | %s |" % (area(block), block.capability)


def lay(into, block, files):
    """The capability file written into `into/spec` and the capability named in its area's row of `## Composition`
    (`_with`; the section made at the end of spec/index.md when it has none); spec/index.md added to `files`."""
    path_of(into, block.capability).write_text(text(into, block))
    index = Path(into) / "spec" / "index.md"
    was = index.read_text()
    span = _composition(was)
    if span:
        now = was[:span[0]] + _with(was[span[0]:span[1]], block, into) + was[span[1]:]
    else:
        now = was.rstrip("\n") + "\n\n## Composition\n\n%s\n%s\n" % (HEADER, _row(block))
    index.write_text(now)
    files.append("spec/index.md")


def unlay(into, block, files):
    """The reverse of `lay`: the capability file, its feature and its Composition row removed (the section too when
    `lay` made it), each path added to `files`."""
    for rel in ("spec/capabilities/%s.md" % block.capability, "features/%s.feature" % block.capability):
        if (Path(into) / rel).exists():
            (Path(into) / rel).unlink()
            files.append(rel)
    index = Path(into) / "spec" / "index.md"
    was = index.read_text()
    made = "\n\n## Composition\n\n%s\n%s\n" % (HEADER, _row(block))
    span = _composition(was)
    if was.endswith(made):
        now = was[:-len(made)] + "\n"
    elif span:
        now = was[:span[0]] + _without(was[span[0]:span[1]], block, into) + was[span[1]:]
    else:
        now = was
    if now != was:
        index.write_text(now)
        files.append("spec/index.md")
