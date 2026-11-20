"""The relative clauses and "whose" of grammar 4 (the CNL 4 design, call 1; I9, b107 folded in), generated into the
module `Context` beside spec_rgl's frames and spec_rgl_np's noun phrases. Each is a state, never an action (call 3),
and each takes a polarity: "that does not follow", "whose status is not `done`".

As the RGL's RelCN does (b437), a relative clause is built once, of the kind O it follows (`O_RS`, an RS), and
attached to the noun of each kind K under O by one fun of the pair, `K_RelCN_O : K_CN -> O_RS -> K_CN`; the grammar
grows by a few funs a kind, not a fun per clause and kind. A subject kind S with a state verb phrase (`S_St`: a state
frame's, or a row's "has" and "holds") gives `S_Rel : Pol -> S_St -> S_RS`, "a session that follows a stage". A state
frame with one of its kinds O left out is `S_Gap_O`, its verb phrase with a gap: the first kind's gap, with the
frame's words after it ("a stage that sessions follow"), or the last kind's with its preposition stranded when nothing
follows it ("a channel that a viewer subscribes to"); it gives `S_Gapped_O : Pol -> S_Arg -> S_Gap_O -> O_RS`. A row
`k1 | of | k2` gives "whose" for each S above k1 with a state, `r<n>_Whose_S : Pol -> S_St -> k2_RS`, "a session whose
worktree holds a file"; an attribute T of kinds ks, for each of ks under no other, `T_Whose_B : Pol -> T_Val ->
B_RS`, "a stage whose status is `done`" (`whose_value` the tree of one, for the readers that build one). The relative
pronoun is "that" (call 1), its clause after the noun's modifiers.
"""
import spec_rgl
import spec_rgl_np
import spec_rgl_vocab


def gapped(v, pieces):
    """[(gap kind, the other kinds in order, the VPSlash's linearisation)] of one frame's pieces: the first kind left
    out, and the last when it is not the first and nothing follows it."""
    out, slots = [], [n for n, (_, kind) in enumerate(pieces) if kind is not None]
    if not slots:
        return out
    if slots[0] == 0:
        words, kind = pieces[0]
        lin, others = "mkVPSlash (mkV2 (%s)%s)" % (v, " (mkPrep %s)" % spec_rgl.s(" ".join(words)) if words else ""), []
        for said, k in pieces[1:]:
            if k is None:
                lin = "G.AdvVPSlash (%s) (ParadigmsEng.mkAdv %s)" % (lin, spec_rgl.s(" ".join(said)))
                continue
            others.append(k)
            lin = "G.AdvVPSlash (%s) (SyntaxEng.mkAdv (mkPrep %s) x%d)" % (lin, spec_rgl.s(" ".join(said)), len(others))
        out.append((kind, others, lin))
    last = slots[-1]
    if last > 0 and last == len(pieces) - 1:
        words, kind = pieces[last]
        others, vp = spec_rgl.frame_lin(v, pieces[:last])
        out.append((kind, others, "G.VPSlashPrep (%s) (mkPrep %s)" % (vp, spec_rgl.s(" ".join(words)))))
    return out


def gaps(w, vocab):
    """Each state frame's verb phrases with a gap, and each "has" and "holds" row's; the (S, O) of each gap made."""
    made = set()

    def gap(subject, kind, name, others, lin):
        cat = "%s_Gap_%s" % (spec_rgl.kid(subject), spec_rgl.kid(kind))
        w.cat(cat, "VPSlash")
        made.add((subject, kind))
        w.fun(name, " -> ".join(["%s_Arg" % spec_rgl.kid(k) for k in others] + [cat]), lin,
              " ".join("x%d" % (i + 1) for i in range(len(others))))
    for n, v in enumerate(vocab.verbs, 1):
        for m, (subject, pieces) in enumerate(v.frames, 1):
            if v.aspect != "state":
                continue
            for g, (kind, others, lin) in enumerate(gapped(spec_rgl.verb(v.term), pieces), 1):
                gap(subject, kind, "g_%s_%d_%d_%d" % (spec_rgl.slug(v.term.term), n, m, g), others, lin)
    seen = set()
    for n, (k1, word, k2) in enumerate(vocab.rows, 1):
        verb = {"of": "have_V2", "in": spec_rgl_np.HOLD}.get(word)
        if verb and (k1, word, k2) not in seen:
            seen.add((k1, word, k2))
            gap(k2, k1, "r%d_%s_Gap" % (n, spec_rgl.slug(word)), [], "mkVPSlash (%s)" % verb)
    return made


