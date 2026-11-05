#!/usr/bin/env python3
"""A stand-in for GitHub's `gh` (workflow simplification plan 4, D20), which `work batch` runs as `$SHOPSYSTEM_WORK_GH`
in the suite, so no test reaches a network.

Each call appends `{"argv": [...]}` to the file `$STUB_GH_CALLS`. `pr create` prints
`https://github.com/ex/ctx/pull/<k>`, k counting the creates that did not fail. `pr view <url> --json
state,mergeCommit` prints the entry for `<url>` of the JSON file `$STUB_GH_STATE`, else `{"state": "OPEN",
"mergeCommit": null}`. `pr close` prints nothing. When `$STUB_GH_FAIL` equals the call's first two words (`pr
create`), the call exits 1 with `stand-in gh: refused` on stderr (and is recorded with `"failed": true`)."""
import json
import os
import sys
from pathlib import Path


def calls():
    path = Path(os.environ["STUB_GH_CALLS"])
    return [json.loads(line) for line in path.read_text().splitlines()] if path.is_file() else []


def main(argv):
    failed = os.environ.get("STUB_GH_FAIL") == " ".join(argv[:2])
    creates = sum(1 for c in calls() if c["argv"][:2] == ["pr", "create"] and not c.get("failed"))
    with open(os.environ["STUB_GH_CALLS"], "a") as out:
        out.write(json.dumps(dict({"argv": argv}, **({"failed": True} if failed else {}))) + "\n")
    if failed:
        print("stand-in gh: refused", file=sys.stderr)
        return 1
    if argv[:2] == ["pr", "create"]:
        print("https://github.com/ex/ctx/pull/%d" % (creates + 1))
    elif argv[:2] == ["pr", "view"]:
        path = Path(os.environ.get("STUB_GH_STATE", ""))
        states = json.loads(path.read_text()) if path.is_file() else {}
        print(json.dumps(states.get(argv[2], {"state": "OPEN", "mergeCommit": None})))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
