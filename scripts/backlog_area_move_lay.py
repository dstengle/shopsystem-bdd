"""An item's moves laid over a spec (b607, batches r117, r118), before its model lines are laid (backlog_model's
`lay`).

A model line's move takes the element (its header and members) out of the fence of `spec/model/<source>.md` and
declares it in `spec/model/<target>.md` (made for a capability the item makes, backlog_model_area), with each entry of
the source's layer that means it (backlog_area_move's `means`) out of `spec/vocabulary/<source>.md` into the target's
layer (made when missing); a term's move takes its entry out of its layer into the target's. Each model file of an area
whose capabilities' lines use a moved word is given the import of the target area, so that the word stays in a layer
its lines read (v_m1)."""
import re
from pathlib import Path

import backlog_area_move
import backlog_model
import backlog_model_area
from backlog_items import Refused
from plumbing import shop_files

IMPORTS = re.compile(r"^imports:\s*\[(.*)\]\s*$", re.MULTILINE)


def _rel(kind, area):
    return "spec/%s/%s.md" % (kind, area)


def _body(into, area):
    path = backlog_model.model_path(into, area)
    lines, start, end = backlog_model._fence(path.read_text(), _rel("model", area))
    return path, lines, start, end


def _bullets(text):
    """[(start, end)] of each `- ` bullet of `text`'s lines with its continuation lines."""
    lines, out = text.split("\n"), []
    for n, line in enumerate(lines):
        if line.startswith("- "):
            out.append([n, n + 1])
        elif out and out[-1][1] == n and line[:1].isspace() and line.strip():
            out[-1][1] = n + 1
    return lines, out


def _entry_ref(bullet):
    import spec_vocabulary
    found = spec_vocabulary.ENTRY.match(" ".join(bullet.split()))
    ref = spec_vocabulary.REF.match(found.group("text").strip()) if found and found.group("arrow") else None
    return (found.group("term").strip(), " ".join(ref.group("ref").split())) if ref else (None, None)


def _layer(into, area):
    path = backlog_model.vocabulary_path(into, area)
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(backlog_model._skeleton(into, area))
    return path


def _out_of_layer(into, layer, wanted):
    """The lines of each entry of `layer` `wanted` admits, taken out of its file."""
    path = backlog_model.vocabulary_path(into, layer)
    if not path.is_file():
        return []
    lines, spans = _bullets(path.read_text())
    taken = [(s, e) for s, e in spans if wanted(*_entry_ref(" ".join(lines[s:e])))]
    out = [x for s, e in taken for x in lines[s:e]]
    for s, e in reversed(taken):
        del lines[s:e]
    if taken:
        path.write_text("\n".join(lines))
    return out


def _words(bullets):
    """Every spelling of the moved entries: the word, its forms and its plural."""
    out = set()
    for line in bullets:
        if line.startswith("- "):
            word, _ = _entry_ref(line)
            out |= {word} if word else set()
    text = " ".join(bullets)
    for field in re.findall(r"(?:Forms|Plural):\s*([^.]+)\.", text):
        out |= {w.strip() for w in field.split(",") if w.strip()}
    return out


def _users(into, words, target):
    """The areas other than `target` a capability of which says one of `words` in its lines."""
    out = set()
    pattern = re.compile(r"(?i)\b(?:%s)\b" % "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)))
    for path in sorted((Path(into) / "spec" / "capabilities").glob("*.md")):
        head, body = shop_files.frontmatter(path.read_text())
        area = str(head.get("area") or "")
        if area and area != target and backlog_model.model_path(into, area).is_file() and pattern.search(body):
            out.add(area)
    return out


def _imported(text):
    found = IMPORTS.search(text)
    return [x.strip() for x in found.group(1).split(",") if x.strip()] if found else []


def _with_imports(text, names):
    line = "imports: [%s]" % ", ".join(names)
    return IMPORTS.sub(line, text, count=1) if IMPORTS.search(text) else text.replace("\n---\n", "\n%s\n---\n" % line, 1)


def lay(into, blocks, files):
    """The item's moves laid over `into/spec`, each path changed added to `files`."""
    moves, words = getattr(blocks, "moves", ()), {}
    for move in moves:
        if move.kind == "model line":
            path, lines, start, end = _body(into, move.source)
            body = lines[start:end]
            at = backlog_model._at(body, move.what)
            if at is None:
                raise Refused("the area %s holds no model line %s to move" % (move.source, move.what))
            chunk = body[at:backlog_model._end(body, at)]
            path.write_text("\n".join(lines[:start] + _cut(body, at, at + len(chunk)) + lines[end:]))
            backlog_model_area.made(into, move.target, blocks)
            path2, lines2, start2, end2 = _body(into, move.target)
            path2.write_text("\n".join(lines2[:start2] + backlog_model.merged(lines2[start2:end2], chunk) +
                                       lines2[end2:]))
            files += [_rel("model", move.source), _rel("model", move.target)]
            bullets = _out_of_layer(into, move.source, lambda w, r, m=move: bool(r) and backlog_area_move.means(m.what, r))
        else:
            word, _, ref = move.what.partition(" → ")
            bullets = _out_of_layer(into, move.source, lambda w, r, a=word, b=ref: (w, r) == (a, b))
            if not bullets and not any(_entry_ref(x) == (word, ref) for x in _all(into, move.target)):
                raise Refused("the layer %s holds no term %s to move" % (move.source, move.what))
        if bullets:
            path = _layer(into, move.target)
            path.write_text(backlog_model.with_terms(path.read_text(), bullets))
            files += [_rel("vocabulary", move.source), _rel("vocabulary", move.target)]
        words.setdefault(move.target, set()).update(_words(bullets))
    for target, said in words.items():
        for area in sorted(_users(into, said, target)) if said else ():
            path = backlog_model.model_path(into, area)
            text = path.read_text()
            if target not in _imported(text):
                path.write_text(_with_imports(text, _imported(text) + [target]))
                files.append(_rel("model", area))


def _all(into, layer):
    path = backlog_model.vocabulary_path(into, layer)
    return path.read_text().split("\n") if path.is_file() else []


def _cut(body, at, end):
    """`body` without its lines at:end and the blank line that set them apart."""
    body = body[:at] + body[end:]
    if at > 0 and not body[at - 1].strip() and (at == len(body) or not body[at].strip()):
        del body[at - 1]
    return body
