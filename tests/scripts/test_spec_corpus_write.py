"""The corpus blocks `work batch start` writes (b333): a block placed in id order, one of the same id replaced, a
retired id's taken out; a bounded context with no `grammar/corpus/spec/` keeps no corpus; and the batch brief names a
catalogue the lay could not write."""
import spec_corpus_write as corpus

HEAD = "# queue: every live line with its intended reading\n"
R2 = corpus.block("r2", "Kept.", "line two", "shall []")
R9 = corpus.block("r9", "Kept.", "line nine", "shall []")


def test_a_block_goes_before_the_first_of_a_higher_id():
    text = corpus.with_block(HEAD + "\n" + R2 + R9, "r5", corpus.block("r5", "From: b7 r5.", "line five", "shall []"))
    assert text.index("## r2") < text.index("## r5") < text.index("## r9")


def test_a_block_of_a_higher_id_than_any_goes_at_the_end():
    text = corpus.with_block(HEAD + "\n" + R2.rstrip("\n") + "\n", "r12", corpus.block("r12", "From: b7 r12.", "x", "y"))
    assert text.endswith("```\n\n## r12\nFrom: b7 r12.\n\n```reading\nx\ny\n```\n")


def test_a_block_of_the_same_id_is_replaced_and_a_retired_one_taken_out():
    text = corpus.with_block(HEAD + "\n" + R2 + R9, "r2", corpus.block("r2", "From: b7 r2.", "new", "shall []"))
    assert text.count("## r2") == 1 and "new" in text and "line two" not in text
    assert "## r9" not in corpus.without_block(text, "r9")


def test_the_last_block_replaced_in_place_leaves_no_blank_line_at_the_end():
    last = HEAD + "\n" + R2 + R9.rstrip("\n") + "\n"
    text = corpus.with_block(last, "r9", corpus.block("r9", "From: b7 r9.", "new", "shall []"))
    assert text.endswith("```reading\nnew\nshall []\n```\n") and "line two" in text
    assert corpus.without_block(text, "r2").endswith("```\n") and not text.endswith("\n\n")


def test_a_context_with_no_corpus_keeps_none(tmp_path):
    assert corpus.write(tmp_path, []) == [] and not (tmp_path / "grammar").exists()


def test_the_brief_names_a_catalogue_the_lay_could_not_write(tmp_path, monkeypatch):
    import batch_driver
    from batch_plan import Batch
    monkeypatch.setattr(batch_driver, "push_prefix", lambda root: None)
    batch = Batch(name="batch-1", ident="batch/x/batch-1", status="building", base="main", forked_from="0",
                  branch="batch-1", pull_request=None, tasks=[])
    text = batch_driver.text(tmp_path, batch, [], ["grammar/constructs.md: F is no construct's function"])
    assert "## The lay's bookkeeping" in text
    assert "- Not written, for the task of the item that brings it to mend: grammar/constructs.md: F is no" in text
