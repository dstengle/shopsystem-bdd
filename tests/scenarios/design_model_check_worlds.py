"""The worlds of design-model-check's scenarios in grammar 4 (b152, b240 phase 23), picked by the facts its Givens
kept (design_model_check_handlers_facts): each world of the table is the one a condition of the codified-1 Givens built
(design_model_check_handlers_conditions, _packs, _forms, codified2_world), its instance named by the scenario's first
of the kind, and what the output names each other instance by (`ALIASES`: an instance said as another was).

A row's facts must all be among the scenario's; the first row that matches builds the world, so a row comes before
any row whose facts are a part of its own. A scenario whose facts no row has fails, naming them; a row of `nothing` is the base world's."""
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
CACHE = _sibling("design_model_check_handlers_cache.py", "shop_design_model_check_handlers_cache")


class As:
    """The step as a codified-1 condition's Given saw it: `the <kind> <name> is <word>`."""

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


def frameless_verb(step):
    """The verb v1, a glossary entry of its own with no frame."""
    name = first(step, "verb", "v1")
    H.base(step.repo, step.context)
    index = step.repo / "spec" / "index.md"
    index.write_text(index.read_text() + "- **%s** (noun): a thing.\n" % name)
    C.term(As(step, name, "frameless"))


def sectionless(step):
    """A capability file with no `## Behaviour` section."""
    name = first(step, "capability", "c1")
    C.capability(As(step, name, "unnumbered"))
    path = step.repo / "spec" / "capabilities" / ("%s.md" % name)
    path.write_text(path.read_text().replace("- **When** asked", "- [r1] **When** asked").replace(
        "## Behaviour\n", "## Lines\n"))
    H.says(step, name, "%s.md" % name)


def line(text):
    """A builder: the smallest codified-2 world whose r1 is `text`."""
    return lambda step: C2.context(step.repo, H.PATH, [text])


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


def stale_catalogue(step):
    F.given_catalogue(As(step, "r2", "stale"))
    F.stale_catalogue(step)


def stale_index(step):
    H.given_index(As(step, "d2", "stale"))
    C.stale(step)


def unattributed(step):
    F.given_unattributed(step)
    H.says(step, "t1", "--about")


def served(step):
    """The capability c1, sound: one requirement and its scenario."""
    name = first(step, "capability", "c1")
    H.write(step.repo, "spec/capabilities/%s.md" % name, H.cap(name, ["- [r1] **When** asked, `thing` shall answer."]))
    H.write(step.repo, "features/%s.feature" % name, H.feature(name, "@r1"))


def nothing(step):
    pass


