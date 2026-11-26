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


def _repo(tmp_path):
    spec = tmp_path / "spec"
    for rel, text in (("index.md", INDEX), ("model/notes.md", NOTES), ("model/stock.md", STOCK),
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
