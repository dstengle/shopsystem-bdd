"""An item's requirement lines (capability readiness; workflow simplification plan 3, D2-D5): the item file's
`## Requirements` section read and written, `work line` giving a new line the next ids of its capability, and the
section laid over a copy of `spec/`, where the bar checks it.

The section holds one `### <capability>` block for each capability the lines go into, in the capability file's own
syntax one heading level down (backlog_section reads and writes it; the pieces beside the lines, relation rows, given
blocks, universal conditions and upstream entries, are backlog_forms'). The lines stay on the item until its batch
merges; `spec/` itself is never written here."""
import re
import shutil
from pathlib import Path

import backlog_forms
import backlog_recodify
import backlog_retires
import spec_lexicon
import spec_read
from backlog_items import Refused, commit, find, label, one_line
from backlog_section import (
    SECTION,
    Block,
    Blocks,
    Group,
    capability_file,
    ids,  # noqa: F401  (backlog_lines.ids, as its callers read it)
    laid_group,
    read,
    render,
    takes,
)


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
    takes(item, command)
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


def retire(root, name, ident, text, into=None, group=None, in_group=None):
    """`work line --retires <cap>#r<n> <line>`: the line written into the item `name` as `work line` writes it, and the
    old id under its block's `retired:` (backlog_retires), committed; refused, changing nothing, when the capability
    holds no live requirement of that id. The item and the new line's `<cap>#r<n>`."""
    item = find(root, name)
    capability, rid = backlog_retires.check(root, item, ident, into)
    new = add_line_to(root, item, capability, text, group, in_group)
    backlog_retires.with_retired(item, capability, rid)
    commit(root, item, "work line: %s %s retires %s" % (label(item), new, ident))
    return item, new


def recodify(root, name, capability):
    """`work line --recodify <capability>`: the item's block for it given `language: codified-2` (backlog_recodify),
    committed; refused, changing nothing, when the capability is in the new language already."""
    item = find(root, name)
    backlog_recodify.check(root, item, capability)
    backlog_recodify.with_language(item, capability)
    commit(root, item, "work line: %s recodifies %s" % (label(item), capability))
    return item


def add_term(root, name, capability, bullet):
    """`work line --term`: one term bullet written into the item's block for `capability` and committed."""
    item = find(root, name)
    takes(item)
    capability_file(root, capability)
    bullet = one_line(bullet, "term bullet")
    if spec_lexicon.entry(bullet, capability) is None:
        raise Refused("work line: the term bullet %s is not a term entry `- **<term>** (<part of speech>): <text>`" % bullet)
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


def lay_onto(into, item, files=None):
    """The item's blocks laid over `into/spec`: term bullets at the end of the capability file's `## Terms`, relation
    rows at the end of its `## Relations` table (made when it has none), the lines it retires out of its `## Behaviour`
    and into its `retired:` (backlog_retires), groups (headings raised to `### `, each with its given block) at the end
    of its `## Behaviour`, its marker switched when the block says `language:` (backlog_recodify); its universal conditions and upstream entries by `backlog_forms.lay_spec`, the paths they
    change added to `files`. The names of the capabilities laid."""
    blocks = read(item, "the item %s" % item.name)
    for block in blocks:
        path = capability_file(into, block.capability)
        text = path.read_text()
        if block.language:
            text = backlog_recodify.lay(text)
        if block.retired:
            text = backlog_retires.lay(text, block.capability, block.retired)
        if block.terms:
            text = _append(text, "Terms", "\n".join(block.terms))
        if block.relations:
            text = backlog_forms.with_lines(text, "Relations", block.relations, backlog_forms.HEADER, "Behaviour")
        if block.groups:
            text = _append(text, "Behaviour", "\n\n".join(laid_group(g) for g in block.groups))
        path.write_text(text)
    backlog_forms.lay_spec(into, blocks, [] if files is None else files)
    return [b.capability for b in blocks]


