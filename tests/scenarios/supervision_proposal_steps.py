"""supervision's steps about drafting: the formulated capability-proposal `work run` drafts work-items for, and the
work-item it drafts for a kept branch review's findings to fix now."""
import re

from pytest_bdd import given, parsers, then

from .conftest import cap, feature, full
from .supervision_review_steps import FINDINGS
from .supervision_rounds_steps import rounds
from .supervision_world import calls, commit_all, fields, git, item_text, section, write

DIR = ".shop/work/i1"
FIX_NOW = ["Important, w1, thing.py:3: the first thing to fix now", "Important, w1, thing.py:9: the second thing to fix now"]


def named(text):
    """The requirement ids in "thing#r1 and thing#r2"."""
    return re.findall(r"\w+#r\d+(?:-r\d+)?", text or "")


@given(parsers.re(r"i1's capability-proposal p1 is formulated(?:, its adds naming (?P<adds>[^,]+?))?"
                  r"(?:,? and)?(?:,? its changes naming (?P<changes>.+))?$"))
def formulated(repo, adds, changes):
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: formulated\nargues: [thing]\n"
          "adds: [%s]\nchanges: [%s]\nremoves: []\ndate: 2026-10-15\n---\n"
          % (full("capability-proposal", "p1"), full("initiative", "i1"), ", ".join(named(adds)), ", ".join(named(changes))))
    commit_all(repo, "a formulated capability-proposal")


@given(parsers.re(r'features/thing\.feature has the scenario "(?P<a>[^"]+)", tagged @deprecated and (?P<ta>@r\d+), the scenario '
                  r'"(?P<b>[^"]+)", tagged @deprecated and (?P<tb>@r\d+), and the scenario "(?P<c>[^"]+)", tagged (?P<tc>@r\d+)$'))
def thing_feature_deprecated(repo, a, ta, b, tb, c, tc):
    write(repo, "features/thing.feature", feature("thing", ("@deprecated " + ta, a), ("@deprecated " + tb, b), (tc, c)))
    commit_all(repo, "the thing's scenarios")


@given("i1's work-items w1 is green, part of the capability-proposal p1, and w2 is withdrawn")
def green_and_withdrawn(repo):
    write(repo, DIR + "/w1.md", item_text("w1", "green"))
    write(repo, DIR + "/w2.md", item_text("w2", "withdrawn"))
    commit_all(repo, "work-items")


@given("every worker gives DONE, and the branch reviewer's result lists two findings to fix now, both concerning w1, in "
       "its findings.md")
def reviewer_lists(plan):
    plan["default"] = {"status": "DONE"}
    plan["bdd-branch-reviewer"] = [{"questions": FIX_NOW, "notes": {"findings.md": FINDINGS + "\n".join(FIX_NOW) + "\n"}},
                                   {"questions": []}]     # a review of the fix lists nothing


@given("every worker gives DONE, the first branch reviewer's result lists two findings to fix now, both concerning w1, in "
       "its findings.md, and the second lists nothing to fix now")
def reviewers_first_and_second(plan):
    reviewer_lists(plan)


@then("one work-item was drafted in i1 for the two findings, and it is green")
def fix_drafted_green(repo, context):
    found = drafted(repo)
    assert len(found) == 1, (found, context["done"].stderr)
    assert fields(repo / DIR / (found[0][0] + ".md"))["status"] == "green", found


@then("after that work-item turned green a second session of bdd-branch-reviewer was started, before `work run` exited")
def second_review_after_fix(repo, context):
    events = calls(repo)
    review = [i for i, c in enumerate(events) if c["event"] == "start" and c["agent"].endswith("bdd-branch-reviewer")]
    green = [i for i, c in enumerate(events) if c["event"] == "end" and c["agent"].endswith("bdd-task-reviewer")]
    assert len(review) == 2 and green and green[-1] < review[1], (events, context["done"].stderr)


def drafted(repo, base=0):
    """The work-items `work add` drafted in i1: (name, fields, text) of each commit 'work add: i1/<name> drafted'."""
    subjects = git(repo, "log", "--format=%s", "main").split("\n")
    names = [m.group(1) for s in subjects for m in [re.fullmatch(r"work add: i1/(w\d+) drafted", s)] if m]
    return [(n, fields(repo / DIR / (n + ".md")), (repo / DIR / (n + ".md")).read_text()) for n in sorted(names)]


@then("`work add` drafted two work-items in i1, each part of p1: one under thing accepting thing#r1, thing#r2 and "
      "thing#r3, and one under other accepting other#r4")
def two_drafted(repo, context):
    found = sorted((f["under"], f["accepts"], f["part_of"]) for _, f, _ in drafted(repo))
    assert [(u, a) for u, a, _ in found] == [("other", "[other#r4]"), ("thing", "[thing#r1, thing#r2, thing#r3]")], (
        found, context["done"].stderr)
    assert all(p.startswith("capability-proposal/") and p.endswith("/p1") for _, _, p in found), found


