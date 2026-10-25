"""Probes of `work run` on a proposed initiative's integrate round, driven through scripts/work of this worktree.
Each probe builds its own repository and remote under this scratch directory and runs the stand-in claude."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SCRATCH = Path(__file__).resolve().parent
WT = Path(__file__).resolve().parents[3]
WORK = WT / "scripts" / "work"
STUB = WT / "tests" / "scripts" / "stub_claude.py"
DELIVERY = '[tests]\nwork_item = "python3 tests.py --work-item {work_item}"\nsuite = "python3 tests.py"\n'
TESTS_PY = 'print("1 passed in 0.01s")\n'
ALL_DONE = {"default": {"status": "DONE"}, "initiative-round": {"status": "DONE"}}


def git(repo, *args):
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return (p.stdout + p.stderr).strip()


def build(name, outcomes, fulfils="q1", request=True):
    base = SCRATCH / "probe_repos" / name
    if base.exists():
        shutil.rmtree(base)
    repo = base / "repo"
    repo.mkdir(parents=True)
    fm = "---\nid: work-item/x/i1\nkind: initiative\nstatus: proposed\n%s---\n" % (
        "fulfils: %s\n" % fulfils if fulfils else "")
    (repo / ".shop/work/i1").mkdir(parents=True)
    (repo / ".shop/work/i1/initiative.md").write_text(fm)
    if request:
        (repo / ".shop/work/requests").mkdir(parents=True)
        (repo / ".shop/work/requests/q1.md").write_text(
            "---\nid: request/q1\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n"
            + "".join("%d. Line %d text.\n" % (n, n) for n in range(1, 4))
            + "\n## Outcomes\n" + "".join("%d. %s\n" % (n, w) for n, w in sorted(outcomes.items())))
    (repo / ".shop/delivery.toml").write_text(DELIVERY)
    (repo / "tests.py").write_text(TESTS_PY)
    (repo / "README.md").write_text("# repo\n")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Someone")
    git(repo, "config", "user.email", "someone@example.com")
    git(repo, "config", "commit.gpgsign", "false")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "the repository")
    bare = base / "remote.git"
    git(base, "init", "-q", "--bare", str(bare))
    git(repo, "remote", "add", "origin", str(bare))
    git(repo, "push", "-q", "-u", "origin", "main")
    stub = base / "stub"
    (stub / "bin").mkdir(parents=True)
    claude = stub / "bin" / "claude"
    claude.write_text("#!/bin/sh\nexec %s %s \"$@\"\n" % (sys.executable, STUB))
    claude.chmod(0o755)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", "i1 is proposed")
    return repo


def work(repo, plan, args="run i1"):
    stub = repo.parent / "stub"
    (stub / "plan.json").write_text(json.dumps(plan))
    env = {k: v for k, v in os.environ.items() if k not in ("SHOPSYSTEM_WORK_RUN_WORKER", "PYTHONPATH")}
    env.update(PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"), PYTEST_XDIST_AUTO_NUM_WORKERS="2",
               CLAUDE_CONFIG_DIR=str(stub / "claude"))
    return subprocess.run([sys.executable, str(WORK), *args.split()], cwd=repo, env=env,
                          capture_output=True, text=True, timeout=300)


def report(repo, p, label):
    print("\n==== %s" % label)
    print("rc=%s" % p.returncode)
    print("stdout:", p.stdout[-600:])
    print("stderr:", p.stderr[-900:])
    print("status of .shop/work:", repr(git(repo, "status", "--porcelain", "--", ".shop/work")))
    print("initiative.md:", repr((repo / ".shop/work/i1/initiative.md").read_text()))
    print("log:", git(repo, "log", "--oneline", "-4"))
    calls = repo.parent / "stub" / "calls.jsonl"
    if calls.exists():
        for line in calls.read_text().splitlines():
            c = json.loads(line)
            print("call:", c.get("event"), c.get("agent"))
    print("branches:", git(repo, "branch", "--list"))


def test_a_done_round_then_second_run():
    repo = build("a", {1: "accepted", 2: "refused", 3: "accepted"})
    first = work(repo, ALL_DONE)
    report(repo, first, "A first run, integrate round DONE")
    second = work(repo, ALL_DONE)
    report(repo, second, "A second run")


def test_b_request_with_no_accepted_line():
    repo = build("b", {1: "refused", 2: "refused", 3: "refused"})
    p = work(repo, ALL_DONE)
    report(repo, p, "B request held, no accepted line")
    calls = repo.parent / "stub" / "calls.jsonl"
    for line in (calls.read_text().splitlines() if calls.exists() else []):
        c = json.loads(line)
        if c.get("event") == "start":
            print("brief section:", c["brief"][:400].replace("\n", " | "))


def test_c_round_ends_not_done():
    repo = build("c", {1: "accepted", 2: "refused", 3: "accepted"})
    plan = {"default": {"status": "DONE"}, "initiative-round": {"status": "BLOCKED"}}
    first = work(repo, plan)
    report(repo, first, "C first run, integrate round BLOCKED")
    second = work(repo, plan)
    report(repo, second, "C second run")


def test_d_no_fulfils_stays_proposed():
    repo = build("d", {1: "accepted"}, fulfils=None)
    p = work(repo, ALL_DONE)
    report(repo, p, "D proposed, no fulfils")
