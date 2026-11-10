"""The registry's handlers of the (template, term) keys whose one registry handler was supervision's, retired in
plugin 2.0.0 (workflow simplification plan 9, Task 3). A feature's own handler (`work_queue_world.local`) takes each
of these steps first; these are what is left when none does. The Given records nothing, as supervision's recorded
nothing another feature read: the When's handler reads the scenario's text. A Then or a When no feature's handler
took fails, naming the step, so that no step passes unchecked. The keys of requests' codified-2 steps (read in the
step grammar 4, whose terms are the verbs and row words) are here too: requests' locals take each of its steps."""
from vocab import handler


@handler("GivenR", "on")
def given_on(step):
    """`the question q1 is on the work-item w1`: read off the scenario by the handler of its When."""


@handler("GivenK", "text")
@handler("GivenK", "citation")
@handler("GivenK", "field block")
@handler("GivenK", "host")
def given_instance(step):
    """`a host h1`: an instance with no file of its own, which the conditions that name it build (requests')."""


def untaken(step):
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


for _template, _term in (("ThenDoes", "keep"), ("ThenDoes", "remove"), ("ThenR", "for"), ("ThenR", "on"),
                       ("WhenHappens", "merge"),
                       # requests' (codified-2): its steps are taken by requests_handlers_givens' and _thens' locals
                       ("GivenK", "comment"), ("GivenDoes", "address"), ("GivenDoes", "block"), ("GivenDoes", "has"),
                       ("GivenDoes", "holds"), ("GivenDoes", "lack"), ("GivenDoes", "on"), ("GivenDoes", "originate"),
                       ("GivenDoes", "proposed in"), ("GivenDoes", "reject"), ("GivenDoesNot", "address"),
                       ("GivenDoesNot", "holds"), ("GivenDoesNot", "identify"), ("GivenDoesNot", "originate"),
                       ("ThenDoes", "assign"), ("ThenDoes", "has"), ("ThenDoes", "name"), ("ThenDoes", "proposed in"),
                       ("ThenDoes", "raised for"), ("ThenDoes", "refuse"), ("ThenDoes", "set")):
    handler(_template, _term)(untaken)
