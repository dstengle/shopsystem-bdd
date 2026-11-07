"""The generated GF modules of a lexicon (design §9.1, §9.2): `Lex` (actors, events, resources) and `Typed` (one
block of slots per kind, attribute, condition and relation row), each with its English.

A relation row (from kind, word, to kind) gives a modifier fun `rel_<k1>_<word>_<k2>` and a clause fun of the same
name with `_Atom`, and its negation `_AtomNot` (design-r2 §4.2; b82): a preposition between two kinds is the one row given for that pair, so PP
attachment is typed and a line where two attachments typecheck has two trees and is refused.

A typed slot is what makes "an initiative that is `drafted`" fail to parse: a value is a fun of its own
attribute's category only. Names come from `spec_lexicon.Lexicon.ids`; the suffixes are the ones `spec_tree` reads
(`<kind>_<det>`, `<attribute>_One`/`_More`).
"""
import re

import spec_lexicon

# A backticked or quoted span is one token; GF's lexer splits on spaces, so inside a span a space is this.
PLACEHOLDER = ""
TOKEN = re.compile(r'`[^`]*`|"[^"]*"|[^\s`"]+')
PREPOSITIONS = {"under", "of", "for", "on", "in", "with", "outside", "by", "into", "from", "to", "at", "within"}
DETS = {"An": "detA cn", "Every": 'det "every" cn', "The": 'det "the" cn', "No": 'det "no" cn',
        "AtMostOne": 'det ("at" ++ "most" ++ "one") cn', "One": 'det "one" cn', "Pl": "plural cn",
        "Its": 'det "its" cn'}


def tokens(text):
    """Words, backticked and quoted spans (kept whole), and trailing punctuation as tokens of their own."""
    out = []
    for found in TOKEN.finditer(text):
        token = found.group()
        if token[0] in '`"':
            out.append(token)
            continue
        trail = []
        while token and token[-1] in ",.;:":
            trail.insert(0, token[-1])
            token = token[:-1]
        out += ([token] if token else []) + trail
    return out


def gf_str(text):
    """A spelling as a GF string expression: `"spec" ++ "lock"`; a span keeps its spaces as PLACEHOLDER."""
    parts = []
    for t in tokens(text):
        t = t.replace(" ", PLACEHOLDER).replace("\\", "\\\\").replace('"', '\\"')
        parts.append('"%s"' % t)
    return " ++ ".join(parts) if len(parts) == 1 else "(%s)" % " ++ ".join(parts)


def _last(word, rule):
    head, _, last = word.rpartition(" ")
    return (head + " " if head else "") + rule(last)


def plural(word):
    def rule(w):
        if re.search(r"(s|sh|ch|x|z)$", w):
            return w + "es"
        if re.search(r"[^aeiou]y$", w):
            return w[:-1] + "ies"
        return w + "s"
    return _last(word, rule)


def past(word):
    if word.endswith("e"):
        return word + "d"
    if re.search(r"[^aeiou]y$", word):
        return word[:-1] + "ied"
    return word + "ed"


def _lex(lex, ids):
    funs, lins = [], []
    for t in lex.of("actor"):
        funs.append("%s : Actor ;" % ids[t.key])
        lins.append("%s = %s ;" % (ids[t.key], gf_str(t.term)))
    for t in lex.of("event"):
        s3, part = t.forms if len(t.forms) == 2 else (plural(t.term), past(t.term))
        funs.append("%s : Event ;" % ids[t.key])
        lins.append("%s = mkEvent %s %s %s ;" % (ids[t.key], gf_str(t.term), gf_str(s3), gf_str(part)))
    for t in lex.of("resource"):
        funs.append("%s : Resource ;" % ids[t.key])
        lins.append("%s = mkRes %s %s ;" % (ids[t.key], gf_str(t.term), gf_str(t.plural or plural(t.term))))
    return funs, lins


def _kind(t, kid):
    sg, pl = gf_str(t.term), gf_str(t.plural or plural(t.term))
    cats = ["%s_CN ; %s_NP ;" % (kid, kid)]
    funs = ["%s : %s_CN ;" % (kid, kid), "%s : %s_CN -> %s_NP ;" % (", ".join("%s_%s" % (kid, d) for d in DETS),
                                                                    kid, kid),
            "%s_Named : Code -> %s_NP ;" % (kid, kid), "%s_It : %s_NP ;" % (kid, kid),
            "%s_toNP : %s_NP -> NP ;" % (kid, kid), "%s_NumberOf : %s_CN -> NP ;" % (kid, kid)]
    lincats = ["%s_CN = CN ; %s_NP = NP ;" % (kid, kid)]
    lins = ["%s = mkCN %s %s ;" % (kid, sg, pl)] + ["%s_%s cn = %s ;" % (kid, d, body) for d, body in DETS.items()]
    lins += ['%s_Named c = np ("the" ++ %s ++ c) ;' % (kid, sg), "%s_It = itNP ;" % kid, "%s_toNP x = x ;" % kid,
             '%s_NumberOf cn = np ("the" ++ "number" ++ "of" ++ cn.s ! Pl) ;' % kid]
    return cats, funs, lincats, lins


