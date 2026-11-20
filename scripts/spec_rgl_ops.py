"""Operations with parameters in grammar 4 (the domain contract design, §5.1): for each verb naming an operation of a
service (spec_vocabulary_terms' `operation`), the request with its parameters, generated over the verb's frames.

- A verb naming an operation keeps its frame's act (spec_rgl's `e_<verb>_action_<n>_<m>`): "the person adds a note",
  a request with no parameter said. With its parameters it is `q_<verb>_<n>_<m> : <the frame's arguments> ->
  o_<O>_Params -> <S>_Req`, a request's verb phrase, which only a trigger takes (`<S>_Request : <S>_Arg -> <S>_Req ->
  Trig`): "the person adds a note with the text `milk` and the priority `high`" (session's call: a Params list is said
  in a trigger only; a history Given of a request is not generated yet).
- `o_<O>_Params` is "with" a list of given parameters (`o_<O>_With`), "without" a list of absent ones (`o_<O>_Without`:
  "without a text and a priority", each absent) or both (`o_<O>_WithWithout`: "with the text `a` and without a
  priority"); a list's members joined by "and" (`o_<O>_P1`, `_P2`, `_A1`, `_A2`).
- Per parameter p of O, but the one naming O's object (its slot in the frame): a value of p's values
  `o_<O>_<p>_Is : o_<O>_<p>_Val -> o_<O>_P` ("the priority `high`", each value `o_<O>_<p>_v_<value>`); a text,
  number, time or version a code (`o_<O>_<p>_Is : Code -> o_<O>_P`, "the text `milk`"); an object its noun phrase
  (`o_<O>_<p>_Is_<K> : K_NP -> o_<O>_P`, "a tag", "the tag t1"); "a p" given with no value said (`_Some`) and absent
  (`_No`, after "without"); a flag "the p" given (`_Flag`) or absent (`_NoFlag`).
- param-of (b418, design-decision 0110): a parameter p that is not a flag nor an object and is the word of an
  attribute T takes "the T of <np>" as its value (`o_<O>_<p>_Of_<T> : <T>_NP -> o_<O>_P`, "the title of another
  checklist"), role "Is": its value is the image's referent, as a thing's is.
- Per parameter name of no object, "the p" a noun phrase of the request pack's kind `parameter` (`p_<p>_NP`), which a
  response names: "refuse the request and name the text". None whose name is a kind's noun or an actor.

`funs(vocab)` gives each generated fun's (operation, parameter, role), which the logical form (spec_lf_request) and the
steps (spec_steps4_request) read the trees by.
"""
import spec_rgl

ROLES = ("Is", "Some", "No", "Flag", "NoFlag")
_funs = {}


def oid(op):
    return "o_" + spec_rgl.slug(op)


def article(word):
    return ("an " if word[:1] in "aeiou" and not word.startswith(("uni", "use", "user")) else "a ") + word


def said(op):
    """The parameters of an operation (a domain_model Operation) said after its object: every one but the first
    naming the object it acts on."""
    out, skipped = [], False
    for p in op.parameters:
        if not skipped and p.type == "object" and op.object in p.targets:
            skipped = True
            continue
        out.append(p)
    return out


def parameter_nps(vocab):
    """The parameter names a response may name ("the text"): of no object, no kind's noun or actor, in order."""
    if "parameter" not in vocab.kinds:
        return []
    names = [p.name for op in vocab.operations.values() for p in said(op) if p.type != "object"]
    nouns = {w for pair in vocab.nouns.values() for w in pair} | set(vocab.kinds) | {t for t, _ in vocab.actors}
    return [n for n in dict.fromkeys(names) if n not in nouns]


def funs(vocab):
    """{fun name: (operation id, parameter name or None, role)} of the funs `requests` generates for `vocab`."""
    key = id(vocab)
    if key not in _funs:
        _funs.clear()
        out = {}
        for op_id, op in vocab.operations.items():
            O = oid(op_id)
            for p in said(op):
                P = "%s_%s" % (O, spec_rgl.slug(p.name))
                out.update({"%s_%s" % (P, r): (op_id, p.name, r) for r in ROLES})
                out.update({"%s_Is_%s" % (P, spec_rgl.kid(k)): (op_id, p.name, "Is") for k in p.targets})
                out.update({"%s_v_%s" % (P, spec_rgl.slug(v)): (op_id, p.name, "v:" + v) for v in p.values})
                out.update({"%s_Of_%s" % (P, T): (op_id, p.name, "Is") for T in attributes(vocab, p)})
        out.update({"p_%s_NP" % spec_rgl.slug(n): (None, n, "NP") for n in parameter_nps(vocab)})
        _funs[key] = (vocab, out)
    return _funs[key][1]


