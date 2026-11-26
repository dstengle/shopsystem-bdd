"""An item's `## Requirements` section (capability readiness): its text read into blocks and written back, byte-stable.

The section holds one `### <capability>` block for each capability the item's pieces go into, in the capability
file's own syntax one heading level down: an optional `language: codified-2` line first, the marker the item switches
the capability's file to (`work line --recodify`, backlog_recodify), an optional `retired: [r<n>, ...]` line next, the live requirements of the
capability the item's lines replace (`work line --retires`, backlog_retires), then an optional `retires: [r<n> r<m>, ...]`
line, which of the item's lines retires which of those ids (b323; an id `--no-line` retired is in no pair), then an
optional `serves: [g<n> <job>, ...]` line, the jobs the item dedicates groups of the capability to (b641), then optional term bullets, then relation rows (`| from | word | to |
cardinality |`), then `#### [g<n>] <title>` groups of `- [r<n>] <statement>` bullets, one line each, a group's fenced
`given` block after its lines. After the capability blocks, a `### universal` block of `- [U<n>] <statement>`
conditions (after an optional `language: codified-2` line and an optional `retired: [U<n>, ...]` line, spec/universal.md
switched and the conditions the item's replace: backlog_universal) and a `### index` block of upstream entries (`- bounded-context/<path>: ...`), the pieces of
`spec/universal.md` and of `spec/index.md`'s `## Upstreams` (b43). Between the capability blocks and the universal
block, in a context with a domain model, a `### <area> model` block for each area the item adds to: a ` ```model `
fence of model lines, then vocabulary entries (backlog_model, the domain contract), then a `### <port> adapter` block
of withheld operations and operation tables (backlog_adapter, b355), then a `### <name> pack` block of term entries
of a context's own pack (backlog_pack, b472), then a `### moves` block (backlog_area_move, b607), an `### imports`
block (backlog_import, b672) and a `### retirements` block (backlog_retire, b672)."""
import re
from collections import namedtuple
from pathlib import Path

import backlog_adapter
import backlog_pack
import backlog_relied
import spec_read
from backlog_items import Refused, label
from backlog_model import CLOSE as MODEL_CLOSE
from backlog_model import FENCE as MODEL_FENCE
from backlog_model import HEAD as MODEL_HEAD
from backlog_model import ModelBlock
from backlog_section_render import (  # noqa: F401
    CLOSE,
    FENCE,
    INDEX,
    LISTS,
    NEW_FIELDS,
    REQUIRED,
    UNIVERSAL,
    ids,
    laid_group,
    render,
)

SECTION = "Requirements"
TAKES = ("idea", "shaped", "in-batch")     # an in-batch item's lines are laid again by `work batch amend` (b460)
Group = namedtuple("Group", "id title requirements given relied", defaults=((), ()))   # relied: (r<n>, ids) (b705)
Block = namedtuple("Block", "capability terms groups relations retired language new retires serves",
                   defaults=((), (), None, None, (), ()))     # serves: (g<n>, job) pairs (backlog_serves, b641)

CAP = re.compile(r"^### ([a-z0-9]+(?:-[a-z0-9]+)*)$")
GROUP = re.compile(r"^#### \[(g[1-9]\d*)\] (\S.*)$")
REQ = re.compile(r"^- \[(r[1-9]\d*)\] (\S.*)$")
U = re.compile(r"^- \[(U[1-9]\d*)\] (\S.*)$")
RETIRED = re.compile(r"^retired: \[(r[1-9]\d*(?:, r[1-9]\d*)*)\]$")
RETIRES = re.compile(r"^retires: \[(r[1-9]\d* r[1-9]\d*(?:, r[1-9]\d* r[1-9]\d*)*)\]$")
U_RETIRED = re.compile(r"^retired: \[(U[1-9]\d*(?:, U[1-9]\d*)*)\]$")
SERVES = re.compile(r"^serves: \[(g[1-9]\d* \S+(?:, g[1-9]\d* \S+)*)\]$")
LANGUAGE = re.compile(r"^language: (codified-2)$")
NEW = re.compile(r"^(%s): (\S.*)$" % "|".join(NEW_FIELDS))
LISTED = tuple(name for name, _ in LISTS)
HEADS = {module.HEAD: name for name, module in LISTS}


class Blocks(list):
    """The capability blocks, in file order (a list, as callers compare it), with the item's universal conditions
    ((U<n>, statement)) and upstream entries (the bullet's text after `- `) beside them, and the universal block's
    marker (`universal_language`) and the U ids its conditions replace (`universal_retired`)."""

    def __init__(self, blocks=(), universal=(), upstreams=(), universal_language=None, universal_retired=(),
                 models=(), adapters=(), packs=(), moves=(), imports=(), retirements=()):
        super().__init__(blocks)
        self.universal, self.upstreams, self.models = list(universal), list(upstreams), list(models)
        self.adapters, self.packs, self.moves = list(adapters), list(packs), list(moves)
        self.imports, self.retirements = list(imports), list(retirements)
        self.universal_language, self.universal_retired = universal_language, tuple(universal_retired)


