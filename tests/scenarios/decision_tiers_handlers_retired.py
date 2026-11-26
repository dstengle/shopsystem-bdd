"""Handlers of features/decisions.feature's decision that names a retired requirement (g26, r26, b735), each a
`work_queue_world.local` that takes only a step of a scenario of g26 (`mine`), over decision_tiers_handlers' decision
files and design-model-check's base: the requirement r2 is `thing#r1` (design_model_check_handlers'
`given_requirement`), the design-decision d1 written whole (a summary and its Decision section, decision_tiers_handlers'
`decision`), so the decision it enforces names `thing#r1` under `enforced_by`; its requirement id r3 is that
id, and "the requirement r1 retires the requirement id r3" writes the capability `thing` with r1 under `retired:` and
a live line r2 in its place, its feature tagged so. `spec check` then reads a decision whose `enforced_by` names a
retired id."""
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
GROUPS = {"g26"}
FEATURE = ("# generated from spec/capabilities/thing.md by features generate; do not edit\nFeature: thing\n"
           "  Narrator: a client\n\n  @g1 @r2\n  Scenario: it answers 1\n    Given a thing\n    Then it is so\n")


def _tiers():
    """decision_tiers_handlers.py, loaded once under its shared name."""
    if "shop_decision_tiers_handlers" not in sys.modules:
        import importlib.util
        spec = importlib.util.spec_from_file_location("shop_decision_tiers_handlers",
                                                      Path(__file__).with_name("decision_tiers_handlers.py"))
        sys.modules["shop_decision_tiers_handlers"] = module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return sys.modules["shop_decision_tiers_handlers"]


def _handlers():
    return next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith(
        "/design_model_check_handlers.py"))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "decisions" and bool(GROUPS & set(found.tags))


def given_id(step):
    """`a design-decision d1`: written whole, its status set by the Given after it; `a requirement id r3`: the id the
    requirement that has it names, kept by its name."""
    if not mine(step) or step.kind not in ("design-decision", "requirement id"):
        return False
    if step.kind == "design-decision":
        _tiers().decision(step, step.names[0].strip("`"))
        return None
    step.context.setdefault("retired ids", {})[step.names[0]] = None


def given_state(step):
    """`the requirement r2 has the requirement id r3` (the id its name says, `thing#r1`) and `the requirement r1
    retires the requirement id r3` (`thing` written with that id retired and a live r2 in place of it)."""
    if not mine(step) or step.term not in ("has", "retire"):
        return False
    ids = step.context["retired ids"]
    if step.term == "has":
        ids[step.names[-1]] = step.context["says"][step.names[0]]
        return None
    retired = ids[step.names[-1]]
    assert retired == "thing#r1", retired
    H = _handlers()
    H.write(step.repo, "spec/capabilities/thing.md", H.cap("thing", ["- [r2] **When** asked"], retired="[r1]"))
    H.write(step.repo, "features/thing.feature", FEATURE)


W.local("GivenK")(given_id)
W.local("GivenDoes")(given_state)
