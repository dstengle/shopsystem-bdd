"""features/migration-tools.feature, bound to scripts/migrate: every scenario of the file, by `scenarios()`.

A Given builds a repository on the old system in `repo` and commits it (`old.before` keeps what each file held); the
When runs `migrate run` once; the Then steps read what it left.
"""
import json
import pathlib
import re
import shutil
import subprocess

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("migration-tools.feature")

CONTEXT = "example.org/acme/shop"


class Old:
    """A repository on the old system: files written, committed, and remembered as they were."""

    def __init__(self, root):
        self.root = root
        self.before = {}
        self.git("init", "-q")

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=self.root,
                              capture_output=True, text=True)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "old system")
        self.before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                       for p in self.root.rglob("*") if p.is_file() and ".git" not in p.relative_to(self.root).parts}

    def read(self, rel):
        return (self.root / rel).read_text()


@pytest.fixture
def old(repo):
    return Old(repo)


@pytest.fixture
def ran(context):
    return context


def migrate(run, old, context, root=None):
    context["done"] = run("migrate", "run", "--context", CONTEXT, cwd=root or old.root)


@given("a repository on the old system with decisions/0001-d0.md, work/i1/w1.md and records/logs/r1.md")
def _(old):
    old.write("decisions/0001-d0.md", "---\nid: design-decision/%s/d0\nsummary: d\nstatus: accepted\n---\nBody d0.\n" % CONTEXT)
    old.write("work/i1/w1.md", "Work one.\n")
    old.write("records/logs/r1.md", "A log.\n")
    old.commit()


@when(parsers.re(r"the session runs `migrate run --context example.org/acme/shop`( on the repository)?"))
def _(run, old, context):
    migrate(run, old, context)


@then(parsers.parse("{new} has the content {was} had"))
def _(old, new, was):
    assert old.read(new) == old.before[was].decode()


@then("decisions/, work/ and records/ are gone")
def _(old):
    for gone in ("decisions", "work", "records"):
        assert not (old.root / gone).exists(), gone


@then("git status shows each of the three as renamed")
def _(old):
    status = old.git("status", "--porcelain").stdout.splitlines()
    renamed = [l for l in status if l.startswith("R")]
    assert len(renamed) == 3, status


@given("a repository on the old system with docs/superpowers/plans/p1.md and docs/superpowers/specs/s1.md")
def _(old):
    # both already carry their ids, so run leaves their content as it was (migration-tools#r9 gives an id only where none is)
    old.write("docs/superpowers/plans/p1.md", "---\nid: initiative-archive/%s/p1\nkind: initiative-archive\n---\nA plan.\n" % CONTEXT)
    old.write("docs/superpowers/specs/s1.md", "---\nid: decision-argument/%s/s1\nkind: decision-argument\n---\nA design note.\n" % CONTEXT)
    old.commit()


@then("docs/superpowers/plans/ and docs/superpowers/specs/ are gone")
def _(old):
    assert not (old.root / "docs/superpowers/plans").exists()
    assert not (old.root / "docs/superpowers/specs").exists()


@then("git status shows each of the two as renamed")
def _(old):
    status = old.git("status", "--porcelain").stdout.splitlines()
    assert len([l for l in status if l.startswith("R")]) == 2, status


