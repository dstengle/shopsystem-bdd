"""The generated part of grammar 4 (the CNL 4 design, call 1; I7a): the module `Context`, which extends the base
grammar (`grammar/Base.gf`), and its English `ContextEng` over the RGL, from a context's Vocab (spec_rgl_vocab).

Per kind K: its noun `K_N`, `K_CN`, a determiner's noun phrase `K_NP0`, and the noun phrase a slot of kind K takes,
`K_NP`: K's own (`K_Simple`), a kind's under K (`<k>_Up_K`, one fun for each kind above, so a noun reaches a slot one
way), or a code (`K_Code`). An actor is a `K_NP0` of its kind. A verb's frame gives its subject kind S a raw verb
phrase, `S_V` for an action and `S_St` for a state; a trigger is `S_Event : S_NP -> S_V -> Trig`, a condition
`S_Holds : Pol -> S_NP -> S_St -> Cond`, so the RGL makes the verb agree with its subject ("sessions write", "a
session writes"). A response's subject is a doer D's own `D_NP0`: `D_Shall` over `D_Acts`, each act a `S_V` of D or a
kind above it (`D_Act_S`), with its polarity. An attribute of K: `<t>_K_Is : Pol -> K_NP -> <t>_Val -> Cond` ("a
stage is not `done`"), one `<t>_Val` fun per value.
"""
import re

import spec_frames
import spec_typed

TOKEN = spec_typed.PLACEHOLDER


