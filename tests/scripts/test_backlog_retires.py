"""`work line --retires` (b128): the new line and the old id under its block's `retired:`, the refusals, and the
retired line laid out of a spec and put back."""
import backlog_items
import backlog_lines
import backlog_section
import spec_read
from backlog_section import Block, Group
from backlog_testing import git, work, write_item

LINE = ("While an initiative is `proposed`, when the person runs `work start` on the initiative, `work` shall set the status of the initiative to "
        "`started` and commit the initiative.")
CAP = "spec/capabilities/work-queue.md"


def item(repo, name="b1"):
    return backlog_items.find(repo, name)


def blocks(repo, name="b1"):
    return backlog_lines.read(item(repo, name), backlog_items.rel_of(name))


def test_the_retired_line_reads_back_byte_stable():
    found = Block("work-queue", ["- **x** (noun): a thing."], [Group("g4", "T", [("r5", LINE)])], (), ("r1", "r3"))
    text = backlog_section.render([found])
    assert text.startswith("### work-queue\n\nretired: [r1, r3]\n\n- **x**")
    reader = backlog_section._Reader("t")
    for line in text.split("\n"):
        reader.line(line)
    assert reader.blocks == [found]


def test_a_retired_line_after_the_terms_is_refused():
    reader = backlog_section._Reader("t")
    reader.line("### work-queue")
    reader.line("- **x** (noun): a thing.")
    try:
        reader.line("retired: [r1]")
    except backlog_items.Refused as err:
        assert "retired:" in str(err)
    else:
        raise AssertionError("a retired: line after the terms was read")


def test_retires_writes_the_line_and_the_old_id_and_commits(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--retires", "work-queue#r1", LINE)
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": work-queue#r5 retires work-queue#r1\n'
    assert blocks(ready_repo) == [Block("work-queue", [], [Group("g4", "Fix the parser", [("r5", LINE)])], (),
                                        ("r1",))]
    assert git(ready_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]


def test_a_nonexistent_or_retired_id_is_refused_changing_nothing(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    head = git(ready_repo, "rev-parse", "HEAD")
    path = ready_repo / CAP
    path.write_text(path.read_text().replace("retired: []", "retired: [r9]"))
    git(ready_repo, "commit", "-qam", "a retired r9")
    head = git(ready_repo, "rev-parse", "HEAD")
    for ident in ("work-queue#r99", "work-queue#r9", "nothing#r1", "work-queue#g1"):
        done = work(ready_repo, "line", "b1", "--retires", ident, LINE)
        assert done.returncode == 1 and ident in done.stderr, (ident, done.stderr)
    assert git(ready_repo, "rev-parse", "HEAD") == head
    assert work(ready_repo, "line", "b1", "--retires", "work-queue#r1", LINE).returncode == 0
    done = work(ready_repo, "line", "b1", "--retires", "work-queue#r1", LINE)
    assert done.returncode == 1 and "retires work-queue#r1 already" in done.stderr, done.stderr


def test_retires_takes_only_a_line_into_its_own_capability(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--retires", "work-queue#r1", "--into", "other", LINE)
    assert done.returncode == 1 and "goes into work-queue" in done.stderr, done.stderr
    done = work(ready_repo, "line", "b1", "--retires", "work-queue#r1", "--into", "work-queue", "--term",
                "- **x** (noun): a thing.")
    assert done.returncode == 1 and "--retires takes a requirement line" in done.stderr, done.stderr


def lay_and_unlay(repo, retired):
    write_item(repo, "b1", status="shaped")
    for ident in retired:
        assert work(repo, "line", "b1", "--retires", ident, LINE).returncode == 0
    path = repo / CAP
    was = path.read_text()
    backlog_lines.lay_onto(repo, item(repo))
    laid = path.read_text()
    git(repo, "commit", "-qam", "laid")
    backlog_lines.unlay(repo, item(repo))
    return was, laid, path.read_text()


def test_a_line_laid_out_of_its_group_and_put_back(ready_repo):
    was, laid, back = lay_and_unlay(ready_repo, ["work-queue#r1"])
    cap = spec_read.capability(ready_repo / CAP)
    assert "- [r1] " not in laid and "- [r2] " in laid and "retired: [r1]" in laid
    assert back == was and cap.problems == []


def test_a_group_s_last_line_takes_its_group_out_and_back(ready_repo):
    was, laid, back = lay_and_unlay(ready_repo, ["work-queue#r3", "work-queue#r4"])
    assert "[g2]" not in laid and "[g3]" not in laid and "```given\nthe file" not in laid
    assert "retired: [g2, r3, g3, r4]" in laid
    assert back == was


def test_laid_over_a_copy_the_spec_reads_clean(ready_repo, tmp_path):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--retires", "work-queue#r3", LINE).returncode == 0
    backlog_lines.lay(ready_repo, item(ready_repo), tmp_path / "copy")
    cap = spec_read.capability(tmp_path / "copy" / CAP)
    assert cap.problems == [] and "g2" not in {g.id for g in cap.groups}
    assert {"g2", "r3"} <= set(cap.retired) and "r5" in {r.id for g in cap.groups for r in g.requirements}
