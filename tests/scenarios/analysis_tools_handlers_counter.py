"""analysis-tools' counter-examples (b273), beside analysis_tools_handlers.py: the Givens of a thing that fails what
the line says (a test file that holds no test of the function, a test that calls nothing of src/cart.py, an untested
function of another file, a use of another identifier), each written into the scenario's project so that a `tools`
that ignored the restriction would print it, and bound to what it would be printed as."""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from vocab import handler

four = sys.modules["shop_world_four"].four   # loaded before the handlers, by the glob of world_*.py

from scenarios.analysis_tools_handlers import bare, files, function, named

STRAY = "def stray(order):\n    return order\n"     # an untested function of another file than src/cart.py
OTHER = "from cart import total\n\n\ndef other(items):\n    return total(items)\n"   # a use of another identifier


@four("GivenDoesNot", "holds", "analysis-tools")
def given_holds_not(step):
    """A Python file that does not hold a test (a counter-example, b273): a test file of its own whose one test calls
    no function of src/cart.py, which `tools tests-of --by-file` lists only if it lists every test file."""
    path = "tests/test_%s.py" % bare(step.names[0])
    files(step)[path] = "def test_%s_other():\n    assert True\n" % bare(step.names[0])
    named(step)[step.names[0]] = path


@handler("GivenDoesNot", "execute")
def given_executes_not(step):
    """A test that does not execute the function f1 (a counter-example, b273): its file calls nothing of src/cart.py."""
    function(step, step.names[-1], "executed")
    name = bare(step.names[0])
    files(step)["tests/test_%s.py" % name] = "def test_%s():\n    assert True\n" % name
    named(step)[name] = "test_%s" % name


@four("GivenDoesNot", "has", "analysis-tools")
def given_has_not(step):
    """A Python file that does not have a function no test executes (a counter-example, b273): the function is in
    another file, src/stray.py, which `tools untested` on the Python file prints only if it reads every file."""
    files(step)["src/stray.py"] = STRAY
    named(step)[step.names[-1]] = "stray"


@handler("GivenDoesNot", "to")
def given_reference_not(step):
    """A reference that is not to the identifier (a counter-example, b273): a use of another identifier, `total`, in
    src/other.py, which `tools refs` prints only if it prints every call."""
    files(step)["src/other.py"] = OTHER
    line = next(n for n, text in enumerate(OTHER.splitlines(), 1) if "total(" in text)
    named(step)[step.names[0]] = "src/other.py:%d" % line
