"""The world of two terms of one element (consistency r35, b544), a row design_model_check_worlds' TABLE takes first:
the domain-model fixture (tests/scripts/fixtures/domain-model/) with a second proper noun of the actor the person,
"the owner", in the notes layer (`spec/vocabulary/notes.md`) beside the shared layer's "the person", r1 obliging an
act on the request of the person and r2 forbidding it on the request of the owner, which clash as lines on one
thing (an L1)."""
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
FIXTURE = Path(__file__).resolve().parents[1] / "scripts" / "fixtures" / "domain-model"

OWNER = "- **the owner** (proper noun) → actor the person. The one whose notes they are.\n"
OBLIGING = "When the person adds a note, the notes service shall file the note."
FORBIDDING = "When the owner adds a note, the notes service shall not file the note."


def aliased(step):
    """The domain-model fixture, the owner a second term of the person, and r1, r2 in thing.md."""
    for part in ("spec/index.md", "spec/model", "spec/vocabulary"):
        source, target = FIXTURE / part, step.repo / part
        if source.is_dir():
            shutil.copytree(source, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    vocabulary = step.repo / "spec" / "vocabulary" / "notes.md"
    vocabulary.write_text(vocabulary.read_text() + OWNER)
    body = "\n\n".join("### [g%d] line %d\n- [r%d] %s" % (k, k, k, line)
                       for k, line in enumerate((OBLIGING, FORBIDDING), 1))
    H.write(step.repo, "spec/capabilities/thing.md", (
        "---\nid: capability/example.org/fixture/domain-model/thing\ntitle: thing\nnarrator: the person\n"
        "group: service\narea: notes\nspecifies: service notes\nlanguage: codified-2\nretired: []\n---\n\n"
        "# thing\n\n## Purpose\nSomething.\n\n## Behaviour\n\n%s\n" % body))


ROWS = [
    (("term mean element", "requirement use term", "requirement oblige act", "requirement forbid act"), aliased, {}),
]
