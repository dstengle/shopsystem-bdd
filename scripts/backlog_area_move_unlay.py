"""An item's moves taken out of a spec again (b607), the reverse of backlog_area_move_lay's `lay`: each import of a
moved element's target area that the model file did not hold taken out, each moved entry taken out of the target's
layer and put back where the source's layer held it, each moved element taken out of the target's model and put back
where the source's held it. Where the source held them is read off the commit `base` (the batch's base) when one is
given, else off the latest version git holds of the file with them; with neither, they go at the end."""
import subprocess
from pathlib import Path

import backlog_area_move
import backlog_area_move_lay as laid
import backlog_model
import backlog_model_area


def held(path, base, needle=None):
    """The text of `path` at the commit `base`, else in the latest version git holds of it with the line `needle` (any
    version with no needle); None when git holds none."""
    path = Path(path)

    def git(*args):
        return subprocess.run(["git", "-C", str(path.parent), *args], capture_output=True, text=True)
    if not path.parent.is_dir():
        return None
    prefix = git("rev-parse", "--show-prefix")
    if prefix.returncode != 0:
        return None
    rel = prefix.stdout.strip() + path.name
    shas = [base] if base else git("log", "--format=%H", "--", path.name).stdout.split()
    for sha in shas:
        shown = git("show", "%s:%s" % (sha, rel))
        if shown.returncode == 0 and (needle is None or needle in shown.stdout.split("\n")):
            return shown.stdout
    return None


def _imports(into, targets, base, files):
    for path in sorted((Path(into) / "spec" / "model").glob("*.md")):
        text = path.read_text()
        names = laid._imported(text)
        was = held(path, base)
        before = laid._imported(was) if was is not None else []
        kept = [n for n in names if n not in targets or n in before]
        if kept != names:
            path.write_text(laid._with_imports(text, kept))
            files.append(laid._rel("model", path.stem))


def _entries_back(into, move, wanted, base, files):
    """The entries `wanted` admits taken out of the target's layer and put back where the source's held them."""
    bullets = laid._out_of_layer(into, move.target, wanted)
    if not bullets:
        return
    path = backlog_model.vocabulary_path(into, move.source)
    was = held(path, base, bullets[0])
    text = path.read_text() if path.is_file() else backlog_model._skeleton(into, move.source)
    put, end = _put_bullets(text, was, bullets), was if was is not None else text
    path.write_text(put.rstrip("\n") + "\n" * (len(end) - len(end.rstrip("\n"))))
    target = backlog_model.vocabulary_path(into, move.target)
    if target.is_file() and target.read_text().rstrip("\n") == backlog_model._skeleton(into, move.target).rstrip("\n"):
        target.unlink()
    files += [laid._rel("vocabulary", move.source), laid._rel("vocabulary", move.target)]


def _put_bullets(text, was, bullets):
    """`text` with `bullets` after the bullet `was` held before them, else at the end of its `## Terms`."""
    lines = text.split("\n")
    old = was.split("\n") if was is not None else []
    at = old.index(bullets[0]) if bullets[0] in old else None
    anchor = next((old[k] for k in range(at - 1, -1, -1) if old[k].startswith("- ")), None) if at else None
    if anchor is None or anchor not in lines:
        first = next((n for n, x in enumerate(lines) if x.startswith("- ")), None)
        if at is not None and first is not None:
            lines[first:first] = bullets
            return "\n".join(lines)
        return backlog_model.with_terms(text, bullets)
    _, spans = laid._bullets(text)
    end = next(e for s, e in spans if lines[s] == anchor)
    lines[end:end] = bullets
    return "\n".join(lines)


def _element_back(into, move, base, files, blocks):
    """The element taken out of the target's model and put back where the source's held it."""
    path, lines, start, end = laid._body(into, move.target)
    body = lines[start:end]
    at = backlog_model._at(body, move.what)
    if at is None:
        return
    stop = backlog_model._end(body, at)
    chunk = body[at:stop]
    path.write_text("\n".join(lines[:start] + laid._cut(body, at, stop) + lines[end:]))
    backlog_model_area.unmade(into, move.target, blocks)
    source, lines, start, end = laid._body(into, move.source)
    was = held(source, base, move.what)
    old = backlog_model._fence(was, source.name) if was is not None and "```model" in was else None
    body = lines[start:end]
    prev = None
    if old is not None:
        old_body = old[0][old[1]:old[2]]
        k = old_body.index(move.what) if move.what in old_body else 0
        chunk = old_body[k:backlog_model._end(old_body, k)] if move.what in old_body else chunk
        prev = next((old_body[j] for j in range(k - 1, -1, -1) if old_body[j].strip() and
                     not old_body[j].startswith(" ")), None)
    where = backlog_model._at(body, prev) if prev else None
    if where is not None:
        stop = backlog_model._end(body, where)
        body[stop:stop] = [""] + chunk
    elif prev is None and old is not None:
        body[0:0] = chunk + ([""] if body else [])
    else:
        body = backlog_model.merged(body, chunk)
    source.write_text("\n".join(lines[:start] + body + lines[end:]))
    files += [laid._rel("model", move.source), laid._rel("model", move.target)]


def unlay(into, blocks, files, base=None):
    """The item's moves taken out of `into/spec`, each path changed added to `files`."""
    moves = list(getattr(blocks, "moves", ()))
    if not moves:
        return
    _imports(into, {m.target for m in moves}, base, files)
    for move in reversed(moves):
        if move.kind == "model line":
            _entries_back(into, move, lambda w, r, m=move: bool(r) and backlog_area_move.means(m.what, r), base, files)
            _element_back(into, move, base, files, blocks)
        else:
            word, _, ref = move.what.partition(" → ")
            _entries_back(into, move, lambda w, r, a=word, b=ref: (w, r) == (a, b), base, files)
