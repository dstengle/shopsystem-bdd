"""features/requests.feature's steps for a session the person gives a delegation (requests r72).

The When runs the UserPromptSubmit command of hooks/hooks.json in the repository, as the harness does. A session double
then acts only on what the hook gave it: where the hook's text tells it to write a delegation in the same reply with
`work delegate`, as `The person, <date>: "<words>"`, it runs that command; otherwise it runs nothing.
"""
import json
import os
import subprocess
import sys

from pytest_bdd import parsers, then, when

from .migration_upgrade_steps import PLUGIN
from .requests_write_steps import ident_delegation_is


@when(parsers.parse('the person tells a session, on {date}, that for {ident} it may "{words}"'))
def person_tells_a_session(repo, run, context, date, ident, words):
    command = json.loads((PLUGIN / "hooks/hooks.json").read_text())["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(PLUGIN), PYTHON=sys.executable)
    prompt = json.dumps({"prompt": 'On %s: for %s you may "%s"' % (date, ident, words)})
    hook = subprocess.run(command, shell=True, cwd=repo, env=env, input=prompt, capture_output=True, text=True)
    told = hook.stdout
    context["ran"] = None
    if hook.returncode == 0 and "work delegate" in told and "same reply" in told and 'The person, <date>: "<the person' in told:
        context["ran"] = ["delegate", ident, 'The person, %s: "%s"' % (date, words)]
        context["done"] = run("work", *context["ran"])


@then(parsers.parse("in its reply to that message the session runs `work delegate`, giving {ident} and the delegation '{text}'"))
def session_ran_delegate(context, ident, text):
    assert context["ran"] == ["delegate", ident, text], context["ran"]


@then(parsers.parse("when that reply ends, {ident}'s delegation is '{text}'"))
def delegation_when_reply_ends(repo, ident, text):
    ident_delegation_is(repo, ident, None, text)
