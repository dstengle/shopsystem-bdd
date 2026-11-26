"""An item's own model lines and terms taken back out of it or given a new text (b367, drafting r43-r50), as
`--remove` and `--reword` do for its requirement lines (backlog_reword). Each commits only the item.

`work line <item> --remove-model "<model lines>"`: an element header alone (`object checklist`, `service notes`)
takes the element out of the item's model block with its members; a header with indented member lines takes only
those members. `--reword-model "<header>" "<model lines>"` puts the new model lines (checked as `--model`'s are) in
place of the element and its members. `--remove-term <term>` takes a term out (a vocabulary entry of a model block,
or a term bullet of a capability block); `--reword-term <term> "<entry>"` puts the new entry in its place. A term is
named by its word, by `<word> → <element>` when two entries share the word, or by its whole bullet. A model block
left with no line and no entry goes. A model line or a term the item does not hold is refused, naming it; `--into
<capability>` narrows a model line to its capability's area, and a term, as `--term` takes it, to the model block of
its area or the capability's own block (b800)."""
import re

import backlog_model
from backlog_items import Refused, commit, find, label, one_line

FLAGS = ("remove_model", "reword_model", "remove_term", "reword_term")


def add_arguments(p):
    """`work line`'s options that take an item's own model line or term out, or reword it."""
    p.add_argument("--remove-model", metavar="MODEL", help="an element header of the item's model lines (taken out "
                   "with its members), or the header with member lines (only those taken out)")
    p.add_argument("--reword-model", metavar="HEADER", help="an element header of the item's model lines, its "
                   "element and members replaced by the model lines given as the text")
    p.add_argument("--remove-term", metavar="TERM", help="an item's term (its word, `<word> → <element>`, or its "
                   "whole bullet) taken out")
    p.add_argument("--reword-term", metavar="TERM", help="an item's term (its word, `<word> → <element>`, or its "
                   "whole bullet) replaced by the entry given as the text, its bullet as --term takes it "
                   "(`- **w** (...) ...`, no `--` before it); with --into, the capability's term")


def given(args):
    """True when the run is one of this module's."""
    return any(getattr(args, k, None) is not None for k in FLAGS)


def _model_blocks(blocks, area):
    return [(n, b) for n, b in enumerate(blocks.models) if area is None or b.area == area]


def _located(root, blocks, header, into):
    """(block index, start, end) of the element `header` declares in the item's model blocks; refused, naming the
    model line, when none holds it or more than one area does."""
    area = backlog_model.area_of(root, into, blocks) if into else None
    found = []
    for n, block in _model_blocks(blocks, area):
        at = backlog_model._at(list(block.lines), header)
        if at is not None:
            found.append((n, at, backlog_model._end(list(block.lines), at)))
    if not found:
        raise Refused("work line: the item holds no model line %s" % header, reason="model line not in the item",
                      names=["model line:%s" % header])
    if len(found) > 1:
        raise Refused("work line: the model line %s is in the model blocks of %s; name one with --into" % (
            header, ", ".join(blocks.models[n].area for n, _, _ in found)))
    return found[0]


def _cut(body, at, end):
    """`body` without its lines at:end and the blank line that set them apart."""
    body = body[:at] + body[end:]
    if at > 0 and at <= len(body) and not body[at - 1].strip() and (at == len(body) or not body[at].strip()):
        del body[at - 1]
    while body and not body[0].strip():
        del body[0]
    return body


def _put(item, blocks, n, lines=None, terms=None):
    """The model block `n` given `lines` or `terms`, gone when it holds neither."""
    from backlog_section import SECTION, render
    block = blocks.models[n]
    block = block._replace(**{k: tuple(v) for k, v in (("lines", lines), ("terms", terms)) if v is not None})
    if any(x.strip() for x in block.lines) or block.terms:
        blocks.models[n] = block
    else:
        del blocks.models[n]
    item.sections[SECTION] = render(blocks)


def _opened(root, name):
    from backlog_section import read, takes
    item = find(root, name)
    takes(item)
    return item, read(item, "the item %s" % item.name)


def _lines(text):
    return [x.rstrip() for x in text.replace("\r\n", "\n").split("\n") if x.strip()]


def remove_model(root, name, model, into=None):
    """`--remove-model`: the element (or only the member lines given) out of the item, committed."""
    item, blocks = _opened(root, name)
    for header, members in reversed(backlog_model.chunks(_lines(model))):
        n, at, end = _located(root, blocks, header, into)
        body = list(blocks.models[n].lines)
        if members:
            held = [x.rstrip() for x in body[at + 1:end]]
            missing = [m for m in members if m not in held]
            if missing:
                raise Refused("work line: the item holds no model line %s under %s" % (missing[0].strip(), header),
                              reason="model line not in the item", names=["model line:%s" % missing[0].strip()])
            body = body[:at + 1] + [x for x in body[at + 1:end] if x.rstrip() not in members] + body[end:]
            if backlog_model._end(body, at) == at + 1:
                body = _cut(body, at, at + 1)
        else:
            body = _cut(body, at, end)
        _put(item, blocks, n, lines=body)
    said = model.strip().split("\n")[0]
    commit(root, item, "work line: %s removes the model line %s" % (label(item), said))
    return item


