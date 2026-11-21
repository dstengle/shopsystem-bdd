"""backlog_adapter's unlay against the batch's base (b479): each operation an item's adapter block names put back as
the contract at the base commit held it, whatever git held before the base or after it."""
import subprocess

import adapter_tables
import backlog_adapter
import backlog_section

OLD = '[operations."notes.add"]\ncommand = "notes add old"'
ADD = '[operations."notes.add"]\ncommand = "notes add"'
LIST = '[operations."notes.list"]\ncommand = "notes list"'
OTHER = '[operations."notes.add"]\ncommand = "notes put"'
ARCHIVE = '[operations."notes.archive"]\ncommand = "notes archive"'


def _git(root, *args):
    return subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@e", *args],
                          check=True, capture_output=True, text=True).stdout.strip()


def _contract(root, *tables, unexposed=()):
    text = "[programs]\nnotes = \"notes.py\"\n\n" + "\n\n".join(tables) + "\n"
    for ident in unexposed:
        text = adapter_tables.listed(text, ident, True)
    path = root / "spec" / "adapters" / "cli.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    _git(root, "add", ".")
    _git(root, "commit", "-qm", "contract")
    return _git(root, "rev-parse", "HEAD")


def _blocks(tables=(), withheld=()):
    return backlog_section.Blocks(adapters=[backlog_adapter.AdapterBlock(
        "cli", tuple((adapter_tables.operations(t)[0], t) for t in tables), tuple(withheld))])


def _laid(root, blocks):
    backlog_adapter.lay(root, blocks, [])
    _git(root, "commit", "-qam", "lay")
    return root / "spec" / "adapters" / "cli.toml"


def _repo(tmp_path):
    _git(tmp_path, "init", "-q")
    _contract(tmp_path, OLD, LIST)
    return tmp_path


def test_a_table_equal_to_the_base_s_leaves_the_base_s(tmp_path):
    base = _contract(_repo(tmp_path), ADD, LIST)
    blocks = _blocks([ADD])
    path = _laid(tmp_path, blocks)
    backlog_adapter.unlay(tmp_path, blocks, [], base)
    back = path.read_text()
    assert adapter_tables.table(back, "notes.add") == ADD and adapter_tables.table(back, "notes.list") == LIST


def test_a_table_of_an_operation_the_base_has_none_of_leaves_none(tmp_path):
    base = _contract(_repo(tmp_path), ADD, LIST)
    blocks = _blocks([ARCHIVE])
    path = _laid(tmp_path, blocks)
    backlog_adapter.unlay(tmp_path, blocks, [], base)
    back = path.read_text()
    assert adapter_tables.table(back, "notes.archive") is None
    assert "notes.archive" not in adapter_tables.unexposed(back)
    assert adapter_tables.table(back, "notes.add") == ADD and adapter_tables.table(back, "notes.list") == LIST


def test_a_withheld_operation_gets_the_base_s_table_back_and_is_exposed(tmp_path):
    base = _contract(_repo(tmp_path), ADD, LIST)
    blocks = _blocks(withheld=["notes.add"])
    path = _laid(tmp_path, blocks)
    assert "notes.add" in adapter_tables.unexposed(path.read_text())
    backlog_adapter.unlay(tmp_path, blocks, [], base)
    back = path.read_text()
    assert adapter_tables.table(back, "notes.add") == ADD and "notes.add" not in adapter_tables.unexposed(back)
    assert adapter_tables.table(back, "notes.list") == LIST


def test_an_operation_unexposed_at_the_base_is_unexposed_again(tmp_path):
    base = _contract(_repo(tmp_path), LIST, unexposed=["notes.add"])
    blocks = _blocks([ADD])
    path = _laid(tmp_path, blocks)
    backlog_adapter.unlay(tmp_path, blocks, [], base)
    back = path.read_text()
    assert adapter_tables.table(back, "notes.add") is None and "notes.add" in adapter_tables.unexposed(back)


def test_a_later_commit_on_the_operation_changes_nothing_restored(tmp_path):
    base = _contract(_repo(tmp_path), ADD, LIST)
    blocks = _blocks([OTHER])
    path = _laid(tmp_path, blocks)
    _contract(tmp_path, OLD, LIST)
    _contract(tmp_path, OTHER, LIST)
    backlog_adapter.unlay(tmp_path, blocks, [], base)
    back = path.read_text()
    assert adapter_tables.table(back, "notes.add") == ADD and adapter_tables.table(back, "notes.list") == LIST
