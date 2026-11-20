"""`work line --capability` (b317): a capability new to the context written in an item, as a block of its
`## Requirements` (`### <name>`, then its `narrator:`, `group:` and `purpose:`; backlog_section reads and writes it),
refused when `spec/capabilities/<name>.md` exists. Laid over a spec (`lay`), the block writes the capability file in
0.38's form (its id under the context's, its title, narrator, group, `area:` and `specifies:`, `language: codified-2`,
`retired: []`, `## Purpose`, `## Behaviour`, no empty section) and names it in its area's row of the one table
`| area | kind | capabilities |` under `spec/index.md`'s `## Composition` (b391), before its lines, terms and rows go
into it as any block's do; taken out again (`unlay`), the file, its feature and the name are removed."""
import re
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
    holds a block for it already; or when the group is neither service nor guarantees."""
    if not CAP.match("### %s" % capability) or capability in (UNIVERSAL, INDEX):
        raise Refused("%s: %s is no capability name: lowercase words joined by -" % (COMMAND, capability))
    if path_of(root, capability).exists():
        raise Refused("%s: the capability %s exists: spec/capabilities/%s.md" % (COMMAND, capability, capability))
    if any(b.capability == capability for b in read(item, "the item %s" % item.name)):
        raise Refused("%s: %s holds a block of the capability %s already" % (COMMAND, label(item), capability))
    if group not in GROUPS:
        raise Refused("%s: the group %s is neither %s" % (COMMAND, group, " nor ".join(GROUPS)))


def add(root, name, capability, narrator, group, purpose):
    """The new capability's block written into the item `name` and committed; the item."""
    item = find(root, name)
    takes(item, COMMAND)
    check(root, item, capability, group)
    new = (one_line(narrator, "narrator"), group, one_line(purpose, "purpose"))
    blocks = read(item, "the item %s" % item.name)
    blocks.append(Block(capability, [], [], new=new))
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s a new capability %s" % (label(item), capability))
    return item


def cmd(args):
    """`work line <item> --capability <name> --narrator <who> [--group service|guarantees] <purpose>`."""
    others = [k for k in ("into", "in_group", "retires", "reword", "remove", "term", "relation", "given", "universal",
                          "upstream", "recodify") if getattr(args, k) is not None] + (["no_line"] if args.no_line else [])
    if args.narrator is None or args.text is None or others:
        raise Refused("%s: takes --narrator and the capability's purpose, with --group service or guarantees "
                      "(default service), and no other piece" % COMMAND)
    item = add(args.root, args.name, args.capability, args.narrator, args.group or "service", args.text)
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


def _with(body, block):
    """The Composition section's `body` with the capability named in its area's row of the table `| area | kind |
    capabilities |` (the row, and the table, made when missing); an old table `| capability | narrator | group |`
    given the capability's row."""
    rows = list(re.finditer(r"(?m)^\|.*\|[ \t]*$", body))
    if rows and _cells(rows[0].group(0))[0] == "capability":
        at = rows[-1].end()
        return body[:at] + "\n" + _old_row(block) + body[at:]
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


def _without(body, block):
    """The reverse of `_with`: the capability out of its area's row, the row out when `_with` made it, the table out
    when no row is left."""
    old = "\n" + _old_row(block)
    if old in body:
        return body.replace(old, "", 1)
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


def _old_row(block):
    fields = dict(zip(NEW_FIELDS, block.new))
    return "| `%s` | %s | %s |" % (block.capability, fields["narrator"], fields["group"])


def lay(into, block, files):
    """The capability file written into `into/spec` and the capability named in its area's row of `## Composition`
    (`_with`; the section made at the end of spec/index.md when it has none); spec/index.md added to `files`."""
    path_of(into, block.capability).write_text(text(into, block))
    index = Path(into) / "spec" / "index.md"
    was = index.read_text()
    span = _composition(was)
    if span:
        now = was[:span[0]] + _with(was[span[0]:span[1]], block) + was[span[1]:]
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
        now = was[:span[0]] + _without(was[span[0]:span[1]], block) + was[span[1]:]
    else:
        now = was
    if now != was:
        index.write_text(now)
        files.append("spec/index.md")
