"""Handlers of applying's scenarios of an item that retires an area (r48-r50, b898; r51, b903), `work_queue_world.local`s tried
before applying_handlers' own, each taking only a step of a scenario of one of their groups (`mine`). The world, built
at the When (applying_handlers' `applied`) on readiness_world's codified spec with the domain-model fixture beside it
(applying_handlers' `fixture`), so the Givens record nothing: an area a1 `shelving`, an empty model file of kind port
and an empty layer (the area a2 of g49), notes' model (g49's a1) and labels' (g49's a3) importing it, and two capabilities of it, c1 `shelves` and c2 `racks`, each holding
only retired ids; the item i1 (`b1`) holding a line of notebook and the retirement `- area `shelving``. The Thens
read the reply's changed paths and the specification's files: no model file and no layer of the area (g48), no area
that imports it (g49), the capabilities kept in the specification, in no area (g50); in g51 c1 is `shelving`, the
stem of the area, and no capability is read in the area by backlog_retire_area's `capabilities`."""
import re
import sys

import backlog_retire_area
from plumbing import shop_files

A = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/applying_handlers.py"))   # loaded before this, by name
W, world = A.W, A.world
GROUPS = ("g48", "g49", "g50", "g51")
AREA = "shelving"
CAPS = {"c1": "shelves", "c2": "racks"}
NOTEBOOK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the "
            "person archives the note, the notes service shall keep the note.\n\n### retirements\n\n- area `%s`" % AREA)
MODEL = ("---\nid: model/example.org/fixture/shelving\narea: shelving\nkind: port\nimports: [notes]\n---\n\n"
         "# Shelving\n\n## Purpose\n\nThe shelves notes stand on.\n\n```model\n```\n")
LABELS = ("---\nid: model/example.org/fixture/labels\narea: labels\nkind: core\nimports: [shelving]\n---\n\n"
          "# Labels\n\n## Purpose\n\nThe labels notes carry.\n\n```model\n```\n")
LAYER = "---\nid: vocabulary/example.org/fixture/shelving\narea: shelving\n---\n\n# The words of shelving\n\n## Terms\n"
CAPABILITY = ("---\nid: capability/example.org/fixture/%s\ntitle: %s\nnarrator: the person\ngroup: service\n"
              "area: shelving\nspecifies: service notes\nlanguage: codified-2\nretired: [g1, r1]\nunbuilt: []\n---\n\n"
              "# %s\n\n## Purpose\n\nShelves.\n\n## Behaviour\n")


def _caps(step):
    """{name: file stem} of the capabilities of the scenario's world: c1 the area's stem in g51."""
    return dict(CAPS, c1=AREA) if A.group(step, GROUPS) == "g51" else CAPS


def mine(step):
    return A.group(step, GROUPS) is not None


def given(step):
    """A Given of these groups: what the world builds at the When."""
    if not mine(step):
        return False
    world(step)


def _world(step):
    A.fixture(step)
    spec = step.repo / "spec"
    (spec / "model" / ("%s.md" % AREA)).write_text(MODEL)
    (spec / "vocabulary" / ("%s.md" % AREA)).write_text(LAYER)
    (spec / "model" / "labels.md").write_text(LABELS)
    notes = spec / "model" / "notes.md"
    notes.write_text(notes.read_text().replace("imports: []", "imports: [%s]" % AREA))
    for name in _caps(step).values():
        (spec / "capabilities" / ("%s.md" % name)).write_text(CAPABILITY % (name, name.title(), name.title()))
    return NOTEBOOK


def requests(step):
    """`the batches service applies the item i1 to the specification s1`: the world built, the item applied."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    A.applied(step, _world)


def _capability(step, name):
    """(frontmatter, path) of the capability `name` in the specification."""
    path = world(step)["tree"] / "spec" / "capabilities" / ("%s.md" % _caps(step)[name])
    return (shop_files.frontmatter(path.read_text())[0] if path.is_file() else None), path


def then(step):
    """`keeps the domain model d1`: the apply done, the area's model file among what it changed; `the domain model d1
    does not hold the area a1`: no model file, no layer and no import of it; `does not hold the area a3` (g49): no
    model file that imports it; `the specification s1 holds the
    capability c1`, `keeps the capability c1`: its file kept, which the apply changed; `does not keep the capability
    c2`: no capability of the area kept, c2's file in no area."""
    if not mine(step) or "tree" not in world(step):
        return False
    w, tree = world(step), world(step)["tree"]
    assert w["response"].outcome == "done", w["response"]
    name = next((n for n in CAPS if "capability %s" % n in step.text), None)
    if "domain model d1" in step.text and step.template == "ThenDoes":
        assert "spec/model/%s.md" % AREA in w["response"].content["changed"], w["response"]
    elif "the area a3" in step.text:
        importing = [p.stem for p in sorted((tree / "spec" / "model").glob("*.md"))
                     if re.search(r"(?m)^imports: \[[^\]]*\b%s\b" % AREA, p.read_text())]
        assert importing == [], importing
    elif "domain model d1" in step.text:
        model = tree / "spec" / "model"
        assert not (model / ("%s.md" % AREA)).exists(), "the model file of the area is kept"
        assert not (tree / "spec" / "vocabulary" / ("%s.md" % AREA)).exists(), "the layer of the area is kept"
        assert AREA not in (model / "notes.md").read_text(), (model / "notes.md").read_text()
    elif name is not None and step.template == "ThenDoes":
        head, path = _capability(step, name)
        assert head is not None, path
        assert path.relative_to(tree).as_posix() in w["response"].content["changed"], w["response"]
    elif name is not None:
        head, path = _capability(step, name)
        assert head is None or head.get("area") != AREA, (path, head)
        assert all(_capability(step, n)[0].get("area") != AREA for n in CAPS), "a capability is kept in the area"
        read = [p.name for p in backlog_retire_area.capabilities(tree, AREA)]
        assert read == [], "a capability is read in the area: %s" % read
    else:
        raise AssertionError("applying_handlers_retire_area takes no Then %s: %s" % (step.template, step.text))


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
