"""Handlers of applying's scenarios of what an apply keeps of an item's model lines, terms and operation tables
(r10-r23; laying's r28-r41 before b872, b746), `work_queue_world.local`s tried before applying_handlers' own, each
taking only a step of a scenario of one of their groups (`mine`). A scenario's world is its group's (`WORLDS`),
built at the When (applying_handlers' `applied`) on readiness_world's codified spec with the domain-model fixture's
model, vocabulary, CLI contract and notebook beside it (applying_handlers' `fixture`), so the Givens record nothing:
the item i1 (`b1`) holding a table of `notes.archive` told apart by its parameter's example (g10), `notes.archive`
withheld (g11), a model line adding `notes.pin` (g12), the table under ids `g1` and `r1` that work-queue holds
already (g13, as g20 the moved term); a model line restating notes' `archive` (g14), `object note` (g15), the event
`a note is added` (g16), the actor `the person` (g17); `object tag` moved to an area `labels` (g18), shared's `the
person` moved to notes (g19); notes' event retired (g21), the term `low` (g22), an `object folder` and its term
`folder` (g23). The Thens are applying_handlers_model_then's."""
import re
import sys

A = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/applying_handlers.py"))   # loaded before this, by name
R, W, world, L = A.R, A.W, A.world, A
OPERATION, CONTRACT = "notes.archive", "spec/adapters/cli.toml"
MODEL, LABELS, NOTES, SHARED = ("spec/model/notes.md", "spec/model/labels.md", "spec/vocabulary/notes.md",
                                "spec/vocabulary/shared.md")
NOTEBOOK = ("### notebook\n\n#### [g10] An active note archived is kept\n- [r10] While a note is `active`, when the "
            "person archives the note, the notes service shall keep the note.\n\n%s")
MODELLED = "### notes model\n\n```model\n%s\n```"
PIN = ("### notebook\n\n#### [g10] An active note pinned is kept\n- [r10] While a note is `active`, when the person pins "
       "the note, the notes service shall keep the note.\n\n### notes model\n\n```model\nservice notes\n  operation "
       "pin(note)  outcomes: done\n```\n\n- **pin** (verb, action) → operation notes.pin. Forms: pins, pinned. "
       "Frame: <actor> pins <note>.")
# What each restating group's model line says in place of what the model held: (the model's line, the item's).
ARCHIVED = ("  operation archive(note)  outcomes: done", "  operation archive(note, reason)  outcomes: done")
HEADER = "object note"
NOTE_OLD = "  attributes: text (text); priority: low | high"
NOTE = (HEADER, "  attributes: text (text); priority: low | high | urgent",
        "  lifecycle status: draft → active; active → retired; draft → retired",
        "  relations: carries → tag (many)")
LONE = {"g16": ("event a note is added: raised by notes.add",
                "event a note is added: raised by notes.add; delivery: at least once"),
        "g17": ("actor the person kind of agent", "actor the person")}
LABELLED = ("---\nid: model/example.org/fixture/labels\narea: labels\nkind: core\nimports: []\n---\n\n# Labels\n\n"
            "## Purpose\n\nThe labels notes carry.\n\n```model\n```\n")
PERSON = "- **the person** (proper noun) → actor the person. The human who keeps the notes."
FOLDER = "- **folder** (noun) → object folder. A place a person keeps notes in."
# What each retiring group's item retires, and the line of the area's file it takes out: (file, line).
RETIRES = {"g21": ("- model line `event a note is added: raised by notes.add` in notes",
                   (MODEL, "event a note is added: raised by notes.add")),
           "g22": ("- term `low → value note.priority low` in notes",
                   (NOTES, "- **low** (adjective) → value note.priority low.")),
           "g23": ("- model line `object folder` in notes\n- term `folder → object folder` in notes",
                   (NOTES, FOLDER))}
WORLDS = {}


def table(name):
    """The tables of the operation table `name`: notes.archive's, its parameter's example its name."""
    return ('[operations."%s"]\ncommand = "notes archive"\n[operations."%s".parameters]\nnote = { positional = 1, '
            'example = "%s" }' % (OPERATION, OPERATION, name))


def group(step):
    return A.group(step, WORLDS)


def mine(step):
    return group(step) is not None


def colliding(text):
    """The item's block with its first group and requirement ids `g1` and `r1`, which its capability holds already."""
    text = re.sub(r"(?m)^#### \[g\d+\]", "#### [g1]", text, count=1)
    return re.sub(r"(?m)^- \[r\d+\]", "- [r1]", text, count=1)


def _tabled(step):
    """The item's `### cli adapter` block of the table o1; of g13 after the PASSING line under colliding ids, on the
    codified spec alone (no model, which the request pack would not read the line in) with a contract of no table."""
    block = "### cli adapter\n\n```toml\n%s\n```" % table("o1")
    if group(step) != "g13":
        A.fixture(step)
        return block
    contract = step.repo / CONTRACT
    contract.parent.mkdir(parents=True, exist_ok=True)
    contract.write_text('[programs]\nnotes = "notes.py"\n')
    return colliding(R().block("Title of i1", R().PASSING) + "\n\n" + block)


def _labels(step):
    (step.repo / LABELS).write_text(LABELLED)
    return NOTEBOOK % "### moves\n\n- model line `object tag` from notes to labels"


def _moved(step):
    text = NOTEBOOK % "### moves\n\n- term `the person → actor the person` from shared to notes"
    return colliding(text) if group(step) == "g20" else text


def _folder(step):
    """notes given an `object folder` that no line says and its term `folder`."""
    model = step.repo / MODEL
    text = model.read_text()
    at = text.rindex("```")
    model.write_text(text[:at] + "\nobject folder\n  attributes: name (text)\n" + text[at:])
    vocabulary = step.repo / NOTES
    vocabulary.write_text(vocabulary.read_text().rstrip("\n") + "\n" + FOLDER + "\n")
    return _retiring(step)


def _retiring(step):
    return NOTEBOOK % ("### retirements\n\n%s" % RETIRES[group(step)][0])


WORLDS.update({
    "g10": _tabled,
    "g11": lambda step: "### cli adapter\n\nwithheld: [%s]" % OPERATION,
    "g12": lambda step: PIN,
    "g13": _tabled,
    "g14": lambda step: NOTEBOOK % (MODELLED % ("service notes\n" + ARCHIVED[1])),
    "g15": lambda step: NOTEBOOK % (MODELLED % "\n".join(NOTE)),
    "g16": lambda step: NOTEBOOK % (MODELLED % LONE["g16"][1]),
    "g17": lambda step: NOTEBOOK % (MODELLED % LONE["g17"][1]),
    "g18": _labels,
    "g19": _moved,
    "g20": _moved,
    "g21": _retiring,
    "g22": _retiring,
    "g23": _folder,
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
    A.applied(step, _world)


def _world(step):
    """The group's world, the domain-model fixture beside the codified spec but of the tables' groups (`_tabled`)."""
    if group(step) not in ("g10", "g13"):
        A.fixture(step)
    return WORLDS[group(step)](step)


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
