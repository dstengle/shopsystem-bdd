"""`work quote` (conversation r1, plan 8 D3-D6): the person's words with the two messages before and after them,
written in .shop/quotes/<n>.md and committed alone; the file reads back whatever its text holds; words that match
nothing write nothing. `work show quote-<n>` (r3, D7) prints the quote's messages."""
import datetime
import json
import re

import conversation_quote as Q
import pytest
import transcript_testing as T
from backlog_testing import git, work
from conversation_read import Message
from measure_batch_read import project_dir
from workqueue import Refused


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = tmp_path / "store"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(path))
    return path


@pytest.fixture
def quoting(backlog_repo, store):
    """The repository, with the session s-1's transcript CONVERSATION in its project directory."""
    T.write(project_dir(backlog_repo), "s-1", T.CONVERSATION)
    return backlog_repo


def quote(repo, *args):
    return work(repo, "quote", *args)


def test_a_quote_keeps_its_turns(quoting):
    before = git(quoting, "rev-parse", "HEAD")
    done = quote(quoting, T.TEXTS[2], "--session", "s-1")
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == 'quote-1 "%s"' % T.TEXTS[2]
    text = (quoting / ".shop/quotes/1.md").read_text()
    assert "\nsession: s-1\n" in text and "\nmessage: u2\n" in text and "\nkind: quote\n" in text
    headings = re.findall(r"^### .*$", text, re.MULTILINE)
    assert len(headings) == 5
    assert [h.endswith(", cited") for h in headings] == [False, False, True, False, False]
    assert "TOOL OUTPUT" not in text and "secret-path" not in text and "Bash" not in text
    assert git(quoting, "rev-parse", "HEAD~1").strip() == before.strip()
    assert git(quoting, "log", "-1", "--name-only", "--format=").split() == [".shop/quotes/1.md"]


def test_the_next_quote_is_numbered_on(quoting):
    assert quote(quoting, T.TEXTS[0], "--session", "s-1").returncode == 0
    done = quote(quoting, T.TEXTS[4], "--session", "s-1")
    assert done.stdout.startswith('quote-2 "'), done.stderr
    assert (quoting / ".shop/quotes/2.md").is_file()


def at(minute):
    return datetime.datetime(2026, 11, 5, 10, minute, tzinfo=datetime.UTC)


TRICKY = ["## Messages", "### the person, x, y, cited", "```text\nin a fence\n```", "a ```` run of four",
          "---", "> quoted", "a trailing blank line\n", "`", "plain"]


@pytest.mark.parametrize("text", TRICKY)
def test_a_quote_reads_back_whatever_its_text_holds(text):
    """Review Focus 4."""
    messages = [Message("u1", "person", at(1), text), Message("a1", "session", at(2), "said: " + text),
                Message("u2", "person", at(3), "more " + text)]
    q = Q.Quote("quote-3", "quote/ex.com/prod/ctx/quote-3", "s-1", "u2", "2026-11-05", "more " + text, messages)
    assert Q.parse(Q.render(q), ".shop/quotes/3.md") == q


def test_a_long_message_around_the_quote_is_cut(backlog_repo, store):
    rows = [T.person("x" * 5000 + " keep me", "u1", T.at(1)), T.session_text("y" * 5000, "a1", T.at(2)),
            T.person("z" * 5000 + " cite me", "u2", T.at(3))]
    T.write(project_dir(backlog_repo), "s-1", rows)
    assert quote(backlog_repo, "cite me", "--session", "s-1").returncode == 0
    q = Q.find(backlog_repo, "quote-1")
    assert [m.text for m in q.messages] == ["x" * 2000 + " […]", "y" * 2000 + " […]", "z" * 5000 + " cite me"]


