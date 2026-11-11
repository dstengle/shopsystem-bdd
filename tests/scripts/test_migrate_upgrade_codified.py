"""The 0.30.0 upgrade step "codified requirements" (the GF conversion's design §13.4, §15; migration-tools g29):
`spec/restated.json` written when missing, each uncodified capability's Behaviour scaffolded, `@deprecated` scenarios
deleted, the 0.29 references of `.shop/work/**` written `<cap>#r<n>@0.29`, and what is left for a session reported."""
import atexit
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import migrate_upgrade
import migrate_upgrade_codified as step

FROZEN = "96818f71"
CTX = "example.org/acme/shop"
INDEX = "---\nid: bounded-context/%s\ntitle: shop\n---\n# shop\n\n## Glossary\n- **cart**: a basket.\n" % CTX
CART = """---
id: capability/%s/cart
title: Cart
group: service
retired: [r2]
---

# Cart

## Purpose
A cart.

## Behaviour

### Codes
- [r1] **When** the shopper applies a code, `cart` shall take
  ten percent off.
- [r3] **If** the code is unknown, then `cart` shall say so.

**If** `cart` finds a case of a row below, then `cart` shall print it:

| id | code | what |
|---|---|---|
| [r4] | c1 | an empty cart |

## Not yet
- gift cards.
""" % CTX
CODIFIED = """---
id: capability/%s/till
title: Till
group: service
language: codified-1
retired: []
---

# Till

## Behaviour

### [g1] the till opens
- [r1] When the person runs `till open`, `till` shall exit successfully.

## Dropped
""" % CTX
FEATURE = """Feature: Cart

  @r1
  Scenario: a code takes ten percent off
    Given a cart
    Then ten percent is off

  @r3 @deprecated
  Scenario: an unknown code (deprecated)
    Deprecated for: removal
    Given a cart
    Then it says so

  @r4
  Scenario Outline: a row
    Given <x>

    Examples:
      | x |
      | a |

  @r5
  Scenario: a feature file given as text
    Given the file holds:
      \"\"\"
      @r1 @deprecated
      Scenario: quoted
        Given nothing
      \"\"\"
"""
ITEM = """---
id: work-item/%s/w1
kind: work-item
accepts: [cart#r1, capability/%s/cart#r3-r4, till#r1@0.29, capability/example.org/other/ctx/cart#r9]
for:
  - cart#r3-r4
---
# w1
Delivers cart#r1 and nothing#r2.
""" % (CTX, CTX)

PROPOSAL = "---\nkind: capability-proposal\nstatus: %s\nadds: [cart#r5]\n---\n# cart\n"


def repository(files, later=None):
    root = Path(tempfile.mkdtemp())
    atexit.register(shutil.rmtree, root, True)
    init(root)
    for batch in (files, later):
        if batch is None:
            continue
        for rel, text in batch.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(text)
        git(root, "add", "-A", "-f")
        git(root, "commit", "-q", "-m", "files")
    return root


def init(root):
    git(root, "init", "-q")
    git(root, "config", "user.name", "t")
    git(root, "config", "user.email", "t@t")


def git(root, *args):
    return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", *args], cwd=root, check=True,
                          capture_output=True, text=True).stdout


def upgraded(root):
    """`migrate upgrade` run in-process by a plugin on 0.30.0: (exit code, what it printed)."""
    out, err = io.StringIO(), io.StringIO()
    real = migrate_upgrade.plugin_version
    migrate_upgrade.plugin_version = lambda: "0.30.0"
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err), contextlib.chdir(root):
            code = migrate_upgrade.run("upgrade")
    finally:
        migrate_upgrade.plugin_version = real
    return code, out.getvalue() + err.getvalue()


