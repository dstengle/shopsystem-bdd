"""An item's `## Requirements` section (capability readiness): its text read into blocks and written back, byte-stable.

The section holds one `### <capability>` block for each capability the item's pieces go into, in the capability
file's own syntax one heading level down: an optional `language: codified-2` line first, the marker the item switches
the capability's file to (`work line --recodify`, backlog_recodify), an optional `retired: [r<n>, ...]` line next, the live requirements of the
capability the item's lines replace (`work line --retires`, backlog_retires), then optional term bullets, then relation rows (`| from | word | to |
cardinality |`), then `#### [g<n>] <title>` groups of `- [r<n>] <statement>` bullets, one line each, a group's fenced
`given` block after its lines. After the capability blocks, a `### universal` block of `- [U<n>] <statement>`
conditions and a `### index` block of upstream entries (`- bounded-context/<path>: ...`), the pieces of
`spec/universal.md` and of `spec/index.md`'s `## Upstreams` (b43)."""
import re
from collections import namedtuple
from pathlib import Path

import spec_read
from backlog_items import Refused, label

SECTION = "Requirements"
UNIVERSAL, INDEX = "universal", "index"
TAKES = ("idea", "shaped")
Group = namedtuple("Group", "id title requirements given", defaults=((),))
Block = namedtuple("Block", "capability terms groups relations retired language", defaults=((), (), None))

CAP = re.compile(r"^### ([a-z0-9]+(?:-[a-z0-9]+)*)$")
GROUP = re.compile(r"^#### \[(g[1-9]\d*)\] (\S.*)$")
REQ = re.compile(r"^- \[(r[1-9]\d*)\] (\S.*)$")
U = re.compile(r"^- \[(U[1-9]\d*)\] (\S.*)$")
RETIRED = re.compile(r"^retired: \[(r[1-9]\d*(?:, r[1-9]\d*)*)\]$")
LANGUAGE = re.compile(r"^language: (codified-2)$")
FENCE, CLOSE = "```given", "```"


class Blocks(list):
    """The capability blocks, in file order (a list, as callers compare it), with the item's universal conditions
    ((U<n>, statement)) and upstream entries (the bullet's text after `- `) beside them."""

    def __init__(self, blocks=(), universal=(), upstreams=()):
        super().__init__(blocks)
        self.universal, self.upstreams = list(universal), list(upstreams)


class _Reader:
    def __init__(self, rel):
        self.rel, self.blocks, self.mode, self.fence = rel, Blocks(), None, None

    def refuse(self, what):
        raise Refused("%s: %s: %s" % (self.rel, SECTION, what))

    def line(self, line):
        if self.fence is not None:
            return self.given(line)
        if not line.strip():
            return None
        if line in ("### %s" % UNIVERSAL, "### %s" % INDEX):
            if line[4:] == self.mode or (line[4:] == UNIVERSAL and self.mode == INDEX):
                self.refuse("the %s block is there twice, or out of order" % line[4:])
            self.mode = line[4:]
            return None
        if self.mode == UNIVERSAL:
            return self.condition(line)
        if self.mode == INDEX:
            if not line.startswith("- "):
                self.refuse("a line of the index block that is no upstream entry: %s" % line)
            return self.blocks.upstreams.append(line[2:].strip())
        return self.capability_line(line)

    def condition(self, line):
        m = U.match(line)
        if not m:
            self.refuse("a line of the universal block that is no `- [U<n>] <statement>`: %s" % line)
        if any(u == m.group(1) for u, _ in self.blocks.universal):
            self.refuse("the universal condition %s is there twice" % m.group(1))
        self.blocks.universal.append((m.group(1), m.group(2).strip()))

    def given(self, line):
        if line.strip() == CLOSE:
            groups = self.blocks[-1].groups
            groups[-1] = groups[-1]._replace(given=tuple(self.fence))
            self.fence = None
        elif line.strip():
            self.fence.append(line.rstrip())

    def capability_line(self, line):
        blocks = self.blocks
        if (m := CAP.match(line)):
            if any(b.capability == m.group(1) for b in blocks):
                self.refuse("the capability %s has two blocks" % m.group(1))
            blocks.append(Block(m.group(1), [], []))
        elif (m := LANGUAGE.match(line)):
            if not blocks or blocks[-1] != Block(blocks[-1].capability, [], []):
                self.refuse("a `language:` line that is not the first line of a `### <capability>` block: %s" % line)
            blocks[-1] = blocks[-1]._replace(language=m.group(1))
        elif (m := RETIRED.match(line)):
            if not blocks or blocks[-1].terms or blocks[-1].relations or blocks[-1].groups or blocks[-1].retired:
                self.refuse("a `retired:` line that is not the first line of a `### <capability>` block, or after its "
                            "`language:` line: %s" % line)
            blocks[-1] = blocks[-1]._replace(retired=tuple(m.group(1).split(", ")))
        elif (m := GROUP.match(line)):
            if not blocks:
                self.refuse("the group %s comes before any `### <capability>` heading" % m.group(1))
            if any(g.id == m.group(1) for g in blocks[-1].groups):
                self.refuse("the group %s is there twice" % m.group(1))
            blocks[-1].groups.append(Group(m.group(1), m.group(2).strip(), []))
        elif (m := REQ.match(line)):
            if not blocks or not blocks[-1].groups or blocks[-1].groups[-1].given:
                self.refuse("the requirement %s comes before any `#### [g<n>]` heading, or after its given block"
                            % m.group(1))
            if m.group(1) in {r for g in blocks[-1].groups for r, _ in g.requirements}:
                self.refuse("the requirement %s is there twice" % m.group(1))
            blocks[-1].groups[-1].requirements.append((m.group(1), m.group(2).strip()))
        elif line.strip() == FENCE:
            if not blocks or not blocks[-1].groups or blocks[-1].groups[-1].given:
                self.refuse("a given block that is not after the lines of a group of its own")
            self.fence = []
        elif line.startswith(("- **", "|")):
            if not blocks or blocks[-1].groups:
                self.refuse("a term bullet or relation row that is not before the groups of a `### <capability>` "
                            "block: %s" % line)
            if line.startswith("|"):
                blocks[-1] = blocks[-1]._replace(relations=blocks[-1].relations + (line.strip(),))
            elif blocks[-1].relations:
                self.refuse("a term bullet after the relation rows: %s" % line)
            else:
                blocks[-1].terms.append(line.strip())
        else:
            self.refuse("a line that is no heading, requirement, `language:` or `retired:` line, term bullet or relation "
                        "row: %s" % line)


