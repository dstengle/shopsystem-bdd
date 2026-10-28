"""supervision's steps about what `work run` makes and gives before a branch review (r154-r157): the runs at the head,
their record in the branch reviewer's brief, its commits with their work-items and its files to read."""
import re

from pytest_bdd import given, parsers, then

from .conftest import cap
from .supervision_review_steps import FINDINGS, reviewer_calls
from .supervision_world import calls, commit_all, git, item_text, write

RUNS = ["the whole suite", "w1's scenarios", "w2's scenarios", "w2's check", "tools check", "tools size",
        "features deprecated", "features bindings"]


def brief(repo):
    found = reviewer_calls(repo)
    assert len(found) == 1, found
    return found[0]["brief"]


def part(text, heading, level="##"):
    """The lines under `heading` of the brief, up to the next heading of its level or above."""
    marker = "\n%s %s\n" % (level, heading)
    assert marker in text, (marker, text)
    return re.split(r"\n#{2,%d} " % len(level), text.split(marker, 1)[1], maxsplit=1)[0]


def run_of(text, title):
    """(command, exit code, output) of the run `title` the brief gives."""
    body = part(text, title, "###")
    command, code = re.search(r"^Command: (.*)$", body, re.M), re.search(r"^Exit code: (\S+)$", body, re.M)
    assert command and code and "\nOutput:\n" in body, body
    return command.group(1), code.group(1), body.split("\nOutput:\n", 1)[1]


def read_list(text):
    return re.findall(r"^- (.+)$", text.split("\nRead:\n", 1)[1].split("\n\n", 1)[0], re.M)


def commit_lines(text):
    """[(commit, work-item or none, subject)] the brief gives."""
    return [tuple(line.strip().split(" ", 2)) for line in part(text, "Commits").splitlines() if line.startswith("    ")]


@given(parsers.re(r"i1's work-items w1 and w2 are green, w2 naming the check `(?P<check>.+)`$"))
def green_with_check(repo, check):
    write(repo, ".shop/work/i1/w1.md", item_text("w1", "green"))
    write(repo, ".shop/work/i1/w2.md", item_text("w2", "green", check=check))
    commit_all(repo, "work-items")


@given(parsers.re(r"i1's work-item w1 is under thing and w2 under other, spec/capabilities/thing\.md's rests_on naming "
                  r"(?P<a>design-decision/\w+) and spec/capabilities/other\.md's rests_on naming (?P<b>design-decision/\w+)$"))
def under_two_capabilities(repo, context, a, b):
    context["unders"] = {"w1": "thing", "w2": "other"}
    write(repo, "spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, `thing` shall answer."], rests_on="[%s]" % a))
    write(repo, "spec/capabilities/other.md", cap("other", ["- [r1] **When** asked, `other` shall answer."], rests_on="[%s]" % b))
    commit_all(repo, "two capabilities")


@given("every worker gives DONE, each planner writing plan.md, each implementer writing report.md and each reviewer "
       "writing findings.md beside its brief")
