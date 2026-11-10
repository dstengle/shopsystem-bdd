"""Handlers of design-model-check's Givens in grammar 4 (b152): each instance and each state a Given says is kept as a
fact (`the term t1 violates `v_t4`` as "term violate `v_t4`"), and at the When the facts pick the world that
design_model_check_worlds.py builds of them (`built`), with what the output names each instance by. The Thens of a
refusal (`refuse`, `name`, of any tool's run) and of what `model` used or printed read the run back.

The keys are the registry's (`features vocab --check` reads it); where another feature's handler holds the key
(`GivenK` of a kind world_nodes writes, `ThenDoes use` of the batches) a `work_queue_world.local` of this feature only
comes first and passes any other feature's step on."""
import importlib.util
import re
import sys
from pathlib import Path

from vocab import handler


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


W = _sibling("work_queue_world.py", "shop_work_queue_world")
H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
WORLDS = _sibling("design_model_check_worlds.py", "shop_design_model_check_worlds")
local = W.local
FEATURE = "design-model-check.feature"
NAME = re.compile(r"^[a-z][a-z-]*[1-9]\d*$")


def ours(step):
    """True for a step of features/design-model-check.feature."""
    scenario = getattr(step.request.node.function, "__scenario__", None)
    return scenario is not None and Path(scenario.feature.filename).name == FEATURE


def phrase(text):
    """A noun phrase as a fact says it: an instance by its kind (`the term t1` "term"), else its words without the
    article (`the request form` "request form", `no job`, `` `v_t4` ``)."""
    words = re.sub(r"^(the|an?) ", "", text).split()
    return " ".join(words[:-1] if len(words) > 1 and NAME.match(words[-1]) else words)


def remember(step, fact):
    step.context.setdefault("facts", []).append(fact)
    step.context["build"] = WORLDS.build


# The kinds only this feature's Givens bring in: nothing is written of one, its instance is a fact (`instance`).
KINDS = ("act", "antecedent", "assignment", "boxed noun phrase", "catalogue entry", "clash", "clock trigger",
         "comparison", "compound noun", "consequence", "count", "definite noun phrase", "demonstrative",
         "distributive genitive", "fact", "file form", "frame", "genitive", "index entry", "inner genitive",
         "later sense", "logical form", "modal adverb", "negated indefinite", "negated modifier", "negation",
         "negative quantifier", "noun phrase", "number", "object", "oblique recipient", "option", "pack",
         "passive form", "perfect", "permission", "plural subject", "precondition", "preposition", "recipient",
         "refusal", "relative clause", "requirement id", "restriction", "rule", "self-reference", "sense", "subject",
         "text", "trigger", "unification failure", "universal quantifier", "whose clause")
STATES = ("add", "allow", "conform", "contradict", "disagree", "forbid", "has", "holds", "import", "lack", "mismatch",
          "oblige", "omit", "override", "permit", "redefine", "refer", "use", "violate")


@local("GivenK")
def instance(step):
    """`a precondition p1`: its kind kept under its name and as a fact; the step then goes on to the registry's
    handler (world_nodes' for a kind it writes, else `brought_in`)."""
    if ours(step):
        step.context.setdefault("kinds", {}).setdefault(step.kind, []).append(step.names[0])
        remember(step, step.kind)
    return False


for _kind in KINDS:
    @handler("GivenK", _kind)
    def brought_in(step):
        """An instance of a kind of the spec's words: the local `instance` kept it."""


def state(step):
    """`the requirement r1 uses the negation n1`: "requirement use negation"; negated, "not" before the verb."""
    verb = ("not " if step.template.endswith("Not") else "") + step.event
    remember(step, " ".join([phrase(step.subject), verb] + [phrase(np) for np in step.nps]))


for _verb in STATES:
    handler("GivenDoes", _verb)(state)
for _verb in ("conform", "holds", "import"):
    handler("GivenDoesNot", _verb)(state)


@handler("GivenK_A", "capability")
@handler("GivenK_A", "term")
def value(step):
    """`the term t1 is `state``: "term is `state`"."""
    remember(step, "%s is %s" % (step.kind, step.text.rsplit(" is ", 1)[1]))


@handler("ThenDoes", "refuse")
@handler("ThenDoes", "name")
@handler("ThenDoes", "has")
@handler("ThenDoes", "import")
def then_does(step):
    """The Thens that say what a tool did: refuse the command (an error exit), name an instance (by what a Given said
    it is named by) or a code; and design-model-check's of what the facts gave: a logical form, an interpreter that
    imports clingo (design_model_check_worlds' `then`)."""
    done = step.context["result"]
    if step.event == "refuse":
        assert done.returncode != 0, (step.text, done.stdout)
    elif step.event == "name":
        for word in H.named(step):
            assert word in done.stdout + done.stderr, (step.text, word, done.stdout, done.stderr)
    else:
        assert WORLDS.then(step, done) is not False, "no Then of design-model-check says %r" % step.text


@local("ThenDoes")
@local("ThenDoes", "requirement")
def then_uses(step):
    """`model` uses the interpreter i2, the requirement r4 uses the refusal r3 (the registry's `use` is the
    batches'), and the refusal and naming Thens of a step read in grammar 3 (`the requirement r1` its kind)."""
    if not ours(step) or step.event not in ("use", "refuse", "name"):
        return False
    then_does(step)


@local("WhenRuns")
def run_on(step):
    """`model parse` on the fragment f1: "run on fragment", for the world it picks; the run is the registry's, but
    `model decisions --check`'s, whose registry handler (decision-tiers') writes the index first."""
    if not ours(step):
        return False
    if step.names:
        remember(step, "run on " + phrase(step.text.split(" on ", 1)[1]))
    if step.term != "`model decisions --check`":
        return False
    H.run_model(step, "decisions", "--check")


@local("ThenPrintsNot")
def no_violation(step):
    """`model` does not print a violation: it printed that it found none."""
    if not ours(step) or step.nps != ["a violation"]:
        return False
    done = step.context["result"]
    assert done.returncode == 0 and "0 violations" in done.stdout, (done.stdout, done.stderr)


@handler("WhenRuns", "`work record --about`")
def work_record_about(step):
    """`work record` with the `--about` the text a Given gave (design_model_check_handlers_forms)."""
    _sibling("design_model_check_handlers_forms.py", "shop_design_model_check_handlers_forms").work_record(step)
