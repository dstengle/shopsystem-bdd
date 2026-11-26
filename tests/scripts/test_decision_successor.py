"""decision_successor (b741, batches r173, r174; b750, r177, r178): an accepted decision items' retirements leave unenforced is
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


SECOND = (ITEM.replace("b7", "b8").replace("Retire it", "Retire the other").replace("[r1]", "[r2]")
          .replace("[r5 r1]", "[r6 r2]").replace("[g4]", "[g5]").replace("[r5]", "[r6]"))
JOINT = "spec/decisions/0003-kept-in-order-b7.md"


def two(tmp_path):
    root, first = tree(tmp_path)
    (root / "spec/decisions/0002-other.md").write_text(OTHER.replace("work-queue#r2", "work-queue#r3"))
    return root, first, backlog_items.parse(SECOND, ".shop/backlog/b8.md")


def test_two_items_retiring_ids_of_one_decision_give_one_successor(tmp_path):
    root, first, second = two(tmp_path)
    written = []
    decision_successor.lay(root, [first, second], written)
    assert decision_successor.said(written) == [
        'b7 "Retire it": %s supersedes design-decision/ex.com/prod/ctx/kept-in-order' % JOINT,
        'b8 "Retire the other": %s supersedes design-decision/ex.com/prod/ctx/kept-in-order' % JOINT]
    data, body = frontmatter((root / JOINT).read_text())
    assert data["enforced_by"] == ["work-queue#r5", "work-queue#r6"]
    assert data["source"] == ["item/ex.com/prod/ctx/b7", "item/ex.com/prod/ctx/b8"]
    assert data["by"] == "the lay of item/ex.com/prod/ctx/b7, item/ex.com/prod/ctx/b8"
    assert sorted(p.name for p in (root / "spec/decisions").glob("*.md")) == [
        "0001-kept-in-order.md", "0002-other.md", "0003-kept-in-order-b7.md", "index.md"]
    assert set(decision_successor.entries(body)) == {"item/ex.com/prod/ctx/b7", "item/ex.com/prod/ctx/b8"}


def test_the_unlay_of_one_keeps_the_successor_with_the_others_lines(tmp_path):
    root, first, second = two(tmp_path)
    decision_successor.lay(root, [first, second])
    assert JOINT in decision_successor.unlay(root, [first])
    data, _ = frontmatter((root / JOINT).read_text())
    assert data["enforced_by"] == ["work-queue#r1", "work-queue#r6"]
    assert data["source"] == ["item/ex.com/prod/ctx/b8"]
    assert frontmatter((root / "spec/decisions/0001-kept-in-order.md").read_text())[0]["status"] == "superseded"
    decision_successor.unlay(root, [second])
    assert not (root / JOINT).exists()
    assert (root / "spec/decisions/0001-kept-in-order.md").read_text() == OLD


def test_a_relay_lays_the_item_into_the_successor_of_the_batch(tmp_path):
    root, first, second = two(tmp_path)
    decision_successor.lay(root, [first, second])
    decision_successor.unlay(root, [first])
    decision_successor.lay(root, [first])
    data, _ = frontmatter((root / JOINT).read_text())
    assert sorted(data["enforced_by"]) == ["work-queue#r5", "work-queue#r6"]
    assert sorted(p.name for p in (root / "spec/decisions").glob("0*.md")) == [
        "0001-kept-in-order.md", "0002-other.md", "0003-kept-in-order-b7.md"]


def test_a_delivered_items_successor_is_superseded_in_its_turn(tmp_path):
    root, first, second = two(tmp_path)
    decision_successor.lay(root, [first])
    (root / ".shop" / "backlog").mkdir(parents=True)
    (root / ".shop/backlog/b7.md").write_text(ITEM.replace("status: in-batch", "status: delivered"))
    decision_successor.lay(root, [second])
    assert frontmatter((root / JOINT).read_text())[0]["status"] == "superseded"
    data, _ = frontmatter((root / "spec/decisions/0004-kept-in-order-b7-b8.md").read_text())
    assert data["enforced_by"] == ["work-queue#r5", "work-queue#r6"]
    assert data["supersedes"] == ["design-decision/ex.com/prod/ctx/kept-in-order-b7"]
