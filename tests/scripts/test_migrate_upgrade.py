"""`migrate upgrade` on repositories the scenarios do not build: the move check (migration-tools r7)."""
import atexit
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from typing import ClassVar
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))
import migrate_upgrade

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


class TheStaging(unittest.TestCase):
    def setUp(self):
        self.root = repository({"spec/index.md": INDEX})

    def test_apply_stages_every_text_with_one_add_per_batch(self):
        calls = []
        changes = types.SimpleNamespace(moves=[], texts={"f%04d.md" % i: "x\n" for i in range(1201)})
        with mock.patch.object(migrate_upgrade, "git", side_effect=lambda root, *a: calls.append(a)):
            migrate_upgrade.apply(self.root, changes)
        adds = [c for c in calls if c[0] == "add"]
        self.assertEqual([len(c) - 3 for c in adds], [500, 500, 201])
        self.assertTrue(all(c[:3] == ("add", "-f", "--") for c in adds))
        self.assertEqual(sorted(p for c in adds for p in c[3:]), sorted(changes.texts))

    def test_apply_on_a_real_repository_stages_every_text(self):
        texts = {"a.md": "a\n", "spec/index.md": INDEX + "more\n", "b.md": "b\n"}
        migrate_upgrade.apply(self.root, types.SimpleNamespace(moves=[], texts=texts))
        staged = subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=self.root, capture_output=True,
                                text=True).stdout.split()
        self.assertEqual(sorted(staged), ["a.md", "b.md", "spec/index.md"])


class ALargeNoteList(unittest.TestCase):
    """The upgrade's commit message is passed on stdin: notes over Linux's 128 KB limit for one argument (b240 review)."""

    def test_notes_over_one_arguments_limit_are_committed(self):
        root = repository({"spec/index.md": INDEX, ".shop/plugin-version": "0.32.1\n"})
        notes = ["spec/capabilities/x.md r%d: a note of some length to make the message large enough" % i
                 for i in range(3000)]
        step = types.SimpleNamespace(plan=lambda _root: types.SimpleNamespace(failures=[], moves=[], texts={}, notes=notes))
        with mock.patch.object(migrate_upgrade, "pending", return_value=[("0.33.0", "big", "notes", step)]), \
                mock.patch.object(migrate_upgrade.shop_files, "pushed"), mock.patch("builtins.print"):
            self.assertEqual(migrate_upgrade.upgrade(root), 0)
        message = subprocess.run(["git", "log", "-1", "--format=%B"], cwd=root, capture_output=True,
                                 text=True).stdout
        self.assertGreater(len(message.encode()), 128 * 1024)
        self.assertIn(notes[-1], message)


class NoIdentity(unittest.TestCase):
    """With no git identity to commit with, `migrate upgrade` refuses before it plans a step (plan-9 review M1)."""

    def test_no_identity_is_refused_before_any_step_naming_git_config(self):
        root = repository({"spec/index.md": INDEX, ".shop/plugin-version": "0.30.0\n", ".shop/work/README.md": "q\n"})
        subprocess.run(["git", "config", "--unset", "user.name"], cwd=root, check=True)
        subprocess.run(["git", "config", "--unset", "user.email"], cwd=root, check=True)
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "EMAIL"}
        env.update(HOME=str(root / ".git" / "home"), XDG_CONFIG_HOME=str(root / ".git" / "home"),
                   GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="user.useConfigOnly",
                   GIT_CONFIG_VALUE_0="true")
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True).stdout
        done = subprocess.run([sys.executable, str(SCRIPTS / "migrate"), "upgrade"], cwd=root, capture_output=True,
                              text=True, env=env)
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertEqual(done.stderr.strip(), 'migrate changed nothing; git has no identity to commit with: set one '
                                              'with git config user.name "…" and git config user.email "…"')
        self.assertEqual(status_of(root), "")
        self.assertFalse((root / ".shop/work/FROZEN.md").exists())
        self.assertEqual(subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True,
                                        text=True).stdout, head)


if __name__ == "__main__":
    unittest.main()
