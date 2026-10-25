"""supervision's steps about the integrate round `work run` starts (r91, r92, r93, r96): the initiative it is started for, the
change list and drafts the stand-in gives, and the capability-proposals and drafts `work run` commits from them."""
import re

from pytest_bdd import given, parsers, then

from .supervision_rounds_steps import proposed_fulfilling
from .supervision_world import git

DRAFT = "# thing\nThe thing as the integrate round drafted it.\n"
DRAFTS = ".shop/scratch/1-integrate/drafts/spec/capabilities/thing.md"
KEPT = ".shop/work/i1/runs/i1/"


@given(parsers.re(r"i1 is started, has neither a capability-proposal nor a work-item, and fulfils the request q1, whose "
                  r"(?P<text>lines? .+)$"))
def started_fulfilling(repo, text):
    proposed_fulfilling(repo, text, "started")


@given("the integrate round for i1 gives DONE with no change list")
def integrate_without_changes(plan):
    plan["round:integrate"] = {"status": "DONE"}


@given("every other round ends")
def every_other_round_ends(plan):
    plan["initiative-round"] = {"status": "DONE"}


def entry(capability, text):
    """The change-list entry for one capability from "adds thing#r4 and the term "ledger", changes thing#r2 ..."."""
    found = {"capability": capability}
    for kind in ("adds", "changes", "removes"):
        got = re.search(kind + r' (\S+#r\d+)(?: and the term "(\w+)")?', text)
        found[kind] = [got.group(1)] + (["term/" + got.group(2)] if got.group(2) else []) if got else []
    return found


@given(parsers.re(r"the integrate round for i1 gives DONE with a change list that (?P<first>.+) on thing, and "
                  r"(?P<second>.+) on other$"))
def integrate_with_changes(plan, first, second):
    plan["round:integrate"] = {"status": "DONE", "fields": {"changes": [entry("thing", first), entry("other", second)]}}


@given(parsers.re(r"the integrate round for i1 writes spec/capabilities/thing\.md under its drafts path and "
                  r"(?P<ending>gives DONE with a change list naming thing|ends at its turn limit)$"))
def integrate_writes_drafts(plan, ending):
    step = {"status": "DONE", "write": {DRAFTS: DRAFT}}
    if ending.startswith("gives"):
        step["fields"] = {"changes": [entry("thing", "adds thing#r4")]}
    else:
        step["subtype"] = "error_max_turns"
    plan["round:integrate"] = step


@then("`work run` names the integrate round of i1")
def names_integrate_round(context):
    assert "integrate round of i1" in context["done"].stderr, context["done"].stderr


@then("the initiative branch has a commit of the integrate round's drafts, its spec/capabilities/thing.md as the round "
      "wrote it")
def drafts_committed(repo, context):
    kept = [p for p in git(repo, "ls-files", "--", KEPT).split() if p.endswith("drafts/spec/capabilities/thing.md")]
    assert len(kept) == 1, (git(repo, "ls-files", "--", KEPT), context["done"].stdout, context["done"].stderr)
    assert git(repo, "show", "HEAD:" + kept[0]) == DRAFT
    assert git(repo, "log", "--format=%H", "--", kept[0]).split()


def listed(text, field):
    got = re.search(r"^%s: \[(.*)\]$" % field, text, re.M)
    return [i.strip() for i in got.group(1).split(",") if i.strip()] if got else None


@then(parsers.re(r"the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming "
                 r'thing#r4 and the term "ledger", its changes thing#r2 and its removes thing#r3, and one for other, its '
                 r"adds naming other#r1 and its changes and removes naming nothing$"))
def proposals_written(repo, context):
    where = (context["done"].stdout, context["done"].stderr)
    commits = git(repo, "log", "--diff-filter=A", "--format=%H", "--", ".shop/work/i1/thing.md").split()
    assert len(commits) == 1, where
    added = git(repo, "show", "--diff-filter=A", "--name-only", "--format=", commits[0]).split()
    assert sorted(p for p in added if p.startswith(".shop/work/i1/") and p.endswith(".md") and "/runs/" not in p) == [
        ".shop/work/i1/other.md", ".shop/work/i1/thing.md"], (added, where)
    expected = {"thing": (["thing#r4", "term/ledger"], ["thing#r2"], ["thing#r3"]), "other": (["other#r1"], [], [])}
    for name, lists in expected.items():
        text = git(repo, "show", "%s:.shop/work/i1/%s.md" % (commits[0], name))
        assert "\nkind: capability-proposal\n" in text and "\nstatus: drafted\n" in text, text
        assert tuple(listed(text, f) for f in ("adds", "changes", "removes")) == lists, text

