"""What the batches' script tests share (plan 4, Task 1): the stand-in gh's environment and its calls, a ready item
written by hand, and a commit made on a branch (the fixture `batch_repo` is in conftest.py)."""
import json
import os
import sys
import tempfile
from pathlib import Path

from backlog_testing import git, write_item

HERE = Path(__file__).resolve().parent
STUB = HERE / "stub_gh.py"


def gh_env(where):
    """The environment of the stand-in gh, its files under `where`: `$SHOPSYSTEM_WORK_GH` a script running
    stub_gh.py with this Python, and no git or gh that asks for a password."""
    where = Path(where)
    script = where / "gh"
    script.write_text('#!/bin/sh\nexec %s %s "$@"\n' % (sys.executable, STUB))
    os.chmod(script, 0o755)
    return {"SHOPSYSTEM_WORK_GH": str(script), "STUB_GH_CALLS": str(where / "gh-calls.jsonl"),
            "STUB_GH_STATE": str(where / "gh-state.json"), "GH_TOKEN": "", "GIT_TERMINAL_PROMPT": "0"}


def gh_calls(where):
    path = Path(where) / "gh-calls.jsonl"
    return [json.loads(line)["argv"] for line in path.read_text().splitlines()] if path.is_file() else []


def block(title, text, group="g4", req="r5"):
    return "### work-queue\n\n#### [%s] %s\n- [%s] %s" % (group, title, req, text)


def ready_item(repo, name, title, text, **fields):
    """A `ready` item `name` with the one line `text` as work-queue g4/r5, committed."""
    body = "\n## Requirements\n\n%s\n" % block(title, text)
    return write_item(repo, name, title=title, status="ready", body=body, **fields)


def tree_of(repo, branch):
    """The worktree `branch` is checked out in, or None."""
    path = None
    for line in git(repo, "worktree", "list", "--porcelain").splitlines():
        if line.startswith("worktree "):
            path = line.split(" ", 1)[1]
        elif line == "branch refs/heads/%s" % branch:
            return Path(path)
    return None


def commit_on(repo, branch, path, text, message):
    """Write `text` to `path` (relative) on `branch` and commit it there, in the worktree it is checked out in, else in
    a throwaway one; the commit's sha."""
    tree = tree_of(repo, branch)
    throwaway = tree is None
    if throwaway:
        tree = Path(tempfile.mkdtemp(prefix="commit-on-")) / "tree"
        git(repo, "worktree", "add", "-q", str(tree), branch)
    try:
        (tree / path).parent.mkdir(parents=True, exist_ok=True)
        (tree / path).write_text(text)
        git(tree, "add", "-A", "--", path)
        git(tree, "commit", "-q", "-m", message)
        return git(tree, "rev-parse", "HEAD").strip()
    finally:
        if throwaway:
            git(repo, "worktree", "remove", "--force", str(tree))
