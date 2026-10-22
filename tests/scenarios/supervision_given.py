"""supervision's Given steps: the work-items a scenario writes and commits, and what the stand-in claude is told
to do (`plan`)."""
import json
import re
import shlex
import shutil
import sys

from pytest_bdd import given, parsers

from .conftest import INDEX, ROOT, cap, feature, full
from .supervision_world import CONFTEST_PY, DELIVERY, NEEDS_FEATURE, ROLES, STUB, TESTS_PY, commit_all, committed, git, item_text, remote, scripts_in, write


@given("a git repository with an initiative i1 under .shop/work/, a remote the initiative branch can be pushed to, a "
       "stand-in claude first on PATH and as $SHOPSYSTEM_WORK_CLAUDE, and tests that pass", target_fixture="plan")
def repository(repo):
    write(repo, "spec/index.md", INDEX)
    write(repo, "spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
    write(repo, ".shop/work/i1/initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", "i1"))
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
    stub = repo.parent / "stub"
    (stub / "bin").mkdir(parents=True)
    claude = stub / "bin" / "claude"
    claude.write_text("#!/bin/sh\nexec %s %s \"$@\"\n" % (shlex.quote(sys.executable), shlex.quote(str(STUB))))
    claude.chmod(0o755)
    return {}


@given(parsers.re(r"i1's work-items? (?P<items>[\w -]+?)(?:, under (?P<under>\w+))?"
                  r"(?:, though log\.jsonl's last transition of (?P<lname>\w+) is to (?P<lafter>[\w-]+))?"
                  r"(?P<nogit>, in a directory that is not a git repository)?"
                  r"(?P<detached>, its checkout's HEAD detached)?$"))
def work_items(repo, items, under, lname, lafter, nogit, detached):
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
    if nogit:
        shutil.rmtree(repo / ".git")
    if detached:
        git(repo, "checkout", "-q", "--detach")


@given("every worker gives DONE")
def every_done(plan):
    plan["default"] = {"status": "DONE"}


@given(parsers.re(r"every worker gives DONE, the implementer (?P<doing>committing .+|giving .+|deleting its own branch)$"))
def done_implementer(repo, plan, doing):
    """The implementer's commit, its result, or (with its stage's tools widened in .shop/delivery.toml to let it) the
    deletion of its own branch, which makes work run's merge fail."""
    plan["default"] = {"status": "DONE"}
    if doing.startswith("committing "):
        commit = {}
        for what in doing[len("committing "):].split(" and "):
            commit.update(committed(what))
        plan["bdd-implementer"] = {"commit": commit}
    elif doing.startswith("giving "):
        status, question = re.match(r'giving (\S+), asking "([^"]+)"$', doing).groups()
        plan["bdd-implementer"] = {"status": status, "questions": [question]}
    else:
        plan["bdd-implementer"] = {"run": [["git", "checkout", "-q", "--detach"], ["git", "branch", "-q", "-D", "work/w1"]]}
        with open(repo / ".shop/delivery.toml", "a") as out:
            out.write('\n[allowed_tools]\nimplement = ["Read", "Write", "Bash(git checkout *)", "Bash(git branch *)"]\n')
        commit_all(repo, "the implementer may delete its branch")


@given(parsers.parse("every worker gives DONE, the {who} running `{command}`"))
def worker_runs(plan, who, command):
    plan["default"] = {"status": "DONE"}
    plan[ROLES[who]] = {"run": [shlex.split(scripts_in(command))]}


@given(".shop/delivery.toml names no tools")
def no_tools(repo):
    assert "allowed_tools" not in (repo / ".shop/delivery.toml").read_text()


@given(parsers.parse(".shop/delivery.toml gives the {stage} stage {tools}"))
def stage_tools(repo, stage, tools):
    listed = tools.replace(" and ", ", ").split(", ")
    with open(repo / ".shop/delivery.toml", "a") as out:
        out.write('\n[allowed_tools]\n%s = [%s]\n' % (stage, ", ".join('"%s"' % t for t in listed)))
    commit_all(repo, "the %s stage's tools" % stage)


@given(parsers.re(r'the researcher gives (?P<status>[A-Z_-]+), its questions the (?:string "(?P<text>[^"]+)"|number (?P<number>\d+))$'))
def researcher_odd_questions(plan, status, text, number):
    plan["code-scout"] = {"status": status, "questions": text if text is not None else int(number)}


@given(parsers.re(r"i1's work-item (?P<name>\w+) is (?P<status>[\w-]+), its file with a ## Questions of "
                  r'"(?P<question>[^"]+)" and then a Rulings section with "(?P<ruling>[^"]+)"$'))
def item_with_sections(repo, name, status, question, ruling):
    write(repo, ".shop/work/i1/%s.md" % name, item_text(name, status) + "\n## Questions\n- %s\n\n## Rulings\n- %s\n" % (question, ruling))
    commit_all(repo, "a work-item with questions and rulings")


@given(parsers.parse("every worker gives DONE, the researcher also writing {first} and {second}"))
def researcher_adds(plan, first, second):
    plan["default"] = {"status": "DONE"}
    plan["code-scout"] = {"write": {first: "added by a worker\n", second: "added by a worker\n"}}


@given("the work-item's scenarios pass only where feature.txt is")
def needs_feature(repo):
    write(repo, "tests.py", NEEDS_FEATURE)
    commit_all(repo, "the scenarios need feature.txt")


