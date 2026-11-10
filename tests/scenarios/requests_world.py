"""The scenario repository of features/requests.feature and features/intake.feature's issues (not a handler module, so
the glob does not load it): the stand-in gh (tests/scripts/stub_gh.py) with its files beside the repository, the
repository's `origin` on GitHub (`ex/ctx`, never reached), a request given the issue its conversation is on, and the
comments the Givens of a codified-2 scenario describe, put on their requests' issues before the run (`put_comments`).
requests_handlers*.py and intake_handlers.py load it by path as `shop_requests_world`."""
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

STUB = Path(__file__).resolve().parents[1] / "scripts" / "stub_gh.py"
OWN_REPO = "ex/ctx"
ISSUE = "https://github.com/%s/issues/1" % OWN_REPO
READABLE = "~~~shop-request\nstep: turn\nstatus: awaiting-upstream\nturn: upstream\nanswer 1: The work queue\n~~~\n"
UNREADABLE = "~~~shop-request\nstep: turn\nthis is no field\n~~~\n"
OFFER = "~~~shop-request\nstep: offer\nstatus: awaiting-asker\nturn: asker\noffer: This may serve.\nanswer 1: %s\n~~~\n"


def outside(step):
    """A directory beside the repository: the stand-in gh's files."""
    if "outside" not in step.context:
        step.context["outside"] = step.request.getfixturevalue("tmp_path_factory").mktemp("outside")
    return step.context["outside"]


def env(step):
    where = outside(step)
    return dict(os.environ, SHOPSYSTEM_WORK_GH="%s %s" % (shlex.quote(sys.executable), shlex.quote(str(STUB))),
                STUB_GH_CALLS=str(where / "gh-calls.jsonl"), STUB_GH_ISSUES=str(where / "gh-issues.json"),
                GH_TOKEN="", GIT_TERMINAL_PROMPT="0")


def gh_calls(step):
    path = outside(step) / "gh-calls.jsonl"
    return [json.loads(line)["argv"] for line in path.read_text().splitlines()] if path.is_file() else []


def issues(step):
    path = outside(step) / "gh-issues.json"
    return json.loads(path.read_text()) if path.is_file() else {}


def write_issues(step, found):
    (outside(step) / "gh-issues.json").write_text(json.dumps(found))


def hosted(repo):
    """The repository's `origin` on GitHub, once it is a git repository; it pushes to a bare repository beside it, so
    the commits `work` pushes (U4) never reach GitHub."""
    have = subprocess.run(["git", "remote"], cwd=repo, capture_output=True, text=True).stdout.split()
    if "origin" not in have:
        subprocess.run(["git", "remote", "add", "origin", "https://github.com/%s.git" % OWN_REPO], cwd=repo, check=True)
        pushes = Path(repo).parent / ("%s-origin.git" % Path(repo).name)
        subprocess.run(["git", "init", "-q", "--bare", str(pushes)], check=True)
        subprocess.run(["git", "remote", "set-url", "--push", "origin", str(pushes)], cwd=repo, check=True)


def with_issue(step, path, url=ISSUE):
    """The request at `path` on the issue `url`, which the stand-in gh holds."""
    text = path.read_text()
    if "\nissue: " not in text:
        path.write_text(text.replace("\nkind: request\n", "\nkind: request\nissue: %s\n" % url, 1))
    found = issues(step)
    found.setdefault(url, {"title": "a request", "body": "", "state": "OPEN", "comments": []})
    write_issues(step, found)


def pend(step):
    """What the Givens wrote on the stand-in's issues, its new issues and its comments, moved to `gh-pending.json`
    (the issues file's form), for the stand-in's `webhook forward` or `api notifications` to bring back."""
    found, pending = issues(step), {}
    for url in step.context.get("issues", {}).values():
        pending[url] = found.pop(url)
    for url in step.context.get("comments", {}).values():
        issue = found[url.split("#", 1)[0]]
        comment = next(c for c in issue["comments"] if c["url"] == url)
        issue["comments"].remove(comment)
        pending.setdefault(url.split("#", 1)[0], dict(issue, comments=[]))["comments"].append(comment)
    write_issues(step, found)
    (outside(step) / "gh-pending.json").write_text(json.dumps(pending))


OWN = "bounded-context/ex.com/prod/ctx"
UP = "bounded-context/ex.com/prod/up"


def sided(path, word):
    """The request at `path` received (kept in its upstream's repository, this one, asked by another context) or sent
    (kept in its asker's, this one, to another upstream). A received request with no status Given is `awaiting-asker`,
    so that its turn alone would let the asker's command run."""
    text = path.read_text().replace("\nkind: request\n", "\nkind: request\nupstream: %s\n" % (OWN if word == "received" else UP), 1)
    if word == "sent":
        text = text.replace("\nasker: other\n", "\nasker: %s\n" % OWN, 1)
    else:
        text = text.replace("\nasker: other\n", "\nasker: bounded-context/ex.com/prod/other\n", 1)
        text = text.replace("\nstatus: open\n", "\nstatus: awaiting-asker\n", 1)
    path.write_text(text)


def feature(step):
    """The stem of the running scenario's feature file (`requests`)."""
    found = getattr(getattr(step.request.node, "function", None), "__scenario__", None)
    return Path(found.feature.filename).stem if found is not None else None


def comment(step, name):
    """What the Givens said of the comment `name`: its request and its body (`readable`, `unreadable`, or the name of
    the foreign entry its field block holds). No request holds it: requests' Givens say only that one does not."""
    return step.context.setdefault("comment", {}).setdefault(name, {"request": None, "body": "readable"})


def put_comments(step, path_of):
    """Each comment a Given put on a request posted on that request's issue (`<issue>#issuecomment-<k>`); its URL is
    what names it."""
    found = issues(step)
    for name, said in step.context.get("comment", {}).items():
        if said["request"] is None or name in step.context.get("comments", {}):
            continue
        path = path_of(step, said["request"])
        url = re.search(r"^issue: (.*)$", path.read_text(), re.MULTILINE).group(1).strip()
        comments = found[url]["comments"]
        link = "%s#issuecomment-%d" % (url, 100 + len(comments))
        body = {"readable": READABLE, "unreadable": UNREADABLE}.get(said["body"])
        comments.append({"url": link, "body": body or OFFER % step.context["foreign"][said["body"]]})
        step.context.setdefault("comments", {})[name] = link
        step.context.setdefault("says", {})[name] = link
    write_issues(step, found)
