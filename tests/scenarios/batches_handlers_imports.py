"""A driven port's imports taken out per item (batches r155, r156, b704): beside readiness_world's codified spec, the
domain-model fixture's model, vocabulary and notebook (the index importing the request pack) and a port area spec/model/
holds already, importing nothing. r155: the port `stock`, the area a1, the fixture's `notes` the supporting area a2;
the item i1's new capability `stock-reserving` and i2's `stock-releasing`, each of `kind: port` in `stock` with a line
saying a note, so the lay of i1 (laid first) makes `stock` import `notes`; `work batch park` of i2, and the Then reads
`stock`'s imports off the batch's branch: `notes` kept, i2's capability gone. r156: the port `registry` and the
supporting area `tracking`; i1's new capability `registry-recording` of `kind: port` in `registry`, its line saying a
parcel (a word of `tracking`), laid with the batch, then taken out of i1 on main before `work batch amend`; the Then
reads `registry`'s imports off the batch's branch and the task's: none, as before the item's lay. The handlers are put
first in their keys' chains, before batches_handlers4's and the other areas' of an item, a capability and an area."""
import re
import shutil
import sys
from pathlib import Path

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
MODEL = "---\nid: model/example.org/fixture/%s\narea: %s\nkind: %s\nimports: []\n---\n\n# %s\n\n## Purpose\n\n%s\n\n```model\n%s\n```\n"
WORDS = "---\nid: vocabulary/example.org/fixture/%s\narea: %s\n---\n\n# The words of %s\n\n## Terms\n\n%s\n"
AREAS = {
    "stock": ("port", "What the notes service needs of the stock it reaches.",
              ("service stock\n  operation reserve(note)  outcomes: done | refused: no stock\n"
               "  operation release(note)  outcomes: done"),
              ("- **reserve** (verb, action) → operation stock.reserve. Forms: reserves, reserved. Frame: <actor> reserves"
               " <note>.\n- **release** (verb, action) → operation stock.release. Forms: releases, released. Frame: "
               "<actor> releases <note>.\n- **the stock service** (proper noun) → service stock.")),
    "tracking": ("supporting", "The parcels the notes service tracks.", "object parcel\n  attributes: label (text)",
                 "- **parcel** (noun) → object parcel. A thing sent. Plural: parcels."),
    "registry": ("port", "What the notes service needs of the registry it reaches.",
                 "service registry\n  operation record(parcel)  outcomes: done | refused: no room",
                 ("- **record** (verb, action) → operation registry.record. Forms: records, recorded. Frame: <actor> "
                  "records <parcel>.\n- **the registry service** (proper noun) → service registry.")),
}
BLOCK = ("### %s\n\nnarrator: the notes service\ngroup: service\npurpose: What the notes service asks of %s.\n"
         "area: %s\nkind: port\n\n#### [g1] %s\n- [r1] When the notes service %s, the %s service shall not refuse the "
         "request.")
BLOCKS = {"reserving": BLOCK % ("stock-reserving", "the stock", "stock", "A note reserved is reserved",
                                "reserves a note", "stock"),
          "releasing": BLOCK % ("stock-releasing", "the stock", "stock", "A note released is released",
                                "releases a note", "stock"),
          "recording": BLOCK % ("registry-recording", "the registry", "registry", "A parcel recorded is recorded",
                                "records a parcel", "registry")}


def first(template, term):
    """`four`, the handler put first in its key's chain."""
    def mark(fn):
        four(template, term, *BOTH)(fn)
        chain = F.CHAINS[(template, term)]
        chain.insert(0, chain.pop())
        return fn
    return mark


def mine(step):
    """r155 or r156, the tag of the step's scenario, else None."""
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return next((t for t in ("r155", "r156") if found is not None and t in found.tags), None)


