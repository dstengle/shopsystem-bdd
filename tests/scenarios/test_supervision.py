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
import json
import os
import shlex
import subprocess
import sys

from pytest_bdd import parsers, scenarios, then, when

from .conftest import SCRIPTS
from .supervision_given import *  # noqa: F401,F403  the steps are fixtures pytest-bdd finds by their names here
from .supervision_then_workers import *  # noqa: F401,F403
from .supervision_world import *  # noqa: F401,F403  the `repo` fixture among them
from .supervision_world import fields, git, moves, questions, section, state, tree_has

scenarios("supervision.feature")


# --- When -----------------------------------------------------------------------------------------------------

@when(parsers.parse("the person runs `work {args}`"))
def run_work(repo, plan, context, args):
    stub = repo.parent / "stub"
    (stub / "plan.json").write_text(json.dumps(plan))
    env = dict(os.environ, PATH="%s%s%s" % (stub / "bin", os.pathsep, os.environ.get("PATH", "")),
               SHOPSYSTEM_WORK_CLAUDE=str(stub / "bin" / "claude"), STUB_CLAUDE_PLAN=str(stub / "plan.json"),
               STUB_CLAUDE_CALLS=str(stub / "calls.jsonl"))
    context["before"] = state(repo)
    context["done"] = subprocess.run([sys.executable, str(context.get("work", SCRIPTS / "work")), *shlex.split(args)], cwd=repo, env=env,
                                     capture_output=True, text=True, timeout=300)


# --- Then -----------------------------------------------------------------------------------------------------

@then(parsers.parse("{names} are green"))
def all_green(repo, context, names):
    for name in names.replace(", ", " and ").split(" and "):
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


@then(parsers.parse("log.jsonl gives {name}'s transitions from {first} to {rest}, in that order"))
def moves_in_order(repo, context, name, first, rest):
    statuses = [first] + rest.replace(" and ", ", ").split(", ")
    assert moves(repo, name) == list(zip(statuses, statuses[1:])), (moves(repo, name), context["done"].stderr)


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


@then(parsers.parse("log.jsonl's first transition of {name} is from {before} to {after}"))
def first_move(repo, name, before, after):
    assert moves(repo, name)[:1] == [(before, after)], moves(repo, name)


@then("the researcher's notes.md is in its stage directory")
def notes_kept(repo):
    found = list((repo / ".shop/work/i1/runs/w1").glob("*-research/notes.md"))
    assert len(found) == 1 and found[0].read_text() == "what the researcher found\n", found


@then("the initiative branch has one commit for each transition log.jsonl gives, `work: w1 drafted -> researched` first and "
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


@then(parsers.parse("work says in one line that {reason}"))
def says_in_one_line(context, reason):
    err = context["done"].stderr
    assert "Traceback" not in err and len(err.splitlines()) == 1 and reason in err, err


@then("nothing in the repository has changed, its commits included")
def nothing_changed(repo, context):
    assert state(repo) == context["before"]


@then(parsers.parse("{first} and {second} are not there"))
def not_there(repo, context, first, second):
    for rel in (first, second):
        assert not (repo / rel).exists(), (rel, context["done"].stderr)


@then(parsers.parse("{rel} is not there, and git lists no worktree but the repository's own"))
def no_worktree(repo, context, rel):
    assert not (repo / rel).exists(), (rel, context["done"].stdout, context["done"].stderr)
    trees = git(repo, "worktree", "list", "--porcelain").count("worktree ")
    assert trees == 1, git(repo, "worktree", "list")


@then("the branch work/w1 changes nothing under .shop/work/")
def branch_put_back(repo):
    assert git(repo, "branch", "--list", "work/w1").strip(), git(repo, "branch")
    assert git(repo, "diff", "--name-only", "main...work/w1", "--", ".shop/work/") == "", git(repo, "log", "--stat", "main..work/w1")


@then(parsers.re(r'(?P<name>\w+)\'s Questions section holds "(?P<old>[^"]+)" and then "(?P<new>[^"]+)", and its Rulings '
                 r'section only "(?P<ruling>[^"]+)"$'))
def sections(repo, context, name, old, new, ruling):
    text = (repo / (".shop/work/i1/%s.md" % name)).read_text()
    asked = [l for l in section(text, "Questions").splitlines() if l.strip()]
    ruled = [l for l in section(text, "Rulings").splitlines() if l.strip()]
    assert len(asked) == 2 and old in asked[0] and new in asked[1], (text, context["done"].stderr)
    assert ruled == ["- " + ruling], text


@then(parsers.re(r'`work run` prints the question "(?P<question>[^"]+)" and not "(?P<other>[^"]+)"$'))
def prints_question_only(context, question, other):
    out = context["done"].stdout
    assert question in out and other not in out, out


@then(parsers.parse("{run_dir} has report.md, as the implementer wrote it"))
def report_copied(repo, context, run_dir):
    report = repo / run_dir / "report.md"
    assert report.is_file() and report.read_text() == "the implementer's report\n", (
        sorted(str(p.relative_to(repo)) for p in (repo / run_dir).rglob("*")), context["done"].stderr)


@then(parsers.parse("git lists no branch {branch}"))
def no_branch(repo, context, branch):
    assert git(repo, "branch", "--list", branch).strip() == "", (git(repo, "branch"), context["done"].stderr)


@then("the initiative branch has both implementers' commits, one after the other, with no merge commit")
def merged_in_line(repo, context):
    subjects = git(repo, "log", "main", "--format=%s").splitlines()
    assert len([s for s in subjects if s.startswith("bdd-implementer:")]) == 2, (subjects, context["done"].stderr)
    assert git(repo, "log", "--merges", "--format=%s", "main") == "", git(repo, "log", "--graph", "--oneline", "main")