def writes_beside_brief(plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-branch-reviewer"] = {"notes": {"findings.md": FINDINGS}}
    for agent, name in (("bdd-planner", "plan.md"), ("bdd-implementer", "report.md"), ("bdd-task-reviewer", "findings.md")):
        plan[agent] = {"notes": {name: "# %s\n" % name}}


@given("every worker gives DONE, each implementer committing a change to src/<work-item>.py, and while w1's implementer "
       "works another session commits notes.txt on the initiative branch")
def implementers_change_and_notes(repo, plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-branch-reviewer"] = {"notes": {"findings.md": FINDINGS}}
    plan["bdd-implementer"] = {"commit": {"src/{work_item}.py": "the change\n"},
                               "elsewhere": {"root": str(repo), "commit": {"notes.txt": "notes\n"}, "work_item": "w1"}}


# --- r154: the runs --------------------------------------------------------------------------------------------

@then(parsers.re(r"(?P<run>.+) was run at the initiative branch's head before the branch reviewer was started$"))
def run_before_the_reviewer(repo, context, run):
    text = brief(repo)
    named = re.fullmatch(r"(w\d+'s check) `(.+)`", run)
    title, command = named.groups() if named else (run.strip("`"), "")
    given_command, _, _ = run_of(text, title)
    assert command in given_command, (run, given_command, context["done"].stderr)
    head = re.search(r"^Head: (\w+)$", text, re.M).group(1)
    assert re.search(r"^Ran at: %s$" % head, text, re.M), text
    assert git(repo, "merge-base", "--is-ancestor", head, "main") == "", head
    made = [c for c in calls(repo, ("start", "tests")) if c["event"] == "tests" or c["agent"].endswith("bdd-branch-reviewer")]
    start = next(i for i, c in enumerate(made) if c["event"] == "start")
    here = made[start]["cwd"]
    ran = [c["argv"] for c in made[:start] if c["cwd"] == here]
    if title == "the whole suite":
        assert any("--work-item" not in argv for argv in ran), made
    elif title.endswith("'s scenarios"):
        assert any(argv[-2:] == ["--work-item", title.split("'")[0]] for argv in ran), made


# --- r155: what is given of each run ------------------------------------------------------------------------------

@then("the branch reviewer's brief gives each run made before it was started with its command, how it exited and its output")
def gives_each_run(repo, context):
    text = brief(repo)
    titles = re.findall(r"^### (.+)$", text, re.M)
    assert sorted(titles) == sorted(RUNS), (titles, context["done"].stderr)
    for title in titles:
        assert run_of(text, title)[1].isdigit(), title


@then(parsers.re(r"the branch reviewer's brief gives w2's check with its command, that it exited with an error, and its "
                 r'output "(?P<output>[^"]+)"$'))
def gives_failed_check(repo, output):
    command, code, got = run_of(brief(repo), "w2's check")
    assert "too short" in command and code != "0" and output in got, (command, code, got)


@then("the branch reviewer's brief gives the whole suite's run with its command, that it exited successfully, and its output")
def gives_suite(repo):
    command, code, got = run_of(brief(repo), "the whole suite")
    assert command and code == "0" and got.strip(), (command, code, got)


@then("the branch reviewer's brief names the initiative branch's head as the commit those runs ran at")
def names_head(repo):
    text = brief(repo)
    head = git(repo, "log", "main", "--format=%H", "--grep", "branch review 1 of", "--invert-grep", "-1").strip()
    assert re.search(r"^Ran at: %s$" % head, text, re.M) and re.search(r"^Head: %s$" % head, text, re.M), (head, text)


# --- r156: the commits and the change -----------------------------------------------------------------------------

@then("the branch reviewer's brief gives each commit from the initiative branch's base to its head")
def gives_each_commit(repo, context):
    text = brief(repo)
    base, head = (re.search(r"^%s: (\w+)$" % key, text, re.M).group(1) for key in ("Base", "Head"))
    given = [sha for sha, _, _ in commit_lines(text)]
    assert given == git(repo, "rev-list", "--reverse", "%s..%s" % (base, head)).split() and given, (given, context["done"].stderr)


@then("the branch reviewer's brief gives w1 for w1's implementer's commit, the merge of work/w1 and each commit of a "
      "transition of w1, and w2 for w2's in the same way")
def gives_work_items(repo):
    found = {name: [] for name in ("w1", "w2")}
    for _, owner, subject in commit_lines(brief(repo)):
        for name in found:
            if subject.startswith("bdd-implementer: src/%s.py" % name) or subject.startswith("work: %s " % name):
                found[name].append(owner)
                assert owner == name, (subject, owner)
    for name, owners in found.items():
        assert len(owners) >= 2 and "bdd-implementer" not in owners, (name, commit_lines(brief(repo)))


@then("the branch reviewer's brief gives none for the commit of notes.txt")
def gives_none(repo):
    notes = [c for c in commit_lines(brief(repo)) if c[2] == "another session's commit"]
    assert len(notes) == 1 and notes[0][1] == "none", commit_lines(brief(repo))


@then(parsers.re(r"the branch reviewer's brief gives the change from the initiative branch's base to its head, containing "
                 r"src/w1\.py, src/w2\.py and notes\.txt and nothing under \.shop/$"))
def gives_change(repo):
    change = part(brief(repo), "Change")
    assert all(p in change for p in ("src/w1.py", "src/w2.py", "notes.txt")) and ".shop/" not in change, change


# --- r157: the files to read -------------------------------------------------------------------------------------

@then(parsers.re(r"the branch reviewer's brief names as files to read (?P<first>[\w/.-]+) and (?P<second>[\w/.-]+)$"))
def names_files(repo, first, second):
    files = read_list(brief(repo))
    assert first in files and second in files, files


@then("the branch reviewer's brief names as files to read, for each of w1 and w2, its plan.md, its implementer's "
      "report.md and its reviewer's findings.md, in its stage directories")
def names_stage_files(repo):
    files = read_list(brief(repo))
    for name in ("w1", "w2"):
        for stage in ("plan", "implement", "review"):
            kept = {"plan": "plan.md", "implement": "report.md", "review": "findings.md"}[stage]
            assert any(re.fullmatch(r"\.shop/work/i1/runs/%s/\d+-%s/%s" % (name, stage, kept), f) for f in files), (name, files)
