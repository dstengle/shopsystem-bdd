"""`work line --capability` (b317): a capability new to the context written in an item, as a block of its
`## Requirements` (`### <name>`, then its `narrator:`, `group:` and `purpose:`; backlog_section reads and writes it),
refused when `spec/capabilities/<name>.md` exists. Laid over a spec (`lay`), the block writes the capability file
(its id under the context's, its title, narrator, group, `language: codified-2`, `retired: []`, `## Purpose`,
`## Terms`, `## Behaviour`) and its row under `spec/index.md`'s `## Composition`, before its lines, terms and rows go
into it as any block's do; taken out again (`unlay`), the file, its feature and the row are removed."""
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
HEADER = "| capability | narrator | group |\n|---|---|---|"


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


def text(root, block):
    """The capability file the block makes, its id under spec/index.md's `bounded-context/<path>`."""
    path = context_path(root)
    fields = dict(zip(NEW_FIELDS, block.new))
    title = block.capability.replace("-", " ").capitalize()
    return ("---\nid: capability/%s/%s\ntitle: %s\nnarrator: %s\ngroup: %s\nlanguage: codified-2\nretired: []\n---\n\n"
            "# %s\n\n## Purpose\n%s\n\n## Terms\n\n## Behaviour\n" % (path, block.capability, title, fields["narrator"],
                                                                     fields["group"], title, fields["purpose"]))


def _row(block):
    fields = dict(zip(NEW_FIELDS, block.new))
    return "| `%s` | %s | %s |" % (block.capability, fields["narrator"], fields["group"])


def lay(into, block, files):
    """The capability file written into `into/spec` and its row added to the last table of `## Composition` (the
    section and its table made at the end of spec/index.md when it has none); spec/index.md added to `files`."""
    path_of(into, block.capability).write_text(text(into, block))
    index = Path(into) / "spec" / "index.md"
    was = index.read_text()
    found = re.search(r"(?ms)^## Composition[ \t]*\n(.*?)(?=^## |\Z)", was)
    rows = list(re.finditer(r"(?m)^\|.*\|[ \t]*$", found.group(1))) if found else []
    if rows:
        at = found.start(1) + rows[-1].end()
        now = was[:at] + "\n" + _row(block) + was[at:]
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
    now = was.replace(made, "\n", 1) if was.endswith(made) else was.replace("\n" + _row(block), "", 1)
    if now != was:
        index.write_text(now)
        files.append("spec/index.md")
