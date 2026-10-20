"""features/supervision.feature, bound to `work run` (scripts/work and its supervisor scripts/supervise.py): every
scenario, by `scenarios()`.

The Background builds a git repository in `repo` (the initiative branch is the one checked out) with tests a
`.shop/delivery.toml` names, and puts tests/scripts/stub_claude.py first on PATH as `claude` and in
$SHOPSYSTEM_WORK_CLAUDE, so no model runs. A Given writes the work-items and commits them, or adds to what the stand-in
is told to do (`context["plan"]`); the When runs `work run` once as a program; the Then steps read what it printed,
the stand-in's record of its calls, log.jsonl, the files and the git history.
"""
import json
import os
import re
import shlex
import subprocess
import sys
import uuid

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from .conftest import INDEX, ROOT, SCRIPTS, cap, full

STUB = ROOT / "tests" / "scripts" / "stub_claude.py"
AGENTS = ["code-scout", "bdd-planner", "bdd-implementer", "bdd-task-reviewer"]
TESTS_PY = """import os, sys
which = "scenarios" if "--work-item" in sys.argv else "suite"
if os.path.exists(which + "-fail"):
    print("FAILED: %s-fail is here, so the %s fails" % (which, which))
    sys.exit(1)
print("passed")
"""
NEEDS_FEATURE = """import os, sys
if "--work-item" in sys.argv and not os.path.exists("feature.txt"):
    print("FAILED: no feature.txt")
    sys.exit(1)
print("passed")
"""
DELIVERY = '[tests]\nwork_item = "python3 tests.py --work-item {work_item}"\nsuite = "python3 tests.py"\n'

scenarios("supervision.feature")


@pytest.fixture
def repo(tmp_path):
    """The repository work run runs in; the stand-in's script and record live beside it, outside it."""
    path = tmp_path / "repo"
    path.mkdir()
    return path


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def write(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return p


def commit_all(repo, message):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "--allow-empty", "-m", message)


def item_text(name, status, under="thing"):
    return "---\nid: %s\nkind: work-item\npart_of: capability-proposal/p1\nstatus: %s\nunder: %s\naccepts: [%s#r1]\n---\n\n# %s\n" % (
        full("work-item", name), status, under, under, name)


def fields(path):
    head = path.read_text().split("---\n")[1]
    return dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)


def calls(repo):
    path = repo.parent / "stub" / "calls.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def starts(repo):
    return [c for c in calls(repo) if c["event"] == "start"]


def work_item_of(call):
    return re.search(r"^Work-item: \.shop/work/i1/(\S+)\.md$", call["brief"], re.M).group(1)


