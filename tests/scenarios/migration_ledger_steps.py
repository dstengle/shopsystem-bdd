"""migration-tools' ledger steps (r2, r11, and r7 for a ledger migrate cannot read): spec/decisions.md as the old
system wrote it, and the decision files migrate leaves."""
import re

from pytest_bdd import given, parsers, then

from .migration_old import CONTEXT, front, load_model

@given("a repository on the old system whose spec/decisions.md has nothing but the entry `## decision/0007-a`")
def _(old, context):
    context["entry"] = "## decision/0007-a\n"
    context["ledger"] = "## decision/0007-a\n%s\ndate: 2025-03-01\nsource: alice\n"


@given('the entry is dated 2025-03-01, its source is alice, and its first paragraph is "We do a."')
def _(old, context):
    old.write("spec/decisions.md", context["entry"] + "We do a.\n\ndate: 2025-03-01\nsource: alice\n")
    old.commit()


@given("a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a`, its first paragraph "
       '"We do a." followed with no blank line by its date 2025-03-01 and its source alice')
def _(old):
    old.write("spec/decisions.md", "## decision/0007-a\nWe do a.\ndate: 2025-03-01\nsource: alice\n")
    old.commit()


@given(parsers.re(r"a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a`, its first "
                  r"paragraph (?P<paragraph>(?:(?! followed with no blank line).)+) and its source (?P<source>.+)$"))
def _(old, paragraph, source):
    old.write("spec/decisions.md", "## decision/0007-a\n%s\n\ndate: 2025-03-01\nsource: %s\n" % (paragraph, source))
    old.commit()


@then(parsers.re(r"model reads spec/decisions/0007-a.md's summary as (?P<paragraph>.+) and its by as (?P<source>.+)$"))
def _(old, paragraph, source):
    data, _ = front(old, "spec/decisions/0007-a.md")
    assert (data["summary"], data["by"]) == (paragraph, source)


@given(parsers.re(r"a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a` and "
                  r"(?P<where>after|before) it (?:the heading `(?P<heading>[^`]+)`|the text \"(?P<text>[^\"]+)\")$"))
def _(old, where, heading, text):
    entry = "## decision/0007-a\nWe do a.\n\ndate: 2025-03-01\nsource: alice\n"
    other = heading + "\nWe do b.\n\ndate: 2025-03-02\nsource: bob\n" if heading else text + "\n"
    old.write("spec/decisions.md", entry + "\n" + other if where == "after" else other + "\n" + entry)
    old.commit()


@given(parsers.re(r"a repository on the old system whose spec/decisions.md has, in order, the entries (?P<entries>.+?)"
                  r"(?:, and (?P<there>decisions/.+|a tracked .+|an untracked .+))?$"))
def _(old, entries, there):
    headings = re.findall(r"`([^`]+)`", entries)
    old.write("spec/decisions.md", "\n".join("%s\nWe do %s.\n\ndate: 2025-03-01\nsource: alice\n"
                                              % (h, re.sub(r"^## decision/(\d+-)?", "", h)) for h in headings))
    if there:
        path = re.search(r"(?:spec/)?decisions/\S+?\.md", there).group(0)
        decision = "---\nid: design-decision/%s/a\nsummary: other\nstatus: accepted\n---\nAnother a.\n" % CONTEXT
        if not there.startswith("an untracked"):
            old.write(path, decision)
    old.commit()
    if there and there.startswith("an untracked"):
        old.untracked(path, decision)


@then(parsers.parse("spec/decisions/ has {files}"))
def _(old, files):
    found = {p.name for p in (old.root / "spec/decisions").glob("*.md") if p.name != "index.md"}
    assert found == set(re.findall(r"[\w-]+\.md", files)), found


@then("spec/decisions.md is gone")
def _(old):
    assert not (old.root / "spec/decisions.md").exists()


@then('spec/decisions/0007-a.md has the summary "We do a." and its Decision has "We do a."')
def _(old):
    data, body = front(old, "spec/decisions/0007-a.md")
    assert data["summary"] == "We do a."
    assert "\n".join(load_model().section(body, "Decision")).strip() == "We do a."


