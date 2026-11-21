"""`work line --remove-model`, `--reword-model`, `--remove-term` and `--reword-term` (b367): an item's own model line
(an element with its members, or only some members) or term taken out or reworded, one commit of the item; one the
item does not hold refused, naming it and changing nothing."""
import backlog_items
import backlog_section
from backlog_testing import git, state, work
from test_backlog_terms import modelled  # noqa: F401  (the fixture)

FOLDER = "object folder\n  attributes: name (text)\n  relations: holds → note (many)"
SHELF = "object shelf\n  attributes: label (text)"
REMOVE = "- **remove** (verb, action) → operation notes.archive. Forms: removes, removed. Frame: <actor> removes <note>."
DROP = "- **remove** (verb, action) → operation notes.file. Forms: removes, removed. Frame: <actor> removes <note>."


def _models(repo):
    return backlog_section.read(backlog_items.find(repo, "b1"), "b1").models


def _given(repo):
    assert work(repo, "line", "b1", "--into", "notebook", "--model", FOLDER + "\n" + SHELF).returncode == 0
    assert work(repo, "line", "b1", "--into", "notebook", "--term", REMOVE, "--term", DROP).returncode == 0


def test_an_element_goes_with_its_members_in_one_commit(modelled):  # noqa: F811
    _given(modelled)
    done = work(modelled, "line", "b1", "--remove-model", "object folder")
    assert done.returncode == 0 and done.stdout == 'b1 "Fix the parser": model line object folder removed\n', \
        done.stderr
    assert _models(modelled)[0].lines == tuple(SHELF.split("\n"))
    assert git(modelled, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]


def test_member_lines_alone_go_and_the_element_stays(modelled):  # noqa: F811
    _given(modelled)
    done = work(modelled, "line", "b1", "--remove-model", "object folder\n  relations: holds → note (many)")
    assert done.returncode == 0, done.stderr
    assert _models(modelled)[0].lines == ("object folder", "  attributes: name (text)", "") + tuple(SHELF.split("\n"))


def test_reword_puts_the_new_lines_in_place(modelled):  # noqa: F811
    _given(modelled)
    done = work(modelled, "line", "b1", "--reword-model", "object folder", "object folder\n  attributes: title (text)")
    assert done.returncode == 0, done.stderr
    assert _models(modelled)[0].lines[:2] == ("object folder", "  attributes: title (text)")
    assert work(modelled, "line", "b1", "--reword-model", "object shelf", "object shelf\n  bogus").returncode == 1


def test_a_term_by_its_word_and_element_and_its_block_goes_when_empty(modelled):  # noqa: F811
    _given(modelled)
    done = work(modelled, "line", "b1", "--remove-term", "remove")
    assert done.returncode == 1 and "notes.file" in done.stderr, done.stderr
    assert work(modelled, "line", "b1", "--remove-term", "remove → operation notes.file").returncode == 0
    assert _models(modelled)[0].terms == (REMOVE,)
    done = work(modelled, "line", "b1", "--reword-term", "remove", "--", DROP)
    assert done.returncode == 0, done.stderr
    assert _models(modelled)[0].terms == (DROP,)
    for args in (("--remove-term", "remove"), ("--remove-model", "object folder"), ("--remove-model", "object shelf")):
        assert work(modelled, "line", "b1", *args).returncode == 0, args
    assert _models(modelled) == []


def test_what_the_item_does_not_hold_is_refused_changing_nothing(modelled):  # noqa: F811
    _given(modelled)
    before = state(modelled)
    for args, named in ((("--remove-model", "object box"), "object box"),
                        (("--remove-model", "object shelf\n  attributes: size (text)"), "attributes: size (text)"),
                        (("--reword-model", "object box", SHELF), "object box"),
                        (("--remove-term", "shelf"), "shelf"),
                        (("--reword-term", "shelf", "--", REMOVE), "shelf")):
        done = work(modelled, "line", "b1", *args)
        assert done.returncode == 1 and named in done.stderr and "usage:" not in done.stderr, (args, done.stderr)
    for args in (("--remove-model", "object shelf", "--remove-term", "remove"), ("--remove-term", "remove", "x"),
                 ("--remove-term", "remove", "--into", "notebook"), ("--reword-model", "object shelf")):
        assert work(modelled, "line", "b1", *args).returncode == 1, args
    assert state(modelled) == before
