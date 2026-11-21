"""A model line that restates an operation (b463): laid in place of the operation's line and its outcomes, and put
back as git held the model file before the lay."""
import subprocess

import backlog_model
import backlog_model_ops

BODY = ["object note", "  attributes: text (text)", "", "service notes", "  operation add(text)",
        "    outcomes: done | refused: no text", "  operation archive(note)  outcomes: done", ""]
LINES = ["service notes", "  operation add(text, priority)  outcomes: done", "  operation drop(note)"]


def test_restated_in_place_and_new_appended():
    laid = backlog_model.merged(BODY, LINES)
    assert laid == ["object note", "  attributes: text (text)", "", "service notes",
                    "  operation add(text, priority)  outcomes: done", "  operation archive(note)  outcomes: done",
                    "  operation drop(note)", ""]


def test_unmerged_puts_the_operation_back():
    laid = backlog_model.merged(BODY, LINES)
    assert backlog_model.unmerged(laid, LINES, lambda header, op, lines: BODY) == BODY


def test_unmerged_without_a_held_version_takes_the_line_out():
    laid = backlog_model.merged(BODY, LINES)
    assert backlog_model.unmerged(laid, LINES) == [x for x in BODY if not x.lstrip().startswith(("operation add",
                                                                                                  "outcomes: done |"))]


def test_held_reads_the_version_before_the_lay(tmp_path):
    def git(*args):
        subprocess.run(["git", "-C", str(tmp_path), *args], check=True, capture_output=True)
    path = tmp_path / "notes.md"
    git("init", "-q")
    path.write_text("# Notes\n\n```model\n%s\n```\n" % "\n".join(BODY))
    git("add", "notes.md")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "model")
    lines = path.read_text().split("\n")
    path.write_text("\n".join(lines[:3] + backlog_model.merged(lines[3:-2], LINES) + lines[-2:]))
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "laid")
    unit = ["  operation add(text, priority)  outcomes: done"]
    assert backlog_model_ops.held(path, "service notes", "add", unit) == BODY
    assert backlog_model_ops.held(tmp_path / "other.md", "service notes", "add", unit) is None
