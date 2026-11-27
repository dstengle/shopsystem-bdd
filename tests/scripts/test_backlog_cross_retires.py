"""`work line --into <cap> --retires <other cap>#r<n>` (b882): the line in --into's block, the pair `<cap>#r<n> r<m>`
under the retired id's block, read back byte-stable, laid, read by batch_laid's `fresh` and the corpus's trace,
carried by the renumbering and taken out with the line by `--remove`."""
import backlog_items
import backlog_lines
import backlog_renumber
import backlog_section
import batch_laid
import spec_corpus_write
from backlog_section import Block, Group
from backlog_testing import git, work, write_item

LINE = "When the person runs `work start` on an initiative, `work` shall give a brief to every stage."


def item(repo, name="b1"):
    return backlog_items.find(repo, name)


def blocks(repo, name="b1"):
    return backlog_lines.read(item(repo, name), backlog_items.rel_of(name))


def drafted(repo):
    write_item(repo, "b1", status="shaped")
    done = work(repo, "line", "b1", "--into", "review", "--retires", "work-queue#r1", LINE)
    assert done.returncode == 0, done.stderr
    return {b.capability: b for b in blocks(repo)}


def test_the_line_goes_into_its_capability_and_the_pair_under_the_retired_ids(ready_repo):
    found = drafted(ready_repo)
    rid = found["review"].groups[0].requirements[0][0]
    assert found["review"].groups[0].requirements == [(rid, LINE)] and not found["review"].retired
    assert found["work-queue"].retired == ("r1",) and found["work-queue"].retires == (("review#%s" % rid, "r1"),)
    assert not found["work-queue"].groups
    assert batch_laid.fresh(item(ready_repo)) == []
    assert not git(ready_repo, "status", "--porcelain").strip()


def test_a_cross_pair_reads_back_byte_stable():
    found = [Block("work-queue", [], [], (), ("r1",), retires=(("review#r2", "r1"),)),
             Block("review", [], [Group("g2", "T", [("r2", LINE)])])]
    text = backlog_section.render(found)
    assert "\nretires: [review#r2 r1]\n" in text + "\n"
    reader = backlog_section._Reader("t")
    for line in text.split("\n"):
        reader.line(line)
    assert reader.blocks == found


def test_no_line_still_goes_into_its_own_capability(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--into", "review", "--retires", "work-queue#r1", "--no-line")
    assert done.returncode == 1 and "goes into work-queue" in done.stderr, done.stderr


def test_the_lay_retires_the_id_in_its_capability_and_the_trace_names_it(ready_repo, tmp_path_factory):
    drafted(ready_repo)
    tmp_path = tmp_path_factory.mktemp("laid")
    backlog_lines.lay(ready_repo, item(ready_repo), tmp_path)
    queue = (tmp_path / "spec" / "capabilities" / "work-queue.md").read_text()
    assert "- [r1] " not in queue and "r1" in queue.split("retired: [", 1)[1].split("]")[0]
    review = (tmp_path / "spec" / "capabilities" / "review.md").read_text()
    assert LINE in review
    laid = spec_corpus_write._edits(item(ready_repo))["review"][0]
    assert laid[0][1].startswith("Retires: work-queue#r1. From: "), laid


def test_the_renumbering_carries_the_pair(ready_repo):
    found = drafted(ready_repo)
    rid = found["review"].groups[0].requirements[0][0]
    one = item(ready_repo)
    pairs = backlog_renumber.renumber(ready_repo, one, {"review": {rid}})
    new = dict(pairs)["review#%s" % rid]
    read = {b.capability: b for b in backlog_lines.read(one, backlog_items.rel_of("b1"))}
    assert read["work-queue"].retires == ((new, "r1"),)


def test_removing_the_line_reinstates_the_id_it_retires(ready_repo):
    found = drafted(ready_repo)
    rid = found["review"].groups[0].requirements[0][0]
    done = work(ready_repo, "line", "b1", "--remove", "review#%s" % rid)
    assert done.returncode == 0, done.stderr
    assert "### work-queue" not in (ready_repo / backlog_items.rel_of("b1")).read_text()