def that(rcl):
    return "mkRS p (%s)" % rcl


def whose(noun):
    return "E.GenRP G.NumSg (mkCN (%s))" % noun


def tops(vocab, ks):
    """The kinds of an attribute's entry that are under no other of them: the kinds its "whose" clause follows."""
    return [b for b in dict.fromkeys(ks) if not any(o != b and o in vocab.ancestors(b) for o in ks)]


def rel_cn(kind, rs_kind, cn, rs):
    """The tree of the common noun `cn` of `kind` followed by the relative clause `rs` of `rs_kind` (`K_RelCN_O`)."""
    return ("%s_RelCN_%s" % (spec_rgl.kid(kind), spec_rgl.kid(rs_kind)), cn, rs)


def whose_value(vocab, kind, T, pol, cn, value):
    """The tree of "<cn> whose T is v" on a noun of `kind`, `T` the attribute's id `t_<word>_<n>`."""
    ks = vocab.attributes[int(T.rsplit("_", 1)[1]) - 1][1]
    base = next(b for b in tops(vocab, ks) if b in vocab.ancestors(kind))
    return rel_cn(kind, base, cn, ("%s_Whose_%s" % (T, spec_rgl.kid(base)), pol, value))


def clauses(w, vocab, states):
    """Every relative clause and "whose" of `vocab` written to `w`, `states` the kinds with a state verb phrase: each
    clause built once, of the kind it follows (`O_RS`), and attached to the noun of each kind under that kind
    (`K_RelCN_O`), as the RGL's RelCN does (b437)."""
    follows = set()

    def clause(kind, name, typ, lin):
        cat = "%s_RS" % spec_rgl.kid(kind)
        w.cat(cat, "RS")
        follows.add(kind)
        w.fun(name, "Pol -> %s -> %s" % (typ, cat), that(lin), "p " + " ".join(
            "x%d" % (i + 1) for i in range(typ.count("->") + 1)))
    for s in sorted(states):
        S = spec_rgl.kid(s)
        clause(s, "%s_Rel" % S, "%s_St" % S, "mkRCl E.that_RP x1")
    for s, o in sorted(gaps(w, vocab)):
        S, O = spec_rgl.kid(s), spec_rgl.kid(o)
        clause(o, "%s_Gapped_%s" % (S, O), "%s_Arg -> %s_Gap_%s" % (S, S, O),
               "E.StrandRelSlash E.that_RP (mkClSlash x1 x2)")
    for n, (k1, word, k2) in enumerate(vocab.rows, 1):
        if word != "of":
            continue
        noun = spec_rgl.noun(k1, vocab.nouns.get(k1, (k1, spec_rgl_vocab.regular_plural(k1)))[1])
        for s in [a for a in vocab.ancestors(k1) if a in states]:
            clause(k2, "r%d_Whose_%s" % (n, spec_rgl.kid(s)), "%s_St" % spec_rgl.kid(s),
                   "mkRCl (%s) x1" % whose(noun))
    for n, (t, ks) in enumerate(vocab.attributes, 1):
        T = "t_%s_%d" % (spec_rgl.slug(t.term), n)
        noun = spec_rgl.noun(t.term, spec_rgl_vocab.regular_plural(t.term))
        for base in tops(vocab, ks):
            clause(base, "%s_Whose_%s" % (T, spec_rgl.kid(base)), "%s_Val" % T,
                   "mkRCl (%s) (mkVP (ParadigmsEng.mkAdv x1.s))" % whose(noun))
    for k in vocab.kinds:
        K = spec_rgl.kid(k)
        for o in vocab.ancestors(k):
            if o in follows:
                w.fun("%s_RelCN_%s" % (K, spec_rgl.kid(o)), "%s_CN -> %s_RS -> %s_CN" % (K, spec_rgl.kid(o), K),
                      "mkCN cn rs", "cn rs")
