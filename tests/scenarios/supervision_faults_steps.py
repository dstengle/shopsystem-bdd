"""supervision's steps about where a work-item stops: awaiting a ruling or failed, its branch kept, the remote it is
pushed to, and the faults `work run` records."""
import re

from pytest_bdd import given, parsers, then

from .supervision_world import commit_all, fields, git, item_text, log_lines, remote_dir, section, starts, tree_has, work_commits, work_item_of, write


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
    other = repo.parent / "other"
    git(repo.parent, "clone", "-q", "-b", "main", str(remote_dir(repo)), str(other))
    git(other, "-c", "user.name=Other", "-c", "user.email=other@example.com", "commit", "-q", "--allow-empty", "-m", "elsewhere")
    git(other, "push", "-q", "origin", "main")


@given("every worker gives DONE, the remote refusing pushes once the implementer has started")
def remote_refuses_later(repo, plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-implementer"] = {"touch": [str(remote_dir(repo) / "refuse")]}


@given(parsers.re(r"the researcher's session ends at its turn limit, having written (?P<result>no result file|a result "
                  r"file that is not JSON)$"))
def researcher_turn_limit(plan, result):
    plan["code-scout"] = {"result": "none" if result.startswith("no ") else "not-json", "subtype": "error_max_turns",
                          "num_turns": 25}


FAULT_WORDS = {
    "that the researcher's session ended at its turn limit": ["researcher", "turn limit"],
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


@then("before each of w1's four workers was started, `work run` had verified that it can push the initiative branch to "
      "the remote")
def verified_before(repo, context):
    lines = [l for l in log_lines(repo) if l.get("work-item") == "w1"]
    starts_at = [i for i, l in enumerate(lines) if l.get("event") == "start"]
    assert len(starts_at) == 4, (lines, context["done"].stderr)
    for before, at in zip([-1] + starts_at, starts_at):
        assert any(l.get("event") == "push verified" for l in lines[before + 1:at]), lines


@then("after each commit `work run` made on the initiative branch, it pushed the initiative branch to the remote")
def pushed_after_each(repo, context):
    pushed = [line.split()[1] for line in (remote_dir(repo) / "pushed").read_text().splitlines() if line.endswith(" refs/heads/main")]
    made = work_commits(repo)
    assert made and all(sha in pushed for sha, _ in made), (made, pushed, context["done"].stderr)


@then("the remote's initiative branch is at the initiative branch's head")
def remote_at_head(repo):
    assert git(remote_dir(repo), "rev-parse", "main") == git(repo, "rev-parse", "main")


@given(parsers.re(r"i1's work-item (?P<name>\w+) is awaiting-ruling, its ## Questions section with \"(?P<question>[^\"]+)\" and "
                  r"(?:no ruling|its Rulings section \"(?P<ruling>[^\"]+)\")$"))
def awaiting_with_questions(repo, name, question, ruling):
    text = item_text(name, "awaiting-ruling") + "\n## Questions\n- %s\n" % question
    write(repo, ".shop/work/i1/%s.md" % name, text + ("\n## Rulings\n- %s\n" % ruling if ruling else ""))
    commit_all(repo, "%s awaiting a ruling" % name)
