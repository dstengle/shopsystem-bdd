import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import migrate_layout as layout


class FakePlan:
    def __init__(self, moves, texts):
        self.context = "shop"
        self.moves, self.texts, self.read_paths = moves, {}, []
        self._files = texts

    def read(self, rel):
        self.read_paths.append(rel)
        return self._files[rel].decode() if isinstance(self._files[rel], bytes) else self._files[rel]


class OnlyMarkdownGetsAKind(unittest.TestCase):
    def test_a_non_markdown_file_in_plans_or_notes_has_no_kind(self):
        for final in (".shop/records/archive/design-notes/shape.png",
                      ".shop/records/archive/plans/x-slices.json",
                      ".shop/records/archive/plans/notes.txt",
                      ".shop/records/run-test-log.json"):
            self.assertIsNone(layout.record_kind(final), final)

    def test_a_markdown_file_keeps_its_kind(self):
        self.assertEqual(layout.record_kind(".shop/records/archive/plans/a.md"), "initiative-archive")
        self.assertEqual(layout.record_kind(".shop/records/archive/design-notes/a.md"), "decision-argument")
        self.assertEqual(layout.record_kind(".shop/records/a-test-log.md"), "measurement")

    def test_an_adr_and_a_request_have_the_kind_of_their_place(self):
        self.assertEqual(layout.record_kind(".shop/records/decision-arguments/0001-x.md"), "decision-argument")
        self.assertEqual(layout.record_kind(".shop/records/archive/requests/q1.md"), "initiative-archive")

    def test_plan_ids_does_not_read_or_write_a_moved_image(self):
        final = ".shop/records/archive/design-notes/shape.png"
        plan = FakePlan({"docs/superpowers/specs/shape.png": final}, {"docs/superpowers/specs/shape.png": b"\x89PNG\xff"})
        layout.plan_ids(plan)
        self.assertEqual(plan.texts, {})
        self.assertEqual(plan.read_paths, [])


if __name__ == "__main__":
    unittest.main()
