"""A request's issue on GitHub (capability requests, r27-r41): where it lives, and the `gh` calls that open it, comment
on it, read it and close it, through `$SHOPSYSTEM_WORK_GH` as batch_gh.py calls gh.

An upstream's GitHub repository is the `github: <owner>/<name>` its bullet under `## Upstreams` in spec/index.md names
(r28: an upstream with none is unhosted); this context's own is read off its git remote `origin`. Standard library
only."""
import json
import re
from pathlib import Path

import batch_gh
import shop_files
from shop_files import Refused

REPO = r"[\w.-]+/[\w.-]+"


def bullets(root):
    """{bounded-context id: its bullet's text} of spec/index.md's `## Upstreams`."""
    index = Path(root) / "spec" / "index.md"
    section = re.search(r"(?ms)^## Upstreams\s*$(.*?)(?=^## |\Z)", index.read_text() if index.is_file() else "")
    found = [re.match(r"^- (bounded-context/[^\s:]+):(.*)$", line) for line in (section.group(1) if section else
                                                                                 "").splitlines()]
    return {m.group(1): m.group(2) for m in found if m}


def own_repo(root, command):
    """`<owner>/<name>` of this repository's git remote `origin` on GitHub; refused, naming the context, without one."""
    try:
        url = shop_files.git(root, "remote", "get-url", "origin").strip()
    except Refused:
        url = ""
    found = re.search(r"github\.com[:/]([\w.-]+/[\w.-]+?)(?:\.git)?/?$", url)
    if not found:
        raise Refused("%s: bounded-context/%s has no GitHub repository: its git remote origin (%s) is not on GitHub"
                      % (command, shop_files.context_path(root), url or "none"))
    return found.group(1)


def repo_of(root, context, command):
    """The GitHub repository of the context `context` (a bounded-context id): its upstream bullet's `github:`, or this
    context's own remote; an upstream with none (unhosted, r28) is refused, naming it."""
    if context == "bounded-context/" + shop_files.context_path(root):
        return own_repo(root, command)
    bullet = bullets(root).get(context)
    found = re.search(r"\bgithub: *(%s)" % REPO, bullet or "")
    if not found:
        raise Refused("%s: the upstream %s names no GitHub repository under ## Upstreams in spec/index.md: add "
                      "`github: <owner>/<name>` to its bullet" % (command, context))
    return found.group(1).rstrip(".")


def last_line(out, command, what):
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    if not lines:
        raise Refused("%s: gh %s printed no URL" % (command, what))
    return lines[-1]


def open_issue(root, repo, title, body, command):
    """The URL of a new issue on `repo`."""
    out = batch_gh.gh(root, "issue", "create", "--repo", repo, "--title", title, "--body", body, command=command)
    return last_line(out, command, "issue create")


def comment(root, url, body, command):
    """The URL of a new comment on the issue `url`."""
    return last_line(batch_gh.gh(root, "issue", "comment", url, "--body", body, command=command), command,
                     "issue comment")


def close(root, url, command):
    batch_gh.gh(root, "issue", "close", url, command=command)


def _json(out, command, what):
    try:
        return json.loads(out)
    except ValueError:
        raise Refused("%s: gh %s printed no JSON" % (command, what)) from None


def view(root, url, command):
    """(body, [(comment URL, body)], state) of the issue `url`."""
    data = _json(batch_gh.gh(root, "issue", "view", url, "--json", "body,comments,state", command=command), command,
                 "issue view")
    comments = [(c.get("url"), c.get("body") or "") for c in data.get("comments") or [] if c.get("url")]
    return data.get("body") or "", comments, data.get("state")


def listed(root, repo, command):
    """[(URL, title, body)] of the open issues of `repo`."""
    data = _json(batch_gh.gh(root, "issue", "list", "--repo", repo, "--state", "open", "--limit", "200", "--json",
                             "url,title,body", command=command), command, "issue list")
    return [(i.get("url"), i.get("title") or "", i.get("body") or "") for i in data if i.get("url")]
