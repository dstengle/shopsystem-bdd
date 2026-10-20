"""migrate's plan of a run, the moves, the ids of what moved, and the check and write of every change: the part of
`migrate run` that knows the old directories and where they land."""
import re
import subprocess
from pathlib import Path

# directory of the old system -> where it lands
DIRECTORY_MOVES = (
    ("decisions/", "spec/decisions/"),
    ("work/", ".shop/work/"),
    ("docs/superpowers/plans/", ".shop/records/archive/plans/"),
    ("docs/superpowers/specs/", ".shop/records/archive/design-notes/"),
    ("docs/superpowers/requests/", ".shop/records/archive/requests/"),
    ("adrs/", ".shop/records/decision-arguments/"),
    ("records/", ".shop/records/"),
)


class Plan:
    """What a run will do: files moved, texts written (new files), files removed."""

    def __init__(self, root, context):
        self.root, self.context = root, context
        self.moves = {}
        self.texts = {}
        self.removes = []
        self.failures = []      # each change that cannot be made
        self.renamed = {}       # an old id -> its new id
        self.created = {}       # a new file -> what it is written for

    def read(self, rel):
        return (self.root / rel).read_text()


def tracked(root):
    out = subprocess.run(["git", "ls-files", "-z"], cwd=root, capture_output=True, text=True, check=True).stdout
    return [p for p in out.split("\0") if p]


def destination(path):
    for old, new in DIRECTORY_MOVES:
        if path.startswith(old):
            return new + path[len(old):]
    return None


def plan_moves(plan):
    for path in tracked(plan.root):
        target = destination(path)
        if target is not None:
            plan.moves[path] = target


def with_id(text, ident, kind=None, about=None):
    """`text` with `id: <ident>` (and `kind: <kind>`, and `about: <about>` where it has no about) first in its
    frontmatter, one is added when it has none; unchanged if it has an id."""
    given = "id: %s\n" % ident + ("kind: %s\n" % kind if kind else "")
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end > 0:
            if re.search(r"^id:", text[4:end], re.MULTILINE):
                return text
            if about and not re.search(r"^about:", text[4:end], re.MULTILINE):
                given += "about: %s\n" % about
            return "---\n" + given + text[4:]
    return "---\n" + given + ("about: %s\n" % about if about else "") + "---\n" + text


def record_kind(final):
    """The kind of a moved record that gets an id: a Markdown plan, design note or test log; None for any other."""
    if not final.endswith(".md"):
        return None
    if final.startswith((".shop/records/archive/plans/", ".shop/records/archive/requests/")):
        return "initiative-archive"
    if final.startswith((".shop/records/archive/design-notes/", ".shop/records/decision-arguments/")):
        return "decision-argument"
    if final.endswith("-test-log.md") and final.startswith(".shop/records/"):
        return "measurement"
    return None


def plan_ids(plan):
    """Give each moved plan, design note, test log and decision file the id of its kind."""
    stem = lambda rel: Path(rel).stem
    for old, final in plan.moves.items():
        text = lambda: plan.texts.get(final) or plan.read(old)     # read only a file that gets an id: a moved image is not
        kind = record_kind(final)
        if kind:
            plan.texts[final] = with_id(text(), "%s/%s/%s" % (kind, plan.context, stem(final)), kind,
                                        "bounded-context/" + plan.context)      # r12
        elif final.startswith("spec/decisions/") and final.endswith(".md"):
            name = re.sub(r"^\d+-", "", stem(final))
            plan.texts[final] = with_id(text(), "design-decision/%s/%s" % (plan.context, name))


def load_model():
    """scripts/model, read by path: migrate reads frontmatter the way model does."""
    import importlib.machinery
    import importlib.util
    path = str(Path(__file__).resolve().with_name("model"))
    loader = importlib.machinery.SourceFileLoader("model_by_path", path)
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader("model_by_path", loader))
    loader.exec_module(module)
    return module


def check_moves(plan):
    """Name each move that cannot be made: onto a file that exists, tracked or not, or two sources to one destination;
    and each new file that cannot be written: where a file is, or where a file moves."""
    present = set(tracked(plan.root)) - set(plan.moves)
    by_destination = {}
    for old, new in plan.moves.items():
        by_destination.setdefault(new, []).append(old)
    for new, sources in by_destination.items():
        if len(sources) > 1:
            plan.failures.append("could not move both %s to %s" % (" and ".join(sources), new))
        elif new in present or (new not in plan.moves and (plan.root / new).exists()):
            plan.failures.append("could not move %s onto %s" % (sources[0], new))
    for new, purpose in plan.created.items():
        if new in by_destination:
            plan.failures.append("could not write %s for %s: %s moves there" % (new, purpose, " and ".join(by_destination[new])))
        elif new in present or (new not in plan.moves and (plan.root / new).exists()):
            plan.failures.append("could not write %s for %s: a file is there" % (new, purpose))


def write(plan):
    root = plan.root
    for old, new in plan.moves.items():
        (root / new).parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "mv", old, new], cwd=root, capture_output=True, text=True, check=True)
    for old in plan.moves:
        parent = (root / old).parent
        while parent != root and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent
    for rel in plan.removes:
        subprocess.run(["git", "rm", "-q", rel], cwd=root, capture_output=True, text=True, check=True)
    for rel, text in plan.texts.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
        subprocess.run(["git", "add", "--", rel], cwd=root, capture_output=True, text=True, check=True)


def write_decisions_index(plan):
    """spec/decisions/index.md as `model decisions` writes it from the decision files now on disk, added to git."""
    target = plan.root / "spec/decisions/index.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(load_model().render_decisions(plan.root))
    subprocess.run(["git", "add", "--", "spec/decisions/index.md"], cwd=plan.root, capture_output=True, text=True, check=True)


def uncommitted(root):
    """Each path git status shows as changed or untracked (an ignored file is not shown)."""
    out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root, capture_output=True,
                         text=True, check=True).stdout
    return [line[3:] for line in out.splitlines()]
