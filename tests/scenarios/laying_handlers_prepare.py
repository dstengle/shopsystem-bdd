"""Handlers of laying's scenarios of a workspace prepared for a batch (r6, r9-r18, b758),
`work_queue_world.local`s tried before laying_handlers' own, each taking only a step of a scenario of one of their
groups (`mine`). A scenario's world is its group's (`WORLDS`: this module's for g6 and g9-g16, laying_handlers_reached's
for g17, g18), built on readiness_world's codified spec at the When, so the Givens of these groups record nothing: the
item i1 (`b1`) holding readiness_world's PASSING line as `work-queue#r5` (g6, g14-g16), beside a corpus
(`grammar/corpus/spec/`, g9), retiring `work-queue#r4` whose block the corpus holds (g10), with a line citing a rule's
code (`v15k`, g11) or using a construct (`order-by`, the spec pack imported, g12), or one of a value that spells a
construct's code and uses none, no construct catalogue in the repository (g13); the index given a Composition naming
`work-queue` and `shelved`, a capability every line of which is retired (g15, g16). The When commits the world, makes
the workspace w1 a worktree of it, lays the item there and prepares the workspace for the batch `batch-1` with the
item (`laying.prepare`), and keeps the laying service's reply.
The Thens read the reply's changed paths and the workspace's files."""
import re
import subprocess
import sys
from pathlib import Path

L = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers.py"))   # loaded before this, by name
R, W, world = L.R, L.W, L.world
B = sys.modules["shop_backlog_world"]
SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
OWN = {"g6", "g9", "g10", "g11", "g12", "g13", "g14", "g15", "g16"}
CORPUS = "grammar/corpus/spec/work-queue.md"
RULES, CONSTRUCTS, INDEX = "grammar/rules.md", "grammar/constructs.md", "spec/index.md"
RETIRED = "r4"         # the fixture's work-queue#r4, whose group g3 holds no other line
CITING = "When the person runs `work check`, `work` shall print `v15k`."
USING = "When the person runs `work check` on a requirement that uses `order-by`, `work` shall exit successfully."
VALUED = ("While an initiative is `done`, when the person runs `work abandon` on the initiative, `work` shall exit "
          "successfully.")      # `done` spells a construct's code, cited by no "uses"
SHELVED = ("---\nid: capability/ex.com/prod/ctx/shelved\ntitle: Shelved\nnarrator: the person\ngroup: service\n"
           "language: codified-2\nretired: [g1, r1]\n---\n\n# Shelved\n\n## Purpose\nThings once shelved.\n\n"
           "## Behaviour\n")
COMPOSITION = ("\n\n## Composition\n\nThe capabilities, by area.\n\n| area | kind | capabilities |\n|---|---|---|\n"
               "| work-queue | core | work-queue |\n| shelved | core | shelved |\n\n### Retired\n\n`shelved`.\n")
HEADER = re.compile(r"^\|\s*area\s*\|\s*kind\s*\|\s*capabilities\s*\|$")
WORLDS = {}


