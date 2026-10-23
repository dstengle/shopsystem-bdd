"""`migrate upgrade` and `migrate status` on repositories the scenarios do not build: the move check, and a version
file that holds no version (migration-tools r7, r18, r22)."""
import atexit
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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
    base = {"spec/index.md": INDEX, ".shop/work/i1-x/a.md": item("a"), ".shop/work/i1-x/runs/a/f": "f\n"}

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


class AVersionFileThatHoldsNoVersion(unittest.TestCase):
    def repo(self, text):
        return repository({"spec/index.md": INDEX, ".shop/plugin-version": text, ".shop/work/i1-x/a.md": item("a")})

    def test_status_prints_nothing_and_says_on_stderr_what_the_file_holds(self):
        for text, held in (("next\n", "next"), ("", "nothing")):
            with self.subTest(text=text):
                done = migrate(self.repo(text), "status")
                self.assertEqual((done.returncode, done.stdout), (1, ""))
                self.assertIn(".shop/plugin-version", done.stderr)
                self.assertIn(held, done.stderr)
                self.assertNotIn("Traceback", done.stderr)

    def test_upgrade_refuses_in_the_same_words_and_changes_nothing(self):
        for text, held in (("next\n", "next"), ("", "nothing")):
            with self.subTest(text=text):
                root = self.repo(text)
                done = migrate(root, "upgrade")
                self.assertEqual(done.returncode, 1)
                self.assertIn(".shop/plugin-version", done.stderr)
                self.assertIn(held, done.stderr)
                self.assertNotIn("Traceback", done.stderr)
                self.assertEqual(status_of(root), "")

    def test_the_hook_exits_0_and_prints_one_line_telling_the_session_to_tell_the_person(self):
        for text, held in (("next\n", "next"), ("", "nothing")):
            with self.subTest(text=text):
                done = migrate(self.repo(text), "status", "--hook")
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(len(done.stdout.strip().splitlines()), 1)
                self.assertIn(".shop/plugin-version", done.stdout)
                self.assertIn(held, done.stdout)
                self.assertIn("tell the person", done.stdout)


if __name__ == "__main__":
    unittest.main()
