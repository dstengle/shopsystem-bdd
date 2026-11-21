"""The rest of batch-4 review 1 on `work line`'s spec pieces (b476): the universal file a lay made taken out by the
unlay (f2), an upstream another item laid refused by the readiness bar (f3), a docstring given block's blank lines kept
by the writer and the item's reader (f4), and `--group` or `--in` beside a piece other than a requirement line refused
(f5)."""
import shutil

import backlog_forms
import backlog_items
import backlog_lines
import pytest
import readiness_bar
from backlog_testing import state, work, write_item
from test_backlog_forms import ABANDON, ROW, UNIVERSAL, UPSTREAM

SPACED = "the file `notes.md` holds:\n  The first line.\n\n  The third line."


def test_the_unlay_takes_out_the_universal_file_the_lay_made(ready_repo, tmp_path):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--universal", UNIVERSAL).returncode == 0
    item = backlog_items.find(ready_repo, "b1")
    into = tmp_path / "copy"
    shutil.copytree(ready_repo / "spec", into / "spec")
    assert not (into / "spec" / "universal.md").exists()
    backlog_lines.lay_onto(into, item, [])
    assert (into / "spec" / "universal.md").is_file()
    files = []
    backlog_lines.unlay(into, item, files)
    assert not (into / "spec" / "universal.md").exists() and files == ["spec/universal.md"]


def test_the_unlay_keeps_a_universal_file_the_spec_had(ready_repo, tmp_path):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--universal", UNIVERSAL).returncode == 0
    item = backlog_items.find(ready_repo, "b1")
    into = tmp_path / "copy"
    shutil.copytree(ready_repo / "spec", into / "spec")
    backlog_forms._universal_file(into)
    had = (into / "spec" / "universal.md").read_text().replace("Universal conditions\n\n", "The conditions\n\n")
    (into / "spec" / "universal.md").write_text(had)
    backlog_lines.lay_onto(into, item, [])
    backlog_lines.unlay(into, item, [])
    assert (into / "spec" / "universal.md").read_text().rstrip("\n") == had.rstrip("\n")


def test_the_bar_refuses_an_upstream_an_item_picked_before_lays(ready_repo):
    for name in ("b1", "b2"):
        write_item(ready_repo, name, status="shaped")
        assert work(ready_repo, "line", name, "--into", "work-queue", ABANDON).returncode == 0
        assert work(ready_repo, "line", name, "--upstream", UPSTREAM).returncode == 0
    first, second = (backlog_items.find(ready_repo, n) for n in ("b1", "b2"))
    reasons = readiness_bar.well_formed(ready_repo, second, [first])[0]
    assert any("bounded-context/ex.com/prod/up" in r and "upstream" in r for r in reasons), reasons
    alone = readiness_bar.well_formed(ready_repo, second)[0]
    assert not any("bounded-context/ex.com/prod/up" in r for r in alone), alone


def test_a_docstring_keeps_its_blank_lines(ready_repo):
    assert backlog_forms.given_block("\n" + SPACED + "\n\n") == tuple(SPACED.split("\n"))
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON).returncode == 0
    done = work(ready_repo, "line", "b1", "--into", "work-queue", "--given", "g4", SPACED)
    assert done.returncode == 0, done.stderr
    item = backlog_items.find(ready_repo, "b1")
    blocks = backlog_lines.read(item, "b1")
    assert blocks[0].groups[0].given == tuple(SPACED.split("\n"))
    assert backlog_lines.render(blocks) == item.sections["Requirements"]


@pytest.mark.parametrize("args", [
    ("--into", "work-queue", "--relation", ROW, "--group", "Rows"),
    ("--into", "work-queue", "--given", "g4", SPACED, "--in", "g4"),
    ("--universal", UNIVERSAL, "--group", "Conditions"),
    ("--upstream", UPSTREAM, "--in", "g4"),
])
def test_group_or_in_beside_another_piece_is_refused(ready_repo, args):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON).returncode == 0
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", *args)
    assert done.returncode == 1 and "--group and --in" in done.stderr, done.stderr
    assert state(ready_repo) == before
