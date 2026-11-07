"""A verb's funs generated per frame (design call 5, `.shop/records/2026-11-07-verb-frames/design.md`): a verb's
subject, object and recipient are typed by the kinds its `Frame:` names, so a noun of another kind does not parse.

Each kind or actor T a frame names as a subject gets the category `<T>_Sb`, and as an object or a recipient `<T>_Ob`.
A noun fills it when its kind (or the actor) is T or a kind of T (`spec_frames.below`); a noun phrase with no kind
(a code or quoted literal, a quoted figure for a thing, an attribute's "the status of the item", "a status") fills any object slot, and a code any
subject slot. A verb `e` with its frame gives `e__Happens` / `e__HappensI` / `e__HappensTo` (a trigger, its
recipient after "to"), `e__Do` / `e__DoI` /
`e__DoTo` (a verb phrase) and, for the step grammar, `e__SDoes`, `e__SDoesNot`, `e__SDoesTo`, `e__SDoesI`,
`e__SDoesINot`.

The rest of the tools read a tree in its normal form (`normal`): the verb's clause as `Do e x`, `DoTo e x y`,
`DoI e`, `Happens s e x`, `HappensI s e`, `HappensTo s e x y` (and `SDoes s e x` ...), a subject as `ActorSubj` / `NPSubj`, an object as
the noun phrase it is (`k_item_toNP x`, `CodeNP c`, `Only x`). `typed` writes a normal tree back in the generated
funs, for GF to linearise.
"""
import spec_frames
import spec_lexicon
import spec_typed

SEP = "__"
STEPS = ("SDoes", "SDoesNot", "SDoesTo", "SDoesI", "SDoesINot")
# the normal form of each verb fun: (argument places of subject, object, recipient), the event placed after a subject
SHAPES = {"Happens": "so", "HappensI": "s", "HappensTo": "sor", "Do": "o", "DoI": "", "DoTo": "or", "SDoes": "so", "SDoesNot": "so",
          "SDoesTo": "sor", "SDoesI": "s", "SDoesINot": "s"}


def _type_id(name, ids, lex):
    """The GF id of a kind or an actor a frame names."""
    actors = {t.term: t for t in lex.of("actor")}
    return ids[actors[name].key] if name in actors else ids[("kind", name, ())]


def frames(lex):
    """{event id: (inf, s3, (subject type id, object type id or None, recipient type id or None))} of every verb
    whose frame reads."""
    ids, known, out = lex.ids(), spec_frames.names(lex), {}
    for t in lex.of("event"):
        found = spec_frames.frame(t, known)
        if found is None:
            continue
        inf, s3 = spec_typed.event_forms(t)
        out[ids[t.key]] = (inf, s3, tuple(_type_id(n, ids, lex) if n else None for n in found))
    return out


def members(lex):
    """{type id: ([kind ids at or below it], [actor ids at or below it])} for every kind and actor."""
    ids, below = lex.ids(), spec_frames.below(lex)
    actors = {t.term: ids[t.key] for t in lex.of("actor")}
    kinds = {t.term: ids[t.key] for t in lex.of("kind")}
    out = {}
    for name, under in below.items():
        tid = actors.get(name) or kinds.get(name)
        if tid:
            out[tid] = (sorted(kinds[n] for n in under if n in kinds), sorted(actors[n] for n in under if n in actors))
    return out


def _slots(found):
    """The type ids the frames name as subjects, and as objects or recipients."""
    subjects = sorted({f[2][0] for f in found.values()})
    objects = sorted({x for f in found.values() for x in f[2][1:] if x})
    return subjects, objects


def _fields(lex):
    """The noun phrases with no kind that fill an object slot, as spec_typed names them: an attribute's ("the status
    of X", "a status") and a count's ("the number of Xs"), each (fun, the category of its argument or None)."""
    ids, kinds, out = lex.ids(), lex.kind_names(), []
    for t in lex.of("attribute"):
        for kind in t.kinds:
            if kind in kinds and t.values:
                tid = ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], ids[("kind", kind, ())])
                out.append(("%s_Of" % tid, ids[("kind", kind, ())]))
    out = sorted(set(out)) + [("%s_NumberOf" % ids[t.key], "cn:" + ids[t.key]) for t in lex.of("kind")]
    words = sorted({t.term for t in lex.of("attribute")})
    return out + [("n_" + spec_lexicon.ident(w, "attribute")[2:], None) for w in words]


