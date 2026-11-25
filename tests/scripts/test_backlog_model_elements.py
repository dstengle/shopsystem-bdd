"""A model line that restates an element (b598): an object that repeats a member line of the declared object laid in
its place, its members the line's alone, and put back as git held the model file before the lay; an object that only
adds members still gets them at its end."""
import subprocess

import backlog_model
import backlog_model_ops

BODY = ["object tag", "  attributes: name (text)", "", "object note kind of text",
        "  attributes: text (text); priority: low | high", "  relations: carries → tag (many)", ""]
LINES = ["object note", "  attributes: text (text); priority: low | high | urgent",
         "  relations: carries → tag (many)"]
LAID = ["object tag", "  attributes: name (text)", "", "object note kind of text",
        "  attributes: text (text); priority: low | high | urgent", "  relations: carries → tag (many)", ""]


def test_restated_in_place():
    assert backlog_model.merged(BODY, LINES) == LAID


def test_a_kind_named_replaces_the_header():
    lines = ["object note kind of file"] + LINES[1:]
    assert backlog_model.merged(BODY, lines)[3] == "object note kind of file"


def test_added_members_still_appended():
    lines = ["object note", "  lifecycle status: draft → active"]
    assert backlog_model.merged(BODY, lines) == BODY[:6] + [lines[1]] + BODY[6:]


def test_unmerged_puts_the_element_back():
    assert backlog_model.unmerged(LAID, LINES, lambda header, op, lines: BODY) == BODY


def test_unmerged_without_a_held_element_takes_it_out():
    assert backlog_model.unmerged(LAID, LINES, lambda header, op, lines: BODY[:2]) == BODY[:2] + [""]


def test_held_reads_the_version_before_the_lay(tmp_path):
    def git(*args):
        subprocess.run(["git", "-C", str(tmp_path), *args], check=True, capture_output=True)
    path = tmp_path / "notes.md"
    git("init", "-q")
    path.write_text("# Notes\n\n```model\n%s\n```\n" % "\n".join(BODY))
    git("add", "notes.md")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "model")
    path.write_text("# Notes\n\n```model\n%s\n```\n" % "\n".join(LAID))
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "laid")
    assert backlog_model_ops.held(path, "object note", None, LINES[1:]) == BODY