def load_model():
    """scripts/model, read by path: its own reading of frontmatter."""
    import importlib.machinery
    import importlib.util
    SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
    loader = importlib.machinery.SourceFileLoader("model_by_path", str(SCRIPTS / "model"))
    spec = importlib.util.spec_from_loader("model_by_path", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def front(old, rel):
    data, body = load_model().frontmatter(old.read(rel))
    return data, body


@given("a repository on the old system whose spec/decisions.md has nothing but the entry `## decision/0007-a`")
def _(old, context):
    context["entry"] = "## decision/0007-a\n"


@given('the entry is dated 2025-03-01, its source is alice, and its first paragraph is "We do a."')
def _(old, context):
    old.write("spec/decisions.md", context["entry"] + "We do a.\n\ndate: 2025-03-01\nsource: alice\n")
    old.commit()


@then("spec/decisions.md is gone")
def _(old):
    assert not (old.root / "spec/decisions.md").exists()


@then('spec/decisions/0007-a.md has the summary "We do a." and a Decision of "We do a."')
def _(old):
    data, body = front(old, "spec/decisions/0007-a.md")
    assert data["summary"] == "We do a."
    assert "\n".join(load_model().section(body, "Decision")).strip() == "We do a."


@then("its status is accepted, its date is 2025-03-01 and its by is alice")
def _(old):
    data, _ = front(old, "spec/decisions/0007-a.md")
    assert (data["status"], data["date"], data["by"]) == ("accepted", "2025-03-01", "alice")


@given("a repository on the old system whose spec/index.md gives no id")
def _(old):
    old.write("spec/index.md", "# shop\n")
    old.commit()


@then(parsers.parse("{rel} gives the id {ident}"))
def _(old, rel, ident):
    data, _ = front(old, rel)
    assert data.get("id") == ident


def capability(old, ident=None, retired="[]", lines=("- [r1] **When** a, `thing` shall a.",)):
    head = "id: %s\n" % ident if ident else ""
    old.write("spec/capabilities/thing.md", "---\n%stitle: thing\nnarrator: a client\ngroup: service\nrests_on: []\nretired: %s\n---\n\n"
              "# thing\n\n## Purpose\nSomething.\n\n## Behaviour\n%s\n\n## Not yet\n- None.\n" % (head, retired, "\n".join(lines)))


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


@given("its spec/decisions.md has the entry `## decision/0007-a`")
def _(old):
    old.write("spec/decisions.md", "## decision/0007-a\nWe do a.\n\ndate: 2025-03-01\nsource: alice\n")


@given("it has docs/superpowers/plans/p1.md, docs/superpowers/specs/s1.md and records/logs/run1-test-log.md")
def _(old):
    old.write("docs/superpowers/plans/p1.md", "A plan.\n")
    old.write("docs/superpowers/specs/s1.md", "A design note.\n")
    old.write("records/logs/run1-test-log.md", "A test log.\n")
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


@given("a capability spec/capabilities/thing.md whose frontmatter rests_on names decision/0007-a")
def _(old):
    capability(old, ident="capability/%s/thing" % CONTEXT)
    text = old.read("spec/capabilities/thing.md").replace("rests_on: []", "rests_on: [decision/0007-a]")
    old.write("spec/capabilities/thing.md", text)
    old.commit()


@then("README.md names .shop/work/i1/w1.md where it named work/i1/w1.md")
def _(old):
    assert old.read("README.md") == old.before["README.md"].decode().replace("work/i1/w1.md", ".shop/work/i1/w1.md")


@then("notes/n1.md has the link `[w1](../.shop/work/i1/w1.md)`")
def _(old):
    assert "[w1](../.shop/work/i1/w1.md)" in old.read("notes/n1.md")


@then("spec/capabilities/thing.md's rests_on names design-decision/example.org/acme/shop/a")
def _(old):
    data, _ = front(old, "spec/capabilities/thing.md")
    assert data["rests_on"] == ["design-decision/%s/a" % CONTEXT]


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


@given("a repository on the old system with work/i1/w1.md, and .shop/work/i1/w1.md already exists")
def _(old):
    old.write("work/i1/w1.md", "Old work.\n")
    old.write(".shop/work/i1/w1.md", "Work already in place.\n")


@given("it has records/archive/plans/p1.md and docs/superpowers/plans/p1.md, which both move to .shop/records/archive/plans/p1.md")
def _(old):
    old.write("records/archive/plans/p1.md", "A plan in records.\n")
    old.write("docs/superpowers/plans/p1.md", "A plan in docs.\n")
    old.commit()


def said(context):
    done = context["done"]
    return done.stdout + done.stderr


@then("migrate says it could not move work/i1/w1.md onto .shop/work/i1/w1.md")
def _(context):
    assert "could not move work/i1/w1.md onto .shop/work/i1/w1.md" in said(context)


@then("it says it could not move both records/archive/plans/p1.md and docs/superpowers/plans/p1.md to .shop/records/archive/plans/p1.md")
def _(context):
    found = re.findall(r"could not move both (\S+) and (\S+) to (\S+)", said(context))
    assert [(set(pair), to) for *pair, to in found] == [({"records/archive/plans/p1.md", "docs/superpowers/plans/p1.md"},
                                                         ".shop/records/archive/plans/p1.md")], said(context)


@then("it exits non-zero")
def _(context):
    assert context["done"].returncode != 0


@then("nothing under the repository has changed")
def _(old):
    now = {p.relative_to(old.root).as_posix(): p.read_bytes()
           for p in old.root.rglob("*") if p.is_file() and ".git" not in p.relative_to(old.root).parts}
    assert now == old.before
    assert old.git("status", "--porcelain").stdout == ""


@given("a repository on the old system with decisions/, work/, records/, docs/superpowers/plans/, docs/superpowers/specs/, "
       "a ledger spec/decisions.md, a capability and a @holding scenario")
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
    # each moved record says what it is about already: migrate gives an id, not an `about` (an open question of the report)
    about = "---\nabout: bounded-context/%s\n---\n" % CONTEXT
    old.write("records/logs/run1-test-log.md", about + "A test log.\n")
    old.write("docs/superpowers/plans/p1.md", about + "A plan.\n")
    old.write("docs/superpowers/specs/s1.md", about + "A design note.\n")
    old.commit()


@given("the session has run `migrate run --context example.org/acme/shop`")
def _(run, old, context):
    migrate(run, old, context)
    assert context["done"].returncode == 0, said(context)


@when("the session runs `model check`")
def _(run, old, context):
    context["checked"] = run("model", "--root", old.root, "check", "--json")


@then("it reports no violation, no unresolved reference and no file problem")
def _(context):
    out = context["checked"]
    report = json.loads(out.stdout)
    assert (out.returncode, report["violations"], report["unresolved"], report["problems"]) == (0, [], [], []), out.stdout


@then("the Behaviour lines of spec/capabilities/thing.md are, in order, [r1], [r5], [r3] and [r6]")
def _(old):
    _, body = front(old, "spec/capabilities/thing.md")
    lines = [l for l in load_model().section(body, "Behaviour") if l.startswith("- ")]
    assert [l.split()[1] for l in lines] == ["[r1]", "[r5]", "[r3]", "[r6]"], lines
