#!/usr/bin/env python3
"""A stand-in for GitHub's `gh` (workflow simplification plan 4, D20), which `work batch` runs as `$SHOPSYSTEM_WORK_GH`
in the suite, so no test reaches a network.

Each call appends `{"argv": [...]}` to the file `$STUB_GH_CALLS`. `pr create` prints
`https://github.com/ex/ctx/pull/<k>`, k counting the creates that did not fail. `pr view <url> --json
state,mergeCommit` prints the entry for `<url>` of the JSON file `$STUB_GH_STATE`, else `{"state": "OPEN",
"mergeCommit": null}`. `pr close`, `pr comment` and `pr ready` (the pull request review's, plan 5)
print nothing.

The issues of a request (capability requests) are kept in the JSON file `$STUB_GH_ISSUES` (else `gh-issues.json`
beside `$STUB_GH_CALLS`), `{url: {"title", "body", "state", "comments": [{"url", "body"}]}}`, which a test may write
first: `issue create --repo <r>` adds `https://github.com/<r>/issues/<k>` and prints it, `issue comment <url>` adds
`<url>#issuecomment-<k>` and prints it, `issue close <url>` sets its state `CLOSED`, `issue view <url>` prints its
body, comments and state, and `issue list --repo <r>` its open issues.

GitHub's events (`work watch --forward`, requests r57, r58): `repo view <r> --json viewerPermission` prints `ADMIN`,
else `WRITE` for a repository `$STUB_GH_NOT_ADMIN` names (comma-separated); `extension list` names cli/gh-webhook
unless `$STUB_GH_NO_WEBHOOK` is set, and `extension install` prints nothing. What a test keeps pending in the file
`gh-pending.json` beside the calls (the issues file's form: issues, and comments on issues) is brought back into the
issues by `webhook forward --repo <r> --url <u>`, for `<r>`'s issues once a later call has listed issues (the end of the
check at the watch's start), and posted to `<u>` as an `issues` event; the forward then stays, as gh's does, until it
is killed (at most 60 s). `api --include ... notifications` with no If-Modified-Since prints a 200 with no
notifications; with one, a 200 bringing all that is pending back, one notification a repository, else a 304 (exit
1, as gh exits on a status over 299), each with `X-Poll-Interval: 0`. When `$STUB_GH_FAIL` equals the call's first two words (`pr
create`), the call exits 1 with `stand-in gh: refused` on stderr (and is recorded with `"failed": true`)."""
import json
import os
import sys
import time
import urllib.request
from pathlib import Path


