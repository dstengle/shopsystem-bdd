"""The upgrade step "work-items named by ids" on repositories the scenarios do not build (migration-tools r19, r25, r26)."""
import atexit
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def repository(files):
    root = Path(tempfile.mkdtemp())
    atexit.register(shutil.rmtree, root, True)
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    git = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=root, check=True,
                                    capture_output=True)
    git("init", "-q")
    git("config", "user.name", "t")
    git("config", "user.email", "t@t")
    git("add", "-A", "-f")
    git("commit", "-q", "-m", "base")
    return root


def upgrade(root):
    return subprocess.run([sys.executable, str(SCRIPTS / "migrate"), "upgrade"], cwd=root, capture_output=True, text=True)


INDEX = "---\nid: bounded-context/example.org/acme/shop\n---\n# shop\n"


def item(name, extra=""):
    return "---\nkind: work-item\nid: work-item/example.org/acme/shop/%s\n%s---\n\nBody.\n" % (name, extra)


class UpgradeRecordsTheVersion(unittest.TestCase):
    def test_a_repository_with_shop_and_no_work_directory_records_the_version(self):
        root = repository({"spec/index.md": INDEX, ".shop/records/.keep": ""})
        done = upgrade(root)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue((root / ".shop/plugin-version").is_file())

    def test_a_blocked_by_written_as_a_block_list_follows_the_rename(self):
        root = repository({"spec/index.md": INDEX, ".shop/work/i1-x/a.md": item("a"),
                           ".shop/work/i1-x/b.md": item("b", "blocked_by:\n  - work-item/a\n")})
        done = upgrade(root)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("  - work-item/w1\n", (root / ".shop/work/i1-x/w2.md").read_text())


class UpgradeFollowsReferences(unittest.TestCase):
    def test_a_for_written_as_a_block_list_and_a_name_held_only_by_another_initiative_follow_the_rename(self):
        root = repository({"spec/index.md": INDEX, ".shop/work/i1-x/a.md": item("a"),
                           ".shop/work/i2-y/b.md": item("b", "for:\n  - a\nblocked_by: [a]\n")})
        done = upgrade(root)
        self.assertEqual(done.returncode, 0, done.stderr)
        text = (root / ".shop/work/i2-y/w2.md").read_text()
        self.assertIn("  - w1\n", text)
        self.assertIn("blocked_by: [w1]\n", text)

    def test_a_name_held_by_two_other_initiatives_is_refused_and_nothing_changes(self):
        root = repository({"spec/index.md": INDEX, ".shop/work/i1-x/a.md": item("a"), ".shop/work/i2-y/a.md": item("a"),
                           ".shop/work/i3-z/c.md": item("c", "blocked_by: [a]\n")})
        done = upgrade(root)
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("i1-x", done.stderr)
        self.assertIn("i2-y", done.stderr)
        self.assertTrue((root / ".shop/work/i1-x/a.md").is_file())
        self.assertFalse((root / ".shop/plugin-version").exists())

    def test_a_name_that_names_no_work_item_is_left_alone(self):
        root = repository({"spec/index.md": INDEX, ".shop/work/i1-x/a.md": item("a", "for: nothing\n")})
        self.assertEqual(upgrade(root).returncode, 0)
        self.assertIn("for: nothing\n", (root / ".shop/work/i1-x/w1.md").read_text())


class UpgradeHardening(unittest.TestCase):
    def test_an_ambiguous_name_is_refused_once_per_place_naming_the_field(self):
        root = repository({"spec/index.md": INDEX, ".shop/work/i1-x/a.md": item("a"), ".shop/work/i2-y/a.md": item("a"),
                           ".shop/work/i3-z/c.md": item("c", "blocked_by: [a]\nfor: a\n"),
                           ".shop/work/i3-z/d.md": item("d", "depends_on: [a]\n")})
        done = upgrade(root)
        self.assertNotEqual(done.returncode, 0)
        lines = [l for l in done.stderr.splitlines() if "could not rename" in l]
        self.assertEqual(len(lines), len(set(lines)))
        self.assertEqual(len(lines), 3)
        self.assertNotIn("reference", done.stderr)
        for field in ("blocked_by", "depends_on", "for"):
            self.assertEqual(len([l for l in lines if field in l]), 1, lines)

    def test_a_qualified_token_and_a_comment_are_left_alone(self):
        root = repository({"spec/index.md": INDEX, ".shop/work/i1-x/item.md": item("item"),
                           ".shop/work/i1-x/b.md": item("b", "for: item#r26\nblocked_by:\n  - work-item/item # item\n")})
        done = upgrade(root)
        self.assertEqual(done.returncode, 0, done.stderr)
        text = (root / ".shop/work/i1-x/w1.md").read_text()
        self.assertIn("for: item#r26\n", text)
        self.assertIn("  - work-item/w2 # item\n", text)

    def test_an_index_without_an_id_or_without_a_file_is_refused_and_nothing_changes(self):
        for index in ({"spec/index.md": "# shop\n"}, {"README": "x\n"}):
            with self.subTest(index=index):
                root = repository({**index, ".shop/work/i1-x/a.md": item("a")})
                done = upgrade(root)
                self.assertEqual(done.returncode, 1)
                self.assertIn("spec/index.md", done.stderr)
                self.assertIn("bounded-context id", done.stderr)
                self.assertNotIn("Traceback", done.stderr)
                self.assertTrue((root / ".shop/work/i1-x/a.md").is_file())

    def test_initiatives_with_one_number_are_numbered_by_name(self):
        for first, second in (("i1-a", "i1-b"), ("i1-b", "i1-a")):
            with self.subTest(first=first):
                root = repository({"spec/index.md": INDEX, ".shop/work/%s/a.md" % first: item("a"),
                                   ".shop/work/%s/b.md" % second: item("b")})
                self.assertEqual(upgrade(root).returncode, 0)
                self.assertTrue((root / ".shop/work/i1-a/w1.md").is_file())
                self.assertTrue((root / ".shop/work/i1-b/w2.md").is_file())


if __name__ == "__main__":
    unittest.main()
