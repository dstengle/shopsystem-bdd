"""analysis-tools' base branch (code-analysis r15, r16, b490), beside analysis_tools_handlers.py: a Python file that
differs from this base branch, or does not, kept as the branch the project is on when `tools` runs
(analysis_tools_world's `branched`); and a test that breaks (code-analysis r1, b748): its file asserts False, as
analysis_tools_handlers' failing test."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

four = sys.modules["shop_world_four"].four   # loaded before the handlers, by the glob of world_*.py


@four("GivenDoes", "differ", "analysis-tools")
def given_differs(step):
    step.context["branch"] = "differs"


@four("GivenDoesNot", "differ", "analysis-tools")
def given_same(step):
    step.context["branch"] = "same"


@four("GivenDoes", "break", "analysis-tools")
def given_breaks(step):
    name = step.names[0].strip("`")
    step.context.setdefault("files", {})["tests/test_%s.py" % name] = "def test_%s():\n    assert False\n" % name
