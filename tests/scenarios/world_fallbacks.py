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


@handler("GivenK")
@handler("GivenK_A")
@handler("GivenDoes")
@handler("GivenDoesNot")
def given_recorded(step):
    """A codified-2 feature's Given of an instance, a value or a link that no handler of its kind or verb takes (b240):
    the scenario's example data holds the thing, and its When's handler reads the given block, so it records nothing."""


for _template, _term in (("ThenDoes", "has"), ("ThenDoes", "holds"), ("ThenDoes", "for"), ("ThenDoes", "give"),
                         ("ThenDoes", "name"), ("ThenDoes", "refuse"), ("ThenDoes", "supersede"),
                         ("ThenDoes", "include"), ("ThenDoes", "rewrite"), ("GivenK_C", "repository"),
                         ("ThenDoes", "relocate"), ("ThenDoes", "rename"), ("ThenK_A", "design-decision")):
    handler(_template, _term)(untaken)
