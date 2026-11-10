"""The noun phrases of grammar 4 (the CNL 4 design, calls 1 and 4; I8), generated into the module `Context` beside
spec_rgl's kinds and frames, from a context's relation rows and attributes.

A row `| k1 | word | k2 |` gives a modifier on k1's bare noun, "a file in its worktree" (`r<n>_Mod : k1_N -> k2_NP
-> k1_CN`: modifiers take a bare head, so they never stack to the left). A row whose word is `of` also gives "its k1"
(`k1_Its`), the frame "k2 has k1" (a state of k2, `r<n>_Has`) and the compound "a k2 k1" (`r<n>_Cpd`, "a request
comment", which means "a comment of a request"); a row whose word is `in` gives the frame "k2 holds k1"
(`r<n>_Holds`). An attribute T of a kind K gives its noun phrases (`T_NP`): "the T of x" (`T_Of_K`), "its T"
(`T_Its`) and the compound "the K T" (`T_Cpd_K`), each a thing (`T_Up`), and the condition "the T of x is v"
(`T_IsOf`). "no K" is the base grammar's determiner `DetNo`; lists with and/or and "only" are spec_rgl's `K_Arg`.
"""
import spec_rgl
import spec_rgl_vocab

HOLD = 'mkV2 (mkV "hold" "holds" "held" "held" "holding")'


def compound(head, before):
    """The noun `before head` ("stage status"): `head`'s noun with `before`'s words in front of it."""
    return "compoundN %s (%s)" % (spec_rgl.s(before), spec_rgl.noun(head, spec_rgl_vocab.regular_plural(head)))


def rows(w, vocab):
    """The modifier, its, has, holds and compound funs of each relation row; the kinds given a state frame, in the
    order of their rows (a set's order changes with the process, and the sources with it)."""
    states, its, seen = {}, set(), set()
    for n, (k1, word, k2) in enumerate(vocab.rows, 1):
        K1, K2, R = spec_rgl.kid(k1), spec_rgl.kid(k2), "r%d_%s" % (n, spec_rgl.slug(word))
        w.fun(R + "_Mod", "%s_N -> %s_NP -> %s_CN" % (K1, K2, K1),
              "mkCN n (SyntaxEng.mkAdv (mkPrep %s) x)" % spec_rgl.s(word), "n x")
        verb = {"of": "have_V2", "in": HOLD}.get(word)
        if verb is None or (k1, word, k2) in seen:
            continue
        seen.add((k1, word, k2))
        w.cat(K2 + "_St", "VP")
        states[k2] = None
        w.fun(R + ("_Has" if word == "of" else "_Holds"), "%s_Arg -> %s_St" % (K1, K2), "mkVP (%s) x" % verb, "x")
        if word == "of":
            w.fun(R + "_Cpd", K1 + "_CN", "mkCN (%s)" % compound(k1, k2))
            if k1 not in its:
                its.add(k1)
                w.fun(K1 + "_Its", "%s_N -> %s_NP0" % (K1, K1), "mkNP (SyntaxEng.mkQuant it_Pron) n", "n")
    return list(states)


def attributes(w, vocab):
    """The noun phrases and the condition of each attribute's noun."""
    for n, (t, ks) in enumerate(vocab.attributes, 1):
        T = "t_%s_%d" % (spec_rgl.slug(t.term), n)
        noun = "mkCN (%s)" % spec_rgl.noun(t.term, spec_rgl_vocab.regular_plural(t.term))
        w.cat(T + "_NP", "NP")
        w.fun(T + "_Its", T + "_NP", "mkNP (SyntaxEng.mkQuant it_Pron) (%s)" % noun)
        w.fun(T + "_Up", "%s_NP -> k_thing_NP" % T, "x", "x")
        w.fun(T + "_IsOf", "Pol -> %s_NP -> %s_Val -> Cond" % (T, T),
              "mkS p (mkCl x (mkVP (ParadigmsEng.mkAdv v.s)))", "p x v")
        for k in ks:
            K = spec_rgl.kid(k)
            w.fun("%s_Of_%s" % (T, K), "%s_NP -> %s_NP" % (K, T),
                  "mkNP the_Det (mkCN (%s) (SyntaxEng.mkAdv (mkPrep \"of\") x))" % noun.split(" ", 1)[1], "x")
            w.fun("%s_Cpd_%s" % (T, K), "Det -> %s_NP" % T, "mkNP d (mkCN (%s))" % compound(t.term, k), "d")


def noun_phrases(w, vocab):
    """Every noun-phrase fun of `vocab` written to `w`; the kinds a row gave a state frame (spec_rgl's `S_Holds`)."""
    attributes(w, vocab)
    return rows(w, vocab)

