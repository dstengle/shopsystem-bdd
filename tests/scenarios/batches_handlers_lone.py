"""A model line that restates an event or an actor, laid by `work batch start` (batches r120, r121, b647): over
batches_handlers_restate's world (its Given of a model line: the domain-model fixture's model, vocabulary and
notebook), the item's `### notes model` block restating notes' event `a note is added` with a delivery property, or
its actor `the person` with no kind, and the Thens read `spec/model/notes.md` off the batch's branch after the
command: the element as the line says it, once, and the line the model held gone. Loaded before
batches_handlers_restate, whose handlers of a model line would take these steps."""
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
MODEL = "spec/model/notes.md"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's
LINES = {"event": ("event a note is added: raised by notes.add",
                   "event a note is added: raised by notes.add; delivery: at least once"),
         "actor": ("actor the person kind of agent", "actor the person")}
BLOCK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
         "archives the note, the notes service shall keep the note.\n\n### notes model\n\n```model\n%s\n```")


@four("GivenK", "event", *BOTH)
@four("GivenK", "actor", *BOTH)
def given_lone(step):
    """an event e1 (the fixture's `a note is added`), an actor a1 (its `the person`): which the model line
    restates."""
    step.context["lone"] = step.kind


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the model line m1 that restates the event or the actor: its `### notes model` block."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("item", "model line") or not step.context.get("lone"):
        return False
    B.write_item(step, n1, sections={"Requirements": BLOCK % LINES[step.context["lone"]][1]})


def _lines(step):
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], MODEL)).split("\n")


@four("ThenDoes", "holds", *BOTH)
def model_holds(step):
    """this domain model holds the model line m1: the batch's notes model declares the element once, as the line
    says it."""
    (k1, _), (k2, _) = parts(step)
    if k1 not in ("domain model", "model") or k2 != "model line" or not step.context.get("lone"):
        return False
    old, new = LINES[step.context["lone"]]
    lines = _lines(step)
    head = old.partition(":")[0] if step.context["lone"] == "event" else "actor the person"
    assert [x for x in lines if x.startswith(head)] == [new], lines


@four("ThenDoesNot", "holds", *BOTH)
@four("ThenDoesNot", "hold", *BOTH)
def model_holds_not(step):
    """the domain model d1 does not hold the event e1 or the actor a1: the line the model held is gone."""
    (k1, _), (k2, _) = parts(step)
    if k1 != "domain model" or k2 not in ("event", "actor") or not step.context.get("lone"):
        return False
    old, new = LINES[step.context["lone"]]
    lines = _lines(step)
    assert old not in lines and lines.count(new) == 1, lines


def keeps(step):
    """the batches service keeps the model line m1 or the domain model d1: spec/model/notes.md on the batch's
    branch, holding the line."""
    if parts(step)[1][0] not in ("model line", "domain model") or not step.context.get("lone"):
        return False
    lines = _lines(step)
    if parts(step)[1][0] == "model line":
        assert LINES[step.context["lone"]][1] in lines, lines


for _verb in KEEPS:
    four("ThenDoes", _verb, *BOTH)(keeps)
