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


def test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case(tmp_path):
    from supervise_glossary import names_one
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text("# Index\n\n## Glossary\n\n- **ledger**: a log. Not: journal.\n")
    (tmp_path / ".shop" / "work" / "i1").mkdir(parents=True)
    (tmp_path / ".shop" / "work" / "i1" / "g1.md").write_text("---\nkind: glossary-proposal\nstatus: drafted\n---\n")
    assert names_one(tmp_path, "Does it write the ledger?")
    assert names_one(tmp_path, "Is the Ledger kept?")
    assert names_one(tmp_path, "Does it wait for g1 to be applied?")
    assert not names_one(tmp_path, "Does the pledger own it?")
    assert not names_one(tmp_path, "Does it wait for g10?")
    assert not names_one(tmp_path, "Is a journal kept?")
    assert not names_one(tmp_path, "Which module owns the log?")
