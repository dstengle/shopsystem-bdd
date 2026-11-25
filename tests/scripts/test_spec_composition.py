"""spec_composition (b606): spec/index.md's Composition written in the index form from the capability files."""
import tempfile
import unittest
from pathlib import Path

import spec_composition

LIVE = "---\nid: x\n%sretired: []\n---\n\n# X\n\n## Behaviour\n\n### [g1] G\n- [r1] A line.\n"
DEAD = "---\nid: x\nretired: [g1, r1]\n---\n\n# X\n\n## Behaviour\n\n## Moved\n\n| r1 | other#r1 |\n"
OLD = ("---\nid: c\n---\n\n# C\n\n## Composition\n\nThe capabilities, by area.\n\n### spec (core)\n\n"
       "| capability | narrator | group |\n|---|---|---|\n| `beta` | p | service |\n| `gone` | p | service |\n\n"
       "### Retired in 0.38.0\n\nEvery line moved: `alpha`.\n\n## Testing\n\nThe suite.\n")


class Composition(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "spec" / "capabilities").mkdir(parents=True)

    def capability(self, name, text):
        (self.root / "spec" / "capabilities" / ("%s.md" % name)).write_text(text)

    def index(self, text):
        (self.root / "spec" / "index.md").write_text(text)

    def read(self):
        return (self.root / "spec" / "index.md").read_text()

    def test_old_tables_written_in_the_index_form(self):
        self.capability("alpha", LIVE % "area: spec\n")
        self.capability("beta", LIVE % "area: spec\n")
        self.capability("gone", DEAD)
        self.capability("solo", LIVE % "")
        self.index(OLD)
        self.assertEqual(spec_composition.write(self.root), ["spec/index.md"])
        self.assertEqual(self.read(), "---\nid: c\n---\n\n# C\n\n## Composition\n\nThe capabilities, by area.\n\n"
                         "| area | kind | capabilities |\n|---|---|---|\n| spec | core | beta, alpha |\n"
                         "| solo | core | solo |\n\n## Testing\n\nThe suite.\n")
        self.assertEqual(spec_composition.write(self.root), [])

    def test_section_made_when_missing(self):
        self.capability("alpha", LIVE % "")
        self.index("---\nid: c\n---\n\n# C\n")
        spec_composition.write(self.root)
        self.assertEqual(self.read(), "---\nid: c\n---\n\n# C\n\n## Composition\n\n"
                         "| area | kind | capabilities |\n|---|---|---|\n| alpha | core | alpha |\n")

    def test_kind_of_the_model_file(self):
        self.capability("alpha", LIVE % "area: stock\n")
        (self.root / "spec" / "model").mkdir()
        (self.root / "spec" / "model" / "stock.md").write_text("---\narea: stock\nkind: port\n---\n")
        self.index("# C\n\n## Composition\n\n| area | kind | capabilities |\n|---|---|---|\n| stock | core | alpha |\n")
        spec_composition.write(self.root)
        self.assertIn("| stock | port | alpha |", self.read())

    def test_no_requirement_anywhere_no_section(self):
        self.capability("gone", DEAD)
        self.index("# C\n")
        self.assertEqual(spec_composition.write(self.root), [])


if __name__ == "__main__":
    unittest.main()
