"""design-model-check's worlds of a negated restriction of an object beside a value (b232), rows
design_model_check_worlds' TABLE takes in its place: r1 forbids printing a stage whose status is not `done`, r2 obliges
printing a stage whose status is `open` (another value, which rules `done` out: an L1) or `done` (the code r1 names:
no finding). Each world is codified2_world's, its r1 and r2 the lines here."""
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


RUN = "When the person runs `work start`, `work` shall "
UNDONE = RUN + "not print a stage whose status is not `done`."
OPEN = RUN + "print a stage whose status is `open`."
DONE = RUN + "print a stage whose status is `done`."

NEGATED = ("requirement use `not-relative`", "requirement forbid act", "requirement oblige act",
           "requirement use `rc-whose`")
ROWS = [
    (NEGATED + ("requirement not use code",), line(UNDONE, OPEN), {}),
    (NEGATED + ("requirement use code",), line(UNDONE, DONE), {}),
]
