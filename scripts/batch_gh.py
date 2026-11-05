"""The `gh` calls of a batch (capability batches; workflow simplification plan 4, D11, D13, D14): a draft pull
request created, its state and merge commit read, and it closed. gh is `$SHOPSYSTEM_WORK_GH`, else `gh` on the PATH;
a gh that fails is refused naming its subcommand and the first line of its complaint. Standard library only."""
import json
import os
import shlex
import subprocess

from workqueue import Refused

GH = "SHOPSYSTEM_WORK_GH"


def gh(root, *args, command="work batch"):
    """gh's output; a gh that fails is refused under `command`, naming its subcommand."""
    argv = shlex.split(os.environ.get(GH) or "gh")
    try:
        done = subprocess.run([*argv, *args], cwd=root, capture_output=True, text=True)
    except OSError as err:
        raise Refused("%s: gh %s failed: %s" % (command, " ".join(args[:2]), err)) from None
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise Refused("%s: gh %s failed: %s" % (command, " ".join(args[:2]), said))
    return done.stdout


def create(root, base, head, title, body, command="work batch"):
    """A draft pull request of `head` into `base`; its URL, the last line gh prints. When gh fails, the open pull
    request of `head` it may have created anyway is looked for, and its URL given (plan 4 review, M5)."""
    try:
        out = gh(root, "pr", "create", "--draft", "--base", base, "--head", head, "--title", title, "--body", body,
                 command=command)
    except Refused:
        found = existing(root, head)
        if found:
            return found
        raise
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if not lines:
        raise Refused("%s: gh pr create failed: it printed no URL" % command)
    return lines[-1]


def existing(root, head):
    """The URL of the open pull request whose head is `head`, or None (a gh that fails, or prints no list, is None)."""
    try:
        found = json.loads(gh(root, "pr", "list", "--head", head, "--json", "url"))
    except (Refused, ValueError):
        return None
    urls = [p.get("url") for p in found if isinstance(p, dict) and p.get("url")] if isinstance(found, list) else []
    return urls[0] if urls else None


def state(root, url, command="work batch"):
    """(state, the merge commit's oid or None) of the pull request `url`."""
    out = gh(root, "pr", "view", url, "--json", "state,mergeCommit", command=command)
    try:
        data = json.loads(out)
    except ValueError:
        raise Refused("%s: gh pr view failed: it printed no JSON object" % command) from None
    merge = data.get("mergeCommit") or {}
    return data.get("state"), merge.get("oid")


def close(root, url, command="work batch"):
    gh(root, "pr", "close", url, command=command)
