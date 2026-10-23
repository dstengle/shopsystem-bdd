"""migration-tools' steps for a .shop/plugin-version that holds no version (r30, r31): the Given commits a repository whose
version file holds the quoted text; the Whens run `migrate` or the SessionStart hook; the Thens read what they left."""
import json
import os
import subprocess
import sys

from pytest_bdd import given, parsers, then, when

from .migration_old import said
from .migration_upgrade_steps import PLUGIN, final_layout


@given(parsers.parse('a repository on the final layout whose .shop/plugin-version holds "{held}"'))
def _(old, context, held):
    final_layout(old, held)
    old.commit()
    context["held"] = held


@when("a session starts in the repository")
def _(old, context):
    """Run the SessionStart command of hooks/hooks.json, as the harness does, in the repository."""
    hooks = json.loads((PLUGIN / "hooks/hooks.json").read_text())["hooks"]["SessionStart"]
    command = hooks[0]["hooks"][0]["command"]
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(PLUGIN), PYTHON=sys.executable)
    context["done"] = subprocess.run(command, shell=True, cwd=old.root, env=env, capture_output=True, text=True)


@then("migrate exits with an error")
def _(context):
    assert context["done"].returncode != 0, said(context)


@then(parsers.parse('it says that .shop/plugin-version holds "{held}", which is no version'))
def _(context, held):
    sentence = '.shop/plugin-version holds "%s", which is no version' % held
    assert sentence in said(context), said(context)


@then("no file of the repository has changed")
def _(old, context):
    assert old.git("status", "--porcelain").stdout == ""
    assert len(old.git("log", "--oneline").stdout.splitlines()) == context["before_log"]
    assert (old.root / ".shop/plugin-version").read_text().strip() == context["held"]


@then(parsers.parse('the session is told to tell the person that .shop/plugin-version holds "{held}", which is no version'))
def _(context, held):
    done = context["done"]
    assert done.returncode == 0, said(context)
    sentence = '.shop/plugin-version holds "%s", which is no version: tell the person.' % held
    assert sentence in done.stdout, said(context)
