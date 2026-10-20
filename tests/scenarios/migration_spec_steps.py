"""migration-tools' steps for spec/, features/ and references (r3, r4, r5, r6, r9, r10)."""
import json
import shutil

from pytest_bdd import given, parsers, then, when

from .migration_old import CONTEXT, body, capability, front, load_model, migrate, said

RECORDS = ("docs/superpowers/plans/p1.md", "docs/superpowers/requests/q1.md", "docs/superpowers/specs/s1.md",
           "adrs/0001-use-x.md", "records/logs/run1-test-log.md")


def write_records(old):
    """One record of each kind migrate moves and gives an id, with no id and no about."""
    for rel in RECORDS:
        old.write(rel, body(rel))


@given("a repository on the old system whose spec/index.md gives no id")
def _(old):
    old.write("spec/index.md", "# shop\n")
    old.commit()


@then(parsers.parse("{rel} gives the id {ident}"))
def _(old, rel, ident):
    data, _ = front(old, rel)
    assert data.get("id") == ident


@given("a repository on the old system with a capability spec/capabilities/thing.md whose retired: lists r4")
def _(old, context):
    context["retired"] = "[r4]"


@given("whose Behaviour lines are, in order, one with [r1], one with no id, one with [r3] and one with no id")
def _(old, context):
    capability(old, ident="capability/%s/thing" % CONTEXT, retired=context["retired"],
               lines=("- [r1] **When** a, `thing` shall a.", "- **When** b, `thing` shall b.",
                      "- [r3] **When** c, `thing` shall c.", "- **When** d, `thing` shall d."))
    old.commit()


@given("a repository on the old system with a capability spec/capabilities/thing.md with no id")
def _(old):
    capability(old)


@given("it has docs/superpowers/plans/p1.md, docs/superpowers/requests/q1.md, docs/superpowers/specs/s1.md, "
       "adrs/0001-use-x.md and records/logs/run1-test-log.md")
def _(old):
    write_records(old)
    old.commit()


@given("a repository on the old system with a capability spec/capabilities/thing.md whose id is capability/thing")
def _(old):
    old.write("spec/index.md", "# shop\n")
    capability(old, ident="capability/thing")
    old.commit()


@given("a repository on the old system with work/i1/w1.md")
def _(old):
    old.write("work/i1/w1.md", "Work one.\n")


@given("a tracked README.md that names work/i1/w1.md")
def _(old):
    old.write("README.md", "See work/i1/w1.md for the work.\n")


@given("a tracked notes/n1.md with the Markdown link `[w1](../work/i1/w1.md)`")
def _(old):
    old.write("notes/n1.md", "Read [w1](../work/i1/w1.md) first.\n")


@given(parsers.parse("a capability spec/capabilities/thing.md whose frontmatter rests_on names {ref}"))
def _(old, ref):
    capability(old, ident="capability/%s/thing" % CONTEXT)
    text = old.read("spec/capabilities/thing.md").replace("rests_on: []", "rests_on: [%s]" % ref)
    old.write("spec/capabilities/thing.md", text)
    old.commit()


@then("README.md names .shop/work/i1/w1.md where it named work/i1/w1.md")
def _(old):
    assert old.read("README.md") == old.before["README.md"].decode().replace("work/i1/w1.md", ".shop/work/i1/w1.md")


@then("notes/n1.md has the link `[w1](../.shop/work/i1/w1.md)`")
def _(old):
    assert "[w1](../.shop/work/i1/w1.md)" in old.read("notes/n1.md")


@then(parsers.parse("spec/capabilities/thing.md's rests_on names {ref}"))
def _(old, ref):
    data, _ = front(old, "spec/capabilities/thing.md")
    assert data["rests_on"] == [ref]


@given('a repository on the old system whose features/thing.feature has a scenario "s1" tagged @holding')
def _(old):
    old.write("features/thing.feature", "Feature: thing\n  Narrator: a client\n\n  @holding\n  Scenario: s1\n    Given a thing\n    Then it is so\n")


@given('a test that names "s1" by title')
def _(old):
    old.write("tests/test_thing.py", 'from pytest_bdd import scenario\n\n\n@scenario("thing.feature", "s1")\ndef test_s1():\n    pass\n')
    old.commit()


@given('a copy of that repository on which `features deprecate` has been run for "s1"')
def _(old, context, run):
    copy = old.root.parent / (old.root.name + "-copy")
    shutil.copytree(old.root, copy)
    done = run("features", "deprecate", "s1", "--for-removal", cwd=copy)
    assert done.returncode == 0, done.stdout + done.stderr
    context["copy"] = copy


