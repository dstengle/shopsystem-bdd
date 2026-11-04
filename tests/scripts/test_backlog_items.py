"""backlog r1, r15: an item's file in .shop/backlog/, `work idea` writing one, and `work show` naming it by its title
(workflow simplification plan 2, Task 1)."""
import json

import backlog_items
import pytest
import workqueue
import workqueue_list
from backlog_testing import git, state, work, write_item


def test_idea_writes_b1_and_commits_only_it(backlog_repo):
    done = work(backlog_repo, "idea", "Fix the parser")
    assert done.returncode == 0, done.stderr
    assert 'b1 "Fix the parser"' in done.stdout
    rel = ".shop/backlog/b1.md"
    item = backlog_items.parse((backlog_repo / rel).read_text(), rel)
    assert (item.status, item.provenance, item.value, item.depends_on) == ("idea", "own", None, ())
    assert item.title == "Fix the parser" and item.ident == "item/ex.com/prod/ctx/b1"
    assert git(backlog_repo, "show", "--name-only", "--format=", "HEAD").split() == [rel]
    assert git(backlog_repo, "status", "--porcelain") == ""


def test_idea_keeps_its_note_and_provenance(backlog_repo):
    assert work(backlog_repo, "idea", "Fix it", "--provenance", "peer", "--note", "seen twice").returncode == 0
    item = backlog_items.find(backlog_repo, "b1")
    assert item.provenance == "peer" and "seen twice" in item.sections["Notes"]


def test_idea_numbers_one_above_the_highest(backlog_repo):
    write_item(backlog_repo, "b1")
    write_item(backlog_repo, "b7")
    done = work(backlog_repo, "idea", "Another")
    assert done.returncode == 0, done.stderr
    assert (backlog_repo / ".shop/backlog/b8.md").is_file()


@pytest.mark.parametrize("title", ["", "  ", "a\nb"])
def test_idea_refuses_an_empty_or_multi_line_title(backlog_repo, title):
    before = state(backlog_repo)
    done = work(backlog_repo, "idea", title)
    assert done.returncode == 1 and done.stderr.startswith("work: "), done.stderr
    assert state(backlog_repo) == before


def test_render_round_trips():
    item = backlog_items.Item(name="b3", ident="item/ex.com/prod/ctx/b3", title="Fix the parser", status="needs-input",
                              provenance="product", value="high-value", urgency="low-urgency", size="small",
                              depends_on=("b1", "b2"), sections={"Notes": "the note", "Question": "Which?"})
    rel = ".shop/backlog/b3.md"
    assert backlog_items.parse(backlog_items.render(item), rel) == item
    assert backlog_items.render(backlog_items.parse(backlog_items.render(item), rel)) == backlog_items.render(item)


def test_an_unrated_item_renders_its_fields_empty():
    item = backlog_items.Item(name="b1", ident="item/x/b1", title="T", status="idea", provenance="own")
    text = backlog_items.render(item)
    assert "\nvalue:\n" in text and "\ndepends_on: []\n" in text
    assert backlog_items.parse(text, "b1.md") == item


@pytest.mark.parametrize("fields, word", [({"status": "doing"}, "status"), ({"value": "huge"}, "value"),
                                          ({"title": ""}, "title"), ({"provenance": "mine"}, "provenance"),
                                          ({"depends_on": "x1"}, "depends_on")])
def test_a_malformed_item_is_refused_naming_the_file_and_field(backlog_repo, fields, word):
    path = write_item(backlog_repo, "b1", **fields)
    if not fields.get("title", "x"):
        path.write_text(path.read_text().replace("\n# \n", "\n"))
        git(backlog_repo, "commit", "-qam", "no heading")
    before = state(backlog_repo)
    done = work(backlog_repo, "show", "b1")
    assert done.returncode == 1, done.stdout
    assert ".shop/backlog/b1.md" in done.stderr and word in done.stderr, done.stderr
    assert "Traceback" not in done.stderr
    assert state(backlog_repo) == before


def test_show_names_the_item_by_its_title(backlog_repo):
    write_item(backlog_repo, "b1", value="high-value")
    done = work(backlog_repo, "show", "b1")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines()[0].startswith('b1 "Fix the parser"'), done.stdout
    shown = json.loads(work(backlog_repo, "show", "b1", "--json").stdout)
    assert shown["item"]["title"] == "Fix the parser" and shown["item"]["id"] == "b1"
    assert shown["item"]["value"] == "high-value" and shown["item"]["urgency"] is None


def test_show_refuses_an_item_there_is_not(backlog_repo):
    done = work(backlog_repo, "show", "b4")
    assert done.returncode == 1 and "b4" in done.stderr


def test_show_of_a_work_item_is_unchanged(backlog_repo, capsys):
    path = backlog_repo / ".shop/work/i1/w1.md"
    path.parent.mkdir(parents=True)
    path.write_text("---\nid: work-item/ex.com/prod/ctx/w1\nkind: work-item\npart_of: initiative/i1\n"
                    "status: drafted\nunder: thing\ncheck: true\n---\n\n# w1\n")
    done = work(backlog_repo, "show", "w1")
    assert workqueue_list.show(backlog_repo, "w1", False) == 0
    assert done.stdout == capsys.readouterr().out and done.returncode == 0


def test_label_names_the_item_by_id_and_title():
    item = backlog_items.Item(name="b3", ident="item/x/b3", title="Fix the parser", status="idea", provenance="own")
    assert backlog_items.label(item) == 'b3 "Fix the parser"'
    assert backlog_items.is_item("b3") and not backlog_items.is_item("b0") and not backlog_items.is_item("w3")


def test_find_refuses_a_missing_item(backlog_repo):
    with pytest.raises(workqueue.Refused, match="there is no item b2 in .shop/backlog/"):
        backlog_items.find(backlog_repo, "b2")
