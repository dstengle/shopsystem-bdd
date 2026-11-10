"""The noun phrases of grammar 4 (the CNL 4 design, calls 1 and 4; I8), generated into the module `Context` beside
spec_rgl's kinds and frames, from a context's relation rows and attributes.

A row `| k1 | word | k2 |` gives a modifier on k1's bare noun, "a file in its worktree" (`r<n>_Mod : k1_N -> k2_NP
-> k1_CN`: modifiers take a bare head, so they never stack to the left). A row whose word is `of` also gives "its k1"
(`k1_Its`), the frame "k2 has k1" (a state of k2, `r<n>_Has`) and the compound "a k2 k1" (`r<n>_Cpd`, "a request
comment", which means "a comment of a request"); a row whose word is `in` gives the frame "k2 holds k1"
(`r<n>_Holds`). An attribute T of a kind K gives its noun phrases (`T_NP`): "the T of x" (`T_Of_K`), "its T"
(`T_Its`) and the compound "the K T" (`T_Cpd_K`), each a thing (`T_Up`), and the condition "the T of x is v"
(`T_IsOf`). An attribute whose entry says `Order:` (b240) also gives a point `T_Pt`, one of its values (`T_PtVal`) or a
code (`T_PtCode`), "the T of x is after v" (`T_Cmp`), "the T of x is after v and before w" (`T_Between`), and, ordered
by number, "the T of x is v" and "x is v" of a code (`T_IsCodeOf`, `T_<K>_IsCode`, the Given of a value no entry
lists). Each attribute with `Values:` gives a list of them, "the T of x is one of `a` or `b`", "is not `a` or `b`"
and "x has no T" (`sets`, b240). "no K" is the base grammar's
determiner `DetNo`; lists with and/or and "only" are spec_rgl's `K_Arg`.
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
        if t.order:
            ordered(w, T, t, ks)
        if t.values:
            sets(w, T, ks, noun)


def sets(w, T, ks, noun):
    """A list of the attribute's values (`T_Vals`, "`a`, `b` or `c`"), "the T of x is one of" it (`T_IsOneOf`), "is not"
    it (`T_IsNoneOf`), the same said of a thing of each kind (`T_<K>_IsOneOf`, `T_<K>_IsNoneOf`), and "x has no T"
    (`T_<K>_HasNo`): value sets and a value's absence (b240, construct #4)."""
    w.cat(T + "_Vals", "{s : Str}")
    w.fun(T + "_Vals2", "%s_Val -> %s_Val -> %s_Vals" % (T, T, T), '{s = a.s ++ "or" ++ b.s}', "a b")
    w.fun(T + "_ValsMore", "%s_Val -> %s_Vals -> %s_Vals" % (T, T, T), '{s = a.s ++ "," ++ b.s}', "a b")
    one = 'mkS (mkCl x (mkVP (ParadigmsEng.mkAdv ("one" ++ "of" ++ v.s))))'
    none = "mkS E.UncNeg (mkCl x (mkVP (ParadigmsEng.mkAdv v.s)))"
    for head, said in ((T + "_NP", ""), *(("%s_NP" % spec_rgl.kid(k), "_" + spec_rgl.kid(k)) for k in ks)):
        w.fun("%s%s_IsOneOf" % (T, said), "%s -> %s_Vals -> Cond" % (head, T), one, "x v")
        w.fun("%s%s_IsNoneOf" % (T, said), "%s -> %s_Vals -> Cond" % (head, T), none, "x v")
    for k in ks:
        w.fun("%s_%s_HasNo" % (T, spec_rgl.kid(k)), "%s_NP -> Cond" % spec_rgl.kid(k),
              "mkS (mkCl x (mkVP have_V2 (mkNP no_Quant (%s))))" % noun, "x")


def ordered(w, T, t, ks):
    """The comparison of an ordered attribute's value with a point (b240, construct #6)."""
    w.cat(T + "_Pt", "{s : Str}")
    w.fun(T + "_PtVal", "%s_Val -> %s_Pt" % (T, T), "v", "v")
    w.fun(T + "_PtCode", "Code -> %s_Pt" % T, "c", "c")
    w.fun(T + "_Cmp", "Pol -> %s_NP -> Order -> %s_Pt -> Cond" % (T, T),
          "mkS p (mkCl x (mkVP (ParadigmsEng.mkAdv (o.s ++ v.s))))", "p x o v")
    w.fun(T + "_Between", "%s_NP -> Order -> %s_Pt -> Order -> %s_Pt -> Cond" % (T, T, T),
          'mkS (mkCl x (mkVP (ParadigmsEng.mkAdv (o.s ++ v.s ++ "and" ++ o2.s ++ v2.s))))', "x o v o2 v2")
    if "number" in t.order.lower():
        w.fun(T + "_IsCodeOf", "Pol -> %s_NP -> Code -> Cond" % T, "mkS p (mkCl x (mkVP (ParadigmsEng.mkAdv c.s)))",
              "p x c")
        for k in ks:
            w.fun("%s_%s_IsCode" % (T, spec_rgl.kid(k)), "Pol -> %s_NP -> Code -> Cond" % spec_rgl.kid(k),
                  "mkS p (mkCl x (mkVP (ParadigmsEng.mkAdv c.s)))", "p x c")


def noun_phrases(w, vocab):
    """Every noun-phrase fun of `vocab` written to `w`; the kinds a row gave a state frame (spec_rgl's `S_Holds`)."""
    attributes(w, vocab)
    return rows(w, vocab)

