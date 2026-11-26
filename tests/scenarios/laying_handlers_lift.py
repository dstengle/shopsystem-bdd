"""Handlers of laying's scenarios of what a lift keeps (r42-r45, b747), moved from batches' (r91, r119, r155, r156,
whose handler modules went with them), `work_queue_world.local`s tried before laying_handlers' own, each taking only a step of a scenario of one of their groups (`mine`). A scenario's world is its group's, built at
the When, so the Givens record nothing: readiness_world's codified spec with the domain-model fixture's model,
vocabulary and notebook beside it, the index importing the request pack (`_spec`), committed on `main`; the workspace
w1 a worktree of it on a branch of its own, each item the group lays laid there in its order (`LAID`) and committed,
then the item the When names lifted with `main`'s head as the batch's base, and the reply kept.

g42: the port `registry` and the supporting area `tracking`; the item i1 as laid holds `registry-recording`, its line
saying a parcel (so its lay makes `registry` import `tracking`), the item lifted as laid, as an amend lifts an item
that holds no capability of `registry` any more; the Then: `registry` kept, importing nothing, as before the lay.
g43: i1's model line repeating notes' `archive(note)` unchanged (the domain model holds it); the Thens: notes' model
declares `archive` once, as before. g44: i2's model line restating `object note` whole, laid first, and i1's adding the
member line `relations: pins → tag (many)` after, i2 lifted; the Thens: `object note` holds the member line once and
its other members as the model held them. g45: the port `stock`, the area a1, importing nothing, and notes, the area a2,
of kind `supporting`; i1's new capability `stock-reserving` and i2's `stock-releasing`, each in `stock` with a line
saying a note, i1 laid first, i2 lifted; the Then: `stock` still imports `notes` and i2's capability is gone."""
import re
import shutil
import sys
from pathlib import Path

L = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers.py"))   # loaded before this, by name
R, W, world, parts = L.R, L.W, L.world, sys.modules["shop_world_four"].parts
B = sys.modules["shop_backlog_world"]
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
NOTES = "spec/model/notes.md"
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
PORT = ("### %s\n\nnarrator: the notes service\ngroup: service\npurpose: What the notes service asks of %s.\n"
        "area: %s\nkind: port\n\n#### [g1] %s\n- [r1] When the notes service %s, the %s service shall not refuse the "
        "request.")
NOTEBOOK = "### notebook\n\n#### [g%d] %s\n- [r%d] %s\n\n### notes model\n\n```model\n%s\n```"
ARCHIVED = "While a note is `active`, when the person archives the note, the notes service shall keep the note."
FILED = "While a note is `draft`, when the person files the note, the notes service shall keep the note."
OPERATION = "  operation archive(note)  outcomes: done"
HEADER, MEMBER = "object note", "  relations: pins → tag (many)"
OLD = ("  attributes: text (text); priority: low | high",
       "  lifecycle status: draft → active; active → retired; draft → retired", "  relations: carries → tag (many)")
RESTATED = ("  attributes: text (text); priority: low | high | urgent",) + OLD[1:]
# Each group's areas, the items' blocks and the order they are laid in.
WORLDS = {
    "g42": (["tracking", "registry"], {"i1": PORT % ("registry-recording", "the registry", "registry",
                                                     "A parcel recorded is recorded", "records a parcel", "registry")}),
    "g43": ([], {"i1": NOTEBOOK % (10, "An active note archived is kept", 10, ARCHIVED, "service notes\n" + OPERATION)}),
    "g44": ([], {"i2": NOTEBOOK % (10, "An active note archived is kept", 10, ARCHIVED, "\n".join((HEADER,) + RESTATED)),
                 "i1": NOTEBOOK % (11, "A draft note filed is kept", 11, FILED, "%s\n%s" % (HEADER, MEMBER))}),
    "g45": (["stock"], {"i1": PORT % ("stock-reserving", "the stock", "stock", "A note reserved is reserved",
                                      "reserves a note", "stock"),
                        "i2": PORT % ("stock-releasing", "the stock", "stock", "A note released is released",
                                      "releases a note", "stock")}),
}