def group(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    if found is None or Path(found.feature.filename).stem != "laying":
        return None
    return next((t for t in found.tags if t in WORLDS), None)


def mine(step):
    return group(step) is not None


def _corpus(step, blocks=""):
    where = step.repo / "grammar" / "corpus" / "spec"
    where.mkdir(parents=True, exist_ok=True)
    (where / "README.md").write_text("# The spec corpus\n")
    (where / "work-queue.md").write_text("# work-queue: every live line with its intended reading\n%s" % blocks)


def _composed(step):
    index = step.repo / INDEX
    index.write_text(index.read_text().rstrip("\n") + COMPOSITION)
    (step.repo / "spec" / "capabilities" / "shelved.md").write_text(SHELVED)


def _world(step, text, corpus=None, composed=False, imports=None, block=None):
    R().codify(step)
    if corpus is not None:
        _corpus(step, corpus)
    if composed:
        _composed(step)
    if imports:
        index = step.repo / INDEX
        index.write_text(index.read_text().replace("imports: [cli]", "imports: [%s]" % imports, 1))
    if block is not None:
        B.write_item(step, "i1", sections={"Requirements": block})
    else:
        R().give_lines(step, "i1", text)


WORLDS.update({
    "g6": lambda step: _world(step, R().PASSING),
    "g9": lambda step: _world(step, R().PASSING, corpus=""),
    "g10": lambda step: _world(step, None, corpus="\n## %s\nKept.\n\n```reading\nthe retired line\nshall []\n```\n"
                               % RETIRED, block="### work-queue\n\nretired: [%s]\n\n#### [g4] Retiring\n- [r5] %s"
                               % (RETIRED, R().PASSING)),
    "g11": lambda step: _world(step, CITING),
    "g12": lambda step: _world(step, USING, imports="cli, spec"),
    "g13": lambda step: _world(step, VALUED),
    "g14": lambda step: _world(step, R().PASSING),
    "g15": lambda step: _world(step, R().PASSING, composed=True),
    "g16": lambda step: _world(step, R().PASSING, composed=True),
})


def given(step):
    """A Given of these groups: what the group's world builds at the When."""
    if not mine(step):
        return False
    world(step)


def requests(step):
    """`the batches service prepares the workspace w1 for the batch b1`: the world built, the item laid and the
    workspace prepared for `batch-1`; the reply kept."""
    if not mine(step) or step.template != "WhenRequests":
        return False
    import backlog_items
    import laying
    w = world(step)
    WORLDS[group(step)](step)
    W.init(step.repo)
    W.git(step.repo, "add", "-A")
    W.git(step.repo, "commit", "-q", "--allow-empty", "-m", "the world")
    tree = step.request.getfixturevalue("tmp_path_factory").mktemp("laying") / "w1"
    W.git(step.repo, "worktree", "add", "-q", "-b", "workspace", str(tree))
    item = backlog_items.find(step.repo, "b1")
    w["tree"], w["item"] = tree, item
    laid = laying.lay(item, tree)
    assert laid.outcome == "done", laid
    w["prepared"] = laying.prepare(tree, "batch-1", [item])
    assert w["prepared"].outcome == "done", w["prepared"]
    w["response"] = w["prepared"]


def kept(step, rel):
    """The workspace's file `rel`, which the prepare done changed."""
    w = world(step)
    assert w["prepared"].outcome == "done" and rel in w["prepared"].content["changed"], (
        step.text, rel, w["prepared"])
    return (w["tree"] / rel).read_text()


def _line(step):
    item = world(step)["item"]
    import backlog_lines
    return next((rid, text) for b in backlog_lines.read(item, item.name) for g in b.groups
                for rid, text in g.requirements)


def form(tree, line):
    return subprocess.run([sys.executable, str(SCRIPTS / "spec"), "--root", str(tree), "parse", "--form", line],
                          capture_output=True, text=True, check=True).stdout.rstrip("\n")


def rows(text):
    found = re.search(r"(?ms)^## Composition[ \t]*\n(.*?)(?=^## |\Z)", text)
    lines = [r.strip() for r in found.group(1).splitlines() if r.strip().startswith("|")] if found else []
    if not lines or not HEADER.match(lines[0]):
        return None
    return [[c.strip() for c in r.strip("|").split("|")] for r in lines[2:]]


def named(cells):
    return [n.strip().strip("`") for n in cells[2].split(",") if n.strip()]


def index_problems(tree, text):
    """What keeps the index `text` from the index form: one `## Composition`, its table, each capability of the
    workspace with a requirement named in its area's row (its `area:`, else its name)."""
    import spec_read
    if len(re.findall(r"(?m)^## Composition[ \t]*$", text)) != 1:
        return ["not one ## Composition"]
    table = rows(text)
    if table is None:
        return ["no table | area | kind | capabilities |"]
    found = []
    for path in sorted((Path(tree) / "spec" / "capabilities").glob("*.md")):
        body = path.read_text()
        if not any(spec_read.REQ.match(line) for _, line in spec_read.numbered(body, "Behaviour")):
            continue
        area = (re.search(r"(?m)^area: (\S+)", body.split("\n---", 1)[0]) or [None, path.stem])[1]
        if not any(c[0] == area and path.stem in named(c) for c in table):
            found.append("%s not in the row of %s" % (path.stem, area))
    return found


def then(step):
    """The Thens of g9-g16: the corpus holding the line's block with its form (kept: the corpus changed) or no longer
    the retired id's; the rule catalogue's entry of `v15k` citing the line; the construct catalogue kept, or none; the
    index file kept, of the index form, holding `work-queue` and not `shelved` (g15) or naming `supervision` (g16).
    g6's are laying_handlers'."""
    tag = group(step)
    if tag not in OWN or tag == "g6" or "tree" not in world(step):
        return False
    w, text, negated = world(step), step.text, step.template.endswith("Not")
    if tag in ("g9", "g10"):
        corpus = kept(step, CORPUS)
        if tag == "g9" and text.startswith("this corpus holds"):
            rid, line = _line(step)
            want = "## %s\nFrom: %s %s.\n\n```reading\n%s\n%s\n```\n" % (rid, "b1", rid, line, form(w["tree"], line))
            assert want in corpus, (want, corpus)
        elif tag == "g10" and "does not hold" in text:
            assert "## %s\n" % RETIRED not in corpus, corpus
    elif tag == "g11":
        entry = kept(step, RULES).split("\n## v15k\n", 1)[1].split("\n## ", 1)[0]
        assert "work-queue#%s" % _line(step)[0] in entry, entry
    elif tag == "g12":
        kept(step, CONSTRUCTS)
    elif tag == "g13":
        assert negated and w["prepared"].outcome == "done", (step.text, w["prepared"])
        assert not (w["tree"] / CONSTRUCTS).exists() and CONSTRUCTS not in w["prepared"].content["changed"], text
    else:
        index = kept(step, INDEX)
        if "conforms" in text:
            assert not index_problems(w["tree"], index), (index_problems(w["tree"], index), index)
        elif tag == "g15" and negated:
            assert not re.search(r"(?<![\w-])shelved(?![\w-])", index), index
        elif tag == "g16" and not negated and "holds" in text:
            assert any("supervision" in named(c) for c in rows(index) or []), index
    return None


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
