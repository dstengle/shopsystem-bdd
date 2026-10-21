"""features/migration-tools.feature, bound to scripts/migrate: every scenario of the file, by `scenarios()`.

A Given builds a repository on the old system in `repo` and commits it (`old.before` keeps what each file held); the
When runs `migrate run` once; the Then steps read what it left.
"""
import re

from pytest_bdd import given, parsers, scenarios, then, when

from .migration_ledger_steps import *  # noqa: F401,F403  the steps are fixtures pytest-bdd finds by their names here
from .migration_old import CONTEXT, body, front, migrate, said
from .migration_spec_steps import *  # noqa: F401,F403

scenarios("migration-tools.feature")

@given("a repository on the old system with decisions/0001-d0.md, work/i1/w1.md and records/logs/r1.md")
def _(old):
    old.write("decisions/0001-d0.md", "---\nid: design-decision/%s/d0\nsummary: d\nstatus: accepted\n---\nBody d0.\n" % CONTEXT)
    old.write("work/i1/w1.md", "Work one.\n")
    old.write("records/logs/r1.md", "A log.\n")
    old.commit()


@given("a repository on the old system with records/img/a.png, which is not text")
def _(old):
    (old.root / "records/img").mkdir(parents=True)
    (old.root / "records/img/a.png").write_bytes(b"\x89PNG\r\n\x1a\n\xff\xfe\x00")
    old.commit()


@then(".shop/records/img/a.png is records/img/a.png as it was, byte for byte")
def _(old, context):
    assert context["done"].returncode == 0, said(context)
    assert (old.root / ".shop/records/img/a.png").read_bytes() == old.before["records/img/a.png"]


@when(parsers.re(r"the session runs `migrate run --context example.org/acme/shop`( on the repository)?"))
def _(run, old, context):
    migrate(run, old, context)


@then(parsers.parse("{new} has the content {was} had"))
def _(old, new, was):
    assert old.read(new) == old.before[was].decode()


@then("records/img/a.png is gone")
def _(old):
    assert not (old.root / "records/img/a.png").exists()


@then(parsers.re(r"(?P<new>\S+) has the content (?P<was>\S+) had, apart from (?:the id r9 gives it|any id r9 and about r12 give it)$"))
def _(old, new, was):
    """What r9 and r12 give is frontmatter lines at the top: take off the `id:`, `kind:` and `about:` lines they
    added, and a frontmatter of their own when the file had none."""
    text, before = old.read(new), old.before[was].decode()
    if text != before:
        assert text.startswith("---\n"), text
        head, _, rest = text[4:].partition("---\n")
        added = [l for l in head.splitlines() if l.split(":")[0] not in ("id", "kind", "about")]
        kept = ("---\n" + "\n".join(added) + "\n---\n" if added else "") + rest
        assert kept == before, (text, before)


@then("decisions/, work/ and records/ are gone")
def _(old):
    for gone in ("decisions", "work", "records"):
        assert not (old.root / gone).exists(), gone


@then("git status shows each of the three as renamed")
def _(old):
    status = old.git("status", "--porcelain").stdout.splitlines()
    renamed = [l for l in status if l.startswith("R")]
    assert len(renamed) == 3, status


@given("a repository on the old system with docs/superpowers/plans/p1.md, docs/superpowers/specs/s1.md and "
       "docs/superpowers/requests/q1.md")
def _(old):
    old.write("docs/superpowers/plans/p1.md", body("p1"))
    old.write("docs/superpowers/specs/s1.md", "---\ntitle: s1\n---\n" + body("s1"))
    old.write("docs/superpowers/requests/q1.md", body("q1"))
    old.commit()


@given("a repository on the old system with adrs/0001-use-x.md")
def _(old):
    old.write("adrs/0001-use-x.md", body("x"))
    old.commit()


@given("a repository on the old system with records/logs/README.md")
def _(old):
    old.write("records/logs/README.md", body("readme"))
    old.commit()


