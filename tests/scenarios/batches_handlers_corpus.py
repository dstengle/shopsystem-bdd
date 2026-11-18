"""The lay's bookkeeping in features/batches.feature (b333, batches r46-r49): the scenario repository given a corpus
(`grammar/corpus/spec/`, the one corpus file `work-queue.md`), an item that retires `work-queue#r4` whose block the
corpus holds, an item whose line cites a rule's or a construct's code; and the Thens read off the lay's commit on the
batch's branch: the laid line's block with its form as `model parse --form` prints it on that branch, the retired id's
block gone, the catalogue entry citing the line, the construct catalogue written."""
import subprocess
import sys

import backlog_items
import backlog_lines

W, B, T, F = (sys.modules[n] for n in ("shop_work_queue_world", "shop_backlog_world", "shop_batches_world",
                                       "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
CORPUS = "grammar/corpus/spec/work-queue.md"
SCRIPTS = __import__("pathlib").Path(__file__).resolve().parents[2] / "scripts"
RETIRED = "r4"         # the fixture's work-queue#r4, whose group g3 holds no other line
# A line citing a code: a rule's (`v15k`, model.lp's) or a construct's (`order-by`, the construct catalogue's), on a
# trigger no other group of the fixture has.
CITING = "When the person runs `work check`, `work` shall print `%s`."
CODES = {"rule": "v15k", "construct": "order-by"}


def corpus(step, blocks=""):
    """The repository's corpus: its README and work-queue's file, with `blocks`."""
    R = sys.modules["shop_readiness_world"]
    R.codify(step)
    where = step.repo / "grammar" / "corpus" / "spec"
    where.mkdir(parents=True, exist_ok=True)
    (where / "README.md").write_text("# The spec corpus\n")
    (where / "work-queue.md").write_text("# work-queue: every live line with its intended reading\n%s" % blocks)


@four("GivenK", "logical form", *BOTH)
@four("GivenK", "requirement id", *BOTH)
@four("GivenK", "rule", *BOTH)
@four("GivenK", "construct", *BOTH)
def given_named(step):
    """A thing a later Given says what it is."""


@four("GivenDoes", "has", *BOTH)
def has_given(step):
    """The requirement has the logical form (the repository keeps a corpus), or has the requirement id (the corpus
    holds the block of the id the item retires)."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) == ("requirement", "logical form"):
        corpus(step)
    elif (k1, k2) == ("requirement", "requirement id"):
        corpus(step, "\n## %s\nKept.\n\n```reading\n%s\nshall []\n```\n" % (RETIRED, "the retired line"))
        step.context.setdefault("corpus_ids", {})[n1] = RETIRED
    else:
        return False


@four("GivenDoes", "holds", *BOTH)
def holds_given(step):
    """The item holds the requirement id: it retires `work-queue#r4` beside a passing line; this corpus holds the
    requirement (its block written by `has_given`)."""
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) == ("item", "requirement id"):
        R = sys.modules["shop_readiness_world"]
        R.codify(step)
        B.write_item(step, n1, sections={"Requirements": "### work-queue\n\nretired: [%s]\n\n#### [g4] Retiring\n- [r5] %s"
                                         % (RETIRED, R.PASSING)})
    elif step.subject != "this corpus":
        return False


@four("GivenDoes", "use", *BOTH)
def uses_given(step):
    """The requirement uses the rule or the construct: the item's line cites its code."""
    (k1, n1), (k2, _) = parts(step)
    if k1 != "requirement" or k2 not in CODES:
        return False
    step.context["cited"] = CODES[k2]
    sys.modules["shop_readiness_world"].give_lines(step, step.context["proposed"][n1], CITING % CODES[k2])


def _laid(step, rel):
    """The run exited 0; the file `rel` on the batch's branch, and whether the lay's commit changed it."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branch = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()[0]
    changed = T.git(step, "show", "--name-only", "--format=", branch).split()
    return T.git(step, "show", "%s:%s" % (branch, rel)), rel in changed, branch


def _line(step, name):
    """(id, line) of the item's one line, as the item holds it after the pick renumbered it."""
    item = backlog_items.find(step.repo, B.ident(name))
    blocks = backlog_lines.read(item, item.name)
    return next((rid, text) for b in blocks for g in b.groups for rid, text in g.requirements)


@four("ThenDoes", "holds", *BOTH)
def corpus_holds(step):
    """This corpus holds the logical form: the laid line's block on the batch's branch, its form what `model parse
    --form` prints of the line on that branch."""
    if step.subject != "this corpus":
        return False
    text, _, branch = _laid(step, CORPUS)
    rid, line = _line(step, next(iter(step.context["proposed"].values())))
    tree = step.repo / ".shop" / "worktrees" / branch
    form = subprocess.run([sys.executable, str(SCRIPTS / "model"), "--root", str(tree), "parse", "--form", line],
                          capture_output=True, text=True, check=True).stdout.rstrip("\n")
    want = "## %s\nFrom: %s %s.\n\n```reading\n%s\n%s\n```\n" % (rid, B.ident(next(iter(
        step.context["proposed"].values()))), rid, line, form)
    assert want in text, (want, text)


@four("ThenDoes", "write", *BOTH)
def writes(step):
    """The lay's commit wrote the corpus (the logical form), the rule catalogue (the catalogue entry) or the construct
    catalogue, each citing the item's line where it is a catalogue."""
    k = "construct catalogue" if step.nps[-1] == "this construct catalogue" else parts(step)[1][0]
    rel = {"logical form": CORPUS, "catalogue entry": "grammar/rules.md",
           "construct catalogue": "grammar/constructs.md"}.get(k)
    if rel is None:
        return False
    text, changed, _ = _laid(step, rel)
    assert changed, (step.text, rel)
    if k != "logical form":
        rid = _line(step, next(iter(step.context["proposed"].values())))[0]
        entry = text.split("## %s\n" % step.context["cited"], 1)[1].split("\n## ", 1)[0]
        assert "work-queue#%s" % rid in entry, (step.text, entry)


@four("ThenDoes", "has", *BOTH)
def rule_has(step):
    """The rule has the catalogue entry: its `## <code>` entry is in the batch branch's rule catalogue."""
    (k1, _), (k2, _) = parts(step)
    if (k1, k2) != ("rule", "catalogue entry"):
        return False
    text, _, _ = _laid(step, "grammar/rules.md")
    assert "\n## %s\n" % step.context["cited"] in text, step.text


@four("ThenDoes", "remove", *BOTH)
def removes(step):
    """The requirement the corpus held under the retired id: its block is out of the batch branch's corpus."""
    name = parts(step)[1][1]
    if name not in step.context.get("corpus_ids", {}):
        return False
    text, changed, _ = _laid(step, CORPUS)
    assert changed and "## %s\n" % step.context["corpus_ids"][name] not in text, (step.text, text)
