"""features/supervision.feature, bound to `work run` (scripts/work and its supervisor scripts/supervise.py): every
scenario, by `scenarios()`.

The Background builds a git repository in `repo` (the initiative branch is the one checked out) with tests a
`.shop/delivery.toml` names, and puts tests/scripts/stub_claude.py first on PATH as `claude` and in
$SHOPSYSTEM_WORK_CLAUDE, so no model runs. A Given writes the work-items and commits them, or adds to what the stand-in
is told to do (`context["plan"]`); the When runs `work run` once as a program; the Then steps read what it printed,
the stand-in's record of its calls, log.jsonl, the files and the git history.

The Given steps are supervision_given.py's, the Then steps about the workers supervision_then_workers.py's and the
helpers they share supervision_world.py's; the When and the Then steps about the work-items, the repository and the
exit are here.
"""
import itertools
import json
import os
import shlex
import subprocess
import sys

from pytest_bdd import parsers, scenarios, then, when

from .conftest import SCRIPTS
from .supervision_answers_steps import *
from .supervision_faults_steps import *
from .supervision_given import *
from .supervision_parallel_steps import *
from .supervision_review_steps import *
from .supervision_tests_steps import *
from .supervision_then_workers import *
from .supervision_world import *
from .supervision_world import (
    BY_WORKER,
    fields,
    git,
    moves,
    section,
    state,
    tree_has,
    work_commits,
)

scenarios("supervision.feature")


# --- When -----------------------------------------------------------------------------------------------------

@when(parsers.parse("the person runs `work {args}`"))
def run_work(repo, plan, context, args):
    stub = repo.parent / "stub"
    (stub / "plan.json").write_text(json.dumps(plan))
    env = dict({k: v for k, v in os.environ.items() if k != "SHOPSYSTEM_WORK_RUN_WORKER"}, PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"), PYTEST_XDIST_AUTO_NUM_WORKERS="2",
               CLAUDE_CONFIG_DIR=str(stub / "claude"),     # where the stand-in keeps its sessions' transcripts
               **context.get("env", {}))     # `-n auto` in a scenario's own small suite: two processes, not one a CPU
    context["before"] = state(repo)
    context["done"] = subprocess.run([sys.executable, str(context.get("work", SCRIPTS / "work")), *shlex.split(args)], cwd=repo, env=env,
                                     capture_output=True, text=True, timeout=300)


@when("`work run i1` is started by a worker of another `work run`")
def run_by_worker(repo, plan, context):
    context["env"] = BY_WORKER
    run_work(repo, plan, context, "run i1")


@then("`work run` refuses, saying that it was started by a worker of another `work run`")
def refuses_worker(context):
    done = context["done"]
    assert done.returncode != 0 and "it was started by a worker of another `work run`" in done.stderr, done


# --- Then -----------------------------------------------------------------------------------------------------

@then(parsers.parse("{names} are green"))
def all_green(repo, context, names):
    for name in names.replace(", ", " and ").split(" and "):
        assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "green", (name, context["done"].stdout, context["done"].stderr)


@then(parsers.parse("{name} is green"))
def is_green(repo, context, name):
    assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "green", (context["done"].stdout, context["done"].stderr)


@then("it exits successfully")
def exits_successfully(context):
    assert context["done"].returncode == 0, context["done"]


@then("it exits with an error")
def exits_with_error(context):
    assert context["done"].returncode != 0, context["done"]


@then(parsers.parse("log.jsonl gives {name}'s transitions from {first} to {rest}, in that order"))
def moves_in_order(repo, context, name, first, rest):
    statuses = [first] + rest.replace(" and ", ", ").split(", ")
    assert moves(repo, name) == list(itertools.pairwise(statuses)), (moves(repo, name), context["done"].stderr)


@then("the initiative branch has the implementer's commit of feature.txt")
def merged(repo, context):
    subjects = git(repo, "log", "main", "--format=%s").splitlines()
    assert any(s.startswith("bdd-implementer:") for s in subjects) and tree_has(repo, "feature.txt"), (
        subjects, context["done"].stderr)


@then("the initiative branch does not have feature.txt")
def no_feature(repo, context):
    assert not tree_has(repo, "feature.txt"), context["done"].stderr


@then("the initiative branch does not have the implementer's commit")
def not_merged(repo):
    subjects = git(repo, "log", "main", "--format=%s").splitlines()
    assert not any(s.startswith("bdd-implementer:") for s in subjects) and not tree_has(repo, "feature.txt"), subjects


@then(parsers.re(r"(?P<name>\w+) is awaiting-answer$"))
def awaiting(repo, context, name):
    assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "awaiting-answer", (context["done"].stdout, context["done"].stderr)


@then(".shop/work/i1/initiative.md is as it was")
def initiative_as_it_was(repo, context):
    assert (repo / ".shop/work/i1/initiative.md").read_text() == context["initiative.md"]


@then(".shop/work/i2/initiative.md and .shop/work/i1/initiative.md are as that session committed them, with nothing "
      "under .shop/work/ left uncommitted")
