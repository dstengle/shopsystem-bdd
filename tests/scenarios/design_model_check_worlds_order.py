"""design-model-check's worlds of comparisons and orders (b275), rows design_model_check_worlds' TABLE takes first:
one thing's value compared with another's (`value-compare`, `value-same`), of an attribute with no value order
(refused, naming it), under a line that forbids what it obliges (an L1) and beside one whose comparison of the same
two values contradicts it (none); an order on a collection (`order-by`) and on a printed every (`order-by-every`), of
an attribute with no value order (refused, naming it), printed by `model parse --form`, and two in opposite directions
on one trigger (an L1). Each world is codified2_world's, its r1 (r2) the lines here."""
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
DESCENDING = "When the person runs `work start`, `work` shall print every file, ordered by version, in descending order."
OUTCOMES = "When the person runs `work start`, `work` shall print every line, ordered by outcome, in ascending order."

ROWS = [
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
    (("requirement use `order-by-every`",), line(EVERY), {}),
    (("requirement use order",), line(EVERY), {"o1": "ordered(x4, version, ascending)"}),
]
