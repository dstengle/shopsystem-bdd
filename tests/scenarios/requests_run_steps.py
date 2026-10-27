"""features/requests.feature's steps about `work run` in an upstream's repository taking in what has been sent before its
intake rounds start (requests r40): the upstream is a repository `work run` can run in, with the stand-in claude of
supervision's scenarios (tests/scripts/stub_claude.py) first on PATH, and a request q1 sent and not yet taken in."""
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

from pytest_bdd import given, then

from . import requests_world_steps as world
from .requests_send_steps import request_item
from .supervision_world import CONFTEST_PY, DELIVERY, STUB, TESTS_PY
from .work_queue_git_steps import git


@given("a request q1 that the asker ctx-a has sent to the upstream ctx-u and that ctx-u has not taken in")
def sent_and_not_taken(repo, context):
    world.upstream(repo, context, "ctx-u")
    world.asker_repo(repo, context, "ctx-a")
    world.send(repo, context, "ctx-a", request_item("q1", "ctx-a"))
    for rel, text in ((".shop/delivery.toml", DELIVERY), ("tests.py", TESTS_PY), ("conftest.py", CONFTEST_PY), ("README.md", "# repo\n")):
        (repo / rel).write_text(text)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "the repository")
    origin = world.sibling(repo, "origin.git")
    subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True, capture_output=True)
    git(repo, "remote", "add", "origin", str(origin))
    git(repo, "push", "-q", "-u", "origin", "main")
    stub = world.sibling(repo, "stub")
    (stub / "bin").mkdir(parents=True)
    claude = stub / "bin" / "claude"
    claude.write_text("#!/bin/sh\nexec %s %s \"$@\"\n" % (shlex.quote(sys.executable), shlex.quote(str(STUB))))
    claude.chmod(0o755)
    (stub / "plan.json").write_text(json.dumps({"initiative-round": {"status": "DONE", "watch": [".shop/work/requests/q1.md"]}}))
    context["stub"] = stub


def stub_env(context):
    """The environment `work run` runs in with the stand-in claude, as supervision's scenarios give it."""
    stub = context["stub"]
    env = dict({k: v for k, v in os.environ.items() if k != "SHOPSYSTEM_WORK_RUN_WORKER"},
               PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"), PYTEST_XDIST_AUTO_NUM_WORKERS="2",
               CLAUDE_CONFIG_DIR=str(stub / "claude"))
    kept = [p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p and not (Path(p) / "work_items.py").exists()]
    env["PYTHONPATH"] = os.pathsep.join(kept)
    return env


def records(context):
    path = context["stub"] / "calls.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def first_intake(context):
    """The stand-in's records from the start of the first intake round on: its start, then what it saw."""
    found = records(context)
    at = next(i for i, c in enumerate(found) if c["event"] == "start" and "Kind: intake" in c["brief"])
    return found[at], found[at + 1]


@then("ctx-u had taken in q1 when work run started its first round of the kind intake")
def taken_in_before_the_round(context):
    start, seen = first_intake(context)
    assert seen["event"] == "seen" and "asker: ctx-a\n" in seen["seen"][".shop/work/requests/q1.md"], (seen, context["done"])


@then("that round is given q1")
def the_round_is_given_q1(context):
    start, _ = first_intake(context)
    assert "# intake of q1" in start["brief"] and "Request: .shop/work/requests/q1.md" in start["brief"], start["brief"]

