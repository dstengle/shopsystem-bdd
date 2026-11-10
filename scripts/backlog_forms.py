"""The spec pieces beside an item's lines (capability readiness r5-r11, b43): a relation row, a given block, a universal
condition and an upstream entry, each written onto the item's `## Requirements` by a flag of `work line` and
committed, checked for its shape when written (its parse waits for `work ready`, as a line's does), and laid into
`spec/` with the item's lines by backlog_lines (`lay_onto`, `unlay`, `renumber`), never straight onto the base.

A relation row goes onto the end of its capability's `## Relations` table (the table made when it has none), a given
block under its group's lines, a universal condition as the next `[U<n>]` of `spec/universal.md` (past its
`retired:`), an upstream entry under `## Upstreams` of `spec/index.md`."""
import re
from pathlib import Path

import backlog_universal
import shop_files
import spec_lexicon
import spec_read
import spec_read_given
from backlog_items import Refused, commit, find, label, one_line
from backlog_section import SECTION, Block, capability_file, read, render, takes

HEADER = ("| from | word | to | cardinality |", "|---|---|---|---|")
UPSTREAM = re.compile(r"^(bounded-context/[\w.-]+(?:/[\w.-]+)+):(?:\s.*)?$")
GITHUB = re.compile(r"\bgithub:\s*(\S*)")
REPO = re.compile(r"[\w.-]+/[\w.-]+")
UNIVERSAL_REL, INDEX_REL = "spec/universal.md", "spec/index.md"


def _blocks(item):
    return read(item, "the item %s" % item.name)


def _refuse(what, text, why):
    raise Refused("work line: the %s %s is malformed: %s" % (what, text, why))


def relation_row(root, blocks, capability, row):
    """The row `| from | word | to | cardinality |` of `row`; refused unless it is four cells whose from and to are
    kinds of the lexicon (or of the item's own term bullets)."""
    row = one_line(row, "relation row")
    cells = [c.strip().strip("`").strip() for c in row.strip("|").split("|")]
    if len(cells) != 4 or not all(cells[:3]):
        _refuse("relation row", row, "it is not four cells `| from | word | to | cardinality |`")
    kinds = spec_lexicon.read(root).kind_names()
    kinds |= {t.term for b in blocks for t in (spec_lexicon.entry(x, b.capability) for x in b.terms)
              if t is not None and t.category == "kind"}
    missing = [k for k in (cells[0], cells[2]) if k not in kinds]
    if missing:
        _refuse("relation row", row, "%s is no kind of the lexicon" % ", ".join(missing))
    return "| %s |" % " | ".join(cells)


def upstream_entry(bullet):
    """The entry `bounded-context/<path>: ...` of `bullet` (a leading `- ` taken off); refused unless it starts with a
    bounded-context id and each `github:` is `<owner>/<name>`."""
    bullet = one_line(bullet, "upstream entry")
    bullet = bullet[2:].strip() if bullet.startswith("- ") else bullet
    if not UPSTREAM.match(bullet):
        _refuse("upstream entry", bullet, "it does not start with a bounded-context id `bounded-context/<path>:`")
    for found in GITHUB.finditer(bullet):
        if not REPO.fullmatch(found.group(1).rstrip(".,;")):
            _refuse("upstream entry", bullet, "its github: %s is not <owner>/<name>" % found.group(1))
    return bullet


def given_block(text):
    """The lines of a given block (its fence, when given, taken off); refused unless every given line is example data
    in the form spec_read_given reads, the data indented two spaces under a line ending in ':'."""
    lines = [x.rstrip() for x in text.replace("\r\n", "\n").split("\n") if x.strip()]
    if lines and lines[0].strip() == "```given":
        lines = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
    shown = lines[0].strip() if lines else ""
    if not lines:
        _refuse("given block", "(empty)", "it has no line")
    steps = []
    for line in lines:
        if line.strip().startswith("```") or line.lstrip().startswith("#") and not line.startswith("  "):
            _refuse("given block", shown, "the line %s would end the block or read as a heading" % line.strip())
        if line.startswith("  "):
            if not steps or not steps[-1][0].endswith(":"):
                _refuse("given block", shown, "the indented line %s is under no line ending in ':'" % line.strip())
            kind = "table" if line.strip().startswith("|") else "docstring"
            if steps[-1][1] not in (None, kind):
                _refuse("given block", shown, "it mixes table rows and text under %s" % steps[-1][0])
            steps[-1][1] = kind
        else:
            steps.append([line.strip(), None])
    for step, data in steps:
        if not spec_read_given.example(step, data and spec_read_given.Block(data, [])):
            _refuse("given block", shown, "%s is not example data (`the <words> <name> holds:` with data under it, "
                    "or `the <words> <name> holds` and one code span or quoted string)" % step)
    return tuple(lines)


