"""Handlers of checking's check for an item of what the item brings (r164-r167, b871), each a `work_queue_world.local`
tried beside checking_handlers_item's, taking only a step of a scenario of its groups (`mine`).
The Givens are taken as said; the world is written at the When over the domain-model fixture as
checking_handlers_item's `build` writes it: of r164 its item b1 (i1) holding a notebook group of its own (`KEPT`), no rule of
severity error violated; of r165 the item holding readiness_handlers_outcome's BLOCK (the driven
port `stock-port` excluding the refusal of `stock.reserve`, no core line on its completion: `stock.reserve done`
unhandled, v_pb2); of r166 the fixture given readiness_handlers_lifecycle's area `desk` and the item holding its BLOCK
(notebook#r10 setting the status of a note on the request of desk's `stamp`: v_m9); of r167 the fixture's notebook
given a line of its own (`notebook#r20`, a retired note archived set `active`, a transition the lifecycle does not
allow: v_m6, of severity error) and the item holding `ITEM`. The When runs `spec check --item b1` (and of r167 `spec
check` too); the Thens read its exit and what it names, and of r167 that the requirement `spec check` names without the
item is named by no row with it."""
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
GROUPS = {"g164", "g165", "g166", "g167"}
PAST = "notebook#r20"
KEPT = ("#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person archives the "
        "note, the notes service shall keep the note.\n")
LINE = ("\n### [g20] A retired note archived becomes active\n- [r20] While a note is `retired`, when the person "
        "archives the note, the notes service shall set the status of the note to `active`.\n")


def _module(stem):
    return next(m for m in list(sys.modules.values())
                if getattr(m, "__file__", None) and m.__file__.endswith("/%s.py" % stem))


def tags(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return set(found.tags) if found is not None and Path(found.feature.filename).stem == "checking" else set()


def group(step):
    return next(iter(GROUPS & tags(step)), None)


def given(step):
    """The Givens of these groups: what the group's world writes at the When."""
    if group(step) is None:
        return False
    step.context["item brings"] = True


def _world(step, tag):
    """The group's world over the repository (the module's doc)."""
    item = _module("checking_handlers_item")
    text = {"g164": "### notebook\n\n" + KEPT, "g165": _module("readiness_handlers_outcome").BLOCK,
            "g166": _module("readiness_handlers_lifecycle").BLOCK}.get(tag)
    head = item.ITEM.partition("serves:")[0].rsplit("### notebook", 1)[0]
    item.build(step.repo, head + text + "\n" if text else item.ITEM)
    spec = step.repo / "spec"
    if tag == "g166":
        life = _module("readiness_handlers_lifecycle")
        notes = spec / "model" / "notes.md"
        notes.write_text(notes.read_text().replace("imports: []", "imports: [desk]", 1))
        for rel, body in life.DESK.items():
            (spec / rel).write_text(body)
    if tag == "g167":
        notebook = spec / "capabilities" / "notebook.md"
        notebook.write_text(notebook.read_text().rstrip("\n") + "\n" + LINE)


def runs(step):
    """`the person validates this specification with the item i1`: `spec check --item b1` on the group's world."""
    tag = group(step)
    if tag is None or step.term != "`spec check`":
        return False
    _world(step, tag)
    for args in (("features", "generate"), ("spec", "annotate")):
        done = step.run(*args)
        assert done.returncode == 0, done.stdout + done.stderr
    step.context["without item"] = step.run("spec", "check")
    step.context["result"] = step.run("spec", "check", "--item", "b1")


def _done(step):
    done = step.context["result"]
    assert "Traceback" not in done.stderr and "usage:" not in done.stderr, done.stdout + done.stderr
    return done


def completes(step):
    """`the specification service completes this request` (r164): `spec check --item` exits 0."""
    if group(step) is None or "result" not in step.context:
        return False
    done = _done(step)
    assert done.returncode == 0, done.stdout + done.stderr


def fails(step):
    """`the specification service fails this check` (r165, r166): `spec check --item` exits 1."""
    if group(step) is None or "result" not in step.context:
        return False
    done = _done(step)
    assert done.returncode == 1, done.stdout + done.stderr


def names(step):
    """`... names the operation outcome o2` (r165): its output names `stock.reserve done` under v_pb2; `... names the
    core line c1` and `` `v_m9` `` (r166): a v_m9 row, and the core line notebook#r10 the item's lay brings it by."""
    tag = group(step)
    if tag is None or "result" not in step.context or step.term != "name":
        return False
    done, rows = _done(step), _module("checking_handlers_item").rows
    kind = sys.modules["shop_world_four"].parts(step)[-1][0]
    if tag == "g165":
        outcome = _module("readiness_handlers_outcome").OUTCOME
        assert any(outcome in row for row in rows(done.stdout, "v_pb2")), done.stdout + done.stderr
    elif kind == "core line":
        assert _module("readiness_handlers_lifecycle").LINE in done.stdout, done.stdout + done.stderr
    else:
        assert rows(done.stdout, "v_m9"), done.stdout + done.stderr


def not_returned(step):
    """`the specification service does not return the requirement r1` (r167): `spec check` names notebook#r20, and
    `spec check --item b1` names it in no row."""
    if group(step) != "g167" or "result" not in step.context:
        return False
    without, done = step.context["without item"], _done(step)
    assert PAST in without.stdout, without.stdout + without.stderr
    assert PAST not in done.stdout, done.stdout + done.stderr


for template in ("GivenK", "GivenDoes", "GivenDoesNot", "GivenCode", "GivenK_A"):
    W.local(template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(completes)
W.local("ThenExitsErr")(fails)
W.local("ThenDoes")(names)
W.local("ThenPrintsNot")(not_returned)
