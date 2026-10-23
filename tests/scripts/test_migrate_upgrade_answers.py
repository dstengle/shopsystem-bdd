"""Tests of the 0.25.0 upgrade step (scripts/migrate_upgrade_answers.py) on trees the r29 scenario does not build."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import migrate_upgrade_answers as answers

ITEM = "---\nid: work-item/x/%s\nkind: work-item\nstatus: %s\n---\n\n# %s\n\n%s\n"


class AnswersStepTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_a_file_with_neither_the_old_status_nor_the_old_heading_is_not_written(self):
        self.write(".shop/work/i1/w1.md", ITEM % ("w1", "ready", "w1", "## Answers"))
        self.assertEqual(answers.plan(self.root).texts, {})

    def test_a_log_line_renames_before_and_after_and_leaves_a_line_with_no_status(self):
        lines = [{"work-item": "w1", "before": "awaiting-ruling", "after": "ready"}, {"event": "start"}]
        self.write(".shop/work/i1/log.jsonl", "".join(json.dumps(l) + "\n" for l in lines))
        out = answers.plan(self.root).texts[".shop/work/i1/log.jsonl"].splitlines()
        self.assertEqual(json.loads(out[0])["before"], "awaiting-answer")
        self.assertEqual(json.loads(out[1]), {"event": "start"})

    def test_free_text_naming_the_old_status_stays(self):
        self.write(".shop/work/i1/w1.md", ITEM % ("w1", "ready", "w1", "It was awaiting-ruling once."))
        self.assertEqual(answers.plan(self.root).texts, {})

    def test_a_file_that_is_not_a_work_item_is_left(self):
        self.write(".shop/work/i1/initiative.md", "---\nkind: initiative\n---\n\n## Rulings\n")
        self.assertEqual(answers.plan(self.root).texts, {})


if __name__ == "__main__":
    unittest.main()
