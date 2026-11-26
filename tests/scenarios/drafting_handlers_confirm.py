"""drafting's requirement drafted into an item returned with its id (drafting#r98, b815): in readiness_world's codified
spec, a plain `work line <item> --into work-queue <line>` drafts the world's line into the item, and the Thens read what
`work` printed: the requirement id the item gave the line, as committed, and the line's text beside it. Each a
`local` handler that takes a step of r98's scenario (`mine`) and returns False on any other."""
import importlib.util
import re
import sys
from pathlib import Path


def shared(name, file):
    """A world module loaded once by path, the one the other handler modules load under the same name."""
    if name not in sys.modules:
        spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(file))
        sys.modules[name] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules[name]


W = shared("shop_work_queue_world", "work_queue_world.py")
B = shared("shop_backlog_world", "backlog_world.py")
R = shared("shop_readiness_world", "readiness_world.py")
local = W.local


def mine(step):
    """True when the step is of drafting's scenario of r98."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return sys.modules["vocab"].origin(step.request.node) == "drafting" and found is not None and "r98" in found.tags


@local("GivenK")
@local("GivenDoes")
def given(step):
    """an item, a requirement, its requirement id: what the item and the When make."""
    return None if mine(step) else False


@local("WhenRuns")
@local("WhenRequests")
def draft(step):
    """`work line <item> --into work-queue <line>`, the item shaped with no line of its own."""
    if not mine(step):
        return False
    item = step.names[0] if step.names else "i1"
    step.context["drafted"] = item
    R.codify(step)
    B.write_item(step, item, status="shaped")
    B.run_work(step, "line", B.ident(item), "--into", R.CAPABILITY, R.LINE, **R.NO_INPUT)
    return None


def _printed(step):
    done = step.context["result"]
    assert done.returncode == 0, (done.stdout, done.stderr)
    return done.stdout


@local("ThenPrints")
def returns(step):
    """the drafting service returns the requirement id r2 (the id the committed item gives the line, printed as
    `<capability>#r<n>`) or the requirement r1 (the line's text, printed on the same line as its id)."""
    if not mine(step):
        return False
    out = _printed(step)
    rel = step.context["items"][step.context["drafted"]]
    text = W.git(step.repo, "show", "HEAD:%s" % rel)
    rid = re.search(r"(?m)^- \[(r\d+)\] " + re.escape(R.LINE), text).group(1)
    said = "%s#%s" % (R.CAPABILITY, rid)
    if "requirement id" in step.text:
        assert said in out, out
    else:
        assert "%s %s" % (said, R.LINE) in out, out
    return None
