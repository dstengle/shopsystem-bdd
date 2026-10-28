"""supervision's steps about the integrate round `work run` starts (r91, r92, r93, r96): the initiative it is started for, the
change list and drafts the stand-in gives, and the capability-proposals and drafts `work run` commits from them."""
import re

from pytest_bdd import given, parsers, then

from .conftest import INDEX, cap, full
from .supervision_rounds_steps import proposed_fulfilling, rounds
from .supervision_world import commit_all, git, starts, write

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
def integrate_with_changes(plan, repo, first, second):
    write(repo, "spec/capabilities/other.md", cap("other", ["- [r1] **When** asked, `other` shall answer."]))
    commit_all(repo, "spec/capabilities/ holds the capability other")
    plan["round:integrate"] = {"status": "DONE", "fields": {"changes": [entry("thing", first), entry("other", second)]}}


@given(parsers.re(r'spec/index\.md\'s Glossary holds the terms "(?P<one>\w+)", "(?P<two>\w+)" and "(?P<three>\w+)"$'))
def glossary_holds(repo, one, two, three):
    write(repo, "spec/index.md", INDEX + "\n## Glossary\n\n" + "".join("- **%s**: a thing.\n" % t for t in (one, two, three)))
    commit_all(repo, "spec/index.md's Glossary")


@given(parsers.re(r'the integrate round for i1 gives DONE with a change list that adds the term "(?P<added>\w+)", changes the '
                  r'term "(?P<changed>\w+)" and removes the term "(?P<removed>\w+)" in the glossary$'))
def integrate_changes_glossary(plan, added, changed, removed):
    plan["round:integrate"] = {"status": "DONE", "fields": {"changes": [{
        "glossary": True, "adds": ["term/" + added], "changes": ["term/" + changed], "removes": ["term/" + removed]}]}}


def glossary_proposals(repo):
    """The commits that added a glossary-proposal file under .shop/work/i1/, each with its files' text."""
    found = []
    for commit in git(repo, "log", "--diff-filter=A", "--format=%H", "--", ".shop/work/i1/").split():
        for path in git(repo, "show", "--diff-filter=A", "--name-only", "--format=", commit).split():
            if path.startswith(".shop/work/i1/") and path.endswith(".md") and "/runs/" not in path:
                text = git(repo, "show", "%s:%s" % (commit, path))
                if "\nkind: glossary-proposal\n" in text:
                    found.append((commit, path, text))
    return found


@then(parsers.re(r'the commit that wrote i1\'s glossary-proposal wrote one, drafted, its adds naming the term "(?P<added>\w+)", '
                 r'its changes the term "(?P<changed>\w+)" and its removes the term "(?P<removed>\w+)"$'),
      target_fixture="glossary_text")
def glossary_proposal_written(repo, context, added, changed, removed):
    found = glossary_proposals(repo)
    where = (found, context["done"].stdout, context["done"].stderr)
    assert len(found) == 1, where
    commit, _, text = found[0]
    assert "\nstatus: drafted\n" in text, where
    assert tuple(listed(text, f) for f in ("adds", "changes", "removes")) == (
        ["term/" + added], ["term/" + changed], ["term/" + removed]), where
    return text


@then(parsers.re(r'it names the term "(?P<term>\w+)" in none of its adds, changes and removes$'))
def names_in_none(glossary_text, term):
    for field in ("adds", "changes", "removes"):
        assert "term/" + term not in listed(glossary_text, field), glossary_text


@given("an initiative i2 under .shop/work/, proposed, that fulfils the request q2, whose line 1 has the line outcome accepted")
def proposed_i2(repo):
    write(repo, ".shop/work/i2/initiative.md",
          "---\nid: %s\nkind: initiative\nstatus: proposed\nfulfils: q2\n---\n" % full("initiative", "i2"))
    write(repo, ".shop/work/requests/q2.md", "---\nid: %s\nkind: request\nasker: internal\nstatus: accepted\n---\n\n## Lines\n"
          "1. Line 1 text.\n\n## Outcomes\n1. accepted\n" % full("request", "q2"))
    commit_all(repo, "i2 is proposed and fulfils q2")


@given(parsers.re(r"the integrate round for i1 gives DONE with a change list that (?P<first>.+) on thing, and the integrate "
                  r"round for i2 gives DONE with a change list that (?P<second>.+) on thing$"))
def integrate_each_with_changes(plan, first, second):
    for name, text in (("i1", first), ("i2", second)):
        plan["round:integrate:" + name] = {"status": "DONE", "fields": {"changes": [entry("thing", text)]}}


@given(parsers.re(r"the integrate round for i1 writes spec/capabilities/thing\.md under its drafts path and "
                  r"(?P<ending>gives DONE with a change list naming thing|ends at its turn limit)$"))
def integrate_writes_drafts(plan, ending):
    step = {"status": "DONE", "write": {DRAFTS: DRAFT}}
    if ending.startswith("gives"):
        step["fields"] = {"changes": [entry("thing", "adds thing#r4")]}
    else:
        step["subtype"] = "error_max_turns"
    plan["round:integrate"] = step


