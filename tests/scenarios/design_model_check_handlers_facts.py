"""Handlers of design-model-check's Givens in grammar 4 (b152, b240 phase 23): each state a Given says is kept as a
fact (`the term t1 violates `v_t4`` as "term violate `v_t4`"), and at the When the facts pick the world that
design_model_check_worlds.py builds of them (`H.built`), with what the output names each instance by. The Thens of a
refusal (`refuse`, `name`) and of what `model` used, read, wrote or translated read the run back.

The keys are the registry's (`features vocab --check` reads it). A key other codified-2 features say too (`has`,
`holds`, `violate`, `refuse`, `name`, `use`, a rule, a requirement id, a text) is world_fallbacks' or another
feature's: a `work_queue_world.local` of this feature only takes the step first and passes any other feature's on."""
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
CACHE = _sibling("design_model_check_handlers_cache.py", "shop_design_model_check_handlers_cache")
local = W.local
FEATURE = "design-model-check.feature"
NAME = re.compile(r"^[a-z][a-z-]*[1-9]\d*$")


def ours(step):
    """True for a step of features/design-model-check.feature."""
    scenario = getattr(getattr(step.request.node, "function", None), "__scenario__", None)
    return scenario is not None and Path(scenario.feature.filename).name == FEATURE


def phrase(text):
    """A noun phrase as a fact says it: an instance by its kind (`the term t1` "term"), else its words without the
    article (`the request form` "request form", `no section`, `` `v_t4` ``)."""
    words = re.sub(r"^(the|an?) ", "", text).split()
    return " ".join(words[:-1] if len(words) > 1 and NAME.match(words[-1]) else words)


def remember(step, fact):
    step.context.setdefault("facts", []).append(fact)
    step.context["build"] = WORLDS.build


# The kinds only this feature's Givens bring in: nothing is written of one, the world its facts pick writes it.
KINDS = ("act", "catalogue entry", "clock trigger", "code", "compiled grammar", "consequence", "count",
         "definite noun phrase", "fact", "file form", "frame", "index entry", "logical form", "negated indefinite",
         "noun phrase", "number", "object", "pack", "parse", "parse cache", "passive form", "perfect", "precondition",
         "preposition", "recipient", "refusal", "sense", "subject", "trigger", "verb")
SHARED = ("rule", "requirement id", "text", "universal condition")


def instance(step):
    """`a precondition p1`: its name kept under its kind."""
    step.context.setdefault("kinds", {}).setdefault(step.kind, []).append(step.names[0])


for _kind in KINDS:
    handler("GivenK", _kind)(instance)


@local("GivenK")
def shared_instance(step):
    """An instance of a kind other features bring in too (world_fallbacks' key)."""
    if not ours(step) or step.kind not in SHARED:
        return False
    instance(step)


def state(step):
    """`the requirement r1 uses the negation n1`: "requirement use negation"; negated, "not" before the verb."""
    verb = ("not " if step.template.endswith("Not") else "") + step.event
    remember(step, " ".join([phrase(step.subject), verb] + [phrase(np) for np in step.nps]))


OWN = {"GivenDoes": ("add", "allow", "contradict", "exist", "forbid", "import", "lack", "oblige", "omit",
                     "override", "permit", "redefine", "refer", "take", "use"),
       "GivenDoesNot": ("agree", "import", "unify", "use")}
for _template, _verbs in OWN.items():
    for _verb in _verbs:
        handler(_template, _verb)(state)


@local("GivenDoes")
@local("GivenDoesNot")
def shared_state(step):
    """`has`, `holds` and `violate` of this feature (world_fallbacks' keys), and `conform` (codified2_world's)."""
    if not ours(step) or step.term not in ("has", "holds", "violate", "conform"):
        return False
    state(step)


@handler("GivenK_A", "capability")
@handler("GivenK_A", "term")
def value(step):
    """`the term t1 is `state``: "term is `state`"; `the term t1 has no part of speech`: "term has no part of
    speech"."""
    if step.values:
        remember(step, "%s is %s" % (step.kind, step.values[0]))
    else:
        remember(step, "%s has no %s" % (step.kind, step.attribute))


@local("ThenDoes")
def then_does(step):
    """What a tool did: refused the command (an error exit), named an instance (by what a Given said it is named by)
    or a code; `model` used the compiled grammar, read the parse cache, wrote the rule catalogue or the parse cache;
    the requirement r4 uses the refusal r3 (its line in `model explain`'s output says the tool shall refuse)."""
    if not ours(step):
        return False
    done = step.context["result"]
    if step.event == "refuse":
        assert done.returncode != 0, (step.text, done.stdout)
    elif step.event == "name":
        for word in H.named(step):
            assert word in done.stdout + done.stderr, (step.text, word, done.stdout, done.stderr)
    elif step.event == "use" and step.nps[0].startswith("the refusal"):
        ident = step.context["says"][step.names[0]]
        lines = [line for line in done.stdout.splitlines() if line.strip().startswith(ident + "  ")]
        assert lines and any(" shall refuse " in line for line in lines), (ident, done.stdout)
    elif step.event == "write" and step.nps[0].startswith("the rule catalogue"):
        assert done.returncode == 0 and (step.repo / "grammar" / "rules.md").is_file(), (done.stdout, done.stderr)
    elif step.event in ("use", "read", "write"):
        return CACHE.then(step, done)
    else:
        return False


@local("ThenDoesNot")
def then_does_not(step):
    """`model` does not write a compiled grammar (design_model_check_handlers_cache)."""
    if not ours(step) or step.event != "write":
        return False
    return CACHE.then(step, step.context["result"])


@handler("ThenDoes", "read")
@handler("ThenDoes", "translate")
def then_own(step):
    """`model` reads the parse cache p1; `model` translates the requirement r1: `model logic` reached the check with
    the requirement (an exit with no line it could not translate)."""
    done = step.context["result"]
    if step.event == "translate":
        assert done.returncode == 0 and "no translation" not in done.stdout + done.stderr, (done.stdout, done.stderr)
    else:
        assert CACHE.then(step, done) is not False, step.text


@local("ThenPrints")
@local("ThenPrintsNot")
def prints(step):
    """`model` prints the file form f1 (design_model_check_handlers_forms'); `model` does not print the capability
    c1."""
    if not ours(step):
        return False
    if step.nps and step.nps[0].startswith("the file form"):
        return _sibling("design_model_check_handlers_forms.py", "shop_design_model_check_handlers_forms") \
            .prints_every_form(step)
    if step.template != "ThenPrintsNot":
        return False
    done = step.context["result"]
    for word in H.named(step):
        assert word not in done.stdout, (step.text, word, done.stdout)
    return None
