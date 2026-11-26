"""batch_reached (b707, b758, b763; batches r157): a workspace whose change since its HEAD touches grammar 4's inputs
(`reached`) has the features and corpus blocks it reaches beyond the laid capabilities written again (`prepared`), and
one whose change touches none has nothing written."""
import shutil
import subprocess
from pathlib import Path

import batch_reached
import pytest
import spec_corpus_write
import spec_held
import toolchain

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "domain-model"
LINE = "When the person lists the notes, the notes service shall complete the request."
STALE = "## r6\nKept.\n\n```reading\n%s\nshall []\n```\n" % LINE
KEPT = "## U1\nKept.\n\n```reading\nthe line\nshall []\n```\n"


def _git(root, *args):
    subprocess.run(["git", *args], cwd=str(root), check=True, capture_output=True)


def _context(tmp_path):
    """The fixture with a corpus, committed, so that its change since HEAD is what a test makes."""
    root = tmp_path / "ctx"
    shutil.copytree(FIXTURE, root)
    corpus = root / spec_corpus_write.CORPUS
    corpus.mkdir(parents=True)
    (corpus / "notebook.md").write_text("# notebook\n\n" + STALE)
    (corpus / "legacy.md").write_text("# legacy\n\n" + KEPT)       # no capability of it: left as it is
    (root / "notes.txt").write_text("kept\n")
    _git(root, "init", "-q")
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "fixture")
    return root, corpus


def _touch(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text((path.read_text() if path.is_file() else "# added\n") + "\n")


def test_reached_by_nothing_when_the_workspace_is_unchanged(tmp_path):
    root, _ = _context(tmp_path)
    assert not batch_reached.reached(root)


def test_reached_not_by_a_change_of_an_unrelated_file(tmp_path):
    root, _ = _context(tmp_path)
    _touch(root / "notes.txt")
    _touch(root / "features" / "notebook.feature")
    _touch(root / "spec" / "capabilities" / "notebook.md")          # a context with a domain model reads none
    assert not batch_reached.reached(root)


@pytest.mark.parametrize("path", ["spec/index.md", "spec/universal.md", "spec/model/notes.md",
                                  "spec/vocabulary/notes.md", "spec/vocabulary/added.md", "spec/packs/household.md",
                                  "provider/stock/contract.toml"])
def test_reached_by_a_change_of_each_input(tmp_path, path):
    root, _ = _context(tmp_path)
    _touch(root / path)
    assert batch_reached.reached(root)


def test_reached_by_a_capability_of_a_context_with_no_domain_model(tmp_path):
    root, _ = _context(tmp_path)
    shutil.rmtree(root / "spec" / "model")
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "no model")
    _touch(root / "spec" / "capabilities" / "notebook.md")
    assert batch_reached.reached(root)


@pytest.mark.parametrize("name", ["packs/cli.md", "Base.gf"])
def test_reached_by_the_plugins_pack_and_grammar_under_the_tree(tmp_path, monkeypatch, name):
    root, _ = _context(tmp_path)
    grammar = root / "grammar"
    monkeypatch.setattr(spec_held, "GRAMMARS", grammar)              # the workspace is the plugin's own repository
    monkeypatch.setattr(spec_held, "PACKS", grammar / "packs")
    _touch(grammar / name)
    assert batch_reached.reached(root)


def test_prepared_writes_nothing_when_unreached(tmp_path):
    root, corpus = _context(tmp_path)
    feature = root / "features" / "notebook.feature"
    feature.write_text("stale\n")
    assert batch_reached.prepared(root, set()) == []
    assert feature.read_text() == "stale\n"
    assert (corpus / "notebook.md").read_text() == "# notebook\n\n" + STALE


def test_prepared_writes_each_reached_feature_and_block_again(tmp_path):
    toolchain.require()
    root, corpus = _context(tmp_path)
    feature = root / "features" / "notebook.feature"
    was = feature.read_text()
    _touch(root / "spec" / "vocabulary" / "notes.md")
    feature.write_text("stale\n")
    changed = batch_reached.prepared(root, set())
    assert changed == ["features/notebook.feature", spec_corpus_write.CORPUS + "/notebook.md"]
    assert feature.read_text() == was
    want = "## r6\nKept.\n\n```reading\n%s\n%s\n```\n" % (LINE, spec_corpus_write.form(root, LINE))
    assert (corpus / "notebook.md").read_text() == "# notebook\n\n" + want
    assert (corpus / "legacy.md").read_text() == "# legacy\n\n" + KEPT


def test_prepared_leaves_a_laid_capability_to_the_lay(tmp_path):
    toolchain.require()
    root, _ = _context(tmp_path)
    _touch(root / "spec" / "index.md")
    feature = root / "features" / "notebook.feature"
    feature.write_text("stale\n")
    assert "features/notebook.feature" not in batch_reached.prepared(root, {"notebook"})
    assert feature.read_text() == "stale\n"


def test_reached_by_an_input_taken_out(tmp_path):
    root, _ = _context(tmp_path)
    (root / "spec" / "vocabulary" / "notes.md").unlink()
    assert batch_reached.reached(root)


def _committed(root, path):
    _touch(root / path)
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "one input")


@pytest.mark.parametrize("path", ["spec/packs/household.md", "provider/stock/contract.toml"])
def test_reached_by_an_input_taken_out_when_it_was_the_last_of_its_folder(tmp_path, path):
    root, _ = _context(tmp_path)
    _committed(root, path)                                           # the one pack, the one provider contract
    (root / path).unlink()
    assert batch_reached.reached(root)
