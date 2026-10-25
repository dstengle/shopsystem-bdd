"""supervision's steps about drafting: the formulated capability-proposal `work run` drafts work-items for, and the
work-item it drafts for a kept branch review's findings to fix now."""
import re

from pytest_bdd import given, parsers, then

from .conftest import feature, full
from .supervision_review_steps import FINDINGS
from .supervision_world import commit_all, fields, git, item_text, section, write

DIR = ".shop/work/i1"
FIX_NOW = ["Important, w1, thing.py:3: the first thing to fix now", "Important, w1, thing.py:9: the second thing to fix now"]


def named(text):
    """The requirement ids in "thing#r1 and thing#r2"."""
    return re.findall(r"\w+#r\d+", text or "")


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
    plan["bdd-branch-reviewer"] = {"questions": FIX_NOW, "notes": {"findings.md": FINDINGS + "\n".join(FIX_NOW) + "\n"}}


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
