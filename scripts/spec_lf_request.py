"""A request with its parameters in the logical form (the domain contract design, §5.1; beside spec_lf_option, the CLI
pack's run, which stays until the old reading is deleted), one translation of spec_rgl_ops' funs in each place a line
is read.

- the form: a trigger whose verb names an operation is the atom `request(e, O, subject: actor, object: x)` (O the
  operation's qualified id), and each parameter the line says `param(e, p, v)` (v a value, a code's referent, a
  thing's referent, `some` of "with a p", `on` of a flag) or `noparam(e, p)` ("without a p", "without the p")
  (`vp`, `frame`, `expand`); "the p" a response names a constant of the request pack's kind `parameter` (`np`);
  "the request" is the request the trigger makes, the pack's `This:` (R2's indexical, spec_lf_read's `the`). An act of
  a response keeps its event atom: a request is said in a trigger only.
- its lines in `model parse --form` (`show`).
- the steps' reading of a When step's request (`read`: the operation, each parameter given with its value or True,
  each absent), which features_vocab4's `WhenRequests` gives a handler.
The check's facts of a request are plan 3's: until then spec_lf_facts reads a request as the event of its verb, its
parameters left out (`as_events`, the bootstrap of the domain contract's branch).
"""
from dataclasses import replace

import spec_rgl_ops
from spec_lf_core import Atom, Box

PRED, PARAM, NOPARAM = "request", "param", "noparam"
SOME, ON = "some", "on"


# --- the form ------------------------------------------------------------------------------------------------------
def operation(st, n):
    """The operation verb n names when a trigger is being read, else None."""
    return st.names.verbs[n].term.operation or None if st.origin == "trigger" else None


def frame(st, n, e, verb, sense, roles):
    """The request atom of verb n's frame in a trigger (its parameters added by `vp`), or None."""
    op = operation(st, n)
    return Atom(PRED, (e, op, verb, sense, roles, ())) if op else None


def _walk(st, tree, out):
    """The (parameter, role, value tree) of each parameter a Params tree says, in order (a nullary fun a string)."""
    name, a = (tree, ()) if isinstance(tree, str) else (tree[0], tree[1:])
    found = spec_rgl_ops.funs(st.vocab).get(name)
    if found is not None and found[2] in spec_rgl_ops.ROLES:
        out.append((found[1], found[2], a[0] if a else None))
        return out
    for x in a:
        _walk(st, x, out)
    return out


def _thing(v):
    """True of a parameter's noun phrase, False of its code or value."""
    name = v if isinstance(v, str) else v[0]
    return name != "CodeLit" and not (name.startswith("o_") and "_v_" in name)


def vp(st, tree, nps, frame_atom):
    """(noun phrases, build) of a `q_<verb>_<n>_<m>` request with its parameters, or None of any other fun: the frame's
    arguments, then each parameter's thing, placed by apply; `frame_atom(n, m, slots)` the frame's atom."""
    name = nps.fun(tree)
    if not name.startswith("q_"):
        return None
    n, m = (int(x) for x in name.rsplit("_", 2)[1:])
    a = nps.args(tree)
    params = _walk(st, a[-1], [])
    args = [nps.np(st, x) for x in a[:-1]]
    things = [nps.np(st, v) for _, role, v in params if role == "Is" and _thing(v)]

    def build(s, refs):
        refs = list(refs)
        atom = frame_atom(st, n, m, [s] + refs[:len(args)])
        given, it = [], iter(refs[len(args):])
        for p, role, v in params:
            if role in ("No", "NoFlag"):
                given.append((p, None))
            elif role == "Some":
                given.append((p, SOME))
            elif role == "Flag":
                given.append((p, ON))
            elif nps.fun(v) == "CodeLit":
                given.append((p, nps.code(st, "thing", v).ref))
            elif not _thing(v):
                given.append((p, "`%s`" % spec_rgl_ops.funs(st.vocab)[nps.fun(v)][2][2:]))
            else:
                given.append((p, next(it)))
        return Atom(PRED, atom.args[:5] + (tuple(given),))
    return args + things, build


def expand(conds):
    """`conds` with each request atom made the request and its parameters' atoms, in boxes too."""
    out = []
    for c in conds:
        if isinstance(c, Atom) and c.pred == PRED and len(c.args) == 6:
            e, params = c.args[0], c.args[5]
            out.append(Atom(PRED, c.args[:5]))
            out += [Atom(NOPARAM, (e, p)) if v is None else Atom(PARAM, (e, p, v)) for p, v in params]
        elif isinstance(c, Box):
            out.append(replace(c, body=tuple(expand(c.body)),
                               scope=replace(c.scope, body=tuple(expand(c.scope.body))) if c.scope else None))
        else:
            out.append(c)
    return out


def np(st, name):
    """The constant "the p" names (`p_<p>_NP`), or None of any other fun."""
    if not name.startswith("p_"):
        return None
    found = spec_rgl_ops.funs(st.vocab).get(name)
    return st.constant("parameter", found[1], "constant") if found else None


def show(atom, term):
    if atom.pred == PRED:
        e, op, _, _, roles = atom.args
        return "%s(%s)" % (PRED, ", ".join([e, op] + [term(r) for r in roles]))
    if atom.pred == PARAM:
        e, p, v = atom.args
        return "%s(%s, %s, %s)" % (PARAM, e, p, term(v))
    return "%s(%s, %s)" % (NOPARAM, atom.args[0], atom.args[1])


def params(body, e):
    """[(parameter, value or None)] of the request whose event is `e`, in the order the line says them."""
    return [(a.args[1], a.args[2] if a.pred == PARAM else None) for a in body
            if isinstance(a, Atom) and a.pred in (PARAM, NOPARAM) and a.args[0] == e]


def as_events(part):
    """The trigger `part` with each request its verb's event and no parameter atom (the bootstrap's facts)."""
    body = tuple(Atom("event", (a.args[0],) + a.args[2:]) if isinstance(a, Atom) and a.pred == PRED else a
                 for a in part.body if not (isinstance(a, Atom) and a.pred in (PARAM, NOPARAM)))
    return replace(part, body=body)
