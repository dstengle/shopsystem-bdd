"""The grammar tools the suite needs (design §11.3). Every fixture that compiles or parses calls `require()`: a
missing tool fails the test, never skips it, with one message naming `tools install`."""
import importlib.util
import pathlib
import sys

import pytest

SCRIPTS = str(pathlib.Path(__file__).resolve().parent.parent / "scripts")
if SCRIPTS not in sys.path:
    sys.path.append(SCRIPTS)

WHEELS = ("pgf", "clingo")


def missing():
    """The grammar tools that are not there: `gf` and the wheels."""
    import tools_grammar
    out = [] if tools_grammar.gf_binary() else ["gf"]
    return out + [w for w in WHEELS if importlib.util.find_spec(w) is None]


def require():
    gone = missing()
    if gone:
        pytest.fail("the grammar tools %s are missing: run `python3 scripts/tools install`" % ", ".join(gone),
                    pytrace=False)