WHILE_ACTION = "While a session ends a stage, when the person runs `work start`, `work` shall print the stage."
NONCONFORMING = "When a session ends a stage, `work` shall banana the stage."
TABLE = [
    # the base world: nothing violates a rule, and it has facts
    (("no thing violate rule",), nothing, {}),
    (("this bounded context has fact",), nothing, {}),
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
    (("term violate `v_t12`",), term("relational"), {}),
    (("term violate `v_t13`",), term("misframed"), {}),
    (("term violate `v_t14`",), term("aspectless"), {}),
    (("term violate `v_t15`",), term("overlapping"), {}),
    (("term violate `v_t16`",), term("unmarked"), {}),
    (("pack violate `v_t17`",), lambda step: P.bounded_context(step, "misimporting"), {}),
    (("observation violate `w_uncited_obs`",), nothing, {}),
    (("capability violate `w_unserved_cap`",), served, {}),
    # model check: a file not of its form
    (("request not conform request form",), request("misformed"), {}),
    (("capability not conform capability id form",), capability("misnamed"), {}),
    (("capability has no section",), sectionless, {}),
    (("feature not conform feature form",), old(C.misfiled, "feature", "f1", "misfiled"), {}),
    (("design-decision has no id",), old(C.headless, "design-decision", "d1", "headless"), {}),
    (("design-decision has no section",), old(C.headless, "design-decision", "d1", "headless"), {}),
    (("term not conform entry form",), term("malformed"), {}),
    (("this bounded context not conform final layout",), unmigrated, {}),
    (("scenario refer requirement id",), old(C.scenario, "scenario", "s1", "misreferring"), {}),
    (("interpreter not import `clingo`",), clingoless("clingoless"), {}),
    (("no interpreter import `clingo`",), clingoless("unfound"), {}),
    # model check: the entries of a verb
    (("verb has no frame",), frameless_verb, {}),
    (("term has no part of speech",), term("unlabelled"), {}),
    (("term has frame", "frame has preposition", "requirement use term"), requirement("prepositioned"), {}),
    (("term has frame", "frame has preposition"), term("prepositional"), {}),
    (("term has frame",), term("multiframed"), {}),
    (("term has sense",), term("polysemous"), {}),
    (("term redefine pack",), term("redefining"), {}),
    (("this bounded context import pack",), importing, {}),
    # model decisions, model rules, work record
    (("decisions index not holds index entry",), stale_index, {}),
    (("no decisions index lack index entry",), current_index, {}),
    (("rule catalogue not holds catalogue entry",), stale_catalogue, {}),
    (("text not conform node id form",), unattributed, {}),
    # model parse: a frame's refusals and passes
    (("requirement omit object",), requirement("objectless"), {}),
    (("requirement omit recipient",), requirement("recipientless"), {}),
    (("no frame take noun phrase",), requirement("mistyped"), {}),
    (("term not agree subject",), requirement("disagreeing"), {}),
    (("passive form has no by-phrase",), requirement("agentless"), {"p1": "t1"}),
    (("precondition use term", "term is `action`"), line(WHILE_ACTION), {}),
    (("trigger use term", "term is `state`"), requirement("misaspected"), {}),
    (("precondition use term", "term is `state`"), requirement("verbal"), {}),
    (("trigger use recipient",), requirement("addressed"), {}),
    (("requirement not conform language reference",), line(NONCONFORMING), {}),
    # model parse: the constructs
    (("capability has requirement", "requirement use `only`", "requirement allow act"), capability("restricting"),
     {}),
    (("requirement use `not-condition`",), requirement("negating"), {}),
    (("requirement use `bare-plural`",), requirement("plural"), {}),
    (("requirement use `option-set-to`",), requirement("optioned"), {}),
    (("requirement use `of-relation`",), requirement("genitive"), {}),
    (("requirement use `no-noun`",), requirement("denying"), {}),
    (("requirement use `compound`",), requirement("compound"), {}),
    (("requirement use `only`",), requirement("restrictive"), {}),
    (("requirement use `rc-object`",), requirement("relative"), {}),
    (("requirement use `rc-whose`",), requirement("possessive"), {}),
    (("requirement use `this`",), requirement("indexical"), {}),
    (("requirement has logical form", "requirement conform language reference"), nothing, {}),
    (("this corpus holds logical form",), nothing, {}),
    (("requirement has logical form",), requirement("ambiguous"), {}),
    (("definite noun phrase has no antecedent",), requirement("antecedentless"), {"d1": "t1"}),
    (("precondition use negated indefinite",), requirement("unquantified"), {"n1": "t1"}),
    (("requirement has no trigger",), requirement("triggerless"), {}),
    (("run on fragment",), requirement("unfinished"), {"f1": "thing#r1"}),
    # model parse: counts, time and modality
    (("requirement use `count`",), requirement("counted"), {}),
    (("count contradict count",), capability("overcounted"), {}),
    (("requirement use `moment-compare`",), requirement("timed"), {}),
    (("requirement use clock trigger",), requirement("clocked"), {}),
    (("precondition use perfect",), requirement("historical"), {}),
    (("number has no unit",), requirement("unitless"), {}),
    (("requirement use `may`",), requirement("permissive"), {}),
    (("requirement use `always-never`",), requirement("invariant"), {}),
    # model parse: the caches
    (("parse cache holds parse",), CACHE.held, {}),
    (("compiled grammar exist",), CACHE.compiled, {}),
    (("no parse cache holds parse",), CACHE.unheld, {}),
    # model logic and model explain
    (("`model` not unify code",), capability("unpairable"), {"r5": "r1"}),
    (("requirement use `every`",), capability("exhaustive"), {}),
    (("capability has requirement", "requirement override requirement"), capability("overriding"), {}),
    (("requirement override requirement",), requirement("overridden"), {"r4": "r2"}),
    (("universal condition forbid act",), capability("contravening"), {}),
    (("requirement permit act",), capability("forbidding"), {}),
    (("requirement add no consequence",), requirement("restating"), {}),
    (("requirement use refusal",), requirement("refusing"), {}),
    (("capability is `codified-2`",), capability("recodified"), {}),
    (("capability has requirement", "requirement conform language reference"), capability("recodified"), {}),
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
    raise AssertionError("no world of design-model-check has the facts %s" % sorted(facts))
