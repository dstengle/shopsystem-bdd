"""What migration-tools' step modules share: the repository on the old system a Given builds (`Old`, the `old`
fixture conftest gives), migrate's one run, and model's reading of what it left."""
import pathlib
import subprocess

CONTEXT = "example.org/acme/shop"


class Old:
    """A repository on the old system: files written, committed, and remembered as they were."""

    def __init__(self, root):
        self.root = root
        self.before = {}
        self.git("init", "-q")

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=self.root,
                              capture_output=True, text=True)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
        return p

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "old system")
        self.keep()

    def keep(self):
        """Remember each file as it is, and what git status says (nothing, after a commit)."""
        self.before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                       for p in self.root.rglob("*") if p.is_file() and ".git" not in p.relative_to(self.root).parts}
        self.status = self.git("status", "--porcelain").stdout

    def untracked(self, rel, text):
        """A file written after the commit and never added."""
        self.write(rel, text)
        self.keep()

    def read(self, rel):
        return (self.root / rel).read_text()


def migrate(run, old, context, root=None):
    context["done"] = run("migrate", "run", "--context", CONTEXT, cwd=root or old.root)


def load_model():
    """scripts/model, read by path: its own reading of frontmatter."""
    import importlib.machinery
    import importlib.util
    SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
    loader = importlib.machinery.SourceFileLoader("model_by_path", str(SCRIPTS / "model"))
    spec = importlib.util.spec_from_loader("model_by_path", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def front(old, rel):
    data, body = load_model().frontmatter(old.read(rel))
    return data, body


def capability(old, ident=None, retired="[]", lines=("- [r1] **When** a, `thing` shall a.",)):
    head = "id: %s\n" % ident if ident else ""
    old.write("spec/capabilities/thing.md", "---\n%stitle: thing\nnarrator: a client\ngroup: service\nrests_on: []\nretired: %s\n---\n\n"
              "# thing\n\n## Purpose\nSomething.\n\n## Behaviour\n%s\n\n## Not yet\n- None.\n" % (head, retired, "\n".join(lines)))


def said(context):
    done = context["done"]
    return done.stdout + done.stderr
