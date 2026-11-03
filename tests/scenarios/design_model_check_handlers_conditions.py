"""Handlers of the condition Givens of design-model-check (and work-queue's `out of step`) (`the work-item w1 is parentless`): each changes the repository
so that the rule the condition's Means names fires, and keeps in `says` what the output names the instance by. The
nodes themselves are written by world_nodes.py first; a capability, requirement, scenario or term condition writes
its own files."""
import importlib.util
import re
import shutil
import sys
from pathlib import Path

from vocab import handler


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


# The handlers module is loaded by vocab under another name: its helpers are read from this copy, whose handler
# registrations repeat the same file and line, so no key is claimed twice.
H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
ROOT = Path(__file__).resolve().parents[2]
BROKEN = ROOT / "tests" / "scripts" / "fixtures" / "generate" / "broken" / "spec"


def condition(step):
    return step.text.rsplit(" is ", 1)[1]


def edit(path, pattern, replacement):
    path.write_text(re.sub(pattern, replacement, path.read_text(), count=1, flags=re.MULTILINE))


def node_path(step, name):
    return step.repo / step.context["nodes"][name][1]


@handler("GivenK_C", "capability")
def capability(step):
    name, word, repo = step.names[0], condition(step), step.repo
    lines = {"unnumbered": ["- **When** asked, `%s` shall answer." % name],
             "renumbered": ["- [r1] **When** asked, `%s` shall answer." % name] * 2,
             "reusing": ["- [r1] **When** asked, `%s` shall answer." % name],
             "misnamed": ["- [r1] **When** asked, `%s` shall answer." % name]}[word]
    ident = H.full("capability", "other") if word == "misnamed" else None
    H.write(repo, "spec/capabilities/%s.md" % name, H.cap(name, lines, "[r1]" if word == "reusing" else "[]", ident))
    H.write(repo, "features/%s.feature" % name, H.feature(name, "@r1"))
    H.says(step, name, "%s.md" % name)


@handler("GivenK_C", "capability-proposal")
@handler("GivenK_C", "glossary-proposal")
def proposal(step):
    name, word = step.names[0], condition(step)
    path = node_path(step, name)
    if word == "reaching":
        edit(path, r"^changes: .*$", "changes: [thing#r9]")
    elif word == "unformulated":
        H.write(step.repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r1] **When** asked, `thing` shall answer.",
                                                                         "- [r2] **When** told, `thing` shall nod."]))
        H.write(step.repo, "features/thing.feature", H.feature("thing", "@r1"))
        edit(path, r"^status: .*$", "status: formulated")
        edit(path, r"^adds: .*$", "adds: [thing#r2]")
    elif word == "plural":
        H.write(step.repo, "spec/capabilities/other.md", H.cap("other", ["- [r1] **When** asked, `other` shall answer."]))
        H.write(step.repo, "features/other.feature", H.feature("other", "@r1"))
        edit(path, r"^argues: .*$", "argues: [thing, other]")
    elif word == "dangling":
        edit(path, r"^adds: .*$", "adds: [thing#r9]")
        H.says(step, name, "thing#r9")
    elif word == "termless":
        text = path.read_text()
        path.write_text(re.sub(r"^adds: .*$", "adds: [term/nothing]", text, flags=re.MULTILINE) if "\nadds:" in text
                        else text.replace("\n---\n", "\nadds: [term/nothing]\n---\n", 1))
        H.says(step, name, "term/%s/nothing" % H.PATH)


@handler("GivenK_C", "requirement")
def requirement(step):
    word, repo = condition(step), step.repo
    if word == "untested":
        H.write(repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r1] **When** asked, `thing` shall answer."]))
        H.write(repo, "features/thing.feature", H.feature("thing"))
    elif word == "avoiding":
        H.write(repo, "spec/index.md", H.INDEX + "- **answer** (kind): what `thing` gives back. Not: reply.\n")
        H.write(repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r1] When asked, `thing` shall reply."]))
        H.write(repo, "features/thing.feature", H.feature("thing", "@r1"))
    elif word == "unparsed":
        shutil.copytree(BROKEN, repo / "spec", dirs_exist_ok=True)
        H.write(repo, "spec/capabilities/thing.md", (BROKEN / "capabilities" / "thing.md").read_text().replace(
            "capability/example.org/fixture/thing", H.full("capability", "thing")))
        H.write(repo, "spec/index.md", (BROKEN / "index.md").read_text().replace(
            "bounded-context/example.org/fixture", "bounded-context/" + H.PATH))


@handler("GivenK_C", "scenario")
def scenario(step):
    name, word, repo = step.names[0], condition(step), step.repo
    H.write(repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r1] **When** asked, `thing` shall answer.",
                                                                 "- [r2] **When** told, `thing` shall nod."]))
    tags = ("@r1 @r2", "@r2") if word == "overtagged" else ("@r1", "@r2", "@r9")
    H.write(repo, "features/thing.feature", H.feature("thing", *tags))
    H.says(step, name, "g9" if word == "misreferring" else "@r1")


@handler("GivenK_C", "feature")
def misfiled(step):
    H.write(step.repo, "features/%s.feature" % step.names[0], H.feature(step.names[0], "@r1"))
    H.says(step, step.names[0], "%s.feature" % step.names[0])


