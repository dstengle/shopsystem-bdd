"""`work line --recodify` (CNL 4's I19): the marker written into the item's block, read back byte-stable, laid over a
spec and taken out again; the refusals; and the readiness bar over a mixed spec, each line parsed in its capability
file's grammar (spec_language)."""
import pathlib
import sys

import backlog_items
import backlog_lines
import backlog_section
import readiness_bar
import spec_language
import spec_read
from backlog_section import Block, Group
from backlog_testing import git, work, write_item

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scenarios"))
import codified2_mixed as M  # noqa: E402
import toolchain  # noqa: E402

CAP = "spec/capabilities/work-queue.md"
# a line of grammar 4, which the old grammar refuses (its verb end has no frame the old reader reads)
FOUR = "When a session ends a stage, `work` shall print the stage."


def blocks(repo, name="b1"):
    return backlog_lines.read(backlog_items.find(repo, name), backlog_items.rel_of(name))


def test_the_marker_reads_back_byte_stable():
    found = Block("work-queue", [], [Group("g4", "T", [("r5", FOUR)])], (), ("r1",), "codified-2")
    text = backlog_section.render([found])
    assert text.startswith("### work-queue\n\nlanguage: codified-2\n\nretired: [r1]\n\n#### [g4] T")
    reader = backlog_section._Reader("t")
    for line in text.split("\n"):
        reader.line(line)
    assert reader.blocks == [found]


def test_a_marker_after_the_block_s_first_line_is_refused():
    reader = backlog_section._Reader("t")
    reader.line("### work-queue")
    reader.line("retired: [r1]")
    try:
        reader.line("language: codified-2")
    except backlog_items.Refused as err:
        assert "language:" in str(err)
    else:
        raise AssertionError("a language: line after retired: was read")


def test_recodify_writes_the_marker_and_commits_the_item(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--recodify", "work-queue")
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": work-queue recodified\n'
    assert blocks(ready_repo) == [Block("work-queue", [], [], (), (), "codified-2")]
    assert git(ready_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    again = work(ready_repo, "line", "b1", "--recodify", "work-queue")
    assert again.returncode != 0 and "recodifies work-queue already" in again.stderr, again.stderr


def test_a_capability_in_the_new_language_is_refused(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    path = ready_repo / CAP
    path.write_text(path.read_text().replace("language: codified-1", "language: codified-2"))
    git(ready_repo, "commit", "-qam", "work-queue in the new language")
    head = git(ready_repo, "rev-parse", "HEAD")
    done = work(ready_repo, "line", "b1", "--recodify", "work-queue")
    assert done.returncode != 0 and "says `language: codified-2` already" in done.stderr, done.stderr
    assert git(ready_repo, "rev-parse", "HEAD") == head


def test_the_marker_is_laid_and_taken_out(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--recodify", "work-queue").returncode == 0
    was = (ready_repo / CAP).read_text()
    item = backlog_items.find(ready_repo, "b1")
    backlog_lines.lay_onto(ready_repo, item)
    assert spec_read.codified(ready_repo / CAP, ("codified-2",))
    assert backlog_lines.unlay(ready_repo, item) == ["work-queue"]
    assert (ready_repo / CAP).read_text() == was


def _mixed(repo):
    M.mixed(repo, "ex.com/prod/ctx")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "a mixed spec")


def test_a_line_is_read_in_its_capability_file_s_grammar(backlog_repo):
    _mixed(backlog_repo)
    assert spec_language.four(backlog_repo, "shelf") and not spec_language.four(backlog_repo, "thing")
    assert spec_language.four(backlog_repo) and spec_language.four(backlog_repo, "nonesuch")    # the index's


def test_the_bar_reads_a_recodified_capability_s_lines_in_grammar_4(backlog_repo):
    toolchain.require()
    _mixed(backlog_repo)
    write_item(backlog_repo, "b1", status="shaped")
    assert work(backlog_repo, "line", "b1", "--into", "thing", FOUR).returncode == 0
    reasons, _ = readiness_bar.well_formed(backlog_repo, backlog_items.find(backlog_repo, "b1"))
    assert reasons and reasons[0].startswith("thing#r2: "), reasons       # the old grammar refuses it
    assert work(backlog_repo, "line", "b1", "--recodify", "thing").returncode == 0
    reasons, _ = readiness_bar.well_formed(backlog_repo, backlog_items.find(backlog_repo, "b1"))
    assert reasons == [], reasons


def test_a_request_line_is_checked_in_the_grammar_of_its_capability(backlog_repo):
    toolchain.require()
    import request_lines
    _mixed(backlog_repo)
    assert request_lines.check(backlog_repo, [FOUR], "shelf") is None
    try:
        request_lines.check(backlog_repo, [FOUR], "thing")
    except backlog_items.Refused as err:
        assert "does not parse in the upstream's requirement grammar" in str(err)
    else:
        raise AssertionError("a grammar 4 line passed in a codified-1 capability's grammar")
