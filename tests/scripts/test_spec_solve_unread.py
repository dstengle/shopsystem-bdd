"""spec_solve's report of the requirements `model logic` has no translation of (b272): each printed by its id with
what it cannot read, in text and JSON, never `no findings` beside one, and the exit the findings' alone."""
import json

import spec_solve
from spec_solve_pairs import Finding

UNREAD = [("shelf#r1", "no translation of a count of other than an object")]


def test_an_unread_requirement_alone_is_printed_and_exits_0():
    text, code = spec_solve.report([], False, UNREAD)
    assert code == 0 and "no findings" not in text
    assert text.splitlines() == ["unread shelf#r1: no translation of a count of other than an object",
                                 "0 findings; 1 requirement unread"]


def test_an_unread_requirement_beside_findings_keeps_their_exit():
    l1 = Finding("L1", ["shelf#r2", "shelf#r3"], "shelf#r2 and shelf#r3 clash")
    text, code = spec_solve.report([l1], False, UNREAD)
    assert code == 1
    assert text.splitlines()[1:] == ["unread shelf#r1: no translation of a count of other than an object",
                                     "1 finding: 1 L1; 1 requirement unread"]


def test_the_json_report_lists_the_unread():
    text, code = spec_solve.report([], True, UNREAD)
    assert code == 0 and json.loads(text) == {"findings": [], "unread": [
        {"id": "shelf#r1", "text": "no translation of a count of other than an object"}], "exit": 0}


def test_with_nothing_unread_the_report_is_as_before():
    assert spec_solve.report([], False) == ("no findings", 0)