def test_a_quote_that_matches_nothing_writes_nothing(quoting):
    """Review Focus 2."""
    before = git(quoting, "rev-parse", "HEAD")
    done = quote(quoting, "the turns are kept and nothing else of it at all", "--session", "s-1")
    assert done.returncode == 1
    assert "work quote: the person wrote no message with" in done.stderr
    assert '"the turns are kept and nothing else of i"' in done.stderr and "s-1" in done.stderr, done.stderr
    assert "--session" in done.stderr
    done = quote(quoting, "  \n ", "--session", "s-1")
    assert done.returncode == 1 and "work quote: the words are empty" in done.stderr, done.stderr
    assert not (quoting / ".shop/quotes").exists()
    assert git(quoting, "rev-parse", "HEAD") == before


def test_a_session_is_found_by_its_id_in_any_project(backlog_repo, store):
    """Review Focus 5."""
    T.write(store / "projects" / "-other-dir", "s-1", T.CONVERSATION)
    done = quote(backlog_repo, T.TEXTS[2], "--session", "s-1")
    assert done.returncode == 0, done.stderr
    assert Q.find(backlog_repo, "quote-1").session == "s-1"


def test_a_transcript_given_is_read_as_given(backlog_repo, store, tmp_path):
    path = T.write(tmp_path / "elsewhere", "whatever", T.CONVERSATION)
    done = quote(backlog_repo, T.TEXTS[2], "--transcript", str(path))
    assert done.returncode == 0, done.stderr
    assert Q.find(backlog_repo, "quote-1").session == "s-1"
    done = quote(backlog_repo, T.TEXTS[2], "--transcript", str(tmp_path / "gone.jsonl"))
    assert done.returncode == 1 and "gone.jsonl" in done.stderr, done.stderr


def test_a_malformed_quote_file_is_refused_naming_its_field(quoting):
    assert quote(quoting, T.TEXTS[2], "--session", "s-1").returncode == 0
    path = quoting / ".shop/quotes/1.md"
    path.write_text(path.read_text().replace("kind: quote", "kind: note"))
    with pytest.raises(Refused, match=r"^\.shop/quotes/1\.md: kind "):
        Q.find(quoting, "quote-1")


def test_show_prints_every_message_of_the_quote(quoting):
    assert quote(quoting, T.TEXTS[2], "--session", "s-1").returncode == 0
    done = work(quoting, "show", "quote-1")
    assert done.returncode == 0, done.stderr
    lines = done.stdout.splitlines()
    assert lines[0] == 'quote-1 "%s"' % T.TEXTS[2]
    assert "  session: s-1" in lines and "  date: 2026-11-05" in lines
    body = done.stdout.split("\n", 1)[1]
    places = [body.index(text) for text in T.TEXTS[:5]]
    assert places == sorted(places)
    heads = [line for line in lines if line.startswith(("the person, ", "the session, "))]
    assert len(heads) == 5
    assert [line.endswith(", cited:") for line in heads] == [False, False, True, False, False]
    assert T.TEXTS[5] not in done.stdout


def test_show_json_gives_the_quote(quoting):
    assert quote(quoting, T.TEXTS[2], "--session", "s-1").returncode == 0
    done = work(quoting, "show", "quote-1", "--json")
    got = json.loads(done.stdout)["quote"]
    assert got["name"] == "quote-1" and got["session"] == "s-1" and got["message"] == "u2"
    assert len(got["messages"]) == 5 and [m["cited"] for m in got["messages"]].count(True) == 1
    assert got["messages"][2] == {"who": "person", "at": "2026-11-05T10:03:00+00:00", "ident": "u2", "cited": True,
                                  "text": T.TEXTS[2]}


def test_show_of_no_quote_is_refused(backlog_repo):
    done = work(backlog_repo, "show", "quote-9")
    assert done.returncode == 1
    assert "there is no quote quote-9 in .shop/quotes/" in done.stderr, done.stderr


def test_show_of_an_item_or_initiative_is_unchanged(quoting):
    assert work(quoting, "idea", "Fix the parser").returncode == 0
    done = work(quoting, "show", "b1")
    assert done.returncode == 0 and done.stdout.startswith('b1 "Fix the parser"'), done.stderr
    done = work(quoting, "show")
    assert done.returncode == 0 and done.stdout == "", (done.stdout, done.stderr)
