"""Handlers of applying's scenarios of what an apply prepares in the specification (r38-r47, b873; laying's r9-r18 of
a workspace prepared for a batch before, b758), `work_queue_world.local`s tried before applying_handlers' own, each
taking only a step of a scenario of one of their groups (`mine`). A scenario's world is its group's (`WORLDS`: this
module's for g38-g45, applying_handlers_reached's for g46, g47), built on readiness_world's codified spec at the When
(applying_handlers' `applied`), so the Givens record nothing: the item i1 (`b1`) holding readiness_world's PASSING
line as `work-queue#r5` (g43-g45) beside a corpus (`grammar/corpus/spec/`, g38), retiring `work-queue#r4` whose block
the corpus holds (g39), with a line citing a rule's code (`v15k`, g40) or using a construct (`order-by`, the spec pack
imported, g41), or one of a value that spells a construct's code and uses none, no construct catalogue in the
repository (g42); the index given a Composition naming `work-queue` and `shelved`, a capability every line of which is
retired (g44, g45). The When applies the item to the specification s1 and keeps the specification service's reply.
The Thens read the reply's changed paths and the specification's files."""
import re
import subprocess
import sys
from pathlib import Path

A = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/applying_handlers.py"))   # loaded before this, by name
R, W, world, kept = A.R, A.W, A.world, A.kept
SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
OWN = {"g38", "g39", "g40", "g41", "g42", "g43", "g44", "g45"}
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
    return A.group(step, WORLDS)


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
        return block            # applying_handlers' `applied` writes it as the item's `## Requirements`
    R().give_lines(step, "i1", text)
    return None


WORLDS.update({
    "g38": lambda step: _world(step, R().PASSING, corpus=""),
    "g39": lambda step: _world(step, None, corpus="\n## %s\nKept.\n\n```reading\nthe retired line\nshall []\n```\n"
                                % RETIRED, block="### work-queue\n\nretired: [%s]\n\n#### [g4] Retiring\n- [r5] %s"
                                % (RETIRED, R().PASSING)),
    "g40": lambda step: _world(step, CITING),
    "g41": lambda step: _world(step, USING, imports="cli, spec"),
    "g42": lambda step: _world(step, VALUED),
    "g43": lambda step: _world(step, R().PASSING),
    "g44": lambda step: _world(step, R().PASSING, composed=True),
    "g45": lambda step: _world(step, R().PASSING, composed=True),
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
    """The Thens of g38-g45: the corpus holding the line's block with its form (kept: the corpus changed) or no longer
    the retired id's; the rule catalogue's entry of `v15k` citing the line; the construct catalogue kept, or none; the
    index file kept, of the index form, holding `work-queue` and not `shelved` (g44) or naming `supervision` (g45)."""
    tag = group(step)
    if tag not in OWN or "response" not in world(step):
        return False
    w, text, negated = world(step), step.text, step.template.endswith("Not")
    if tag in ("g38", "g39"):
        corpus = kept(step, CORPUS)
        if tag == "g38" and text.startswith("this corpus holds"):
            rid, line = _line(step)
            want = "## %s\nFrom: %s %s.\n\n```reading\n%s\n%s\n```\n" % (rid, "b1", rid, line, form(w["tree"], line))
            assert want in corpus, (want, corpus)
        elif tag == "g39" and "does not hold" in text:
            assert "## %s\n" % RETIRED not in corpus, corpus
    elif tag == "g40":
        entry = kept(step, RULES).split("\n## v15k\n", 1)[1].split("\n## ", 1)[0]
        assert "work-queue#%s" % _line(step)[0] in entry, entry
    elif tag == "g41":
        kept(step, CONSTRUCTS)
    elif tag == "g42":
        assert negated and w["response"].outcome == "done", (step.text, w["response"])
        assert not (w["tree"] / CONSTRUCTS).exists() and CONSTRUCTS not in w["response"].content["changed"], text
    else:
        index = kept(step, INDEX)
        if "conforms" in text:
            assert not index_problems(w["tree"], index), (index_problems(w["tree"], index), index)
        elif tag == "g44" and negated:
            assert not re.search(r"(?<![\w-])shelved(?![\w-])", index), index
        elif tag == "g45" and not negated and "holds" in text:
            assert any("supervision" in named(c) for c in rows(index) or []), index
    return None


for _template in ("GivenK", "GivenK_A", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRequests")(requests)
for _template in ("ThenDoes", "ThenDoesNot"):
    W.local(_template)(then)
