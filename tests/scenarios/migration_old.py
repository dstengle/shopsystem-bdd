"""The repository `migrate` runs in, for migration-tools' handlers (`Old`, also the `old` fixture conftest gives):
files written, committed, and remembered as they were; and the plugin `migrate` runs from (`plugin`)."""
import atexit
import json
import pathlib
import shutil
import subprocess
import tempfile

CONTEXT = "example.org/acme/shop"
PLUGIN = pathlib.Path(__file__).resolve().parents[2]
TARGET = "0.31.0"     # the release migration-tools' scenarios describe
_copy = {}


def number(version):
    return tuple(int(p) for p in version.split("."))


def plugin():
    """(root, version) of the plugin the scenarios run: this one, or, while its version is below TARGET, a copy of its
    scripts and hooks whose plugin.json says TARGET, made once."""
    data = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
    if number(data["version"]) >= number(TARGET):
        return PLUGIN, data["version"]
    if not _copy:
        root = pathlib.Path(tempfile.mkdtemp())
        atexit.register(shutil.rmtree, root, True)
        for part in ("scripts", "hooks"):
            shutil.copytree(PLUGIN / part, root / part, ignore=shutil.ignore_patterns("__pycache__"))
        (root / ".claude-plugin").mkdir()
        (root / ".claude-plugin/plugin.json").write_text(json.dumps(dict(data, version=TARGET), indent=2) + "\n")
        _copy["root"] = root
    return _copy["root"], TARGET


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


