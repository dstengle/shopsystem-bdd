"""Handlers of checking's scenario of a domain model object spelled by an imported pack's term (r113, b688), each a
`work_queue_world.local` that takes only a step of its group (`mine`). The world is the domain-model fixture
(tests/scripts/fixtures/domain-model/), written at the When: the pack p1 the context's own `spec/packs/p1.md`, which
spec/index.md imports, its term t1 the noun `binder`; the element e1 notes' `object binder` with the attribute
`title`, no vocabulary entry meaning the object; the element e2 `object folder kind of binder`, the noun `folder`,
and notebook's line r10 saying "the title of a folder", which reads only once the binder is the pack's kind. The
contract annotated and the features generated, `spec check` is run; the Then reads its exit."""
import shutil
import sys
from pathlib import Path

W = sys.modules["shop_work_queue_world"]
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"
PACK = "---\nsource: ex.com/prod/up\n---\n# p1\n\n## Glossary\n\n- **binder** (noun): a thing the pack gives.\n"
OBJECTS = "object binder\n  attributes: title (text)\n\nobject folder kind of binder\n"
ENTRIES = ("- **folder** (noun) → object folder. A binder a person keeps notes in.\n"
           "- **title** (attribute) → attribute binder.title. What a binder is called.\n")
GROUP = ("\n\n### [g10] A note filed while a folder is untitled is archived\n- [r10] While the title of a folder is "
         "`untitled`, when the person files a note, the notes service shall archive the note.\n")


def mine(step):
    found = sys.modules["vocab"].vocab4.requested.scenario(step.request.node)
    return found is not None and Path(found.feature.filename).stem == "checking" and "g113" in found.tags


def given(step):
    """a pack p1, a term t1, an element e1; this bounded context imports the pack p1, the pack p1 has the term t1, the
    term t1 spells the element e1, no term means the element e1, the element e2 refers to the term t1: so the world
    built at the When says."""
    return None if mine(step) else False


def build(step):
    """The fixture copied into the repository with the pack, the objects, their entries and notebook's r10."""
    repo = step.repo
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    (repo / "spec" / "packs").mkdir(exist_ok=True)
    (repo / "spec" / "packs" / "p1.md").write_text(PACK)
    index = repo / "spec" / "index.md"
    assert "imports: [request]\n" in index.read_text()
    index.write_text(index.read_text().replace("imports: [request]\n", "imports: [request, p1]\n", 1))
    model = repo / "spec" / "model" / "notes.md"
    text = model.read_text()
    at = text.rindex("```")
    model.write_text(text[:at] + OBJECTS + text[at:])
    vocabulary = repo / "spec" / "vocabulary" / "notes.md"
    vocabulary.write_text(vocabulary.read_text().rstrip("\n") + "\n" + ENTRIES)
    notebook = repo / "spec" / "capabilities" / "notebook.md"
    notebook.write_text(notebook.read_text().rstrip("\n") + GROUP)
    step.run("spec", "annotate")
    step.run("features", "generate")


def runs(step):
    if not mine(step) or step.term != "`spec check`":
        return False
    build(step)
    step.context["result"] = step.run("spec", "check")


def then_ok(step):
    """the specification service completes this request: `spec check` exits 0."""
    if not mine(step) or "result" not in step.context:
        return False
    done = step.context["result"]
    assert done.returncode == 0, done.stdout + done.stderr


for _template in ("GivenK", "GivenDoes", "GivenDoesNot"):
    W.local(_template)(given)
W.local("WhenRuns")(runs)
W.local("ThenExitsOk")(then_ok)
