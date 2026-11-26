"""A park of an item that restates an element while another item of the batch adds a member line to it (batches
r119, b647): over batches_handlers_restate's world (its Given of a model line: the domain-model fixture's model,
vocabulary and notebook), the item that restates (i2) restating notes' `object note` whole (as laying_handlers_model's
g33 does), laid first, and the other item (i1) adding the member line `relations: pins → tag (many)` to it after; `work
batch park` of i2, and the Thens read `spec/model/notes.md` off the batch's branch: the member line kept, the object's
members as the model held them before the lay, the restatement's gone. Loaded before
batches_handlers_restate, whose handlers of a model line would take these steps."""
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
MODEL = "spec/model/notes.md"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's
HEADER = "object note"
MEMBER = "  relations: pins → tag (many)"
OLD = ("  attributes: text (text); priority: low | high",
       "  lifecycle status: draft → active; active → retired; draft → retired", "  relations: carries → tag (many)")
NEW = "  attributes: text (text); priority: low | high | urgent"
RESTATED = (NEW,) + OLD[1:]
NOTEBOOK = "### notebook\n\n#### [g%d] %s\n- [r%d] %s\n\n### notes model\n\n```model\n%s\n```"
ARCHIVED = "While a note is `active`, when the person archives the note, the notes service shall keep the note."
FILED = "While a note is `draft`, when the person files the note, the notes service shall keep the note."
LINES = {"restates": NOTEBOOK % (10, "An active note archived is kept", 10, ARCHIVED, "\n".join((HEADER,) + RESTATED)),
         "adds": NOTEBOOK % (11, "A draft note filed is kept", 11, FILED, f"{HEADER}\n{MEMBER}")}


@four("GivenK", "member line", *BOTH)
def given_member(step):
    """a member line m2: MEMBER, which the other item's model line adds."""
    step.context["member"] = True


def _first(step, name):
    """The item `name` laid first by batches_world's make_batch (its batch's items in the order of this dict)."""
    items = step.context["given"]["item"]
    step.context["given"]["item"] = dict([(name, items[name])] + [(n, f) for n, f in items.items() if n != name])


@four("GivenDoes", "holds", *BOTH)
@four("GivenDoes", "restates", *BOTH)
@four("GivenDoes", "restate", *BOTH)
def holds(step):
    """the model line m1 holds the member line m2, the model line m3 restates the element e1: so LINES say it; the
    item i1 holds the model line m1 (it adds MEMBER), the item i2 holds the model line m3 (it restates `object note`,
    laid first)."""
    if not step.context.get("member"):
        return False
    (k1, n1), (k2, n2) = parts(step)
    if k1 == "model line":
        step.context.setdefault("adds" if k2 == "member line" else "restates", n1)
        return None
    if (k1, k2) != ("item", "model line"):
        return False
    restates = n2 == step.context.get("restates")
    B.write_item(step, n1, sections={"Requirements": LINES["restates" if restates else "adds"]})
    if restates:
        _first(step, n1)


@four("GivenDoesNot", "holds", *BOTH)
@four("GivenDoesNot", "hold", *BOTH)
def given_not(step):
    """the element e1 does not hold the member line m2: the fixture's `object note` has no MEMBER."""
    return None if step.context.get("member") else False


def _element(step):
    """The member lines of `object note` in the batch's notes model, after the command."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    lines = T.git(step, "show", "%s:%s" % (T.batch_name(step, "b1"), MODEL)).split("\n")
    assert lines.count(HEADER) == 1, lines
    at = lines.index(HEADER)
    end = at + 1
    while end < len(lines) and lines[end].startswith(" "):
        end += 1
    return lines[at + 1:end]


@four("ThenDoes", "holds", *BOTH)
def model_holds(step):
    """this domain model holds the member line m2: the batch's `object note` holds MEMBER once."""
    if not step.context.get("member") or parts(step)[1][0] != "member line":
        return False
    members = _element(step)
    assert members.count(MEMBER) == 1, members


@four("ThenDoesNot", "holds", *BOTH)
@four("ThenDoesNot", "hold", *BOTH)
def model_holds_not(step):
    """the domain model d1 does not hold the model line m3: `object note` is as the model held it before the lay, its
    restated attributes line gone, with MEMBER."""
    if not step.context.get("member") or parts(step)[1][0] != "model line":
        return False
    members = _element(step)
    assert members == list(OLD) + [MEMBER], members


def keeps(step):
    """the batches service keeps the member line m2 or the domain model d1: spec/model/notes.md on the batch's
    branch."""
    if not step.context.get("member") or parts(step)[1][0] not in ("member line", "domain model"):
        return False
    members = _element(step)
    if parts(step)[1][0] == "member line":
        assert MEMBER in members, members


for _verb in KEEPS:
    four("ThenDoes", _verb, *BOTH)(keeps)
