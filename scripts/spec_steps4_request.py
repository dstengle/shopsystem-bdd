"""A request with its parameters as Gherkin steps (the domain contract design, §5.1), beside spec_steps4, whose Reader
(`r`) it extends: the trigger's Givens and When.

- Givens: what the trigger says of its referents besides its event (spec_steps4's `given`), then each referent the
  event names not yet brought in (b263) and each thing a parameter names ("a tag t1", brought in at its first
  mention). A code or a value a parameter is given is said in the When, never in a Given.
- When: the trigger's event (`STrig`): a request with no parameter said its frame's act ("the person files the note
  n1"); with parameters `q_<verb>_<n>_<m>` under `<S>_Request`, the given ones after "with" and the absent ones after
  "without", in the order the line says them: "the person adds the note n1 with the text `milk` and without a
  priority", "the person labels the note n1 with the tag t1".
- "the p" a response names is the parameter's own noun phrase (`p_<p>_NP`, `np`).
"""
import re

import spec_lf_request
import spec_rgl
import spec_steps4_boxes
import spec_rgl_ops
from spec_lf_core import Atom

kid = spec_rgl.kid
EVENTS = ("event", spec_lf_request.PRED)
PARAMS = (spec_lf_request.PARAM, spec_lf_request.NOPARAM)


def trigger(r, part):
    """(the Givens, the When steps) of a trigger part: a When for each of its events (one act on each of "two Ks",
    b240, a When each), a request's with its parameters."""
    events = [i for i in part.body if isinstance(i, Atom) and i.pred in EVENTS]
    params = [i for i in part.body if isinstance(i, Atom) and i.pred in PARAMS]
    r.in_use = in_use(r, part.body, params)
    givens = [g for item in part.body if item not in events and item not in params for g in r.given(item)]
    givens += [g for x, (term, value) in r.in_use.items() for g in in_use_given(r, x, term, value)]
    when = []
    for event in events:
        fresh = made(r, event)
        r.known.update(fresh)
        givens += r.introduce(event)
        givens += [g for p in params if p.args[0] == event.args[0] for g in r.introduce(p)]
        subject, s, vp = r.clause(event)
        said = spec_lf_request.params(part.body, event.args[0])
        if event.pred == spec_lf_request.PRED and said:
            when.append(("STrig", (kid(subject) + "_Request", s, request(r, event, vp, said))))
        else:
            when.append(("STrig", (kid(subject) + "_Event", s, vp)))
        when[-1] = _fresh(r, when[-1], fresh)
    return givens, when


def made(r, event):
    """The referent a request's operation makes, its object when the operation's object is its `done →` outcome's
    and no parameter names it (b418): brought in by the When ("the person creates a checklist c2"), never a Given;
    [] of any other event or one brought in already."""
    if event.pred != spec_lf_request.PRED:
        return []
    op = r.vocab.operations.get(event.args[1])
    refs = [x[1] for x in event.args[4][1:] if len(x) == 2][:1]
    if op is None or not refs or not hasattr(refs[0], "origin") or refs[0] in r.known or not op.object \
            or op.object not in r.vocab.ancestors(refs[0].kind):
        return []
    done = any(o.kind == "done" and re.sub(r"\s*\(.*\)$", "", re.sub(r"^(?:the|a|an)\s+", "", o.phrase)).strip()
               == op.object for o in op.outcomes)
    named = any(p.type == "object" and op.object in p.targets for p in op.parameters)
    return refs if done and not named else []


def _fresh(r, tree, refs):
    """`tree` with each referent of `refs` said "a K n1" (`K_New`) in place of "the K n1" (`K_Inst`)."""
    names = {r.name(x) for x in refs}
    if isinstance(tree, tuple) and len(tree) == 3 and tree[0].endswith("_Inst") and tree[2][1:] and \
            tree[2][1] in names:
        return (tree[0][:-len("_Inst")] + "_New",) + tree[1:]
    return tuple(_fresh(r, t, refs) for t in tree) if isinstance(tree, tuple) and names else tree


