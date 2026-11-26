"""Handlers of features/laying.feature (r1-r4, b611), each a `work_queue_world.local` that takes only a step of its
scenarios (`mine`): the requests of the laying service, a driven port, made in process of scripts/laying.py with the
adapter wired in, the in-process one, on readiness_world's codified spec (committed on `main`) with the item i1
holding readiness_world's PASSING line as `work-queue#r5`, or, when a Given says its requirement violates a rule,
batches_handlers_broken's line citing `v_zz`, which no entry of the kept rule catalogue has, so the laid workspace
violates `v_c1` (`VIOLATED`). The workspace w1 is a worktree of the repository beside it on a branch of its own
(`workspace`). The When lays the item there, or lifts it once its lay is committed there (r2), or checks it once it
is laid there (r3, r4), and keeps the laying service's reply, a domain_envelope Response. The
Thens read the reply and the workspace: its capability file holding the line or not, its feature holding a scenario
tagged with the requirement's id. The prepare of a workspace for a batch and a check after it are
laying_handlers_prepare's and laying_handlers_reached's (b758)."""
import sys
from pathlib import Path

from vocab import handler

W = sys.modules["shop_work_queue_world"]
ID = "r5"                       # readiness_world's `block` gives the item's line this id in work-queue
CAP = "spec/capabilities/work-queue.md"
FEATURE = "features/work-queue.feature"
RULES = "grammar/rules.md"
VIOLATED = "v_c1"               # a requirement names a rule the rule catalogue has no entry of
KEEPS = ("keep", "write", "commit", "make")
CITING = "When the person runs `work check`, `work` shall print `v_zz`."


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "laying"


def world(step):
    return step.context.setdefault("laying", {"rules": {}})


def R():
    return sys.modules["shop_readiness_world"]


def given_instance(step):
    if not mine(step) or step.kind not in ("requirement", "item", "workspace", "rule", "scenario"):
        return False
    world(step)


def given_state(step):
    """`the item i1 holds (has) the requirement r1`, `the workspace w1 holds the requirement r1` (r2: laid before the
    When), `the requirement r1 violates the rule r2` (the item's line cites `v_zz`), `no requirement in the item i1
    violates ...` (the passing line)."""
    if not mine(step):
        return False
    w = world(step)
    if step.term == "violate" and not step.text.startswith("no "):
        w["violating"] = True
        w["rules"][step.names[-1]] = VIOLATED
    elif step.term == "holds" and step.text.startswith("the workspace"):
        w["laid"] = True


def given_severity(step):
    if not mine(step) or step.attribute != "severity":
        return False
    assert step.values[0].strip("`") == "error", step.text


def build(step):
    """The repository's codified spec with the item i1's line, committed, and the workspace a worktree of it."""
    import backlog_items
    w = world(step)
    R().codify(step)
    if w.get("violating"):
        catalogue = step.repo / RULES
        catalogue.parent.mkdir(parents=True, exist_ok=True)
        catalogue.write_text("# The rule catalogue\n")
    R().give_lines(step, "i1", CITING if w.get("violating") else R().PASSING)
    W.init(step.repo)
    W.git(step.repo, "add", "-A")
    W.git(step.repo, "commit", "-q", "--allow-empty", "-m", "the world")
    tree = step.request.getfixturevalue("tmp_path_factory").mktemp("laying") / "w1"
    W.git(step.repo, "worktree", "add", "-q", "-b", "workspace", str(tree))
    w["tree"], w["item"] = tree, backlog_items.find(step.repo, "b1")
    return tree, w["item"]


def requests(step):
    """`the batches service lays (lifts, checks) the item i1 in (from) the workspace w1`: the laying service's reply
    to the request, made in process of laying."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    w = world(step)
    tree, item = build(step)
    import laying
    if step.term.endswith(".lift") or w.get("laid"):
        laid = laying.lay(item, tree)
        W.git(tree, "add", "-A")
        W.git(tree, "commit", "-q", "-m", "laid\n\nItem: b1")
        w["laid_reply"] = laid
    elif step.term.endswith(".check"):
        w["laid_reply"] = laying.lay(item, tree)
    w["response"] = getattr(laying, step.term.rsplit(".", 1)[-1])(item, tree)


def _response(step, outcome):
    w = world(step)
    found = w.get("response")
    assert found is not None and found.outcome == outcome, found
    return found


def _text(step, rel):
    path = world(step)["tree"] / rel
    return path.read_text() if path.is_file() else ""


def then_does(step):
    """`the laying service keeps the workspace w1 (w2)`: the lay or the lift done; `the workspace holds the requirement
    r1` (does not): its line in the workspace's capability file under its id; `the laying service keeps the scenario
    s1` and `the scenario s1 refers to the requirement id r2`: the workspace's feature holds a scenario tagged
    `@r5`; `the requirement r1 has the requirement id r2`: the line is the one laid; `fails this request`, `names the
    rule r2`: the check failed naming `v_c1`."""
    if not mine(step) or "laying" not in step.context:
        return False
    w, negated = world(step), step.template.endswith("Not")
    line, term = "- [%s] %s" % (ID, R().PASSING), "keep" if step.term in KEEPS else step.term
    if step.template == "ThenExitsErr":
        term = "fail"
    if term == "keep" and "workspace" in step.text:
        _response(step, "done")
    elif term == "holds" and step.text.startswith("the workspace"):
        assert (line in _text(step, CAP)) != negated, (step.text, _text(step, CAP))
    elif term == "has":
        assert line in _text(step, CAP), _text(step, CAP)
    elif term in ("keep", "refer"):
        _response(step, "done")
        assert "@%s" % ID in _text(step, FEATURE).split(), _text(step, FEATURE)[-400:]
    elif term == "fail":
        _response(step, "failed")
    elif term == "name":
        names = [n for e in _response(step, "failed").errors for n in e["names"]]
        assert "rule:%s" % w["rules"][step.names[-1]] in names, names
    else:
        raise AssertionError("laying_handlers takes no Then %s %s: %s" % (step.template, step.term, step.text))


def then_completes(step):
    """`the laying service completes this request`: the check done."""
    if not mine(step) or "laying" not in step.context:
        return False
    _response(step, "done")


W.local("GivenK")(given_instance)
W.local("GivenK_A")(given_severity)
W.local("GivenDoes")(given_state)
W.local("WhenRequests")(requests)
W.local("ThenDoes")(then_does)
W.local("ThenDoesNot")(then_does)
W.local("ThenExitsErr")(then_does)
W.local("ThenExitsOk")(then_completes)


def untaken(step):
    """The laying service's key of its requests, which `features vocab --check` reads: what is left when the local
    above takes no step."""
    raise AssertionError("no handler of this scenario's feature took the step: %s" % step.text)


for key in (("WhenRequests", "laying.lay"), ("WhenRequests", "laying.lift"), ("WhenRequests", "laying.check"),
            ("WhenRequests", "laying.prepare"), ("ThenDoes", "refer"), ("ThenDoes", "generate")):
    handler(*key)(untaken)
