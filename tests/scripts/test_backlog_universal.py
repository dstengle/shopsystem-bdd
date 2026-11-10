"""`work line --recodify universal` and `work line --universal --retires` (b220): the item's universal block with its
marker and `retired:` read back byte-stable, the refusals, and spec/universal.md laid and put back."""
import backlog_items
import backlog_lines
import backlog_section
import spec_read
from backlog_testing import git, work, write_item

REL = "spec/universal.md"
OLD = "`work` shall commit every transition."
NEW = "`work` shall commit every transition and push it."
UNIVERSAL = ("---\nid: capability/ex.com/prod/ctx/universal\ntitle: Universal conditions\ngroup: guarantees\n"
             "language: codified-1\nretired: []\n---\n\n# Universal conditions\n\n## Behaviour\n\n"
             "- [U1] %s\n- [U2] `work` shall print every transition.\n- [U3] `work` shall exit.\n" % OLD)


def item(repo, name="b1"):
    return backlog_items.find(repo, name)


def with_universal(repo):
    (repo / REL).write_text(UNIVERSAL)
    git(repo, "add", REL)
    git(repo, "commit", "-qm", "universal conditions")
    write_item(repo, "b1", status="shaped")
    return repo / REL


def test_the_universal_block_reads_back_byte_stable():
    blocks = backlog_section.Blocks([], [("U4", NEW)], [], "codified-2", ("U1", "U2"))
    text = backlog_section.render(blocks)
    assert text == "### universal\n\nlanguage: codified-2\n\nretired: [U1, U2]\n\n- [U4] %s" % NEW
    reader = backlog_section._Reader("t")
    for line in text.split("\n"):
        reader.line(line)
    got = reader.blocks
    assert (got.universal, got.universal_language, got.universal_retired) == ([("U4", NEW)], "codified-2",
                                                                              ("U1", "U2"))


def test_recodify_universal_writes_the_marker_and_refuses_twice(ready_repo):
    with_universal(ready_repo)
    done = work(ready_repo, "line", "b1", "--recodify", "universal")
    assert done.returncode == 0, done.stderr
    assert "### universal\n\nlanguage: codified-2" in (ready_repo / ".shop/backlog/b1.md").read_text()
    assert git(ready_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    done = work(ready_repo, "line", "b1", "--recodify", "universal")
    assert done.returncode == 1 and "already" in done.stderr, done.stderr


def test_retires_a_nonexistent_condition_is_refused_changing_nothing(ready_repo):
    with_universal(ready_repo)
    head = git(ready_repo, "rev-parse", "HEAD")
    for ident in ("universal#U9", "universal#r1", "work-queue#U1"):
        done = work(ready_repo, "line", "b1", "--universal", NEW, "--retires", ident)
        assert done.returncode == 1 and ident in done.stderr, (ident, done.stderr)
    assert git(ready_repo, "rev-parse", "HEAD") == head


def test_laid_and_put_back(ready_repo):
    path = with_universal(ready_repo)
    assert work(ready_repo, "line", "b1", "--recodify", "universal").returncode == 0
    done = work(ready_repo, "line", "b1", "--universal", NEW, "--retires", "universal#U2")
    assert done.returncode == 0 and "universal#U4 retires universal#U2" in done.stdout, done.stdout + done.stderr
    files = []
    backlog_lines.lay_onto(ready_repo, item(ready_repo), files)
    laid = path.read_text()
    assert files == [REL]
    assert "language: codified-2" in laid and "retired: [U2]" in laid and "[U2]" not in laid.split("---")[2]
    found = spec_read.read_universal(ready_repo)
    assert found.problems == [] and [u.id for u in found.conditions] == ["U1", "U3", "U4"]
    git(ready_repo, "commit", "-qam", "laid")
    backlog_lines.unlay(ready_repo, item(ready_repo))
    lines = [line for line in path.read_text().split("\n") if line]     # backlog_forms' lay drops a blank line
    assert lines == [line for line in UNIVERSAL.split("\n") if line]
