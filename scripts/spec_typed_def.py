"""The generated `Def` module pair (design-r2 §4.3): a condition defined in the controlled language.

`Def.gf` extends Req with one fun for each (condition, kind) of the lexicon, `c_<cond>_<kind>_Def : Cond -> Def`,
English "a <kind> is <cond> when <Cond>." `spec_grammar.parse(root, text, grammar="Def")` parses a definition
with it, and refuses a tree holding an `_It` fun: a definition names its subject as "the <kind>".
"""
import spec_tree
import spec_typed


def fun_name(cid, kid):
    """c_outputless, k_result -> c_outputless_k_result_Def."""
    return "%s_%s_Def" % (cid, kid)


def funs(lex):
    """{fun: (condition term, kind term)} of every (condition, kind) whose kind is a kind of the lexicon."""
    ids, kinds = lex.ids(), lex.kind_names()
    return {fun_name(ids[t.key], ids[("kind", k, ())]): (t.term, k) for t in lex.of("condition") for k in t.kinds
            if k in kinds}


def modules(lex):
    """{file name: GF source} of Def.gf and DefEng.gf."""
    abstract, concrete = [], []
    for name, (cond, kind) in sorted(funs(lex).items()):
        abstract.append("    %s : Cond -> Def ;\n" % name)
        concrete.append('    %s c = art ++ %s ++ "is" ++ %s ++ "when" ++ c ++ "." ;\n' % (
            name, spec_typed.gf_str(kind), spec_typed.gf_str(cond)))
    fun = "  fun\n%s" % "".join(abstract) if abstract else ""
    lin = "  lin\n%s" % "".join(concrete) if concrete else ""
    return {"Def.gf": "abstract Def = Req ** {\n  flags startcat = Def ;\n  cat Def ;\n%s}\n" % fun,
            "DefEng.gf": "concrete DefEng of Def = ReqEng ** {\n  lincat Def = Str ;\n%s}\n" % lin}


def refusal(tree, lex):
    """Why a definition's tree is refused, or None: it names its subject as "it" (design-r2 §4.3)."""
    if any(node[0].endswith("_It") for node in spec_tree.nodes(tree)):
        kind = funs(lex).get(tree[0], (None, "thing"))[1]
        return "a definition names its subject as the %s" % kind
    return None
