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
import spec_lf_request
import spec_rgl
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
    givens = [g for item in part.body if item not in events and item not in params for g in r.given(item)]
    when = []
    for event in events:
        givens += r.introduce(event)
        givens += [g for p in params if p.args[0] == event.args[0] for g in r.introduce(p)]
        subject, s, vp = r.clause(event)
        said = spec_lf_request.params(part.body, event.args[0])
        if event.pred == spec_lf_request.PRED and said:
            when.append(("STrig", (kid(subject) + "_Request", s, request(r, event, vp, said))))
        else:
            when.append(("STrig", (kid(subject) + "_Event", s, vp)))
    return givens, when


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
    if p.type == "values":
        return (P + "_Is", ("%s_v_%s" % (P, spec_rgl.slug(v.strip("`"))),))
    if p.type != "object":
        return (P + "_Is", ("CodeLit", v.value))
    k = next(t for t in p.targets if t in r.vocab.ancestors(v.kind))
    return ("%s_Is_%s" % (P, kid(k)), r.np(v, k))


def np(ref, slot):
    """The `K_NP` tree of "the p" a response names (`p_<p>_NP`), or None of any other referent."""
    if ref.kind != "parameter" or ref.origin != "constant":
        return None
    tree = ("p_%s_NP" % spec_rgl.slug(ref.value),)
    return ("k_parameter_Simple", tree) if slot == "parameter" else ("k_parameter_Up_%s" % kid(slot), tree)
