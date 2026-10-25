"""supervision's steps about the retiring of deprecated scenarios: the scenarios a feature file holds with a `Deprecated
for:` line, the work-items of other proposals and initiatives their replacements stand under, and what `work run` drafts
and lists under a work-item's Retires (r73, r123, r124)."""
import re
import subprocess

from pytest_bdd import given, parsers, then

from .conftest import full
from .supervision_proposal_steps import DIR, drafted
from .supervision_world import commit_all, git, log_lines, section, write

SCENARIO = re.compile(r'the scenario "([^"]+)", tagged ([@\w ]+?)(?:, deprecated for "([^"]+)")?(?=,|$)')
FILE = re.compile(r"features/(\w+)\.feature has (.*?)(?=,? and features/|$)")


def add_scenarios(repo, capability, found):
    """Append the scenarios `found` ((title, tags, deprecated-for or None) of each) to features/<capability>.feature."""
    path = repo / "features" / (capability + ".feature")
    text = path.read_text() if path.exists() else "Feature: %s\n  Narrator: a client\n\n" % capability
    for title, tags, target in found:
        text += "  %s\n  Scenario: %s\n" % (" ".join(re.findall(r"@\w+", tags)), title)
        text += "    Deprecated for: %s\n" % target if target else ""
        text += "    Given a thing\n    Then it is so\n\n"
    write(repo, "features/%s.feature" % capability, text)


@given(parsers.re(r"(?P<text>features/\w+\.feature has (?=.*deprecated for ).+)$"))
@given(parsers.re(r"(?P<text>features/\w+\.feature has .+ and features/\w+\.feature has .+)$"))
def scenarios_with_replacements(repo, text):
    for capability, body in FILE.findall(text):
        add_scenarios(repo, capability, SCENARIO.findall(body))
    commit_all(repo, "the scenarios")


def work_item(repo, initiative, name, status, proposal, accepts):
    under = accepts.split("#")[0]
    write(repo, ".shop/work/%s/%s.md" % (initiative, name),
          "---\nid: %s\nkind: work-item\npart_of: %s\nstatus: %s\nunder: %s\naccepts: [%s]\n---\n\n# %s\n"
          % (full("work-item", name), full("capability-proposal", proposal), status, under, accepts, name))


@given(parsers.re(r"i1's work-item w1 is green, part of the capability-proposal p1 and accepting thing#r2, and i1's "
                  r"work-item w2, drafted after w1, is green, part of the capability-proposal p2 and accepting other#r4$"))
def two_green(repo):
    work_item(repo, "i1", "w1", "green", "p1", "thing#r2")
    work_item(repo, "i1", "w2", "green", "p2", "other#r4")
    commit_all(repo, "work-items")


@given("i1's work-item w3 is withdrawn")
def w3_withdrawn(repo):
    work_item(repo, "i1", "w3", "withdrawn", "p1", "thing#r1")
    commit_all(repo, "w3")


@given("i2's work-item w4 is ready, accepting thing#r7")
def w4_ready(repo):
    work_item(repo, "i2", "w4", "ready", "p1", "thing#r7")
    commit_all(repo, "w4")


@given("i1's work-item w1 is green, part of the capability-proposal p1 and accepting thing#r2, and w2 is withdrawn")
def green_and_w2_withdrawn(repo):
    work_item(repo, "i1", "w1", "green", "p1", "thing#r2")
    work_item(repo, "i1", "w2", "withdrawn", "p1", "thing#r1")
    commit_all(repo, "work-items")


@then(parsers.re(r'the work-item drafted for p1 under thing lists "it used to wait" under its ## Retires, and neither '
                 r'"it used to answer", "it waits" nor "it answers"$'))
def retires_listed_by_replacement(repo, context):
    found = [t for _, f, t in drafted(repo) if f["under"] == "thing"]
    assert len(found) == 1, (found, context["done"].stderr)
    held = section(found[0], "Retires")
    assert '"it used to wait"' in held and "it used to answer" not in held and "it waits" not in held and (
        "it answers" not in held), held


@then('one work-item was drafted in i1, part of p2, listing "it used to wait" and "it used to answer" under its '
      '## Retires, and not "it used to close"')
def retire_item_drafted(repo, context):
    found = drafted(repo)
    assert len(found) == 1, (found, context["done"].stderr)
    held = section(found[0][2], "Retires")
    assert found[0][1]["part_of"].endswith("/p2"), found
    assert '"it used to wait"' in held and '"it used to answer"' in held and "it used to close" not in held, held


def retire_commit(repo):
    """The commit that drafted the work-item retiring "it used to wait"."""
    found = [n for n, _, t in drafted(repo) if '"it used to wait"' in section(t, "Retires")]
    assert len(found) == 1, found
    return git(repo, "log", "--format=%H", "--grep", "work add: i1/%s drafted" % found[0], "main").split()[0]


def precedes(repo, first, last):
    return subprocess.run(["git", "merge-base", "--is-ancestor", first, last], cwd=repo).returncode == 0


@then('the work-item retiring "it used to wait" was drafted in i1 before `work run` started the branch review of i1')
def drafted_before_review(repo, context):
    brief = (repo / DIR / "runs/branch-review/1/brief.md").read_text()
    head = re.search(r"^Head: (\w+)$", brief, re.MULTILINE).group(1)
    assert precedes(repo, retire_commit(repo), head), (brief, log_lines(repo), context["done"].stderr)


@then("it was drafted before `work run` ran `measure initiative` on i1")
def drafted_before_measure(repo, context):
    """The measurement file is written after the review's brief, whose Head holds the drafting commit."""
    drafted_before_review(repo, context)
    brief = repo / DIR / "runs/branch-review/1/brief.md"
    found = sorted((repo / ".shop/records/measurements").glob("*-i1.md"))
    assert len(found) == 1 and found[0].stat().st_mtime_ns >= brief.stat().st_mtime_ns, (found, context["done"].stderr)
