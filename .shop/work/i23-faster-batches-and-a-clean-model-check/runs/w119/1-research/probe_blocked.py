"""Probe: `work run i1` with blocked_by across initiatives, against today's code. Each case is its own repository
under this scratch directory; the stand-in claude records each worker's start."""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from tests.scenarios.conftest import INDEX, SCRIPTS, cap, full
from tests.scenarios.supervision_world import (
    CONFTEST_PY, DELIVERY, STUB, TESTS_PY, commit_all, git, item_text, remote, write,
)

BASE = Path("/home/vscode/shopsystem-bdd/.shop/worktrees/w119-1-research/.shop/scratch/1-research/probe_blocked_runs")


def build(case, items):
    """items: (initiative, work-item, status, blocked_by list or None)."""
    base = BASE / case
    shutil.rmtree(base, ignore_errors=True)
    repo = base / "repo"
    repo.mkdir(parents=True)
    write(repo, "spec/index.md", INDEX)
    write(repo, "spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
    initiatives = sorted({i for i, _, _, _ in items} | {"i1"})
    for ini in initiatives:
        write(repo, ".shop/work/%s/initiative.md" % ini,
              "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", ini))
    write(repo, ".shop/delivery.toml", DELIVERY)
    write(repo, "tests.py", TESTS_PY)
    write(repo, "conftest.py", CONFTEST_PY)
    write(repo, "README.md", "# repo\n")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Someone")
    git(repo, "config", "user.email", "someone@example.com")
    git(repo, "config", "commit.gpgsign", "false")
    commit_all(repo, "the repository")
    remote(repo)
    for ini, name, status, by in items:
        write(repo, ".shop/work/%s/%s.md" % (ini, name), item_text(name, status, blocked_by=by))
    commit_all(repo, "work-items")
    stub = base / "stub"
    (stub / "bin").mkdir(parents=True)
    claude = stub / "bin" / "claude"
    claude.write_text("#!/bin/sh\nexec %s %s \"$@\"\n" % (sys.executable, STUB))
    claude.chmod(0o755)
    (stub / "plan.json").write_text(json.dumps({"default": {"status": "DONE"}}))
    return repo, stub


def run_case(case, items):
    repo, stub = build(case, items)
    env = dict({k: v for k, v in os.environ.items() if k != "SHOPSYSTEM_WORK_RUN_WORKER"},
               PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"), PYTEST_XDIST_AUTO_NUM_WORKERS="2",
               CLAUDE_CONFIG_DIR=str(stub / "claude"))
    done = subprocess.run([sys.executable, str(SCRIPTS / "work"), "run", "i1"], cwd=repo, env=env,
                          capture_output=True, text=True, timeout=300)
    starts = []
    calls = stub / "calls.jsonl"
    for line in (calls.read_text().splitlines() if calls.exists() else []):
        c = json.loads(line)
        if c["event"] == "start":
            found = re.search(r"Work-item: \.shop/work/(\S+?)\.md", c["brief"])
            starts.append(found.group(1) if found else c["agent"])
    print("\nCASE %s" % case)
    print("  exit %d" % done.returncode)
    print("  stdout: %s" % " | ".join(done.stdout.strip().splitlines()))
    print("  stderr tail: %s" % " | ".join(done.stderr.strip().splitlines()[-2:]))
    print("  worker starts (work-item of each brief): %s" % starts)


def test_scenario_two_blocker_green_in_other_initiative():
    run_case("s2_green_other_initiative", [("i1", "w1", "drafted", ["w2"]), ("i2", "w2", "green", None)])


def test_blocker_not_green_in_other_initiative():
    run_case("blocker_awaiting_other", [("i1", "w1", "drafted", ["w2"]), ("i2", "w2", "awaiting-answer", None)])


def test_blocker_green_same_initiative():
    run_case("blocker_green_same", [("i1", "w1", "drafted", ["w2"]), ("i1", "w2", "green", None)])


def test_blocker_absent_everywhere():
    run_case("blocker_absent", [("i1", "w1", "drafted", ["w9"])])


def test_blocker_green_other_initiative_as_id_form():
    run_case("id_form_other", [("i1", "w1", "drafted", ["work-item/w2"]), ("i2", "w2", "green", None)])
