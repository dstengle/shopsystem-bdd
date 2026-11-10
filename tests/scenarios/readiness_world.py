"""The scenario repository of features/readiness.feature and features/intake.feature (not a handler module, so the
glob does not load it): the codified spec of tests/scripts/fixtures/generate/repo/ written over the repository's
`spec/` (plan 3, D17), an item given requirement lines, and `work` run with no input. readiness_handlers.py and
intake_handlers.py load it by path as `shop_readiness_world`."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

SPEC = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "generate" / "repo" / "spec"
# A line that passes the bar in the fixture's spec, and one that does not parse there (`frobnicate` is no word of it).
PASSING = ("When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to "
           "`abandoned`.")
FAILING = ("When the person runs `work start` on an initiative that is `proposed`, `work` shall frobnicate the "
           "initiative.")
# A line `features generate` writes with a step no Steps fun words (b46): a negated `exit with an error`, and the step.
UNWORDED = ("When the person runs `work abandon` on an initiative that is `started`, `work` shall not exit with an "
            "error naming the initiative.")
UNWORDED_STEP = "`work` does not [exit_error] the initiative i1"
# A term bullet that brings a lexicon problem the fixture's lexicon does not have (v_t12: a condition whose gloss
# names another kind, the brief, with "the"), and its term.
ILL_TERM = "briefed"
ILL_TERMED = "- **%s** (adjective of initiative): an initiative that the brief names." % ILL_TERM
# What `work` must answer with no person there: no stdin, and a ceiling on the run (D16).
NO_INPUT = {"stdin": subprocess.DEVNULL, "timeout": 120}


def B():
    return sys.modules["shop_backlog_world"]


def codify(step):
    """D17's spec over the repository's `spec/`, once: the fixture less its uncodified `legacy.md`, its index naming
    the context `ex.com/prod/ctx`."""
    if step.context.get("codified"):
        return
    spec = step.repo / "spec"
    shutil.copytree(SPEC, spec, dirs_exist_ok=True)
    (spec / "capabilities" / "legacy.md").unlink()
    index = spec / "index.md"
    index.write_text(re.sub(r"(?m)^id: .*$", "id: bounded-context/ex.com/prod/ctx", index.read_text(), count=1))
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