def calls():
    path = Path(os.environ["STUB_GH_CALLS"])
    return [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []


def made():
    """The URLs of the creates before this call that did not fail, each with its head."""
    found = [c["argv"] for c in calls() if c["argv"][:2] == ["pr", "create"] and not c.get("failed")]
    return [(a[a.index("--head") + 1] if "--head" in a else None, "https://github.com/ex/ctx/pull/%d" % k)
            for k, a in enumerate(found, 1)]


def issues_path():
    return Path(os.environ.get("STUB_GH_ISSUES") or Path(os.environ["STUB_GH_CALLS"]).with_name("gh-issues.json"))


def opt(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def issue(argv):
    """`gh issue ...` on the issues file; what it prints."""
    path = issues_path()
    issues = json.loads(path.read_text()) if path.is_file() else {}
    if argv[1] == "create":
        repo = opt(argv, "--repo")
        url = "https://github.com/%s/issues/%d" % (repo, 1 + sum(u.startswith("https://github.com/%s/" % repo)
                                                                 for u in issues))
        issues[url] = {"title": opt(argv, "--title"), "body": opt(argv, "--body"), "state": "OPEN", "comments": []}
        out = url
    elif argv[1] == "comment":
        url = "%s#issuecomment-%d" % (argv[2], 1 + sum(len(i["comments"]) for i in issues.values()))
        issues[argv[2]]["comments"].append({"url": url, "body": opt(argv, "--body")})
        out = url
    elif argv[1] == "close":
        issues[argv[2]]["state"] = "CLOSED"
        out = None
    elif argv[1] == "view":
        out = json.dumps(issues[argv[2]])
    else:      # list
        prefix = "https://github.com/%s/issues/" % opt(argv, "--repo")
        out = json.dumps([dict(i, url=u) for u, i in issues.items() if u.startswith(prefix) and i["state"] == "OPEN"])
    path.write_text(json.dumps(issues))
    return out


def pending_path():
    return Path(os.environ["STUB_GH_CALLS"]).with_name("gh-pending.json")


def bring_back(repo=None):
    """The pending issues and comments (of `repo`'s issues, else all) put back into the issues; the repositories."""
    path, back = pending_path(), set()
    pending = json.loads(path.read_text()) if path.is_file() else {}
    issues = json.loads(issues_path().read_text()) if issues_path().is_file() else {}
    for url in [u for u in pending if repo is None or u.startswith("https://github.com/%s/" % repo)]:
        given = pending.pop(url)
        issues.setdefault(url, dict(given, comments=[]))["comments"].extend(given["comments"])
        back.add(url.split("/")[3] + "/" + url.split("/")[4])
    issues_path().write_text(json.dumps(issues))
    path.write_text(json.dumps(pending))
    return back


def forward(argv):
    """Once a later call lists the repository's issues, the pending ones back and an event posted; then stay."""
    repo, url, start = opt(argv, "--repo"), opt(argv, "--url"), len(calls())
    end = time.time() + 60
    while time.time() < end and not any(c["argv"][:2] == ["issue", "list"] for c in calls()[start:]):
        time.sleep(0.05)
    bring_back(repo)
    event = urllib.request.Request(url, data=json.dumps({"repository": {"full_name": repo}}).encode(),
                                   headers={"X-GitHub-Event": "issues", "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(event, timeout=10).read()
    except OSError:     # the watch has ended
        return
    time.sleep(max(0, end - time.time()))


def notifications(argv):
    """A 200 (the baseline, or all that is pending brought back) or a 304; gh's exit code."""
    since = any(a.lower().startswith("if-modified-since:") for a in argv)
    back = bring_back() if since else set()
    if since and not back:
        print("HTTP/2.0 304 Not Modified\nX-Poll-Interval: 0\n")
        return 1
    print("HTTP/2.0 200 OK\nLast-Modified: Fri, 06 Nov 2026 10:00:00 GMT\nX-Poll-Interval: 0\n")
    print(json.dumps([{"repository": {"full_name": r}, "subject": {"type": "Issue"}} for r in sorted(back)]))
    return 0


def main(argv):
    failed = os.environ.get("STUB_GH_FAIL") == " ".join(argv[:2])
    late = os.environ.get("STUB_GH_LATE") == " ".join(argv[:2])
    creates = len(made())
    with open(os.environ["STUB_GH_CALLS"], "a") as out:
        out.write(json.dumps(dict({"argv": argv}, **({"failed": True} if failed else {}))) + "\n")
    if failed:
        print("stand-in gh: refused", file=sys.stderr)
        return 1
    if argv[:2] == ["webhook", "forward"]:
        forward(argv)
    elif argv[:1] == ["api"] and "notifications" in argv:
        return notifications(argv)
    elif argv[:2] == ["repo", "view"]:
        admin = argv[2] not in os.environ.get("STUB_GH_NOT_ADMIN", "").split(",")
        print(json.dumps({"viewerPermission": "ADMIN" if admin else "WRITE"}))
    elif argv[:2] == ["extension", "list"]:
        print("" if os.environ.get("STUB_GH_NO_WEBHOOK") else "gh webhook\tcli/gh-webhook\tv0.1.0")
    elif argv[:1] == ["issue"]:
        out = issue(argv)
        if out is not None:
            print(out)
    elif argv[:2] == ["pr", "create"]:
        print("https://github.com/ex/ctx/pull/%d" % (creates + 1))
    elif argv[:2] == ["pr", "view"]:
        path = Path(os.environ.get("STUB_GH_STATE", ""))
        states = json.loads(path.read_text()) if path.is_file() else {}
        print(json.dumps(states.get(argv[2], {"state": "OPEN", "mergeCommit": None})))
    elif argv[:2] == ["pr", "list"]:
        head = argv[argv.index("--head") + 1] if "--head" in argv else None
        closed = {c["argv"][2] for c in calls() if c["argv"][:2] == ["pr", "close"] and not c.get("failed")}
        print(json.dumps([{"url": url} for h, url in made() if h == head and url not in closed]))
    if late:
        print("stand-in gh: timed out", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