def reword_model(root, name, header, model, into=None):
    """`--reword-model`: the element and its members replaced by `model`, checked as `--model`'s lines; committed."""
    item, blocks = _opened(root, name)
    header = one_line(header, "model line").strip()
    n, at, end = _located(root, blocks, header, into)
    lines = _lines(model or "")
    if not lines:
        raise Refused("work line: --reword-model %s takes the model lines that replace it" % header)
    backlog_model._checked(root, blocks.models[n].area, lines, blocks)
    body = list(blocks.models[n].lines)
    _put(item, blocks, n, lines=body[:at] + lines + body[end:])
    commit(root, item, "work line: %s rewords the model line %s" % (label(item), header))
    return item


def _matches(bullet, term):
    import spec_vocabulary
    found = spec_vocabulary.ENTRY.match(bullet)
    if bullet == term or not found:
        return bullet == term
    word = found.group("term")
    ref = spec_vocabulary.REF.match(found.group("text") or "")
    element = ref.group("ref").strip() if found.group("arrow") and ref else None
    return term == word or (element is not None and re.sub(r"\s+", " ", term) == "%s → %s" % (word, element))


def _term_at(blocks, term, root=None, into=None):
    """[(kind, block index, bullet)] of the item's terms `term` names: a model block's ("model") or a capability
    block's ("capability"), of `into`'s area or its own block when given; refused, naming the term, when none or more
    than one."""
    area = backlog_model.area_of(root, into, blocks) if into else None
    found = [("model", n, b) for n, block in _model_blocks(blocks, area) for b in block.terms if _matches(b, term)]
    found += [("capability", n, b) for n, block in enumerate(blocks) for b in block.terms
              if (into is None or block.capability == into) and _matches(b, term)]
    if not found:
        raise Refused("work line: the item holds no term %s" % term, reason="term not in the item",
                      names=["term:%s" % term])
    if len(found) > 1:
        raise Refused("work line: %d terms of the item are %s; name one by `<word> → <element>` or its whole "
                      "bullet: %s" % (len(found), term, "; ".join(b for _, _, b in found)))
    return found[0]


def _replace_term(item, blocks, term, new, root=None, into=None):
    from backlog_section import SECTION, render
    kind, n, bullet = _term_at(blocks, term, root, into)
    if kind == "model":
        terms = list(blocks.models[n].terms)
        at = terms.index(bullet)
        terms[at:at + 1] = [new] if new else []
        _put(item, blocks, n, terms=terms)
        return
    block = blocks[n]
    at = block.terms.index(bullet)
    block.terms[at:at + 1] = [new] if new else []
    if not (block.groups or block.terms or block.relations or block.retired or block.language or block.new):
        del blocks[n]
    item.sections[SECTION] = render(blocks)


def remove_term(root, name, term, into=None):
    """`--remove-term`: the item's term out of it, committed."""
    item, blocks = _opened(root, name)
    term = one_line(term, "term").strip()
    _replace_term(item, blocks, term, None, root, into)
    commit(root, item, "work line: %s removes the term %s" % (label(item), term))
    return item


def reword_term(root, name, term, entry, into=None):
    """`--reword-term`: the item's term replaced by `entry` (a model block's checked as `--term`'s are), committed."""
    item, blocks = _opened(root, name)
    term = one_line(term, "term").strip()
    if not entry:
        raise Refused("work line: --reword-term %s takes the entry that replaces it" % term)
    kind = _term_at(blocks, term, root, into)[0]
    new = backlog_model._entries([entry])[0] if kind == "model" else one_line(entry, "term")
    _replace_term(item, blocks, term, new, root, into)
    commit(root, item, "work line: %s rewords the term %s" % (label(item), term))
    return item


def cmd(args):
    """`work line` with one of this module's options: one of them, the text only of a reword, `--into` narrowing
    where the model line or term is; what was done, printed."""
    flags = [k for k in FLAGS if getattr(args, k, None) is not None]
    from backlog_cli import PIECES
    others = [k for k in PIECES[1:] + ("retires", "reword", "remove", "group", "in_group")
              if getattr(args, k, None) is not None]
    if len(flags) != 1 or others:
        raise Refused("work line: --remove-model, --reword-model, --remove-term and --reword-term take one of them, "
                      "the text of a reword, and --into")
    flag = flags[0]
    value = getattr(args, flag)
    if flag.startswith("remove") and args.text is not None:
        raise Refused("work line: --%s takes no text" % flag.replace("_", "-"))
    if flag == "remove_model":
        item, said = remove_model(args.root, args.name, value, args.into), "model line %s removed"
    elif flag == "reword_model":
        item, said = reword_model(args.root, args.name, value, args.text, args.into), "model line %s reworded"
    elif flag == "remove_term":
        item, said = remove_term(args.root, args.name, value, args.into), "term %s removed"
    else:
        item, said = reword_term(args.root, args.name, value, args.text, args.into), "term %s reworded"
    print("%s: %s" % (label(item), said % value.strip().split("\n")[0]))
    return 0
