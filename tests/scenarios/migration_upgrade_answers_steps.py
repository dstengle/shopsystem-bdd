"""The steps of migration-tools r29: the upgrade step of the plugin version after 0.24.0. The Given builds the repository at
0.24.0 and a copy of the plugin whose version is 0.25.0; the shared When runs `migrate` from that copy."""
import json
import re
import shutil

from pytest_bdd import given, parsers, then

from .migration_old import CONTEXT, said
from .migration_upgrade_steps import PLUGIN, final_layout

WORK = ".shop/work/"


def work_item(old, rel, status, heading):
    name = rel.rsplit("/", 1)[1][:-3]
    old.write(rel, "---\nid: work-item/%s/%s\nkind: work-item\nstatus: %s\n---\n\n# %s\n\n%s\n\nA ruling.\n"
              % (CONTEXT, name, status, name, heading))
    old.commit()


@given("a repository on the final layout whose .shop/plugin-version is 0.24.0")
def _(old, context, tmp_path_factory):
    final_layout(old, "0.24.0")
    old.commit()
    copy = tmp_path_factory.mktemp("plugin") / "plugin-0.25.0"
    shutil.copytree(PLUGIN / "scripts", copy / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
    (copy / ".claude-plugin").mkdir()
    (copy / ".claude-plugin/plugin.json").write_text(json.dumps({"name": "shopsystem-bdd", "version": "0.25.0"}))
    context["plugin_scripts"] = copy / "scripts"


@given(parsers.re(r'(?P<rel>\.shop/work/\S+\.md), a work-item with the status (?P<status>\S+) and a heading "(?P<heading>[^"]+)"$'))
def _(old, rel, status, heading):
    work_item(old, rel, status, heading)


@given(parsers.parse("{rel}, with a line for w1 naming the status awaiting-ruling"))
def _(old, rel):
    old.write(rel, json.dumps({"time": "t", "work-item": "w1", "before": "ready", "after": "awaiting-ruling"}) + "\n")
    old.commit()


@then(parsers.parse('{rel} now has the status {status} and the heading "{heading}"'))
def _(old, context, rel, status, heading):
    text = old.read(rel)
    assert re.search(r"^status: %s$" % re.escape(status), text, re.M) and "\n%s\n" % heading in text, said(context)


@then(parsers.parse('{rel} still has the status {status} and now has the heading "{heading}"'))
def _(old, rel, status, heading):
    text = old.read(rel)
    assert re.search(r"^status: %s$" % re.escape(status), text, re.M) and "\n%s\n" % heading in text, text
    assert "## Rulings" not in text


@then(parsers.parse("the line of {rel} for w1 now names the status {status}"))
def _(old, rel, status):
    lines = [json.loads(l) for l in old.read(rel).splitlines()]
    assert [l["after"] for l in lines if l["work-item"] == "w1"] == [status], lines
