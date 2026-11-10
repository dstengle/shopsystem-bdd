"""The worlds of design-model-check's scenarios in grammar 4 (b152), picked by the facts its Givens kept
(design_model_check_handlers_facts): each world of the table is the one a condition of the old Givens built
(design_model_check_handlers_conditions, _packs, _forms, codified2_world), its instance named by the scenario's first
of the kind, and what the output names each other instance by (`ALIASES`: an instance said as another was).

A row's facts must all be among the scenario's; the first row that matches builds the world, so a row comes before
any row whose facts are a part of its own. A scenario whose facts no row has is the base world's."""
import importlib.util
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C = _sibling("design_model_check_handlers_conditions.py", "shop_design_model_check_handlers_conditions")
P = _sibling("design_model_check_handlers_packs.py", "shop_design_model_check_handlers_packs")
F = _sibling("design_model_check_handlers_forms.py", "shop_design_model_check_handlers_forms")
C2 = _sibling("codified2_world.py", "shop_codified2_world")


class As:
    """The When's step as an old condition's Given saw it: `the <kind> <name> is <word>`."""

    def __init__(self, step, name, word):
        self._step, self.names, self.text = step, [name], "the thing %s is %s" % (name, word)

    def __getattr__(self, attr):
        return getattr(self._step, attr)


def first(step, kind, default):
    return step.context.get("kinds", {}).get(kind, [default])[0]


def old(fn, kind, default, word):
    """A builder: the old condition `word` given to the first instance of `kind` (`default` when none was given)."""
    return lambda step: fn(As(step, first(step, kind, default), word))


def request(word):
    """A builder: the old condition `word` of the request, its file first named as `work request` names it."""
    def build(step):
        name = first(step, "request", "r1")
        kind, rel = step.context["nodes"][name]
        path = step.repo / rel
        text = path.read_text().replace("/%s\n" % name, "/q1\n", 1)
        path.unlink()
        step.context["nodes"][name] = (kind, ".shop/requests/q1.md")
        H.write(step.repo, ".shop/requests/q1.md", text)
        C.request(As(step, name, word))
        H.says(step, name, "q1")
    return build


def requirement(word):
    return old(C.requirement, "requirement", "r1", word)


def term(word):
    return old(C.term, "term", "t1", word)


def capability(word):
    return old(C.capability, "capability", "c1", word)


def sectionless(step):
    """A capability file with no `## Behaviour` section."""
    name = first(step, "capability", "c1")
    path = step.repo / "spec" / "capabilities" / ("%s.md" % name)
    path.write_text(path.read_text().replace("## Behaviour\n", "## Lines\n"))
    H.says(step, name, "%s.md" % name)


def misaspected_while(step):
    """r1 says an action verb in its While clause, which grammar 4 reads as a state."""
    C2.context(step.repo, H.PATH, [("While a session ends a stage, when the person runs `work start`, `work` shall "
                                    "print the stage.")])


def importing(step):
    """The context imports the CLI pack and its own pack p1, which defines t1 and t2."""
    H.base(step.repo, step.context)
    P.pack(step.repo, first(step, "pack", "p1"), *step.context.get("kinds", {}).get("term", ["t1"]))
    P.imports(step.repo, "cli", first(step, "pack", "p1"))


def current_index(step):
    H.given_index(As(step, "d1", "current"))


def unmigrated(step):
    """A `records/` directory at the root, which the final layout has not."""
    H.write(step.repo, "records/old.md", "# old\n")


def clingoless(word):
    def build(step):
        step.context["interpreter"] = word
    return build


def unattributed(step):
    F.given_unattributed(step)


