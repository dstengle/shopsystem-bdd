"""The carrier of what an asker sends an upstream (capability requests r28, r39 to r44, decision 0071): git, on the upstream's
remote. An asker's repository names that remote and the asker id it is registered under in `.shop/requests.toml`
(`[asker]` `remote`, `id`); it pushes each request, answer or turn it sends to the ref `refs/sent/<asker id>/<n>`, one
JSON object a ref, and reads the requests the upstream publishes as `refs/published/<request>` by fetching them. It holds
no checkout of the upstream. Standard library only."""
import json
import re
import subprocess
import tomllib
from pathlib import Path

import workqueue
from workqueue import Refused

SETTINGS = Path(".shop") / "requests.toml"
SENT, PUBLISHED = "refs/sent/", "refs/published/"
SEEN = "refs/carrier/"      # where a fetch keeps what it read


def settings(root):
    """`.shop/requests.toml` as a dict; empty when the repository has none."""
    path = Path(root) / SETTINGS
    if not path.is_file():
        return {}
    try:
        return tomllib.loads(workqueue.read(path, root))
    except tomllib.TOMLDecodeError as error:
        raise Refused("%s is not TOML: %s" % (SETTINGS, error)) from None


def asker(root):
    """The `[asker]` setting (`remote`, `id`) of an asker's repository, else None."""
    return settings(root).get("asker") or None


def upstream(root):
    """The `[upstream]` setting (`remote`, and `allow`: asker id -> askers) of an upstream's repository, else None."""
    return settings(root).get("upstream") or None


def git(root, *args, data=None):
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, input=data)
    if done.returncode != 0:
        said = (done.stderr.strip() or "exit %d" % done.returncode).splitlines()[0]
        raise Refused("git %s failed: %s" % (args[0], said))
    return done.stdout


def _refs(root, remote, prefix):
    """Fetch every ref of `remote` under `prefix`; return {name below prefix: its content}."""
    git(root, "fetch", "-q", "--prune", remote, "+%s*:%s%s*" % (prefix, SEEN, prefix))
    found = {}
    for line in git(root, "for-each-ref", "--format=%(refname)", SEEN + prefix).splitlines():
        found[line[len(SEEN + prefix):]] = git(root, "cat-file", "blob", line)
    return found


def _push(root, remote, text, ref):
    blob = git(root, "hash-object", "-w", "--stdin", data=text).strip()
    git(root, "push", "-q", "--force", remote, "%s:%s" % (blob, ref))


def published(root, remote):
    """The requests the upstream published, by name, as their file text."""
    return _refs(root, remote, PUBLISHED)


def sent(root, remote):
    """(asker id, number, item) of everything sent and not taken in, each asker id's in the order sent."""
    items = []
    for name, text in _refs(root, remote, SENT).items():
        who, number = name.rsplit("/", 1)
        items.append((who, int(number), json.loads(text)))
    return sorted(items, key=lambda i: (i[0], i[1]))


def send(root, item):
    """Push `item` as the next thing this asker's repository sends."""
    conf = asker(root)
    mine = {int(n.rsplit("/", 1)[1]) for n in _refs(root, conf["remote"], SENT) if n.startswith(conf["id"] + "/")}
    _push(root, conf["remote"], json.dumps(item), "%s%s/%d" % (SENT, conf["id"], max(mine, default=0) + 1))


def next_request(root):
    """The name of the next request: one above every request the remote shows, published or sent."""
    conf = asker(root)
    names = list(published(root, conf["remote"])) + [i["id"] for _, _, i in sent(root, conf["remote"]) if i.get("kind") == "request"]
    return "q%d" % (max([int(n[1:]) for n in names if re.fullmatch(r"q\d+", n)], default=0) + 1)


def drop(root, who, number):
    """Take what was sent as `who`'s number `number` off the remote: it is taken in."""
    git(root, "push", "-q", upstream(root)["remote"], ":%s%s/%d" % (SENT, who, number))


def publish(root, ident, text):
    """Publish request `ident` (its file text) to the upstream's remote, when this repository has one and the request is
    from another asker, so that its asker can read its questions and its turn."""
    conf = upstream(root)
    found = re.search(r"(?m)^asker: *(.*)$", text)
    if conf is not None and found and found.group(1).strip() not in ("internal", workqueue.context_path(root)):
        _push(root, conf["remote"], text, PUBLISHED + ident)
