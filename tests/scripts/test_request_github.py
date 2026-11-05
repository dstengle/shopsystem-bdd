"""A request through a real GitHub issue, on demand (requests r27-r41): run only when `$SHOPSYSTEM_TEST_GITHUB_REPO`
names a GitHub repository (`owner/name`) the logged-in gh may open and close issues on, and not collected otherwise
(conftest.py). The upstream's repository is that one (its `origin`, never pushed to); the downstream names it under
`## Upstreams`. The test closes every issue it opens, whatever happens. gh's own login is used; `GH_TOKEN` is unset.

    SHOPSYSTEM_TEST_GITHUB_REPO=owner/name python3 -m pytest -q -n0 tests/scripts/test_request_github.py
"""
import os
import subprocess

import pytest
import request_text
from backlog_testing import git
from test_backlog_lines import ABANDON
from test_request_flow import DOWN, UP, record, run, where

REPO = os.environ.get("SHOPSYSTEM_TEST_GITHUB_REPO", "")
if not REPO:      # named on the command line: conftest.py leaves it out of every other run
    pytest.skip("no $SHOPSYSTEM_TEST_GITHUB_REPO to write issues to", allow_module_level=True)


@pytest.fixture
def pair(ready_repo, tmp_path_factory):
    down = tmp_path_factory.mktemp("down")
    git(down, "init", "-q", "-b", "main")
    for key, value in (("user.name", "T"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
        git(down, "config", key, value)
    (down / "spec").mkdir()
    (down / "spec/index.md").write_text("---\nid: %s\n---\n# down\n\n## Upstreams\n- %s: the upstream, github: %s\n"
                                        % (DOWN, UP, REPO))
    git(down, "add", "-A")
    git(down, "commit", "-qm", "init")
    git(ready_repo, "remote", "add", "origin", "https://github.com/%s.git" % REPO)
    env = {k: v for k, v in os.environ.items() if k not in ("GH_TOKEN", "SHOPSYSTEM_WORK_GH")}
    opened = []
    yield ready_repo, down, env, opened
    for url in opened:
        subprocess.run(["gh", "issue", "close", url], env=env, capture_output=True)


def test_a_request_goes_from_ask_to_resolution_on_github(pair):
    up, down, env, opened = pair
    _, url = run(down, env, "request", "A test request of shopsystem-bdd", "--from", DOWN, "--thread",
                 "job-thread/ex.com/prod/t1", "--ask", "Only a test; it closes itself.").split()
    opened.append(url)
    run(up, env, "sync")
    taken = [p for p in (up / ".shop" / "requests").glob("q*.md") if request_text.field(p.read_text(), "issue") == url]
    assert len(taken) == 1
    name = taken[0].stem
    run(up, env, "offer", name, "--capability", "work-queue")
    run(down, env, "sync")
    assert where(record(down)) == ("awaiting-asker", "asker")
    run(down, env, "propose", "q1", "--line", ABANDON)
    run(down, env, "turn", "q1")
    run(up, env, "sync")
    run(up, env, "outcome", name, "1", "accepted", "--into", "work-queue")
    run(up, env, "turn", name)
    run(up, env, "accept", name)
    run(up, env, "resolve", name, "--line", "1", "work-queue#r5", "2.1.0")
    run(down, env, "sync")
    assert where(record(down)) == ("delivered", "asker")
    state = subprocess.run(["gh", "issue", "view", url, "--json", "state"], env=env, capture_output=True, text=True)
    assert '"CLOSED"' in state.stdout, state.stdout + state.stderr