def elsewhere_kept(repo, context):
    for rel, text in context["elsewhere"].items():
        assert (repo / rel).is_file() and (repo / rel).read_text() == text, rel
        assert git(repo, "show", "HEAD:" + rel) == text, rel
    assert git(repo, "status", "--porcelain", "--", ".shop/work") == ""


@then("the researcher's notes.md is in its stage directory")
def notes_kept(repo):
    found = list((repo / ".shop/work/i1/runs/w1").glob("*-research/notes.md"))
    assert len(found) == 1 and found[0].read_text() == "what the researcher found\n", found


@then("the initiative branch has one commit for each transition log.jsonl gives")
def one_commit_per_move(repo, context):
    made = work_commits(repo)
    assert moves(repo) and len(made) == len(moves(repo)), (made, moves(repo), context["done"].stderr)


@then("each of those commits changes .shop/work/i1/w1.md and .shop/work/i1/log.jsonl, and nothing but them and w1's "
      "stage directories")
def commit_contents(repo):
    for sha, subject in work_commits(repo):
        changed = set(git(repo, "show", "--name-only", "--format=", sha).split())
        assert {".shop/work/i1/w1.md", ".shop/work/i1/log.jsonl"} <= changed, (subject, changed)
        others = changed - {".shop/work/i1/w1.md", ".shop/work/i1/log.jsonl"}
        assert all(p.startswith(".shop/work/i1/runs/w1/") for p in others), (subject, others)


@then("README.md's change is still not committed")
def readme_not_committed(repo):
    assert git(repo, "status", "--porcelain", "README.md").startswith(" M"), git(repo, "status", "--porcelain")
    assert git(repo, "show", "main:README.md") == "# repo\n"


@then(parsers.re(r'`work run` prints (?P<name>\w+) with (?P<status>[\w-]+) and the question "(?P<question>[^"]+)", '
                 r'and (?P<name2>\w+) with (?P<status2>[\w-]+)$'))
def prints_end(context, name, status, question, name2, status2):
    out = context["done"].stdout.splitlines()
    for n, s in ((name, status), (name2, status2)):
        assert [l for l in out if n in l.split() and s in l.split()], (n, s, out)
    assert [l for l in out if question in l], out


@then(parsers.re(r"`work run` prints (?P<name>\w+) with (?P<status>[\w-]+), and (?P<name2>\w+) with (?P<status2>[\w-]+)$"))
def prints_statuses(context, name, status, name2, status2):
    out = context["done"].stdout.splitlines()
    for n, s in ((name, status), (name2, status2)):
        assert [l for l in out if n in l.split() and s in l.split()], (n, s, out)


@then(parsers.parse("work says that {reason}"))
def says(context, reason):
    err = context["done"].stderr
    assert "Traceback" not in err and reason in err, err


@then("nothing in the repository has changed, its commits included")
def nothing_changed(repo, context):
    assert state(repo) == context["before"]


@then(parsers.parse("{first} and {second} are not there"))
def not_there(repo, context, first, second):
    for rel in (first, second):
        assert not (repo / rel).exists(), (rel, context["done"].stderr)


@then("git lists no worktree but the repository's own")
def no_worktree(repo, context):
    trees = git(repo, "worktree", "list", "--porcelain").count("worktree ")
    assert trees == 1, git(repo, "worktree", "list")


@then("the branch work/w1 changes nothing under .shop/work/")
def branch_put_back(repo):
    assert git(repo, "branch", "--list", "work/w1").strip(), git(repo, "branch")
    assert git(repo, "diff", "--name-only", "main...work/w1", "--", ".shop/work/") == "", git(repo, "log", "--stat", "main..work/w1")


@then(parsers.re(r'(?P<name>\w+)\'s ## Questions holds "(?P<old>[^"]+)" and then "(?P<new>[^"]+)", and its Answers '
                 r'section only "(?P<answer>[^"]+)"$'))
def sections(repo, context, name, old, new, answer):
    text = (repo / (".shop/work/i1/%s.md" % name)).read_text()
    asked = [l for l in section(text, "Questions").splitlines() if l.strip()]
    answered = [l for l in section(text, "Answers").splitlines() if l.strip()]
    assert len(asked) == 2 and old in asked[0] and new in asked[1], (text, context["done"].stderr)
    assert answered == ["- " + answer], text


@then(parsers.re(r'`work run` prints the question "(?P<question>[^"]+)"$'))
def prints_question(context, question):
    assert question in context["done"].stdout, context["done"]


@then(parsers.re(r'it prints neither "(?P<first>[^"]+)" nor "(?P<second>[^"]+)"$'))
def prints_neither(context, first, second):
    out = context["done"].stdout
    assert first not in out and second not in out, out


@then("w1's implementation stage directory has report.md, as the implementer wrote it")
def report_copied(repo, context):
    found = list((repo / ".shop/work/i1/runs/w1").glob("*-implement/report.md"))
    assert len(found) == 1 and found[0].read_text() == "the implementer's report\n", (found, context["done"].stderr)


@then(parsers.parse("git lists no branch {branch}"))
def no_branch(repo, context, branch):
    assert git(repo, "branch", "--list", branch).strip() == "", (git(repo, "branch"), context["done"].stderr)