def slug(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_") or "x"


def kid(kind):
    return "k_" + slug(kind)


def s(text):
    """A spelling as a GF string: its tokens joined by ++ (spec_typed.gf_str)."""
    return spec_typed.gf_str(text)


def noun(singular, plural):
    """A noun of one or more words: the last word inflected (its plural the plural's last word), the others before it."""
    words, last = spec_typed.tokens(singular), spec_typed.tokens(plural)[-1]
    lin = "mkN %s %s" % (s(words[-1]), s(last))
    for word in reversed(words[:-1]):
        lin = "compoundN %s (%s)" % (s(word), lin)
    return lin


def verb(term):
    """A verb's RGL V: its base, third person, past and participle (`Forms:`), and -ing; a second word a particle."""
    base, _, particle = term.term.partition(" ")
    s3 = spec_frames.s3(term).split()[0]
    pp = term.forms[1].split()[0] if len(term.forms) > 1 else (base + "d" if base.endswith("e") else base + "ed")
    ing = (base[:-1] if base.endswith("e") and not base.endswith("ee") else base) + "ing"
    lin = "mkV %s %s %s %s %s" % (s(base), s(s3), s(pp), s(pp), s(ing))
    return "partV (%s) %s" % (lin, s(particle)) if particle else lin


def frame_lin(v, pieces):
    """(argument kinds, linearisation) of one frame's verb phrase over its pieces."""
    kinds, vp = [], None
    for n, (words, kind) in enumerate(pieces):
        said = " ".join(words)
        if kind is not None:
            kinds.append(kind)
            x = "x%d" % len(kinds)
            if n == 0:
                vp = "mkVP (mkV2 (%s)%s) %s" % (v, " (mkPrep %s)" % s(said) if said else "", x)
            else:
                vp = "mkVP (%s) (SyntaxEng.mkAdv (mkPrep %s) %s)" % (vp, s(said), x)
        else:
            vp = "mkVP (%s) (ParadigmsEng.mkAdv %s)" % (vp or "mkVP (%s)" % v, s(said))
    return kinds, vp or "mkVP (%s)" % v


class Writer:
    def __init__(self):
        self.cats, self.lincats, self.funs, self.lins = [], [], [], []

    def cat(self, name, lincat):
        if name not in self.cats:
            self.cats.append(name)
            self.lincats.append("  %s = %s ;" % (name, lincat))

    def fun(self, name, typ, lin, args=""):
        self.funs.append("  %s : %s ;" % (name, typ))
        self.lins.append("  %s %s= %s ;" % (name, args + " " if args else "", lin))


def kinds(w, vocab):
    for k in vocab.kinds:
        K = kid(k)
        for suffix, lincat in (("N", "N"), ("CN", "CN"), ("NP0", "NP"), ("NP", "NP")):
            w.cat("%s_%s" % (K, suffix), lincat)
        w.fun(K + "_n", K + "_N", noun(*vocab.nouns[k]))
        w.fun(K + "_UseN", "%s_N -> %s_CN" % (K, K), "mkCN n", "n")
        w.fun(K + "_Det", "Det -> %s_CN -> %s_NP0" % (K, K), "mkNP d cn", "d cn")
        w.fun(K + "_Simple", "%s_NP0 -> %s_NP" % (K, K), "x", "x")
        w.fun(K + "_Code", "Code -> %s_NP" % K, "actor c.s", "c")
        for above in vocab.ancestors(k)[1:]:
            w.fun("%s_Up_%s" % (K, kid(above)), "%s_NP0 -> %s_NP" % (K, kid(above)), "x", "x")
    w.fun("k_thing_Nothing", "k_thing_NP", "nothing_NP")
    for n, (term, k) in enumerate(vocab.actors):
        w.fun("a_%s_%d" % (slug(term), n + 1), kid(k) + "_NP0", "actor %s" % s(term))


def verbs(w, vocab):
    subjects = {}
    for n, v in enumerate(vocab.verbs, 1):
        for m, (subject, pieces) in enumerate(v.frames, 1):
            cat = "%s_%s" % (kid(subject), "V" if v.aspect == "action" else "St")
            w.cat(cat, "VP")
            subjects.setdefault(subject, set()).add(v.aspect)
            args, lin = frame_lin(verb(v.term), pieces)
            typ = " -> ".join(["%s_NP" % kid(k) for k in args] + [cat])
            w.fun("e_%s_%s_%d_%d" % (slug(v.term.term), v.aspect, n, m), typ, lin,
                  " ".join("x%d" % (i + 1) for i in range(len(args))))
    for subject, aspects in subjects.items():
        S = kid(subject)
        if "action" in aspects:
            w.fun(S + "_Event", "%s_NP -> %s_V -> Trig" % (S, S), "mkS (mkCl x v)", "x v")
        if "state" in aspects:
            w.fun(S + "_Holds", "Pol -> %s_NP -> %s_St -> Cond" % (S, S), "mkS p (mkCl x v)", "p x v")
    doers = [k for k in vocab.kinds if any("action" in subjects.get(a, ()) for a in vocab.ancestors(k))]
    for d in doers:
        D = kid(d)
        w.cat(D + "_Act", "{s : Str}")
        w.cat(D + "_Acts", "Acts")
        for above in vocab.ancestors(d):
            if "action" in subjects.get(above, ()):
                w.fun("%s_Act_%s" % (D, kid(above)), "Pol -> %s_V -> %s_Act" % (kid(above), D),
                      "{s = act p v}", "p v")
        w.fun(D + "_Shall", "%s_NP0 -> %s_Acts -> Resp" % (D, D), "shall x l", "x l")
        w.fun(D + "_OneAct", "%s_Act -> %s_Acts" % (D, D), "oneAct a.s", "a")
        w.fun(D + "_AndAct", "%s_Act -> %s_Acts -> %s_Acts" % (D, D, D), "andAct a.s l", "a l")


def attributes(w, vocab):
    for n, (t, ks) in enumerate(vocab.attributes, 1):
        T = "t_%s_%d" % (slug(t.term), n)
        w.cat(T + "_Val", "{s : Str}")
        for value in t.values:
            w.fun("%s_v_%s" % (T, slug(value)), T + "_Val", "{s = %s}" % s(value))
        for k in ks:
            w.fun("%s_%s_Is" % (T, kid(k)), "Pol -> %s_NP -> %s_Val -> Cond" % (kid(k), T),
                  "mkS p (mkCl x (mkVP (ParadigmsEng.mkAdv v.s)))", "p x v")


def modules(vocab):
    """{file name: text} of `Context.gf` and `ContextEng.gf`."""
    w = Writer()
    kinds(w, vocab)
    verbs(w, vocab)
    attributes(w, vocab)
    head = "-- generated by scripts/spec_rgl.py from the context's vocabulary; do not edit"
    abstract = [head, "abstract Context = Base ** {", "  flags startcat = Req ;", "  cat " + " ; ".join(w.cats) + " ;",
                "  fun"] + w.funs + ["}"]
    concrete = [head, "concrete ContextEng of Context = BaseEng ** open SyntaxEng, ParadigmsEng, Prelude in {",
                "  lincat"] + w.lincats + ["  lin"] + w.lins + ["}"]
    return {"Context.gf": "\n".join(abstract) + "\n", "ContextEng.gf": "\n".join(concrete) + "\n"}
