"""Unit tests of scripts/model_spec's term ids: a condition that shares its word with another entry is
keyed `<term> of <kind>`, so same-named entries are two terms and no v_t2 (a term with two entries)."""

from test_model_spec import GLOSSARY, PATH, CodifiedTest

TWO = ("- **open** (adjective of work-item): A work-item is open when the work-item is not `green`.\n"
       "- **open** (adjective of initiative): An initiative is open when the initiative is not `done`.\n")


class TermIdTest(CodifiedTest):
    def test_same_named_conditions_with_glosses_are_two_terms(self):
        text = GLOSSARY.read_text().replace(
            "- **open** (adjective of initiative): its status is not `done` and not `abandoned`.\n", TWO)
        self.write("spec/index.md", text)
        f = self.facts()
        self.assertIn(f'category("term/{PATH}/open-of-work-item", "condition").', f)
        self.assertIn(f'category("term/{PATH}/open-of-initiative", "condition").', f)
        found, _ = self.check()
        self.assertEqual(self.rows(found, "v_t2"), [])

    def test_a_condition_with_a_gloss_and_no_twin_is_keyed_by_its_word(self):
        text = GLOSSARY.read_text().replace(
            "- **open** (adjective of initiative): its status is not `done` and not `abandoned`.\n",
            TWO.splitlines(True)[0])
        self.write("spec/index.md", text)
        self.assertIn(f'category("term/{PATH}/open", "condition").', self.facts())
