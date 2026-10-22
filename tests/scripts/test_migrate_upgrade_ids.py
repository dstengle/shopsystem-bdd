"""The upgrade step "work-items named by ids" on repositories the scenarios do not build (migration-tools r19, r25, r26)."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def repository(files):
    root = Path(tempfile.mkdtemp())
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


if __name__ == "__main__":
    unittest.main()
