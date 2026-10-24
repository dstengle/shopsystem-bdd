"""migration-tools' steps for what the plugin's hooks give a session about its initiatives (r24, r32-r34): the Givens
commit initiatives and their ledgers; the Whens run the real hook commands of hooks/hooks.json; the Thens read stdout."""
import json
import os
import re
import subprocess
import sys

from pytest_bdd import given, then, when

from .migration_old import said
from .migration_upgrade_steps import PLUGIN

ID = "initiative/example.org/acme/shop/%s"


def initiatives(old, **statuses):
    """Commit each initiative at .shop/work/<name>/initiative.md with its status."""
    for name, status in statuses.items():
        old.write(".shop/work/%s/initiative.md" % name,
                  "---\nid: %s\nkind: initiative\nstatus: %s\n---\n\n# %s\n" % (ID % name, status, name))
    old.commit()


@given("its initiatives are i1, which is `done`, and i2, which is `abandoned`")
def _(old):
    initiatives(old, i1="done", i2="abandoned")


@given("its initiatives are i1 and i2, which are neither `done` nor `abandoned`, i3, which is `done`, and i4, which is `abandoned`")
def _(old):
    initiatives(old, i1="started", i2="proposed", i3="done", i4="abandoned")


@given("a repository with .shop/ whose initiatives are i1 and i2, which are neither `done` nor `abandoned`, and i3, which is `done`")
def _(old):
    initiatives(old, i1="started", i2="proposed", i3="done")


@given("each of i1, i2 and i3 has a ledger")
def _(old):
    for name in ("i1", "i2", "i3"):
        old.write(".shop/work/%s/ledger.md" % name, "- 2026-01-02: began\n")
    old.commit()


@given("a repository with .shop/ whose initiative i1 is neither `done` nor `abandoned`")
def _(old):
    initiatives(old, i1="started")


@when("a session in it is about to be compacted")
def _(old, context):
    """Run the PreCompact command of hooks/hooks.json, as the harness does, in the repository."""
    command = json.loads((PLUGIN / "hooks/hooks.json").read_text())["hooks"]["PreCompact"][0]["hooks"][0]["command"]
    who = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(PLUGIN), PYTHON=sys.executable, **who)
    context["done"] = subprocess.run(command, shell=True, cwd=old.root, env=env, capture_output=True, text=True)


@then("the ledger of i1 and the ledger of i2 each end with a line of `compacted` and the time")
def _(old):
    for name in ("i1", "i2"):
        last = old.read(".shop/work/%s/ledger.md" % name).splitlines()[-1]
        assert re.fullmatch(r"- \d{4}-\d{2}-\d{2} \d{2}:\d{2}: compacted", last), last


@then("the ledger of i3 is as it was")
def _(old):
    path = ".shop/work/i3/ledger.md"
    assert old.read(path).encode() == old.before[path]


@then("the plugin's PreCompact hook tells the session to write its hand-off with `work note`")
def _(context):
    assert context["done"].returncode == 0, said(context)
    assert "work note" in context["done"].stdout and "hand-off" in context["done"].stdout, said(context)


@then("it tells the session to end instead of being compacted")
def _(context):
    assert "end this session instead of being compacted" in context["done"].stdout, said(context)


@then("the plugin's SessionStart hook gives the session what `work status` prints for i1 and for i2")
def _(old, context):
    done = context["done"]
    printed = subprocess.run([sys.executable, str(PLUGIN / "scripts/work"), "status"], cwd=old.root,
                             capture_output=True, text=True).stdout
    assert "initiative i1 " in printed and "initiative i2 " in printed, printed
    assert done.returncode == 0, said(context)
    assert printed in done.stdout, said(context)


@then("it gives the session nothing of i3 or i4")
def _(context):
    assert "initiative i3" not in context["done"].stdout and "initiative i4" not in context["done"].stdout, said(context)
