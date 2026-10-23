"""migration-tools' steps for what migrate must not touch or take as given: symbolic links, ignored files, line
endings, ids in another form, the top level and a directory that is not a repository (r1, r4, r5, r7, r9, r15)."""
import os
import shutil

from pytest_bdd import given, parsers, then, when

from .migration_old import migrate

NAMES_W1 = "Notes on work/i1/w1.md.\n"


def outside(old, context, text):
    """A file outside the repository, which a tracked symbolic link points to."""
    away = old.root.parent / (old.root.name + "-outside")
    away.mkdir(exist_ok=True)
    target = away / "notes.md"
    target.write_text(text)
    context["outside"] = (target, text)
    return target


@given("a repository on the old system with work/i1/w1.md and a tracked notes/n1.md")
def _(old):
    old.write("work/i1/w1.md", "Work one.\n")
    old.write("notes/n1.md", "Notes.\n")
    old.commit()


@when("the session runs `migrate run --context example.org/acme/shop` from notes/")
def _(run, old, context):
    migrate(run, old, context, root=old.root / "notes")


@then("notes/.shop does not exist")
def _(old):
    assert not (old.root / "notes/.shop").exists()


@given(parsers.parse("a repository on the old system whose spec/index.md gives the id {ident}"))
def _(old, ident):
    old.write("spec/index.md", "---\nid: %s\n---\n# shop\n" % ident)
    old.commit()


@given("a repository on the old system with decisions/0001-x.md whose id is decision/0001-x")
def _(old):
    old.write("decisions/0001-x.md", "---\nid: decision/0001-x\nsummary: x\ndate: 2025-03-01\nstatus: accepted\nby: alice\n"
                                      "---\n\n# x\n\n## Decision\nWe do x.\n")
    old.commit()


@given("a tracked linked.md, a symbolic link to a file outside the repository that names work/i1/w1.md")
def _(old, context):
    os.symlink(outside(old, context, NAMES_W1), old.root / "linked.md")
    context["link"] = os.readlink(old.root / "linked.md")
    old.commit()


@then("the file outside the repository is as it was")
def _(context):
    target, text = context["outside"]
    assert target.read_text() == text


@then("linked.md is the same symbolic link")
def _(old, context):
    assert os.readlink(old.root / "linked.md") == context["link"]


@given("a tracked notes/n1.md with CRLF line endings that names work/i1/w1.md")
def _(old):
    (old.root / "notes").mkdir()
    (old.root / "notes/n1.md").write_bytes(b"First line.\r\nSee work/i1/w1.md.\r\nLast line.\r\n")
    old.commit()


@then("notes/n1.md is as it was, byte for byte, with .shop/work/i1/w1.md for work/i1/w1.md")
def _(old):
    expected = old.before["notes/n1.md"].replace(b"work/i1/w1.md", b".shop/work/i1/w1.md")
    assert (old.root / "notes/n1.md").read_bytes() == expected


@given(parsers.re(r"a repository on the old system with work/i1/w1.md and (?P<there>docs/superpowers/plans/p1\.md, a "
                  r"tracked symbolic link to a file outside the repository|an ignored .+)$"))
def _(old, context, there):
    old.write("work/i1/w1.md", "Work one.\n")
    if there.startswith("docs/"):
        (old.root / "docs/superpowers/plans").mkdir(parents=True)
        os.symlink(outside(old, context, "A plan kept elsewhere.\n"), old.root / "docs/superpowers/plans/p1.md")
        old.commit()
        return
    ignored = there.split()[-1]
    old.write(".gitignore", "/%s\n" % ignored)
    old.commit()
    old.untracked(ignored, "The person's own text, which git does not hold.\n")


@given("a tracked README.md deleted since the last commit")
def _(old):
    old.write("README.md", "As committed.\n")
    old.commit()
    (old.root / "README.md").unlink()
    old.keep()


@given("a directory that is not a git repository, with work/i1/w1.md")
def _(old):
    shutil.rmtree(old.root / ".git")
    old.write("work/i1/w1.md", "Work one.\n")
    old.keep()
