"""The registry's handlers of the (template, term) keys whose one registry handler was supervision's, retired in
plugin 2.0.0 (workflow simplification plan 9, Task 3). A feature's own handler (`work_queue_world.local`) takes each
of these steps first; these are what is left when none does. The Given records nothing, as supervision's recorded
nothing another feature read: the When's handler reads the scenario's text. A Then or a When no feature's handler
took fails, naming the step, so that no step passes unchecked."""
from vocab import handler


@handler("GivenR", "on")
def given_on(step):
    """`the question q1 is on the work-item w1`: read off the scenario by the handler of its When."""


def untaken(step):
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


for _template, _term in (("ThenDoes", "keep"), ("ThenDoes", "remove"), ("ThenR", "for"), ("ThenR", "on"),
                       ("WhenHappens", "merge")):
    handler(_template, _term)(untaken)


# The keys of grammar 4's steps that more than one codified-2 feature may say (b240): a feature's own `local` handler
# takes its steps (design-model-check's in design_model_check_handlers_facts.py); these are what is left when none does.
for _template, _term in (("GivenDoes", "has"), ("GivenDoes", "holds"), ("GivenDoes", "violate"),
                         ("GivenDoesNot", "holds"), ("GivenK", "rule"), ("GivenK", "requirement id"),
                         ("GivenK", "text"), ("ThenDoes", "refuse"), ("ThenDoes", "name")):
    handler(_template, _term)(untaken)