@handler("GivenK_C", "term")
def term(step):
    name, word, path = step.names[0], condition(step), step.repo / "spec" / "index.md"
    text = path.read_text()
    if word == "duplicated":
        path.write_text(text + "- **%s** (kind): a thing again.\n" % name)
    elif word == "selfavoiding":
        path.write_text(text.replace("- **%s** (kind): a thing.\n" % name, "- **%s** (kind): a thing. Not: %s.\n" % (name, name)))
    elif word == "malformed":
        path.write_text(text + "- %s, written with no bold term\n" % name)
        H.says(step, name, "glossary bullet")


@handler("GivenK_C", "work-item")
def work_item(step):
    name, word = step.names[0], condition(step)
    path = node_path(step, name)
    if word == "out of step":     # work-queue's: `work` refuses its transition
        step.context.setdefault("out_of_step", set()).add(name)
    elif word == "parentless":
        edit(path, r"^part_of: .*\n", "")
    elif word == "uncommitted":
        edit(path, r"^check: .*\n", "")
    elif word == "misnumbered":
        path.rename(path.with_name("item-1.md"))
        H.says(step, name, "item-1.md")
    elif word == "alien":
        edit(path, r"^part_of: .*$", "part_of: initiative/ex.org/other/ctx/i1")
    elif word == "misreferenced":
        path.write_text(path.read_text().replace("\n---\n", "\naccepts: [thing#x1]\n---\n", 1))
        H.says(step, name, "thing#x1")
    elif word == "unresolving":
        edit(path, r"^under: .*$", "under: nothing")
        H.says(step, name, "nothing")
    elif word == "misidentified":
        edit(path, r"^id: .*$", "id: %s" % H.full("initiative", name))
    elif word == "homeless":
        step.context["homeless"] = True
        H.says(step, name, path.parent.name)


@handler("GivenK_C", "initiative")
def initiative(step):
    name, word = step.names[0], condition(step)
    path = node_path(step, name)
    if word == "crowded":
        path.write_text(H.initiative_text(name, kind="defect"))
        for item in ("w1", "w2"):
            H.write(step.repo, ".shop/work/%s/%s.md" % (name, item), "---\nid: %s\nkind: work-item\npart_of: "
                    "initiative/%s\nstatus: drafted\nunder: thing\ncheck: true\n---\n" % (H.full("work-item", item), name))
    elif word == "unrequested":
        path.write_text(H.initiative_text(name, date="2026-11-01"))
    elif word == "unwaiting":
        path.write_text(H.initiative_text(name, status="done"))
        H.write(step.repo, ".shop/work/requests/q9.md", "---\nid: %s\nkind: request\nasker: internal\nsource: "
                "[%s]\nstatus: open\nturn: upstream\n---\n\n# q9\n\n## Lines\n1. line 1\n\n## Outcomes\n\n"
                "## Resolution\n" % (H.full("request", "q9"), H.full("initiative", name)))
    elif word == "jobbed":
        path.write_text(H.initiative_text(name, kind="job"))


@handler("GivenK_C", "request")
def request(step):
    name, word = step.names[0], condition(step)
    path = node_path(step, name)
    if word == "unanchored":
        path.write_text(path.read_text().replace("\n---\n", "\npart_of: initiative/i1\n---\n", 1))
    elif word == "misresolved":
        edit(path, r"^status: .*$", "status: delivered")
        path.write_text(path.read_text().replace("## Resolution\n", "## Resolution\n1. thing#r9 1.0.0\n"))
    elif word == "misformed":
        path.write_text(path.read_text().replace("## Lines\n", "## Things\n"))


@handler("GivenK_C", "design-decision")
def headless(step):
    H.says(step, step.names[0], "%s.md" % step.names[0])


@handler("GivenK_C", "decisions index")
def stale(step):
    (step.repo / "spec" / "decisions" / "index.md").write_text("# Decisions\n\nnothing here\n")


@handler("GivenK_C", "interpreter")
def interpreter(step):
    step.context["interpreter"] = condition(step)
    if condition(step) == "unfound":
        H.says(step, step.names[0], "pip install clingo")


@handler("GivenK", "requirement group")
def given_group(step):
    """A requirement group of the capability `thing`, which base() writes; a condition rewrites it."""


@handler("GivenK_C", "requirement group")
def group(step):
    word, line = condition(step), "- [r%d] " + H.STATEMENT
    groups = {"compound": ["### [g1] two\n%s\n%s" % (line % 1, line % 2)],
              "repeating": ["### [g1] one\n%s" % (line % 1), "### [g2] two\n%s" % (line % 2)],
              "unexampled": ["### [g1] one\n%s\n\n```given\na work-item w1\n```" % (line % 1)]}[word]
    text = H.cap("thing", ["- [r1] **When** asked, `thing` shall answer."])
    text = text.replace("### [g1] line 1\n- [r1] %s" % H.STATEMENT, "\n\n".join(groups))
    H.write(step.repo, "spec/capabilities/thing.md", text)
    tags = ("@r1 @r2",) if word == "compound" else ("@r1", "@r2") if word == "repeating" else ("@r1",)
    H.write(step.repo, "features/thing.feature", H.feature("thing", *tags))
