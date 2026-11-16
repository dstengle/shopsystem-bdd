"""design-model-check's worlds of comparisons and orders (b275), rows design_model_check_worlds' TABLE takes first:
one thing's value compared with another's (`value-compare`, `value-same`), of an attribute with no value order
(refused, naming it), under a line that forbids what it obliges (an L1) and beside one whose comparison of the same
two values contradicts it (none); an order on a collection (`order-by`) and on a printed every (`order-by-every`), of
an attribute with no value order (refused, naming it), printed by `model parse --form`, and two in opposite directions
on one trigger (an L1), and on every K that a verb whose one frame names K takes (b300); an order in a precondition, in a trigger and in a forbidden act (b285, refused, naming it).
Each world is codified2_world's, its r1 (r2) the lines here."""
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
C2 = _sibling("codified2_world.py", "shop_codified2_world")


def line(*texts):
    return lambda step: C2.context(step.repo, H.PATH, list(texts))


COMPARED = ("While the version of a file is after the version of another file, when the person runs `work start`, "
            "`work` shall print the file.")
SAME = ("While the version of a file is the same as the version of another file, when the person runs `work start`, "
        "`work` shall print the file.")
UNORDERED = ("While the status of a stage is after the status of another stage, when the person runs `work start`, "
             "`work` shall print the stage.")
# the `a` file is one thing of both lines, the written file another: r1's comparison and r2's contradict
AFTER = ("While the version of the `a` file is after the version of a file, when a session writes the file, `work` "
         "shall print the file.")
BEFORE = ("While the version of the `a` file is before the version of a file, when a session writes the file, `work` "
          "shall not print the file.")
UNPRINTED = "When a session writes a file, `work` shall not print the file."
HELD = ("When the person runs `work start`, `work` shall print a worktree that holds a file, ordered by version, in "
        "descending order.")
EVERY = "When the person runs `work start`, `work` shall print every file, ordered by version, in ascending order."
# b300: an order on every K that a verb whose one frame names K (give: agent gives file to agent) takes
GIVEN = ("When the person runs `work start`, `work` shall give every file, ordered by version, in ascending order to "
         "the person.")
DESCENDING = "When the person runs `work start`, `work` shall print every file, ordered by version, in descending order."
PRECONDITION = ("While a session has a worktree that holds a file, ordered by version, in descending order, when the "
                "person runs `work start`, `work` shall print the worktree.")
TRIGGER = ("When the person runs `work start` on a worktree that holds a file, ordered by version, in descending order, "
           "`work` shall print the worktree.")
FORBIDDEN = ("When the person runs `work start`, `work` shall not print a worktree that holds a file, ordered by "
             "version, in descending order.")
NAMED = {"o1": "ordered by version, in descending order"}
OUTCOMES = "When the person runs `work start`, `work` shall print every line, ordered by outcome, in ascending order."

# two senses of one attribute word (b287): the version of a worktree beside the fixture's version of a file, of the
# file's value order or of another (the scenario's second value order)
SENSE = ("- **version** (attribute of worktree): the release a worktree is checked out at. Values (noun): `1.0.0`, "
         "`3.0.0`. Order: %s.\n")
CROSS = ("While the version of a worktree is after the version of a file, when the person runs `work start`, `work` "
         "shall print the file.")
CROSS_SAME = ("While the version of a worktree is the same as the version of a file, when the person runs `work start`, "
              "`work` shall print the file.")
CROSS_AFTER = ("While the version of the `a` worktree is after the version of a file, when a session writes the file, "
               "`work` shall print the file.")


def senses(*texts):
    """A builder: the world of `texts` with the worktree's sense of version, as listed when the scenario gave a
    second value order, else by number as the file's."""
    def build(step):
        line(*texts)(step)
        orders = step.context.get("kinds", {}).get("value order", [])
        index = step.repo / "spec" / "index.md"
        index.write_text(index.read_text() + SENSE % ("as listed" if len(orders) > 1 else "by number"))
    return build


SENSED = ("term has sense", "sense has value order")
ROWS = [
    (SENSED + ("requirement use `value-compare`", "requirement oblige act", "requirement forbid act"),
     senses(CROSS_AFTER, UNPRINTED), {}),
    (SENSED + ("requirement use `value-compare`",), senses(CROSS), {"t1": "the senses of version"}),
    (SENSED + ("requirement use `value-same`",), senses(CROSS_SAME), {"t1": "the senses of version"}),
    (("requirement has precondition", "precondition use order"), line(PRECONDITION), NAMED),
    (("requirement has trigger", "trigger use order"), line(TRIGGER), NAMED),
    (("act holds order", "requirement forbid act"), line(FORBIDDEN), NAMED),
    (("requirement use `value-compare`", "requirement use term", "term has no value order"), line(UNORDERED),
     {"t1": "status"}),
    (("requirement use `value-compare`", "requirement oblige act", "requirement forbid act"), line(AFTER, UNPRINTED),
     {}),
    (("comparison contradict comparison", "requirement oblige act", "requirement forbid act"), line(AFTER, BEFORE), {}),
    (("requirement use `value-compare`",), line(COMPARED), {}),
    (("requirement use `value-same`",), line(SAME), {}),
    (("requirement use order", "order on term", "term has no value order"), line(OUTCOMES), {"t1": "outcome"}),
    (("capability holds order", "order contradict order"), line(EVERY, DESCENDING), {}),
    (("requirement use `order-by`",), line(HELD), {}),
    (("requirement use `order-by-every`", "no frame take `thing`", "requirement use verb"), line(GIVEN), {}),
    (("requirement use `order-by-every`",), line(EVERY), {}),
    (("requirement use order",), line(EVERY), {"o1": "ordered(x4, version, ascending)"}),
]
