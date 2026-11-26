"""The directive (conversation r10-r16, b20): its file read back as written, `work directive --quote`, `work
directives`, `work show directive-<n>`, `work promote` to each kind of target and the refusals no scenario drives, and
the SessionStart hook's `conversation_hook directives`, silent with none live and never failing."""
import datetime
import json
import subprocess
import sys

import conversation_quote
import directive
import pytest
import transcript_testing as T
from backlog_testing import SCRIPTS, git, work
from conversation_read import Message
from plumbing.shop_files import Refused


def quote(repo, n=1, words="Merge and release while I am away."):
    at = datetime.datetime(2026, 11, 16, 10, tzinfo=datetime.UTC)
    found = conversation_quote.Quote("quote-%d" % n, "quote/ex.com/prod/ctx/quote-%d" % n, "s", "m%d" % n,
                                     "2026-11-16", words, [Message("m%d" % n, "person", at, words)])
    path = repo / conversation_quote.rel_of(found.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(conversation_quote.render(found))
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "quote")


@pytest.fixture
def kept(backlog_repo):
    quote(backlog_repo)
    done = work(backlog_repo, "directive", "--quote", "quote-1")
    assert done.returncode == 0, done.stderr
    return backlog_repo


@pytest.mark.parametrize("why", [None, "Kept as CLAUDE.md's line: # not a comment\nand a second line."])
def test_a_directive_reads_back_as_written(why):
    found = directive.Directive("directive-3", "directive/ex.com/prod/ctx/directive-3", "dropped" if why else "live",
                                "2026-11-16", "quote-7", "Merge it.\n\nThen > release it.", None, why)
    assert directive.parse(directive.render(found), "x.md") == found


@pytest.mark.parametrize(("old", "new", "said"), [("status: live", "status: done", "status"),
                                                  ("quote: quote-1", "quote: q1", "quote"),
                                                  ("> Merge", "Merge", "words")])
def test_a_malformed_directive_is_refused_naming_the_field(kept, old, new, said):
    path = kept / directive.rel_of("directive-1")
    with pytest.raises(Refused, match=said):
        directive.parse(path.read_text().replace(old, new), "x.md")


def test_work_directive_of_a_quote_commits_the_directive_alone(kept):
    assert git(kept, "show", "--name-only", "--format=", "HEAD").split() == [".shop/directives/1.md"]
    found = directive.find(kept, "directive-1")
    assert (found.status, found.quote, found.words) == ("live", "quote-1", "Merge and release while I am away.")


def test_work_directive_takes_words_or_a_quote(kept):
    assert work(kept, "directive").returncode == 1
    assert "one of them" in work(kept, "directive", "x", "--quote", "quote-1").stderr
    assert "no quote quote-9" in work(kept, "directive", "--quote", "quote-9").stderr


def test_work_directives_lists_the_live_ones_and_all_with_their_status(kept):
    quote(kept, 2, "Name items by their titles.")
    work(kept, "directive", "--quote", "quote-2")
    (kept / "CLAUDE.md").write_text("# rules\n")
    git(kept, "add", "-A")
    git(kept, "commit", "-q", "-m", "claude")
    assert work(kept, "promote", "directive-2", "--to", "CLAUDE.md").returncode == 0
    live = work(kept, "directives").stdout
    assert "directive-1" in live and "directive-2" not in live
    every = work(kept, "directives", "--all").stdout
    assert "| directive-2 |" in every and "| promoted |" in every


def test_work_show_prints_the_directive_with_its_quote(kept):
    done = work(kept, "show", "directive-1")
    assert done.stdout.startswith('directive-1 "Merge and release') and "status: live" in done.stdout
    assert 'quote-1 "Merge and release' in done.stdout and ", cited:" in done.stdout
    shown = json.loads(work(kept, "show", "directive-1", "--json").stdout)["content"]
    assert shown["directive"]["name"] == "directive-1"


def test_a_directive_is_promoted_to_a_design_decision_by_its_id(kept):
    path = kept / "spec/decisions/0007-merge-when-away.md"
    path.parent.mkdir(parents=True)
    path.write_text("---\nid: design-decision/ex.com/prod/ctx/merge-when-away\n---\n")
    assert work(kept, "promote", "directive-1", "--to", "design-decision/no-such").returncode == 1
    done = work(kept, "promote", "directive-1", "--to", "design-decision/ex.com/prod/ctx/merge-when-away")
    assert done.returncode == 0, done.stderr
    assert directive.find(kept, "directive-1").promoted_to == "design-decision/ex.com/prod/ctx/merge-when-away"


def test_a_drop_with_no_reason_and_a_missing_directive_are_refused(kept):
    assert "--why is empty" in work(kept, "drop", "directive-1", "--why", " ").stderr
    assert "no directive directive-4" in work(kept, "drop", "directive-4", "--why", "x").stderr
    assert git(kept, "status", "--porcelain") == ""


def hook(cwd):
    return subprocess.run(T.hook_command("SessionStart", "directives"), cwd=cwd, input="{}", capture_output=True,
                          text=True, timeout=60)


def test_the_hook_prints_the_live_directives_under_its_line(kept):
    done = hook(kept)
    assert done.returncode == 0 and done.stdout.splitlines() == [
        directive.HOOK_LINE, '- directive-1 (quote-1, %s): Merge and release while I am away.'
        % directive.find(kept, "directive-1").date], done.stdout
    work(kept, "drop", "directive-1", "--why", "Done.")
    assert (hook(kept).returncode, hook(kept).stdout) == (0, "")


def test_the_hook_is_silent_outside_a_repository_and_on_a_broken_file(kept, tmp_path_factory):
    assert (hook(tmp_path_factory.mktemp("outside")).stdout, hook(kept / "spec").returncode) == ("", 0)
    (kept / ".shop/directives/x.md").write_text("no")
    done = hook(kept)
    assert done.returncode == 0 and done.stdout.startswith("work directives: "), done.stdout


def test_the_hook_exits_0_when_its_modules_are_missing(tmp_path):
    alone = tmp_path / "alone"
    alone.mkdir()
    (alone / "conversation_hook").write_text((SCRIPTS / "conversation_hook").read_text())
    done = subprocess.run([sys.executable, "-S", str(alone / "conversation_hook"), "directives"], cwd=tmp_path,
                          input="{}", capture_output=True, text=True, timeout=60)
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
