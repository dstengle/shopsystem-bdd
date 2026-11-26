"""A capability an item's model lines reach, though the item holds no line of it (batches r157, b707): over
batches_handlers_restate's world (its Given of a model line: the domain-model fixture's model, vocabulary and
notebook), the repository keeping notebook's feature and a corpus whose `notebook.md` holds each line of notebook with
its form, as `features generate` and `spec parse --form` write them before the lay; the item holding a line of a
capability `shelf` new to the notes area, no line of notebook, and a `### notes model` block that restates notes' `add`
with a parameter `note` added (so notebook r4's scenario brings the note in by a Given and names it in its When) and
gives a note a request (so r4's "the request" is the note's, not the trigger's: its form changes). The Thens read
notebook's feature and corpus file off the batch's branch after `work batch start`: what `features generate` and
`spec parse --form` write on that branch. Loaded before batches_handlers_corpus, batches_handlers_new_op and
batches_handlers_restate, whose handlers would take these steps."""
import re
import subprocess
import sys

B, T, F = (sys.modules[n] for n in ("shop_backlog_world", "shop_batches_world", "shop_world_four"))
four, parts = F.four, F.parts
BOTH = ("backlog", "batches")
SCRIPTS = __import__("pathlib").Path(__file__).resolve().parents[2] / "scripts"
CAPABILITY = "spec/capabilities/notebook.md"
FEATURE = "features/notebook.feature"
CORPUS = "grammar/corpus/spec/notebook.md"
GOVERNING = "r4"       # notebook's "If the person adds a note without a text and the reminder, then ... the request"
BLOCK = ("### shelf\n\nnarrator: a person keeping notes\ngroup: service\npurpose: Notes kept on a shelf.\narea: notes\n\n"
         "#### [g1] An active note archived is shelved\n- [r1] While a note is `active`, when the person archives the "
         "note, the notes service shall keep the note.\n\n"
         "### notes model\n\n```model\nobject note\n  relations: has → request (one)\n\nservice notes\n"
         "  operation add(note, text, priority, reminder (flag))  outcomes: done → the note | refused: no text\n```")
STEP = "    Given a note n1\n    When the person adds the note n1 without a text and the reminder\n"
KEEPS = ("write", "commit", "post", "keep", "make", "rewrite", "publish")     # requested.py's


def _form(root, line):
    return subprocess.run([sys.executable, str(SCRIPTS / "spec"), "--root", str(root), "parse", "--form", line],
                          capture_output=True, text=True, check=True).stdout.rstrip("\n")


def _lines(root):
    """{id: line} of notebook's requirements at `root`."""
    text = (root / CAPABILITY).read_text()
    return dict(re.findall(r"(?m)^- \[(r\d+)\] (.*)$", text.replace("\n  ", " ")))


def _corpus(step):
    """The corpus (its README and notebook's file, each line's block with its form before the lay) and notebook's
    feature, as the base holds them."""
    where = step.repo / "grammar" / "corpus" / "spec"
    where.mkdir(parents=True, exist_ok=True)
    (where / "README.md").write_text("# The spec corpus\n")
    blocks = "".join("\n## %s\nKept.\n\n```reading\n%s\n%s\n```\n" % (rid, line, _form(step.repo, line))
                     for rid, line in _lines(step.repo).items())
    (where / "notebook.md").write_text("# notebook: every live line with its intended reading\n%s" % blocks)
    subprocess.run([sys.executable, str(SCRIPTS / "features"), "generate", "--root", str(step.repo), "notebook"],
                   capture_output=True, text=True, check=True)


@four("GivenDoes", "specifies", *BOTH)
@four("GivenDoes", "specify", *BOTH)
def specifies(step):
    """the model line m1 specifies the operation o1, said before the item holds it: notes' `add`, which BLOCK
    restates."""
    if [k for k, _ in parts(step)] != ["model line", "operation"] or "model_item" in step.context \
            or not step.context.get("restating"):
        return False
    step.context["governed"] = True


@four("GivenDoes", "holds", *BOTH)
@four("GivenDoesNot", "holds", *BOTH)
@four("GivenDoesNot", "hold", *BOTH)
def holds(step):
    """the item i1 holds the model line m1: BLOCK, and no requirement line; the capability c1 holds no requirement id
    (of the item)."""
    if not step.context.get("governed"):
        return False
    (k1, n1), (k2, _) = parts(step)
    if (k1, k2) == ("item", "model line"):
        B.write_item(step, n1, sections={"Requirements": BLOCK})
    elif " holds no requirement id" not in step.text:     # "... in the capability c1" (b716)
        return False


@four("GivenDoes", "has", *BOTH)
@four("GivenDoes", "governs", *BOTH)
@four("GivenDoes", "govern", *BOTH)
def governs(step):
    """the capability c1 has the requirement r1, the requirement r1 governs the operation o1: notebook and its r4,
    whose line requests `add`; the corpus written once both are said."""
    if not step.context.get("governed"):
        return False
    kinds = [k for k, _ in parts(step)]
    if kinds not in (["capability", "requirement"], ["requirement", "operation"]):
        return False
    if kinds[0] == "requirement":
        _corpus(step)


def _laid(step, rel):
    """The run exited 0; (the file `rel` on the batch's branch, the branch's worktree)."""
    done = step.context["result"]
    assert done.returncode == 0, (step.text, done.stdout, done.stderr)
    branches = T.git(step, "branch", "--list", "batch-*", "--format=%(refname:short)").split()
    assert branches, (step.text, done.stdout, done.stderr)
    return T.git(step, "show", "%s:%s" % (branches[0], rel)), step.repo / ".shop" / "worktrees" / branches[0]


@four("ThenDoes", "generates", *BOTH)
@four("ThenDoes", "generate", *BOTH)
@four("ThenDoes", "has", *BOTH)
def feature(step):
    """the batches service generates the feature f1, the capability c1 has it: notebook's feature on the batch's
    branch is what `features generate` writes there, r4's scenario naming the note its When adds."""
    if not step.context.get("governed") or parts(step)[-1][0] != "feature":
        return False
    text, tree = _laid(step, FEATURE)
    assert STEP in text.split("@r4\n", 1)[1].split("@r5", 1)[0], text
    check = subprocess.run([sys.executable, str(SCRIPTS / "features"), "generate", "--check", "--root", str(tree), "notebook"],
                           capture_output=True, text=True)
    assert check.returncode == 0, (check.stdout, check.stderr)


def corpus(step):
    """this corpus holds the requirement r1, the batches service keeps the logical form l1, the requirement r1 has it:
    r4's block on the batch's branch holds the form `spec parse --form` prints of its line there, the note's
    request."""
    if not step.context.get("governed") or parts(step)[-1][0] not in ("requirement", "logical form"):
        return False
    text, tree = _laid(step, CORPUS)
    line = _lines(tree)[GOVERNING]
    form = _form(tree, line)
    assert "of(x4, x2)" in form, form
    assert "## %s\nKept.\n\n```reading\n%s\n%s\n```\n" % (GOVERNING, line, form) in text, (form, text)


four("ThenDoes", "holds", *BOTH)(corpus)
four("ThenDoes", "has", *BOTH)(corpus)
for _verb in KEEPS:
    four("ThenDoes", _verb, *BOTH)(corpus)
