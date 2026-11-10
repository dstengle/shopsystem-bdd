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
C2 = _sibling("codified2_world.py", "shop_codified2_world")
ROOT = Path(__file__).resolve().parents[2]
BROKEN = ROOT / "tests" / "scripts" / "fixtures" / "generate" / "broken" / "spec"


def condition(step):
    return step.text.rsplit(" is ", 1)[1]


def edit(path, pattern, replacement):
    path.write_text(re.sub(pattern, replacement, path.read_text(), count=1, flags=re.MULTILINE))


def node_path(step, name):
    return step.repo / step.context["nodes"][name][1]


# An unpairable capability: r1 and r2 name the code `x` of an initiative and of a request, which no unification makes
# one thing; r3 and r4 clash (an L1). `model logic` sets r1 and r2 aside and still finds r3 and r4's L1.
UNPAIRABLE = [("While the initiative `x` is `proposed`, when the person runs `work stop` on a stage, `work run` shall "
               "end the stage."),
              ("While the request `x` is `open`, when the person runs `work stop` on a stage, `work run` shall not "
               "end the stage."),
              "When the person runs `work check`, `work` shall exit successfully.",
              "When the person runs `work check`, `work` shall exit with an error naming `work check`."]


@handler("GivenK_C", "capability")
def capability(step):
    name, word, repo = step.names[0], condition(step), step.repo
    if word == "unpairable":
        H.write(repo, "spec/capabilities/%s.md" % name,
                H.cap(name, ["- [r%d] %s" % (k, line) for k, line in enumerate(UNPAIRABLE, 1)]))
        H.write(repo, "features/%s.feature" % name, H.feature(name, "@r1", "@r2", "@r3", "@r4"))
        H.says(step, "r1", "%s#r1" % name)
        return
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
        H.write(repo, "spec/index.md", H.INDEX + "- **answer** (noun): what `thing` gives back. Not: reply.\n")
        H.write(repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r1] When asked, `thing` shall reply."]))
        H.write(repo, "features/thing.feature", H.feature("thing", "@r1"))
    elif word == "unparsed":
        shutil.copytree(BROKEN, repo / "spec", dirs_exist_ok=True)
        H.write(repo, "spec/capabilities/thing.md", (BROKEN / "capabilities" / "thing.md").read_text().replace(
            "capability/example.org/fixture/thing", H.full("capability", "thing")))
        H.write(repo, "spec/index.md", (BROKEN / "index.md").read_text().replace(
            "bounded-context/example.org/fixture", "bounded-context/" + H.PATH))
    elif word == "withholding":
        withholding(step)
    elif word in C2.LINES:      # a line of grammar 4, in the smallest codified-2 world
        C2.requirement(step, word, H.PATH)
    elif word in FRAMED:
        H.write(repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r1] " + FRAMED[word][0]]))
        H.write(repo, "features/thing.feature", H.feature("thing", "@r1"))
        if FRAMED[word][1]:     # the scenario's term t1 is the verb the line leaves short: the refusal names it so
            H.says(step, "t1", FRAMED[word][1])
        if word == "prepositioned":     # the verb whose preposition the line says before each of its objects
            H.base(repo, step.context)
            index = repo / "spec" / "index.md"
            index.write_text(index.read_text() + "- **subscribe** (verb, action): Frame: agent subscribes to stage.\n")
        if word == "negating":     # the relation the line negates, a row of `## Relations`
            H.base(repo, step.context)
            index = repo / "spec" / "index.md"
            index.write_text(index.read_text() + "\n## Relations\n\n| from | word | to | cardinality |\n"
                             "|---|---|---|---|\n| stage | for | work-item |  |\n")


# A requirement of the fixture glossary for each frame condition, and how its refusal names the verb's term: `write`
# takes an object (agent writes text), `give` a recipient (agent gives thing to thing), and a stage is no text;
# a verb names its subject: "a file is not written" names no agent that writes it.
# An addressed line gives its trigger's verb its object and, after `to`, its recipient.
FRAMED = {"objectless": ("When the person runs `work start`, `work` shall write.", "the verb write takes an object"),
          "recipientless": ("When the person runs `work start`, `work run` shall give a brief.",
                            "the verb give takes a recipient"),
          "mistyped": ("When the person runs `work start`, `work` shall write a stage.",
                       "the verb write takes as its object text or a kind of it"),
          "negating": (("While a stage is not for a work-item, when the person runs `work start`, `work` shall not "
                        "write a file."), None),
          "verbal": (("While a session writes a file and a session does not commit a file, when the person runs "
                      "`work start`, `work` shall commit a file."), None),
          "agentless": ("While a file is not written, when the person runs `work start`, `work` shall write a file.",
                        "the verb write takes a subject"),
          "prepositioned": (("While a session does not subscribe to a stage, when a session subscribes to a stage, "
                             "`work` shall subscribe to a stage."), None),
          "addressed": ("When `work` gives a brief to a stage, `work` shall write a file.", None)}


