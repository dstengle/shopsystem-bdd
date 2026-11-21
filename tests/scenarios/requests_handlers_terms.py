"""The term proposals of features/context-requests.feature (b42, context-requests r57-r60), taken as requests'
scenarios: a term proposal a Given makes, written as one vocabulary entry for each term it concerns (`- **<word>**
(noun) → object <word>. ...`), or words that are no entry where a Given says it does not conform to the
vocabulary-entry form; a request that holds it holds it as its next line; `work suggest` run on it, and `work accept`
with it written into its request first; the Thens of a request that holds it and of an item that holds a term. Each is
a local of work_queue_world's table, taken only of a term proposal or a term; any other step goes on."""
import importlib.util
import re
import sys
from pathlib import Path

import request_text
from vocab import handler


def shared(name, file):
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
Q = shared("shop_requests_world", "requests_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
local = W.local
UNFORMED = "shelf: a place for books, with no part of speech and no element"


def handlers():
    return next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith("requests_handlers.py"))


def givens():
    return handlers().givens()


def proposals(step):
    """{term proposal: [the words of the terms it concerns]}, or None for one that does not conform."""
    return step.context.setdefault("proposals", {})


def ours(step, at=0):
    """Whether the step's thing at `at` is a term proposal a Given made, in a requests' scenario."""
    return Q.feature(step) == "requests" and len(step.names) > at and step.names[at] in proposals(step)


def word(step, term):
    """The word of the term `term` (`t2`): `shelf2`, a word of no other entry."""
    return step.context.setdefault("terms", {}).setdefault(term, "shelf%s" % re.sub(r"\D", "", term))


def text_of(step, name):
    """The term proposal `name` as `work suggest` is given it: an entry of each term it concerns (one of its own where
    no Given said which), or the words that do not conform."""
    words = proposals(step)[name]
    if words is None:
        return UNFORMED
    words = words or ["shelf"]
    return " ".join("- **%s** (noun) → object %s. A place the person keeps books on." % (w, w) for w in words)


def said(step):
    for name in proposals(step):
        step.context.setdefault("says", {})[name] = text_of(step, name)


@local("GivenK", "term proposal")
def given_proposal(step):
    if Q.feature(step) != "requests":
        return False
    proposals(step).setdefault(step.names[0], [])
    said(step)


@local("GivenK", "term")
def given_term(step):
    """A term beside a term proposal: its word."""
    if Q.feature(step) != "requests" or not proposals(step):
        return False
    word(step, step.names[0])


@local("GivenK_A", "term proposal")
def given_outcome(step):
    """`the line outcome of the term proposal t1 is `accepted``: its request's line outcome."""
    if not ours(step):
        return False
    step.context.setdefault("lines", {})[step.names[0]] = step.values[0].strip("`")


@local("GivenDoes")
def given_does(step):
    """A request holds a term proposal: its next line; a term proposal concerns a term: an entry of it."""
    if not (ours(step, 1) and step.event == "holds" or ours(step) and step.event in ("concern", "concerns")):
        return False
    if step.event == "holds":
        givens().propose(step, step.names[1], step.names[0])
    else:
        proposals(step)[step.names[0]].append(word(step, step.names[1]))
    said(step)


@local("GivenDoesNot")
def given_does_not(step):
    """A term proposal that does not conform to the vocabulary-entry form: words that are no entry; one that does
    not concern a term: no entry of it."""
    if not ours(step) or step.event not in ("conform", "concern", "concerns"):
        return False
    if step.event == "conform":
        proposals(step)[step.names[0]] = None
    else:
        word(step, step.names[1])
    said(step)


def written(step, request):
    """Each line of the request written as `work accept` takes it: a term proposal it holds as its text, any other as
    a line that parses; each going into the capability work-queue."""
    path = handlers().path_of(step, request)
    text = path.read_text()
    held = sorted((k, name) for name, (r, k) in step.context.get("line_of", {}).items() if r == request)
    for k, name in held or [(1, None)]:
        words = text_of(step, name) if name in proposals(step) else shared("shop_readiness_world", "readiness_world.py").PASSING
        text = text.replace("\n%d. line %d\n" % (k, k), "\n%d. %s\n" % (k, words), 1)
    into = "".join("%d. work-queue\n" % k for k, _ in held or [(1, None)])
    path.write_text(text.replace("## Resolution\n", "## Into\n%s\n## Resolution\n" % into, 1))


@handler("WhenRuns", "`work suggest`")
def work_suggest(step):
    """`work suggest` on the request the When names (one of its own, in the asker's turn, where it names none) with
    the term proposal it names, each read off the step's text."""
    name = re.search(r"\bthe term proposal (\w+)", step.text).group(1)
    found = re.search(r"\bthe request (\w+)", step.text)     # the step's own words: owner() names t1 by a request
    request = found.group(1) if found else "the request of %s" % name
    givens().asker_turn(step, request)
    q = handlers().prepare(step, request)
    handlers().run_work(step, "suggest", q, "--term-proposal", text_of(step, name))


@local("WhenRuns")
def work_accept(step):
    """`work accept` on a request that holds a term proposal, its lines written as `work accept` takes them."""
    if step.term != "`work accept`" or not proposals(step):
        return False
    request = step.names[-1]
    shared("shop_readiness_world", "readiness_world.py").codify(step)
    written(step, request)
    handlers().run_work(step, "accept", handlers().prepare(step, request))


def thens():
    return next(m for m in list(sys.modules.values()) if getattr(m, "__file__", "").endswith(
        "requests_handlers_thens.py"))


@local("ThenDoes")
def then_does(step):
    """The request `work suggest` wrote, the request that holds the term proposal, the item that holds a term."""
    if Q.feature(step) != "requests" or not proposals(step) or not step.names:
        return False
    np = step.nps[-1]
    if step.event == "write" and np.startswith("the request ") and not np.startswith("the request line"):
        path = thens().bound(step, step.names[0])
        assert path.relative_to(step.repo).as_posix() in W.runs(step)[-1]["changed"], step.text
    elif step.event == "holds" and step.names[-1] in proposals(step):
        path = thens().bound(step, step.names[0])
        lines = request_text.entries(path.read_text(), "Lines")
        assert any(e.split(". ", 1)[-1] == text_of(step, step.names[-1]) for e in lines), (step.text, lines)
    elif step.event == "holds" and step.subject.startswith("the item ") and step.names[-1] in step.context.get(
            "terms", {}):
        assert read_terms(step, word(step, step.names[-1])), (step.text, item_text(step))
    else:
        return False


@local("ThenDoesNot")
def then_does_not(step):
    """The item that does not hold a term."""
    if Q.feature(step) != "requests" or not proposals(step) or not step.names or step.event not in ("hold", "holds") \
            or not step.subject.startswith("the item ") or step.names[-1] not in step.context.get("terms", {}):
        return False
    assert "**%s**" % word(step, step.names[-1]) not in item_text(step), (step.text, item_text(step))


def item_text(step):
    return (step.repo / B.bind_written(step, step.names[0])).read_text()


def read_terms(step, term):
    """The entries of the item's blocks for the term that the lexicon reads as term entries (r58, f1)."""
    import backlog_items
    import backlog_section
    import spec_lexicon
    item = backlog_items.parse(item_text(step), "the item")
    blocks = backlog_section.read(item, "the item")
    bullets = [b for block in blocks for b in block.terms] + [b for m in blocks.models for b in m.terms]
    found = [spec_lexicon.entry(b, "the item") for b in bullets]
    return [e for e in found if e and e.term == term]
