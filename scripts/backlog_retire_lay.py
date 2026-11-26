"""An item's imports and retirements laid over a spec and taken out again (b672, batches r132-r134), after its moves
and before its model lines are laid, and after its model lines and before its moves are taken out (backlog_model's
`lay`, `unlay`).

The imports are backlog_import's. A model line's retirement takes the element (its header and members) out of the
fence of `spec/model/<area>.md`, with each entry of any layer that means it (backlog_area_move's `means`); a term's
retirement takes its entry out of its layer. The unlay puts each back where the file held it at the commit `base`
(the batch's base), else in the latest version git holds of it with it (backlog_area_move_unlay's `put_element` and
`_put_bullets`)."""
import subprocess
from pathlib import Path

import backlog_area_move
import backlog_area_move_lay as laid
import backlog_area_move_unlay as unlaid
import backlog_import
import backlog_model
from backlog_items import Refused


def _wanted(retirement):
    """Whether an entry (word, ref) is one the retirement takes out."""
    if retirement.kind == "model line":
        return lambda w, r: bool(r) and backlog_area_move.means(retirement.what, r)
    word, _, ref = retirement.what.partition(" → ")
    return lambda w, r: (w, r) == (word, ref)


def _layers(into):
    return [p.stem for p in sorted((Path(into) / "spec" / "vocabulary").glob("*.md"))]


def lay(into, blocks, files):
    """The item's imports and retirements laid over `into/spec`, each path changed added to `files`."""
    backlog_import.lay(into, blocks, files)
    for retirement in getattr(blocks, "retirements", ()):
        if retirement.kind == "model line":
            path, lines, start, end = laid._body(into, retirement.area)
            body = lines[start:end]
            at = backlog_model._at(body, retirement.what)
            if at is None:
                raise Refused("the area %s holds no model line %s to retire" % (retirement.area, retirement.what))
            path.write_text("\n".join(lines[:start] + laid._cut(body, at, backlog_model._end(body, at)) +
                                      lines[end:]))
            files.append(laid._rel("model", retirement.area))
            layers = _layers(into)
        else:
            layers = [retirement.area]
        taken = [layer for layer in layers if laid._out_of_layer(into, layer, _wanted(retirement))]
        if retirement.kind == "term" and not taken:
            raise Refused("the layer %s holds no term %s to retire" % (retirement.area, retirement.what))
        files += [laid._rel("vocabulary", layer) for layer in taken]


def _versions(path, base):
    """The texts of `path` at `base`, else each version git holds of it, latest first."""
    if base:
        yield unlaid.held(path, base)
        return
    shas = subprocess.run(["git", "-C", str(path.parent), "log", "--format=%H", "--", path.name],
                          capture_output=True, text=True).stdout.split() if path.parent.is_dir() else []
    for sha in shas:
        yield unlaid.held(path, sha)


def _entries_back(into, layer, wanted, base, files):
    """The entries `wanted` admits put back into `layer` where a version git holds of it held them."""
    path = backlog_model.vocabulary_path(into, layer)
    if not path.is_file():
        return
    text = path.read_text()
    have = {laid._entry_ref(text.split("\n")[s]) for s, _ in laid._bullets(text)[1]}
    for was in _versions(path, base):
        if was is None:
            continue
        lines, spans = laid._bullets(was)
        bullets = [x for s, e in spans if wanted(*laid._entry_ref(" ".join(lines[s:e])))
                   and laid._entry_ref(lines[s]) not in have for x in lines[s:e]]
        if bullets:
            put = unlaid._put_bullets(text, was, bullets)
            path.write_text(put.rstrip("\n") + "\n")
            files.append(laid._rel("vocabulary", layer))
            return


def unlay(into, blocks, files, base=None):
    """The item's retirements and imports taken out of `into/spec` again, each path changed added to `files`."""
    for retirement in reversed(list(getattr(blocks, "retirements", ()))):
        if retirement.kind == "model line":
            path = backlog_model.model_path(into, retirement.area)
            if not path.is_file():
                continue
            _, lines, start, end = laid._body(into, retirement.area)
            if backlog_model._at(lines[start:end], retirement.what) is None:
                unlaid.put_element(into, retirement.area, retirement.what, None, base)
                files.append(laid._rel("model", retirement.area))
            layers = _layers(into)
        else:
            layers = [retirement.area]
        for layer in layers:
            _entries_back(into, layer, _wanted(retirement), base, files)
    backlog_import.unlay(into, blocks, files, base)
