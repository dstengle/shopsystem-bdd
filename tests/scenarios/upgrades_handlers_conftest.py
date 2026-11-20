"""upgrades' scenario conftest (b423, r36, r37), each handler a `local` of work_queue_world's table taken before
migration-tools' own: "the scenario conftest s1 conforms to the old scenario conftest form" writes the text
`migrate init` wrote before 0.41.0 into the given block, one that conforms to neither form a hand-edited text; the
Thens read the conftest `migrate upgrade` left, rewritten to the text `migrate init` writes now and kept in the
upgrade's one commit, or left byte for byte and named in what it printed."""
import re

from scenarios import migration_tools_handlers as M

local = M.local
CONFTEST = "tests/scenarios/conftest.py"
OLD = '''"""The generated features' scenarios: one `test_<capability>.py` a capability binds its feature's steps."""
'''
EDITED = '''"""This context's own scenarios' conftest, edited by hand."""
import pytest
'''
FORM = re.compile(r"the scenario conftest \w+ (conforms|does not conform) to the (old )?scenario conftest form$")


def mine(step):
    return M.migration(step) and any(re.sub(r"^(the|a|an|this) ", "", np).startswith("scenario conftest ")
                                     for np in step.nps)


def current():
    """The text `migrate init` writes now (the scenario conftest form), of the plugin `migrate` runs from."""
    import migrate_init
    return migrate_init.CONFTEST_TEXT


@local("GivenDoes")
@local("GivenDoesNot")
def conforms(step):
    found = FORM.match(step.text) if M.migration(step) else None
    if found is None:
        return False
    tracked = M.held(step)
    if found.group(1) == "conforms":
        tracked[CONFTEST] = OLD if found.group(2) else current()
    else:
        tracked.setdefault(CONFTEST, EDITED)
    return None


def committed(step):
    """The conftest in the one commit `migrate upgrade` made, nothing left uncommitted."""
    old = step.context["old"]
    assert len(old.git("log", "--oneline").stdout.splitlines()) == step.context["commits"] + 1
    files = old.git("show", "--name-only", "--format=", "HEAD").stdout.split()
    assert CONFTEST in files, files
    assert old.git("status", "--porcelain").stdout == "", old.git("status", "--porcelain").stdout


@local("ThenDoes")
def changed(step):
    if not mine(step):
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert M.read(step, CONFTEST) == current() != M.held(step)[CONFTEST], M.read(step, CONFTEST)
    if step.term in ("keep", "commit", "write"):     # "keeps", which the CLI's spelling says "writes"
        committed(step)
    return None


@local("ThenDoesNot")
def unchanged(step):
    if not mine(step):
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert M.read(step, CONFTEST) == M.held(step)[CONFTEST]
    files = step.context["old"].git("show", "--name-only", "--format=", "HEAD").stdout.split()
    assert CONFTEST not in files, files
    return None


@local("ThenPrints")
def named(step):
    if not mine(step):
        return False
    assert step.context["done"].returncode == 0, M.said(step)
    assert CONFTEST in M.said(step), M.said(step)
    return None
