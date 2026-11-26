"""Handlers of checking's obtained contract refused for its upstream (r132, r133, b736), each a
`work_queue_world.local` that takes only a step of a scenario of g132 or g133 (`mine`), over checking_handlers_obtain's
world (the domain-model fixture, the stand-in gh, the bounded context `UPSTREAM` obtained from, in no folder of the
shop). r132: the bounded context hosted on the stand-in gh, but no upstream entry under `## Upstreams` of spec/index.md
identifies it (`unlisted`), and no adapter spec names it. r133: the provider's upstream entry kept, every read of its
contents refused by the stand-in gh (`failing`), and no adapter spec names it. The When runs `spec obtain` with its
id; the Thens read the refusal, the id and the reason it names, and that nothing was kept (no provider/, no commit)."""
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
O = next(m for m in list(sys.modules.values()) if (getattr(m, "__file__", None) or "").endswith(
    "/checking_handlers_obtain.py"))     # loaded before this module: the glob is sorted
GROUPS = {"g132", "g133"}


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and bool(GROUPS & set(found.tags))


def given_instance(step):
    if not mine(step) or step.kind not in ("contract", "bounded context", "provider"):
        return False
    O.world(step)["kinds"][step.names[0]] = step.kind


def given_state(step):
    """`this shop does not hold the bounded context b1` (no folder of the shop is its: the fixture's alone), `no
    upstream entry identifies the bounded context b1` (`unlisted`) and `no adapter spec has the provider p1`."""
    if not mine(step) or step.term not in ("holds", "identify", "has"):
        return False
    w = O.world(step)
    if step.term == "holds":
        assert step.template.endswith("Not"), step.text
    elif step.term == "identify":
        assert step.text.startswith("no upstream entry"), step.text
        w["unlisted"] = True
    else:
        assert step.text.startswith("no adapter spec"), step.text
    w["unheld"] = True


def given_health(step):
    """`the health of the provider p1 is `failing``: every read of its repository's contents refused."""
    if not mine(step) or step.attribute != "health":
        return False
    O.world(step)["failing"] = step.values[0].strip("`") == "failing"


def runs(step):
    if not mine(step) or step.term != "`spec obtain`":
        return False
    O.build(step)
    step.context["head"] = W.head(step.repo)
    step.context["result"] = step.run("spec", "obtain", O.UPSTREAM, env=O.env(step, O.world(step)["failing"]))


def then_does(step):
    """`the specification service refuses this request`: exit 1, nothing kept, no commit; `... names the bounded
    context b1` and `... names the provider p1`: its id; `... names `bounded context not an upstream``: the reason."""
    if not mine(step) or "result" not in step.context or step.term not in ("refuse", "name"):
        return False
    done = step.context["result"]
    said = done.stdout + done.stderr
    assert done.returncode == 1, said
    if step.term == "refuse":
        assert not list(step.repo.rglob("provider")), list(step.repo.rglob("provider"))
        assert W.head(step.repo) == step.context["head"], said
        return None
    code = next((n.strip("`") for n in step.nps if n.startswith("`")), None)
    if code is None:
        assert O.world(step)["kinds"].get(step.names[0]) in ("bounded context", "provider"), step.names
    assert (code or O.UPSTREAM) in said, said


W.local("GivenK")(given_instance)
W.local("GivenK_A")(given_health)
W.local("GivenDoes")(given_state)
W.local("GivenDoesNot")(given_state)
W.local("WhenRuns")(runs)
W.local("ThenDoes")(then_does)
