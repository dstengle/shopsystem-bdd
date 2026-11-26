"""drafting's term whose frame does not end it, or names a slot that refers to nothing, refused when written into an
item (r110, r111, b840). Each a `local` handler that takes a step of those scenarios (`mine`) and returns False on any
other. The world is the domain-model fixture's spec: the term t1 `jot`, a verb meaning notes' operation `add`, its
frame f1 `<actor> jots <note>.` with text after it that starts no field (r110), or `<actor> jots <gadget>.`, its slot
s1 `<gadget>` naming no kind, no actor and no parameter (r111). The When writes the term with `work line <item> --into
notebook --term`; the Thens read the refusal (an error exit, no usage error, the item as it was) and the frame or the
slot in what it printed."""
import re
import shutil
import sys
from pathlib import Path

W, B, R = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_readiness_world"))
local = W.local
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
ENTRY = "- **jot** (verb, action) → operation notes.add. To write a note down. Forms: jots, jotted. Frame: %s"
# of each scenario's tag, the frame the term is given and what the refusal names
CASES = {"r110": ("<actor> jots <note>. Then it is kept by the tester.", "<actor> jots <note>."),
         "r111": ("<actor> jots <gadget>.", "<gadget>")}


def case(step):
    """The scenario's tag among CASES, None on a step of another scenario."""
    if sys.modules["vocab"].origin(step.request.node) != "drafting":
        return None
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return next((t for t in CASES if found is not None and t in found.tags), None)


def mine(step):
    return case(step) is not None


@local("GivenK")
@local("GivenDoes")
@local("GivenDoesNot")
def given(step):
    """a frame f1, a term t1, a slot s1, an item i1; the term t1 has the frame f1, the frame f1 does not end the term
    t1, has the slot s1, the slot s1 refers to no term and no parameter: the world the When writes."""
    return None if mine(step) else False


@local("WhenRuns")
@local("WhenRequests")
def write(step):
    """`work line <item> --into notebook --term <t1>`."""
    if not mine(step):
        return False
    world = step.context["slot"] = {}
    item = world["item"] = re.search(r"\bthe item (i\d+)", step.text).group(1)
    shutil.copytree(FIXTURE, step.repo / "spec", dirs_exist_ok=True)
    B.write_item(step, item, status="shaped")
    world["before"] = (step.repo / step.context["items"][item]).read_text()
    entry = ENTRY % CASES[case(step)][0]
    B.run_work(step, "line", B.ident(item), "--into", "notebook", "--term", entry, **R.NO_INPUT)
    return None


@local("ThenDoes")
def then(step):
    """refuses this request: an error exit that is no usage error, the item as it was; names the frame f1 (as
    written) or the slot s1 (in its angle brackets)."""
    if not mine(step):
        return False
    world, done = step.context["slot"], step.context["result"]
    if step.term in ("refuses", "refuse"):
        assert done.returncode != 0 and "usage:" not in done.stderr, (done.stdout, done.stderr)
        rel = step.context["items"][world["item"]]
        assert (step.repo / rel).read_text() == world["before"], step.text
        return None
    said = done.stdout + done.stderr
    assert "v_t13" in said and CASES[case(step)][1] in said, (step.text, said)
    return None
