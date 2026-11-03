"""The generated `StepsTyped` module of a lexicon (design §14.1, design-r2 §4.4): for each kind its instance mention
and Given templates, and for each attribute slot its Given. A relation between two instances has no fun here: its
step is the `SAtom` of its `## Relations` row's clause (`rel_<k1>_<word>_<k2>_Atom`, design-r2 §4.4), read as
GivenR or ThenR. features_vocab compiles it over `grammar/Steps.gf`."""
import spec_typed


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
    funs, lins = ("".join("    %s\n" % x for x in xs) for xs in (funs, lins))
    return {"StepsTyped.gf": "abstract StepsTyped = Steps ** {\n  flags startcat = Step ;\n  fun\n%s}\n" % funs,
            "StepsTypedEng.gf": "concrete StepsTypedEng of StepsTyped = StepsEng ** {\n  lin\n%s}\n" % lins}