def _capability_block(blocks, capability):
    found = next((i for i, b in enumerate(blocks) if b.capability == capability), None)
    if found is None:
        blocks.append(Block(capability, [], []))
        found = len(blocks) - 1
    return found


def add_relation(root, name, capability, row):
    """`work line --relation`: one relation row written into the item's block for `capability` and committed."""
    item = find(root, name)
    takes(item)
    capability_file(root, capability)
    blocks = _blocks(item)
    row = relation_row(root, blocks, capability, row)
    at = _capability_block(blocks, capability)
    blocks[at] = blocks[at]._replace(relations=blocks[at].relations + (row,))
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s a relation row of %s" % (label(item), capability))
    return item


def add_given(root, name, capability, group, text):
    """`work line --given`: the given block of one of the item's own groups in `capability`, written and committed."""
    item = find(root, name)
    takes(item)
    capability_file(root, capability)
    blocks = _blocks(item)
    lines = given_block(text)
    block = next((b for b in blocks if b.capability == capability), None)
    at = next((i for i, g in enumerate(block.groups) if g.id == group), None) if block else None
    if at is None:
        raise Refused("work line: %s has no group %s in %s: a given block goes under one of the item's own groups"
                      % (label(item), group, capability))
    if block.groups[at].given:
        raise Refused("work line: %s: the group %s of %s has a given block already" % (label(item), group, capability))
    block.groups[at] = block.groups[at]._replace(given=lines)
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s a given block of %s#%s" % (label(item), capability, group))
    return item


def universal_ids(root):
    """The U ids of `spec/universal.md` of `root`: its conditions and its `retired:`."""
    found = spec_read.read_universal(root)
    return {u.id for u in found.conditions} | {str(r) for r in found.frontmatter.get("retired") or ()}


def next_universal(used):
    return "U%d" % (max((int(u[1:]) for u in used if re.fullmatch(r"U\d+", u)), default=0) + 1)


def add_universal(root, name, statement, retires=None):
    """`work line --universal`: one universal condition written into the item's `### universal` block, its id the
    next past `spec/universal.md`'s and the item's own, and committed; with `retires` (`universal#U<n>`), the live
    condition it replaces under the block's `retired:` (backlog_universal), refused when it is nonexistent."""
    item = find(root, name)
    takes(item)
    old = backlog_universal.check_retires(root, item, retires) if retires is not None else None
    statement = one_line(statement, "universal condition")
    if statement.startswith("#"):
        raise Refused("work line: %s: the universal condition starts with #, which would read as a heading" %
                      label(item))
    blocks = _blocks(item)
    ident = next_universal(universal_ids(root) | {u for u, _ in blocks.universal})
    blocks.universal.append((ident, statement))
    blocks.universal_retired = tuple(blocks.universal_retired) + ((old,) if old else ())
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s universal#%s%s" % (label(item), ident, " retires %s" % retires if old else ""))
    return item, ident


def upstreams(text):
    """The ids of the upstream entries of an index's text."""
    section = re.search(r"(?ms)^## Upstreams[ \t]*$(.*?)(?=^## |\Z)", text)
    return [m.group(1) for m in (UPSTREAM.match(x[2:]) for x in (section.group(1) if section else "").splitlines()
                                 if x.startswith("- ")) if m]


def add_upstream(root, name, bullet):
    """`work line --upstream`: one upstream entry written into the item's `### index` block and committed; an
    upstream already in `spec/index.md` or on the item is refused."""
    item = find(root, name)
    takes(item)
    bullet = upstream_entry(bullet)
    ident = UPSTREAM.match(bullet).group(1)
    blocks = _blocks(item)
    index = Path(root) / INDEX_REL
    known = upstreams(index.read_text() if index.is_file() else "") + [UPSTREAM.match(b).group(1)
                                                                      for b in blocks.upstreams]
    if ident in known:
        raise Refused("work line: %s: the upstream entry %s: %s is an upstream already" % (label(item), bullet, ident))
    blocks.upstreams.append(bullet)
    item.sections[SECTION] = render(blocks)
    commit(root, item, "work line: %s an upstream entry %s" % (label(item), ident))
    return item


