"""The scenario repository of features/readiness.feature and features/intake.feature (not a handler module, so the
glob does not load it): the codified spec of tests/scripts/fixtures/generate/repo/ written over the repository's
`spec/` (plan 3, D17), an item given requirement lines, `work` run with no input, and what `work line` is given in
readiness's scenarios (the pieces, the ids it retires, spec/universal.md). The readiness_handlers*.py and
intake_handlers.py load it by path as `shop_readiness_world`; `mine` tells a step of readiness's feature."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "generate" / "repo" / "spec"
# A line that passes the bar in the fixture's spec, and one that does not parse there (`frobnicate` is no word of it).
PASSING = ("While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set the status of the initiative to "
           "`abandoned`.")
FAILING = ("While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall frobnicate the "
           "initiative.")
# A term bullet that brings a lexicon problem the fixture's lexicon does not have (v_t12: a condition whose gloss
# names another kind, the brief, with "the"), and its term.
ILL_TERM = "briefed"
ILL_TERMED = "- **%s** (adjective of initiative): an initiative that the brief names." % ILL_TERM
# What `work` must answer with no person there: no stdin, and a ceiling on the run (D16).
NO_INPUT = {"stdin": subprocess.DEVNULL, "timeout": 120}


# `work line`'s option: (kind of its piece, a piece that conforms to its form, one that does not), in the fixture's
# spec (kinds initiative, work-item); `--given`'s piece goes into the group g4 the item's lines open.
PIECES = {
    "--relation": ("relation row", "| initiative | holds | work-item | many |", "| initiative | holds | frobnicator |"),
    "--universal": ("universal condition", "`work` shall commit every transition.", None),
    "--upstream": ("upstream entry", "bounded-context/ex.com/prod/up: the upstream, github: ex/up",
                   "the upstream, github: ex/up"),
    "--given": ("given block", "the file `notes.md` holds:\n  The first line.\n  The second line.",
                "an initiative i1 that is `proposed`"),
}
INTO = {"--relation": ["--into", "work-queue"], "--given": ["--into", "work-queue", "--given", "g4"]}
# `work line --retires`: a live requirement of the fixture's work-queue, an id it does not hold, and the new line.
LIVE = "work-queue#r1"
NONEXISTENT = "work-queue#r99"
LINE = ("While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall set the status of the initiative to "
        "`started` and commit the initiative.")
# `work line --universal --retires`: spec/universal.md of one live condition U1 in the old language.
LIVE_U = "universal#U1"
NONEXISTENT_U = "universal#U9"
CONDITION = "`work` shall commit every transition and push it."
UNIVERSAL = ("---\nid: capability/ex.com/prod/ctx/universal\ntitle: Universal conditions\ngroup: guarantees\n"
             "language: codified-1\nretired: []\n---\n\n# Universal conditions\n\n## Behaviour\n\n"
             "- [U1] `work` shall commit every transition.\n")
CAPABILITY = "work-queue"       # the fixture's capability: the capability a scenario recodifies, put back to codified-1


def mine(step):
    """True when the step is of a scenario of features/readiness.feature."""
    node = step.request.node
    scenario = getattr(getattr(node, "obj", None) or getattr(node, "function", None), "__scenario__", None)
    return scenario is not None and Path(scenario.feature.filename).name == "readiness.feature"


def universal(step):
    """The fixture's codified spec, with a spec/universal.md of one live condition U1 in the old language."""
    codify(step)
    (step.repo / "spec" / "universal.md").write_text(UNIVERSAL)


def B():
    return sys.modules["shop_backlog_world"]


def codify(step, old=False):
    """D17's spec over the repository's `spec/`, once: the fixture less its uncodified `legacy.md`, its index naming
    the context `ex.com/prod/ctx`; with `old`, its work-queue in `language: codified-1`, as a recodify finds it."""
    if step.context.get("codified"):
        return
    spec = step.repo / "spec"
    shutil.copytree(SPEC, spec, dirs_exist_ok=True)
    (spec / "capabilities" / "legacy.md").unlink()
    index = spec / "index.md"
    index.write_text(re.sub(r"(?m)^id: .*$", "id: bounded-context/ex.com/prod/ctx", index.read_text(), count=1))
    if old:
        path = spec / "capabilities" / ("%s.md" % CAPABILITY)
        path.write_text(path.read_text().replace("language: codified-2", "language: codified-1"))
    step.context["codified"] = True


def block(title, text, terms=()):
    return "### work-queue\n\n%s#### [g4] %s\n- [r5] %s" % ("".join("%s\n\n" % t for t in terms), title, text)


def give_lines(step, name, text, terms=()):
    """The item `name` given the one requirement line `text`, as `work-queue#r5` in a group `g4`, after the term
    bullets `terms`."""
    codify(step)
    fields = step.context.get("item_fields", {}).get(name, {})
    B().write_item(step, name, sections={"Requirements": block(fields.get("title", "Title of %s" % name), text,
                                                               terms)})


# The world's own request, which a request line of an item is a line of: a peer's, in the upstream's turn.
REQUEST = "q9"
PEER = "bounded-context/ex.com/prod/peer"


def request_text(outcome=None):
    return ("---\nid: request/ex.com/prod/ctx/%s\nkind: request\nasker: %s\npart_of: job-thread/ex.com/prod/t1\n"
            "status: open\nturn: upstream\n---\n\n# A peer's request\n\n## Lines\n1. %s\n\n## Questions\n\n"
            "## Answers\n\n## Outcomes\n%s\n## Resolution\n" % (REQUEST, PEER, PASSING,
                                                               "1. %s\n" % outcome if outcome else ""))


def write_request(step, outcome=None):
    """The world's request `q9`, its one line with the line outcome `outcome` (none when None)."""
    path = step.repo / ".shop" / "requests" / ("%s.md" % REQUEST)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(request_text(outcome))
    step.context.setdefault("nodes", {})[REQUEST] = ("request", path.relative_to(step.repo).as_posix())


def link_request(step, line, item):
    """`the request line r1 is of the item i1`: the world's request q9 written with the line, the item taken in from it
    (`request: q9`), and the line kept as line 1 of q9, which is what `work` names it by."""
    write_request(step, step.context.get("lines", {}).get(line))
    B().write_item(step, item, request=REQUEST)
    step.context.setdefault("line_of", {})[line] = (REQUEST, 1)
    step.context.setdefault("says", {})[line] = "line 1 of request %s" % REQUEST


# The counter-proposal `work outcome rewritten` gives: a line that parses in the fixture's spec.
COUNTER = PASSING
