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


# A codified-2 step (b240) whose verb or row word many features say: each feature's `local` handler takes it.
for _template, _term in (("GivenDoes", "has"), ("ThenDoes", "has"), ("ThenDoes", "holds"), ("ThenDoes", "run"),
                         ("ThenDoes", "set"), ("ThenDoes", "on"), ("ThenDoes", "for"), ("ThenDoes", "from"),
                         ("ThenDoes", "list"), ("GivenK", "title"),
                         ("GivenK_C", "universal condition")):     # readiness's nonexistent condition, kept from 3.x
    handler(_template, _term)(untaken)