def with_lines(text, heading, lines, made=(), before=None):
    """`text` with `lines` added to its `## <heading>` section: after the last row of its table when `made` (a table's
    header and rule) is given, the table made when it has none, else after its last line; the section made before
    `## <before>` (or at the end) when there is none."""
    found = re.search(r"(?ms)^## %s[ \t]*\n(.*?)(?=^## |\Z)" % re.escape(heading), text)
    if found is None:
        section = "## %s\n\n%s\n\n" % (heading, "\n".join(list(made) + list(lines)))
        at = re.search(r"(?m)^## %s[ \t]*$" % re.escape(before), text) if before else None
        return text[:at.start()] + section + text[at.start():] if at else text.rstrip("\n") + "\n\n" + section
    inside = found.group(1).rstrip("\n").split("\n")
    rows = [i for i, x in enumerate(inside) if x.startswith("|")] if made else []
    if rows:
        inside[rows[-1] + 1:rows[-1] + 1] = list(lines)
    elif not any(x.strip() for x in inside):
        inside = list(made) + list(lines)
    else:
        gap = [] if not made and inside[-1].startswith("- ") else [""]
        inside += gap + list(made) + list(lines)
    return text[:found.start(1)] + "\n".join(inside).strip("\n") + "\n\n" + text[found.end(1):].lstrip("\n")


def without_lines(text, heading, lines, made=()):
    """`text` less each of `lines` once in its `## <heading>` section, the section taken out when nothing but `made`
    is left in it."""
    found = re.search(r"(?ms)^## %s[ \t]*\n(.*?)(?=^## |\Z)" % re.escape(heading), text)
    if found is None:
        return text
    kept = found.group(1).split("\n")
    for line in lines:
        if line in kept:
            kept.remove(line)
    left = [x for x in kept if x.strip()]
    if left == list(made) or not left:
        return (text[:found.start()].rstrip("\n") + "\n\n" + text[found.end():]).rstrip("\n") + "\n"
    return text[:found.start(1)] + "\n".join(kept).strip("\n") + "\n\n" + text[found.end(1):].lstrip("\n")


def _universal_file(into):
    path = Path(into) / UNIVERSAL_REL
    if not path.is_file():
        path.write_text("---\nid: capability/%s/universal\ntitle: Universal conditions\ngroup: guarantees\nlanguage: "
                        "codified-1\nretired: []\n---\n\n# Universal conditions\n\n## Behaviour\n"
                        % shop_files.context_path(into))
    return path


def lay_spec(into, blocks, files):
    """The item's universal conditions and upstream entries laid into `into/spec`; each path changed added to
    `files`."""
    if blocks.universal:
        path = _universal_file(into)
        path.write_text(with_lines(path.read_text(), "Behaviour", ["- [%s] %s" % u for u in blocks.universal]))
        files.append(UNIVERSAL_REL)
    if blocks.upstreams:
        path = Path(into) / INDEX_REL
        path.write_text(with_lines(path.read_text(), "Upstreams", ["- %s" % b for b in blocks.upstreams]))
        files.append(INDEX_REL)


def unlay_spec(into, blocks, files):
    """The reverse of `lay_spec`; each path changed added to `files`."""
    universal, index = Path(into) / UNIVERSAL_REL, Path(into) / INDEX_REL
    if blocks.universal and universal.is_file():
        text = universal.read_text()
        for line in ["- [%s] %s" % u for u in blocks.universal]:
            found = re.search(r"(?m)^%s\n?" % re.escape(line), text)
            text = text if found is None else text[:found.start()] + text[found.end():]
        if text != universal.read_text():
            universal.write_text(text)
            files.append(UNIVERSAL_REL)
    if blocks.upstreams and index.is_file():
        text = without_lines(index.read_text(), "Upstreams", ["- %s" % b for b in blocks.upstreams])
        if text != index.read_text():
            index.write_text(text)
            files.append(INDEX_REL)
