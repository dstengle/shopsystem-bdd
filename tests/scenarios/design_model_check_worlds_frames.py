"""The worlds of a verb of several frames (parsing r13-r16, b420, design-decision 0111), rows design_model_check_worlds'
TABLE takes before its world of a requirement of two logical forms: the domain-model fixture
(tests/scripts/fixtures/domain-model/) with a checklist and the verb list of three frames, "the person lists the
notes" (notes.list), "lists a checklist" (notes.show) and "lists the checklists" (notes.browse), where r1 reads by
the last frame alone (r13) or gives archive a plural object, "every note", which is no reading (r14); and
codified2_world's glossary with a verb of no operation, list, whose frames "agent lists stage" and "agent lists the
stages" both read r1, the third frame "agent lists file" read by neither (r16). The Then that the requirement has the
ambiguous text: its words are in r1's line."""
import importlib.util
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
C2 = _sibling("codified2_world.py", "shop_codified2_world")
W = _sibling("work_queue_world.py", "shop_work_queue_world")
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model"

CHECKLIST = "object checklist\n  relations: holds → note (many)\n\n"
OPERATIONS = ("  operation show(checklist)  outcomes: returned → every note\n"
              "  operation browse()  outcomes: returned → every checklist\n")
TERMS = ("- **checklist** (noun) → object checklist. A list of notes kept together. Plural: checklists.\n"
         "- **list** (verb, action) → operation notes.show. Forms: lists, listed. Frame: <actor> lists <checklist>.\n"
         "- **list** (verb, action) → operation notes.browse. Forms: lists, listed. Frame: <actor> lists the "
         "checklists.\n")
BROWSING = "When the person lists the checklists, the notes service shall return every checklist."
PLURAL = "When the person archives every note, the notes service shall complete the request."

LISTING = ("- **list** (verb, action): an agent shows things. Forms: lists, listed. Frame: agent lists stage. "
           "Frame: agent lists the stages. Frame: agent lists file.\n")
AMBIGUOUS = "When the person lists the stages, `work` shall exit successfully."
FRAMES = {"f3": '"agent lists stage"', "f4": '"agent lists the stages"', "f5": '"agent lists file"'}


def notes(text):
    """A builder: the domain-model fixture with the checklist and list's frames, and r1 `text` in thing.md."""
    def build(step):
        for part in ("spec/index.md", "spec/model", "spec/vocabulary", "spec/adapters"):
            source, target = FIXTURE / part, step.repo / part
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
        model = step.repo / "spec" / "model" / "notes.md"
        text_ = model.read_text().replace("object tag\n", CHECKLIST + "object tag\n", 1)
        model.write_text(text_.replace("  operation list()", OPERATIONS + "  operation list()", 1))
        vocabulary = step.repo / "spec" / "vocabulary" / "notes.md"
        vocabulary.write_text(vocabulary.read_text() + TERMS)
        body = "### [g1] line 1\n- [r1] %s" % text
        H.write(step.repo, "spec/capabilities/thing.md", (
            "---\nid: capability/example.org/fixture/domain-model/thing\ntitle: thing\nnarrator: the person\n"
            "group: service\narea: notes\nspecifies: service notes\nlanguage: codified-2\nretired: []\n---\n\n"
            "# thing\n\n## Purpose\nSomething.\n\n## Behaviour\n\n%s\n" % body))
    return build


def ambiguous(step):
    """codified2_world's context with list of three frames, r1 read by two of them."""
    C2.context(step.repo, H.PATH, [AMBIGUOUS])
    index = step.repo / "spec" / "index.md"
    index.write_text(index.read_text() + LISTING)
    H.says(step, "a1", "the person lists the stages")


ROWS = [
    (("verb has frame", "requirement use frame", "requirement has logical form"), notes(BROWSING), {}),
    (("requirement has plural object",), notes(PLURAL), {}),
    (("requirement has ambiguous text", "ambiguous text use frame", "ambiguous text not use frame"), ambiguous,
     FRAMES),
]


@W.local("ThenDoes")
def has_ambiguous_text(step):
    """`the requirement r1 has the ambiguous text a1`: the words the refusal named are r1's line's."""
    if not step.nps or not step.nps[0].startswith("the ambiguous text") or step.event != "has":
        return False
    said = step.context.get("says", {}).get(step.names[-1])
    line = next(line for path in sorted((step.repo / "spec" / "capabilities").glob("*.md"))
                for line in path.read_text().splitlines() if line.startswith("- [r1] "))
    assert said and said.lower() in line.lower(), (said, line)
    assert said in step.context["result"].stdout, (said, step.context["result"].stdout)
