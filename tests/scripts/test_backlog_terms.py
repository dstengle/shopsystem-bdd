"""`work line --term` repeatable (b453): several term bullets (or vocabulary entries, in a context with a domain
model) given in one run, written into the item's block in the order given and committed once; one that does not read
refuses the run, writing none of them."""
import shutil

import backlog_items
import backlog_lines
import backlog_section
import pytest
from backlog_testing import git, state, work, write_item
from test_readiness_lay_model import FIXTURE

FROB = "- **frobnicate** (verb, action): Forms: frobnicates, frobnicated. Frame: `work` frobnicates initiative."
TWIDDLE = "- **twiddle** (verb, action): Forms: twiddles, twiddled. Frame: `work` twiddles initiative."
PIN = "- **pin** (verb, action) → operation notes.pin. Forms: pins, pinned. Frame: <actor> pins <note>."
SHELF = "- **shelf** (noun) → object shelf. A place notes are kept."
DECLARED = "object shelf\n  attributes: name (text)\n\nservice notes\n  operation pin(note)  outcomes: done"


def commits(repo):
    return int(git(repo, "rev-list", "--count", "HEAD"))


def test_two_terms_in_one_run_are_one_commit(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    before = commits(ready_repo)
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--term", FROB, "--term", TWIDDLE)
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": 2 terms of work-queue\n'
    assert commits(ready_repo) == before + 1
    item = backlog_items.find(ready_repo, "b1")
    assert backlog_lines.read(item, "b1.md")[0].terms == [FROB, TWIDDLE]


def test_one_term_is_said_as_before(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--term", FROB)
    assert done.stdout == 'b1 "Fix the parser": a term of work-queue\n', done.stderr


def test_a_bad_term_among_several_writes_none(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--term", FROB, "--term", "- frobnicate")
    assert done.returncode == 1 and "- frobnicate" in done.stderr, done.stderr
    assert state(ready_repo) == before


@pytest.fixture
def modelled(backlog_repo):
    shutil.rmtree(backlog_repo / "spec")
    shutil.copytree(FIXTURE / "spec", backlog_repo / "spec")
    git(backlog_repo, "add", "-A")
    git(backlog_repo, "commit", "-q", "-m", "the domain-model fixture")
    write_item(backlog_repo, "b1", status="shaped")
    return backlog_repo


def test_two_vocabulary_entries_in_one_run_are_one_commit(modelled):
    declared = work(modelled, "line", "b1", "--into", "notebook", "--model", DECLARED)    # their elements (b810)
    assert declared.returncode == 0, declared.stderr
    before = commits(modelled)
    done = work(modelled, "line", "b1", "--into", "notebook", "--term", PIN, "--term", SHELF)
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": 2 vocabulary entries of notes\n'
    assert commits(modelled) == before + 1
    blocks = backlog_section.read(backlog_items.find(modelled, "b1"), "b1")
    assert blocks.models[0].terms == (PIN, SHELF)


def test_a_bad_vocabulary_entry_among_several_writes_none(modelled):
    before = state(modelled)
    done = work(modelled, "line", "b1", "--into", "notebook", "--term", PIN, "--term", "- **pin** (verb): no element.")
    assert done.returncode == 1 and "→ <element>" in done.stderr, done.stderr
    assert state(modelled) == before