TABLE = [
    # model check: a rule's code
    (("capability violate `v15a`",), capability("unnumbered"), {}),
    (("capability violate `v15b`",), capability("renumbered"), {}),
    (("capability violate `v15c`",), capability("reusing"), {}),
    (("requirement group violate `v15l`",), old(C.group, "requirement group", "r1", "compound"), {}),
    (("requirement group violate `v15n`",), old(C.group, "requirement group", "r1", "repeating"), {}),
    (("requirement group violate `v15m`",), old(C.group, "requirement group", "r1", "unexampled"), {}),
    (("requirement group violate `v_s3`",), old(C.requirement, "requirement group", "r1", "untested"), {}),
    (("scenario violate `v_s2`",), old(C.scenario, "scenario", "s1", "overtagged"), {}),
    (("request violate `v17`",), request("unanchored"), {}),
    (("request violate `v3`",), request("misresolved"), {}),
    (("requirement violate `v_t1`",), requirement("avoiding"), {}),
    (("requirement violate `v_p1`",), requirement("unparsed"), {}),
    (("requirement violate `w_example`",), requirement("exemplified"), {}),
    (("term violate `v_t2`",), term("duplicated"), {}),
    (("term violate `v_t3`",), term("selfavoiding"), {}),
    (("term violate `v_t4`",), term("unlabelled"), {}),
    (("term violate `v_t11`",), term("frameless"), {}),
    (("term violate `v_t12`",), term("relational"), {}),
    (("term violate `v_t13`",), term("misframed"), {}),
    (("term violate `v_t14`",), term("aspectless"), {}),
    (("term violate `v_t15`",), term("overlapping"), {}),
    (("term violate `v_t16`",), term("unmarked"), {}),
    (("pack violate `v_t17`",), lambda step: P.bounded_context(step, "misimporting"), {}),
    # model check: a file not of its form
    (("request not conform request form",), request("misformed"), {}),
    (("capability not conform capability id form",), capability("misnamed"), {}),
    (("capability not conform capability section form",), sectionless, {}),
    (("feature not conform feature form",), old(C.misfiled, "feature", "f1", "misfiled"), {}),
    (("design-decision not conform decision form",), old(C.headless, "design-decision", "d1", "headless"), {}),
    (("term not conform entry form",), term("malformed"), {}),
    (("this bounded context not conform final layout",), unmigrated, {}),
    (("scenario refer requirement id", "capability not holds requirement id"),
     old(C.scenario, "scenario", "s1", "misreferring"), {}),
    (("interpreter not import `clingo`",), clingoless("clingoless"), {}),
    (("no interpreter import `clingo`",), clingoless("unfound"), {}),
    # model check: the entries of a verb
    (("term has frame", "frame has preposition", "requirement use term"), requirement("prepositioned"), {}),
    (("term has frame", "frame has preposition"), term("prepositional"), {}),
    (("term has frame",), term("multiframed"), {}),
    (("term has sense",), term("polysemous"), {}),
    (("term has oblique recipient",), term("oblique"), {}),
    (("term redefine pack",), term("redefining"), {}),
    (("this bounded context import pack",), importing, {}),
    # model decisions, model rules, work record
    (("decisions index not holds index entry",), old(C.stale, "decisions index", "d2", "stale"), {}),
    (("no decisions index lack index entry",), current_index, {}),
    (("rule catalogue not holds catalogue entry",), old(F.stale_catalogue, "rule catalogue", "r2", "stale"), {}),
    (("text not conform node id form",), unattributed, {}),
    # model parse: a frame's refusals and passes
    (("requirement omit object",), requirement("objectless"), {}),
    (("requirement omit recipient",), requirement("recipientless"), {}),
    (("noun phrase mismatch term",), requirement("mistyped"), {}),
    (("term disagree subject",), requirement("disagreeing"), {}),
    (("passive form has no by-phrase",), requirement("agentless"), {"p1": "t1"}),
    (("precondition use term", "term is `action`"), misaspected_while, {}),
    (("trigger use term", "term is `state`"), requirement("misaspected"), {}),
    (("precondition use term", "term has no object"), old(C.requirement, "requirement", "r1", "intransitive"), {}),
    (("precondition use term", "term is `state`"), requirement("verbal"), {}),
    (("trigger use recipient",), requirement("addressed"), {}),
    (("trigger use option",), requirement("optioned"), {}),
    (("requirement use negation",), requirement("negating"), {}),
    (("requirement use plural subject",), requirement("plural"), {}),
    # model parse: the reading rules
    (("requirement use boxed noun phrase", "definite noun phrase has no antecedent"), requirement("unreachable"),
     {"d1": "t1"}),
    (("requirement use boxed noun phrase", "definite noun phrase has antecedent"), requirement("shadowed"),
     {"a2": "a1"}),
    (("definite noun phrase has no antecedent",), requirement("antecedentless"), {"d1": "t1"}),
    (("self-reference has no antecedent",), requirement("self-embedding"), {"s1": "t1"}),
    (("precondition use negated indefinite",), requirement("unquantified"), {"n1": "t1"}),
    (("requirement has no trigger", "requirement use no modal adverb"), requirement("triggerless"), {}),
    (("requirement has logical form",), requirement("ambiguous"), {}),
    (("requirement use genitive",), requirement("genitive"), {}),
    (("requirement use negative quantifier",), requirement("denying"), {}),
    (("requirement use compound noun",), requirement("compound"), {}),
    (("requirement use relative clause",), requirement("relative"), {}),
    (("requirement use whose clause",), requirement("possessive"), {}),
    (("requirement use demonstrative",), requirement("indexical"), {}),
    (("requirement use inner genitive",), requirement("self-relating"), {}),
    (("requirement use distributive genitive",), requirement("distributive"), {"d2": "d1"}),
    (("requirement use assignment",), old(C.requirement, "requirement", "r1", "setting"), {}),
    (("requirement use later sense",), requirement("later-sensed"), {}),
    # model parse: counts, time and modality
    (("count contradict count",), capability("overcounted"), {}),
    (("precondition use count",), capability("thresholded"), {}),
    (("requirement use count",), requirement("counted"), {}),
    (("requirement use comparison",), requirement("timed"), {}),
    (("requirement use clock trigger",), requirement("clocked"), {}),
    (("precondition use perfect",), requirement("historical"), {}),
    (("number has no unit",), requirement("unitless"), {}),
    (("requirement use permission",), requirement("permissive"), {}),
    (("requirement use modal adverb",), requirement("invariant"), {}),
    # model logic and model explain
    (("capability holds unification failure", "capability holds clash"), capability("unpairable"), {"c2": "c1#r3"}),
    (("restriction allow act",), capability("restricting"), {}),
    (("requirement use restriction",), requirement("restrictive"), {}),
    (("universal quantifier oblige act",), capability("exhaustive"), {}),
    (("precondition use universal quantifier",), capability("quantifying"), {}),
    (("requirement use negated modifier",), capability("excepting"), {}),
    (("capability has requirement", "requirement override requirement"), capability("overriding"), {}),
    (("requirement override requirement",), old(C.requirement, "requirement", "r1", "overridden"), {"r4": "r2"}),
    (("universal condition forbid act",), capability("contravening"), {}),
    (("requirement permit act",), capability("forbidding"), {}),
    (("requirement add no consequence",), requirement("restating"), {}),
    (("requirement use refusal",), old(C.requirement, "requirement", "r1", "refusing"), {}),
    (("capability is `codified-2`",), capability("recodified"), {}),
    (("run on fragment",), requirement("unfinished"), {"f1": "thing#r1"}),
    (("no capability holds requirement id",), old(C.requirement, "requirement id", "r1", "nonexistent"), {}),
]


