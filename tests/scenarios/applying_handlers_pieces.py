"""Handlers of applying's scenarios of what an apply keeps of an item's spec pieces (r2-r9, r25; laying's r7, r8,
r22-r27, r49 before b872, b745), `work_queue_world.local`s tried before applying_handlers' own, each taking only a
step of a scenario of one of their groups (`mine`). A scenario's world is its group's (`WORLDS`), built on
readiness_world's codified spec at the When (applying_handlers' `applied`), so the Givens record nothing: the item
i1 (`b1`) holding a universal condition, spec/universal.md taken out (g2); a capability new to the spec, `shelf`,
its one group the PASSING line (g3), its block saying `area: tracking` (g5); the PASSING line's group serving the
job `start-work` (g4); the driven port `stock` the item makes, beside the domain-model fixture (g6); a term of the
context's own pack `household` (g7), under ids `g1` and `r1` that work-queue holds already (g8); an import of the
plugin's pack `time` (g9); the capability `shelf` in the fixture's area `notes`, whose model declares the service
`notes` (g25). The Thens read the reply's changed paths and the specification's files."""
import re
import sys

A = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/applying_handlers.py"))   # loaded before this, by name
R, W, world, kept = A.R, A.W, A.world, A.kept
parts = sys.modules["shop_world_four"].parts
JOB, AREA, PACK, PLUGIN_PACK, PORT, PORTED = "start-work", "tracking", "household", "time", "stock", "stock-port"
SERVICE = "notes"      # the fixture's area, and the service its model declares (g25)
UNIVERSAL, INDEX, SHELF = "spec/universal.md", "spec/index.md", "spec/capabilities/shelf.md"
NOTED = "When the person adds a note, the notes service shall keep the note."   # a line of notes' words (g25)
TERM = "- **pantry** (noun): a cupboard food is kept in."
NEW = ("### shelf\n\nnarrator: a person shelving things\ngroup: service\npurpose: Things kept on a shelf, each found "
       "by its name.%s\n\n#### [g1] Shelving\n- [r1] %s")
PORT_BLOCK = """### stock-port

narrator: the notes service
group: service
purpose: What the notes service needs of the stock it reaches.
area: stock
kind: port

#### [g1] A note reserved is reserved
- [r1] When the notes service reserves a note, the stock service shall not refuse the request.

### notebook

#### [g10] A person who starts has a note reserved
- [r10] When the person starts, the notes service shall reserve a note with the quantity `2`.

#### [g11] A reservation completed is kept
- [r11] When the stock service completes a reservation, the notes service shall keep the reservation.

### stock model

```model
object reservation kind of request
  relations: for → note (one)

service stock
  operation reserve(note, quantity)  outcomes: done → the reservation | refused: no stock
```

- **reservation** (noun) → object reservation. Stock set aside for a note.
- **reserve** (verb, action) → operation stock.reserve. Forms: reserves, reserved. Frame: <actor> reserves <note>.
- **the stock service** (proper noun) → service stock."""
WORLDS = {}


def group(step):
    return A.group(step, WORLDS)


def mine(step):
    return group(step) is not None


def _passing(step):
    return R().block("Title of i1", R().PASSING)   # the item i1's one group


def _new(step, area=""):
    """The capability `shelf` new to the spec; spec/index.md given the empty `## Composition` `migrate init`
    writes."""
    index = step.repo / INDEX
    if "\n## Composition" not in index.read_text():
        index.write_text(index.read_text().rstrip("\n") + "\n\n## Composition\n")
    return NEW % (area, R().PASSING)


def _ported(step):
    """The domain-model fixture beside the codified spec (applying_handlers' `fixture`) and the driven port's block."""
    A.fixture(step)
    return PORT_BLOCK


def _specified(step):
    """The capability `shelf` new to the spec in the area `notes` of the domain-model fixture, whose model declares
    the service `notes`."""
    _ported(step)
    return _new(step, "\narea: %s" % SERVICE).replace(R().PASSING, NOTED)


def _colliding(step):
    """The pack's block under the ids `g1` and `r1`, which work-queue holds already."""
    text = re.sub(r"(?m)^#### \[g\d+\]", "#### [g1]", _passing(step), count=1)
    return re.sub(r"(?m)^- \[r\d+\]", "- [r1]", text, count=1) + "\n\n### %s pack\n\n%s" % (PACK, TERM)


WORLDS.update({
    "g2": lambda step: ((step.repo / UNIVERSAL).unlink(missing_ok=True)
                         or R().give_universal(step, "i1", R().TRANSLATED_U)),
    "g3": _new,
    "g4": lambda step: _passing(step).replace("\n\n####", "\n\nserves: [g4 %s]\n\n####" % JOB, 1),
    "g5": lambda step: _new(step, "\narea: %s" % AREA),
    "g6": _ported,
    "g7": lambda step: _passing(step) + "\n\n### %s pack\n\n%s" % (PACK, TERM),
    "g8": _colliding,
    "g9": lambda step: _passing(step) + "\n\n### imports\n\n- pack `%s`" % PLUGIN_PACK,
    "g25": _specified,
})


def given(step):
    """A Given of these groups: what the group's world builds at the When."""
    if not mine(step):
        return False
    world(step)