class TheStepPlan(unittest.TestCase):
    def setUp(self):
        self.root = repository({"spec/index.md": INDEX, "spec/capabilities/cart.md": CART,
                                "spec/capabilities/till.md": CODIFIED, "features/cart.feature": FEATURE,
                                ".shop/plugin-version": "0.29.0\n", ".shop/work/i1/w1.md": ITEM,
                                ".shop/work/i1/open.md": PROPOSAL % "awaiting-answer",
                                ".shop/work/i1/closed.md": PROPOSAL % "merged"})
        self.changes = step.plan(self.root)

    def test_restated_json_holds_each_live_id_of_an_uncodified_capability_with_its_text_and_line(self):
        restated = json.loads(self.changes.texts["spec/restated.json"])
        self.assertEqual(list(restated), ["cart#r1", "cart#r3", "cart#r4"])
        self.assertEqual(restated["cart#r1"], {"text": "**When** the shopper applies a code, `cart` shall take ten "
                                                       "percent off.", "line": 16})
        self.assertEqual(restated["cart#r4"]["text"], "**If** `cart` finds a case of a row below, then `cart` shall "
                                                      "print it: | c1 | an empty cart")
        self.assertEqual(restated["cart#r4"]["line"], 24)

    def test_an_uncodified_capability_gets_one_group_for_each_old_line_with_restates_and_the_old_text(self):
        text = self.changes.texts["spec/capabilities/cart.md"]
        self.assertIn("### [g1] Codes (r1@0.29)\nRestates: r1@0.29.\n<!-- r1@0.29: **When** the shopper", text)
        self.assertIn("### [g3] Codes (r4@0.29)\nRestates: r4@0.29.\n", text)
        self.assertNotIn("- [r", text)
        self.assertNotIn("\nlanguage:", text)
        self.assertIn("retired: []\n", text)
        self.assertIn("## Not yet\n- gift cards.\n", text)
        self.assertTrue(text.rstrip().endswith("## Dropped"), text)

    def test_a_codified_capability_is_skipped(self):
        self.assertNotIn("spec/capabilities/till.md", self.changes.texts)

    def test_a_deprecated_scenario_is_deleted_and_the_others_are_kept(self):
        text = self.changes.texts["features/cart.feature"]
        self.assertNotIn("unknown code", text)
        self.assertIn('      """\n      @r1 @deprecated\n      Scenario: quoted\n        Given nothing\n      """\n', text)
        self.assertIn("  @r1\n  Scenario: a code takes ten percent off\n", text)
        self.assertIn("    Then ten percent is off\n\n  @r4\n  Scenario Outline: a row\n", text)
        self.assertIn("      | a |\n", text)

    def test_old_references_are_written_with_their_release_and_ranges_listed(self):
        text = self.changes.texts[".shop/work/i1/w1.md"]
        self.assertIn("accepts: [cart#r1@0.29, capability/%s/cart#r3@0.29, capability/%s/cart#r4@0.29, "
                      "till#r1@0.29, capability/example.org/other/ctx/cart#r9]" % (CTX, CTX), text)
        self.assertIn("for:\n  - cart#r3@0.29\n  - cart#r4@0.29\n---", text)
        self.assertIn("Delivers cart#r1@0.29 and nothing#r2.", text)

    def test_the_report_names_each_capability_left_and_the_untyped_glossary(self):
        self.assertIn("spec/capabilities/cart.md", "\n".join(self.changes.notes))
        self.assertIn("wrote spec/restated.json", "\n".join(self.changes.notes))
        self.assertNotIn("spec/capabilities/till.md", "\n".join(self.changes.notes))
        self.assertIn("spec/index.md", "\n".join(self.changes.notes))

    def test_the_report_names_each_open_capability_proposal(self):
        self.assertIn(".shop/work/i1/open.md, a capability-proposal that is `awaiting-answer`",
                      "\n".join(self.changes.notes))
        self.assertNotIn("closed.md", "\n".join(self.changes.notes))


