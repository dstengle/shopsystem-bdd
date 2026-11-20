"""A response's referents brought in by a Given before the When, beside spec_steps4, whose Reader (`r`) it extends:
each referent of a response with "two Ks" (b273); the things of a row `K1 | in | K2` of the response whose K1 no
act names, as "print a worktree that holds a file" says them (b286), a K1 an act names ("write a file that a
directory holds") being the act's own; and a thing a response names by its owner, a thing of the pre-state ("return
the items of the checklist", a row `K1 | of | K2` whose K2 the While part, the trigger or a kind's `This:` gives
("the push of this command", b421), K1 named only by acts that make nothing, the packs' verbs that give a thing
out: `CONVEY`), with its row, which the line presupposes, said by a Given and no Then (b416); a K1 an act keeps or
writes is that act's own, its row a Then."""
import spec_lf_distinct
from spec_lf_core import Atom

# the packs' verbs whose act gives a thing out and makes nothing: the CLI pack's print, the request pack's return and
# notify
CONVEY = ("print", "return", "notify")
# the origins of a referent of the pre-state an owner may be: the While part's, the trigger's and a `This:` (b421)
PRESUPPOSED = ("while", "trigger", "indexical")


def bring_response(r, part):
    """The response's body with the atoms said by a Given here left out, each referent brought in."""
    if any(isinstance(i, Atom) and i.pred == spec_lf_distinct.PRED for i in part.body):
        for x in part.refs:
            r.bring_in(x)
    events = [z[1] for i in part.body if isinstance(i, Atom) and i.pred == "event" for z in i.args[-1] if len(z) == 2]
    for atom in (i for i in part.body if isinstance(i, Atom) and i.pred == "rel" and i.args[0] == "in"):
        if all(x in part.refs for x in atom.args[1:]) and atom.args[1] not in events:     # a held thing only described
            for x in atom.args[1:]:
                r.bring_in(x)
    owned = [i for i in part.body if owner(part, i)]
    for atom in owned:
        r.bring_in(atom.args[1])
        r.brought.extend(r.given(atom))
    return [i for i in part.body if i not in owned]


def owner(part, item):
    """True for a row `K1 | of | K2` of a response's own K1 and a K2 of the pre-state, a While, trigger or
    indexical referent (b421), K1 named by an act that conveys it and by no other act."""
    if not (isinstance(item, Atom) and item.pred == "rel" and item.args[0] == "of" and item.args[1] in part.refs
            and getattr(item.args[2], "origin", None) in PRESUPPOSED and item.args[2] not in part.refs):
        return False
    verbs = {i.args[1] for i in part.body if isinstance(i, Atom) and i.pred == "event"
             and any(len(z) == 2 and z[1] == item.args[1] for z in i.args[-1])}
    return bool(verbs) and verbs <= set(CONVEY)
