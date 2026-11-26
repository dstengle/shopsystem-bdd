"""Handlers of laying's scenarios of what a lay keeps of an item's model lines, terms and operation tables (r28-r41,
b746), moved from batches' (r79, r80, r87, r92, r116-r118, r120, r121, r126, r127, r133, r134, r142),
`work_queue_world.local`s tried before laying_handlers' own, each taking only a step of a scenario of one of their
groups (`mine`). A scenario's world is its group's (`WORLDS`), built at the When on readiness_world's codified spec
with the domain-model fixture's model, vocabulary, CLI contract and notebook beside it (`_fixture`), so the Givens
record nothing: the item i1 (`b1`) holding a table of `notes.archive` told apart by its parameter's example (g28),
`notes.archive` withheld (g29), a model line adding `notes.pin` (g30), the table under ids `g1` and `r1` that
work-queue holds already (g31, as g38 the moved term); a model line restating notes' `archive` (g32), `object note`
(g33), the event `a note is added` (g34), the actor `the person` (g35); `object tag` moved to an area `labels` (g36),
shared's `the person` moved to notes (g37); notes' event retired (g39), the term `low` (g40), an `object folder` and
its term `folder` (g41). The When commits the world, makes the workspace w1 a worktree of it and lays the item there;
the Thens are laying_handlers_model_then's."""
import re
import shutil
import sys
from pathlib import Path

L = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers.py"))   # loaded before this, by name
R, W, world = L.R, L.W, L.world
B = sys.modules["shop_backlog_world"]
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
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
LONE = {"g34": ("event a note is added: raised by notes.add",
                "event a note is added: raised by notes.add; delivery: at least once"),
        "g35": ("actor the person kind of agent", "actor the person")}
LABELLED = ("---\nid: model/example.org/fixture/labels\narea: labels\nkind: core\nimports: []\n---\n\n# Labels\n\n"
            "## Purpose\n\nThe labels notes carry.\n\n```model\n```\n")
PERSON = "- **the person** (proper noun) → actor the person. The human who keeps the notes."
FOLDER = "- **folder** (noun) → object folder. A place a person keeps notes in."
# What each retiring group's item retires, and the line of the area's file it takes out: (file, line).
RETIRES = {"g39": ("- model line `event a note is added: raised by notes.add` in notes",
                   (MODEL, "event a note is added: raised by notes.add")),
           "g40": ("- term `low → value note.priority low` in notes",
                   (NOTES, "- **low** (adjective) → value note.priority low.")),
           "g41": ("- model line `object folder` in notes\n- term `folder → object folder` in notes",
                   (NOTES, FOLDER))}
WORLDS = {}


def table(name):
    """The tables of the operation table `name`: notes.archive's, its parameter's example its name."""
    return ('[operations."%s"]\ncommand = "notes archive"\n[operations."%s".parameters]\nnote = { positional = 1, '
            'example = "%s" }' % (OPERATION, OPERATION, name))


def group(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None or Path(found.feature.filename).stem != "laying":
        return None
    return next((t for t in found.tags if t in WORLDS), None)


def mine(step):
    return group(step) is not None


def _fixture(step):
    """The domain-model fixture's model, vocabulary, CLI contract and notebook beside the codified spec, the index
    importing the request pack."""
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary", "adapters"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))


def colliding(text):
    """The item's block with its first group and requirement ids `g1` and `r1`, which its capability holds already."""
    text = re.sub(r"(?m)^#### \[g\d+\]", "#### [g1]", text, count=1)
    return re.sub(r"(?m)^- \[r\d+\]", "- [r1]", text, count=1)


def _tabled(step):
    """The item's `### cli adapter` block of the table o1, after the PASSING line under colliding ids (g31)."""
    block = "### cli adapter\n\n```toml\n%s\n```" % table("o1")
    return colliding(R().block("Title of i1", R().PASSING) + "\n\n" + block) if group(step) == "g31" else block


def _labels(step):
    (step.repo / LABELS).write_text(LABELLED)
    return NOTEBOOK % "### moves\n\n- model line `object tag` from notes to labels"


def _moved(step):
    text = NOTEBOOK % "### moves\n\n- term `the person → actor the person` from shared to notes"
    return colliding(text) if group(step) == "g38" else text


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
    "g28": _tabled,
    "g29": lambda step: "### cli adapter\n\nwithheld: [%s]" % OPERATION,
    "g30": lambda step: PIN,
    "g31": _tabled,
    "g32": lambda step: NOTEBOOK % (MODELLED % ("service notes\n" + ARCHIVED[1])),
    "g33": lambda step: NOTEBOOK % (MODELLED % "\n".join(NOTE)),
    "g34": lambda step: NOTEBOOK % (MODELLED % LONE["g34"][1]),
    "g35": lambda step: NOTEBOOK % (MODELLED % LONE["g35"][1]),
    "g36": _labels,
    "g37": _moved,
    "g38": _moved,
    "g39": _retiring,
    "g40": _retiring,
    "g41": _folder,
})


def given(step):
    """A Given of these groups: what the group's world builds at the When."""
    if not mine(step):
        return False
    world(step)


def requests(step):
    """`the batches service lays the item i1 in the workspace w1`: the world built, the item laid; the reply kept."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    import backlog_items
    import laying
    w = world(step)
    R().codify(step)
    _fixture(step)
    B.write_item(step, "i1", sections={"Requirements": WORLDS[group(step)](step)})
    W.init(step.repo)
    W.git(step.repo, "add", "-A")
    W.git(step.repo, "commit", "-q", "--allow-empty", "-m", "the world")
    tree = step.request.getfixturevalue("tmp_path_factory").mktemp("laying") / "w1"
    W.git(step.repo, "worktree", "add", "-q", "-b", "workspace", str(tree))
    w["tree"], w["item"] = tree, backlog_items.find(step.repo, "b1")
    w["response"] = laying.lay(w["item"], tree)


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
