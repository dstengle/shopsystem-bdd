"""parsing's Then of a value in use (r18, b418): read off the logical form `spec parse --form` printed of the
`param-of` line (design_model_check_worlds_value's IN_USE), a request's parameter whose value is a referent that is
another referent's value of the attribute the parameter names: `param(e, T, v)` beside `T(x) = v` (design-decision
0110), with no atom of its own."""
import importlib.util
import re
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


W = _sibling("work_queue_world.py", "shop_work_queue_world")
PARAM = re.compile(r"param\((e\d+), ([a-z ]+), (x\d+)\)")


def in_use(form):
    """[(parameter, value referent, owner referent)] of each parameter whose value is another referent's value."""
    return [(p, v, owner) for _, p, v in PARAM.findall(form)
            for owner in re.findall(r"%s\((x\d+)\) = %s\b" % (re.escape(p), v), form)]


@W.local("ThenDoes")
def holds(step):
    """The logical form l1 holds the value in use v1."""
    if sys.modules["vocab"].origin(step.request.node) != "parsing" or step.event != "holds" \
            or not step.subject.startswith("the logical form") or not step.nps[0].startswith("the value in use"):
        return False
    form = step.context["result"].stdout
    assert in_use(form), ("no parameter's value is another thing's value", form)
    return None
