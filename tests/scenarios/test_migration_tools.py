"""features/migration-tools.feature, bound to scripts/migrate: every scenario of the file, by `scenarios()`.

A Given builds a repository on the old system in `repo` and commits it (`old.before` keeps what each file held); the
When runs `migrate run` once; the Then steps read what it left.
"""
import pathlib
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
    old.write("docs/superpowers/plans/p1.md", "A plan.\n")
    old.write("docs/superpowers/specs/s1.md", "A design note.\n")
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
