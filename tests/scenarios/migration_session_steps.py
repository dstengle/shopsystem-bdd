"""migration-tools' steps for what the plugin's hooks give a session about its initiatives (r24, r32-r34): the Givens
commit initiatives and their ledgers; the Whens run the real hook commands of hooks/hooks.json; the Thens read stdout."""
from pytest_bdd import given

from .migration_upgrade_steps import final_layout, plugin_version

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
