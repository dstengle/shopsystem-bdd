"""A model line that restates an element (b598): an object that repeats a member line of the declared object laid in
its place, its members the line's alone; an object that only adds members still gets them at its end."""
import backlog_model

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
