"""An item's requirement lines (capability readiness; workflow simplification plan 3, D2-D5): the item file's
`## Requirements` section read and written, `work line` giving a new line the next ids of its capability, and the
section laid over a copy of `spec/`, where the bar checks it.

The section holds one `### <capability>` block for each capability the lines go into, in the capability file's own
syntax one heading level down: optional term bullets first, then `#### [g<n>] <title>` groups of `- [r<n>] <statement>`
bullets, one line each. The lines stay on the item until its batch merges; `spec/` itself is never written here."""
import re
import shutil
from collections import namedtuple
from pathlib import Path

import spec_lexicon
import spec_read
from backlog_items import Refused, commit, find, label, one_line

SECTION = "Requirements"
Group = namedtuple("Group", "id title requirements")
Block = namedtuple("Block", "capability terms groups")
TAKES = ("idea", "shaped")

CAP = re.compile(r"^### ([a-z0-9]+(?:-[a-z0-9]+)*)$")
GROUP = re.compile(r"^#### \[(g[1-9]\d*)\] (\S.*)$")
REQ = re.compile(r"^- \[(r[1-9]\d*)\] (\S.*)$")


def read(item, rel):
    """The blocks of the item's `## Requirements`, in file order; malformed text is refused, naming the file."""
    def refuse(what):
        raise Refused("%s: %s: %s" % (rel, SECTION, what))
    blocks = []
    for line in item.sections.get(SECTION, "").split("\n"):
        if not line.strip():
            continue
        if (m := CAP.match(line)):
            if any(b.capability == m.group(1) for b in blocks):
                refuse("the capability %s has two blocks" % m.group(1))
            blocks.append(Block(m.group(1), [], []))
        elif (m := GROUP.match(line)):
            if not blocks:
                refuse("the group %s comes before any `### <capability>` heading" % m.group(1))
            if any(g.id == m.group(1) for g in blocks[-1].groups):
                refuse("the group %s is there twice" % m.group(1))
            blocks[-1].groups.append(Group(m.group(1), m.group(2).strip(), []))
        elif (m := REQ.match(line)):
            if not blocks or not blocks[-1].groups:
                refuse("the requirement %s comes before any `#### [g<n>]` heading" % m.group(1))
            if m.group(1) in {r for g in blocks[-1].groups for r, _ in g.requirements}:
                refuse("the requirement %s is there twice" % m.group(1))
            blocks[-1].groups[-1].requirements.append((m.group(1), m.group(2).strip()))
        elif line.startswith("- **"):
            if not blocks or blocks[-1].groups:
                refuse("a term bullet that is not before the groups of a `### <capability>` block: %s" % line)
            blocks[-1].terms.append(line.strip())
        else:
            refuse("a line that is no heading, requirement or term bullet: %s" % line)
    return blocks


def render(blocks):
    """The section's text, byte-stable: `read` of it gives `blocks` back."""
    out = []
    for block in blocks:
        parts = ["### %s" % block.capability] + (["\n".join(block.terms)] if block.terms else [])
        parts += ["#### [%s] %s" % (g.id, g.title) + "".join("\n- [%s] %s" % r for r in g.requirements)
                  for g in block.groups]
        out.append("\n\n".join(parts))
    return "\n\n".join(out)


def ids(blocks):
    """`<capability>#r<n>` of each requirement, in file order."""
    return ["%s#%s" % (b.capability, r) for b in blocks for g in b.groups for r, _ in g.requirements]


def capability_file(root, capability):
    """spec/capabilities/<capability>.md of `root`; refused when there is none, or it is not codified (D4)."""
    path = Path(root) / "spec" / "capabilities" / ("%s.md" % capability)
    if "/" in capability or not spec_read.codified(path):
        raise Refused("there is no codified capability %s in spec/capabilities/" % capability)
    return path


def _number(ident):
    return int(ident[1:])


def next_ids(root, capability, blocks):
    """The next `g<n>` and `r<n>` free in the capability: one above the highest over its file's groups, requirements
    and retired ids, and the item's own block for it (D3)."""
    cap = spec_read.capability(capability_file(root, capability))
    groups = [g.id for g in cap.groups] + [g.id for b in blocks if b.capability == capability for g in b.groups]
    reqs = [r.id for g in cap.groups for r in g.requirements] + [r for r in cap.retired if re.fullmatch(r"r\d+", r)]
    reqs += [r for b in blocks if b.capability == capability for g in b.groups for r, _ in g.requirements]
    return "g%d" % (max(map(_number, groups), default=0) + 1), "r%d" % (max(map(_number, reqs), default=0) + 1)


