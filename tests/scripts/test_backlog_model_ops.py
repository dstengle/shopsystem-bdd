"""A model line that restates an operation (b463): laid in place of the operation's line and its outcomes."""
import backlog_model

BODY = ["object note", "  attributes: text (text)", "", "service notes", "  operation add(text)",
        "    outcomes: done | refused: no text", "  operation archive(note)  outcomes: done", ""]
LINES = ["service notes", "  operation add(text, priority)  outcomes: done", "  operation drop(note)"]


def test_restated_in_place_and_new_appended():
    laid = backlog_model.merged(BODY, LINES)
    assert laid == ["object note", "  attributes: text (text)", "", "service notes",
                    "  operation add(text, priority)  outcomes: done", "  operation archive(note)  outcomes: done",
                    "  operation drop(note)", ""]