def read(item, rel):
    """The blocks of the item's `## Requirements`, in file order; malformed text is refused, naming the file."""
    reader = _Reader(rel)
    for line in item.sections.get(SECTION, "").split("\n"):
        reader.line(line)
    if reader.fence is not None:
        reader.refuse("a given block is not closed")
    return reader.blocks


def laid_group(group, level="###"):
    """A group's text as in a capability file (`level` its heading): its lines, then its given block."""
    text = "%s [%s] %s" % (level, group.id, group.title) + "".join("\n- [%s] %s" % r for r in group.requirements)
    return text + ("\n\n%s\n%s\n%s" % (FENCE, "\n".join(group.given), CLOSE) if group.given else "")


def render(blocks):
    """The section's text, byte-stable: `read` of it gives `blocks` back."""
    out = []
    for block in blocks:
        parts = ["### %s" % block.capability] + (["language: %s" % block.language] if block.language else [])
        parts += (["retired: [%s]" % ", ".join(block.retired)] if block.retired else [])
        parts += ["\n".join(block.terms)] if block.terms else []
        parts += ["\n".join(block.relations)] if block.relations else []
        out.append("\n\n".join(parts + [laid_group(g, "####") for g in block.groups]))
    if getattr(blocks, "universal", None):
        out.append("### %s\n\n" % UNIVERSAL + "\n".join("- [%s] %s" % u for u in blocks.universal))
    if getattr(blocks, "upstreams", None):
        out.append("### %s\n\n" % INDEX + "\n".join("- %s" % b for b in blocks.upstreams))
    return "\n\n".join(out)


def ids(blocks):
    """`<capability>#r<n>` of each requirement, in file order."""
    return ["%s#%s" % (b.capability, r) for b in blocks for g in b.groups for r, _ in g.requirements]


def capability_file(root, capability):
    """spec/capabilities/<capability>.md of `root`; refused when there is none, or it is not codified (D4)."""
    path = Path(root) / "spec" / "capabilities" / ("%s.md" % capability)
    if "/" in capability or capability in (UNIVERSAL, INDEX) or not spec_read.codified(path):
        raise Refused("there is no codified capability %s in spec/capabilities/" % capability)
    return path


def takes(item, command="work line"):
    """Refused unless the item is idea or shaped, the states whose lines may change."""
    if item.status not in TAKES:
        raise Refused("%s: %s is %s; %s takes an item that is idea or shaped" % (command, label(item), item.status,
                                                                               command))