@given(parsers.re(r"(?P<tests>the work-item's scenarios|the whole suite) fails? on the implementer's branch$"))
def failing_tests(plan, tests):
    marker = {"the work-item's scenarios": "scenarios-fail", "the whole suite": "suite-fail"}[tests]
    plan["bdd-implementer"]["commit"][marker] = "\n"


@given(parsers.re(r'the researcher gives (?P<status>[A-Z_-]+)(?:, asking "(?P<question>[^"]+)")?$'))
def researcher_asks(plan, status, question):
    plan["code-scout"] = {"status": status, "questions": [question] if question else []}


@given("every worker gives DONE, the researcher also changing .shop/work/i1/initiative.md and writing notes.md in its "
       "stage directory")
def researcher_meddles(repo, plan, context):
    plan["default"] = {"status": "DONE"}
    context["initiative.md"] = (repo / ".shop/work/i1/initiative.md").read_text()
    plan["code-scout"] = {"write": {".shop/work/i1/initiative.md": "changed by a worker\n"},
                          "notes": {"notes.md": "what the researcher found\n"}}


@given("every worker gives DONE, and while the researcher works another session commits .shop/work/i2/initiative.md and a "
       "change to .shop/work/i1/initiative.md in the repository's own checkout")
def another_session_commits(repo, plan, context):
    plan["default"] = {"status": "DONE"}
    context["elsewhere"] = {".shop/work/i2/initiative.md": "---\nid: %s\nkind: initiative\nstatus: proposed\n---\n" % full("initiative", "i2"),
                            ".shop/work/i1/initiative.md": (repo / ".shop/work/i1/initiative.md").read_text() + "\nChanged by another session.\n"}
    plan["code-scout"] = {"elsewhere": {"root": str(repo), "commit": context["elsewhere"]}}


@given("README.md has a change that is not committed")
def readme_changed(repo):
    write(repo, "README.md", "# repo\n\nA change not committed.\n")


@given(parsers.parse("every worker gives DONE, the {who} loading the skill {skill}"))
def loads_skill(plan, who, skill):
    plan["default"] = {"status": "DONE"}
    plan[ROLES[who]] = {"skills": [skill]}


@given("every worker gives DONE, the researcher also writing notes.md into the repository's own checkout")
def researcher_writes_outside(repo, plan):
    plan["default"] = {"status": "DONE"}
    plan["code-scout"] = {"write": {str(repo / "notes.md"): "written outside the worktree\n"}}


@given("every worker gives DONE, the implementer writing feature.txt and not committing it")
def implementer_leaves_uncommitted(plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-implementer"] = {"write": {"feature.txt": "the feature\n"}}


@given("every worker gives DONE, the implementer writing report.md at the top of its worktree and naming it as its report")
def implementer_names_report(plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-implementer"] = {"write": {"report.md": "the implementer's report\n"}, "names": {"report": "report.md"}}


@given("the repository is the plugin: it holds `work run`'s own scripts and agents")
def repository_is_plugin(repo, context):
    for name in ("scripts", "agents"):
        shutil.copytree(ROOT / name, repo / name, ignore=shutil.ignore_patterns("__pycache__"))
    commit_all(repo, "the repository is the plugin")
    context["work"] = repo / "scripts" / "work"


@given(parsers.re(r'every worker gives DONE, the researcher asking "(?P<question>[^"]+)"$'))
def researcher_done_asks(plan, question):
    plan["default"] = {"status": "DONE"}
    plan["code-scout"] = {"questions": [question]}


@given(parsers.re(r"i1's work-items? (?P<items>\w+ is [\w-]+, its file set .+)$"))
def items_with_file_sets(repo, items):
    """Work-items each with its file set: "w1 is ready, its file set a.txt and b.txt, and w2 is ready, ..."."""
    found = re.findall(r"(\w+) is ([\w-]+), its file set (.+?)(?=,? (?:and )?\w+ is |$)", items)
    assert found, items
    for name, status, files in found:
        write(repo, ".shop/work/i1/%s.md" % name, item_text(name, status, fileset=files.replace(", ", " and ").split(" and ")))
    commit_all(repo, "work-items with file sets")


@given(parsers.re(r'features/thing\.feature has the scenario "(?P<first>[^"]+)", tagged (?P<tag1>@r\d+), and the scenario '
                  r'"(?P<second>[^"]+)", tagged (?P<tag2>@r\d+)$'))
def thing_feature(repo, first, tag1, second, tag2):
    write(repo, "features/thing.feature", feature("thing", (tag1, first), (tag2, second)))
    commit_all(repo, "the thing's scenarios")


@given(parsers.re(r"every worker gives DONE, each implementer committing a file named for its work-item"
                  r"(?P<meet> once two implementers have started)?$"))
def implementers_commit_own(plan, meet):
    """Each implementer commits <its work-item>.txt; with `meet`, only once two implementers have been started."""
    plan["default"] = {"status": "DONE"}
    plan["bdd-implementer"] = dict({"commit": {"{work_item}.txt": "the feature\n"}}, **({"meet": 2} if meet else {}))


@given(parsers.parse("the repository has {rel} committed"))
def has_committed(repo, rel):
    write(repo, rel, "tracked\n")
    commit_all(repo, "add %s" % rel)
