"""The 2.0.0 upgrade step "the workflow simplified" (plan 9, D13; migration-tools g24): `.shop/work/` frozen with
`FROZEN.md`, a peer's open request moved to `.shop/requests/`, the decisions index rewritten, and every open
initiative, unapplied proposal, internal request and moved request named; nothing is deleted, and a collision changes
nothing. A 0.29 repository reaches 2.0.0 through the 1.0.0 step in the same commit (D23)."""
import contextlib
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests" / "scripts"))

import migrate_upgrade
import migrate_upgrade_simplified as step
import model_report
from request_testing import hosted
from test_migrate_upgrade_codified import git, repository

INDEX = (ROOT / "tests/scripts/fixtures/glossary/spec/index.md").read_text()
CTX = "example.org/fixture/glossary"
PEER = "bounded-context/example.org/acme/web"
LINE = "While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall set the status of the initiative to `started`."
CART = ("---\nid: capability/%s/cart\ntitle: Cart\ngroup: service\nlanguage: codified-1\nretired: []\n---\n\n# Cart\n\n"
        "## Behaviour\n\n### [g1] a start\n- [r1] %s\n\n## Dropped\n" % (CTX, LINE))
DECISION = ("---\nid: design-decision/%s/one\nsummary: One.\ndate: 2026-01-01\nstatus: accepted\ntier: judgement\n---\n"
            "\n# One\n\n## Decision\nOne.\n" % CTX)
OBSERVATIONS = "".join("## observation/%s/%s\nabout: bounded-context/%s\nby: the person\ndate: 2026-01-01\n\n%s.\n\n"
                       % (CTX, o, CTX, o) for o in ("o1", "o2"))


def request(n, asker, status):
    return ("---\nid: request/%s/q%d\nkind: request\nasker: %s\nsource: [observation/%s/o2]\nstatus: %s\n"
            "turn: upstream\n---\n\n# Request %d\n\n## Lines\n1. %s\n" % (CTX, n, asker, CTX, status, n, LINE))


FILES = {
    ".shop/plugin-version": "1.0.0\n", "spec/index.md": INDEX, "spec/capabilities/cart.md": CART,
    "features/cart.feature": "Feature: Cart\n", "spec/decisions/0001-one.md": DECISION,
    "spec/decisions/index.md": "# Decisions\n\n| decision | summary | status |\n|---|---|---|\n",
    ".shop/records/observations.md": "# Observations\n\n" + OBSERVATIONS,
    ".shop/work/README.md": "The queue.\n",
    ".shop/work/i1/initiative.md": ("---\nid: initiative/%s/i1\nkind: initiative\ntitle: A cart\nstatus: started\n"
                                    "source: [observation/%s/o1]\n---\n\n# i1\n" % (CTX, CTX)),
    ".shop/work/i1/w1.md": "---\nid: work-item/%s/w1\nkind: work-item\nstatus: drafted\n---\n\n# w1\n" % CTX,
    ".shop/work/i1/cart-proposal.md": "---\nkind: capability-proposal\nstatus: drafted\n---\n\n# cart\n",
    ".shop/work/i2/initiative.md": "---\nid: initiative/%s/i2\nkind: initiative\ntitle: Done\nstatus: done\n---\n" % CTX,
    ".shop/work/requests/q1.md": request(1, "internal", "open"),
    ".shop/work/requests/q2.md": request(2, PEER, "open"),
    ".shop/work/requests/q3.md": request(3, PEER, "delivered"),
    ".shop/work/requests/q4.md": request(4, "product/example.org/acme", "accepted"),
    "conftest.py": 'pytest_plugins = ["work_items"]\n',
}


def upgraded(root):
    """`migrate upgrade` run in-process by a plugin on 2.0.0: (exit code, what it printed)."""
    out, err = io.StringIO(), io.StringIO()
    real = migrate_upgrade.plugin_version
    migrate_upgrade.plugin_version = lambda: "2.0.0"
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), contextlib.chdir(root):
            code = migrate_upgrade.run("upgrade")
    finally:
        migrate_upgrade.plugin_version = real
    return code, out.getvalue() + err.getvalue()


