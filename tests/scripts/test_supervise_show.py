"""supervision r9 with observation 2026-10-27-silent-exit-on-questions: `work run <initiative>` prints a capability-proposal
awaiting an answer with its open questions and exits 3, even when the initiative has no work-item yet; a run whose
proposals are formulated and work-items green exits 0."""
import pathlib
import sys

SCRIPTS = pathlib.Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import supervise


class Stand:
    """The parts of supervise.Run that show() reads."""

    def __init__(self, items, proposals, questions=None):
        self.initiative, self.noted, self.dir = "i1", [], pathlib.Path(".")
        self._items, self._proposals, self._questions = items, proposals, questions or {}

    def items(self):
        return self._items

    def proposals(self):
        return self._proposals

    def questions(self, name):
        return self._questions.get(name, [])


def test_a_proposal_awaiting_an_answer_is_printed_with_its_question_and_exits_3(capsys):
    stand = Stand([], [("thing", "awaiting-answer")], {"thing": ["- Is a loan one book or many?"]})
    assert supervise.Run.show(stand) == 3
    out = capsys.readouterr().out
    assert "thing awaiting-answer" in out and "Is a loan one book or many?" in out


def test_formulated_proposals_and_green_work_items_exit_0(capsys):
    assert supervise.Run.show(Stand([("w1", "green")], [("thing", "formulated")])) == 0


def test_a_proposal_left_drafted_with_no_question_is_an_error(capsys):
    assert supervise.Run.show(Stand([("w1", "green")], [("thing", "drafted")])) == 1