def group(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None or Path(found.feature.filename).stem != "laying":
        return None
    return next((t for t in found.tags if t in WORLDS), None)


def given(step):
    """A Given of these groups: what the group's world builds at the When."""
    if group(step) is None:
        return False
    world(step)


def _spec(step, areas):
    """The fixture's model, vocabulary and notebook beside the codified spec, and `areas` each with its model file
    (importing nothing) and its layer."""
    R().codify(step)
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
    if group(step) == "g45":          # the area a2 of kind `supporting`
        path = step.repo / NOTES
        path.write_text(re.sub(r"(?m)^kind: .*$", "kind: supporting", path.read_text(), count=1))


def requests(step):
    """`the batches service lifts the item i2 from the workspace w1`: the world built, its items laid in w1 and
    committed, the item lifted against `main`'s head; the reply kept."""
    if group(step) is None or step.template != "WhenRequests":
        return False
    import backlog_items
    import laying
    w = world(step)
    areas, blocks = WORLDS[group(step)]
    _spec(step, areas)
    for name, block in blocks.items():
        B.write_item(step, name, sections={"Requirements": block})
    W.init(step.repo)
    W.git(step.repo, "add", "-A")
    W.git(step.repo, "commit", "-q", "--allow-empty", "-m", "the world")
    base = W.git(step.repo, "rev-parse", "HEAD").strip()
    tree = step.request.getfixturevalue("tmp_path_factory").mktemp("laying") / "w1"
    W.git(step.repo, "worktree", "add", "-q", "-b", "workspace", str(tree))
    items = {name: backlog_items.find(step.repo, B.ident(name)) for name in blocks}
    for item in items.values():
        laid = laying.lay(item, tree)
        assert laid.outcome == "done", laid
    W.git(tree, "add", "-A")
    W.git(tree, "commit", "-q", "-m", "laid")
    lifted = next(n for n in step.names if re.match(r"i\d+$", n))
    w["tree"], w["item"] = tree, items[lifted]
    w["response"] = laying.lift(items[lifted], tree, base=base)


def _lines(step, rel):
    w = world(step)
    assert w["response"].outcome == "done", (step.text, w["response"])
    return (w["tree"] / rel).read_text().split("\n")


def _imports(step, area):
    text = "\n".join(_lines(step, "spec/model/%s.md" % area))
    found = re.search(r"(?m)^imports: \[(.*)\]$", text)
    return [n.strip() for n in found.group(1).split(",") if n.strip()]


def _members(step):
    lines = _lines(step, NOTES)
    assert lines.count(HEADER) == 1, lines
    at = lines.index(HEADER)
    end = next((i for i in range(at + 1, len(lines)) if not lines[i].startswith(" ")), len(lines))
    return lines[at + 1:end]


def then(step):
    """The Thens of these groups, each read off the workspace after the lift (the module's doc)."""
    tag = group(step)
    if tag is None or "tree" not in world(step):
        return False
    kinds = [k for k, _ in parts(step)]
    if tag == "g42":
        assert _imports(step, "registry") == [], _imports(step, "registry")
    elif tag == "g43":
        lines = _lines(step, NOTES)
        assert [x for x in lines if x.startswith("  operation archive(")] == [OPERATION], lines
    elif tag == "g44" and step.template.endswith("Not"):          # d1 does not hold the restating line m3
        assert _members(step) == list(OLD) + [MEMBER], _members(step)
    elif tag == "g44":
        members = _members(step)
        assert kinds[-1] != "member line" or members.count(MEMBER) == 1, members
    else:
        assert "notes" in _imports(step, "stock"), _imports(step, "stock")
        assert "stock-releasing" not in (world(step)["tree"] / "spec" / "index.md").read_text()
        assert not (world(step)["tree"] / "spec" / "capabilities" / "stock-releasing.md").exists()


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