def requests(step):
    """`the batches service applies the item i1 to the specification s1`: the world built, the item applied."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    A.applied(step, WORLDS[group(step)])


def empty_sections(text):
    """The `## ` headings of `text` with nothing but blank lines under them."""
    found = re.finditer(r"(?ms)^## (.+?)[ \t]*\n(.*?)(?=^## |\Z)", text)
    return [m.group(1) for m in found if not m.group(2).strip()]


def capability_form(text):
    """What keeps `text` from conforming to the capability form, or []."""
    head = text.split("\n---", 1)[0] if text.startswith("---\n") else ""
    problems = ["no %s:" % f for f in ("area", "specifies") if not re.search(r"(?m)^%s: \S" % f, head)]
    return problems + ["the empty section ## %s" % s for s in empty_sections(text)]


def _row(text, area):
    """The cells of `area`'s rows of the index's `## Composition` table."""
    rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in text.splitlines() if r.startswith("|")]
    return [r for r in rows if r[0] == area]


def _imports(text):
    found = re.search(r"(?m)^imports: \[([^\]]*)\]$", text)
    return [n.strip() for n in found.group(1).split(",") if n.strip()] if found else []


def _group(step):
    """The laid group of work-queue that holds the PASSING line."""
    text = kept(step, "spec/capabilities/%s.md" % R().CAPABILITY)
    found = [g for g in re.split(r"(?m)^(?=### \[g)", text) if R().PASSING in g]
    assert len(found) == 1, text
    return found[0]


def _keeps(step, tag):
    """`the specification service keeps X`: the file the apply changed of each group's X."""
    if tag == "g2":
        kept(step, UNIVERSAL)
    elif tag in ("g3", "g5", "g25"):
        kept(step, SHELF)
    elif tag == "g4":
        _group(step)
    elif tag == "g6":
        model = kept(step, "spec/model/%s.md" % PORT)
        assert re.search(r"(?m)^kind: port$", model) and _imports(model) == ["notes"], model
        assert PORT in _imports(kept(step, "spec/model/notes.md")), step.text
        contract = (world(step)["tree"] / "spec/adapters/cli.toml").read_text()
        assert '[operations."%s.reserve"]' % PORT not in contract, contract
    elif tag in ("g7", "g8"):
        kept(step, "spec/packs/%s.md" % PACK)
    else:
        assert PLUGIN_PACK in _imports(kept(step, INDEX)), kept(step, INDEX)


def then(step):
    """The Thens of these groups: what the apply kept (`_keeps`); the language of `universal` its marker; the capability
    of the capability form; the group's `serves:` line naming the job, in work-queue; the capability in its area (its
    `area:`, the area's Composition row naming it) or in the driven port (of kind `port`, its model of kind `port`);
    the pack's `## Glossary` holding the term, and the index importing the pack."""
    tag = group(step)
    if tag is None or "tree" not in world(step):
        return False
    term = "keep" if step.term in A.KEEPS else step.term
    kinds = [k for k, _ in parts(step)]
    if term == "keep":
        _keeps(step, tag)
    elif term == "set":
        wanted = step.text.rsplit(" to ", 1)[1].strip("`")
        assert re.search(r"(?m)^language: %s$" % re.escape(wanted), kept(step, UNIVERSAL)), kept(step, UNIVERSAL)
    elif term == "conform":
        assert not capability_form(kept(step, SHELF)), (capability_form(kept(step, SHELF)), kept(step, SHELF))
    elif term in ("serve", "serves"):
        lines = _group(step).split("\n")
        assert lines[1].startswith("serves:") and JOB in [j.strip() for j in lines[1][7:].split(",")], lines
    elif term == "has" and kinds == ["capability", "requirement group"]:
        _group(step)
    elif term == "holds" and kinds[0] == "area":
        assert re.search(r"(?m)^area: %s$" % AREA, kept(step, SHELF)), kept(step, SHELF)
        assert any("shelf" in r[2] for r in _row(kept(step, INDEX), AREA)), kept(step, INDEX)
    elif term == "holds" and kinds[0] == "driven port":
        assert re.search(r"(?m)^area: %s$" % PORT, kept(step, "spec/capabilities/%s.md" % PORTED)), step.text
        assert _row(kept(step, INDEX), PORT) == [[PORT, "port", PORTED]], kept(step, INDEX)
        assert re.search(r"(?m)^kind: port$", kept(step, "spec/model/%s.md" % PORT)), step.text
    elif term == "has" and kinds == ["area", "service"]:
        assert re.search(r"(?m)^service %s$" % SERVICE, (world(step)["tree"] / "spec/model/notes.md").read_text())
    elif term in ("specify", "specifies"):
        assert re.search(r"(?m)^specifies: service %s$" % SERVICE, kept(step, SHELF)), kept(step, SHELF)
    elif term == "has" and kinds == ["pack", "term"]:
        text = kept(step, "spec/packs/%s.md" % PACK)
        assert "## Glossary" in text and text.index("## Glossary") < text.index(TERM), text
    elif term in ("import", "imports"):
        assert (PACK if tag == "g7" else PLUGIN_PACK) in _imports(kept(step, INDEX)), kept(step, INDEX)
    else:
        raise AssertionError("applying_handlers_pieces takes no Then %s %s: %s" % (step.template, step.term, step.text))


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
for _key in (("ThenDoes", "serve"), ("ThenDoes", "import"), ("ThenDoes", "specify")):   # `features vocab --check`
    sys.modules["vocab"].handler(*_key)(A.untaken)
