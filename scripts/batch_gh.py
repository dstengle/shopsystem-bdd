"""The `gh` calls of a batch (capability batches; workflow simplification plan 4, D11, D13, D14): a draft pull
request created, its state and merge commit read, and it closed. gh is `$SHOPSYSTEM_WORK_GH`, else `gh` on the PATH;
a gh that fails is refused naming its subcommand and the first line of its complaint. Standard library only."""
import json
import os
import shlex
import subprocess

from workqueue import Refused

GH = "SHOPSYSTEM_WORK_GH"


def gh(root, *args):
    command = shlex.split(os.environ.get(GH) or "gh")
    try:
        done = subprocess.run([*command, *args], cwd=root, capture_output=True, text=True)
    except OSError as err:
        raise Refused("work batch: gh %s failed: %s" % (" ".join(args[:2]), err)) from None
    if done.returncode != 0:
        said = (done.stderr.strip() or done.stdout.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise Refused("work batch: gh %s failed: %s" % (" ".join(args[:2]), said))
    return done.stdout


def create(root, base, head, title, body):
    """A draft pull request of `head` into `base`; its URL, the last line gh prints."""
    out = gh(root, "pr", "create", "--draft", "--base", base, "--head", head, "--title", title, "--body", body)
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if not lines:
        raise Refused("work batch: gh pr create failed: it printed no URL")
    return lines[-1]


def state(root, url):
    """(state, the merge commit's oid or None) of the pull request `url`."""
    out = gh(root, "pr", "view", url, "--json", "state,mergeCommit")
    try:
        data = json.loads(out)
    except ValueError:
        raise Refused("work batch: gh pr view failed: it printed no JSON object") from None
    merge = data.get("mergeCommit") or {}
    return data.get("state"), merge.get("oid")


def close(root, url):
    gh(root, "pr", "close", url)
