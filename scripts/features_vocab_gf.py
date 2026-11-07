"""The generated `StepsTyped` module of a lexicon (design §14.1, design-r2 §4.4): for each kind its instance mention
and Given templates, for each attribute slot its Given, and each verb's steps typed by its frame (spec_typed_verbs),
with the vocabulary's rows of them (`verb_rows`). A relation between two instances has no fun here: its step is the
`SAtom` of its `## Relations` row's clause (`rel_<k1>_<word>_<k2>_Atom`, design-r2 §4.4), read as GivenR or ThenR. features_vocab compiles it over `grammar/Steps.gf`."""
import spec_typed
import spec_typed_verbs


def attributes(lex, ids):
    """(entry, kind, attribute id) of each typed attribute slot, as spec_typed builds them."""
    kinds, seen = lex.kind_names(), set()
    for t in lex.of("attribute"):
        for kind in t.kinds:
            if kind not in kinds or not t.values or any((kind, v) in seen for v in t.values):
                continue
            seen |= {(kind, v) for v in t.values}
            yield t, kind, ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], ids[("kind", kind, ())])


def modules(lex):
    """{file name: GF source} of StepsTyped.gf and StepsTypedEng.gf for a lexicon."""
    ids, funs, lins = lex.ids(), [], []
    kinds = {t.term: t for t in lex.of("kind")}
    for k, t in sorted(kinds.items()):
        kid, sg = ids[t.key], spec_typed.gf_str(t.term)
        funs += ["%s_Inst : Name -> %s_NP ;" % (kid, kid), "%s_Given, %s_HoldsBlock : Name -> Step ;" % (kid, kid),
                 "%s_HoldsText : Name -> Quoted -> Step ;" % kid]
        lins += ['%s_Inst n = np ("the" ++ %s ++ n) ;' % (kid, sg), "%s_Given n = art ++ %s ++ n ;" % (kid, sg),
                 '%s_HoldsBlock n = "the" ++ %s ++ n ++ "holds" ++ ":" ;' % (kid, sg),
                 '%s_HoldsText n q = "the" ++ %s ++ n ++ "holds" ++ q ;' % (kid, sg)]
    for t, kind, tid in attributes(lex, ids):
        funs.append("%s_Given : Name -> %s_V -> Step ;" % (tid, tid))
        lins.append('%s_Given n v = art ++ %s ++ n ++ "that" ++ "is" ++ v ;' % (tid, spec_typed.gf_str(kind)))
    verb_funs, verb_lins = spec_typed_verbs.step_modules(lex)
    funs, lins = funs + verb_funs, lins + verb_lins
    funs, lins = ("".join("    %s\n" % x for x in xs) for xs in (funs, lins))
    return {"StepsTyped.gf": "abstract StepsTyped = Steps ** {\n  flags startcat = Step ;\n  fun\n%s}\n" % funs,
            "StepsTypedEng.gf": "concrete StepsTypedEng of StepsTyped = StepsEng ** {\n  lin\n%s}\n" % lins}


def verb_rows(vocab, np, name, meta, then):
    """features_vocab's rows of the verbs: each verb's trigger and Thens with any object (`np`), and with the
    instance (`name`) of each kind its frame takes as its object; `then` maps a step fun to its template."""
    out, members, M = [], spec_typed_verbs.members(vocab.lex), meta
    for eid, (_, _, (_, o, r)) in sorted(vocab.frames.items()):
        e = (eid,)
        if not o:
            out += [("when", "WhenHappens", None, None, ("STrig", ("HappensI", M, e)))]
            out += [("then", then[f], None, None, (f, M, e)) for f in ("SDoesI", "SDoesINot")]
            continue
        if r:
            out.append(("then", "ThenDoesTo", None, None, ("SDoesTo", M, e, np, np)))
            continue
        out += [("then", then[f], None, None, (f, M, e, np)) for f in ("SDoes", "SDoesNot")]
        for kid in members.get(o, ([], []))[0]:
            kind, inst = vocab.owner[kid][1], (kid + "_toNP", (kid + "_Inst", name))
            out.append(("when", "WhenHappens", kind, None, ("STrig", ("Happens", M, e, inst))))
            out += [("then", then[f], kind, None, (f, M, e, inst)) for f in ("SDoes", "SDoesNot")]
    return out
