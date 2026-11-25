"""design-model-check's worlds of a request followed from one line to another's trigger (consistency r37-r39, b545,
decision 0118), rows design_model_check_worlds' TABLE takes first, in the construct catalogue's request context
(design_model_check_worlds_value's `line`): the decisions service's request to publish a design-decision with the
summary `s1`, the lines on that request or on a publish of no parameter (they govern the registry's publish) and a line on the person's entering
that their consequences entail (an L8 through the request, r37; through a consequence of a governing line that
triggers a third line, r38); and two lines on one trigger, one obliging and one forbidding a publish of another
summary (no L1, r39), or a publish of no parameter (an L1, r40, b571); and on one trigger a counted publish beside a
forbidden one (an L1, r41), or a publish of a design-decision whose tier is `check` beside a publish of only those
whose tier is `judgement` (an L1, r42, b579)."""
import importlib.util
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


VALUE = _sibling("design_model_check_worlds_value.py", "shop_design_model_check_worlds_value")
H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
ENTERS = "When the person enters a design-decision, "
PUBLISHES = "When the decisions service publishes a design-decision with the summary `s1`, "
REQUESTING = ENTERS + "the decisions service shall publish the design-decision with the summary `s1`."
KEEPING = PUBLISHES + "the registry shall keep the design-decision."
NOTIFYING = PUBLISHES + "the registry shall notify the person of the design-decision."
NAMING = PUBLISHES + "the registry shall name the design-decision."
NAMING_ANY = "When the decisions service publishes a design-decision, the registry shall name the design-decision."
ENTAILED = (ENTERS + "the registry shall keep the design-decision, notify the person of the design-decision and name "
            "the design-decision.")
OTHER = "When the person enters a design-decision with the tier `judgement`, the decisions service shall keep the " \
        "design-decision."
KEPT = "When the registry keeps a design-decision, the registry shall notify the person of the design-decision."
CHAINED = ENTERS + "the registry shall notify the person of the design-decision."
FORBIDDING = ENTERS + "the decisions service shall not publish the design-decision with the summary `s2`."
FORBIDDING_ANY = ENTERS + "the decisions service shall not publish the design-decision."
COUNTING = ENTERS + "the decisions service shall publish at least two design-decisions."
FORBIDDING_A = ENTERS + "the decisions service shall not publish a design-decision."
CHECKED = ENTERS + "the decisions service shall publish a design-decision whose tier is `check`."
ONLY = ENTERS + "the decisions service shall publish only design-decisions whose tier is `judgement`."


def named(lines, names):
    """A builder: the request context with `lines` as thing's r1, r2 ..., each scenario name said as its line's id."""
    def build(step):
        VALUE.line(*lines)(step)
        for name, n in names.items():
            H.says(step, name, "thing#r%d" % n)
    return build


ROWS = [
    # r37: r1 requests publish with the summary `s1`; r2, r4 govern it on that summary, r5 on no parameter, each
    # forcing a Then of r3; r6 governs no publish
    (("requirement use `response-request`", "requirement govern operation", "requirement not govern operation"),
     named([REQUESTING, KEEPING, ENTAILED, NOTIFYING, NAMING_ANY, OTHER],
           {"r1": 1, "r2": 2, "r3": 3, "r4": 4, "r5": 5, "r6": 6}), {}),
    # r38: r1 governs publish, its consequence (keep) the trigger of r2, whose consequence r4 states; r3 requests
    (("requirement use `response-request`", "requirement govern operation", "trigger use consequence"),
     named([KEEPING, KEPT, REQUESTING, CHAINED], {"r1": 1, "r2": 2, "r3": 3, "r4": 4}), {}),
    # r39: r1 obliges a publish of `s1`, r2 forbids one of `s2`, on one trigger
    (("requirement use `response-request`", "requirement forbid act", "requirement not use code"),
     named([REQUESTING, FORBIDDING], {"r1": 1, "r2": 2}), {}),
    # r40: r1 obliges a publish of `s1`, r2 forbids a publish of no parameter, on one trigger
    (("requirement use `response-request`", "requirement forbid act", "requirement use no code"),
     named([REQUESTING, FORBIDDING_ANY], {"r1": 1, "r2": 2}), {}),
    # r41: r1 obliges a publish of at least two design-decisions, r2 forbids a publish, on one trigger
    (("requirement use `count`", "requirement use operation", "requirement forbid act"),
     named([COUNTING, FORBIDDING_A], {"r1": 1, "r2": 2}), {}),
    # r42: r1 obliges a publish of a design-decision outside r2's only, on one trigger
    (("requirement use `only`", "requirement use operation", "requirement oblige act"),
     named([CHECKED, ONLY], {"r1": 1, "r2": 2}), {}),
]
