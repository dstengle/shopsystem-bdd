"""drafting's model line that restates an element and leaves out a member line of it (drafting r70, b647), in a
context with a domain model (tests/scripts/fixtures/domain-model/'s spec: `object note`, its attributes, lifecycle and
relation). Each a `local` handler that takes a step of r70's scenario (`mine`) and returns False on any other: the
model line `object note` with its priority given a third value and its relation repeated, its lifecycle left out,
`work line --into notebook --model` run on the item, and the Thens read the item's model block and the commit that
kept it, and what the run printed of the lifecycle line it leaves out."""
import re
import shutil
import sys
from pathlib import Path

W, B = sys.modules["shop_work_queue_world"], sys.modules["shop_backlog_world"]
local = W.local
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
NEW = "  attributes: text (text); priority: low | high | urgent"
KEPT = "  relations: carries → tag (many)"
LEFT = "lifecycle status: draft → active; active → retired; draft → retired"
MODEL = "object note\n%s\n%s" % (NEW, KEPT)


def mine(step):
    """True when the step is of drafting's scenario of r70."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and "r70" in found.tags


@local("GivenK")
def given_named(step):
    """a model line m1, an element e1 (the fixture's `object note`), a member line m2 (its lifecycle line): the
    fixture's spec."""
    if not mine(step) or step.kind not in ("model line", "element", "member line"):
        return False
    if not step.context.get("restate_spec"):
        shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
        step.context["restate_spec"] = True
    return None


@local("GivenDoes")
def given_restates(step):
    """the model line m1 restates the element e1, the element e1 holds the member line m2: so MODEL and the fixture
    say it."""
    return None if mine(step) and step.term in ("restates", "restate", "holds", "hold") else False


@local("GivenDoesNot")
def given_not_held(step):
    """the model line m1 does not hold the member line m2: MODEL has no lifecycle line."""
    return None if mine(step) and step.term in ("holds", "hold") else False


@local("WhenRuns")
def declare(step):
    """`work line <item> --into notebook --model <lines>` (the request re-keyed by the CLI contract)."""
    options = {code.strip("`") for code, _ in getattr(step, "options", ()) or ()}
    if not mine(step) or "--model" not in options:
        return False
    item = re.search(r"\bthe item (i\d+)", step.text).group(1)
    step.context["declared"] = item
    B.write_item(step, item, status="shaped")
    B.run_work(step, "line", B.ident(item), "--into", "notebook", "--model", MODEL)
    return None


@local("ThenDoes")
def kept(step):
    """the item i1 holds the model line m1 (its notes model block holds MODEL), the drafting service keeps it
    (committed), the drafting service names the member line m2 (the lifecycle line, printed)."""
    if not mine(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    if "member line" in step.text:
        assert LEFT in done.stdout, (step.text, done.stdout)
        return None
    rel = step.context["items"][step.context["declared"]]
    text = (step.repo / rel).read_text()
    assert MODEL in text, (step.text, text)
    if step.term not in ("holds", "hold"):
        assert MODEL in W.git(step.repo, "show", "HEAD:%s" % rel), step.text
        assert not W.git(step.repo, "status", "--porcelain", "--", rel).strip(), step.text
    return None
