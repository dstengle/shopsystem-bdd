"""supervision's steps about where a work-item stops: awaiting a ruling or failed, its branch kept, the remote it is
pushed to, and the faults `work run` records."""
from pytest_bdd import parsers, then

from .supervision_world import git, starts, work_item_of


@then(parsers.parse("git lists the branch work/w1, with the implementer's commit of feature.txt"))
def branch_kept(repo, context):
    assert git(repo, "branch", "--list", "work/w1").strip(), (git(repo, "branch"), context["done"].stderr)
    assert "feature.txt" in git(repo, "show", "--name-only", "--format=", "work/w1").split(), git(repo, "log", "--stat", "work/w1")


@then(parsers.re(r"no worker was started for (?P<name>\w+)$"))
def none_for(repo, context, name):
    started = [c for c in starts(repo) if work_item_of(c) == name]
    assert started == [], (started, context["done"].stderr)
