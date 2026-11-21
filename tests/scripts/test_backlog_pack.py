"""backlog_pack (b472): an item's pack block read and written back byte-stable, laid into spec/packs/<name>.md with
the pack imported, and taken out again as laid."""
import backlog_pack
import backlog_section
import pytest
from backlog_items import Refused

INDEX = "---\nid: bounded-context/ex.org/x/y\nlanguage: codified-2\nimports: [request]\n---\n\n# y\n"
TERM = "- **pantry** (noun): a cupboard food is kept in."
SECTION = "### household pack\n\n%s" % TERM


class Item:
    name, status = "b1", "shaped"

    def __init__(self, text):
        self.sections = {"Requirements": text}


def test_block_read_and_rendered_byte_stable():
    blocks = backlog_section.read(Item(SECTION), "b1")
    assert blocks.packs == [backlog_pack.PackBlock("household", (TERM,))]
    assert backlog_section.render(blocks) == SECTION


def test_a_line_of_a_pack_block_that_is_no_term_refused():
    with pytest.raises(Refused, match="no term entry"):
        backlog_section.read(Item(SECTION + "\nsomething else"), "b1")


def test_lay_makes_the_pack_and_imports_it_and_unlay_takes_both_out(tmp_path):
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec" / "index.md").write_text(INDEX)
    blocks = backlog_section.read(Item(SECTION), "b1")
    files = []
    backlog_pack.lay(tmp_path, blocks, files)
    pack = tmp_path / "spec" / "packs" / "household.md"
    assert TERM in pack.read_text() and "## Glossary" in pack.read_text()
    assert "imports: [request, household]" in (tmp_path / "spec" / "index.md").read_text()
    assert set(files) == {"spec/packs/household.md", "spec/index.md"}
    backlog_pack.unlay(tmp_path, blocks, [])
    assert not pack.exists()
    assert (tmp_path / "spec" / "index.md").read_text() == INDEX


def test_unlay_keeps_a_pack_that_holds_other_entries(tmp_path):
    (tmp_path / "spec" / "packs").mkdir(parents=True)
    (tmp_path / "spec" / "index.md").write_text(INDEX.replace("[request]", "[request, household]"))
    held = "# household\n\n## Glossary\n\n- **cellar** (noun): a room under the house.\n"
    pack = tmp_path / "spec" / "packs" / "household.md"
    pack.write_text(held)
    blocks = backlog_section.read(Item(SECTION), "b1")
    backlog_pack.lay(tmp_path, blocks, [])
    assert pack.read_text().index("cellar") < pack.read_text().index("pantry")
    backlog_pack.unlay(tmp_path, blocks, [])
    assert pack.read_text().strip() == held.strip()
    assert "household" in (tmp_path / "spec" / "index.md").read_text()


def test_a_plugin_pack_name_refused(tmp_path):
    with pytest.raises(Refused, match="plugin's own pack"):
        backlog_pack.write(tmp_path, "b1", "time", [TERM])
