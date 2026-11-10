"""Handlers of design-model-check's `model explain` (the CNL 4 design, I13b): the command run on the requirement the
When names, by the id a Given gave it (thing#r1 of the base world when none did), with the id kept in `says` so that
a Then naming the requirement looks for the id in the output."""
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


@handler("WhenRuns", "`model explain`")
def model_explain(step):
    name = step.names[0]
    ident = step.context.get("ids", {}).get(name, "thing#r1")
    H.says(step, name, ident)
    H.run_model(step, "explain", ident)
