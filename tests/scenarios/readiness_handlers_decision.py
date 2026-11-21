"""drafting's `work line --retires` of a requirement that enforces a design-decision (r28, b458), read as readiness's
scenarios: "the requirement r2 enforces the design-decision d1" writes spec/decisions/<d1>.md, an accepted decision
whose `enforced_by` names the live requirement the When retires (readiness_world's `LIVE`), and the run names the
decision by its id."""
import sys

W = sys.modules["shop_work_queue_world"]
R = sys.modules.get("shop_readiness_world")
PATH = "ex.com/prod/ctx"


def world():
    global R
    if R is None:
        import importlib.util
        from pathlib import Path
        spec = importlib.util.spec_from_file_location("shop_readiness_world",
                                                      Path(__file__).with_name("readiness_world.py"))
        R = sys.modules["shop_readiness_world"] = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(R)
    return R


@W.local("GivenK", "design-decision")
def given_decision(step):
    """`a design-decision d1`: written once a requirement enforces it."""
    return None if world().mine(step) else False


@W.local("GivenDoes")
def given_enforces(step):
    if not world().mine(step) or step.term != "enforce" or not step.subject.startswith("the requirement "):
        return False
    name = step.names[-1]
    ident = "design-decision/%s/%s" % (PATH, name)
    path = step.repo / "spec" / "decisions" / ("%s.md" % name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("---\nid: %s\nsummary: s\ndate: 2026-11-21\nstatus: accepted\ntier: requirement\n"
                    "enforced_by: [%s]\n---\n\n# %s\n\n## Decision\n\nSo.\n" % (ident, R.LIVE, name))
    step.context.setdefault("says", {})[name] = ident
    return None
