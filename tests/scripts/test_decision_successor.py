"""decision_successor (b741, batches r173, r174): an accepted decision an item's retirement leaves unenforced is
superseded by a successor the lay writes, and the unlay takes the successor out and the decision is accepted again."""
import backlog_items
import decision_successor
from model_parse import frontmatter

INDEX = "---\nid: bounded-context/ex.com/prod/ctx\nlanguage: codified-2\n---\n\n# ctx\n"
OLD = ("---\nid: design-decision/ex.com/prod/ctx/kept-in-order\nsummary: \"Kept in order.\"\ndate: 2026-11-20\n"
       "status: accepted\ntier: requirement\nenforced_by: [work-queue#r1, work-queue#r2]\nverified_by: [scenario]\n---\n\n"
       "# 0001. Kept in order\n\n## Context\n\nOnce.\n\n## Decision\n\nSo it is.\n")
OTHER = OLD.replace("kept-in-order", "other").replace("work-queue#r1, ", "").replace("0001.", "0002.")
ITEM = ("---\nid: item/ex.com/prod/ctx/b7\nkind: item\nstatus: in-batch\nprovenance: own\nvalue: high-value\n"
        "urgency: medium-urgency\nsize: small\ndepends_on: []\n---\n\n# Retire it\n\n## Requirements\n\n"
        "### work-queue\n\nretired: [r1]\nretires: [r5 r1]\n\n#### [g4] A group\n- [r5] A line.\n")


def tree(tmp_path):
    (tmp_path / "spec" / "decisions").mkdir(parents=True)
    (tmp_path / "spec" / "index.md").write_text(INDEX)
    (tmp_path / "spec" / "decisions" / "0001-kept-in-order.md").write_text(OLD)
    (tmp_path / "spec" / "decisions" / "0002-other.md").write_text(OTHER)
    return tmp_path, backlog_items.parse(ITEM, ".shop/backlog/b7.md")


def test_the_lay_supersedes_the_decision_it_leaves_unenforced(tmp_path):
    root, item = tree(tmp_path)
    written = []
    changed = decision_successor.lay(root, [item], written)
    new = "spec/decisions/0003-kept-in-order-b7.md"
    assert sorted(changed) == sorted([new, "spec/decisions/0001-kept-in-order.md", "spec/decisions/index.md"])
    assert decision_successor.said(written) == [
        'b7 "Retire it": %s supersedes design-decision/ex.com/prod/ctx/kept-in-order' % new]
    assert frontmatter((root / "spec/decisions/0001-kept-in-order.md").read_text())[0]["status"] == "superseded"
    assert (root / "spec/decisions/0002-other.md").read_text() == OTHER
    data, body = frontmatter((root / new).read_text())
    assert data == {"id": "design-decision/ex.com/prod/ctx/kept-in-order-b7", "summary": "Kept in order.",
                    "date": data["date"], "status": "accepted", "tier": "requirement",
                    "enforced_by": ["work-queue#r5", "work-queue#r2"], "verified_by": ["scenario"],
                    "supersedes": ["design-decision/ex.com/prod/ctx/kept-in-order"],
                    "source": ["item/ex.com/prod/ctx/b7"], "by": "the lay of item/ex.com/prod/ctx/b7"}
    assert body.startswith("# 0003. Kept in order\n\n## Context\n\nwork-queue#r1, ")
    assert body.endswith("## Decision\n\nSo it is.\n")
    assert "kept-in-order-b7" in (root / "spec/decisions/index.md").read_text()


def test_the_unlay_takes_the_successor_out_and_accepts_the_decision_again(tmp_path):
    root, item = tree(tmp_path)
    decision_successor.lay(root, [item])
    changed = decision_successor.unlay(root, [item])
    assert not (root / "spec/decisions/0003-kept-in-order-b7.md").exists()
    assert (root / "spec/decisions/0001-kept-in-order.md").read_text() == OLD
    assert "spec/decisions/0003-kept-in-order-b7.md" in changed
    assert "kept-in-order-b7" not in (root / "spec/decisions/index.md").read_text()


def test_an_item_that_retires_nothing_changes_nothing(tmp_path):
    root, _ = tree(tmp_path)
    item = backlog_items.parse(ITEM.replace("retired: [r1]\nretires: [r5 r1]\n\n", ""), ".shop/backlog/b7.md")
    assert decision_successor.lay(root, [item]) == [] and decision_successor.unlay(root, [item]) == []
    assert (root / "spec/decisions/0001-kept-in-order.md").read_text() == OLD
