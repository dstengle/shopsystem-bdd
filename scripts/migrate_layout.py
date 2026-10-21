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
        self.crlf = set()       # each file read whose lines end in CRLF, which keep them when it is written

    def linked(self, rel):
        """Whether `rel`, or a directory on the way to it, is a symbolic link: what it points to is not the
        repository's text, and may be outside the repository (r5, r7)."""
        parts = Path(rel).parts
        return any((self.root / Path(*parts[:i])).is_symlink() for i in range(1, len(parts) + 1))

    def read(self, rel):
        """The text of `rel`, its lines ending in LF; a symbolic link is a change migrate cannot make, read as empty."""
        if self.linked(rel):
            self.failures.append("could not change %s: it is a symbolic link" % rel)
            return ""
        raw = (self.root / rel).read_bytes()
        text = raw.decode()
        if b"\r\n" in raw:
            self.crlf.add(rel)
        return text.replace("\r\n", "\n").replace("\r", "\n")


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


def reid(plan, text, ident, **given):
    """`text` with the id `ident`: given one where it has none (`with_id`), and in place of an id in another form, the
    old id then renamed so that what names it follows (r4, r9, r5)."""
    if text.startswith("---\n") and text.find("\n---", 4) > 0:
        head = text[4:text.find("\n---", 4)]
        m = re.search(r"^id:[ \t]*(.*?)[ \t]*$", head, re.MULTILINE)
        if m and m.group(1) != ident:
            plan.renamed[m.group(1)] = ident
            return "---\n" + head[:m.start()] + "id: " + ident + head[m.end():] + text[4 + len(head):]
    return with_id(text, ident, **given)


def record_kind(final):
    """The kind of a moved record that gets an id: a Markdown plan, design note or test log; None for any other."""
    if not final.endswith(".md") or Path(final).name == "README.md":      # a README is not a record (r9)
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
        elif final.startswith("spec/decisions/") and final.endswith(".md") and Path(final).name != "README.md":
            name = re.sub(r"^\d+-", "", stem(final))
            plan.texts[final] = reid(plan, text(), "design-decision/%s/%s" % (plan.context, name))


def load_model():
    """scripts/model, read by path: migrate reads frontmatter the way model does."""
    import importlib.machinery
    import importlib.util
    path = str(Path(__file__).resolve().with_name("model"))
    loader = importlib.machinery.SourceFileLoader("model_by_path", path)
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader("model_by_path", loader))
    loader.exec_module(module)
    return module