def script(root, name, *args, env=None):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / name), "--root", str(root), *args],
                          capture_output=True, text=True, env=env)


class AQueuedRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = repository(FILES)
        cls.before = git(cls.root, "rev-parse", "HEAD").strip()
        cls.code, cls.said = upgraded(cls.root)
        cls.message = git(cls.root, "log", "-1", "--format=%B")

    def test_one_commit_freezes_the_queue(self):
        self.assertEqual(self.code, 0, self.said)
        self.assertEqual(git(self.root, "rev-parse", "HEAD~1").strip(), self.before)
        self.assertTrue(self.message.startswith("migrate upgrade: 1.0.0 to 2.0.0\n"), self.message)
        self.assertIn('upgrade step 2.0.0 "the workflow simplified"', self.message)
        self.assertEqual((self.root / ".shop/plugin-version").read_text(), "2.0.0\n")
        self.assertEqual((self.root / ".shop/work/FROZEN.md").read_text(), step.FROZEN_TEXT)
        self.assertEqual(git(self.root, "status", "--porcelain"), "")

    def test_nothing_under_shop_work_changes_but_the_marker_and_the_moved_requests(self):
        changed = git(self.root, "diff", "-M100%", "--name-status", "HEAD~1", "--", ".shop/work", ".shop/requests")
        self.assertEqual(sorted(changed.splitlines()), [
            "A\t.shop/work/FROZEN.md",
            "R100\t.shop/work/requests/q2.md\t.shop/requests/q2.md",
            "R100\t.shop/work/requests/q4.md\t.shop/requests/q4.md"])

    def test_a_peers_open_request_moves_and_an_internal_one_stays(self):
        for n in (2, 4):
            self.assertEqual((self.root / (".shop/requests/q%d.md" % n)).read_text(), FILES[".shop/work/requests/q%d.md" % n])
            self.assertFalse((self.root / (".shop/work/requests/q%d.md" % n)).exists())
        for n in (1, 3):
            self.assertEqual((self.root / (".shop/work/requests/q%d.md" % n)).read_text(), FILES[".shop/work/requests/q%d.md" % n])
            self.assertFalse((self.root / (".shop/requests/q%d.md" % n)).exists())

    def test_the_decisions_index_is_rewritten(self):
        self.assertEqual((self.root / "spec/decisions/index.md").read_text(), model_report.render_decisions(self.root))
        self.assertIn("| tier |", (self.root / "spec/decisions/index.md").read_text())
        checked = script(self.root, "model", "decisions", "--check")
        self.assertIn("is current", checked.stdout + checked.stderr)

    def test_every_open_thing_is_named_in_the_notes(self):
        for text in (self.said, self.message):
            for want in ('open initiative i1 "A cart"', "cart-proposal.md", 'internal request q1 "Request 1"',
                         "moved request q2", "moved request q4"):
                self.assertIn(want, text)
            self.assertNotIn("i2", text)
            self.assertNotIn("q3", text)

    def test_no_file_is_deleted(self):
        self.assertEqual(git(self.root, "diff", "-M100%", "--diff-filter=D", "--name-only", "HEAD~1"), "")

    def test_the_upgraded_repository_is_on_the_new_workflow(self):
        report = json.loads(script(self.root, "model", "check", "--json").stdout)
        under = [str(x) for x in report["violations"] + report["warnings"] + report["unresolved"] if ".shop/work" in str(x)]
        self.assertEqual(under, [])
        self.assertNotIn("observation/%s/o1" % CTX, json.dumps(report["warnings"]))
        listed = script(self.root, "work", "list").stdout
        self.assertIn("q2", listed)
        self.assertIn("q4", listed)
        self.assertNotIn("q1", listed)
        env = hosted(self.root, self.root.parent / (self.root.name + "-gh"))
        asked = script(self.root, "work", "request", "x", "--from", "internal", "--source", "observation/%s/o1" % CTX,
                       env=env)
        self.assertEqual(asked.returncode, 0, asked.stdout + asked.stderr)
        self.assertTrue((self.root / ".shop/requests/q5.md").is_file())
        self.assertEqual(upgraded(self.root), (0, "no upgrade step is pending\n"))