def modules(lex):
    """(cats, funs, lincats, lins) of the typed verb funs, for spec_typed's Typed module."""
    found, members_ = frames(lex), members(lex)
    actor_str = {lex.ids()[t.key]: spec_typed.gf_str(t.term) for t in lex.of("actor")}
    subjects, objects = _slots(found)
    cats, funs, lincats, lins = ["Field ;"], [], ["Field = NPr ;"], []
    for fun, kid in _fields(lex):
        arg = ("%s_CN -> " % kid[3:]) if kid and kid.startswith("cn:") else ("%s_NP -> " % kid if kid else "")
        funs.append("%s%sField : %sField ;" % (fun, SEP, arg))
        lins.append("%s%sField%s = %s ;" % (fun, SEP, " x" if kid else "", "%s x" % fun if kid else fun))
    for tid in subjects:
        cat, (kids, aids) = tid + "_Sb", members_.get(tid, ([], []))
        cats.append("%s ;" % cat)
        lincats.append("%s = Str ;" % cat)
        for kid in kids:
            funs.append("%s%s%s : %s_NP -> %s ;" % (cat, SEP, kid, kid, cat))
            lins.append("%s%s%s x = x.s ;" % (cat, SEP, kid))
        for aid in aids:
            funs.append("%s%s%s : %s ;" % (cat, SEP, aid, cat))
            lins.append("%s%s%s = %s ;" % (cat, SEP, aid, actor_str[aid]))
        funs.append("%s%sCode : Code -> %s ;" % (cat, SEP, cat))
        lins.append("%s%sCode c = c ;" % (cat, SEP))
    for tid in objects:
        cat, (kids, _) = tid + "_Ob", members_.get(tid, ([], []))
        cats.append("%s ;" % cat)
        lincats.append("%s = NPr ;" % cat)
        for kid in kids:
            funs.append("%s%s%s : %s_NP -> %s ;" % (cat, SEP, kid, kid, cat))
            lins.append("%s%s%s x = x ;" % (cat, SEP, kid))
        funs += ["%s%sOnly : %s -> %s ;" % (cat, SEP, cat, cat), "%s%sCode : Code -> %s ;" % (cat, SEP, cat),
                 "%s%sQuoted : Quoted -> %s ;" % (cat, SEP, cat), "%s%sField : Field -> %s ;" % (cat, SEP, cat),
                 "%s%sQuotedFor : Quoted -> NP -> %s ;" % (cat, SEP, cat)]
        lins += ['%s%sOnly x = {s = "only" ++ x.s ; p = Full ; n = x.n} ;' % (cat, SEP),
                 "%s%sCode c = np c ;" % (cat, SEP), "%s%sQuoted q = np q ;" % (cat, SEP),
                 "%s%sField x = x ;" % (cat, SEP), '%s%sQuotedFor q x = np (q ++ "for" ++ x.s) ;' % (cat, SEP)]
    for eid, (inf, s3, (s, o, r)) in sorted(found.items()):
        i, t = spec_typed.gf_str(inf), spec_typed.gf_str(s3)
        if o and r:
            funs += ["%s%sDoTo : %s_Ob -> %s_Ob -> VP ;" % (eid, SEP, o, r),
                     "%s%sHappensTo : %s_Sb -> %s_Ob -> %s_Ob -> Trig ;" % (eid, SEP, s, o, r)]
            lins += ['%s%sDoTo x y = %s ++ x.s ++ "to" ++ y.s ;' % (eid, SEP, i),
                     '%s%sHappensTo s x y = s ++ %s ++ x.s ++ "to" ++ y.s ;' % (eid, SEP, t)]
        elif o:
            funs += ["%s%sDo : %s_Ob -> VP ;" % (eid, SEP, o), "%s%sHappens : %s_Sb -> %s_Ob -> Trig ;" % (eid, SEP, s, o)]
            lins += ["%s%sDo x = %s ++ x.s ;" % (eid, SEP, i), "%s%sHappens s x = s ++ %s ++ x.s ;" % (eid, SEP, t)]
        else:
            funs += ["%s%sDoI : VP ;" % (eid, SEP), "%s%sHappensI : %s_Sb -> Trig ;" % (eid, SEP, s)]
            lins += ["%s%sDoI = %s ;" % (eid, SEP, i), "%s%sHappensI s = s ++ %s ;" % (eid, SEP, t)]
    return cats, funs, lincats, lins


def step_modules(lex):
    """(funs, lins) of the typed verb funs of the step grammar, for features_vocab_gf's StepsTyped module."""
    funs, lins = [], []
    for eid, (inf, s3, (s, o, r)) in sorted(frames(lex).items()):
        i, t = spec_typed.gf_str(inf), spec_typed.gf_str(s3)
        if o and r:
            funs.append("%s%sSDoesTo : %s_Sb -> %s_Ob -> %s_Ob -> Step ;" % (eid, SEP, s, o, r))
            lins.append('%s%sSDoesTo s x y = s ++ %s ++ x.s ++ "to" ++ y.s ;' % (eid, SEP, t))
        elif o:
            funs += ["%s%sSDoes, %s%sSDoesNot : %s_Sb -> %s_Ob -> Step ;" % (eid, SEP, eid, SEP, s, o)]
            lins += ["%s%sSDoes s x = s ++ %s ++ x.s ;" % (eid, SEP, t),
                     '%s%sSDoesNot s x = s ++ "does" ++ "not" ++ %s ++ x.s ;' % (eid, SEP, i)]
        else:
            funs += ["%s%sSDoesI, %s%sSDoesINot : %s_Sb -> Step ;" % (eid, SEP, eid, SEP, s)]
            lins += ["%s%sSDoesI s = s ++ %s ;" % (eid, SEP, t),
                     '%s%sSDoesINot s = s ++ "does" ++ "not" ++ %s ;' % (eid, SEP, i)]
    return funs, lins