def in_use(r, body, params):
    """{the referent whose value a parameter is given: (the attribute, the value made up)} of each parameter whose
    value is another thing's value of its attribute ("with the title of another checklist", param-of, b418): the
    owner brought in by a Given with the value, the When given the same value as a code."""
    out = {}
    values = {p.args[2] for p in params if p.pred == spec_lf_request.PARAM}
    for a in body:
        if isinstance(a, Atom) and a.pred == "attr" and a.args[2] in values:
            x, term, v = a.args
            r.known.add(v)
            t = next(t for t, _ in r.vocab.attributes if t.term == term)
            out[x] = (term, ("`%s`" % t.values[0]) if t.values else "`%s`" % r.name(v))
            r.__dict__.setdefault("values_in_use", {})[v] = out[x][1]
    return out


def in_use_given(r, x, term, value):
    """The Givens of a thing and its value of an attribute: "a checklist c1", "the title of the checklist c1 is
    `t1`"."""
    givens = [] if x in r.known else [(kid(x.kind) + "_Given", (kid(x.kind) + "_n",), ("NameLit", r.name(x)))]
    r.known.add(x)
    for n, (t, kinds) in enumerate(r.vocab.attributes, 1):
        k = next((k for k in kinds if k in r.vocab.ancestors(x.kind)), None)
        if t.term == term and k is not None:
            T = "t_%s_%d" % (spec_rgl.slug(term), n)
            owner = ("%s_Of_%s" % (T, kid(k)), r.np(x, k))
            if t.values:
                return givens + [("SCond", (T + "_IsOf", ("PPos",), owner,
                                            ("%s_v_%s" % (T, spec_rgl.slug(value.strip("`"))),)))]
            return givens + [("SCond", (T + "_IsCodeOf", ("PPos",), owner, ("CodeLit", value)))]
    raise spec_steps4_boxes.TraceError("no step of the %s of a %s" % (term, x.kind))


def request(r, event, vp, said):
    """The `q_<verb>_<n>_<m>` tree of a request's frame act `vp` with the parameters `said` ([(p, value or None)])."""
    op_id = event.args[1]
    head, n, m = vp[0].rsplit("_", 2)
    fun = "q_%s_%s_%s" % (head[len("e_"):-len("_action")], n, m)
    return (fun,) + tuple(vp[1:]) + (params(r, op_id, said),)


def params(r, op_id, said):
    """The `o_<O>_Params` tree of an operation's parameters `said`."""
    O = spec_rgl_ops.oid(op_id)
    types = {p.name: p for p in spec_rgl_ops.said(r.vocab.operations[op_id])}
    given = [one(r, O, types[p], v) for p, v in said if v is not None]
    absent = [(O + "_%s_%s" % (spec_rgl.slug(p), "NoFlag" if types[p].type == "flag" else "No"),)
              for p, v in said if v is None]
    if given and absent:
        return (O + "_WithWithout", _list(O, "P", given), _list(O, "A", absent))
    return (O + "_With", _list(O, "P", given)) if given else (O + "_Without", _list(O, "A", absent))


def _list(O, letter, items):
    tree = ("%s_%s1" % (O, letter), items[-1])
    for item in reversed(items[:-1]):
        tree = ("%s_%s2" % (O, letter), item, tree)
    return tree


def one(r, O, p, v):
    """The `o_<O>_P` tree of one parameter given."""
    P = "%s_%s" % (O, spec_rgl.slug(p.name))
    if v == spec_lf_request.ON:
        return (P + "_Flag",)
    if v == spec_lf_request.SOME:
        return (P + "_Some",)
    v = getattr(r, "values_in_use", {}).get(v, v)     # another thing's value, said as the code it was given (b418)
    if p.type == "values":
        return (P + "_Is", ("%s_v_%s" % (P, spec_rgl.slug(v.strip("`"))),))
    if p.type != "object":
        return (P + "_Is", ("CodeLit", v if isinstance(v, str) else v.value))
    k = next(t for t in p.targets if t in r.vocab.ancestors(v.kind))
    return ("%s_Is_%s" % (P, kid(k)), r.np(v, k))


def np(ref, slot):
    """The `K_NP` tree of "the p" a response names (`p_<p>_NP`), or None of any other referent."""
    if ref.kind != "parameter" or ref.origin != "constant":
        return None
    tree = ("p_%s_NP" % spec_rgl.slug(ref.value),)
    return ("k_parameter_Simple", tree) if slot == "parameter" else ("k_parameter_Up_%s" % kid(slot), tree)
