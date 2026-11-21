"""adapter_tables and backlog_adapter (b355): an operation's tables changed as text, an item's adapter block read and
written back byte-stable, and the lay into the contract taken out again as git held it."""
import subprocess

import adapter_tables
import backlog_adapter
import backlog_section
import pytest
from backlog_items import Refused

CONTRACT = '''[programs]
notes = "notes.py"

[operations."notes.add"]
command = "notes add"
[operations."notes.add".parameters]
text = { positional = 1 }

[operations."notes.list"]
command = "notes list"

[unexposed]
# none requested by a command
operations = ["notes.sweep"]
'''
ARCHIVE = '[operations."notes.archive"]\ncommand = "notes archive"\n[operations."notes.archive".parameters]\nnote = { positional = 1 }'
ADD = '[operations."notes.add"]\ncommand = "notes put"'


def test_tables_put_in_taken_out_and_listed():
    text = adapter_tables.with_table(CONTRACT, ARCHIVE)
    assert adapter_tables.operations(text) == ["notes.add", "notes.list", "notes.archive"]
    assert adapter_tables.table(text, "notes.archive") == ARCHIVE
    replaced = adapter_tables.with_table(text, ADD)
    assert adapter_tables.table(replaced, "notes.add") == ADD and "text = { positional = 1 }" not in replaced
    assert adapter_tables.without(text, "notes.archive") == CONTRACT
    listed = adapter_tables.listed(CONTRACT, "notes.list", True)
    assert adapter_tables.unexposed(listed) == ["notes.sweep", "notes.list"] and "# none requested" in listed
    assert adapter_tables.listed(listed, "notes.list", False) == CONTRACT
    assert adapter_tables.listed("", "notes.x", True) == '[unexposed]\noperations = ["notes.x"]\n'


def test_one_reads_the_tables_of_one_operation_only():
    assert adapter_tables.one(ARCHIVE) == ("notes.archive", ARCHIVE)
    for bad in ("command = 1", ARCHIVE + "\n" + ADD, "[operations.\"notes.x\"]\nhook = 1\n[programs]\nx = 1",
                "[operations.\"notes.x\"]\nparameters = 1", "not toml ["):
        with pytest.raises(Refused):
            adapter_tables.one(bad)


class _Item:
    name = "b1"

    def __init__(self, text):
        self.sections = {"Requirements": text}


def test_block_read_and_written_back():
    text = "### cli adapter\n\nwithheld: [notes.sweep, notes.list]\n\n```toml\n%s\n\n%s\n```" % (ARCHIVE, ADD)
    blocks = backlog_section.read(_Item(text), "b1")
    assert blocks.adapters == [backlog_adapter.AdapterBlock("cli", (("notes.archive", ARCHIVE), ("notes.add", ADD)),
                                                            ("notes.sweep", "notes.list"))]
    assert backlog_section.render(blocks) == text
    with pytest.raises(Refused):
        backlog_section.read(_Item("### cli adapter\n\nsomething"), "b1")


def _git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def test_lay_and_unlay_put_the_contract_back(tmp_path):
    path = tmp_path / "spec" / "adapters" / "cli.toml"
    path.parent.mkdir(parents=True)
    path.write_text(CONTRACT)
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@e", "commit", "-qm", "c", "--allow-empty")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@e", "commit", "-qm", "contract")
    blocks = backlog_section.Blocks(adapters=[backlog_adapter.AdapterBlock("cli", (("notes.add", ADD),
                                                                                   ("notes.archive", ARCHIVE)),
                                                                           ("notes.list",))])
    files = []
    backlog_adapter.lay(tmp_path, blocks, files)
    laid = path.read_text()
    assert files == ["spec/adapters/cli.toml"] and adapter_tables.table(laid, "notes.add") == ADD
    assert "notes.list" in adapter_tables.unexposed(laid) and adapter_tables.table(laid, "notes.list") is None
    _git(tmp_path, "add", ".")
    _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@e", "commit", "-qm", "lay")
    backlog_adapter.unlay(tmp_path, blocks, [])
    back = path.read_text()
    assert adapter_tables.unexposed(back) == ["notes.sweep"] and adapter_tables.table(back, "notes.archive") is None
    for ident in ("notes.add", "notes.list"):
        assert adapter_tables.table(back, ident) == adapter_tables.table(CONTRACT, ident)


def test_lay_makes_a_contract_and_unlay_removes_it(tmp_path):
    blocks = backlog_section.Blocks(adapters=[backlog_adapter.AdapterBlock("cli", (("notes.archive", ARCHIVE),))])
    backlog_adapter.lay(tmp_path, blocks, [])
    path = tmp_path / "spec" / "adapters" / "cli.toml"
    assert path.read_text() == ARCHIVE + "\n"
    backlog_adapter.unlay(tmp_path, blocks, [])
    assert not path.exists()


def test_operation_table_written_from_the_model():
    """b482: the operation-table form of an operation, its program the contract's other operations', else its
    service; each parameter an option with an example of its type, a flag `flag = true`."""
    from domain_model_parse import Operation, Parameter
    op = Operation("notes", "pin", parameters=(Parameter("priority", "values", ("low", "high")),
                                               Parameter("due date", "time"), Parameter("loud", "flag")))
    contract = CONTRACT.replace('command = "notes add"', 'command = "jot add"')
    assert adapter_tables.of(op, contract) == (
        '[operations."notes.pin"]\ncommand = "jot pin"\n[operations."notes.pin".parameters]\n'
        'priority = { option = "--priority", example = "low" }\n'
        '"due date" = { option = "--due-date", example = "2026-01-01" }\nloud = { option = "--loud", flag = true }')
    assert adapter_tables.of(Operation("tasks", "sweep")) == '[operations."tasks.sweep"]\ncommand = "tasks sweep"'
