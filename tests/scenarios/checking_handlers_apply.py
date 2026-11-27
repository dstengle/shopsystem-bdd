"""Handlers of checking's apply of an item refused for an unresponsive feature generator (r168, b871), each a
`work_queue_world.local` taking only a step of a scenario of g168 (`mine`). The Givens are taken as said; the world is
built at the When as applying_handlers' `build` builds it: readiness_world's codified spec with the item i1 holding its
PASSING line, committed, and the workspace w1 a worktree of it; the workspace given a feature generator of its own
(batches_handlers_generator's stand-in `scripts/features` beside a `scripts/features_generate.py`), committed there,
that sleeps past its time limit, `$SHOPSYSTEM_GENERATE_TIMEOUT` one second. The When applies the item to the
workspace's specification in process of spec_apply and keeps the specification service's reply; the Thens read it
refused, naming the feature generator, and the workspace as it was."""
import sys
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"]


def _module(stem):
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return (found is not None and Path(found.feature.filename).stem == "checking" and "g168" in found.tags)


def given(step):
    """The Givens of g168: what the world builds at the When."""
    if not mine(step):
        return False
    step.context["applied"] = {}


def _generator(tree):
    """The stand-in generator that outlasts its time limit, committed in the workspace."""
    stand_in = _module("batches_handlers_generator")
    scripts = tree / "scripts"
    scripts.mkdir(exist_ok=True)
    (scripts / "features_generate.py").write_text('"""A stand-in of the feature generator."""\n')
    program = stand_in.FEATURES.replace("import argparse\n", "import argparse\n" + stand_in.STALL)
    (scripts / "features").write_text(program)
    (scripts / "features").chmod(0o755)
    W.git(tree, "add", "-A")
    W.git(tree, "commit", "-q", "-m", "the workspace's feature generator")


def applies(step):
    """`the batches service applies the item i1 to the specification s1`: spec_apply's reply, the generator stalled."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    import spec_apply
    tree, item = _module("applying_handlers").build(step)
    _generator(tree)
    step.request.getfixturevalue("monkeypatch").setenv("SHOPSYSTEM_GENERATE_TIMEOUT", "1")
    head = W.git(tree, "rev-parse", "HEAD").strip()
    step.context["applied"] = {"tree": tree, "head": head, "reply": spec_apply.apply(tree, [item])}


def _reply(step):
    reply = step.context["applied"]["reply"]
    assert reply.outcome == "refused", reply
    return reply


def then(step):
    """`the specification service refuses this request`: refused, the workspace as it was (its HEAD, nothing changed);
    `... names the feature generator f1`: an error naming `feature generator:<its program>`."""
    if not mine(step) or "reply" not in step.context.get("applied", {}):
        return False
    reply, w = _reply(step), step.context["applied"]
    if step.term == "refuse":
        assert W.git(w["tree"], "rev-parse", "HEAD").strip() == w["head"]
        assert not W.git(w["tree"], "status", "--porcelain").strip(), W.git(w["tree"], "status")
        return None
    assert step.term == "name", step.text
    names = [n for e in reply.errors for n in e["names"]]
    assert any(n.startswith("feature generator:") and n.endswith("scripts/features") for n in names), names
    return None


for template in ("GivenK", "GivenDoes", "GivenK_A"):
    W.local(template)(given)
W.local("WhenRequests")(applies)
W.local("ThenDoes")(then)


@handler("WhenRequests", "specification.apply")
def untaken(step):
    """The specification service's key of its apply, which `features vocab --check` reads: what is left when the
    local above takes no step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)