def _cut(text, chunk):
    """`text` less the first `chunk` that is a whole run of lines, with the blank line after it; unchanged when there
    is none."""
    found = re.search(r"(?m)^%s(?:\n\n|\n|\Z)" % re.escape(chunk), text)
    return text if found is None else text[:found.start()] + text[found.end():]


def unlay(into, item, files=None):
    """The reverse of `lay_onto` (plan 4 review, B1): the item's pieces taken out of `into/spec` where they are as
    `lay_onto` laid them, the paths outside spec/capabilities/ changed added to `files`. The names of the
    capabilities whose file changed."""
    changed, blocks = [], read(item, "the item %s" % item.name)
    for block in blocks:
        path = capability_file(into, block.capability)
        text = was = path.read_text()
        for chunk in [laid_group(g) for g in block.groups] + block.terms:
            text = _cut(text, chunk)
        if block.relations:
            text = backlog_forms.without_lines(text, "Relations", block.relations, backlog_forms.HEADER)
        if block.retired:
            text = backlog_retires.unlay(path, text, block.retired)
        if block.language:
            text = backlog_recodify.unlay(text)
        if text != was:
            path.write_text(text.rstrip("\n") + "\n")
            changed.append(block.capability)
    backlog_forms.unlay_spec(into, blocks, [] if files is None else files)
    return changed


def lay(root, item, into, others=()):
    """`spec/` of `root` copied to `into/spec`, each of `others` laid over the copy, then the item (`lay_onto`). The
    names of the item's capabilities laid."""
    shutil.copytree(Path(root) / "spec", Path(into) / "spec", dirs_exist_ok=True)
    for other in others:
        lay_onto(into, other)
    return lay_onto(into, item)


def _fresh(old, capability, used, seen, pairs):
    """`old`, or the next id above every one `seen` when it is `used`, the pair noted in `pairs`."""
    if old not in used:
        used.add(old)
        return old
    new = "%s%d" % (old[0], max(_number(i) for i in seen if i[0] == old[0]) + 1)
    seen.add(new)
    used.add(new)
    pairs.append(("%s#%s" % (capability, old), "%s#%s" % (capability, new)))
    return new


def renumber(root, item, taken):
    """New group, requirement and universal ids for the item's wherever they collide with its capability in `spec/`
    (groups, requirements, `retired:`), with `spec/universal.md`'s, or with `taken` ({capability, or "universal":
    ids} of the items picked before it), each the next free in file order (plan 4, D8). `taken` gains the item's ids;
    the item's `## Requirements` is rewritten. The (`<cap>#<old>`, `<cap>#<new>`) pairs."""
    blocks, pairs = read(item, "the item %s" % item.name), []
    out = Blocks(upstreams=blocks.upstreams)
    for block in blocks:
        cap = spec_read.capability(capability_file(root, block.capability))
        used = {g.id for g in cap.groups} | {r.id for g in cap.groups for r in g.requirements}
        used |= {r for r in cap.retired if re.fullmatch(r"[gr][1-9]\d*", r)} | taken.get(block.capability, set())
        seen = used | {g.id for g in block.groups} | {r for g in block.groups for r, _ in g.requirements}

        groups = []
        for g in block.groups:
            gid = _fresh(g.id, block.capability, used, seen, pairs)
            groups.append(Group(gid, g.title, [(_fresh(r, block.capability, used, seen, pairs), text)
                                               for r, text in g.requirements], g.given))
        out.append(block._replace(groups=groups))
        taken.setdefault(block.capability, set()).update(
            {g.id for g in groups} | {r for g in groups for r, _ in g.requirements})
    if blocks.universal:
        used = backlog_forms.universal_ids(root) | taken.get("universal", set())
        seen = used | {u for u, _ in blocks.universal}
        out.universal = [(_fresh(u, "universal", used, seen, pairs), text) for u, text in blocks.universal]
        taken.setdefault("universal", set()).update(u for u, _ in out.universal)
    if pairs:
        item.sections[SECTION] = render(out)
    return pairs
