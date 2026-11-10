"""Handlers of the logical form of design-model-check (b138; the CNL 4 design, I11a): `model parse --form` run on the
requirement r1 of the smallest codified-2 world (codified2_world.py), and what its logical form l1 is printed by."""
import importlib.util
import sys
from pathlib import Path

from vocab import handler


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
C2 = _sibling("codified2_world.py", "shop_codified2_world")

# r1 when no Given wrote one, and the atom of its trigger, which its logical form prints: an event of `end` whose
# subject is the session (x1) and whose object is the stage (x2), the stage the response's "the stage" binds to
LINE = "When a session ends a stage, `work` shall print the stage."
TRIGGER = "end(e1, subject: x1, object: x2)"


@handler("WhenRuns", "`model parse --form`")
def model_parse_form(step):
    """`model parse --form` on the capability file that holds r1, in the codified-2 world."""
    if not (step.repo / "spec" / "capabilities" / "thing.md").is_file():
        C2.context(step.repo, H.PATH, [LINE])
        H.says(step, "l1", TRIGGER)
    H.run_model(step, "parse", "--form", "--file", H.holding(step))
