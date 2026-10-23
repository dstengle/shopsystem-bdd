"""`migrate upgrade` on repositories the scenarios do not build: the move check (migration-tools r7)."""
import atexit
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import ClassVar

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
INDEX = "---\nid: bounded-context/example.org/acme/shop\n---\n# shop\n"


def item(name):
    return "---\nkind: work-item\nid: work-item/example.org/acme/shop/%s\n---\n\nBody.\n" % name


def repository(files, later=None):
    root = Path(tempfile.mkdtemp())
    atexit.register(shutil.rmtree, root, True)
    git = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=root, check=True,
                                    capture_output=True)
    git("init", "-q")
    git("config", "user.name", "t")
    git("config", "user.email", "t@t")
    for batch, tracked in ((files, True), (later or {}, False)):
        for rel, text in batch.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text)
        if tracked:
            git("add", "-A", "-f")
            git("commit", "-q", "-m", "base")
    return root


def migrate(root, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / "migrate"), *args], cwd=root, capture_output=True, text=True)


def status_of(root):
    return subprocess.run(["git", "status", "--porcelain"], cwd=root, capture_output=True, text=True).stdout


class TheMoveCheck(unittest.TestCase):
    base: ClassVar[dict] = {"spec/index.md": INDEX, ".shop/work/i1-x/a.md": item("a"), ".shop/work/i1-x/runs/a/f": "f\n"}

    def test_a_run_directory_moved_onto_a_tracked_one_is_refused_and_nothing_changes(self):
        root = repository({**self.base, ".shop/work/i1-x/runs/w1/y": "y\n"})
        done = migrate(root, "upgrade")
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertIn("could not move .shop/work/i1-x/runs/a onto .shop/work/i1-x/runs/w1", done.stderr)
        self.assertEqual(status_of(root), "")

    def test_a_run_directory_moved_onto_an_ignored_one_is_refused_and_nothing_changes(self):
        root = repository({**self.base, ".gitignore": "**/runs/w1\n"}, later={".shop/work/i1-x/runs/w1/y": "y\n"})
        done = migrate(root, "upgrade")
        self.assertEqual(done.returncode, 1, done.stderr)
        self.assertIn("could not move .shop/work/i1-x/runs/a onto .shop/work/i1-x/runs/w1", done.stderr)
        self.assertEqual(status_of(root), "")


if __name__ == "__main__":
    unittest.main()
