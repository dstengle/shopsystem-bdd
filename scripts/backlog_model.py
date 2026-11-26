"""An item's model lines and vocabulary entries (the domain contract design, §10 "work line and the readiness bar lay
lines into spec/model/ and spec/vocabulary/"), in a context with a domain model (`spec/model/`).

The item keeps them in a `### <area> model` block of its `## Requirements` (backlog_section reads and writes it): a
` ```model ` fence of model lines in the area's own syntax (domain_model_parse), then vocabulary entries `- **w**
(...) → <element>. ...`. `work line --into <capability>` with `--model <lines>`, `--relation "<object>: <phrase> →
<object> (<cardinality>)"` or a `--term` bullet writes into the block of the capability's `area:`, or of the
own name of a capability the item makes (backlog_model_area, b387) (`add`), merged:
an element the block names already gets the new member lines. `lay` puts them into `spec/model/<area>.md` (an element
the area declares gets the member lines at its end, a new one is appended to the fence) and the entries at the end of
`## Terms` of `spec/vocabulary/<area>.md` (made when missing); `unlay` takes them out again as `lay` put them."""
import functools
import re
from collections import namedtuple
from pathlib import Path

import backlog_model_area
import backlog_model_elements
import backlog_model_ops
from backlog_items import Refused, commit, find, label, one_line
from plumbing import shop_files

HEAD = re.compile(r"^### ([a-z0-9]+(?:-[a-z0-9]+)*) model$")
FENCE, CLOSE = "```model", "```"
ModelBlock = namedtuple("ModelBlock", "area lines terms", defaults=((), ()))
ELEMENT = re.compile(r"^(object|service) (.+?)(?: kind of .*)?$")
RELATION = re.compile(r"^([\w -]+?):\s*(\S.*→.*\(.*\))$")


def chunks(lines):
    """[(header, [member lines])] of model lines: a header at no indent, its members indented under it."""
    out = []
    for line in lines:
        if not line.strip():
            continue
        if not line.startswith(" "):
            out.append((line.rstrip(), []))
        elif out:
            out[-1][1].append(line.rstrip())
        else:
            raise Refused("work line: the model line %r is under no element" % line.strip())
    return out


def _end(body, at):
    """The index after the last member line of the element whose header is at `at`."""
    end = at + 1
    while end < len(body) and (body[end].startswith(" ") or not body[end].strip()):
        end += 1
    while end > at + 1 and not body[end - 1].strip():
        end -= 1
    return end


def _at(body, header):
    """The index of the element `header` declares in `body`: its line, or an object's declared with its kind
    (`object item` is `object item kind of file`); None when the body declares none."""
    if header in body:
        return body.index(header)
    if backlog_model_elements.lone(header):
        return backlog_model_elements.lone_at(body, header)
    named = ELEMENT.match(header)
    return next((n for n, line in enumerate(body) if named and ELEMENT.match(line)
                 and ELEMENT.match(line).groups() == named.groups()), None)


def merged(body, lines):
    """`body` (model lines) with `lines` merged in: an object that restates its element, and an event's or an actor's
    line that restates one of its phrase or name, in place of it (backlog_model_elements), each other element's members after the element's own, else the element appended after a blank line (before any blank lines the body ends with)."""
    body = list(body)
    for header, members in chunks(lines):
        at = _at(body, header)
        if at is not None and backlog_model_elements.lone(header):
            body[at] = header
        elif at is not None and backlog_model_elements.restates(header, members, body, at, _end(body, at)):
            backlog_model_elements.restate(body, at, _end(body, at), header, members)
        elif at is not None:
            members, end = backlog_model_ops.restate(body, at, _end(body, at), members)
            body[end:end] = members
        else:
            at = len(body)
            while at and not body[at - 1].strip():
                at -= 1
            body[at:at] = ([""] if at else []) + [header] + members
    return body


