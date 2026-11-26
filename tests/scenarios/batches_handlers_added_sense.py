"""A capability whose line uses a verb an item gives a sense, though the item holds no line of it (batches r164,
b715): readiness_world's codified spec, supervision given a sense of the glossary's `take` in its `## Terms` (take#2,
"agent takes stage") and a line `r5` using it, kept in the corpus (`grammar/corpus/spec/supervision.md`) with the form
`spec parse --form` prints before the lay; the item holding readiness_world's passing line of work-queue and, in a
block of review (whose `## Terms` is a layer before supervision's), a third sense of `take` ("agent takes brief"), so
supervision's sense is read as take#3 once the item is laid. The Thens read supervision's corpus file off the batch's
branch after `work batch start`: r5's block holds the form `spec parse --form` prints of its line there. Loaded before
batches_handlers_beyond and batches_handlers_corpus, whose handlers would take these steps."""
import re
import subprocess
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
SCRIPTS = __import__("pathlib").Path(__file__).resolve().parents[2] / "scripts"
CAPABILITY = "spec/capabilities/supervision.md"
CORPUS = "grammar/corpus/spec/supervision.md"
USING = "r5"
LINE = "When `work` starts a stage, `work` shall take the stage."
OLDER = ("## Terms\n\n- **take** (verb, action): an agent takes a stage up. Forms: takes, taken. "
         "Frame: agent takes stage.\n\n")
GROUP = "### [g4] a stage started is taken\n- [%s] %s\n\n" % (USING, LINE)
NEWER = ("- **take** (verb, action): an agent takes a brief in. Forms: takes, taken. Frame: agent takes brief.")
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's


def _form(root, line):
    return subprocess.run([sys.executable, str(SCRIPTS / "spec"), "--root", str(root), "parse", "--form", line],
                          capture_output=True, text=True, check=True).stdout.rstrip("\n")


def _mine(step, *kinds):
    return step.context.get("sensed") and [k for k, _ in parts(step)] == list(kinds)


@four("GivenK", "sense", *BOTH)
@four("GivenK", "verb", *BOTH)
def given_named(step):
    """a sense s1, a verb v1: `take`, in readiness_world's codified spec."""
    sys.modules["shop_readiness_world"].codify(step)
    step.context["sensed"] = True


@four("GivenDoes", "has", *BOTH)
def has(step):
    """the verb v1 has the sense s1: NEWER; the capability c1 has the requirement r1: supervision and its r5."""
    if not (_mine(step, "verb", "sense") or _mine(step, "capability", "requirement")):
        return False


@four("GivenDoes", "holds", *BOTH)
@four("GivenDoesNot", "holds", *BOTH)
@four("GivenDoesNot", "hold", *BOTH)
def holds(step):
    """the item i1 holds the verb v1: NEWER in a block of review beside the passing line of work-queue; the capability
    c1 holds no requirement id (of the item)."""
    R = sys.modules["shop_readiness_world"]
    if _mine(step, "item", "verb"):
        B.write_item(step, parts(step)[0][1], sections={"Requirements": "### review\n\n%s\n\n%s"
                                                        % (NEWER, R.block("Title", R.PASSING))})
    elif not (step.context.get("sensed") and parts(step)[0][0] in ("capability", "item")
              and " holds no requirement id" in step.text):     # "the item i1 ... in the capability c1" (b716)
        return False


@four("GivenDoes", "uses", *BOTH)
@four("GivenDoes", "use", *BOTH)
def uses(step):
    """the requirement r1 uses the verb v1: supervision given OLDER and r5, and the corpus its block with the form
    printed before the lay."""
    if not _mine(step, "requirement", "verb"):
        return False
    path = step.repo / CAPABILITY
    text = path.read_text().replace("## Behaviour\n", OLDER + "## Behaviour\n", 1)
    path.write_text(text.replace("## Not yet", GROUP + "## Not yet", 1))
    where = step.repo / "grammar" / "corpus" / "spec"
    where.mkdir(parents=True, exist_ok=True)
    (where / "README.md").write_text("# The spec corpus\n")
    (where / "supervision.md").write_text("# supervision: every live line with its intended reading\n\n## %s\nKept."
                                          "\n\n```reading\n%s\n%s\n```\n" % (USING, LINE, _form(step.repo, LINE)))


def corpus(step):
    """this corpus holds the requirement r1, the batches service keeps the logical form l1, the requirement r1 has it:
    r5's block on the batch's branch holds the form `spec parse --form` prints of its line there, take#3."""
    if not step.context.get("sensed") or parts(step)[-1][0] not in ("requirement", "logical form"):
        return False
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    text = T.git(step, "show", "%s:%s" % (branches[0], CORPUS))
    form = _form(step.repo / ".shop" / "worktrees" / branches[0], LINE)
    assert re.search(r"take#3\(e\d+, subject: x\d+, object: x\d+\)", form), form
    assert "## %s\nKept.\n\n```reading\n%s\n%s\n```\n" % (USING, LINE, form) in text, (form, text)


four("ThenDoes", "holds", *BOTH)(corpus)
four("ThenDoes", "has", *BOTH)(corpus)
for _verb in KEEPS:
    four("ThenDoes", _verb, *BOTH)(corpus)