@then("features/thing.feature and the test are as they are in the copy")
def _(old, context):
    copy = context["copy"]
    held = (copy / "features/thing.feature").read_text()
    assert "@holding" in held
    expected = held.replace(" @holding", "").replace("@holding ", "").replace("@holding\n", "")
    assert "@holding" not in expected
    assert old.read("features/thing.feature") == expected
    assert old.read("tests/test_thing.py") == (copy / "tests/test_thing.py").read_text()


@given("a repository on the old system with decisions/, work/, records/, adrs/, docs/superpowers/plans/, "
       "docs/superpowers/specs/, docs/superpowers/requests/, a ledger spec/decisions.md, a capability and a @holding scenario")
def _(old):
    old.write("spec/index.md", "# shop\n")
    old.write("decisions/0001-d0.md", "---\nid: design-decision/%s/d0\nsummary: d\ndate: 2025-03-01\nstatus: accepted\nby: alice\n---\n\n"
                                       "# d0\n\n## Decision\nWe do d0.\n" % CONTEXT)
    old.write("spec/decisions.md", "## decision/0007-a\nWe do a.\n\ndate: 2025-03-01\nsource: alice\n")
    capability(old, lines=("- **When** asked, `thing` shall answer.",))
    text = old.read("spec/capabilities/thing.md").replace("rests_on: []", "rests_on: [decision/0007-a]")
    old.write("spec/capabilities/thing.md", text)
    old.write("features/thing.feature", "Feature: thing\n  Narrator: a client\n\n  @r1\n  Scenario: it answers\n    Given a thing\n"
                                        "    Then it is so\n\n  @holding\n  Scenario: an old one\n    Given a thing\n    Then it is so\n")
    # work/ is final-form but for its place: an initiative is not transcription (it belongs to the living plan)
    old.write("work/i1/initiative.md", "---\nid: initiative/%s/i1\ntitle: t\nsummary: s\nkind: capability-change\nowner-level: ctx\n"
                                       "status: started\npriority: 1\nsource: []\ndate: 2026-10-15\n---\n" % CONTEXT)
    # records as the old system wrote them: no id, no about
    write_records(old)
    old.commit()


@given("a repository on the old system with a capability spec/capabilities/thing.md whose frontmatter has "
       "formulated_as: features/thing.feature")
def _(old):
    old.write("spec/index.md", "# shop\n")
    capability(old)
    text = old.read("spec/capabilities/thing.md").replace("rests_on: []", "rests_on: []\nformulated_as: features/thing.feature")
    old.write("spec/capabilities/thing.md", text)
    old.commit()


@given("a repository on the old system with a ledger whose entry 0007-a has supersedes: decision/0003-b (for artifacts), "
       "and the entry 0003-b")
def _(old):
    old.write("spec/index.md", "# shop\n")
    old.write("spec/decisions.md", "## decision/0003-b\nWe do b.\n\ndate: 2025-02-01\nsource: bob\n\n## decision/0007-a\n"
                                   "We do a.\n\ndate: 2025-03-01\nsource: alice\nsupersedes: decision/0003-b (for artifacts)\n")
    old.commit()


@given("the session has run `migrate run --context example.org/acme/shop`")
def _(run, old, context):
    migrate(run, old, context)
    assert context["done"].returncode == 0, said(context)


@when("the session runs `model check`")
def _(run, old, context):
    context["checked"] = run("model", "--root", old.root, "check", "--json")


@then("it reports no unresolved reference and no file problem")
def _(context):
    out = context["checked"]
    report = json.loads(out.stdout)
    assert (report["unresolved"], report["problems"]) == ([], []), out.stdout


@then("the Behaviour lines of spec/capabilities/thing.md are, in order, [r1], [r5], [r3] and [r6]")
def _(old):
    _, body = front(old, "spec/capabilities/thing.md")
    lines = [l for l in load_model().section(body, "Behaviour") if l.startswith("- ")]
    assert [l.split()[1] for l in lines] == ["[r1]", "[r5]", "[r3]", "[r6]"], lines


@given("a repository on the old system with docs/superpowers/plans/p1.md, docs/superpowers/requests/q1.md, "
       "docs/superpowers/specs/s1.md, adrs/0001-use-x.md and records/logs/run1-test-log.md, none with an about")
def _(old):
    write_records(old)
    old.write("docs/superpowers/specs/s1.md", "---\ntitle: s1\n---\n" + body("s1"))
    old.commit()


@then(parsers.re(r"(?P<files>\S+(?:, \S+)* and \S+) are each about (?P<ref>\S+)$"))
def _(old, files, ref):
    paths = files.replace(" and ", ", ").split(", ")
    found = [front(old, rel)[0].get("about") for rel in paths]
    assert found == [ref] * len(paths), found
