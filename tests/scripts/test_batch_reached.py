"""batch_reached (b707, batches r157): a lay that changes grammar 4's inputs writes again the features and corpus
blocks it reaches beyond the laid capabilities, and a lay that changes none writes nothing."""
import shutil
from pathlib import Path

import batch_reached
import spec_corpus_write
import toolchain

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "domain-model"
LINE = "When the person lists the notes, the notes service shall complete the request."
STALE = "## r6\nKept.\n\n```reading\n%s\nshall []\n```\n" % LINE
KEPT = "## U1\nKept.\n\n```reading\nthe line\nshall []\n```\n"


def _context(tmp_path):
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
    corpus = root / spec_corpus_write.CORPUS
    corpus.mkdir(parents=True)
    (corpus / "notebook.md").write_text("# notebook\n\n" + STALE)
    (corpus / "legacy.md").write_text("# legacy\n\n" + KEPT)       # no capability of it: left as it is
    return root, corpus


def test_a_lay_that_changes_no_input_writes_nothing(tmp_path):
    root, corpus = _context(tmp_path)
    (root / "features" / "notebook.feature").write_text("stale\n")
    assert batch_reached.regenerated(root, batch_reached.digest(root), set()) == []
    assert (corpus / "notebook.md").read_text() == "# notebook\n\n" + STALE


def test_a_lay_that_changes_an_input_writes_each_reached_feature_and_block_again(tmp_path):
    toolchain.require()
    root, corpus = _context(tmp_path)
    before = batch_reached.digest(root)
    vocabulary = root / "spec" / "vocabulary" / "notes.md"
    vocabulary.write_text(vocabulary.read_text() + "\n")
    feature = root / "features" / "notebook.feature"
    was = feature.read_text()
    feature.write_text("stale\n")
    changed = batch_reached.regenerated(root, before, set())
    assert changed == ["features/notebook.feature", spec_corpus_write.CORPUS + "/notebook.md"]
    assert feature.read_text() == was
    want = "## r6\nKept.\n\n```reading\n%s\n%s\n```\n" % (LINE, spec_corpus_write.form(root, LINE))
    assert (corpus / "notebook.md").read_text() == "# notebook\n\n" + want
    assert (corpus / "legacy.md").read_text() == "# legacy\n\n" + KEPT


def test_a_laid_capability_is_left_to_the_lay(tmp_path):
    toolchain.require()
    root, _ = _context(tmp_path)
    before = batch_reached.digest(root)
    (root / "spec" / "index.md").write_text((root / "spec" / "index.md").read_text() + "\n")
    feature = root / "features" / "notebook.feature"
    feature.write_text("stale\n")
    assert "features/notebook.feature" not in batch_reached.regenerated(root, before, {"notebook"})
    assert feature.read_text() == "stale\n"
