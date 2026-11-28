"""`work line --retires` (capability readiness, b128): a new line that replaces a live requirement of a codified
capability (design-decision/requirements-retired-never-edited). The new line takes the next id of its capability as
`work line` gives it, and the old id is written under the item's capability block's `retired:`, the pair of the two
under its `retires:` (backlog_section, b323).

Laid over a spec (`lay`), the old line is taken out of the capability's `## Behaviour`, with its group when it was the
group's last line, and its id (and the group's) put into the capability's `retired:`; a removed group's `Restates:` id
that no group left restates is written under the capability's `## Dropped` as `r<n>@0.29: retired with <cap>#r<m> by
b<k>.` (b333). A line goes with its continuation lines and its `Relied on by:` line (b761)."""
import re

import spec_read
from backlog_items import Refused, label
from backlog_section import SECTION, capability_file, read, render, takes

IDENT = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)#(r[1-9]\d*)$")
GROUP = r"(?ms)^### \[(g[1-9]\d*)\] [^\n]*\n.*?(?=^### |^## |\Z)"
LINE = r"^- \[%s\] .*(?:\n  .*)*(?:\nRelied on by:.*)?(?:\n|\Z)"        # a line, continued, with its support


def _line(rid):
    """A requirement line `- [r<n>] ...` with its continuation lines, its `Relied on by:` line (b761), and the line
    break after it."""
    return "(?m)" + LINE % re.escape(rid)


def check(root, item, ident, into=None, line=False):
    """The capability and r<n> of `<cap>#r<n>`, the live requirement `work line --retires` retires on the item;
    refused when the capability holds no live requirement of that id, or the item retires it already, or `into`
    names another capability than its own when there is no `line`, or one the spec has no file of (b882)."""
    takes(item)
    found = IDENT.match(ident or "")
    if not found:
        raise Refused("work line: --retires takes `<capability>#r<n>`, not %s" % ident)
    capability, rid = found.groups()
    if into is not None and into != capability and not (line and _codified(root, into)):
        raise Refused("work line: --retires %s goes into %s%s, not --into %s" % (
            ident, capability, " or another capability of the spec" if line else "", into))
    try:
        cap = spec_read.capability(capability_file(root, capability))
    except Refused as err:
        raise Refused("work line: %s is nonexistent: %s" % (ident, err)) from None
    if rid not in {r.id for g in cap.groups for r in g.requirements} or rid in cap.retired:
        raise Refused("work line: %s is nonexistent: %s holds no live requirement %s" % (ident, capability, rid))
    if any(b.capability == capability and rid in b.retired for b in read(item, "the item %s" % item.name)):
        raise Refused("work line: %s retires %s already" % (label(item), ident))
    return capability, rid


def _codified(root, capability):
    """Whether the spec has a codified file of `capability`, one a line `--into` it may retire another's from."""
    try:
        path = capability_file(root, capability)
    except Refused:
        return False
    return path.is_file() and str(spec_read.capability(path).frontmatter.get("language", "")).strip() == "codified-2"


def with_retired(item, capability, rid, line=None):
    """The item's block for `capability` given `rid` under its `retired:`, and the pair (`line`, `rid`) under its
    `retires:` when the item's line `line` retires it (b323), `line` an `r<n>` of the block's own capability or a
    `<cap>#r<n>` of another's (b882); nothing is committed. The block is there already."""
    blocks = read(item, "the item %s" % item.name)
    at = next(k for k, b in enumerate(blocks) if b.capability == capability)
    pairs = tuple(blocks[at].retires) + (((line, rid),) if line else ())
    blocks[at] = blocks[at]._replace(retired=tuple(blocks[at].retired) + (rid,), retires=pairs)
    item.sections[SECTION] = render(blocks)


def ident_of(capability, line):
    """The `<cap>#r<n>` of a `retires:` pair's line in the block of `capability`: `r<n>` its own, else as written."""
    return line if "#" in line else "%s#%s" % (capability, line)


def retiring(blocks):
    """{the item's line `<cap>#r<n>`: the `<cap>#r<m>` it retires} of the `retires:` pairs of `blocks` (b882)."""
    return {ident_of(b.capability, line): "%s#%s" % (b.capability, old) for b in blocks for line, old in b.retires}


def _listed(text, ids):
    """A capability file's text with `ids` added to its frontmatter's `retired: [...]`."""
    head_end = text.find("\n---", 4)
    found = re.search(r"(?m)^retired:[ \t]*\[(.*)\][ \t]*$", text[:head_end])
    had = [one.strip() for one in found.group(1).split(",") if one.strip()] if found else []
    kept = list(dict.fromkeys(had + list(ids)))
    listed = "retired: [%s]" % ", ".join(kept)
    if found:
        return text[:found.start()] + listed + text[found.end():]
    return text[:head_end] + "\n" + listed + text[head_end:]


def _group_of(text, rid):
    """The group chunk of `text` holding the requirement `rid`, as a match, or None."""
    return next((g for g in re.finditer(GROUP, text) if re.search(_line(rid), g.group(0))), None)


def lay(text, capability, rids, item=None):
    """The capability file's text with each of `rids` out of its Behaviour and in its `retired:`, the group too when
    the line was its last, each `Restates:` id of the group no other group restates then dropped by `item` (b333);
    refused when a line is not there as a live requirement."""
    gone = []
    for rid in rids:
        chunk = _group_of(text, rid)
        if chunk is None:
            raise Refused("%s#%s is nonexistent: %s holds no live requirement %s" % (capability, rid, capability, rid))
        rest = re.sub(_line(rid), "", chunk.group(0), count=1)
        if re.search(r"(?m)^- \[r[1-9]\d*\] ", rest):
            text = text[:chunk.start()] + rest + text[chunk.end():]
            gone.append(rid)
        else:
            text = text[:chunk.start()] + text[chunk.end():]
            gone += [chunk.group(1), rid]
            text = _dropped(text, capability, rid, item, _restates(chunk.group(0)))
    return _listed(text, gone)


def _restates(chunk):
    """The `Restates:` tokens of a group's text, as written (`r<n>@0.29` or `<cap>#r<n>@0.29`)."""
    return [token.strip() for line in re.findall(r"(?m)^Restates:(.*)$", chunk)
            for token in line.strip().rstrip(".").split(",") if token.strip()]


def _dropped(text, capability, rid, item, tokens):
    """`text` with a `## Dropped` entry for each of `tokens` that no group of it restates any more (b333)."""
    held = set(_restates("\n".join(g.group(0) for g in re.finditer(GROUP, text))))
    entries = ["- %s: retired with %s#%s by %s." % (token, capability, rid, item or "an item")
               for token in tokens if token not in held]
    if not entries:
        return text
    section = re.search(r"(?ms)^## Dropped[ \t]*\n(.*?)(?=^## |\Z)", text)
    if section is None:
        return text.rstrip("\n") + "\n\n## Dropped\n" + "\n".join(entries) + "\n"
    inside = section.group(1).rstrip("\n")
    joined = (inside + "\n" if inside.strip() else "") + "\n".join(entries) + "\n"
    return text[:section.start(1)] + joined + ("\n" if section.end(1) < len(text) else "") + text[section.end(1):]