class AConvertedRepository(unittest.TestCase):
    def test_only_the_references_that_predate_restated_json_and_the_version_change(self):
        index = INDEX.replace("title: shop\n", "title: shop\nlanguage: codified-1\n")
        restated = json.dumps({"till#r1": {"text": "old", "line": 9}, "till#r2": {"text": "old", "line": 10}})
        root = repository({"spec/index.md": index, "spec/capabilities/till.md": CODIFIED,
                           ".shop/plugin-version": "0.29.0\n", ".shop/work/i1/w1.md": "Names till#r2.\n",
                           ".shop/work/i1/log.jsonl": '{"line": "till#r1"}\n'},
                          later={"spec/restated.json": restated})
        (root / ".shop/work/i1/log.jsonl").write_text('{"line": "till#r1"}\n{"line": "till#r1, new"}\n')
        (root / ".shop/work/i2/w2.md").parent.mkdir(parents=True)
        (root / ".shop/work/i2/w2.md").write_text("Names till#r1, a fresh id.\n")
        git(root, "add", "-A")
        git(root, "commit", "-q", "-m", "after the conversion")
        code, said = upgraded(root)
        self.assertEqual(code, 0, said)
        self.assertEqual(git(root, "rev-list", "--count", "HEAD").strip(), "4")
        changed = git(root, "diff", "--name-only", "HEAD~1").split()
        self.assertEqual(sorted(changed), [".shop/plugin-version", ".shop/work/i1/log.jsonl", ".shop/work/i1/w1.md"])
        self.assertEqual((root / ".shop/work/i1/w1.md").read_text(), "Names till#r2@0.29.\n")
        self.assertEqual((root / ".shop/work/i1/log.jsonl").read_text(),
                         '{"line": "till#r1@0.29"}\n{"line": "till#r1, new"}\n')
        self.assertEqual((root / ".shop/plugin-version").read_text(), "0.30.0\n")
        self.assertNotIn("left for a session", said)


class TheRepositoryAtTheFrozenCommit(unittest.TestCase):
    """A copy of this repository at 96818f71, the commit spec/restated.json was frozen from."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp())
        atexit.register(shutil.rmtree, cls.root, True)
        here = SCRIPTS.parent
        archive = subprocess.run(["git", "archive", FROZEN], cwd=here, check=True, capture_output=True).stdout
        subprocess.run(["tar", "-x"], cwd=cls.root, input=archive, check=True)
        init(cls.root)
        git(cls.root, "add", "-A", "-f")
        git(cls.root, "commit", "-q", "-m", "at %s" % FROZEN)
        cls.code, cls.said = upgraded(cls.root)
        cls.frozen = (here / "spec/restated.json").read_text()

    def test_one_commit_makes_every_change(self):
        self.assertEqual(self.code, 0, self.said)
        self.assertEqual(git(self.root, "rev-list", "--count", "HEAD").strip(), "2")
        self.assertEqual(git(self.root, "status", "--porcelain"), "")

    def test_restated_json_is_the_one_frozen_from_it(self):
        self.assertEqual((self.root / "spec/restated.json").read_text(), self.frozen)

    def test_every_capability_is_scaffolded_and_reported(self):
        for path in sorted((self.root / "spec/capabilities").glob("*.md")):
            text = path.read_text()
            self.assertIn("Restates: r", text, path.name)
            self.assertNotRegex(text, r"(?m)^- \[r\d+\]", path.name)
            self.assertIn("spec/capabilities/%s" % path.name, self.said)
        self.assertIn("spec/index.md", self.said)

    def test_no_deprecated_scenario_is_left(self):
        for path in (self.root / "features").glob("*.feature"):
            self.assertNotRegex(path.read_text(), r"(?m)^\s*@.*@deprecated\b", path.name)

    def test_old_references_are_written_with_their_release(self):
        text = (self.root / ".shop/work/i1-first-spec/formulation.md").read_text()
        self.assertIn("formulation#r1@0.29", text)
        self.assertNotRegex(text, r"formulation#r\d+(?![\d@])")


if __name__ == "__main__":
    unittest.main()
