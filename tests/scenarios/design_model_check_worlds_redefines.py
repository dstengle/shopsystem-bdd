"""The worlds of a term that redefines a verb of the request pack (b847, parsing r30, r31; checking r162, r163): the
domain-model fixture (tests/scripts/fixtures/domain-model/) whose notes service has an operation `return(note)`, no
command's (`[unexposed]`), named by the verb return of the notes layer, `Redefines: request`, its frame
`the person returns <note>` (an actor that is no service: the pack's `service returns thing` and it tell the senses
apart) or, `overlapping`, `<actor> returns <note>` (an agent, the kind above service: they do not).

Rows design_model_check_worlds' TABLE takes first: r1 of the capability `thing` a requirement that uses the term
(`REDEFINED`, read by the context's sense, the request of `notes.return`) or the pack's term return beside it
(`PACKED`, read by the pack's sense, the notes service giving every note). `read_by` is what the Then of one logical
form reads the kept tree by: the entry of the verb return its fun names, the context's (naming the operation) or the
pack's."""
import importlib.util
import re
import shutil
import sys
from pathlib import Path


def _sibling(name, module):
    if module not in sys.modules:
        spec = importlib.util.spec_from_file_location(module, Path(__file__).with_name(name))
        sys.modules[module] = loaded = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loaded)
    return sys.modules[module]


H = _sibling("design_model_check_handlers.py", "shop_design_model_check_handlers")
W = _sibling("work_queue_world.py", "shop_work_queue_world")
ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "scripts" / "fixtures" / "domain-model"

OPERATION = "  operation return(note)  outcomes: done\n"
FRAMES = {False: "the person returns <note>", True: "<actor> returns <note>"}
TERM = ("- **return** (verb, action) → operation notes.return. A note given back to the person who lent it. Forms: "
        "returns, returned. Redefines: request. Frame: %s.\n")
REDEFINED = "When the person returns a note, the notes service shall keep the note."
PACKED = "When the person lists the notes, the notes service shall return every note."
OPERATION_OF = {REDEFINED: "notes.return", PACKED: ""}


def fixture(repo, overlapping=False):
    """The fixture copied into `repo` (spec, features and its program), with the operation return and its verb."""
    for part in ("spec", "features"):
        shutil.copytree(FIXTURE / part, repo / part, dirs_exist_ok=True)
    program = (FIXTURE / "notes_cli.py").read_text()
    (repo / "notes_cli.py").write_text(program.replace('Path(__file__).resolve().parents[4] / "scripts"',
                                                       repr(str(ROOT / "scripts"))))
    model = repo / "spec" / "model" / "notes.md"
    text = model.read_text()
    assert "  operation list()" in text, text
    model.write_text(text.replace("  operation list()", OPERATION + "  operation list()", 1))
    vocabulary = repo / "spec" / "vocabulary" / "notes.md"
    vocabulary.write_text(vocabulary.read_text() + TERM % FRAMES[overlapping])
    contract = repo / "spec" / "adapters" / "cli.toml"
    contract.write_text(contract.read_text() + '\n[unexposed]\noperations = ["notes.return"]\n')


def requirement(line):
    """A builder: the fixture with the verb return, and r1 `line` in thing.md."""
    def build(step):
        fixture(step.repo)
        H.write(step.repo, "spec/capabilities/thing.md", (
            "---\nid: capability/example.org/fixture/domain-model/thing\ntitle: thing\nnarrator: the person\n"
            "group: service\narea: notes\nspecifies: service notes\nlanguage: codified-2\nretired: []\n---\n\n"
            "# thing\n\n## Purpose\nSomething.\n\n## Behaviour\n\n### [g1] line 1\n- [r1] %s\n" % line))
        step.context["read by"] = OPERATION_OF[line]
    return build


def read_by(step, stdout):
    """The operation the entry of the verb return names that the one tree `spec parse` printed uses ("" of the
    pack's entry), read off the tree's fun `e_return_action_<n>_<m>` and grammar 4's vocabulary of the world."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import spec_rgl_vocab
    funs = re.findall(r"\be_return_action_(\d+)_\d+\b", stdout)
    assert len(set(funs)) == 1, stdout
    return spec_rgl_vocab.read(step.repo).verbs[int(funs[0]) - 1].term.operation


ROWS = [
    (("term redefine `request`", "`request` has term", "requirement use term"), requirement(PACKED), {}),
    (("term redefine `request`", "requirement use term"), requirement(REDEFINED), {}),
]


@W.local("ThenPrints")
def one_form(step):
    """`the language service returns one logical form of the requirement r1` in these worlds: `spec parse` printed one
    tree, and it reads the verb return by the entry the world says (the context's of `notes.return`, or the pack's)."""
    if "read by" not in step.context or not step.nps or not step.nps[0].startswith("one logical form"):
        return False
    done = step.context["result"]
    trees = re.findall(r"^\d+: (?:When|If|While|Where|NoPre) ", done.stdout, re.MULTILINE)
    assert done.returncode == 0 and len(trees) == 1, done.stdout + done.stderr
    assert read_by(step, done.stdout) == step.context["read by"], done.stdout
