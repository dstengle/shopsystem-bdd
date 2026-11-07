"""Unit tests of scripts/model's glossary, read into facts (r48, r50, r51) and checked. ModelTest and the file
builders are in test_model.py. The glossary is typed (design model v5): spec_lexicon reads its entries, and a codified
requirement and every scenario of a capability's feature use lexicon words by their parse, so only a scenario of a
feature file that is no capability's is read for the words the glossary avoids."""

import sys
import unittest

from test_model import HAVE_CLINGO, HEAD, THING, ModelTest, cap, feature, full


def index(*glossary):
    """A codified spec/index.md with a ## Glossary section with these bullets."""
    return HEAD + "\n## Glossary\n\n" + "\n".join(glossary) + "\n\n## Where things live\n\n- Here.\n"


def term(name):
    return full("term", name)


class GlossaryFactsTest(ModelTest):
    """r48, r50, r51: the glossary read into facts (no solver needed)."""

    def facts(self):
        r = self.run_model("facts", python=[sys.executable, "-I", "-S"])
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout.splitlines()

    def test_a_definition_with_a_period_is_one_definition(self):
        self.write("spec/index.md", index("- **store** (noun): where things are kept, e.g. a shelf."))
        lines = self.facts()
        self.assertIn(f'node("{term("store")}", "term").', lines)
        self.assertEqual([l for l in lines if l.startswith("avoid(")], [])

    def test_r51(self):
        """Only a scenario of no capability's feature is read for words; code spans and tags are no mentions."""
        self.write("spec/index.md", index("- **store** (noun): where things are kept. Not: shelf."))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] x"]))
        self.write("features/thing.feature", "Feature: thing\n\n  @g1 @r1\n  Scenario: one\n    Given a shelf\n")
        self.write("features/stray.feature", "Feature: stray\n\n  Scenario: the store answers\n"
                                             "    Given a `shelf` and a store-front\n")
        mentions = sorted(l for l in self.facts() if l.startswith("mentions("))
        self.assertEqual(mentions, ['mentions("features/stray.feature:the store answers", "store").'])

    def test_a_typed_entry_is_read_by_its_term_and_its_not_words(self):
        self.write("spec/index.md", index(
            "- **initiative** (noun): the delivery of one request's accepted lines. Plural: initiatives. Not: epic.",
            "- **`work run`** (proper noun): the supervisor that runs nodes through their transitions.",
            "- **status** (attribute of initiative): a node's place in its lifecycle. Values: `proposed`, `started`.",
            "  Transitions: `proposed` → `started`: `work start`. Not: state.",
            "- **status** (attribute of work-item): Values: `drafted`, `ready`. Not: state.",
            "- **under** (relation work-item → capability-proposal): a work-item delivers part of a proposal.",
            "- **spec lock** (noun, exclusive): held by every integrate, apply and formulate round."))
        lines = self.facts()
        entries = sorted(line.split(", ", 2)[2] for line in lines if line.startswith("glossary_entry("))
        self.assertEqual(entries, sorted(['"initiative").', '"work run").', '"status").', '"status of work-item").',
                                          '"under of work-item to capability-proposal").',
                                          '"spec lock").']))
        self.assertIn(f'avoid("{term("initiative")}", "epic").', lines)
        self.assertIn(f'avoid("{term("status")}", "state").', lines)
        self.assertIn(f'avoid("{term("status-of-work-item")}", "state").', lines)
        self.assertIn(f'node("{term("work-run")}", "term").', lines)


@unittest.skipUnless(HAVE_CLINGO, "clingo is needed to solve")
class GlossaryCheckTest(ModelTest):
    """r49, r52-r54: the glossary checked."""

    def test_a_term_in_a_proposal_list_is_read_as_the_glossary_writes_its_id(self):
        self.good()
        self.observation()
        self.initiative()
        self.proposal(adds="[term/Initiative]")
        r = self.run_model("check")
        self.assertNotIn("which the glossary does not have", r.stdout)

    def test_a_good_glossary_passes(self):
        self.good()
        found, r = self.check_json()
        self.assertEqual((found["violations"], found["problems"], found["unresolved"]), ([], [], []), found)
        self.assertEqual(r.returncode, 0)

    def test_r52(self):
        self.write("spec/index.md", index("- **slice** (noun): a unit of work. Not: chunk."))
        self.write("spec/capabilities/thing.md", cap("thing", ["- [r1] x"]))
        self.write("features/thing.feature", feature("thing", ("@r1", "a chunk is planned"), ("@r1 @deprecated", "a chunk as it was")))
        self.write("features/stray.feature", "Feature: stray\n\n  Scenario: chunks are planned\n    Given a thing\n")
        found, r = self.check_json()
        self.assertEqual(self.violated(found, "v_t1"), [["features/stray.feature:chunks are planned", "chunk",
                                                         term("slice")]], found)
        self.assertEqual(r.returncode, 1)
        self.assertIn("v_t1  a word the glossary avoids  (1)", self.run_model("check").stdout)
        self.assertNotIn(THING, str(self.violated(found, "v_t1")))


if __name__ == "__main__":
    unittest.main()
