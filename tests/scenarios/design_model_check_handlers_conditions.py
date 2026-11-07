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
    elif word in FRAMED:
        H.write(repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r1] " + FRAMED[word][0]]))
        H.write(repo, "features/thing.feature", H.feature("thing", "@r1"))
        if FRAMED[word][1]:     # the scenario's term t1 is the verb the line leaves short: the refusal names it so
            H.says(step, "t1", FRAMED[word][1])
        if word == "negating":     # the relation the line negates, a row of `## Relations`
            H.base(repo, step.context)
            index = repo / "spec" / "index.md"
            index.write_text(index.read_text() + "\n## Relations\n\n| from | word | to | cardinality |\n"
                             "|---|---|---|---|\n| stage | for | work-item |  |\n")


# A requirement of the fixture glossary for each frame condition, and how its refusal names the verb's term: `write`
# takes an object (`work` writes file), `give` a recipient (`work run` gives brief to stage).
FRAMED = {"objectless": ("When the person runs `work start`, `work` shall write.", "the verb write takes an object"),
          "recipientless": ("When the person runs `work start`, `work run` shall give a brief.",
                            "the verb give takes a recipient"),
          "negating": (("While a stage is not for a work-item, when the person runs `work start`, `work` shall not "
                        "write a file."), None)}


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
    elif word == "frameless":
        path.write_text(text.replace("- **%s** (kind): a thing.\n" % name, "- **%s** (event): a thing done.\n" % name))
    elif word == "relational":     # a condition of a stage whose definition names the session
        path.write_text(text.replace("- **%s** (kind): a thing.\n" % name,
                                     "- **%s** (condition of stage): a stage that the session ends.\n" % name))


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
    elif word == "closed":
        edit(path, r"^status: .*$", "status: delivered")
    elif word in ("received", "sent"):     # the side of a request (requests)
        _sibling("requests_world.py", "shop_requests_world").sided(path, word)


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