def _attribute(t, kind, tid, ids):
    kid, a = ids[("kind", kind, ())], gf_str(t.term)
    cats = ["%s_V ; %s_Vs ;" % (tid, tid)]
    vids = [ids[("value", v, (kind, t.term))] for v in t.values]
    funs = ["%s : %s_V ;" % (", ".join(vids), tid), "%s_One : %s_V -> %s_Vs ;" % (tid, tid, tid),
            "%s_More : %s_V -> %s_Vs -> %s_Vs ;" % (tid, tid, tid, tid),
            "%s_ThatIs, %s_ThatIsNot : %s_CN -> %s_V -> %s_CN ;" % (tid, tid, kid, tid, kid),
            "%s_Whose, %s_WhoseNot : %s_CN -> %s_Vs -> %s_CN ;" % (tid, tid, kid, tid, kid),
            "%s_Pre : %s_V -> %s_CN ;" % (tid, tid, kid), "%s_Is, %s_IsNot : %s_NP -> %s_V -> Atom ;" % (
                tid, tid, kid, tid), "%s_Becomes : %s_NP -> %s_V -> Trig ;" % (tid, kid, tid),
            "%s_Set : %s_NP -> %s_V -> VP ;" % (tid, kid, tid), "%s_Of : %s_NP -> NP ;" % (tid, kid)]
    lincats = ["%s_V = Str ; %s_Vs = Vs ;" % (tid, tid)]
    sg, pl = gf_str(ids[("kind-sg", kind)]), gf_str(ids[("kind-pl", kind)])
    lins = ["%s = %s ;" % (vid, gf_str(v)) for vid, v in zip(vids, t.values)]
    lins += ["%s_One v = oneV v ;" % tid, "%s_More v l = moreV v l ;" % tid,
             "%s_ThatIs cn v = post cn (thatBe v) ;" % tid, '%s_ThatIsNot cn v = post cn (thatBe ("not" ++ v)) ;' % tid,
             "%s_Whose cn l = post cn (whose %s l.s) ;" % (tid, a),
             '%s_WhoseNot cn l = post cn (whose %s ("not" ++ l.s)) ;' % (tid, a),
             "%s_Pre v = mkCN (v ++ %s) (v ++ %s) ;" % (tid, sg, pl), "%s_Is x v = x.s ++ be x ++ v ;" % tid,
             '%s_IsNot x v = x.s ++ be x ++ "not" ++ v ;' % tid,
             '%s_Becomes x v = x.s ++ (case x.n of {Sg => "becomes" ; Pl => "become"}) ++ v ;' % tid,
             '%s_Set x v = "set" ++ (attrOf %s x).s ++ "to" ++ v ;' % (tid, a), "%s_Of x = attrOf %s x ;" % (tid, a)]
    return cats, funs, lincats, lins


def _condition(t, kind, cid, ids):
    kid, c = ids[("kind", kind, ())], gf_str(t.term)
    sg, pl = gf_str(ids[("kind-sg", kind)]), gf_str(ids[("kind-pl", kind)])
    funs = ["%s_Pre : %s_CN ;" % (cid, kid), "%s_ThatIs, %s_ThatIsNot : %s_CN -> %s_CN ;" % (cid, cid, kid, kid),
            "%s_Is, %s_IsNot : %s_NP -> Atom ;" % (cid, cid, kid)]
    lins = ["%s_Pre = mkCN (%s ++ %s) (%s ++ %s) ;" % (cid, c, sg, c, pl),
            "%s_ThatIs cn = post cn (thatBe %s) ;" % (cid, c), '%s_ThatIsNot cn = post cn (thatBe ("not" ++ %s)) ;' % (
                cid, c), "%s_Is x = x.s ++ be x ++ %s ;" % (cid, c), '%s_IsNot x = x.s ++ be x ++ "not" ++ %s ;' % (
                cid, c)]
    return funs, lins


def rows(lex):
    """The relation rows `(from kind, word, to kind, relation id)` of a lexicon: `Lexicon.relations()` (design-r2 §8)."""
    return list(lex.relations())