def _normal_arg(t):
    head, _, tail = t[0].partition(SEP)
    if not tail:
        return normal(t)
    if head.endswith("_Sb"):
        if tail == "Code":
            return ("NPSubj", ("CodeNP", t[1]))
        return ("ActorSubj", (tail,)) if tail.startswith("a_") else ("NPSubj", (tail + "_toNP", normal(t[1])))
    if tail == "Only":
        return ("Only", _normal_arg(t[1]))
    if tail == "QuotedFor":
        return ("QuotedFor", t[1], normal(t[2]))
    if tail in ("Code", "Quoted"):
        return ("CodeNP" if tail == "Code" else "QuotedNP", t[1])
    if tail == "Field" and head.endswith("_Ob"):
        return _normal_arg(t[1])
    if head.endswith("_Ob"):
        return (tail + "_toNP", normal(t[1]))
    return (head,) + tuple(normal(a) for a in t[1:])      # an attribute's noun phrase, `<fun>__Field`


def normal(tree):
    """A parsed tree in its normal form: each typed verb fun written as the clause it is (see the module's doc)."""
    if not isinstance(tree, tuple):
        return tree
    eid, _, shape = tree[0].partition(SEP)
    if shape in SHAPES:
        args = [_normal_arg(a) for a in tree[1:]]
        if SHAPES[shape].startswith("s"):
            return (shape, args[0], (eid,)) + tuple(args[1:])
        return (shape, (eid,)) + tuple(args)
    return (tree[0],) + tuple(normal(a) for a in tree[1:])


def _sb(tid, s, meta):
    if s is meta or tid is None:
        return s
    if s[0] == "ActorSubj":
        return ("%s_Sb%s%s" % (tid, SEP, s[1][0]),)
    np = s[1]
    if np[0] == "CodeNP":
        return ("%s_Sb%sCode" % (tid, SEP), np[1])
    return ("%s_Sb%s%s" % (tid, SEP, np[0][:-len("_toNP")]), typed(np[1], meta=meta))


def _ob(tid, x, meta):
    if x is meta or tid is None:
        return x
    cat = tid + "_Ob" + SEP
    if x[0].endswith("_toNP"):
        return (cat + x[0][:-len("_toNP")], typed(x[1], meta=meta))
    if x[0] == "Only":
        return (cat + "Only", _ob(tid, x[1], meta))
    if x[0] == "QuotedFor":
        return (cat + "QuotedFor", x[1], typed(x[2], meta=meta))
    if x[0] in ("CodeNP", "QuotedNP"):
        return (cat + ("Code" if x[0] == "CodeNP" else "Quoted"), x[1])
    return (cat + "Field", (x[0] + SEP + "Field",) + tuple(typed(a, meta=meta) for a in x[1:]))


def typed(tree, found=None, meta=None):
    """A normal tree written back in the typed verb funs of `found` (`frames(lex)`); `meta` is a hole kept as it
    is (features_vocab's patterns)."""
    if not isinstance(tree, tuple) or tree is meta:
        return tree
    if tree[0] in SHAPES and found is not None:
        shape = SHAPES[tree[0]]
        args = list(tree[1:])
        event = args.pop(1 if shape.startswith("s") else 0)
        s, o, r = found[event[0]][2]
        out = []
        for role, arg in zip(shape, args):
            out.append(_sb(s, arg, meta) if role == "s" else _ob(o if role == "o" else r, arg, meta))
        return ("%s%s%s" % (event[0], SEP, tree[0]),) + tuple(out)
    return (tree[0],) + tuple(typed(a, found, meta) for a in tree[1:])


def unframed(tree, found, text):
    """The step of a verb with no frame (spec_steps' placeholder for a step no step words) as the step grammar
    wrote it before verbs were typed: its arguments by `text`, the verb as GF writes a fun it lacks, "[e]"; None
    for any other tree."""
    if not isinstance(tree, tuple) or tree[0] not in STEPS or tree[2][0] in found:
        return None
    words = [text(tree[1]), "does not" if tree[0].endswith("Not") else "", "[%s]" % tree[2][0]]
    words += [text(tree[3])] if len(tree) > 3 else []
    words += ["to", text(tree[4])] if len(tree) > 4 else []
    return " ".join(w for w in words if w)
