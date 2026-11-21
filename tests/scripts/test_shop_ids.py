"""An item's or a batch's id resolved to its file (b49): held by its file and its frontmatter id, its short form in
this context; and a record about one names something in `spec`'s facts."""
from model_facts import Model
from shop_ids import held

PATH = "ex.com/prod/ctx"


def thing(repo, rel, ident):
    (repo / rel).parent.mkdir(parents=True, exist_ok=True)
    (repo / rel).write_text("---\nid: %s\n---\n\n# x\n" % ident)


def test_an_item_and_a_batch_are_held_by_their_files(tmp_path):
    thing(tmp_path, ".shop/backlog/b3.md", "item/%s/b3" % PATH)
    thing(tmp_path, ".shop/batches/7/plan.md", "batch/%s/batch-7" % PATH)
    for ident in ("item/%s/b3" % PATH, "item/b3", "batch/%s/batch-7" % PATH, "batch/batch-7"):
        assert held(tmp_path, ident, PATH), ident
    for ident in ("item/%s/b4" % PATH, "batch/batch-8", "item/other/prod/ctx/b3", "capability/b3", "item/"):
        assert not held(tmp_path, ident, PATH), ident


def test_a_file_of_another_id_holds_nothing(tmp_path):
    thing(tmp_path, ".shop/backlog/b3.md", "item/%s/b9" % PATH)
    assert not held(tmp_path, "item/b3", PATH)


def test_a_record_about_an_item_names_something(backlog_repo):
    thing(backlog_repo, ".shop/backlog/b3.md", "item/%s/b3" % PATH)
    (backlog_repo / ".shop/records").mkdir()
    for n, about in enumerate(("item/%s/b3" % PATH, "item/%s/b4" % PATH)):
        (backlog_repo / (".shop/records/2026-11-05-r%d.md" % n)).write_text(
            "---\nid: record/%s/2026-11-05-r%d\nkind: analysis\nabout: %s\ndate: 2026-11-05\n---\n\n# r\n"
            % (PATH, n, about))
    dangling = Model(backlog_repo).read().dangling
    assert not any("/b3 " in d for d in dangling) and any("/b4 names nothing" in d for d in dangling), dangling
