"""supervision's steps about where a work-item stops: awaiting a ruling or failed, its branch kept, the remote it is
pushed to, and the faults `work run` records."""
import re

from pytest_bdd import given, parsers, then

from .supervision_world import (
    calls,
    commit_all,
    fields,
    git,
    item_text,
    remote_dir,
    section,
    starts,
    tree_has,
    work_commits,
    work_item_of,
    write,
)


@then(parsers.parse("git lists the branch work/w1, with the implementer's commit of feature.txt"))
def branch_kept(repo, context):
    assert git(repo, "branch", "--list", "work/w1").strip(), (git(repo, "branch"), context["done"].stderr)
    assert "feature.txt" in git(repo, "show", "--name-only", "--format=", "work/w1").split(), git(repo, "log", "--stat", "work/w1")


@then(parsers.re(r"no worker was started for (?P<name>\w+)$"))
def none_for(repo, context, name):
    started = [c for c in starts(repo) if work_item_of(c) == name]
    assert started == [], (started, context["done"].stderr)


@given(parsers.re(r"every worker gives DONE, the researcher (?:also )?changing (?P<path>\S+)$"))
def researcher_changes(repo, plan, context, path):
    plan["default"] = {"status": "DONE"}
    context["initiative.md"] = (repo / ".shop/work/i1/initiative.md").read_text()
    plan["code-scout"] = {"write": {path: "changed by a worker\n"}}


@given("every worker gives DONE, and while the researcher works another session changes .shop/work/i1/initiative.md in "
       "the repository's own checkout without committing it")
def another_session_changes(repo, plan):
    plan["default"] = {"status": "DONE"}
    plan["code-scout"] = {"elsewhere": {"root": str(repo), "write": {".shop/work/i1/initiative.md": "changed elsewhere\n"}}}


@given("the remote refuses pushes to the initiative branch")
def remote_ahead(repo):
    """The remote's initiative branch has a commit the repository does not: git refuses to push over it."""
    git(repo, "push", "-q", "origin", "main")     # the remote has all of the branch's commits, then one more (r54)
    other = repo.parent / "other"
    git(repo.parent, "clone", "-q", "-b", "main", str(remote_dir(repo)), str(other))
    git(other, "-c", "user.name=Other", "-c", "user.email=other@example.com", "commit", "-q", "--allow-empty", "-m", "elsewhere")
    git(other, "push", "-q", "origin", "main")


