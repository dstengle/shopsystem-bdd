"""`work line --import`, `--retire-model` and `--retire-term` (b672): the item's `### imports` and `### retirements`
blocks kept and read back byte for byte, a second import or retirement of one thing refused; laid over the spec (the
import into spec/index.md, the element and the entries that mean it, the term) and taken out again, the spec as it was."""
import backlog_items
import backlog_lines
import backlog_section
import pytest
from backlog_testing import git, work
from test_backlog_terms import modelled  # noqa: F401  (the fixture)

FILES = ("spec/index.md", "spec/model/notes.md", "spec/vocabulary/notes.md", "spec/vocabulary/shared.md")


def _item(repo):
    return backlog_items.find(repo, "b1")


def _given(repo):
    for args in (["--import", "time"], ["--into", "notebook", "--retire-model", "object tag"],
                 ["--retire-term", "low"]):
        done = work(repo, "line", "b1", *args)
        assert done.returncode == 0, done.stderr


def test_the_blocks_are_kept_and_read_back(modelled):  # noqa: F811
    _given(modelled)
    blocks = backlog_section.read(_item(modelled), "b1")
    assert blocks.imports == ["time"]
    assert [tuple(r) for r in blocks.retirements] == [("model line", "object tag", "notes"),
                                                       ("term", "low → value note.priority low", "notes")]
    text = _item(modelled).sections["Requirements"]
    assert backlog_section.render(blocks) == text
    assert "### imports\n\n- pack `time`\n\n### retirements\n\n- model line `object tag` in notes" in text


def test_a_second_import_or_retirement_is_refused(modelled):  # noqa: F811
    _given(modelled)
    for args in (["--import", "time"], ["--retire-term", "low"]):
        done = work(modelled, "line", "b1", *args)
        assert done.returncode == 1 and "usage:" not in done.stderr, (args, done.stderr)


def test_the_import_of_a_pack_the_index_imports_is_kept(modelled):  # noqa: F811
    """drafting r73: `request`, which spec/index.md imports already, kept in the item and laid once."""
    _given(modelled)
    done = work(modelled, "line", "b1", "--import", "request")
    assert done.returncode == 0, done.stderr
    assert backlog_section.read(_item(modelled), "b1").imports == ["time", "request"]
    backlog_lines.lay_onto(modelled, _item(modelled), [])
    assert "imports: [request, time]" in (modelled / "spec/index.md").read_text()


@pytest.mark.parametrize("at_base", [True, False])
def test_the_lay_takes_out_and_the_unlay_puts_back(modelled, at_base):  # noqa: F811
    """With the batch's base, or none (the latest version git holds of each file)."""
    _given(modelled)
    base = git(modelled, "rev-parse", "HEAD").strip() if at_base else None
    before = {rel: (modelled / rel).read_text() for rel in FILES}
    files = []
    backlog_lines.lay_onto(modelled, _item(modelled), files)
    assert "imports: [request, time]" in (modelled / "spec/index.md").read_text()
    model = (modelled / "spec/model/notes.md").read_text().split("\n")
    assert "object tag" not in model and "  relations: of → note (one)" not in model
    words = (modelled / "spec/vocabulary/notes.md").read_text()
    assert "- **tag** (noun)" not in words and "- **low**" not in words and "- **high**" in words
    backlog_lines.unlay(modelled, _item(modelled), [], base)
    assert {rel: (modelled / rel).read_text() for rel in FILES} == before
