"""migration-tools' steps for what the plugin's hooks give a session about its initiatives (r24, r32-r34): the Givens
commit initiatives and their ledgers; the Whens run the real hook commands of hooks/hooks.json; the Thens read stdout."""
import subprocess
import sys

from pytest_bdd import given, then

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
