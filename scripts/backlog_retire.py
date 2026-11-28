"""A model element or a term an item retires (b672, drafting r75-r78, batches r133, r134).

The item keeps its retirements in a `### retirements` block of its `## Requirements` (backlog_section reads and writes
it, after the imports block), one bullet a retirement: `- model line `<element header>` in <area>` and `- term `<word>
→ <element>` in <layer>`. `work line <item> --into <capability> --retire-model "<element header>"` retires the element
the model file of the capability's area declares (backlog_model_area's `area_of`), refused naming the model line when
that file does not declare it; `work line <item> --retire-term "<word>"` (or `"<word> → <element>"`) retires the
entry of a layer, shared.md among them, refused naming the term when no layer holds it (backlog_area_move's
`_entry`); `work line <item> --retire-area <area>` (`- area `<area>``) retires an area that holds nothing
(backlog_retire_area). backlog_retire_lay lays the retirements and takes them out again."""
import re
from collections import namedtuple

from backlog_items import Refused, commit, find, label, one_line

HEAD = "### retirements"
LINE = re.compile(r"^- (model line|term) `(.+)` in ([a-z0-9]+(?:-[a-z0-9]+)*)$")
AREA = re.compile(r"^- area `([a-z0-9]+(?:-[a-z0-9]+)*)`$")
Retirement = namedtuple("Retirement", "kind what area")
FLAGS = ("retire_model", "retire_term", "retire_area")


def add_arguments(p):
    """`work line`'s options that retire a model element or a term."""
    p.add_argument("--retire-model", metavar="HEADER", help="with --into: an element header the model of the area "
                   "of the capability --into names declares (`object tag`), taken out of it with its members and the "
                   "vocabulary entries that mean it once the item is laid")
    p.add_argument("--retire-term", metavar="TERM", help="a vocabulary entry (its word, or `<word> → <element>`) "
                   "taken out of its layer once the item is laid")
    p.add_argument("--retire-area", metavar="AREA", help="an area of the domain model that holds no model line, no "
                   "term and no capability with a requirement, taken out with its model file and its layer once the "
                   "item is laid")


def given(args):
    """True when the run is one of this module's."""
    return any(getattr(args, k, None) is not None for k in FLAGS)


class Lines:
    """The lines of the item's `### retirements` block, read one at a time by backlog_section's reader."""

    def __init__(self, retirements, refuse):
        self.retirements, self.refuse = retirements, refuse

    def line(self, line):
        if line == HEAD or not line.strip():
            return
        found, area = LINE.match(line.strip()), AREA.match(line.strip())
        if not found and not area:
            self.refuse("a line of the retirements block that is no `- model line `<header>` in <area>`, "
                        "`- term `<word> → <element>` in <layer>` or `- area `<area>``: %s" % line)
        retirement = Retirement(*found.groups()) if found else Retirement("area", area.group(1), area.group(1))
        if any(r[:2] == retirement[:2] for r in self.retirements):
            self.refuse("the retirement of the %s %s is there twice" % retirement[:2])
        self.retirements.append(retirement)


def render(retirements):
    return HEAD + "\n\n" + "\n".join(_line(r) for r in retirements) if retirements else ""


def _line(retirement):
    return "- area `%s`" % retirement.what if retirement.kind == "area" else "- %s `%s` in %s" % retirement


def retire_model(root, name, header, into):
    """`--retire-model`: the retirement of the element `header` of the area of `into`, kept in the item."""
    from backlog_model import _at, _fence, area_of, model_path
    item, blocks = _opened(root, name)
    header = one_line(header, "model line").strip()
    area = area_of(root, into, blocks)
    path = model_path(root, area)
    found = None
    if path.is_file():
        lines, start, end = _fence(path.read_text(), path.name)
        at = _at(lines[start:end], header)
        found = lines[start + at] if at is not None else None
    if found is None:
        raise Refused("work line: the domain model holds no model line %s in the area %s" % (header, area),
                      reason="model line not in the domain model", names=["model line:%s" % header])
    return _kept(root, item, blocks, Retirement("model line", found, area))


def retire_term(root, name, term):
    """`--retire-term`: the retirement of the entry `term` of its layer, kept in the item."""
    from backlog_area_move import _entry
    item, blocks = _opened(root, name)
    entry = _entry(root, one_line(term, "term").strip())
    return _kept(root, item, blocks, Retirement("term", "%s → %s" % (entry.term, " ".join(entry.ref.split())),
                                                entry.layer))


def _opened(root, name):
    from backlog_section import read, takes
    item = find(root, name)
    takes(item)
    return item, read(item, "the item %s" % item.name)


def _kept(root, item, blocks, retirement):
    from backlog_section import SECTION
    from backlog_section import render as rendered
    if any(r[:2] == retirement[:2] for r in blocks.retirements):
        raise Refused("work line: %s retires the %s %s already" % (label(item), retirement.kind, retirement.what))
    blocks.retirements.append(retirement)
    item.sections[SECTION] = rendered(blocks)
    commit(root, item, "work line: %s retires the %s %s" % (label(item), retirement.kind, retirement.what))
    return item, retirement


def cmd(args):
    """`work line` with `--retire-model` (and `--into`) or `--retire-term`, alone; what was done, printed."""
    from backlog_cli import PIECES
    flags = [k for k in FLAGS if getattr(args, k, None) is not None]
    others = [k for k in PIECES + ("retires", "reword", "remove", "group", "in_group")
              if getattr(args, k, None) is not None]
    if len(flags) != 1 or others or (flags[0] == "retire_model") != (args.into is not None):
        raise Refused("work line: --retire-model takes --into and --retire-term or --retire-area none, each alone")
    if flags[0] == "retire_area":
        item, retirement = __import__("backlog_retire_area").retire_area(args.root, args.name, args.retire_area)
        print("%s: retires the area %s" % (label(item), retirement.what))
        return 0
    if flags[0] == "retire_model":
        item, retirement = retire_model(args.root, args.name, args.retire_model, args.into)
    else:
        item, retirement = retire_term(args.root, args.name, args.retire_term)
    print("%s: retires the %s %s in %s" % (label(item), *retirement))
    return 0