def relation_fun(kid1, word, kid2):
    """`k_stage`, `for`, `k_work_item` -> rel_stage_for_work_item: the modifier fun of a row; `_Atom` its clause."""
    return "rel_%s_%s_%s" % (kid1[2:], spec_lexicon.ident(word, "relation")[2:], kid2[2:])


def _relation(word, k1, k2, fun):
    """The modifier ("a stage for the work-item") and the clause ("the stage is for the work-item") of one row."""
    funs = ["%s : %s_CN -> %s_NP -> %s_CN ;" % (fun, k1, k2, k1),
            "%s_Atom, %s_AtomNot : %s_NP -> %s_NP -> Atom ;" % (fun, fun, k1, k2)]
    w = gf_str(word)
    if word.split()[-1] in PREPOSITIONS:
        return funs, ["%s cn x = post cn (same (%s ++ x.s)) ;" % (fun, w), "%s_Atom x y = x.s ++ be x ++ %s ++ y.s ;" % (
            fun, w), '%s_AtomNot x y = x.s ++ be x ++ "not" ++ %s ++ y.s ;' % (fun, w)]
    inf = gf_str(re.sub(r"has$", "have", word) if word.endswith("has") else word.removesuffix("s"))
    return funs, ["%s cn x = post cn (verbal %s %s x) ;" % (fun, w, inf),
                  "%s_Atom x y = x.s ++ (case x.n of {Sg => %s ; Pl => %s}) ++ y.s ;" % (fun, w, inf),
                  '%s_AtomNot x y = x.s ++ (case x.n of {Sg => "does" ; Pl => "do"}) ++ "not" ++ %s ++ y.s ;' % (
                      fun, inf)]


def modules(lex):
    """{file name: GF source} for Lex.gf, LexEng.gf, Typed.gf and TypedEng.gf of a lexicon whose problems
    (`spec_lexicon.problems`) have been reported; entries a problem names are left out."""
    ids = lex.ids()
    kinds = {t.term: t for t in lex.of("kind")}
    for k, t in kinds.items():
        ids[("kind-sg", k)], ids[("kind-pl", k)] = t.term, t.plural or plural(t.term)
    lfuns, llins = _lex(lex, ids)
    cats, funs, lincats, lins = [], [], [], []
    for k, t in sorted(kinds.items()):
        for acc, part in zip((cats, funs, lincats, lins), _kind(t, ids[t.key])):
            acc += part
    seen_values = set()
    for t in lex.of("attribute"):
        for kind in t.kinds:
            if kind not in kinds or any((kind, v) in seen_values for v in t.values) or not t.values:
                continue
            seen_values |= {(kind, v) for v in t.values}
            tid = ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], ids[("kind", kind, ())])
            for acc, part in zip((cats, funs, lincats, lins), _attribute(t, kind, tid, ids)):
                acc += part
    for word in sorted({t.term for t in lex.of("attribute")}):
        nid = "n_" + spec_lexicon.ident(word, "attribute")[2:]
        funs.append("%s : NP ;" % nid)
        lins.append("%s = np (art ++ %s) ;" % (nid, gf_str(word)))
    for t in lex.of("condition"):
        for kind in (k for k in t.kinds if k in kinds):
            cid = ids[t.key] if len(t.kinds) == 1 else "%s_%s" % (ids[t.key], ids[("kind", kind, ())])
            f, li = _condition(t, kind, cid, ids)
            funs += f
            lins += li
    seen_rels = set()
    for k1, word, k2, _ in rows(lex):
        if k1 in kinds and k2 in kinds:
            kid1, kid2 = ids[("kind", k1, ())], ids[("kind", k2, ())]
            fun = relation_fun(kid1, word, kid2)
            if fun not in seen_rels:
                seen_rels.add(fun)
                f, li = _relation(word, kid1, kid2, fun)
                funs += f
                lins += li

    def block(head, *sections):
        body = "".join("  %s\n%s" % (kw, "".join("    %s\n" % x for x in xs)) for kw, xs in sections if xs)
        return "%s {\n%s}\n" % (head, body)
    return {
        "Lex.gf": block("abstract Lex = Core **", ("fun", lfuns)),
        "LexEng.gf": block("concrete LexEng of Lex = CoreEng **", ("lin", llins)),
        "Typed.gf": block("abstract Typed = Lex **", ("cat", cats), ("fun", funs)),
        "TypedEng.gf": block("concrete TypedEng of Typed = LexEng **", ("lincat", lincats), ("lin", lins)),
    }
