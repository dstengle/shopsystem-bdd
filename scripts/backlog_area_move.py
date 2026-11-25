"""A model element or a term an item moves to another area (b607, drafting r66-r69, batches r117, r118).

The item keeps its moves in a `### moves` block of its `## Requirements` (backlog_section reads and writes it, after
the pack blocks), one bullet a move: `- model line `<element header>` from <area> to <area>` and `- term `<word> →
<element>` from <layer> to <area>`. `work line <item> --into <capability> --move-model "<element header>"` moves the
element the domain model declares in another area (with its members and the vocabulary entries that mean it) to the
area of the capability (backlog_model_area's `area_of`), refused naming the model line when no model file declares
it; `work line <item> --move-term "<word>"` (or `"<word> → <element>"`) moves the entry out of its layer, shared.md
among them, into the layer of the area that declares its element (the area a move of the item takes it to, else its
own), refused naming the term when no layer holds it. backlog_area_move_lay lays the moves and takes them out again."""
import re
from collections import namedtuple
from pathlib import Path

from backlog_items import Refused, commit, find, label, one_line

HEAD = "### moves"
LINE = re.compile(r"^- (model line|term) `(.+)` from ([a-z0-9]+(?:-[a-z0-9]+)*) to ([a-z0-9]+(?:-[a-z0-9]+)*)$")
Move = namedtuple("Move", "kind what source target")
FLAGS = ("move_model", "move_term")


def add_arguments(p):
    """`work line`'s options that move a model element or a term to another area."""
    p.add_argument("--move-model", metavar="HEADER", help="with --into: an element header the domain model declares "
                   "in another area (`object tag`), the element moved with its members and vocabulary entries into "
                   "the area of the capability --into names")
    p.add_argument("--move-term", metavar="TERM", help="a vocabulary entry (its word, or `<word> → <element>`) moved "
                   "out of its layer into the layer of the area that declares its element")


def given(args):
    """True when the run is one of this module's."""
    return any(getattr(args, k, None) is not None for k in FLAGS)


class Lines:
    """The lines of the item's `### moves` block, read one at a time by backlog_section's reader."""

    def __init__(self, moves, refuse):
        self.moves, self.refuse = moves, refuse

    def line(self, line):
        if line == HEAD or not line.strip():
            return
        found = LINE.match(line.strip())
        if not found:
            self.refuse("a line of the moves block that is no `- model line `<header>` from <area> to <area>` or "
                        "`- term `<word> → <element>` from <layer> to <area>`: %s" % line)
        move = Move(*found.groups())
        if any(m[:2] == move[:2] for m in self.moves):
            self.refuse("the move of the %s %s is there twice" % move[:2])
        self.moves.append(move)


def render(moves):
    return HEAD + "\n\n" + "\n".join("- %s `%s` from %s to %s" % m for m in moves) if moves else ""


def declaring(root, header):
    """(area, the header as its model file writes it) of the model file that declares the element `header`, or
    None."""
    from backlog_model import _at, _fence
    for path in sorted((Path(root) / "spec" / "model").glob("*.md")):
        lines, start, end = _fence(path.read_text(), path.name)
        at = _at(lines[start:end], header)
        if at is not None:
            return path.stem, lines[start + at]
    return None


def _entry(root, term):
    """The vocabulary entry `term` names (its word, or `<word> → <element>`); refused, naming the term, when no layer
    holds one or two do."""
    import spec_vocabulary
    word, _, ref = (x.strip() for x in term.partition("→"))
    found = [e for e in spec_vocabulary.entries(root) if e.term == word and (not ref or " ".join(e.ref.split()) ==
                                                                               " ".join(ref.split()))]
    if not found:
        raise Refused("work line: no area holds the term %s" % term, reason="term not in the vocabulary",
                      names=["term:%s" % term])
    if len(found) > 1:
        raise Refused("work line: %d entries are the term %s; name one by `<word> → <element>`: %s" % (
            len(found), term, "; ".join("%s → %s (%s)" % (e.term, e.ref, e.layer) for e in found)))
    return found[0]


def means(header, ref):
    """Whether the entry naming `ref` means the element `header` declares or one of its members."""
    kind, _, name = " ".join(header.split()).partition(" ")
    name = re.sub(r" kind of .*$", "", name).split(":")[0].strip()
    rkind, _, rid = " ".join(ref.split()).partition(" ")
    if kind == "object":
        return (rkind, rid) == ("object", name) or rkind in ("attribute", "value", "relation", "lifecycle") and \
            rid.startswith(name + ".")
    if kind == "service":
        return (rkind, rid) == ("service", name) or rkind == "operation" and rid.startswith(name + ".")
    return (rkind, rid) == (kind, name)


def move_model(root, name, header, into):
    """`--move-model`: the move of the element `header` to the area of `into`, kept in the item and committed."""
    from backlog_model import area_of
    item, blocks = _opened(root, name)
    header = one_line(header, "model line").strip()
    found = declaring(root, header)
    if found is None:
        raise Refused("work line: the domain model holds no model line %s" % header,
                      reason="model line not in the domain model", names=["model line:%s" % header])
    area = area_of(root, into, blocks)
    if found[0] == area:
        raise Refused("work line: the model line %s is in the area %s already" % (header, area))
    return _kept(root, item, blocks, Move("model line", found[1], found[0], area))


def move_term(root, name, term):
    """`--move-term`: the move of the entry `term` into the layer of the area its element is declared in (or that a
    move of the item takes it to), kept in the item and committed."""
    item, blocks = _opened(root, name)
    term = one_line(term, "term").strip()
    entry = _entry(root, term)
    target = next((m.target for m in blocks.moves if m.kind == "model line" and means(m.what, entry.ref)), None)
    target = target or (entry.element.area if entry.element is not None else None)
    if target is None:
        raise Refused("work line: the term %s means no element the domain model declares" % term)
    if target == entry.layer:
        raise Refused("work line: the term %s is in the layer of %s already" % (term, target))
    return _kept(root, item, blocks, Move("term", "%s → %s" % (entry.term, " ".join(entry.ref.split())),
                                          entry.layer, target))


def _opened(root, name):
    from backlog_section import read, takes
    item = find(root, name)
    takes(item)
    return item, read(item, "the item %s" % item.name)


def _kept(root, item, blocks, move):
    from backlog_section import SECTION
    from backlog_section import render as rendered
    if any(m[:2] == move[:2] for m in blocks.moves):
        raise Refused("work line: %s moves the %s %s already" % (label(item), move.kind, move.what))
    blocks.moves.append(move)
    item.sections[SECTION] = rendered(blocks)
    commit(root, item, "work line: %s moves the %s %s to %s" % (label(item), move.kind, move.what, move.target))
    return item, move


def cmd(args):
    """`work line` with `--move-model` (and `--into`) or `--move-term`, alone; what was done, printed."""
    from backlog_cli import PIECES
    flags = [k for k in FLAGS if getattr(args, k, None) is not None]
    others = [k for k in PIECES + ("retires", "reword", "remove", "group", "in_group")
              if getattr(args, k, None) is not None]
    if len(flags) != 1 or others or (flags[0] == "move_model") != (args.into is not None):
        raise Refused("work line: --move-model takes --into and --move-term none, each alone")
    if flags[0] == "move_model":
        item, move = move_model(args.root, args.name, args.move_model, args.into)
    else:
        item, move = move_term(args.root, args.name, args.move_term)
    print("%s: %s %s moves from %s to %s" % (label(item), move.kind, move.what, move.source, move.target))
    return 0
