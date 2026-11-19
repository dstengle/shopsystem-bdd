"""A request's steps read back (the domain contract design, §5.2), beside features_vocab4: the templates of a When of a
request and of a Then of the request pack's acts, and a request's operation and parameters for its handler.

- `WhenRequests`: a trigger whose verb names an operation, with its parameters (`<S>_Request`) or none said; its term
  the operation's qualified id, its Call's `operation`, `params` (each (parameter, value) in the order the step says
  them: a code's or a value's text, a thing as the step says it, True of "a p" and of a flag, None of an absent one)
  and `without` (each absent parameter).
- A Then of an act of the request pack (`grammar/packs/request.md`): `ThenRefuses`, `ThenReturns`, `ThenReturnsNot`,
  `ThenCompletes`, `ThenFails`, `ThenNotifies`, `ThenKeeps`, keyed by its subject as `ThenPrints` is; "names" and
  "changes nothing" keep features_vocab4's `ThenDoes` and `ThenChangesNothing`. A context importing the CLI pack keeps
  `WhenRuns`, `ThenPrints` and the exits (the bootstrap of the domain contract's branch).
"""
import spec_rgl_ops

PACK = "grammar/packs/request.md"
THENS = {"refuse": "ThenRefuses", "return": "ThenReturns", "complete": "ThenCompletes", "fail": "ThenFails",
         "notify": "ThenNotifies", "keep": "ThenKeeps"}


def _verb(names, vp):
    fun = vp if isinstance(vp, str) else vp[0]
    if not fun.startswith(("e_", "q_")):
        return None
    return names.verbs[int(fun.rsplit("_", 2)[1])]


def template(names, tree):
    """(template, kind, attribute, term) of a request's When or a request pack's Then, or None of any other step."""
    fun, args = tree[0], tree[1:]
    if fun == "STrig":
        verb = _verb(names, args[0][2])
        if verb is not None and verb.term.operation:
            return "WhenRequests", None, None, verb.term.operation
        return None
    if not fun.endswith("_Does"):
        return None
    verb = _verb(names, args[2])
    if verb is None or verb.term.where != PACK or verb.term.term not in THENS:
        return None
    neg = args[0] == ("PNeg",)
    if neg and verb.term.term != "return":
        return None
    return THENS[verb.term.term] + ("Not" if neg else ""), None, None, None


def read(vocab, text, call, operation):
    """`call`'s operation, params and without, of a WhenRequests step; `text` writes a tree out."""
    call.operation, call.params, call.without = operation, [], []
    vp = call.tree[1][2]
    if isinstance(vp, str) or not vp[0].startswith("q_"):
        return
    funs = spec_rgl_ops.funs(vocab)
    for p, role, value in _walk(funs, vp[-1]):
        if role in ("No", "NoFlag"):
            call.params.append((p, None))
            call.without.append(p)
        elif role in ("Some", "Flag"):
            call.params.append((p, True))
        elif value[0] == "CodeLit":
            call.params.append((p, value[1]))
        elif value[0] in funs:
            call.params.append((p, "`%s`" % funs[value[0]][2][2:]))
        else:
            call.params.append((p, text(value)))


def _walk(funs, tree):
    name, a = (tree, ()) if isinstance(tree, str) else (tree[0], tree[1:])
    found = funs.get(name)
    if found is not None and found[2] in spec_rgl_ops.ROLES:
        return [(found[1], found[2], a[0] if a else None)]
    return [x for sub in a for x in _walk(funs, sub)]