@then("its status is accepted, its date is 2025-03-01 and its by is alice")
def _(old):
    data, _ = front(old, "spec/decisions/0007-a.md")
    assert (data["status"], data["date"], data["by"]) == ("accepted", "2025-03-01", "alice")


@given("its spec/decisions.md has the entry `## decision/0007-a`")
def _(old):
    old.write("spec/decisions.md", "## decision/0007-a\nWe do a.\n\ndate: 2025-03-01\nsource: alice\n")


@given('a repository on the old system whose spec/decisions.md has the entry `## decision/0007-a` with the paragraphs '
       '"We do a." and "Because b."')
def _(old):
    old.write("spec/decisions.md", "## decision/0007-a\nWe do a.\n\nBecause b.\n\ndate: 2025-03-01\nsource: alice\n")
    old.commit()


@then('spec/decisions/0007-a.md has the summary "We do a."')
def _(old):
    data, _ = front(old, "spec/decisions/0007-a.md")
    assert data["summary"] == "We do a."


@then('its Decision has "We do a." and then "Because b."')
def _(old):
    _, body = front(old, "spec/decisions/0007-a.md")
    decision = "\n".join(load_model().section(body, "Decision")).strip()
    assert decision == "We do a.\n\nBecause b.", decision


@then("its date is 2025-03-01 and its by is alice")
def _(old):
    data, _ = front(old, "spec/decisions/0007-a.md")
    assert (data["date"], data["by"]) == ("2025-03-01", "alice")


@given("a repository on the old system whose spec/decisions.md has the title `# Decisions` and a blank line, "
       "then the entry `## decision/0007-a`")
def _(context):
    context["ledger"] = "# Decisions\n\n## decision/0007-a\n%s\ndate: 2025-03-01\nsource: alice\n"


@given('the entry\'s first paragraph is "We do a."')
def _(old, context):
    old.write("spec/decisions.md", context["ledger"] % "We do a.\n")
    old.commit()


@given("a repository on the old system whose spec/decisions.md has the entries `## decision/0003-b` and `## decision/0007-a`")
def _(context):
    context["ledger"] = ["## decision/0003-b\nWe do b.\n\ndate: 2025-02-01\nsource: bob\n",
                         "## decision/0007-a\nWe do a.\n\ndate: 2025-03-01\nsource: alice\n"]


@given("the entry 0007-a has supersedes: decision/0003-b and revisit_when: b comes back")
def _(old, context):
    context["ledger"][1] += "supersedes: decision/0003-b\nrevisit_when: b comes back\n"
    old.write("spec/decisions.md", "\n".join(context["ledger"]))
    old.commit()


@then('spec/decisions/0007-a.md\'s supersedes is design-decision/example.org/acme/shop/b and its revisit_when is "b comes back"')
def _(old):
    data, _ = front(old, "spec/decisions/0007-a.md")
    found = (data.get("supersedes"), data.get("revisit_when"))
    assert found == ("design-decision/%s/b" % CONTEXT, "b comes back"), found


@then(parsers.parse("spec/decisions/{name}.md's status is {status}"))
def _(old, name, status):
    data, _ = front(old, "spec/decisions/%s.md" % name)
    assert data["status"] == status, data["status"]


@given(parsers.parse("the entry 0007-a's source is alice and its supersedes is {value}"))
def _(old, context, value):
    context["ledger"][1] += "supersedes: %s\n" % value
    context["ledger"][1] = context["ledger"][1].replace("source: alice\n", "") + "source: alice\n"
    old.write("spec/decisions.md", "\n".join(context["ledger"]))
    old.commit()


@then(parsers.parse("spec/decisions/0007-a.md's supersedes is {ident} alone"))
def _(old, ident):
    data, _ = front(old, "spec/decisions/0007-a.md")
    assert data.get("supersedes") == ident, data.get("supersedes")


@then(parsers.parse('its by is "{by}"'))
def _(old, by):
    data, _ = front(old, "spec/decisions/0007-a.md")
    assert data["by"] == by, data["by"]
