"""supervise_answers: a reviewer's work-item whose every question is answered, with no verdict from this run (capability
supervision r118, r119: `work run` makes the reviewer's transition only on a verdict, and leaves the item otherwise, r77)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import supervise  # noqa: E402,F401  (its import order settles the modules' circular imports)
from supervise_answers import Answers  # noqa: E402


class Stubbed(Answers):
    def __init__(self, root):
        self.root, self.dir, self.initiative = root, root / "i1", "i1"
        self.moves, self.sessions, self.written = [], [], []

    def delegation(self):
        return "Please get everything delivered."

    def asking(self):
        return [("w1", "work-item")]

    def held(self, name, heading):
        return [["- a question"]] if heading == "Questions" else [["- an answer"]]

    def ask(self, name, question, delegation):
        self.sessions.append(name)

    def section(self, name, heading, text):
        self.written.append(text)

    def move(self, name, before, target):
        self.moves.append((name, target))

    def commit(self, *args):
        pass

    def uncommitted(self, name):
        return False

    def push(self):
        pass


def test_a_reviewers_item_with_every_question_answered_and_no_verdict_from_this_run_is_not_moved(tmp_path, monkeypatch):
    (tmp_path / "i1").mkdir()
    (tmp_path / "i1" / "w1.md").write_text("---\nkind: work-item\nstatus: awaiting-answer\n---\n")
    (tmp_path / "i1" / "log.jsonl").write_text(json.dumps(
        {"work-item": "w1", "before": "done", "after": "awaiting-answer"}) + "\n")
    monkeypatch.setattr("supervise_answers.workqueue.agrees", lambda *args: None)
    run = Stubbed(tmp_path)
    run.answers()
    assert run.moves == []
    assert run.written == []
    assert run.sessions == []