def option(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def log_lines(repo):
    path = repo / ".shop/work/i1/log.jsonl"
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []


def moves(repo, name="w1"):
    return [(l["before"], l["after"]) for l in log_lines(repo) if l.get("work-item") == name and "after" in l]


def questions(repo, name):
    text = (repo / (".shop/work/i1/%s.md" % name)).read_text()
    return text.split("## Questions", 1)[1] if "## Questions" in text else ""


def state(repo):
    """The repository as files (outside .git/), its commits and branches, and what git says is not committed."""
    files = {str(p.relative_to(repo)): p.read_bytes() for p in repo.rglob("*")
             if p.is_file() and ".git" not in p.relative_to(repo).parts}
    return files, git(repo, "rev-parse", "HEAD"), git(repo, "branch", "-a"), git(repo, "status", "--porcelain")


# --- Given ----------------------------------------------------------------------------------------------------

@given("a git repository with an initiative i1 under .shop/work/, a stand-in claude first on PATH and as "
       "$SHOPSYSTEM_WORK_CLAUDE, and tests that pass", target_fixture="plan")
def repository(repo):
    write(repo, "spec/index.md", INDEX)
    write(repo, "spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
    write(repo, ".shop/work/i1/initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
    write(repo, ".shop/delivery.toml", DELIVERY)
    write(repo, "tests.py", TESTS_PY)
    write(repo, "README.md", "# repo\n")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "Someone")
    git(repo, "config", "user.email", "someone@example.com")
    git(repo, "config", "commit.gpgsign", "false")
    commit_all(repo, "the repository")
    stub = repo.parent / "stub"
    (stub / "bin").mkdir(parents=True)
    claude = stub / "bin" / "claude"
    claude.write_text("#!/bin/sh\nexec %s %s \"$@\"\n" % (shlex.quote(sys.executable), shlex.quote(str(STUB))))
    claude.chmod(0o755)
    return {}


@given(parsers.re(r"i1's work-items? (?P<items>.+?)(?:, under (?P<under>\w+))?"
                  r"(?:, though log\.jsonl's last move of (?P<lname>\w+) is to (?P<lafter>[\w-]+))?$"))
def work_items(repo, items, under, lname, lafter):
    if " are " in items:
        names, status = items.split(" are ")
        pairs = [(n, status) for n in names.split(" and ")]
    else:
        pairs = [tuple(pair.split(" is ")) for pair in items.split(" and ")]
    for name, status in pairs:
        write(repo, ".shop/work/i1/%s.md" % name, item_text(name, status, under or "thing"))
    if lname:
        write(repo, ".shop/work/i1/log.jsonl", json.dumps({"time": "2026-10-19T10:00:00+00:00", "work-item": lname,
                                                           "before": "drafted", "after": lafter, "by": "someone"}) + "\n")
    commit_all(repo, "work-items")


@given("every worker gives DONE")
def every_done(plan):
    plan["default"] = {"status": "DONE"}


@given("every worker gives DONE, the implementer committing feature.txt")
def done_committing(plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-implementer"] = {"commit": {"feature.txt": "the feature\n"}}


@given("the work-item's scenarios pass only where feature.txt is")
def needs_feature(repo):
    write(repo, "tests.py", NEEDS_FEATURE)
    commit_all(repo, "the scenarios need feature.txt")


@given(parsers.parse("{tests} fail on the implementer's branch"))
def failing_tests(plan, tests):
    marker = {"the work-item's scenarios": "scenarios-fail", "the whole suite": "suite-fail"}[tests]
    plan["bdd-implementer"]["commit"][marker] = "\n"


@given(parsers.re(r'the researcher gives (?P<status>[A-Z_-]+), asking "(?P<question>[^"]+)"$'))
def researcher_asks(plan, status, question):
    plan["code-scout"] = {"status": status, "questions": [question]}


@given("the researcher writes no result file")
def researcher_no_result(plan):
    plan["code-scout"] = {"result": "none"}


@given("the researcher writes a result file that is not JSON")
def researcher_not_json(plan):
    plan["code-scout"] = {"result": "not-json"}


@given("every worker gives DONE, the researcher also setting w1's status to green, changing "
       ".shop/work/i1/initiative.md and writing notes.md in its run directory")
def researcher_meddles(repo, plan, context):
    plan["default"] = {"status": "DONE"}
    context["initiative.md"] = (repo / ".shop/work/i1/initiative.md").read_text()
    plan["code-scout"] = {"write": {".shop/work/i1/w1.md": item_text("w1", "green"),
                                    ".shop/work/i1/initiative.md": "changed by a worker\n"},
                          "notes": {"notes.md": "what the researcher found\n"}}


@given("README.md has a change that is not committed")
def readme_changed(repo):
    write(repo, "README.md", "# repo\n\nA change not committed.\n")


# --- When -----------------------------------------------------------------------------------------------------

@when(parsers.parse("the person runs `work {args}`"))
def run_work(repo, plan, context, args):
    stub = repo.parent / "stub"
    (stub / "plan.json").write_text(json.dumps(plan))
    env = dict(os.environ, PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"))
    context["before"] = state(repo)
    context["done"] = subprocess.run([sys.executable, str(SCRIPTS / "work"), *shlex.split(args)], cwd=repo, env=env,
                                     capture_output=True, text=True, timeout=300)


# --- Then -----------------------------------------------------------------------------------------------------

@then(parsers.parse("each of {names} had code-scout, bdd-planner, bdd-implementer and bdd-task-reviewer as its workers, in that order"))
def four_workers(repo, context, names):
    for name in names.split(" and "):
        agents = [c["agent"] for c in starts(repo) if work_item_of(c) == name]
        assert agents == ["shopsystem-bdd:" + a for a in AGENTS], (name, agents, context["done"].stderr)


@then("no worker was started before the one before it had ended")
def one_at_a_time(repo):
    events = [(c["event"], c["session"]) for c in calls(repo)]
    assert events and events == [e for s in [c["session"] for c in starts(repo)] for e in (("start", s), ("end", s))], events


@then(parsers.parse("{names} are green"))
def all_green(repo, context, names):
    for name in names.split(" and "):
        assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "green", (name, context["done"].stdout, context["done"].stderr)


@then(parsers.parse("{name} is green"))
def is_green(repo, context, name):
    assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "green", (context["done"].stdout, context["done"].stderr)


@then(parsers.parse("it exits {code:d}"))
def exits(context, code):
    assert context["done"].returncode == code, context["done"]


@then("it exits non-zero")
def exits_non_zero(context):
    assert context["done"].returncode != 0, context["done"]


@then("each worker was started as `claude -p <its brief file>` with --agent shopsystem-bdd:<its stage's agent> and a "
      "session id no other worker had")
def started_as(repo):
    started = starts(repo)
    assert [c["agent"] for c in started] == ["shopsystem-bdd:" + a for a in AGENTS], started
    for c in started:
        argv = c["argv"]
        assert argv[0] == "-p" and os.path.isfile(argv[1]), argv
        assert option(argv, "--agent") == c["agent"], argv
        uuid.UUID(option(argv, "--session-id"))
    sessions = [option(c["argv"], "--session-id") for c in started]
    assert len(set(sessions)) == len(sessions) == 4, sessions


@then("each brief file names .shop/work/i1/w1.md and spec/capabilities/thing.md to read, and a result file in the "
      "brief's own directory")
def brief_names(repo):
    for c in starts(repo):
        brief, path = c["brief"], c["argv"][1]
        assert ".shop/work/i1/w1.md" in brief and "spec/capabilities/thing.md" in brief, brief
        result = re.search(r"^Result file: (.+)$", brief, re.M).group(1).strip()
        assert os.path.dirname(result) == os.path.dirname(path), (result, path)


@then(parsers.parse("log.jsonl moves {name} from {first} to {rest}, in that order"))
def moves_in_order(repo, context, name, first, rest):
    statuses = [first] + rest.replace(" and ", ", ").split(", ")
    assert moves(repo, name) == list(zip(statuses, statuses[1:])), (moves(repo, name), context["done"].stderr)


def tree_has(repo, rel):
    return subprocess.run(["git", "cat-file", "-e", "main:" + rel], cwd=repo).returncode == 0


@then("the initiative branch has the implementer's commit of feature.txt")
def merged(repo, context):
    subjects = git(repo, "log", "main", "--format=%s").splitlines()
    assert any(s.startswith("bdd-implementer:") for s in subjects) and tree_has(repo, "feature.txt"), (
        subjects, context["done"].stderr)


@then("the initiative branch does not have the implementer's commit")
def not_merged(repo):
    subjects = git(repo, "log", "main", "--format=%s").splitlines()
    assert not any(s.startswith("bdd-implementer:") for s in subjects) and not tree_has(repo, "feature.txt"), subjects


@then(parsers.parse("{name} is awaiting-ruling, its question naming `{command}` and what it printed"))
def awaiting_failure(repo, context, name, command):
    assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "awaiting-ruling", context["done"]
    asked = questions(repo, name)
    assert command in asked and "FAILED:" in asked, asked


@then(parsers.parse("{name} is awaiting-ruling, its question saying {question}"))
def awaiting_question(repo, context, name, question):
    assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "awaiting-ruling", context["done"]
    assert question in questions(repo, name), questions(repo, name)


@then(parsers.parse("no worker was started for {name} after the {who}"))
def none_after(repo, name, who):
    agent = {"researcher": "code-scout", "implementer": "bdd-implementer"}[who]
    agents = [c["agent"] for c in starts(repo) if work_item_of(c) == name]
    assert agents and agents[-1] == "shopsystem-bdd:" + agent, agents


@then(".shop/work/i1/initiative.md is as it was")
def initiative_as_it_was(repo, context):
    assert (repo / ".shop/work/i1/initiative.md").read_text() == context["initiative.md"]


@then(parsers.parse("log.jsonl's first move of {name} is from {before} to {after}"))
def first_move(repo, name, before, after):
    assert moves(repo, name)[:1] == [(before, after)], moves(repo, name)


@then("the researcher's notes.md is in its run directory")
def notes_kept(repo):
    found = list((repo / ".shop/work/i1/runs/w1").glob("*-research/notes.md"))
    assert len(found) == 1 and found[0].read_text() == "what the researcher found\n", found


@then("the initiative branch has one commit for each move log.jsonl gives, `work: w1 drafted -> researched` first and "
      "`work: w1 done -> green` last")
def one_commit_per_move(repo, context):
    subjects = [s for s in git(repo, "log", "--reverse", "main", "--format=%s").splitlines() if s.startswith("work: ")]
    assert len(subjects) == len(moves(repo)), (subjects, moves(repo))
    assert subjects[0] == "work: w1 drafted -> researched" and subjects[-1] == "work: w1 done -> green", subjects


@then("each of those commits changes .shop/work/i1/w1.md and .shop/work/i1/log.jsonl, and nothing but them and files "
      "under .shop/work/i1/runs/w1/")
def commit_contents(repo):
    for line in git(repo, "log", "main", "--format=%H %s").splitlines():
        sha, subject = line.split(" ", 1)
        if not subject.startswith("work: "):
            continue
        changed = set(git(repo, "show", "--name-only", "--format=", sha).split())
        assert {".shop/work/i1/w1.md", ".shop/work/i1/log.jsonl"} <= changed, (subject, changed)
        others = changed - {".shop/work/i1/w1.md", ".shop/work/i1/log.jsonl"}
        assert all(p.startswith(".shop/work/i1/runs/w1/") for p in others), (subject, others)


@then("README.md's change is still not committed")
def readme_not_committed(repo):
    assert git(repo, "status", "--porcelain", "README.md").startswith(" M"), git(repo, "status", "--porcelain")
    assert git(repo, "show", "main:README.md") == "# repo\n"


@then("log.jsonl has, for each of w1's four workers, a start line and then an end line, each with the time, w1, the "
      "stage, the agent and the session id claude was given")
def worker_lines(repo):
    lines = [l for l in log_lines(repo) if "after" not in l]
    sessions = [option(c["argv"], "--session-id") for c in starts(repo)]
    assert len(sessions) == 4, sessions
    for c, session in zip(starts(repo), sessions):
        mine = [l for l in lines if l.get("session") == session]
        assert [l.get("event") for l in mine] == ["start", "end"], (session, lines)
        for l in mine:
            assert set(l) >= {"time", "work-item", "stage", "agent", "session"} and l["work-item"] == "w1", l
            assert l["agent"] == c["agent"].split(":", 1)[1] and l["stage"], l


@then(parsers.re(r'work run prints (?P<name>\w+) with (?P<status>[\w-]+) and the question "(?P<question>[^"]+)", '
                 r'and (?P<name2>\w+) with (?P<status2>[\w-]+)$'))
def prints_end(context, name, status, question, name2, status2):
    out = context["done"].stdout.splitlines()
    for n, s in ((name, status), (name2, status2)):
        assert [l for l in out if n in l.split() and s in l.split()], (n, s, out)
    assert [l for l in out if question in l], out


@then(parsers.parse("work says in one line that {reason}"))
def says_in_one_line(context, reason):
    err = context["done"].stderr
    assert "Traceback" not in err and len(err.splitlines()) == 1 and reason in err, err


@then("no worker was started")
def no_worker(repo):
    assert calls(repo) == [], calls(repo)


@then("nothing in the repository has changed, its commits included")
def nothing_changed(repo, context):
    assert state(repo) == context["before"]
