"""laying_handlers_prepare's worlds of g17 and g18 (b758), moved from batches' (b707, b715), and their Thens.
g17: beside readiness_world's codified spec, the domain-model fixture's model, vocabulary and notebook (the index
importing the request pack), the repository keeping notebook's feature and a corpus whose `notebook.md` holds each line
of notebook with its form before the lay; the item holding a line of a capability `shelf` new to the notes area, no
line of notebook, and a `### notes model` block restating notes' `add` with a parameter `note` (so notebook r4's
scenario brings the note in by a Given and names it in its When) and giving a note a request (so r4's "the request"
is the note's: its form changes). g18: supervision given a sense of `take` (take#2, "agent takes stage") and a line
`r5` using it, kept in the corpus with its form before the lay; the item holding readiness_world's passing line and,
in a block of review (a layer before supervision's), a third sense of `take`, so supervision's is read as take#3 once
laid. The Thens read the prepared workspace's feature and corpus. Laying's checks of g19 and g20 are the specification
service's now (checking r165, r166, b871)."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

P = next(m for m in list(sys.modules.values())
         if str(getattr(m, "__file__", "") or "").endswith("/laying_handlers_prepare.py"))   # loaded before this
R, W, B, world, group, kept, form = P.R, P.W, P.B, P.world, P.group, P.kept, P.form
SCRIPTS, FIXTURE = P.SCRIPTS, Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model" / "spec"
NOTEBOOK, FEATURE = "spec/capabilities/notebook.md", "features/notebook.feature"
BLOCK = ("### shelf\n\nnarrator: a person keeping notes\ngroup: service\npurpose: Notes kept on a shelf.\narea: notes\n\n"
         "#### [g1] An active note archived is shelved\n- [r1] While a note is `active`, when the person archives the "
         "note, the notes service shall keep the note.\n\n"
         "### notes model\n\n```model\nobject note\n  relations: has → request (one)\n\nservice notes\n"
         "  operation add(note, text, priority, reminder (flag))  outcomes: done → the note | refused: no text\n```")
STEP = "    Given a note n1\n    When the person adds the note n1 without a text and the reminder\n"
GOVERNING = "r4"       # notebook's "If the person adds a note without a text and the reminder, then ... the request"
USING, LINE = "r5", "When `work` starts a stage, `work` shall take the stage."
OLDER = ("## Terms\n\n- **take** (verb, action): an agent takes a stage up. Forms: takes, taken. "
         "Frame: agent takes stage.\n\n")
NEWER = "- **take** (verb, action): an agent takes a brief in. Forms: takes, taken. Frame: agent takes brief."


def _lines(root):
    """{id: line} of notebook's requirements at `root`."""
    return dict(re.findall(r"(?m)^- \[(r\d+)\] (.*)$", (root / NOTEBOOK).read_text().replace("\n  ", " ")))


def _corpus(step, name, blocks):
    where = step.repo / "grammar" / "corpus" / "spec"
    where.mkdir(parents=True, exist_ok=True)
    (where / "README.md").write_text("# The spec corpus\n")
    (where / ("%s.md" % name)).write_text("# %s: every live line with its intended reading\n%s" % (name, blocks))


def _modelled(step):
    """The fixture's model, vocabulary and notebook beside the codified spec, the index importing the request pack."""
    R().codify(step)
    spec = step.repo / "spec"
    for folder in ("model", "vocabulary"):
        shutil.copytree(FIXTURE / folder, spec / folder, dirs_exist_ok=True)
    shutil.copy(FIXTURE / "capabilities" / "notebook.md", spec / "capabilities" / "notebook.md")
    index = spec / "index.md"
    index.write_text(index.read_text().replace("imports: [cli]", "imports: [request]"))


def beyond(step):
    _modelled(step)
    _corpus(step, "notebook", "".join("\n## %s\nKept.\n\n```reading\n%s\n%s\n```\n" % (rid, line, form(step.repo, line))
                                      for rid, line in _lines(step.repo).items()))
    subprocess.run([sys.executable, str(SCRIPTS / "features"), "generate", "--root", str(step.repo), "notebook"],
                   capture_output=True, text=True, check=True)
    B.write_item(step, "i1", sections={"Requirements": BLOCK})


def sensed(step):
    R().codify(step)
    path = step.repo / "spec" / "capabilities" / "supervision.md"
    text = path.read_text().replace("## Behaviour\n", OLDER + "## Behaviour\n", 1)
    group = "### [g4] a stage started is taken\n- [%s] %s\n\n" % (USING, LINE)
    path.write_text(text.replace("## Not yet", group + "## Not yet", 1))
    _corpus(step, "supervision", "\n## %s\nKept.\n\n```reading\n%s\n%s\n```\n" % (USING, LINE, form(step.repo, LINE)))
    B.write_item(step, "i1", sections={"Requirements": "### review\n\n%s\n\n%s" % (NEWER, R().block("Title", R().PASSING))})


P.WORLDS.update({"g17": beyond, "g18": sensed})


def _corpus_holds(step, name, rid, line, want):
    """The prepared workspace's corpus of `name` holds `rid`'s block with the form `spec parse --form` prints of its
    line there, which `want` finds."""
    text, tree = kept(step, "grammar/corpus/spec/%s.md" % name), world(step)["tree"]
    found = form(tree, line)
    assert re.search(want, found), found
    assert "## %s\nKept.\n\n```reading\n%s\n%s\n```\n" % (rid, line, found) in text, (found, text)


def then(step):
    """g17: the feature generated (notebook's, r4's scenario naming the note its When adds, what `features generate`
    writes there) and r4's block of the corpus; g18: supervision's r5 block read as take#3."""
    tag, w = group(step), world(step)
    if tag not in ("g17", "g18") or "tree" not in w:
        return False
    kinds = [k for k, _ in sys.modules["shop_world_four"].parts(step)]
    if tag == "g17" and kinds[-1] == "feature":
        text = kept(step, FEATURE)
        assert STEP in text.split("@r4\n", 1)[1].split("@r5", 1)[0], text
        check = subprocess.run([sys.executable, str(SCRIPTS / "features"), "generate", "--check", "--root",
                                str(w["tree"]), "notebook"], capture_output=True, text=True)
        assert check.returncode == 0, (check.stdout, check.stderr)
    elif tag == "g17":
        _corpus_holds(step, "notebook", GOVERNING, _lines(w["tree"])[GOVERNING], r"of\(x4, x2\)")
    elif tag == "g18":
        _corpus_holds(step, "supervision", USING, LINE, r"take#3\(e\d+, subject: x\d+, object: x\d+\)")
    else:
        return False
    return None


W.local("ThenDoes")(then)
