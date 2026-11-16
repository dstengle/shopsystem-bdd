"""The registry's handlers of the (template, term) keys whose one registry handler was supervision's, retired in
plugin 0.31.0 (workflow simplification plan 9, Task 3). A feature's own handler (`work_queue_world.local`) takes each
of these steps first; these are what is left when none does. The Given records nothing, as supervision's recorded
nothing another feature read: the When's handler reads the scenario's text. A Then or a When no feature's handler
took fails, naming the step, so that no step passes unchecked. The keys of requests' codified-2 steps (read in the
step grammar 4, whose terms are the verbs and row words) are here too: requests' locals take each of its steps."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


@handler("GivenR", "on")
def given_on(step):
    """`the question q1 is on the work-item w1`: read off the scenario by the handler of its When."""


@handler("GivenK", "text")
@handler("GivenK", "entry")
@handler("GivenK", "GitHub repository")
@handler("GivenK", "requirement grammar")
def given_instance(step):
    """`an entry e1`: an instance with no file of its own, which the conditions that name it build (requests')."""


def untaken(step):
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


for _template, _term in (("ThenDoes", "keep"), ("ThenDoes", "remove"), ("ThenR", "for"), ("ThenR", "on"),
                       ("WhenHappens", "merge"),
                       # requests' (codified-2): its steps are taken by requests_handlers_givens' and _thens' locals
                       ("GivenK", "comment"), ("GivenK_A", "comment"), ("GivenK_A", "entry"), ("GivenK_A", "issue"),
                       ("GivenDoes", "address"), ("GivenDoes", "has"), ("GivenDoes", "holds"),
                       ("GivenDoes", "on"), ("GivenDoes", "originate"), ("GivenDoes", "proposed in"),
                       ("GivenDoes", "reject"), ("GivenDoesNot", "address"), ("GivenDoesNot", "holds"),
                       ("GivenDoesNot", "identify"), ("GivenDoesNot", "originate"), ("ThenDoes", "has"),
                       ("ThenDoes", "proposed in"), ("ThenDoes", "raised for"),
                       ("ThenDoes", "set")):
    handler(_template, _term)(untaken)


# A codified-2 step (b240) whose verb or row word many features say: each feature's `local` handler takes it.
for _template, _term in (("GivenDoes", "has"), ("ThenDoes", "has"), ("ThenDoes", "holds"), ("ThenDoes", "run"),
                         ("ThenDoes", "set"), ("ThenDoes", "on"), ("ThenDoes", "for"), ("ThenDoes", "from"),
                         ("ThenDoes", "list"), ("GivenK", "title"),
                         ("GivenK_C", "universal condition")):     # readiness's nonexistent condition, kept from 3.x
    handler(_template, _term)(untaken)


@handler("GivenK")
@handler("GivenK_A")
@handler("GivenDoes")
@handler("GivenDoesNot")
def given_recorded(step):
    """A codified-2 feature's Given of an instance, a value or a link that no handler of its kind or verb takes (b240):
    the scenario's example data holds the thing, and its When's handler reads the given block, so it records nothing."""


for _template, _term in (("ThenDoes", "has"), ("ThenDoes", "holds"), ("ThenDoes", "for"), ("ThenDoes", "give"),
                         ("ThenDoes", "supersede"),
                         ("ThenDoes", "include"), ("ThenDoes", "rewrite"), ("GivenK_C", "repository"),
                         ("ThenDoes", "relocate"), ("ThenDoes", "rename"), ("ThenK_A", "design-decision"),
                         ("ThenDoesNot", "rewrite"), ("ThenDoesNot", "name")):     # counter-examples' (b273)
    handler(_template, _term)(untaken)

# The keys of grammar 4's steps that more than one codified-2 feature may say (b240 phase 20): a feature's own `local`
# handler of the template takes its steps (readiness_handlers_givens.py, readiness_handlers_thens.py); these are
# what is left when none does.
for _template, _term in (("ThenDoes", "holds"), ("ThenDoes", "set"),
                         ("GivenDoes", "has"), ("GivenDoes", "holds"), ("GivenDoes", "pass"),
                         ("GivenDoes", "violate"), ("GivenDoesNot", "pass"), ("GivenDoesNot", "meet"),
                         ("GivenK", "relation row"), ("GivenK", "upstream entry"),
                         ("GivenK", "given block"), ("GivenK", "bar check"),
                         ("GivenK", "step"), ("GivenK", "rule"), ("GivenK", "requirement id"),
                         ("GivenK", "universal condition id")):
    handler(_template, _term)(untaken)


# The keys of grammar 4's steps that more than one codified-2 feature may say (b240): a feature's own `local` handler
# takes its steps (design-model-check's in design_model_check_handlers_facts.py); these are what is left when none does.
for _template, _term in (("GivenDoes", "has"), ("GivenDoes", "holds"), ("GivenDoes", "violate"),
                         ("GivenDoesNot", "holds"), ("GivenK", "rule"), ("GivenK", "requirement id"),
                         ):
    handler(_template, _term)(untaken)


def _shared(module, name):
    """The module every handler module shares, loaded by its path when none has loaded it yet."""
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


# The Then that states an order (b285, decision 0093), in any feature: world_order's check of what the command printed,
# a `local` of ThenPrints tried after every feature's own, which takes no step whose `order` is set.
_shared("shop_work_queue_world", "work_queue_world.py").local("ThenPrints")(
    _shared("shop_world_order", "world_order.py").then)
