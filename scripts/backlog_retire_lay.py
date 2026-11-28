"""An item's imports and retirements laid over a spec (b672, batches r132-r134), after its moves and before its model
lines are laid (backlog_model's `lay`).

The imports are backlog_import's. A model line's retirement takes the element (its header and members) out of the
fence of `spec/model/<area>.md`, with each entry of any layer that means it (backlog_area_move's `means`); a term's
retirement takes its entry out of its layer, and is met when a model line retirement of the item took the entry
out with its element (b688); an area's retirement takes the area out (backlog_retire_area's `lay`, b898)."""
from pathlib import Path

import backlog_area_move
import backlog_area_move_lay as laid
import backlog_import
import backlog_model
import backlog_retire_area
from backlog_items import Refused


def _wanted(retirement):
    """Whether an entry (word, ref) is one the retirement takes out."""
    if retirement.kind == "model line":
        return lambda w, r: bool(r) and backlog_area_move.means(retirement.what, r)
    word, _, ref = retirement.what.partition(" → ")
    return lambda w, r: (w, r) == (word, ref)


def _elemental(retirement, blocks):
    """Whether a model line retirement of the item takes the term's entry out with its element (b688), so that the
    term's retirement has nothing left to take out and is met."""
    ref = retirement.what.partition(" → ")[2]
    return any(r.kind == "model line" and backlog_area_move.means(r.what, ref)
               for r in getattr(blocks, "retirements", ()))


def _layers(into):
    return [p.stem for p in sorted((Path(into) / "spec" / "vocabulary").glob("*.md"))]


def lay(into, blocks, files):
    """The item's imports and retirements laid over `into/spec`, each path changed added to `files`."""
    backlog_import.lay(into, blocks, files)
    for retirement in getattr(blocks, "retirements", ()):
        if retirement.kind == "area":
            backlog_retire_area.lay(into, retirement.what, files)
            continue
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
        if retirement.kind == "term" and not taken and not _elemental(retirement, blocks):
            raise Refused("the layer %s holds no term %s to retire" % (retirement.area, retirement.what))
        files += [laid._rel("vocabulary", layer) for layer in taken]
