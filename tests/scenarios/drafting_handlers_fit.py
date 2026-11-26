"""drafting's term whose part of speech does not fit the element it means refused when written or reworded into an item
(r108, r109, b825). Each a `local` handler that takes a step of those scenarios (`mine`) and returns False on any
other. The world is the domain-model fixture's spec: the term t1 `personal`, an adjective; the element e1 the actor
`the person`, which no adjective fits and no other entry of the notes layer means (so no v_t20 names the term). The
When writes the term with `work line <item> --into notebook --term`, or rewords a term the item holds (`GOOD`, written
first) into it with `--reword-term`; the Thens read the refusal (an error exit, no usage error, the item as it was)
and the term's word in what it printed."""
import re
import shutil
import sys
from pathlib import Path

W, B, R = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_readiness_world"))
local = W.local
TAGS = {"r108", "r109"}
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
WORD = "personal"
MISFIT = "- **personal** (adjective) → actor the person. Of the person."
GOOD = ("jotting", "- **jotting** (noun) → object note.")


def _tags(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return TAGS & set(found.tags) if found is not None else set()


def mine(step):
    """True when the step is of drafting's scenarios of r108 and r109."""
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and bool(_tags(step))


@local("GivenK")
@local("GivenDoes")
@local("GivenDoesNot")
def given(step):
    """a term t1, an element e1, an item i1; the term t1 does not fit the element e1 and means it: the world the When
    writes."""
    return None if mine(step) else False


@local("WhenRuns")
@local("WhenRequests")
def write(step):
    """`work line <item> --into notebook --term <t1>`, or of a reword the good term first and then `--reword-term`."""
    if not mine(step):
        return False
    world = step.context["fit"] = {}
    item = world["item"] = re.search(r"\bthe item (i\d+)", step.text).group(1)
    shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
    B.write_item(step, item, status="shaped")
    if _tags(step) == {"r109"}:
        B.run_work(step, "line", B.ident(item), "--into", "notebook", "--term", GOOD[1], **R.NO_INPUT)
        assert step.context["result"].returncode == 0, step.context["result"].stderr
        args = ["--reword-term", GOOD[0], MISFIT]
    else:
        args = ["--term", MISFIT]
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    B.run_work(step, "line", B.ident(item), "--into", "notebook", *args, **R.NO_INPUT)
    return None


@local("ThenDoes")
def then(step):
    """refuses this request: an error exit that is no usage error, the item as it was; names the term t1: its word."""
    if not mine(step):
        return False
    world, done = step.context["fit"], step.context["result"]
    if step.term in ("refuses", "refuse"):
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        rel = step.context["items"][world["item"]]
        assert (step.repo / rel).read_text() == world["before"], step.text
        return None
    said = done.stdout + done.stderr
    assert re.search(r"(?<![\w-])%s(?![\w-])" % WORD, said), (step.text, said)
    return None
