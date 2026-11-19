"""The records policy (the domain contract design, §8): an item's `source:` cites quotes, requests and decisions,
never a record. v_r1 on an item numbered from backlog_items.RECORDS_POLICY, refused by backlog_items; w_r1, history
kept as it is, on an older one."""
import backlog_items
import model_check
import model_facts
import pytest
from shop_refused import Refused

ITEM = """---
id: item/ex/prod/ctx/b{n}
kind: item
status: idea
provenance: own
value:
urgency:
size:
depends_on: []
source: [{source}]
---

# An item
"""
RECORD = "record/ex/prod/ctx/2026-11-19-plan"


def _repo(tmp_path, items):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text("---\nid: bounded-context/ex/prod/ctx\nlanguage: codified-2\n"
                                                "imports: []\n---\n\n# ctx\n")
    backlog = tmp_path / ".shop" / "backlog"
    backlog.mkdir(parents=True)
    for n, source in items:
        (backlog / ("b%d.md" % n)).write_text(ITEM.format(n=n, source=source))
    found, _ = model_check.solve(model_facts.Model(tmp_path).read())
    return [(name, args[0]) for name, args in found if name in ("v_r1", "w_r1")]


def test_a_new_item_citing_a_record_is_a_violation_and_an_old_one_a_warning(tmp_path):
    new, old = backlog_items.RECORDS_POLICY, backlog_items.RECORDS_POLICY - 1
    found = _repo(tmp_path, [(new, RECORD), (old, RECORD)])
    assert sorted(found) == [("v_r1", "item/ex/prod/ctx/b%d" % new), ("w_r1", "item/ex/prod/ctx/b%d" % old)]


def test_an_item_citing_a_quote_or_a_decision_is_no_problem(tmp_path):
    n = backlog_items.RECORDS_POLICY
    assert _repo(tmp_path, [(n, "quote-56, design-decision/ex/prod/ctx/final-layout")]) == []


def test_backlog_items_refuses_a_record_on_a_new_item():
    text = ITEM.format(n=backlog_items.RECORDS_POLICY, source=RECORD)
    with pytest.raises(Refused, match="source names the record"):
        backlog_items.parse(text, ".shop/backlog/b%d.md" % backlog_items.RECORDS_POLICY)
    with pytest.raises(Refused, match="source names the record"):
        backlog_items.parse(text.replace(RECORD, ".shop/records/2026-11-19-plan.md"), "b.md")


def test_an_older_items_record_is_read_and_kept():
    n = backlog_items.RECORDS_POLICY - 1
    item = backlog_items.parse(ITEM.format(n=n, source=RECORD), ".shop/backlog/b%d.md" % n)
    assert item.source == (RECORD,)
    assert backlog_items.parse(backlog_items.render(item), "x") == item


def test_this_repositorys_items_cite_no_record_in_their_source():
    import pathlib
    root = pathlib.Path(__file__).resolve().parents[2]
    assert all(not item.source for item in backlog_items.items(root))
