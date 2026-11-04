"""backlog r6-r8, r17: `work backlog` prints every item in a table by state, in rank order, with what each waits on
(its blockers and its question), and as one JSON object (workflow simplification plan 2, Task 4, D7-D9)."""
import json
import re

import backlog_items
import backlog_view
import pytest
from backlog_testing import state, work, write_item

RATED = {"value": "medium-value", "urgency": "medium-urgency", "size": "medium"}


def item(name="b1", **fields):
    return backlog_items.Item(name=name, ident="item/x/" + name, title="T " + name,
                              status=fields.pop("status", "shaped"), provenance="own", **fields)


def rows(stdout):
    return [line for line in stdout.splitlines() if re.match(r"\| \d+ \|", line)]


def row(stdout, name):
    return next(line for line in rows(stdout) if line.split("|")[2].strip() == name)


def test_score_is_value_plus_urgency_over_size():
    assert backlog_view.score(item(value="high-value", urgency="medium-urgency", size="small")) == 5.0
    assert backlog_view.score(item(value="low-value", urgency="low-urgency", size="large")) == pytest.approx(2 / 3)
    assert backlog_view.score(item(value="high-value", urgency="high-urgency")) is None


def test_rank_breaks_ties_by_the_item_added_first():
    found = backlog_view.ordered([item("b5", **RATED), item("b1"), item("b2", **RATED)])
    assert [(state, [i.name for i in its]) for state, its in found] == [("shaped", ["b2", "b5", "b1"])]


def test_a_higher_score_ranks_first():
    found = backlog_view.ordered([item("b1", **RATED), item("b2", **dict(RATED, value="high-value"))])
    assert [i.name for i in found[0][1]] == ["b2", "b1"]


def test_tables_come_in_state_order_and_skip_empty_states(backlog_repo):
    write_item(backlog_repo, "b1", status="idea")
    write_item(backlog_repo, "b2", status="ready")
    write_item(backlog_repo, "b3", status="in-batch")
    done = work(backlog_repo, "backlog")
    assert done.returncode == 0, done.stderr
    headings = re.findall(r"^## (\S+) \((\d+)\)$", done.stdout, re.MULTILINE)
    assert headings == [("in-batch", "1"), ("ready", "1"), ("idea", "1")]


def test_every_column_of_a_row(backlog_repo):
    write_item(backlog_repo, "b4", status="needs-input", value="high-value", urgency="medium-urgency", size="small",
               body="\n## Question\n\nWhich reading holds, the first or the second?\nThe second line.\n")
    done = work(backlog_repo, "backlog")
    assert done.stdout == (
        "## needs-input (1)\n\n"
        "| rank | item | title | provenance | value | urgency | size | score | waiting on |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| 1 | b4 | Fix the parser | own | high-value | medium-urgency | small | 5.00 | "
        "question: Which reading holds, the first or the second? |\n")


def test_a_blocked_item_names_its_blocker_in_its_row(backlog_repo):
    write_item(backlog_repo, "b1", status="idea")
    write_item(backlog_repo, "b2", title="Use it", status="idea", depends_on="b1")
    done = work(backlog_repo, "backlog")
    assert 'blocked by b1 "Fix the parser" (idea)' in row(done.stdout, "b2")
    assert "blocked by" not in row(done.stdout, "b1")
    write_item(backlog_repo, "b1", status="delivered")
    assert "blocked by" not in row(work(backlog_repo, "backlog").stdout, "b2")


def test_a_dependency_on_a_missing_or_withdrawn_item_blocks_with_its_status(backlog_repo):
    write_item(backlog_repo, "b1", depends_on="b9, b3")
    write_item(backlog_repo, "b3", title="Gone", status="withdrawn")
    done = work(backlog_repo, "backlog")
    assert done.returncode == 0, done.stderr
    assert row(done.stdout, "b1").split("|")[9].strip() == 'blocked by b9 (missing); blocked by b3 "Gone" (withdrawn)'


def test_backlog_prints_a_hand_written_cycle(backlog_repo):
    write_item(backlog_repo, "b1", depends_on="b2")
    write_item(backlog_repo, "b2", title="Other", depends_on="b1")
    done = work(backlog_repo, "backlog")
    assert done.returncode == 0, done.stderr
    assert 'blocked by b2 "Other"' in row(done.stdout, "b1")
    assert 'blocked by b1 "Fix the parser"' in row(done.stdout, "b2")


def test_a_pipe_in_a_title_keeps_the_columns(backlog_repo):
    write_item(backlog_repo, "b1", title="a | b")
    line = row(work(backlog_repo, "backlog").stdout, "b1")
    assert len(re.findall(r"(?<!\\)\|", line)) == 10 and r"a \| b" in line


def test_needs_input_prints_the_first_line_of_its_question(backlog_repo):
    write_item(backlog_repo, "b1", status="needs-input", body="\n## Question\n\nFirst?\nSecond.\n")
    line = row(work(backlog_repo, "backlog").stdout, "b1")
    assert line.endswith("| question: First? |") and "Second" not in line


def test_json_is_one_object_in_table_order(backlog_repo):
    write_item(backlog_repo, "b1", status="idea")
    write_item(backlog_repo, "b2", status="shaped", **RATED)
    done = work(backlog_repo, "backlog", "--json")
    got = json.loads(done.stdout)
    assert [i["id"] for i in got["items"]] == ["b2", "b1"]
    assert got["items"][1]["score"] is None and got["items"][0]["score"] == 2.0
    assert set(got["items"][0]) == {"id", "title", "status", "provenance", "value", "urgency", "size", "score", "rank",
                                    "depends_on", "blocked_by", "question"}


def test_show_json_has_the_row_keys(backlog_repo):
    write_item(backlog_repo, "b1", depends_on="b9")
    got = json.loads(work(backlog_repo, "show", "b1", "--json").stdout)["item"]
    assert got["rank"] == 1 and got["blocked_by"] == [{"id": "b9", "status": "missing"}]


def test_an_empty_backlog(backlog_repo):
    assert work(backlog_repo, "backlog").stdout == "the backlog is empty\n"
    done = work(backlog_repo, "backlog", "--json")
    assert done.returncode == 0 and json.loads(done.stdout) == {"items": []}


def test_backlog_commits_nothing_and_refuses_a_malformed_item(backlog_repo):
    write_item(backlog_repo, "b1", status="doing")
    before = state(backlog_repo)
    done = work(backlog_repo, "backlog")
    assert done.returncode == 1 and ".shop/backlog/b1.md" in done.stderr and "status" in done.stderr
    assert state(backlog_repo) == before
