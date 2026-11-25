"""A model line that restates an element, laid by `work batch start` (batches r116, b598): over
batches_handlers_restate's world (its Given of a model line: the domain-model fixture's model, vocabulary and
notebook), the item's `### notes model` block restating notes' `object note` whole, its priority given a third value
and its other members repeated, and the Thens read `spec/model/notes.md` off the batch's branch after the command: the
element as the line says it, once, and the element as the model held it gone."""
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
MODEL = "spec/model/notes.md"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's
HEADER = "object note"
OLD = "  attributes: text (text); priority: low | high"
NEW = "  attributes: text (text); priority: low | high | urgent"
MEMBERS = (NEW, "  lifecycle status: draft → active; active → retired; draft → retired",
           "  relations: carries → tag (many)")
BLOCK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the person "
         "archives the note, the notes service shall keep the note.\n\n### notes model\n\n```model\n%s\n```"
         % "\n".join((HEADER,) + MEMBERS))


@four("GivenK", "element", *BOTH)
def given_element(step):
    """an element e1: the fixture's `object note`, which the model line restates."""
    step.context["element"] = True


@four("GivenDoes", "holds", *BOTH)
def holds(step):
    """the item i1 holds the model line m1 that restates the element e1: its `### notes model` block restating
    `object note`."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) != ("item", "model line") or not step.context.get("element"):
        return False
    B.write_item(step, n1, sections={"Requirements": BLOCK})


def _element(step):
    """The lines of `object note` in the batch's notes model, its header and members."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    lines = T.git(step, "show", "%s:%s" % (branches[0], MODEL)).split("\n")
    at = lines.index(HEADER)
    end = at + 1
    while end < len(lines) and lines[end].startswith(" "):
        end += 1
    assert lines.count(HEADER) == 1, lines
    return lines, lines[at + 1:end]


@four("ThenDoes", "holds", *BOTH)
def model_holds(step):
    """this domain model holds the model line m1: the batch's `object note` has the members the line says, each
    once."""
    (k1, _), (k2, _) = parts(step)
    if k1 not in ("domain model", "model") or k2 != "model line" or not step.context.get("element"):
        return False
    _, members = _element(step)
    assert tuple(members) == MEMBERS, members


@four("ThenDoesNot", "holds", *BOTH)
@four("ThenDoesNot", "hold", *BOTH)
def model_holds_not(step):
    """the domain model d1 does not hold the element e1: the members `object note` had before the lay are not all
    its members, its old attributes line gone."""
    (k1, _), (k2, _) = parts(step)
    if k1 != "domain model" or k2 != "element":
        return False
    lines, _ = _element(step)
    assert OLD not in lines and lines.count(NEW) == 1, lines


def keeps(step):
    """the batches service keeps the model line m1: spec/model/notes.md on the batch's branch says it."""
    if parts(step)[1][0] != "model line" or not step.context.get("element"):
        return False
    _, members = _element(step)
    assert NEW in members, members


for _verb in KEEPS:
    four("ThenDoes", _verb, *BOTH)(keeps)
