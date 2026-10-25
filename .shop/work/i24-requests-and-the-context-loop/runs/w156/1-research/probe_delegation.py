"""Probes of `work run`'s answers under a delegation (r77, r78): the real `work` entry point, the stand-in claude,
each case in its own scratch repository under this directory. Prints what came back; asserts nothing."""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from tests.scenarios.conftest import SCRIPTS
from tests.scenarios.supervision_delegation_steps import asked_by_the_log, fulfils_with_delegation
from tests.scenarios.supervision_given import repository
from tests.scenarios.supervision_rounds_steps import DIR
from tests.scenarios.supervision_world import git, item_text, starts, write, commit_all

BASE = Path(__file__).resolve().parent
DELEGATION = "Please get everything delivered. Do not stop to ask me questions or permission."
COVERS = {"fields": {"answer": "The delegation covers it."}}


def setup(name):
    root = BASE / name
    shutil.rmtree(root, ignore_errors=True)
    repo = root / "repo"
    repo.mkdir(parents=True)
    plan = repository(repo)
    plan["default"] = {"status": "DONE"}
    plan["initiative-round"] = {"status": "DONE"}
    plan["delegation-answerer"] = dict(COVERS)
    asked_by_the_log(repo)
    return repo, plan


def run(repo, plan, args="run i1"):
    stub = repo.parent / "stub"
    (stub / "plan.json").write_text(json.dumps(plan))
    env = dict({k: v for k, v in os.environ.items() if k != "SHOPSYSTEM_WORK_RUN_WORKER"},
               PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"), PYTEST_XDIST_AUTO_NUM_WORKERS="2",
               CLAUDE_CONFIG_DIR=str(stub / "claude"))
    kept = [p for p in env.get("PYTHONPATH", "").split(os.pathsep) if p and not (Path(p) / "work_items.py").exists()]
    env["PYTHONPATH"] = os.pathsep.join(kept)
    return subprocess.run([sys.executable, str(SCRIPTS / "work"), *args.split()], cwd=repo, env=env,
                          capture_output=True, text=True, timeout=300)


def report(label, repo, done):
    print("\n=== %s" % label)
    print("EXIT", done.returncode)
    print("STDOUT", done.stdout[-600:])
    print("STDERR", done.stderr[-600:])
    for call in starts(repo):
        brief = call.get("brief", "")
        question = [l for l in brief.splitlines() if l.startswith("Question:")]
        reads = brief.split("Read (paths in your worktree):")[-1].split("Run directory:")[0].split()
        print("START", call.get("agent"), question, "READS", reads if question else "")
    for name in ("w1", "p1"):
        path = repo / DIR / (name + ".md")
        if path.exists():
            print("FILE", name, "\n" + path.read_text())
    print("GIT", git(repo, "log", "--oneline", "-6").strip().replace("\n", " | "))
    print("STATUS", repr(git(repo, "status", "--porcelain").strip()))


def test_control_one_question_one_node():
    repo, plan = setup("control")
    fulfils_with_delegation(repo, {}, DELEGATION)
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- Does scripts/log.py own the log?\n")
    commit_all(repo, "w1 awaiting")
    report("control: one question on one node", repo, run(repo, plan, "run i1"))


def test_two_questions_one_node():
    repo, plan = setup("two_questions")
    fulfils_with_delegation(repo, {}, DELEGATION)
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- Does scripts/log.py own the log?\n"
          "- Does scripts/queue.py own the queue?\n")
    commit_all(repo, "w1 awaiting, two questions")
    report("two questions on one node", repo, run(repo, plan))


def test_request_without_delegation():
    repo, plan = setup("no_delegation")
    write(repo, ".shop/work/requests/q1.md", "---\nid: x\nkind: request\nasker: internal\nstatus: accepted\n---\n\n"
          "## Lines\n1. Something.\n")
    write(repo, DIR + "/initiative.md", "---\nid: x\nkind: initiative\nstatus: started\nfulfils: q1\n---\n")
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- Does scripts/log.py own the log?\n")
    commit_all(repo, "no delegation")
    report("request gives no delegation", repo, run(repo, plan))


def test_answer_with_line_break():
    repo, plan = setup("line_break")
    fulfils_with_delegation(repo, {}, DELEGATION)
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- Does scripts/log.py own the log?\n")
    commit_all(repo, "w1 awaiting")
    plan["delegation-answerer"] = {"fields": {"answer": "first line\nsecond line"}}
    report("answer of two lines", repo, run(repo, plan))


def test_partly_answered_node():
    repo, plan = setup("partly")
    fulfils_with_delegation(repo, {}, DELEGATION)
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n## Questions\n- Does scripts/log.py own the log?\n"
          "- Does scripts/queue.py own the queue?\n\n## Answers\n- 2026-10-01: Earlier answer.\n")
    commit_all(repo, "w1 awaiting, first answered")
    report("first question answered by the person, second open", repo, run(repo, plan))


def test_awaiting_answer_with_no_questions():
    repo, plan = setup("no_questions")
    fulfils_with_delegation(repo, {}, DELEGATION)
    write(repo, DIR + "/w1.md", item_text("w1", "awaiting-answer") + "\n")
    commit_all(repo, "w1 awaiting, no questions")
    report("awaiting-answer work-item with no ## Questions", repo, run(repo, plan))
