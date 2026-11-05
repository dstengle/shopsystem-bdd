"""What the request tests share (capability requests, r27-r41): a repository on GitHub as `ex/<name>` (its `origin`,
never reached), the stand-in gh in its environment (`hosted` gives the whole environment to run `work` in) (batch_testing.gh_env, its issues in `gh-issues.json` beside its
calls), and the issues and calls read back."""
import json
import os
import subprocess
from pathlib import Path

from batch_testing import gh_env


def hosted(repo, where, name="ctx", monkeypatch=None):
    """`repo`'s origin `https://github.com/ex/<name>.git`; the stand-in gh's environment, set when `monkeypatch`."""
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/ex/%s.git" % name], cwd=repo, check=True,
                   capture_output=True)
    Path(where).mkdir(parents=True, exist_ok=True)
    env = gh_env(where)
    for key, value in env.items():
        if monkeypatch is not None:
            monkeypatch.setenv(key, value)
    return dict(os.environ, **env)


def issues(where):
    path = Path(where) / "gh-issues.json"
    return json.loads(path.read_text()) if path.is_file() else {}


def calls(where, *words):
    path = Path(where) / "gh-calls.jsonl"
    found = [json.loads(line)["argv"] for line in path.read_text().splitlines()] if path.is_file() else []
    return [argv for argv in found if argv[:len(words)] == list(words)]