@given("spec/capabilities/ holds no capability nowhere")
def spec_lacks_nowhere(repo):
    assert not (repo / "spec/capabilities/nowhere.md").exists()


@given("the integrate round for i1 gives DONE with a change list that adds nowhere#r1 on nowhere, having written no draft of "
       "nowhere under its drafts path")
def integrate_names_nowhere(plan):
    plan["round:integrate"] = {"status": "DONE", "fields": {"changes": [entry("nowhere", "adds nowhere#r1")]}}


@then("i1 has no capability-proposal for nowhere")
def no_proposal_for_nowhere(repo, context):
    assert not (repo / ".shop/work/i1/nowhere.md").exists(), context["done"].stderr
    assert not git(repo, "ls-files", "--", ".shop/work/i1/nowhere.md").strip()


@then("`work run` names the capability nowhere")
def names_nowhere(context):
    assert "nowhere" in context["done"].stderr, (context["done"].stdout, context["done"].stderr)


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


def thing_of(repo, initiative):
    """The text of the capability-proposal for thing that `initiative` has, as the commit that added it wrote it."""
    path = ".shop/work/%s/thing.md" % initiative
    added = git(repo, "log", "--diff-filter=A", "--format=%H", "--", path).split()
    assert len(added) == 1, (path, added)
    return git(repo, "show", "%s:%s" % (added[0], path))


@then(parsers.re(r"i1 has one drafted capability-proposal for thing, its adds naming thing#r4, and i2 has one drafted "
                 r"capability-proposal for thing, its adds naming thing#r5$"))
def each_has_thing(repo, context):
    for initiative, added in (("i1", "thing#r4"), ("i2", "thing#r5")):
        text = thing_of(repo, initiative)
        assert "\nkind: capability-proposal\n" in text and "\nstatus: drafted\n" in text, (text, context["done"].stderr)
        assert listed(text, "adds") == [added], text


@then("the two capability-proposals have different ids")
def different_ids(repo):
    ids = [re.search(r"^id: (.*)$", thing_of(repo, i), re.MULTILINE).group(1) for i in ("i1", "i2")]
    assert ids[0] != ids[1], ids


def listed(text, field):
    got = re.search(r"^%s: \[(.*)\]$" % field, text, re.MULTILINE)
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


def ids_of(text):
    return re.findall(r"\b\w+#r\d+", text)


@given(parsers.re(r"spec/capabilities/thing\.md on the branch i1's integrate round starts from holds (?P<ids>.+)$"))
def spec_holds(repo, ids):
    write(repo, "spec/capabilities/thing.md",
          cap("thing", ["- [r%s] **When** asked, `thing` shall answer." % i.split("#r")[1] for i in ids_of(ids)]))
    commit_all(repo, "thing holds %s" % ids)


@given(parsers.re(r"an initiative (?P<name>i\d) under \.shop/work/, started, whose capability-proposal (?P<proposal>p\d) is "
                  r"(?P<status>\w+)$"))
def started_with_proposal(repo, name, proposal, status):
    base = ".shop/work/%s/" % name
    write(repo, base + "initiative.md", "---\nid: %s\nkind: initiative\nstatus: started\n---\n" % full("initiative", name))
    write(repo, base + proposal + ".md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: %s\nargues: []\n"
          "adds: []\nchanges: []\nremoves: []\ndate: 2026-10-15\n---\n"
          % (full("capability-proposal", proposal), full("initiative", name), status))
    commit_all(repo, "%s is started with %s %s" % (name, proposal, status))


@given(parsers.re(r"(?P<name>i\d) keeps a draft of (?P<capability>\w+) adding (?P<ids>.+?) at (?P<path>\S+)$"))
def keeps_draft(repo, name, capability, ids, path):
    write(repo, path, cap(capability, ["- [r%s] **When** asked, `%s` shall answer." % (i.split("#r")[1], capability)
                                       for i in ids_of(ids)]))
    commit_all(repo, "%s keeps a draft adding %s" % (name, ids))


@then(parsers.re(r"a round of the kind integrate was started for i1, given (?P<ids>\w+#r\d+ and \w+#r\d+)$"))
def integrate_given_ids(repo, context, ids):
    found = rounds(repo, "integrate", "i1")
    assert len(found) == 1, (starts(repo), context["done"].stdout, context["done"].stderr)
    line = next((l for l in found[0]["brief"].splitlines() if l.startswith("Ids drafted elsewhere")), None)
    assert line is not None, found[0]["brief"]
    for one in ids_of(ids):
        assert one in line, (one, line)


@then(parsers.re(r"the integrate round for i1 was not given thing#r1, thing#r2 or thing#r5$"))
def integrate_not_given(repo):
    brief = rounds(repo, "integrate", "i1")[0]["brief"]
    for one in ("thing#r1", "thing#r2", "thing#r5"):
        assert one not in brief, (one, brief)