def _takes(item, command="work line"):
    if item.status not in TAKES:
        raise Refused("%s: %s is %s; %s takes an item that is idea or shaped" % (command, label(item), item.status,
                                                                               command))


def _text(text, what, item, command="work line"):
    text = one_line(text, what)
    if text.startswith("#"):
        raise Refused("%s: %s: the %s starts with #, which would read as a heading" % (command, label(item), what))
    return text


def _block(blocks, capability):
    found = next((b for b in blocks if b.capability == capability), None)
    if found is None:
        found = Block(capability, [], [])
        blocks.append(found)
    return found


def add_line_to(root, item, capability, text, group=None, in_group=None, command="work line"):
    """Write one requirement into the item's block for `capability`, in the group `in_group` or a new group titled
    `group` (else the item's title); nothing is committed. Its `<capability>#r<n>`. `command` names the refusals."""
    _takes(item, command)
    capability_file(root, capability)
    text = _text(text, "line", item, command)
    rel = "the item %s" % item.name
    blocks = read(item, rel)
    g_next, r_next = next_ids(root, capability, blocks)
    block = _block(blocks, capability)
    if in_group is not None:
        target = next((g for g in block.groups if g.id == in_group), None)
        if target is None:
            raise Refused("work line: %s has no group %s in %s" % (label(item), in_group, capability))
    else:
        target = Group(g_next, _text(group, "group title", item, command) if group is not None else item.title, [])
        block.groups.append(target)
    target.requirements.append((r_next, text))
    item.sections[SECTION] = render(blocks)
    return "%s#%s" % (capability, r_next)


def add_line(root, name, capability, text, group=None, in_group=None):
    """`work line`: one requirement written into the item `name` and committed (D5); it parses nothing."""
    item = find(root, name)
    ident = add_line_to(root, item, capability, text, group, in_group)
    commit(root, item, "work line: %s %s" % (label(item), ident))
    return item, ident


def add_term(root, name, capability, bullet):
    """`work line --term`: one term bullet written into the item's block for `capability` and committed."""
    item = find(root, name)
    _takes(item)
    capability_file(root, capability)
    bullet = one_line(bullet, "term bullet")
    if spec_lexicon.entry(bullet, capability) is None:
        raise Refused("work line: the term bullet %s is not a term entry `- **<term>** (<category>): <text>`" % bullet)
    blocks = read(item, "the item %s" % item.name)
    _block(blocks, capability).terms.append(bullet)
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s a term of %s" % (label(item), capability))
    return item


def _append(text, heading, body, before="Behaviour"):
    """`text` with `body` added at the end of its `## <heading>` section, the section made before `## <before>` (or at
    the end) when it has none."""
    found = re.search(r"(?ms)^## %s[ \t]*\n(.*?)(?=^## |\Z)" % re.escape(heading), text)
    if found is None:
        made = "## %s\n%s\n\n" % (heading, body)
        at = re.search(r"(?m)^## %s[ \t]*$" % re.escape(before), text)
        return text[:at.start()] + made + text[at.start():] if at else text.rstrip("\n") + "\n\n" + made
    inside = found.group(1).rstrip("\n")
    joined = (inside + "\n\n" if inside.strip() else "") + body + "\n\n"
    return text[:found.start(1)] + joined + text[found.end(1):]


def lay(root, item, into):
    """`spec/` of `root` copied to `into/spec`, and the item's blocks laid over the copy: term bullets at the end of the
    capability file's `## Terms`, groups (headings raised to `### `) at the end of its `## Behaviour`. The names of the
    capabilities laid."""
    blocks = read(item, "the item %s" % item.name)
    shutil.copytree(Path(root) / "spec", Path(into) / "spec", dirs_exist_ok=True)
    for block in blocks:
        path = capability_file(into, block.capability)
        text = path.read_text()
        if block.terms:
            text = _append(text, "Terms", "\n".join(block.terms))
        if block.groups:
            text = _append(text, "Behaviour", "\n\n".join(
                "### [%s] %s" % (g.id, g.title) + "".join("\n- [%s] %s" % r for r in g.requirements)
                for g in block.groups))
        path.write_text(text)
    return [b.capability for b in blocks]
