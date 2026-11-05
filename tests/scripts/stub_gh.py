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
body, comments and state, and `issue list --repo <r>` its open issues. When `$STUB_GH_FAIL` equals the call's first two words (`pr
create`), the call exits 1 with `stand-in gh: refused` on stderr (and is recorded with `"failed": true`)."""
import json
import os
import sys
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


def main(argv):
    failed = os.environ.get("STUB_GH_FAIL") == " ".join(argv[:2])
    late = os.environ.get("STUB_GH_LATE") == " ".join(argv[:2])
    creates = len(made())
    with open(os.environ["STUB_GH_CALLS"], "a") as out:
        out.write(json.dumps(dict({"argv": argv}, **({"failed": True} if failed else {}))) + "\n")
    if failed:
        print("stand-in gh: refused", file=sys.stderr)
        return 1
    if argv[:1] == ["issue"]:
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
