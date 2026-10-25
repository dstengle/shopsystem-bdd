"""features/work-queue.feature's steps about the git repository the work-queue is in (r9): `work add` and `work retry`
commit what they change on the current branch.

`init` makes a scenario's repository a git repository on main, with an identity, before anything is committed; a Given
here commits all of it, and the Then steps read main's history and what git says is not committed.
"""
import re
import subprocess

from pytest_bdd import given, parsers, then

from .conftest import full


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True).stdout


def init(repo):
    """`repo` as a git repository on main with an identity and no signing, once."""
    if (repo / ".git").exists():
        return
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "someone")
    git(repo, "config", "user.email", "someone@example.com")
    git(repo, "config", "commit.gpgsign", "false")


@given(parsers.parse("an initiative {ident} under .shop/work/ with a work-item {name} that failed in its implementation stage"))
def failed_implementing(repo, ident, name):
    """A work-item claimed from ready whose implementation stage failed: `work retry` returns it to claimed."""
    from .test_work_queue import initiative, log_line, write
    initiative(repo, ident)
    write(repo, ".shop/work/%s/%s.md" % (ident, name), "---\nid: %s\nkind: work-item\npart_of: initiative/%s\nstatus: failed\n"
          "---\n\n# %s\n" % (full("work-item", name), ident, name))
    write(repo, ".shop/work/%s/log.jsonl" % ident, log_line(name, "planned", "ready") + log_line(name, "ready", "claimed")
          + log_line(name, "claimed", "failed"))


@given("the repository is a git repository on the branch main, everything in it committed")
def all_committed(repo, context):
    init(repo)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "the repository as the scenario gives it")
    context["head"] = git(repo, "rev-parse", "main").strip()


@then(parsers.parse("main has a new last commit, which holds {rel} as work left it"))
def new_commit_holds(repo, context, rel):
    rel = _resolved(repo, context, rel)
    done = context["done"]
    assert done.returncode == 0, done
    assert git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip() == "main"
    assert git(repo, "rev-parse", "main").strip() != context["head"], (git(repo, "log", "--oneline"), done.stderr)
    rel = kept(rel)
    assert git(repo, "show", "main:" + rel) == (repo / rel).read_text()


def _resolved(repo, context, phrase):
    """`phrase` as a path: "the new initiative's initiative.md" and "the new initiative's directory under .shop/work/"
    name the one initiative that is new since the When's snapshot; any other phrase is already a path."""
    if not phrase.startswith("the new initiative's "):
        return phrase
    from .work_queue_start_steps import new_initiatives
    found = new_initiatives(repo, context)
    assert len(found) == 1, found
    rel = str(found[0].relative_to(repo))
    if phrase.endswith("initiative.md"):
        return rel + "/initiative.md"
    assert found[0].is_dir()
    return rel


def kept(rel):
    """The path of `rel`, which may be a request's id (q1) instead: a request is kept in .shop/work/requests/."""
    return ".shop/work/requests/%s.md" % rel if re.fullmatch(r"q\d+", rel) else rel


@then(parsers.parse("nothing work keeps for {request} differs from main's last commit"))
def request_uncommitted(repo, context, request):
    nothing_uncommitted(repo, context, kept(request))


@then(parsers.parse("nothing under {where} differs from main's last commit"))
def nothing_uncommitted(repo, context, where):
    where = _resolved(repo, context, where)
    left = git(repo, "status", "--porcelain", "--untracked-files=all", "--", where)
    assert left == "", left
