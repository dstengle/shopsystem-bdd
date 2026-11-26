"""The Thens of laying's scenarios of what a lay keeps of an item's model lines, terms and operation tables (r28-r41,
b746), moved from batches' (batches_handlers_adapter's, _new_op's, _restate's, _element's, _lone's, _move's,
_retire's and _retire_both's checks), `work_queue_world.local`s tried before laying_handlers' own, over
laying_handlers_model's worlds: each reads a file of the workspace the lay done changed (`kept`). The adapter contract
holding the item's table once, or no table of the operation withheld and it under `[unexposed]`, or the table of
`notes.pin` written from the model; notes' model holding the restating line once in place of the element it restates;
labels' model holding `object tag` and notes' importing labels; notes' layer holding the moved term and shared's not;
the area's file without what the item retires."""
import re
import sys

M = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers_model.py"))   # loaded before this
L, world, parts = M.L, M.world, sys.modules["shop_world_four"].parts
RESTATING = ("g32", "g33", "g34", "g35")


def kept(step, rel):
    """The lines of the workspace's file `rel`, which the lay done changed."""
    w = world(step)
    assert w["response"].outcome == "done" and rel in w["response"].content["changed"], (step.text, rel, w["response"])
    return (w["tree"] / rel).read_text().split("\n")


def _contract(step, tag):
    """The adapter contract as each group's item leaves it."""
    text = "\n".join(kept(step, M.CONTRACT))
    if tag in ("g28", "g31"):
        assert M.table("o1") in text and text.count('[operations."%s"]' % M.OPERATION) == 1, text
    elif tag == "g29":
        assert '[operations."%s"' % M.OPERATION not in text, text
        assert re.search(r'(?ms)^\[unexposed\].*"%s"' % re.escape(M.OPERATION), text), text
    else:
        assert text.count('[operations."notes.pin"]') == 1, text
        assert 'command = "notes pin"' in text and '[operations."notes.pin".parameters]' in text, text


def _restated(step, tag):
    """notes' model holds the item's line once in place of the element it restates."""
    lines = kept(step, M.MODEL)
    if tag == "g32":
        assert [x for x in lines if x.startswith("  operation archive(")] == [M.ARCHIVED[1]], lines
    elif tag == "g33":
        at = lines.index(M.HEADER)
        end = next((i for i in range(at + 1, len(lines)) if not lines[i].startswith(" ")), len(lines))
        assert lines.count(M.HEADER) == 1 and tuple(lines[at:end]) == M.NOTE and M.NOTE_OLD not in lines, lines
    else:
        old, new = M.LONE[tag]
        head = old.partition(":")[0] if tag == "g34" else "actor the person"
        assert [x for x in lines if x.startswith(head)] == [new] and old not in lines, lines


def _moved(step, tag):
    """The area holds what the item moves there, and the area it moved from does not."""
    if tag == "g36":
        target, source = kept(step, M.LABELS), kept(step, M.MODEL)
        assert target.count("object tag") == 1 and "  relations: of → note (one)" in target, target
        assert "object tag" not in source and "imports: [labels]" in source, source
    else:
        target, source = kept(step, M.NOTES), kept(step, M.SHARED)
        assert target.count(M.PERSON) == 1 and M.PERSON not in source, (target, source)


def _retired(step, tag):
    """The area's file without what the item retires."""
    rel, line = M.RETIRES[tag][1]
    assert line not in kept(step, rel), (step.text, rel)


def then(step):
    """The Thens of these groups: the laying service keeps the adapter contract, the domain model, the model line or
    the area, and each holds or does not hold what the group's item says; `does not keep the operation table o2`, the
    withheld operation's."""
    tag = M.group(step)
    if tag is None or "tree" not in world(step):
        return False
    kinds = [k for k, _ in parts(step)]
    if tag in ("g28", "g29", "g30", "g31"):
        _contract(step, tag)
    elif tag in RESTATING:
        _restated(step, tag)
    elif tag in ("g36", "g37", "g38"):
        _moved(step, tag)
    elif step.template.endswith("Not") or kinds[-1] == "area":
        _retired(step, tag)
    else:
        raise AssertionError("laying_handlers_model_then takes no Then %s %s: %s" % (step.template, step.term,
                                                                                      step.text))


for _template in ("ThenDoes", "ThenDoesNot"):
    L.W.local(_template)(then)