def _spec(step, areas):
    """Once: the fixture's model, vocabulary and notebook beside the world's codified spec, and `areas` each with its
    model file (importing nothing) and its layer."""
    if step.context.get("port_world"):
        return
    step.context["port_world"] = True
    sys.modules["shop_readiness_world"].codify(step)
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))
    for area in areas:
        kind, purpose, model, words = AREAS[area]
        (spec / "model" / ("%s.md" % area)).write_text(MODEL % (area, area, kind, area.title(), purpose, model))
        (spec / "vocabulary" / ("%s.md" % area)).write_text(WORDS % (area, area, area, words))


@first("GivenK", "area")
def given_area(step):
    """an area a1: `stock`, the port; an area a2: the fixture's `notes`."""
    if mine(step) != "r155":
        return False
    _spec(step, ["stock"])
    names = step.context.setdefault("port_areas", {})
    names[step.names[0]] = "stock" if not names else "notes"


@first("GivenK_A", "area")
def area_kind(step):
    """the kind of the area a1 is `port`: so `stock` is; of the area a2 `supporting`: the notes model says so; the kind
    of `registry` is `port`: `registry` and `tracking` written, and i1 given its line of `registry`."""
    if not mine(step):
        return False
    if mine(step) == "r156":
        _spec(step, ["tracking", "registry"])
        B.write_item(step, "i1", sections={"Requirements": BLOCKS["recording"]})
        return None
    area = step.context["port_areas"][step.names[0]]
    path = step.repo / "spec" / "model" / ("%s.md" % area)
    path.write_text(re.sub(r"(?m)^kind: .*$", "kind: %s" % B.bare(step.values[-1]), path.read_text(), count=1))


@first("GivenK", "capability")
def given_capability(step):
    """a capability c1: the item's new `stock-reserving`."""
    return None if mine(step) == "r155" else False


@first("GivenDoes", "holds")
def holds(step):
    """the item i1 holds the capability c1: its block of `stock-reserving`; the area a1 holds the capability c1: what
    the block's `area:` says; `registry` holds no capability: i1's line taken out on main before the amend."""
    if not mine(step):
        return False
    (k1, n1), _ = parts(step)
    if mine(step) == "r156":
        step.context.setdefault("dropping", set()).add("i1")
    elif k1 == "item":
        B.write_item(step, n1, sections={"Requirements": BLOCKS["reserving"]})
    elif k1 != "area":
        return False


@first("GivenDoes", "import")
def imports(step):
    """the area a1 imports the area a2, `registry` imports `tracking`: what the item's lay makes them import."""
    return None if mine(step) else False


def released(step):
    """Before r155's batch is made: the item i2, `in-batch`, given its block of `stock-releasing`, laid after i1's."""
    if mine(step) == "r155" and "i2" in step.context.get("items", {}):
        B.write_item(step, "i2", status="in-batch", sections={"Requirements": BLOCKS["releasing"]})


T.BEFORE_BATCH.append(released)


def _imports(step, branch, area):
    text = T.git(step, "show", "%s:spec/model/%s.md" % (branch, area))
    found = re.search(r"(?m)^imports: \[(.*)\]$", text)
    return [n.strip() for n in found.group(1).split(",") if n.strip()]


def keeps(step):
    """r155: `stock` on the batch's branch still imports `notes`, which i1's line needs, and i2's capability is gone.
    r156: `registry` on the batch's branch and on the task's imports nothing, as before the item's lay."""
    if not mine(step):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    batch = T.batch_name(step, "b1")
    if mine(step) == "r155":
        assert "notes" in _imports(step, batch, "stock"), _imports(step, batch, "stock")
        assert "stock-releasing" not in T.git(step, "show", "%s:spec/index.md" % batch)
        return None
    for branch in (batch, T.task_row(step, "t1")[1]):
        assert _imports(step, branch, "registry") == [], (branch, _imports(step, branch, "registry"))


for _verb in KEEPS:
    first("ThenDoes", _verb)(keeps)