def unmerged(body, lines, held=None):
    """The reverse of `merged`: an object, an event or an actor a chunk restated put back as `held(header, None,
    members)` gives it, or a new event or actor taken out (backlog_model_elements), each operation a chunk restated put back as `held(header, operation, lines)` gives
    the model lines before the lay (backlog_model_ops, b463; taken out when it gives None), the chunk's other members
    taken off its element's end, and an element left with no member taken out whole with the blank line before it
    (the chunk made it)."""
    body = list(body)
    for header, members in reversed(chunks(lines)):
        at = _at(body, header)
        if at is None or backlog_model_elements.unrestate(body, at, header, members, held) or \
                backlog_model_elements.unrestate_lone(body, at, header, held):
            continue
        ops, members = backlog_model_ops.restated(members, body, at, _end(body, at))
        end = _end(body, at)
        first = end - len(members)
        if first >= at + 1 and body[first:end] == members:
            del body[first:end]
        for op, unit in ops:
            before = held(header, op, unit) if held else None
            backlog_model_ops.unrestate(body, at, _end(body, at), header, [(op, unit)], before)
        if _end(body, at) == at + 1 and (members or ops):
            del body[at]
            if at > 0 and not body[at - 1].strip():
                del body[at - 1]
    return body


def area_of(root, capability, blocks=()):
    """The area of a capability's model lines (backlog_model_area): a new capability's own name, else its `area:`."""
    return backlog_model_area.area_of(root, capability, blocks)


model_path = backlog_model_area.model_path


def vocabulary_path(root, area):
    return Path(root) / "spec" / "vocabulary" / ("%s.md" % area)


def _fence(text, rel):
    """(start, end) of the lines inside the first ```model fence of `text`'s lines."""
    lines = text.split("\n")
    if FENCE not in lines:
        raise Refused("%s has no ```model block" % rel)
    start = lines.index(FENCE) + 1
    end = next((i for i in range(start, len(lines)) if lines[i] == CLOSE), None)
    if end is None:
        raise Refused("%s: its ```model block is not closed" % rel)
    return lines, start, end


def _checked(root, area, lines, blocks=()):
    """The model lines, refused unless they read as a model block (domain_model_parse); an area with no model file
    is refused unless it is a capability's the item makes (b387), whose file the lay makes."""
    import domain_model_parse
    if not model_path(root, area).is_file() and backlog_model_area.area_block(blocks, area) is None:
        raise Refused("work line: there is no spec/model/%s.md: the area %s has no model to add to" % (area, area))
    domain_model_parse.Reader("the item's model lines", area).read(lines, 1)
    return tuple(lines)


def block_of(blocks, area):
    found = next((i for i, b in enumerate(blocks.models) if b.area == area), None)
    if found is None:
        blocks.models.append(ModelBlock(area))
        found = len(blocks.models) - 1
    return found


def _entries(terms):
    """The vocabulary entries `--term` gave (once or more, b453), each checked; one that does not read refuses all."""
    import spec_vocabulary
    bullets = tuple(one_line(t, "vocabulary entry") for t in terms)
    for bullet in bullets:
        found = spec_vocabulary.ENTRY.match(bullet)
        if not found or not found.group("arrow") or not spec_vocabulary.REF.match(found.group("text")):
            raise Refused("work line: the vocabulary entry %s is not `- **<word>** (<part of speech>) → <element>. "
                          "...`" % bullet)
    return bullets


def add(root, name, capability, model=None, relation=None, term=None):
    """`work line --into <capability>` with `--model`, `--relation` or `--term` (once or more) in a context with a
    domain model: the piece written into the item's model block of the capability's area and committed. What was
    written, said."""
    from backlog_section import SECTION, read, render, takes
    item = find(root, name)
    takes(item)
    blocks = read(item, "the item %s" % item.name)
    area = area_of(root, capability, blocks)
    at = block_of(blocks, area)
    block = blocks.models[at]
    if term is not None:
        bullets = _entries([term] if isinstance(term, str) else term)
        blocks.models[at] = block._replace(terms=block.terms + bullets)
        said = "%s of %s" % ("a vocabulary entry" if len(bullets) == 1 else "%d vocabulary entries" % len(bullets),
                             area)
    else:
        if relation is not None:
            found = RELATION.match(one_line(relation, "relation"))
            if not found:
                raise Refused("work line: the relation %s is not `<object>: <phrase> → <object> (<cardinality>)`"
                              % relation)
            lines = ["object %s" % found.group(1).strip(), "  relations: %s" % found.group(2).strip()]
        else:
            lines = [x.rstrip() for x in model.replace("\r\n", "\n").split("\n") if x.strip()]
        _checked(root, area, lines, blocks)
        blocks.models[at] = block._replace(lines=tuple(merged(block.lines, lines)))
        said = "model lines of %s" % area + _left_out(root, area, block.lines, lines)
    item.sections[SECTION] = render(blocks)
    if term is not None:    # a term that breaks a lexicon rule (b810, b826, drafting r101)
        __import__("backlog_term_rules").refuse(root, item, bullets)
    commit(root, item, "work line: %s %s" % (label(item), said))
    return item, said


