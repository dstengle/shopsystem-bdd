"""drafting's requirement reworded in an item and term written into one, each returned (drafting#r103, r106, r107,
b829). Each a `local` handler that takes a step of those scenarios (`mine`) and returns False on any other. Of r106
and r107, readiness_world's codified spec, the item holding the passing line as `work-queue#r5`, reworded by
`work line <item> --reword work-queue#r5` to `R.LINE` (r106, no text given) or, given the `text` parameter the
requirement itself, to the text it holds (r107); of r103, the
domain-model fixture's spec, `work line <item> --into notebook --term <entry>`. The Thens read the item as committed
and what `work` printed: the id and the line, the term, or that nothing changed and the requirement named."""
import re
import shutil
import sys
from pathlib import Path

W, B, R = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_readiness_world"))
local = W.local
TAGS = {"r103", "r106", "r107"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
ENTRY = "- **jotting** (noun) → object note. A note written in haste."
IDENT = "%s#r5" % R.CAPABILITY      # the id readiness_world's item gives the passing line


def _tags(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return TAGS & set(found.tags) if found is not None else set()


def mine(step):
    """True when the step is of drafting's scenarios of r103, r106 and r107."""
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and bool(_tags(step))


@local("GivenK")
@local("GivenDoes")
def given(step):
    """a term, an item, a requirement, its id, the item holding the requirement: what the When writes."""
    return None if mine(step) else False


@local("WhenRuns")
@local("WhenRequests")
def run(step):
    """`work line <item> --into notebook --term <entry>` (r103), or `--reword work-queue#r5` of the item's line to
    another text (r106) or to its own (r107)."""
    if not mine(step):
        return False
    world = step.context["returned"] = {"item": "i1"}
    if _tags(step) == {"r103"}:
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        B.write_item(step, "i1", status="shaped")
        args = ["--into", "notebook", "--term", ENTRY]
    else:
        R.give_lines(step, "i1", R.PASSING)
        B.write_item(step, "i1", status="shaped")
        world["text"] = _text(step)
        args = ["--reword", IDENT, world["text"]]
    world["before"] = (step.repo / step.context["items"]["i1"]).read_text()
    B.run_work(step, "line", B.ident("i1"), *args, **R.NO_INPUT)
    return None


def _text(step):
    """the text the reword is given: the step's `text` parameter, the requirement the item holds (r107), its held
    text; with none (r106), another text."""
    given = dict(step.params).get("text")
    if given is None:
        return R.LINE
    assert given == "the requirement r1", (step.text, given)
    return R.PASSING


def _done(step):
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    return done.stdout


def _committed(step):
    rel = step.context["items"][step.context["returned"]["item"]]
    assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return W.git(step.repo, "show", "HEAD:%s" % rel)


@local("ThenPrints")
def returns(step):
    """returns the term t1 (the entry, printed whole), the requirement id r3 (`work-queue#r5`), the requirement r2
    (its new text, after its id); re-keyed as a write too (requested's `trying`), read the same way."""
    if not mine(step):
        return False
    out, world = _done(step), step.context["returned"]
    if "term" in step.text:
        assert ENTRY in out, out
    elif "requirement id" in step.text:
        assert re.search(r"(?m)\b%s\b" % re.escape(IDENT), out), out
    else:
        assert re.search(r"(?m)%s\b.*%s$" % (re.escape(IDENT), re.escape(world["text"])), out), out
    return None


@local("ThenChangesNothing")
def unchanged(step):
    """changes nothing: a successful exit, no commit made, the item file as it was."""
    if not mine(step):
        return False
    _done(step)
    world = step.context["returned"]
    assert W.git(step.repo, "rev-parse", "HEAD").strip() == step.context["head"], step.text
    assert (step.repo / step.context["items"][world["item"]]).read_text() == world["before"], step.text
    return None


@local("ThenDoes")
def then(step):
    """keeps the requirement r2 and the item i1 holds it: committed under its id, the old text gone; names the
    requirement r1: its id printed; the requirement r2 has the requirement id r3: the committed line's id."""
    if not mine(step):
        return False
    out, world = _done(step), step.context["returned"]
    if step.term == "write":
        return returns(step)
    if step.term in ("name", "names"):
        assert IDENT in out, out
        return None
    text = _committed(step)
    rid = IDENT.split("#")[1]
    assert re.search(r"(?m)^- \[%s\] %s$" % (rid, re.escape(world["text"])), text), (step.text, text)
    assert world["text"] == R.PASSING or R.PASSING not in text, text
    return None