class ARefusal(unittest.TestCase):
    def test_a_request_already_in_shop_requests_refuses_and_changes_nothing(self):
        root = repository(dict(FILES, **{".shop/requests/q2.md": "a request already here\n"}))
        head = git(root, "rev-parse", "HEAD")
        code, said = upgraded(root)
        self.assertEqual(code, 1, said)
        self.assertIn("could not move", said)
        self.assertEqual(git(root, "rev-parse", "HEAD"), head)
        self.assertEqual(git(root, "status", "--porcelain"), "")

    def test_a_request_whose_frontmatter_does_not_read_refuses(self):
        root = repository(dict(FILES, **{".shop/work/requests/q5.md": "no frontmatter\n"}))
        code, said = upgraded(root)
        self.assertEqual(code, 1, said)
        self.assertIn(".shop/work/requests/q5.md", said)
        self.assertEqual(git(root, "status", "--porcelain"), "")


class OtherRepositories(unittest.TestCase):
    def test_a_repository_with_no_work_gets_only_the_index(self):
        root = repository({k: v for k, v in FILES.items() if not k.startswith(".shop/work/")})
        code, said = upgraded(root)
        self.assertEqual(code, 0, said)
        self.assertFalse((root / ".shop/work/FROZEN.md").exists())
        self.assertEqual(sorted(git(root, "diff", "--name-only", "HEAD~1").split()),
                         [".shop/plugin-version", "spec/decisions/index.md"])

    def test_a_0_29_repository_reaches_2_0_in_one_commit(self):
        root = repository({
            ".shop/plugin-version": "0.29.0\n",
            "spec/index.md": "---\nid: bounded-context/example.org/acme/shop\ntitle: shop\n---\n# shop\n",
            "spec/capabilities/cart.md": ("---\nid: capability/example.org/acme/shop/cart\ntitle: Cart\nretired: []\n"
                                          "---\n# Cart\n## Behaviour\n- [r1] **When** the shopper applies a code, "
                                          "`cart` shall take ten percent off.\n"),
            "features/cart.feature": "Feature: Cart\n  @r1 @deprecated\n  Scenario: a code (deprecated)\n    Given a cart\n",
            ".shop/work/i1/w2.md": "---\nid: work-item/example.org/acme/shop/w2\nkind: work-item\naccepts: [cart#r1]\n---\n# w2\n",
            ".shop/work/i1/cart.md": "---\nkind: capability-proposal\nstatus: awaiting-answer\n---\n# cart\n"})
        code, said = upgraded(root)
        self.assertEqual(code, 0, said)
        # the 2.0.0 step names the proposal; the 1.0.0 step's "left for a session to write" of it would contradict
        # FROZEN.md (plan-9 review S5)
        message = git(root, "log", "-1", "--format=%B")
        for text in (said, message):
            self.assertIn("the lines of proposal .shop/work/i1/cart.md were never applied", text)
            self.assertNotIn("left for a session to write: .shop/work/", text)
        self.assertEqual(git(root, "rev-list", "--count", "HEAD").strip(), "2")
        self.assertIn("migrate upgrade: 0.29.0 to 2.0.0", git(root, "log", "-1", "--format=%B"))
        self.assertTrue((root / "spec/restated.json").is_file())
        self.assertIn("Restates: r1@0.29.", (root / "spec/capabilities/cart.md").read_text())
        self.assertEqual((root / ".shop/work/FROZEN.md").read_text(), step.FROZEN_TEXT)
        self.assertEqual((root / ".shop/plugin-version").read_text(), "2.0.0\n")
        self.assertIn("accepts: [cart#r1@0.29]", (root / ".shop/work/i1/w2.md").read_text())


if __name__ == "__main__":
    unittest.main()
