"""Unit tests of scripts/model's glossary, read into facts (r48, r50, r51) and checked. ModelTest and the file
builders are in test_model.py."""

import sys
import unittest

from test_model import HAVE_CLINGO, INDEX, THING, ModelTest, cap, feature, full


def index(*glossary):
    """spec/index.md with a ## Glossary section with these bullets."""
    return INDEX + "\n## Glossary\n\n" + "\n".join(glossary) + "\n\n## Where things live\n\n- Here.\n"


def term(name):
    return full("term", name)


class GlossaryFactsTest(ModelTest):
    """r48, r50, r51: the glossary read into facts (no solver needed)."""

    def facts(self):
        r = self.run_model("facts", python=[sys.executable, "-I", "-S"])
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.splitlines()

    def test_a_definition_with_a_period_is_one_definition(self):
        self.write("spec/index.md", index("- **store**: where things are kept, e.g. a shelf."))
        lines = self.facts()
        self.assertIn(f'node("{term("store")}", "term").', lines)
        self.assertEqual([l for l in lines if l.startswith("avoid(")], [])

    def test_r51(self):
        self.write("spec/index.md", index("- **store**: where things are kept. Not: shelf."))
        self.write("spec/capabilities/thing.md", cap("thing", [
            "- [r1] **When** asked, the Store answers.",
            "- [r2] **When** asked, it lists the stores.",
            "- [r3] **When** asked, it can restore a backup.",
            "- [r4] **When** asked, it reads a shelf and a store-front."]))
        self.write("features/thing.feature", "Feature: thing\n\n  @r1\n  Scenario: one\n    Given SHELVES\n    When a shelf is read\n    Then it answers\n\n"
                                             "  @r2\n  Scenario: the store answers\n    Given a thing\n    Then it holds\n")
        lines = self.facts()
        mentions = sorted(l for l in lines if l.startswith("mentions("))
        self.assertEqual(mentions, sorted([
            f'mentions("{THING}#r1", "store").',
            f'mentions("{THING}#r2", "store").',
            f'mentions("{THING}#r4", "shelf").',
            'mentions("features/thing.feature:one", "shelf").',
            'mentions("features/thing.feature:the store answers", "store").']))

    def test_a_typed_entry_is_read_by_its_term_and_its_not_words(self):
        """The typed glossary of design model v5 (a category after the term), read by the 0.29 reader."""
        self.write("spec/index.md", index(
            "- **initiative** (kind): the delivery of one request's accepted lines. Plural: initiatives. Not: epic.",
            "- **`work run`** (actor): the supervisor that runs nodes through their transitions.",
            "- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.",
            "  Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete. Not: state.",
            "- **status** (attribute of work-item): Values: `drafted`, `ready`. Not: state.",
            "- **under** (relation work-item → capability-proposal): a work-item delivers part of a proposal.",
            "- **spec lock** (resource, exclusive): held by every integrate, apply and formulate round."))
        lines = self.facts()
        entries = sorted(line.split(", ", 2)[2] for line in lines if line.startswith("glossary_entry("))
        self.assertEqual(entries, sorted(['"initiative").', '"work run").', '"status of initiative").',
                                          '"status of work-item").', '"under of work-item to capability-proposal").',
                                          '"spec lock").']))
        self.assertIn(f'avoid("{term("initiative")}", "epic").', lines)
        self.assertIn(f'avoid("{term("status-of-initiative")}", "state").', lines)
        self.assertIn(f'node("{term("work-run")}", "term").', lines)

    def test_glossary_entry_reads_the_term_and_its_not_words(self):
        from model_parse import glossary_entry
        self.assertEqual(glossary_entry("**open** (condition of initiative): Means: its status is not `done`."),
                         ("open of initiative", []))
        self.assertEqual(glossary_entry("**start** (event): Forms: starts, started. Not: begin, kick off."),
                         ("start", ["begin", "kick off"]))
        self.assertEqual(glossary_entry("**store**: a place. Not: shelf."), ("store", ["shelf"]))
        self.assertIsNone(glossary_entry("**store** (): a place."))
        self.assertIsNone(glossary_entry("**store** (kind) a place."))
        self.assertIsNone(glossary_entry("**status** (attribute): no kind."))


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class GlossaryCheckTest(ModelTest):
    """r49, r52-r54: the glossary checked."""

    def test_a_term_in_a_proposal_list_is_read_as_the_glossary_writes_its_id(self):
        self.good()
        self.write("spec/index.md", index("- **store**: a place."))
        self.observation()
        self.initiative()
        self.proposal(adds="[term/Store]")
        r = self.run_model("check")
        self.assertNotIn("which the glossary does not have", r.stdout)

    def test_a_good_glossary_passes(self):
        self.write("spec/index.md", index("- **slice**: a unit of work, e.g. a scenario. Not: chunk.",
                                          "- **batch**: the slices one session plans."))
        self.good()
        found, r = self.check_json()
        self.assertEqual((found["violations"], found["problems"], found["unresolved"]), ([], [], []), found)
        self.assertEqual(r.returncode, 0)

    def test_r52(self):
        self.write("spec/index.md", index("- **slice**: a unit of work. Not: chunk."))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it plans each chunk.", "- [r2] It plans a slice."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "it plans"), ("@r2", "chunks are planned"),
                                                     ("@r2 @deprecated", "a chunk as it was")))
        found, r = self.check_json()
        self.assertEqual(sorted(self.violated(found, "v_t1")), sorted([
            [THING + "#r1", "chunk", term("slice")],
            ["features/thing.feature:chunks are planned", "chunk", term("slice")]]), found)
        self.assertFalse([a for a in self.violated(found, "v_t1") if "as it was" in a[0]], found)
        self.assertEqual(r.returncode, 1)
        text = self.run_model("check").stdout
        self.assertIn("v_t1  a word the glossary avoids  (2)", text)

    def test_a_restore_is_no_store(self):
        self.write("spec/index.md", index("- **depot**: where things are kept. Not: store."))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] **When** asked, it can restore a backup."]))
        self.write("features/thing.feature", feature("thing", ("@r1", "a restore")))
        found, _ = self.check_json()
        self.assertEqual(self.violated(found, "v_t1"), [], found)


if __name__ == "__main__":
    unittest.main()