@given("every worker gives DONE, the remote refusing pushes once the implementer has started")
def remote_refuses_later(repo, plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-implementer"] = {"touch": [str(remote_dir(repo) / "refuse")]}


@given(parsers.re(r"the researcher's session ends with no error and before its turn limit, having written "
                  r"(?P<result>no result file|a result file that is not JSON)$"))
def researcher_no_result(plan, result):
    plan["code-scout"] = {"result": "none" if result.startswith("no ") else "not-json", "subtype": "success",
                          "num_turns": 12}


FAULT_WORDS = {
    "that the researcher's session exited with an error": ["researcher", "session exited with an error"],
    "that the researcher's session left output that holds no JSON result": [
        "researcher", "session left output that holds no JSON result"],
    "how the researcher's session ended": ["researcher", "its session ended as a success (success, 12 turns"],
    "that the researcher's session ended in an error": ["researcher", "session ended on an error"],
    "that the researcher's session ended at its turn limit": ["researcher", "session ended at its turn limit"],
    "that git merge --ff-only work/w1 failed, with git's reason": ["git merge --ff-only work/w1 failed: "],
    "that the push of the initiative branch failed, with git's reason": [
        "the push of the initiative branch", "the remote refuses pushes to this branch"],
    "why the push could not be verified": ["could not verify", "push", "rejected"],
}


@then(parsers.re(r"(?P<name>\w+) is failed, (?:recording|naming) (?P<what>.+)$"))
def is_failed(repo, context, name, what):
    text = (repo / (".shop/work/i1/%s.md" % name)).read_text()
    assert fields(repo / (".shop/work/i1/%s.md" % name))["status"] == "failed", (context["done"].stdout, context["done"].stderr)
    faults = section(text, "Faults")
    for words in FAULT_WORDS.get(what, [what]):
        assert words in faults, (words, text)
    assert git(repo, "status", "--porcelain", "--", ".shop/work") == "", git(repo, "status")


@then("the initiative branch has none of the branch work/w1's commits")
def unmerged(repo, context):
    subjects = git(repo, "log", "main", "--format=%s").splitlines()
    assert not any(s.startswith("bdd-implementer:") for s in subjects), (subjects, context["done"].stderr)
    assert not tree_has(repo, "feature.txt"), subjects


@then(".shop/work/i1/initiative.md is as its last commit holds it")
def initiative_committed(repo):
    assert (repo / ".shop/work/i1/initiative.md").read_text() == git(repo, "show", "HEAD:.shop/work/i1/initiative.md")


@then(parsers.parse("`work run` names {name} and that its researcher changed {path}"))
def names_fault(context, name, path):
    out = context["done"].stdout + context["done"].stderr
    assert [l for l in out.splitlines() if name in l.split() and "failed" in l.split()], out
    assert re.search(r"its researcher changed %s" % re.escape(path), out), out


@then("after each commit `work run` made on the initiative branch, it pushed the initiative branch to the remote")
def pushed_after_each(repo, context):
    pushed = [line.split()[1] for line in (remote_dir(repo) / "pushed").read_text().splitlines() if line.endswith(" refs/heads/main")]
    made = work_commits(repo)
    assert made and all(sha in pushed for sha, _ in made), (made, pushed, context["done"].stderr)


@then("the remote's initiative branch is at the initiative branch's head")
def remote_at_head(repo):
    assert git(remote_dir(repo), "rev-parse", "main") == git(repo, "rev-parse", "main")


@given(parsers.re(r"i1's work-item (?P<name>\w+) is awaiting-answer, its ## Questions section with \"(?P<question>[^\"]+)\" and "
                  r"(?:no answer|its Answers section \"(?P<answer>[^\"]+)\")$"))
def awaiting_with_questions(repo, name, question, answer):
    text = item_text(name, "awaiting-answer") + "\n## Questions\n- %s\n" % question
    write(repo, ".shop/work/i1/%s.md" % name, text + ("\n## Answers\n- %s\n" % answer if answer else ""))
    commit_all(repo, "%s awaiting an answer" % name)


@given(parsers.re(r'i1\'s work-item (?P<name>\w+) is failed, its fault recorded as "(?P<fault>[^"]+)"$'))
def failed_with_fault(repo, name, fault):
    write(repo, ".shop/work/i1/%s.md" % name, item_text(name, "failed") + "\n## Faults\n- %s\n" % fault)
    commit_all(repo, "%s failed" % name)


@then(parsers.re(r'`work run` prints (?P<first>\w+) with (?P<s1>[\w-]+) and the fault "(?P<fault>[^"]+)", and '
                 r'(?P<second>\w+) with (?P<s2>[\w-]+)$'))
def prints_statuses_and_fault(context, first, s1, fault, second, s2):
    lines = [l.strip() for l in context["done"].stdout.splitlines()]
    assert "%s %s" % (first, s1) in lines and "%s %s" % (second, s2) in lines, context["done"].stdout
    assert any(fault in line for line in lines[lines.index("%s %s" % (first, s1)) + 1:]), context["done"].stdout


@then("`work run` names w1 and that it cannot push the initiative branch to the remote")
def names_cannot_push(context):
    out = context["done"].stdout + context["done"].stderr
    assert [l for l in out.splitlines() if "w1" in l.split() and "failed" in l.split()], out
    assert "could not verify that it can push the initiative branch" in out and "Traceback" not in out, out


@given("the remote refuses pushes to the initiative branch once the branch reviewer has started")
def remote_refuses_at_review(repo, plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-branch-reviewer"] = {"touch": [str(remote_dir(repo) / "refuse")]}


@given("the initiative branch has a commit of notes.txt that the remote does not have")
def unpushed_commit(repo, plan):
    write(repo, "notes.txt", "notes\n")
    commit_all(repo, "notes")
    plan["code-scout"] = {"watch": [str(remote_dir(repo) / "pushed")]}


@then("before the researcher was started, the remote's initiative branch had the commit of notes.txt")
def pushed_before_researcher(repo, context):
    sha = git(repo, "log", "-1", "--format=%H", "--", "notes.txt").strip()
    first = calls(repo, ("seen",))[0]
    seen = first["seen"][str(remote_dir(repo) / "pushed")]
    assert [l for l in seen.splitlines() if l.split()[1:] == [sha, "refs/heads/main"]], (seen, context["done"].stderr)


@given(parsers.parse("in the repository's own checkout {changed} is changed and {added} is added, neither committed"))
def uncommitted_at_start(repo, changed, added):
    """A change and a new work-item under .shop/work/ that no commit holds, both still work-items `work run` can read."""
    with open(repo / changed, "a") as out:
        out.write("\nA line no commit holds.\n")
    write(repo, added, item_text(added.rsplit("/", 1)[-1][:-3], "drafted"))


@then(parsers.parse("work's error names {first} and {second}"))
def error_names(context, first, second):
    err = context["done"].stderr
    assert "Traceback" not in err and first in err and second in err, err