def attributes(vocab, p):
    """The ids `t_<T>_<n>` of the attribute entries whose word is the name of parameter p (of no flag or object)."""
    if p.type in ("flag", "object"):
        return []
    return ["t_%s_%d" % (spec_rgl.slug(t.term), n) for n, (t, _) in enumerate(vocab.attributes, 1) if t.term == p.name]


def _params(w, op_id, op, vocab):
    O = oid(op_id)
    for suffix in ("P", "A", "Ps", "As", "Params"):
        w.cat("%s_%s" % (O, suffix), "{s : Str}")
    w.fun(O + "_P1", "%s_P -> %s_Ps" % (O, O), "{s = p.s}", "p")
    w.fun(O + "_P2", "%s_P -> %s_Ps -> %s_Ps" % (O, O, O), '{s = p.s ++ "and" ++ l.s}', "p l")
    w.fun(O + "_A1", "%s_A -> %s_As" % (O, O), "{s = p.s}", "p")
    w.fun(O + "_A2", "%s_A -> %s_As -> %s_As" % (O, O, O), '{s = p.s ++ "and" ++ l.s}', "p l")
    w.fun(O + "_With", "%s_Ps -> %s_Params" % (O, O), '{s = "with" ++ l.s}', "l")
    w.fun(O + "_Without", "%s_As -> %s_Params" % (O, O), '{s = "without" ++ l.s}', "l")
    w.fun(O + "_WithWithout", "%s_Ps -> %s_As -> %s_Params" % (O, O, O),
          '{s = "with" ++ l.s ++ "and" ++ "without" ++ m.s}', "l m")
    for p in said(op):
        P, the = "%s_%s" % (O, spec_rgl.slug(p.name)), spec_rgl.s("the " + p.name)
        if p.type == "flag":
            w.fun(P + "_Flag", O + "_P", "{s = %s}" % the)
            w.fun(P + "_NoFlag", O + "_A", "{s = %s}" % the)
            continue
        w.fun(P + "_No", O + "_A", "{s = %s}" % spec_rgl.s(article(p.name)))
        if p.type == "object":
            for k in p.targets:
                if k in vocab.kinds:
                    w.fun("%s_Is_%s" % (P, spec_rgl.kid(k)), "%s_NP -> %s_P" % (spec_rgl.kid(k), O),
                          "{s = (mkUtt x).s}", "x")
            continue
        w.fun(P + "_Some", O + "_P", "{s = %s}" % spec_rgl.s(article(p.name)))
        for T in (T for T in attributes(vocab, p) if T + "_NP" in w.cats):     # param-of (b418)
            w.fun("%s_Of_%s" % (P, T), "%s_NP -> %s_P" % (T, O), "{s = (mkUtt x).s}", "x")
        if p.type == "values":
            w.cat(P + "_Val", "{s : Str}")
            for v in p.values:
                w.fun("%s_v_%s" % (P, spec_rgl.slug(v)), P + "_Val", "{s = %s}" % spec_rgl.s("`%s`" % v))
            w.fun(P + "_Is", "%s_Val -> %s_P" % (P, O), "{s = %s ++ v.s}" % the, "v")
        else:
            w.fun(P + "_Is", "Code -> %s_P" % O, "{s = %s ++ c.s}" % the, "c")


def requests(w, vocab):
    """The requests with their parameters of every verb naming an operation, and the parameters' noun phrases."""
    subjects = []
    for n, v in enumerate(vocab.verbs, 1):
        op = vocab.operations.get(v.term.operation)
        if op is None or not said(op):
            continue
        O = oid(v.term.operation)
        if O + "_Params" not in w.cats:
            _params(w, v.term.operation, op, vocab)
        for m, (subject, pieces) in enumerate(v.frames, 1):
            S = spec_rgl.kid(subject)
            w.cat(S + "_Req", "VP")
            args, lin = spec_rgl.frame_lin(spec_rgl.verb(v.term), pieces)
            typ = " -> ".join(["%s_Arg" % spec_rgl.kid(k) for k in args] + [O + "_Params", S + "_Req"])
            names = " ".join("x%d" % (i + 1) for i in range(len(args)))
            w.fun("q_%s_%d_%d" % (spec_rgl.slug(v.term.term), n, m), typ,
                  "mkVP (%s) (ParadigmsEng.mkAdv ps.s)" % lin, (names + " ps").strip())
            subjects.append(S)
    for S in dict.fromkeys(subjects):
        w.fun(S + "_Request", "%s_Arg -> %s_Req -> Trig" % (S, S), "mkS (mkCl x v)", "x v")
    for name in parameter_nps(vocab):
        w.fun("p_%s_NP" % spec_rgl.slug(name), "k_parameter_NP0", "actor %s" % spec_rgl.s("the " + name))