class _Reader:
    def __init__(self, rel):
        self.rel, self.blocks, self.mode, self.fence, self.mfence = rel, Blocks(), None, None, None
        self.adapter = backlog_adapter.Lines(self.blocks.adapters, self.refuse)
        self.pack = backlog_pack.Lines(self.blocks.packs, self.refuse)
        self.lists = {name: module.Lines(getattr(self.blocks, name), self.refuse) for name, module in LISTS}

    def refuse(self, what):
        raise Refused("%s: %s: %s" % (self.rel, SECTION, what))

    def line(self, line):
        if self.fence is not None:
            return self.given(line)
        if self.mfence is not None:
            return self.model_fence(line)
        if self.adapter.fence is not None:
            return self.adapter.line(line)
        if not line.strip():
            return None
        if line in HEADS or (self.mode in LISTED and not line.startswith("### ")):
            if line in HEADS:
                if self.mode in (UNIVERSAL, INDEX) or self.mode in LISTED[LISTED.index(HEADS[line]):]:
                    self.refuse("the %s block is there twice, out of order, or after the universal or index block"
                                % HEADS[line])
                self.mode = HEADS[line]
            return self.lists[self.mode].line(line)
        if (m := backlog_pack.HEAD.match(line)) or (self.mode == "pack" and not line.startswith("### ")):
            if m and self.mode in (UNIVERSAL, INDEX, *LISTED):
                self.refuse("the pack block of %s is after the universal or index block" % m.group(1))
            self.mode = "pack"
            return self.pack.head(m.group(1)) if m else self.pack.line(line)
        if (m := backlog_adapter.HEAD.match(line)):
            if self.mode in (UNIVERSAL, INDEX, "pack", *LISTED):
                self.refuse("the adapter block of %s is after the universal or index block" % m.group(1))
            self.mode = "adapter"
            return self.adapter.head(m.group(1))
        if self.mode == "adapter" and not line.startswith("### "):
            return self.adapter.line(line)
        if (m := MODEL_HEAD.match(line)):
            if self.mode in (UNIVERSAL, INDEX, "adapter", "pack", *LISTED) or any(b.area == m.group(1) for b in self.blocks.models):
                self.refuse("the model block of %s is there twice, or after the universal or index block" % m.group(1))
            self.mode = "model"
            return self.blocks.models.append(ModelBlock(m.group(1)))
        if self.mode == "model" and not line.startswith("### "):
            return self.model_line(line)
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
        blocks = self.blocks
        if (m := LANGUAGE.match(line)):
            if blocks.universal_language or blocks.universal_retired or blocks.universal:
                self.refuse("a `language:` line that is not the first line of the universal block: %s" % line)
            blocks.universal_language = m.group(1)
            return
        if (m := U_RETIRED.match(line)):
            if blocks.universal_retired or blocks.universal:
                self.refuse("a `retired:` line of the universal block after its conditions: %s" % line)
            blocks.universal_retired = tuple(m.group(1).split(", "))
            return
        m = U.match(line)
        if not m:
            self.refuse("a line of the universal block that is no `- [U<n>] <statement>`: %s" % line)
        if any(u == m.group(1) for u, _ in self.blocks.universal):
            self.refuse("the universal condition %s is there twice" % m.group(1))
        self.blocks.universal.append((m.group(1), m.group(2).strip()))

    def model_line(self, line):
        block = self.blocks.models[-1]
        if line.strip() == MODEL_FENCE and not block.lines and not block.terms:
            self.mfence = []
        elif line.startswith("- **"):
            self.blocks.models[-1] = block._replace(terms=block.terms + (line.strip(),))
        else:
            self.refuse("a line of a model block that is no ```model fence first or vocabulary entry: %s" % line)

    def model_fence(self, line):
        if line.strip() == MODEL_CLOSE:
            self.blocks.models[-1] = self.blocks.models[-1]._replace(lines=tuple(self.mfence))
            self.mfence = None
        else:
            self.mfence.append(line.rstrip())

    def given(self, line):
        if line.strip() == CLOSE:        # a docstring's blank lines kept, the fence's first and last not (b476)
            groups = self.blocks[-1].groups
            text = "\n".join(self.fence).strip("\n")
            groups[-1] = groups[-1]._replace(given=tuple(text.split("\n")) if text else ())
            self.fence = None
        else:
            self.fence.append(line.rstrip())

    def new(self, m):
        """`narrator:`, `group:` and `purpose:`, then `area:` when the person named one (b645) and `kind:` when that
        area is a driven port (b701), in that order, first in the block of a capability the item makes."""
        blocks = self.blocks
        have = (blocks[-1].new or ()) if blocks else ()
        if not blocks or blocks[-1]._replace(new=None) != Block(blocks[-1].capability, [], []) \
                or len(have) == len(NEW_FIELDS) \
                or NEW_FIELDS[len(have)] != m.group(1):
            self.refuse("a `%s:` line that is not in the order %s first in a `### <capability>` block: %s"
                        % (m.group(1), ", ".join(NEW_FIELDS), m.group(0)))
        blocks[-1] = blocks[-1]._replace(new=have + (m.group(2).strip(),))

    def capability_line(self, line):
        blocks = self.blocks
        if (m := CAP.match(line)):
            if any(b.capability == m.group(1) for b in blocks) or self.mode in ("model", "adapter", "pack", *LISTED):
                self.refuse("the capability %s has two blocks, or comes after a model block" % m.group(1))
            blocks.append(Block(m.group(1), [], []))
        elif (m := LANGUAGE.match(line)):
            if not blocks or blocks[-1] != Block(blocks[-1].capability, [], []):
                self.refuse("a `language:` line that is not the first line of a `### <capability>` block: %s" % line)
            blocks[-1] = blocks[-1]._replace(language=m.group(1))
        elif (m := NEW.match(line)):
            self.new(m)
        elif (m := RETIRED.match(line)):
            if not blocks or blocks[-1].terms or blocks[-1].relations or blocks[-1].groups or blocks[-1].retired:
                self.refuse("a `retired:` line that is not the first line of a `### <capability>` block, or after its "
                            "`language:` line: %s" % line)
            blocks[-1] = blocks[-1]._replace(retired=tuple(m.group(1).split(", ")))
        elif (m := RETIRES.match(line)):
            if not blocks or not blocks[-1].retired or blocks[-1].retires or blocks[-1].terms or blocks[-1].relations \
                    or blocks[-1].groups:
                self.refuse("a `retires:` line that is not right after a `retired:` line: %s" % line)
            blocks[-1] = blocks[-1]._replace(retires=tuple(tuple(p.split(" ")) for p in m.group(1).split(", ")))
        elif (m := SERVES.match(line)):
            if not blocks or blocks[-1].terms or blocks[-1].relations or blocks[-1].groups or blocks[-1].serves:
                self.refuse("a `serves:` line that is not before the terms, relation rows and groups of a "
                            "`### <capability>` block: %s" % line)
            blocks[-1] = blocks[-1]._replace(serves=tuple(tuple(p.split(" ")) for p in m.group(1).split(", ")))
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
        elif line.startswith(backlog_relied.HEAD):
            if not blocks or not blocks[-1].groups or not blocks[-1].groups[-1].requirements \
                    or blocks[-1].groups[-1].given:
                self.refuse("a `Relied on by:` line that is not after a requirement of a group: %s" % line)
            group = blocks[-1].groups[-1]
            blocks[-1].groups[-1] = backlog_relied.supported_by(group, line)
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
            self.refuse("a line that is no heading, requirement, `Relied on by:`, `language:`, `retired:` or `retires:` line, term "
                        "bullet or relation row: %s" % line)


