"""The messages of a session's transcript (conversation, plan 8 D2 and D4): the person's prompts and the session's
text of each turn, without tool uses, tool results, thinking, reminders, meta, sidechain, compaction or local-command
rows; the newest message of the person the words are in, and the messages around it."""
import backlog_testing  # noqa: F401  (the scripts directory on the path)
import conversation_read as C
import pytest
import transcript_testing as T
from measure_read import Refused


def read(tmp_path, rows):
    return C.messages(T.write(tmp_path, "s-1", rows))


def test_a_conversation_reads_as_its_messages(tmp_path):
    found = read(tmp_path, T.CONVERSATION)
    assert [m.who for m in found] == ["person", "session"] * 3
    assert [m.ident for m in found] == T.IDENTS
    assert [m.text for m in found] == T.TEXTS
    assert found[0].at.isoformat() == "2026-11-05T10:01:00+00:00"


NOISE = {
    "tool result": T.tool_result("RESULT", "n1", T.at(4)),
    "thinking": T.thinking("THOUGHT", "n1", T.at(4), msg="m2"),
    "tool use": T.tool_use("Read", "n1", T.at(4), msg="m2"),
    "meta": T.person("META", "n1", T.at(4), isMeta=True),
    "sidechain person": T.person("SIDE", "n1", T.at(4), isSidechain=True),
    "sidechain session": T.session_text("SIDE", "n1", T.at(4), isSidechain=True),
    "compact summary": T.person("SUMMARY", "n1", T.at(4), isCompactSummary=True),
    "local command": T.person("<local-command-stdout>ok</local-command-stdout>", "n1", T.at(4)),
    "command": T.person("<command-name>/clear</command-name>", "n1", T.at(4)),
    "system": {"type": "system", "uuid": "n1", "timestamp": T.at(4), "content": "SYSTEM"},
    "attachment": {"type": "attachment", "uuid": "n1", "timestamp": T.at(4), "attachment": {"x": "ATTACHED"}},
    "queue operation": {"type": "queue-operation", "operation": "enqueue", "content": "QUEUED"},
}


@pytest.mark.parametrize("kind", sorted(NOISE))
def test_only_the_words_are_messages(tmp_path, kind):
    """Review Focus 1."""
    rows = T.CONVERSATION[:4] + [NOISE[kind]] + T.CONVERSATION[4:]
    found = read(tmp_path, rows)
    assert [m.text for m in found] == T.TEXTS
    assert [m.ident for m in found] == T.IDENTS


def test_a_turn_split_over_rows_is_one_message(tmp_path):
    """Review Focus 1."""
    rows = [T.person("go", "u1", T.at(1)), T.session_text("a", "a1", T.at(2), msg="m1"),
            T.session_text("b", "a2", T.at(3), msg="m2"), T.tool_use("Bash", "a3", T.at(4), msg="m2"),
            T.tool_result("out", "u2", T.at(5)), T.session_text("c", "a4", T.at(6), msg="m3")]
    found = read(tmp_path, rows)
    assert [(m.who, m.ident, m.text) for m in found] == [("person", "u1", "go"), ("session", "a1", "a\n\nb\n\nc")]


def test_system_reminders_are_cut_from_the_persons_text(tmp_path):
    """Review Focus 1."""
    rows = [T.person("Keep this.\n<system-reminder>secret</system-reminder>", "u1", T.at(1)),
            T.person("<system-reminder>only\nthis</system-reminder>", "u2", T.at(2))]
    assert [m.text for m in read(tmp_path, rows)] == ["Keep this."]


def test_text_blocks_of_the_person_are_joined(tmp_path):
    content = [{"type": "text", "text": "a"}, {"type": "image"}, {"type": "text", "text": "b"}]
    assert [m.text for m in read(tmp_path, [T.person(content, "u1", T.at(1))])] == ["a\n\nb"]


def test_a_row_with_no_type_is_refused(tmp_path):
    path = T.write(tmp_path, "s-1", [T.person("a", "u1", T.at(1)), {"uuid": "x"}])
    with pytest.raises(Refused) as why:
        C.messages(path)
    assert str(path) in str(why.value) and ":2" in str(why.value)


def test_whitespace_does_not_stop_a_match(tmp_path):
    """Review Focus 2."""
    found = read(tmp_path, [T.person("Please keep the turns.", "u1", T.at(1))])
    assert C.cited(found, "keep   the\nturns") == 0


def test_the_newest_message_is_cited(tmp_path):
    """Review Focus 2."""
    rows = [T.person("same words here", "u1", T.at(1)), T.session_text("ok", "a1", T.at(2)),
            T.person("again: same words", "u2", T.at(3))]
    assert C.cited(read(tmp_path, rows), "same words") == 2


def test_the_sessions_words_are_not_the_persons(tmp_path):
    """Review Focus 2."""
    assert C.cited(read(tmp_path, T.CONVERSATION), "the turns are kept") is None


def test_around_is_clipped_at_both_ends(tmp_path):
    found = read(tmp_path, T.CONVERSATION)
    assert [len(C.around(found, i)) for i in (0, 2, 5)] == [3, 5, 3]
    assert C.around(found, 2) == found[0:5]
