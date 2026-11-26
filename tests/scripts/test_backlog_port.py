"""A driven port an item makes (b701): laid over a spec, the port's model file importing the areas whose words its
lines say, and taken out again, the model files byte for byte as they were, a port area spec/model/ held already
among them (f1)."""
import subprocess
from types import SimpleNamespace

import backlog_port
from backlog_section import read

INDEX = "---\nid: bounded-context/ex.com/prod/ctx\nlanguage: codified-2\n---\n\n# Ctx\n"
NOTES = "---\nid: model/ex.com/prod/ctx/notes\narea: notes\nkind: core\nimports: []\n---\n\n# Notes\n\n```model\nobject note\n```\n"
STOCK = "---\nid: model/ex.com/prod/ctx/stock\narea: stock\nkind: port\nimports: []\n---\n\n# Stock\n\n```model\n```\n"
WORDS = "---\nid: vocabulary/ex.com/prod/ctx/notes\narea: notes\n---\n\n# The words of notes\n\n## Terms\n- **note** (noun) → object note. A note. Plural: notes.\n"
REQUIREMENTS = ("### stock-port\n\nnarrator: the notes service\ngroup: service\npurpose: Stock.\narea: stock\nkind: port\n\n"
                "#### [g1] A note reserved is reserved\n- [r1] When the notes service reserves a note, the stock "
                "service shall not refuse the request.")


def _repo(tmp_path, stock=STOCK):
    spec = tmp_path / "spec"
    for rel, text in (("index.md", INDEX), ("model/notes.md", NOTES), ("model/stock.md", stock),
                      ("vocabulary/notes.md", WORDS)):
        (spec / rel).parent.mkdir(parents=True, exist_ok=True)
        (spec / rel).write_text(text)
    for args in (["init", "-q"], ["add", "-A"], ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base"]):
        subprocess.run(["git", "-C", str(tmp_path), *args], check=True)
    return read(SimpleNamespace(sections={"Requirements": REQUIREMENTS}, name="b1"), "the item b1")


def test_an_existing_port_area_comes_back_byte_for_byte(tmp_path):
    blocks = _repo(tmp_path)
    base = subprocess.run(["git", "-C", str(tmp_path), "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()
    files = []
    backlog_port.lay(tmp_path, blocks, files)
    stock = tmp_path / "spec" / "model" / "stock.md"
    assert "imports: [notes]\n" in stock.read_text(), stock.read_text()
    files = []
    backlog_port.unlay(tmp_path, blocks, files, base)
    assert stock.read_text() == STOCK
    assert (tmp_path / "spec" / "model" / "notes.md").read_text() == NOTES
    assert "spec/model/stock.md" in files


OTHER = ("---\narea: stock\nlanguage: codified-2\nretired: []\n---\n\n# Stock other\n\n## Behaviour\n\n### [g1] A note "
         "released\n- [r1] When the notes service releases a note, the stock service shall not refuse the request.\n")


def test_an_import_another_line_of_the_port_says_is_kept_without_a_base(tmp_path):
    """b704: per item, never reset to the base: an import a line left in the port says stays, and with no base the
    unlay takes out an import only this item's lines said."""
    blocks = _repo(tmp_path)
    stock = tmp_path / "spec" / "model" / "stock.md"
    backlog_port.lay(tmp_path, blocks, [])
    other = tmp_path / "spec" / "capabilities" / "stock-other.md"
    other.parent.mkdir(parents=True, exist_ok=True)
    other.write_text(OTHER)
    backlog_port.unlay(tmp_path, blocks, [])
    assert "imports: [notes]\n" in stock.read_text(), stock.read_text()
    other.unlink()
    backlog_port.unlay(tmp_path, blocks, [])
    assert stock.read_text() == STOCK


def test_an_import_the_port_held_at_the_base_survives_the_unlay(tmp_path):
    """b704 f1: a port area whose model file held `imports: [notes]` at the base keeps it once the item that says a
    note is taken out against that base, though no line left in the area says a note."""
    blocks = _repo(tmp_path, STOCK.replace("imports: []", "imports: [notes]"))
    stock = tmp_path / "spec" / "model" / "stock.md"
    base = subprocess.run(["git", "-C", str(tmp_path), "rev-parse", "HEAD"], capture_output=True, text=True,
                          check=True).stdout.strip()
    backlog_port.lay(tmp_path, blocks, [])
    backlog_port.unlay(tmp_path, blocks, [], base)
    assert "imports: [notes]\n" in stock.read_text(), stock.read_text()