def _left_out(root, area, held, lines):
    """What `add` says of the member lines an object the lines restate leaves out (drafting r70, b647): each named,
    the area's model as the item's block lays it the body; nothing when none is left out."""
    path = model_path(root, area)
    if not path.is_file():
        return ""
    text, start, end = _fence(path.read_text(), "spec/model/%s.md" % area)
    cut = backlog_model_elements.left_out(merged(text[start:end], held), chunks(lines))
    return "".join("; the restatement leaves out the member line `%s`" % line for line in cut)


def _terms(lines):
    """(heading index, index after the section's last line that is not blank) of `## Terms` in `lines`, or None."""
    if "## Terms" not in lines:
        return None
    h = lines.index("## Terms")
    end = next((i for i in range(h + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    while end > h + 1 and not lines[end - 1].strip():
        end -= 1
    return h, end


def with_terms(text, bullets):
    """`text` with `bullets` after the last line of its `## Terms` (the section made at the end when missing)."""
    lines = text.split("\n")
    found = _terms(lines)
    if found is None:
        return text.rstrip("\n") + "\n\n## Terms\n\n" + "\n".join(bullets) + "\n"
    h, end = found
    lines[end:end] = ([""] if end == h + 1 else []) + list(bullets)
    return "\n".join(lines)


def without_terms(text, bullets):
    """The reverse of `with_terms` where the section has more than `bullets` in it."""
    lines = text.split("\n")
    for bullet in bullets:
        if bullet in lines:
            lines.remove(bullet)
    return "\n".join(lines)


def _skeleton(into, area):
    return ("---\nid: vocabulary/%s/%s\narea: %s\n---\n\n# The words of %s\n\n## Terms\n"
            % (shop_files.context_path(into), area, area, area))


def lay(into, blocks, files):
    """The item's moves (backlog_area_move_lay), imports and retirements (backlog_retire_lay), then its model blocks,
    laid into `into/spec`, each path changed added to `files`."""
    for module in ("backlog_area_move_lay", "backlog_retire_lay"):
        __import__(module).lay(into, blocks, files)
    for block in getattr(blocks, "models", ()):
        if block.lines:
            path, rel = model_path(into, block.area), "spec/model/%s.md" % block.area
            backlog_model_area.made(into, block.area, blocks)
            lines, start, end = _fence(path.read_text(), rel)
            path.write_text("\n".join(lines[:start] + merged(lines[start:end], block.lines) + lines[end:]))
            files.append(rel)
        if block.terms:
            path = vocabulary_path(into, block.area)
            if not path.is_file():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(_skeleton(into, block.area))
            path.write_text(with_terms(path.read_text(), block.terms))
            files.append("spec/vocabulary/%s.md" % block.area)


def unlay(into, blocks, files, base=None):
    """The reverse of `lay`, each path changed added to `files`; a vocabulary file `lay` made removed; an operation a
    model line restates put back as the commit `base` (the batch's base, b485) held it, else as git's history did."""
    for block in getattr(blocks, "models", ()):
        path, rel = model_path(into, block.area), "spec/model/%s.md" % block.area
        if block.lines and path.is_file():
            lines, start, end = _fence(path.read_text(), rel)
            held = (functools.partial(backlog_model_ops.at_base, path, base) if base
                    else functools.partial(backlog_model_ops.held, path))
            text = "\n".join(lines[:start] + unmerged(lines[start:end], block.lines, held) + lines[end:])
            if text != path.read_text():
                path.write_text(text)
                files.append(rel)
            if backlog_model_area.unmade(into, block.area, blocks) and rel not in files:
                files.append(rel)
        path = vocabulary_path(into, block.area)
        if block.terms and path.is_file():
            text = without_terms(path.read_text(), block.terms)
            if text.rstrip("\n") == _skeleton(into, block.area).rstrip("\n"):
                path.unlink()
            elif text != path.read_text():
                path.write_text(text)
            files.append("spec/vocabulary/%s.md" % block.area)
    for module in ("backlog_retire_lay", "backlog_area_move_unlay"):
        __import__(module).unlay(into, blocks, files, base)
