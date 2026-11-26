"""design-model-check's worlds of a response that makes a request with its parameters (b543, `response-request`), rows
design_model_check_worlds' TABLE takes first: the construct catalogue's request context
(grammar/corpus/constructs/request/: the decisions core and the registry port beside it), r1 a line whose response
asks the registry to publish the design-decision with a summary, which parsing's scenarios parse (and read in the
logical form) and consistency's translate with `spec logic`; and r1 a trigger on the registry's reply to the request
to publish the design-decision (b626, `reply-trigger`)."""
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
REQUESTING = ("When the person enters a design-decision, the decisions service shall publish the design-decision "
              "with the summary `s1`.")
REPLYING = ("When the registry completes the request to publish a design-decision, the decisions service shall keep "
            "the design-decision.")


def requesting(step, text=REQUESTING):
    """The request context with r1 the line; the capability the When names (`spec logic` on it) run as `thing`."""
    VALUE.line(text)(step)
    for name in step.names:
        step.context.setdefault("ids", {})[name] = "thing"


def replying(step):
    """The request context with r1 a trigger on the registry's reply to the request to publish (b626)."""
    requesting(step, REPLYING)


ROWS = [
    (("requirement use `reply-trigger`",), replying, {}),
    (("requirement use `response-request`",), requesting, {}),
]
