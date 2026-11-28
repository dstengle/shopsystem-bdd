"""backlog_adapter_ops (b489): an operation an item's model lines add, with no table on the item, given its table by
the lay as `work line --expose` writes it; an operation the model held already, or one
the item tables or withholds, given none."""
import shutil
from pathlib import Path

import adapter_tables
import backlog_adapter
import backlog_adapter_ops
import backlog_model
import backlog_section

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "domain-model" / "spec"
PIN = '[operations."notes.pin"]\ncommand = "notes pin"'


def _root(tmp_path):
    shutil.copytree(FIXTURE, tmp_path / "spec")
    return tmp_path


def _blocks(lines, tables=(), withheld=()):
    blocks = backlog_section.Blocks(models=[backlog_model.ModelBlock("notes", tuple(lines))])
    if tables or withheld:
        blocks.adapters.append(backlog_adapter.AdapterBlock(
            "cli", tuple((adapter_tables.operations(t)[0], t) for t in tables), tuple(withheld)))
    return blocks


def _contract(root):
    return (root / "spec" / "adapters" / "cli.toml").read_text()


def test_a_new_operation_gets_its_table(tmp_path):
    root = _root(tmp_path)
    blocks = _blocks(["service notes", "  operation pin(note)  outcomes: done"])
    files = []
    backlog_adapter_ops.lay(root, blocks, files)
    table = adapter_tables.table(_contract(root), "notes.pin")
    assert table.startswith(PIN) and 'note = { option = "--note"' in table
    assert "spec/adapters/cli.toml" in files


def test_an_operation_the_model_held_gets_no_table(tmp_path):
    root = _root(tmp_path)
    contract = root / "spec" / "adapters" / "cli.toml"
    contract.write_text(adapter_tables.without(_contract(root), "notes.archive"))
    backlog_adapter_ops.lay(root, _blocks(["service notes", "  operation archive(note, reason)  outcomes: done"]), [])
    assert adapter_tables.table(_contract(root), "notes.archive") is None


def test_an_operation_the_item_tables_or_withholds_gets_only_the_item_s(tmp_path):
    root = _root(tmp_path)
    lines = ["service notes", "  operation pin(note)  outcomes: done"]
    own = PIN.replace("notes pin", "notes stick")
    backlog_adapter_ops.lay(root, _blocks(lines, tables=[own]), [])
    assert adapter_tables.table(_contract(root), "notes.pin") == own
    other = _root(tmp_path / "other")
    backlog_adapter_ops.lay(other, _blocks(lines, withheld=["notes.pin"]), [])
    assert adapter_tables.table(_contract(other), "notes.pin") is None
    assert "notes.pin" in adapter_tables.unexposed(_contract(other))
