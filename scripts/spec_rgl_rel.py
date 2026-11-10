"""The relative clauses and "whose" of grammar 4 (the CNL 4 design, call 1; I9, b107 folded in), generated into the
module `Context` beside spec_rgl's frames and spec_rgl_np's noun phrases. Each is a state, never an action (call 3),
and each takes a polarity: "that does not follow", "whose status is not `done`".

A subject kind S with a state verb phrase (`S_St`: a state frame's, or a row's "has" and "holds") gives a subject
relative clause on the noun of each kind K under S, `K_Rel_S : Pol -> K_CN -> S_St -> K_CN`, "a session that follows
a stage". A state frame with one of its kinds O left out is `S_Gap_O`, its verb phrase with a gap: the first kind's
gap, with the frame's words after it ("a stage that sessions follow"), or the last kind's with its preposition
stranded when nothing follows it ("a channel that a viewer subscribes to"); it gives an object relative clause on
each kind K under O, `K_Obj_S_O : Pol -> K_CN -> S_Arg -> S_Gap_O -> K_CN`. A row `k1 | of | k2` gives "whose" on
each kind K under k2, `K_Whose_r<n>_S : Pol -> K_CN -> S_St -> K_CN` for each S above k1 with a state, "a session
whose worktree holds a file"; an attribute T of K, `K_Whose_T : Pol -> K_CN -> T_Val -> K_CN`, "a stage whose status
is `done`". The relative pronoun is "that" (call 1), its clause after the noun's modifiers.
"""
import spec_rgl
import spec_rgl_np
import spec_rgl_vocab


def under(vocab, kind):
    """The kinds under `kind`, itself first."""
    return [k for k in vocab.kinds if kind in vocab.ancestors(k)]


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
    return "mkCN cn (mkRS p (%s))" % rcl


def whose(noun):
    return "E.GenRP G.NumSg (mkCN (%s))" % noun


def clauses(w, vocab, states):
    """Every relative clause and "whose" of `vocab` written to `w`, `states` the kinds with a state verb phrase."""
    for s in sorted(states):
        S = spec_rgl.kid(s)
        for k in under(vocab, s):
            w.fun("%s_Rel_%s" % (spec_rgl.kid(k), S), "Pol -> %s_CN -> %s_St -> %s_CN" % (spec_rgl.kid(k), S,
                  spec_rgl.kid(k)), that("mkRCl E.that_RP v"), "p cn v")
    for s, o in sorted(gaps(w, vocab)):
        S, O = spec_rgl.kid(s), spec_rgl.kid(o)
        for k in under(vocab, o):
            K = spec_rgl.kid(k)
            w.fun("%s_Obj_%s_%s" % (K, S, O), "Pol -> %s_CN -> %s_Arg -> %s_Gap_%s -> %s_CN" % (K, S, S, O, K),
                  that("E.StrandRelSlash E.that_RP (mkClSlash x v)"), "p cn x v")
    for n, (k1, word, k2) in enumerate(vocab.rows, 1):
        if word != "of":
            continue
        noun = spec_rgl.noun(k1, vocab.nouns.get(k1, (k1, spec_rgl_vocab.regular_plural(k1)))[1])
        for k in under(vocab, k2):
            K = spec_rgl.kid(k)
            for s in [a for a in vocab.ancestors(k1) if a in states]:
                w.fun("%s_Whose_r%d_%s" % (K, n, spec_rgl.kid(s)), "Pol -> %s_CN -> %s_St -> %s_CN" % (
                    K, spec_rgl.kid(s), K), that("mkRCl (%s) v" % whose(noun)), "p cn v")
    for n, (t, ks) in enumerate(vocab.attributes, 1):
        T = "t_%s_%d" % (spec_rgl.slug(t.term), n)
        noun = spec_rgl.noun(t.term, spec_rgl_vocab.regular_plural(t.term))
        for k in dict.fromkeys(k for base in ks for k in under(vocab, base)):
            K = spec_rgl.kid(k)
            w.fun("%s_Whose_%s" % (K, T), "Pol -> %s_CN -> %s_Val -> %s_CN" % (K, T, K),
                  that("mkRCl (%s) (mkVP (ParadigmsEng.mkAdv v.s))" % whose(noun)), "p cn v")