# feature-file-tools' withholding requirement, `[r1] `shelf` shall not lend a book to a reader.`, which the example data
# wrote: the feature `features generate` writes of its capability must hold its Then, "does not lend the book to the
# reader" (the instances named as the scenario names them), kept for `ThenDoes write` under `holds`.
WITHHOLDING = re.compile(r"^- \[r1\] .*shall not (\S+) an? ([\w-]+) to an? ([\w-]+)\.$", re.MULTILINE)


def withholding(step):
    found = [(p, m) for p in sorted((step.repo / "spec" / "capabilities").glob("*.md"))
             for m in [WITHHOLDING.search(p.read_text())] if m]
    assert len(found) == 1, found
    path, (verb, thing, recipient) = found[0][0], found[0][1].groups()
    # a verb with a recipient: its frame names one after `to`
    assert re.search(r"\*\*%s\*\* \(verb\):.* Frame: .* to \S+\.$" % verb, path.read_text(), re.MULTILINE), verb
    step.context.setdefault("holds", {})["features/%s.feature" % path.stem] = re.compile(
        r"^\s*Then .* does not %s the %s\b.* to the %s\b" % (verb, thing, recipient), re.MULTILINE)


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
    packs = _sibling("design_model_check_handlers_packs.py", "shop_design_model_check_handlers_packs")
    if word in packs.TERM:      # a word a pack the context imports defines too
        return packs.term(step, word)
    text = path.read_text()
    if word == "duplicated":
        path.write_text(text + "- **%s** (noun): a thing again.\n" % name)
    elif word == "selfavoiding":
        path.write_text(text.replace("- **%s** (noun): a thing.\n" % name, "- **%s** (noun): a thing. Not: %s.\n" % (name, name)))
    elif word == "malformed":
        path.write_text(text + "- %s, written with no bold term\n" % name)
        H.says(step, name, "glossary bullet")
    elif word == "frameless":
        path.write_text(text.replace("- **%s** (noun): a thing.\n" % name, "- **%s** (verb): a thing done.\n" % name))
    elif word == "prepositional":     # the preposition between the verb and its object belongs to the verb
        path.write_text(text.replace("- **%s** (noun): a thing.\n" % name,
                                     "- **%s** (verb, action): a stage is followed. Frame: agent %ss to stage.\n" % (name, name)))
    elif word == "misframed":     # a Frame: whose object is no kind: the refusal names the word it could not read
        path.write_text(text.replace("- **%s** (noun): a thing.\n" % name,
                                     "- **%s** (verb, action): a stage is followed. Frame: agent %ss widget.\n" % (name, name)))
        H.says(step, name, '%s, the Frame: does not read at "widget"' % name)
    elif word == "unlabelled":     # the category of plugin 2.x, which names no part of speech
        path.write_text(text.replace("- **%s** (noun): a thing.\n" % name, "- **%s** (kind): a thing.\n" % name))
    elif word == "relational":     # a condition of a stage whose definition names the session
        path.write_text(text.replace("- **%s** (noun): a thing.\n" % name,
                                     "- **%s** (adjective of stage): a stage that the session ends.\n" % name))
    elif word in SENSES:     # a verb's 4.0 entries: its aspect, its frames, its senses
        path.write_text(text.replace("- **%s** (noun): a thing.\n" % name, SENSES[word].replace("V", name)))
        if word in REFUSED:     # the refusal names the term under its rule, which no other rule of the entries gives
            H.says(step, name, "%s  (1)\n    term/%s/%s" % (REFUSED[word], H.PATH, name))


# The verb entries of each verb condition, V its word: an agent's frame and a text's take kinds neither of which is
# under the other; a session is a kind of agent, so a session's frame overlaps an agent's.
SENSES = {"aspectless": "- **V** (verb): an agent marks a text. Frame: agent Vs text.\n",
          "multiframed": "- **V** (verb, action): an agent marks a text. Frame: agent Vs text. Frame: agent Vs text to "
                         "agent.\n",
          "polysemous": ("- **V** (verb, action): an agent marks a text. Frame: agent Vs text.\n"
                         "- **V** (verb, state): a text bears a thing's mark. Frame: text Vs thing.\n"),
          "overlapping": ("- **V** (verb, action): an agent marks a text. Frame: agent Vs text.\n"
                          "- **V** (verb, state): a session bears a text's mark. Frame: session Vs text.\n")}
REFUSED = {"aspectless": "v_t14  a verb's entry says neither state nor action",
           "overlapping": "v_t15  two entries of one verb take, in every slot, the same kind or one kind under the other"}


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