def read(item, rel):
    """The blocks of the item's `## Requirements`, in file order; malformed text is refused, naming the file."""
    reader = _Reader(rel)
    for line in item.sections.get(SECTION, "").split("\n"):
        reader.line(line)
    if reader.fence is not None or reader.mfence is not None or reader.adapter.fence is not None:
        reader.refuse("a given block or a model block is not closed")
    if any(b.new and len(b.new) < REQUIRED for b in reader.blocks):
        reader.refuse("a new capability's block without each of %s" % ", ".join(NEW_FIELDS[:REQUIRED]))
    return reader.blocks


def capability_file(root, capability):
    """spec/capabilities/<capability>.md of `root`; refused when there is none, or it is not codified (D4), naming
    the item that holds it as a new capability and its batch, when one does (b450)."""
    path = Path(root) / "spec" / "capabilities" / ("%s.md" % capability)
    if "/" in capability or capability in (UNIVERSAL, INDEX) or not spec_read.codified(path):
        new = "" if path.exists() else "; a new one is given to an item with `shop work line <item> --capability %s`" % (
            capability)
        holders = [] if path.exists() else __import__("backlog_retract").holders(root, capability)
        if holders:
            new = "; it is new on %s, and its lines go into that item" % ", ".join(holders)
        raise Refused("there is no codified capability %s in spec/capabilities/%s" % (capability, new))
    return path


def takes(item, command="work line", states=TAKES):
    """Refused unless the item is in one of `states` (idea, shaped or in-batch, the states whose lines may change)."""
    if item.status not in states:
        raise Refused("%s: %s is %s; %s takes an item that is %s" % (
            command, label(item), item.status, command, " or ".join((", ".join(states[:-1]), states[-1]))))