@then('the work-item drafted for p1 under thing lists "it used to wait" under its ## Retires, and neither "it used to '
      'answer" nor "it waits"')
def retires_listed(repo, context):
    found = [t for _, f, t in drafted(repo) if f["under"] == "thing"]
    assert len(found) == 1, (found, context["done"].stderr)
    held = section(found[0], "Retires")
    assert '"it used to wait"' in held and "it used to answer" not in held and "it waits" not in held, held


@then("one work-item was drafted in i1 for the two findings, part of p1, naming the kept branch review's findings.md")
def fix_drafted(repo, context):
    found = drafted(repo)
    assert len(found) == 1, (found, context["done"].stderr)
    fix = found[0][1]
    assert fix["part_of"].endswith("/p1"), fix
    assert fix["findings"] == ".shop/work/i1/runs/branch-review/1/findings.md", fix
    assert (repo / fix["findings"]).is_file()


@given(parsers.re(r"the capability thing holds (?P<ids>.+)$"))
def capability_holds(repo, ids):
    write(repo, "spec/capabilities/thing.md",
          cap("thing", ["- [r%s] **When** asked, `thing` shall answer." % n for n in re.findall(r"#r(\d+)", ids)]))
    commit_all(repo, "thing holds %s" % ids)


@given(parsers.re(r'i1\'s capability-proposal (?P<name>p\d) is drafted, its adds naming (?P<adds>\w+#r\d+)(?: and the term '
                  r'"(?P<term>\w+)")?(?:, its changes (?P<changes>\w+#r\d+))?(?: and its removes (?P<removes>\w+#r\d+))?$'))
def drafted_with(repo, name, adds, term, changes, removes):
    listed = lambda *ids: ", ".join(i for i in ids if i)     # noqa: E731
    write(repo, "%s/%s.md" % (DIR, name), "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: drafted\n"
          "argues: [%s]\nadds: [%s]\nchanges: [%s]\nremoves: [%s]\ndate: 2026-10-15\n---\n"
          % (full("capability-proposal", name), full("initiative", "i1"), adds.split("#")[0],
             listed(adds, term and "term/" + term), listed(changes), listed(removes)))
    commit_all(repo, "%s is drafted" % name)


@given(parsers.re(r"i1's capability-proposal p1 is (?P<status>approved|withdrawn|awaiting-answer|merged), its "
                  r"(?P<field>adds|changes) naming (?P<ids>\w+#r\d+)$"))
def proposal_in_status(repo, plan, status, field, ids):
    """`work run` moves a proposal on by its rounds before it runs the suites; so that p1 is still `status` when they
    run, an awaiting-answer p1 has a question unanswered, and an approved p1's formulate round asks a question."""
    other = {"adds": "changes", "changes": "adds"}[field]
    held = "\n## Questions\n\n- Is it right?\n" if status == "awaiting-answer" else ""
    if status == "approved":
        plan["initiative-round"] = {"status": "DONE", "questions": ["Is it right?"]}
    write(repo, DIR + "/p1.md", "---\nid: %s\nkind: capability-proposal\npart_of: %s\nstatus: %s\nargues: [thing]\n"
          "%s: [%s]\n%s: []\nremoves: []\ndate: 2026-10-15\n---\n%s"
          % (full("capability-proposal", "p1"), full("initiative", "i1"), status, field, ids, other, held))
    commit_all(repo, "p1 is %s" % status)


@given(parsers.re(r"p1 was written from the change list of i1's integrate round, whose drafts are kept at (?P<path>\S+)$"))
def written_from_round(repo, path):
    file = repo / DIR / "p1.md"
    head, sep, rest = file.read_text().partition("\n---\n")     # the sentence follows the front matter, as work run writes it
    file.write_text(head + sep + "\n# thing\n\nThe drafts of this proposal are in %s.\n" % path + rest)
    commit_all(repo, "p1 names the drafts it was written from")


@then(parsers.re(r"the (?P<kind>gate|apply) round for p1 was given the path (?P<path>\S+)$"))
def round_given_drafts(repo, context, kind, path):
    found = rounds(repo, kind, "p1")
    assert len(found) == 1, (context["done"].stdout, context["done"].stderr)
    assert "Drafts path: %s\n" % path in found[0]["brief"], found[0]["brief"]


@then(parsers.re(r'the brief of the gate round for p1 asks only for the questions on thing#r4, thing#r2, thing#r3 and the '
                 r'term "ledger"$'))
def gate_names_its_ids(repo, context):
    found = rounds(repo, "gate", "p1")
    assert len(found) == 1, (context["done"].stdout, context["done"].stderr)
    for one in ("thing#r4", "thing#r2", "thing#r3", "term/ledger"):
        assert one in found[0]["brief"], (one, found[0]["brief"])


@then("it asks for no question on thing#r1 or on other#r1")
def gate_names_no_other(repo):
    brief = rounds(repo, "gate", "p1")[0]["brief"]
    assert "thing#r1" not in brief and "other#r1" not in brief, brief
