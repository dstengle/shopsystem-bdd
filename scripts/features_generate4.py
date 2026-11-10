"""`features generate`'s scenario of a codified-2 group (the CNL 4 design, I14a): its example data, then its
requirements' steps read off their logical forms by spec_steps4 and written in the step grammar 4 (spec_rgl_steps),
each Then a universal condition entails left out with a comment naming it (`entailed`).

An act is entailed when spec_entail answers it forced and a universal condition is among its premises; the comment
names each such condition, and the definition of refuse when the condition's trigger is a refusal and the line's is
not (the CLI pack's bridge: an error exit on a run is a refusal). Other lines that entail it are `model logic`'s L8,
not the generator's: their Then stays. A group with a construct no step words is skipped, as features_generate skips
one of codified-1.
"""
import sys

import spec_entail
import spec_lf
import spec_read_given
import spec_rgl_steps
import spec_steps4
from spec_solve_pairs import order

ALLOWED = {"given": ("SCond", "_Given", "_HoldsBlock", "_HoldsText")}
_entailed = {}


class GenerateError(Exception):
    """A codified-2 group that cannot be written: an example line that is no Given of the step grammar 4."""


def entailed(root, ctx):
    """{requirement id: {act number: the premises that entail it, in words}}, once per context read."""
    if id(ctx) in _entailed:
        return _entailed[id(ctx)][1]
    facts = list(ctx.domain) + [f for s in ctx.statements for f in ctx.facts[s.id]]
    bridge = spec_entail.refuse_defined(root)
    universal = {s.id for s in ctx.statements if s.capability is None}
    refusers = {s.id for s in ctx.statements if any(",does,e_refuse," in f for f in ctx.facts[s.id]
                                                    if f.startswith("trig("))}
    out = {}
    for (line, act), premises in spec_entail.entailed(facts, bridge).items():
        said = [u + (" through the definition of refuse" if bridge and u in refusers and line not in refusers else "")
                for u in sorted(set(premises) & universal, key=order)]
        if said:
            out.setdefault(line, {})[int(act)] = " and ".join(said)
    _entailed[id(ctx)] = (ctx, out)
    return out


def _example(root, gid, group):
    """The (keyword, text, block) lines of a group's example data, each a Given of the step grammar 4."""
    out = []
    for text, block in group.given:
        if not spec_read_given.example(text, block):
            print("features generate: %s: the given line %r is not example data; left out" % (gid, text),
                  file=sys.stderr)
            continue
        try:
            trees = [t for t in spec_rgl_steps.trees(root, text) if t[0].endswith(ALLOWED["given"])]
        except spec_rgl_steps.StepError as err:
            raise GenerateError("%s: the given line %s" % (gid, err))
        if not trees:
            raise GenerateError("%s: the given line %r is no Given" % (gid, text))
        out.append(("given", spec_rgl_steps.text(spec_rgl_steps.load(root)[1], trees[0]), block))
    return out


def lines(root, ctx, cap, group, skipped=None):
    """The (keyword, text, block) lines of each scenario of a codified-2 group (a comment's keyword "#"), one a case of
    its `or` boxes (spec_steps4's `cases`), or None for a group with a construct no step words (its reason kept in
    `skipped`, by group id, when given)."""
    gid = "%s#%s" % (cap.name, group.id)
    mine = [s for s in ctx.statements if s.group == gid]
    if not mine:
        return None
    vocab, gram = spec_rgl_steps.load(root)
    try:
        forms = [(s.id, spec_lf.form(vocab, s.tree)) for s in mine]
        # a permission obliges nothing, and a necessity's scenario waits on its decision's route (I17): neither has a
        # step, and a group of only such lines has no scenario, as a logic-only group of codified-1 (D9)
        forms = [(i, f) for i, f in forms if f.modality == "shall"]
        if not forms:
            return None
        found = spec_steps4.cases(vocab, forms, entailed(root, ctx))
    except (spec_steps4.TraceError, ValueError) as err:
        print("features generate: %s: no scenario: %s" % (gid, err), file=sys.stderr)
        if skipped is not None:
            skipped[gid] = str(err)
        return None
    example = _example(root, gid, group)
    return [example + [(k, t if k == "#" else spec_rgl_steps.text(gram, t), None) for k, t in steps]
            for steps in found]
