"""analysis-tools' base branch (code-analysis r15, r16, b490), beside analysis_tools_handlers.py: a Python file that
differs from this base branch, or does not, kept as the branch the project is on when `tools` runs
(analysis_tools_world's `branched`)."""
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
