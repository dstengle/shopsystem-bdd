"""design-model-check's worlds of a response that makes a request with its parameters (b543, `response-request`), rows
design_model_check_worlds' TABLE takes first: the construct catalogue's request context
(grammar/corpus/constructs/request/: the decisions core and the registry port beside it), r1 a line whose response
asks the registry to publish the design-decision with a summary, which parsing's scenarios parse (and read in the
logical form) and consistency's translate with `spec logic`; and r1 a trigger on the registry's reply to the request
to publish the design-decision (b626, `reply-trigger`), or to publish every design-decision, a plural object no
reading gives a request (b726), and on its failure of that request (b727, `reply-failure`); and two lines on one
trigger whose responses ask the registry to lodge the design-decision on a shelf with its keeper (`oblique-role`, a
thing parameter), the second with a summary too, which `spec explain` of the second reads the first's request in
(b742)."""
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
VALUE = _sibling("design_model_check_worlds_value.py", "shop_design_model_check_worlds_value")
REQUESTING = ("When the person enters a design-decision, the decisions service shall publish the design-decision "
              "with the summary `s1`.")
REPLYING = ("When the registry completes the request to publish a design-decision, the decisions service shall keep "
            "the design-decision.")
FAILING = ("When the registry fails the request to publish a design-decision, the decisions service shall keep the "
           "design-decision.")

PLURAL = ("When the registry completes the request to publish every design-decision, the decisions service shall keep "
          "a design-decision.")
LODGING = ("While a shelf has a keeper, when the person enters a design-decision, the decisions service shall lodge the "
           "design-decision on the shelf with the keeper")
SHELF = "\nobject shelf\n  relations: has → keeper (one)\n\nobject keeper\n"
SHELVED = ("\n- **shelf** (noun) → object shelf. Plural: shelves.\n"
           "- **keeper** (noun) → object keeper. Plural: keepers.\n")
LODGE = "  operation lodge(design-decision, shelf, keeper, summary)  outcomes: done\n"
LODGED = ("\n- **lodge** (verb, action) → operation registry.lodge. Forms: lodges, lodged. Frame: <actor> lodges "
          "<design-decision> on <shelf>.\n")


def lodging(step):
    """The request context with a shelf, its keeper and the registry's lodge (b742): thing's r1 lodges the
    design-decision on the shelf with the keeper, r2 with the summary `s1` too; r2 the requirement explained."""
    VALUE.line(LODGING + ".", LODGING + " and the summary `s1`.")(step)
    spec = step.repo / "spec"
    for path, end, more in (("model/decisions.md", "\nactor the person", SHELF), ("model/registry.md", "```\n", LODGE)):
        text = (spec / path).read_text()
        at = text.rindex(end)
        (spec / path).write_text(text[:at] + more + text[at:])
    for path, more in (("vocabulary/decisions.md", SHELVED), ("vocabulary/registry.md", LODGED)):
        (spec / path).write_text((spec / path).read_text().rstrip("\n") + more)
    step.context.setdefault("ids", {})["r2"] = "thing#r2"
    H.says(step, "r1", "thing#r1")
    H.says(step, "c1", "shall lodge a design-decision on a shelf with a keeper (by")


def requesting(step, text=REQUESTING):
    """The request context with r1 the line; the capability the When names (`spec logic` on it) run as `thing`."""
    VALUE.line(text)(step)
    for name in step.names:
        step.context.setdefault("ids", {})[name] = "thing"


def replying(step):
    """The request context with r1 a trigger on the registry's reply to the request to publish (b626)."""
    requesting(step, REPLYING)


def failing(step):
    """The request context with r1 a trigger on the registry's failure of the request to publish (b727), written here,
    not read off the catalogue."""
    requesting(step, FAILING)


def plural(step):
    """The request context with r1 a trigger on the reply to a request of a plural object (b726)."""
    requesting(step, PLURAL)


ROWS = [
    (("requirement has trigger", "requirement has consequence", "requirement use `response-request`",
      "requirement use `oblique-role`"), lodging, {}),
    (("requirement use `reply-failure`",), failing, {}),
    (("requirement use `reply-trigger`", "requirement has plural object"), plural, {}),
    (("requirement use `reply-trigger`",), replying, {}),
    (("requirement use `response-request`",), requesting, {}),
]
