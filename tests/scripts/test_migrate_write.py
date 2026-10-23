"""migrate's writing, all or none: a failure part way puts the repository back (migration-tools r7), and a file that
is not UTF-8 but names a moved path is a change it cannot make."""
import atexit
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import migrate_write as writing
from migrate_layout import Plan, plan_ids, plan_moves
from migrate_ledger import plan_ledger
from migrate_spec import plan_references


def repository(files):
    root = Path(tempfile.mkdtemp())
    atexit.register(shutil.rmtree, root, True)
    for rel, data in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(data)
    git = lambda *a: subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *a], cwd=root, check=True,
                                    capture_output=True)
    git("init", "-q")
    git("add", "-A")
    git("commit", "-q", "-m", "old")
    return root


def snapshot(root):
    return {p.relative_to(root).as_posix(): (p.read_bytes() if p.is_file() else None)
            for p in root.rglob("*") if ".git" not in p.relative_to(root).parts}


def planned(root):
    plan = Plan(root, "example.org/acme/shop")
    plan_moves(plan)
    plan_ledger(plan)
    plan_ids(plan)
    plan_references(plan)
    writing.check_moves(plan)
    return plan


class AFailurePartWayPutsTheRepositoryBack(unittest.TestCase):
    def test_a_git_add_that_fails_after_the_moves_leaves_the_tree_as_it_was(self):
        root = repository({"work/i1/w1.md": b"Work one.\n", "README.md": b"See work/i1/w1.md.\n",
                           "spec/decisions.md": b"## decision/0007-a\nWe do a.\n\ndate: 2025-03-01\nsource: alice\n"})
        before, status = snapshot(root), writing.git(root, "status", "--porcelain").stdout
        plan = planned(root)
        self.assertEqual(plan.failures, [])
        real = writing.git

        def failing(at, *args):
            if args[0] == "add" and args[-1] == "spec/decisions/0007-a.md":
                raise subprocess.CalledProcessError(1, ["git", *args], stderr="fatal: refused")
            return real(at, *args)
        writing.git = failing
        try:
            with self.assertRaises(writing.Failed) as raised:
                writing.write(plan)
        finally:
            writing.git = real
        self.assertIn("refused", str(raised.exception))
        self.assertEqual(snapshot(root), before)
        self.assertEqual(writing.git(root, "status", "--porcelain").stdout, status)


class AFileThatIsNotUtf8(unittest.TestCase):
    def test_one_that_names_a_moved_path_is_a_change_migrate_cannot_make(self):
        root = repository({"work/i1/w1.md": b"Work one.\n", "notes.txt": b"\xff\xfe see work/i1/w1.md\n"})
        plan = planned(root)
        self.assertEqual(plan.failures, ["could not rewrite work/i1/w1.md in notes.txt: it is not UTF-8 text"])

    def test_one_that_names_nothing_moved_is_left_as_it_is(self):
        root = repository({"work/i1/w1.md": b"Work one.\n", "img.bin": b"\xff\xfe\x00 nothing here\n"})
        self.assertEqual(planned(root).failures, [])


if __name__ == "__main__":
    unittest.main()