def build(step):
    """The world of the first row whose facts the scenario's Givens all said, and its aliases said."""
    facts = set(step.context.get("facts", ()))
    for needed, builder, aliases in TABLE:
        if facts.issuperset(needed):
            builder(step)
            for name, said in aliases.items():
                H.says(step, name, step.context.get("says", {}).get(said, said))
            return


def then(step, done):
    """A Then of what the run gave: r1's logical form, an interpreter that imports clingo (the check ran to its end),
    the requirement r4 that uses a refusal (its line in `model explain`'s output says the tool shall refuse); False
    for any other, which the registry's handler takes (`model` writes ...)."""
    says = step.context.get("says", {})
    if step.event == "has" and step.nps[0].startswith("the logical form"):
        assert done.returncode == 0 and says[step.names[-1]] in done.stdout, (step.text, done.stdout, done.stderr)
    elif step.event in ("import", "use") and "interpreter" in step.subject + " ".join(step.nps):
        assert done.returncode == 0 and "0 violations" in done.stdout, (step.text, done.stdout, done.stderr)
    elif step.event == "use" and step.nps[0].startswith("the refusal"):
        ident = says[step.names[0]]
        lines = [line for line in done.stdout.splitlines() if line.strip().startswith(ident + "  ")]
        assert lines and any(" shall refuse " in line for line in lines), (ident, done.stdout)
    else:
        return False