@then(parsers.parse("{new} has the content {was} had, with no id, no kind and no about"))
def _(old, new, was):
    text = old.read(new)
    assert text == old.before[was].decode()
    assert not text.startswith("---\n"), text


@then(parsers.parse("{new} has the content {was} had, apart from the id r9 and the about r12 give it"))
def _(old, new, was):
    """The id r9 gives a moved record is its frontmatter's `id:` and `kind:` lines, and the about r12 gives it its
    `about:` line after them, in a frontmatter of their own when the file had none."""
    text = old.read(new)
    data, _ = front(old, new)
    given = "id: %s\nkind: %s\nabout: %s\n" % (data["id"], data["kind"], data["about"])
    assert text.startswith("---\n" + given)
    rest = text[len("---\n" + given):]
    kept = rest[len("---\n"):] if rest.startswith("---\n") else "---\n" + rest
    assert kept == old.before[was].decode()


@then("docs/superpowers/plans/, docs/superpowers/specs/ and docs/superpowers/requests/ are gone")
def _(old):
    for gone in ("plans", "specs", "requests"):
        assert not (old.root / "docs/superpowers" / gone).exists(), gone


@then("adrs/ is gone")
def _(old):
    assert not (old.root / "adrs").exists()


@then("git status shows it as renamed")
def _(old):
    status = old.git("status", "--porcelain").stdout.splitlines()
    assert len([l for l in status if l.startswith("R")]) == 1, status


@given("a tracked README.md changed since the last commit")
def _(old):
    old.write("README.md", "As committed.\n")
    old.commit()
    old.untracked("README.md", "Changed since.\n")


@given("an untracked notes/n2.md")
def _(old):
    old.commit()
    old.untracked("notes/n2.md", "Not tracked.\n")


@then(parsers.parse("migrate refuses, naming {named}"))
def _(context, named):
    assert "uncommitted" in said(context) and named in said(context), said(context)


@given("its spec/decisions.md has nothing but the entry `## decision/0007-a`")
def _(old):
    old.write("spec/decisions.md", "## decision/0007-a\nWe do a.\n\ndate: 2025-03-01\nsource: alice\n")
    old.commit()


@then("git status shows .shop/work/i1/w1.md, spec/decisions/0007-a.md and spec/decisions/index.md as staged, and no "
      "file as untracked or changed but not staged")
def _(old):
    status = old.git("status", "--porcelain").stdout.splitlines()
    assert all(l[0] in "ARMD" and l[1] == " " for l in status), status
    for rel in (".shop/work/i1/w1.md", "spec/decisions/0007-a.md", "spec/decisions/index.md"):
        assert any(l[3:].endswith(rel) for l in status), (rel, status)


@then("`model decisions --check` says spec/decisions/index.md is current")
def _(run, old):
    done = run("model", "--root", old.root, "decisions", "--check")
    assert (done.returncode, done.stdout.strip()) == (0, "spec/decisions/index.md is current"), done.stdout + done.stderr


@given("a repository on the old system with work/i1/w1.md, and .shop/work/i1/w1.md already exists")
def _(old):
    old.write("work/i1/w1.md", "Old work.\n")
    old.write(".shop/work/i1/w1.md", "Work already in place.\n")


@given("a repository on the old system with work/i1/w1.md and work/i1/w2.md, and an untracked .shop/work/i1/w2.md")
def _(old):
    old.write("work/i1/w1.md", "Work one.\n")
    old.write("work/i1/w2.md", "Work two.\n")
    old.commit()
    old.untracked(".shop/work/i1/w2.md", "Not tracked.\n")


@given("it has records/archive/plans/p1.md and docs/superpowers/plans/p1.md, which both move to .shop/records/archive/plans/p1.md")
def _(old):
    old.write("records/archive/plans/p1.md", "A plan in records.\n")
    old.write("docs/superpowers/plans/p1.md", "A plan in docs.\n")
    old.commit()


@then(parsers.parse("migrate says it could not {change}"))
def _(context, change):
    assert "could not %s" % change in said(context), said(context)


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
    assert old.git("status", "--porcelain").stdout == old.status
