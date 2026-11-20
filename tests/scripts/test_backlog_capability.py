"""`work line --capability` (b317): a new capability written as a block of an item, lines and terms going into it with
`--into`, laid over a copy of `spec/` as its file and Composition row, taken out again, and through the readiness
bar."""
import shutil

import backlog_items
import backlog_lines
import readiness_bar
from backlog_section import Block, Group
from backlog_testing import git, work, write_item

LINE = ("While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set the "
        "status of the initiative to `abandoned`.")
NEW = ("a person shelving things", "service", "Things kept on a shelf.")


def blocks(repo, name="b1"):
    return backlog_lines.read(backlog_items.find(repo, name), backlog_items.rel_of(name))


def made(repo):
    write_item(repo, "b1", status="shaped")
    done = work(repo, "line", "b1", "--capability", "shelf", "--narrator", NEW[0], NEW[2])
    assert done.returncode == 0, done.stderr
    assert done.stdout == 'b1 "Fix the parser": a new capability shelf\n'


def test_it_writes_the_block_and_lines_go_into_it(ready_repo):
    made(ready_repo)
    assert git(ready_repo, "show", "--name-only", "--format=", "HEAD").split() == [".shop/backlog/b1.md"]
    done = work(ready_repo, "line", "b1", "--into", "shelf", LINE)
    assert done.returncode == 0 and done.stdout.endswith("shelf#r1\n"), done.stderr
    assert blocks(ready_repo) == [Block("shelf", [], [Group("g1", "Fix the parser", [("r1", LINE)])], new=NEW)]
    text = (ready_repo / ".shop" / "backlog" / "b1.md").read_text()
    assert "### shelf\n\nnarrator: %s\ngroup: service\npurpose: %s\n\n#### [g1]" % (NEW[0], NEW[2]) in text


def test_it_refuses_an_existing_capability_a_second_block_and_a_bad_group(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--capability", "work-queue", "--narrator", "n", "p")
    assert done.returncode == 1 and "the capability work-queue exists" in done.stderr, done.stderr
    done = work(ready_repo, "line", "b1", "--capability", "shelf", "--narrator", "n", "--group", "other", "p")
    assert done.returncode == 1 and "neither service nor guarantees" in done.stderr, done.stderr
    assert work(ready_repo, "line", "b1", "--capability", "shelf", "--narrator", "n", "p").returncode == 0
    done = work(ready_repo, "line", "b1", "--capability", "shelf", "--narrator", "n", "p")
    assert done.returncode == 1 and "holds a block of the capability shelf" in done.stderr, done.stderr
    done = work(ready_repo, "line", "b1", "--capability", "shelf2", "p")
    assert done.returncode == 1 and "takes --narrator" in done.stderr, done.stderr


def test_lay_writes_the_file_and_row_and_unlay_takes_them_out(ready_repo, tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("copy")
    made(ready_repo)
    assert work(ready_repo, "line", "b1", "--into", "shelf", LINE).returncode == 0
    item = backlog_items.find(ready_repo, "b1")
    shutil.copytree(ready_repo / "spec", tmp_path / "spec")
    index = (tmp_path / "spec" / "index.md").read_text()
    files = []
    assert backlog_lines.lay_onto(tmp_path, item, files) == ["shelf"]
    assert files == ["spec/index.md"]
    text = (tmp_path / "spec" / "capabilities" / "shelf.md").read_text()
    assert text.startswith("---\nid: capability/ex.com/prod/ctx/shelf\ntitle: Shelf\nnarrator: %s\ngroup: service\n"
                           "area: shelf\nspecifies: service shelf\nlanguage: codified-2\nretired: []\n---\n\n# Shelf\n\n"
                           "## Purpose\n%s\n\n## Behaviour\n" % (NEW[0], NEW[2]))
    assert "### [g1] Fix the parser\n- [r1] %s" % LINE in text
    assert "## Terms" not in text
    laid = (tmp_path / "spec" / "index.md").read_text()
    assert laid.count("## Composition") == 1
    assert "| area | kind | capabilities |\n|---|---|---|\n| shelf | core | shelf |" in laid
    files = []
    assert backlog_lines.unlay(tmp_path, item, files) == []
    assert not (tmp_path / "spec" / "capabilities" / "shelf.md").exists()
    assert (tmp_path / "spec" / "index.md").read_text() == index
    assert files == ["spec/capabilities/shelf.md", "spec/index.md"]


def test_an_item_making_a_capability_passes_the_bar(ready_repo):
    made(ready_repo)
    assert work(ready_repo, "line", "b1", "--into", "shelf", LINE).returncode == 0
    reasons, _ = readiness_bar.check(ready_repo, backlog_items.find(ready_repo, "b1"))
    assert reasons == []


def test_a_new_capability_and_a_chore_exclude_each_other(ready_repo):
    """b316's chore and b317's capability block: each refused on an item holding the other."""
    made(ready_repo)
    done = work(ready_repo, "chore", "b1", "--file", "scripts/x.py", "--check", "true")
    assert done.returncode == 1 and "### shelf" in done.stderr, done.stderr
    write_item(ready_repo, "b2", status="shaped")
    assert work(ready_repo, "chore", "b2", "--file", "scripts/x.py", "--check", "true").returncode == 0
    done = work(ready_repo, "line", "b2", "--capability", "shelf", "--narrator", "n", "p")
    assert done.returncode == 1 and "a chore and requirement lines exclude each other" in done.stderr, done.stderr


def test_lay_names_the_capability_in_its_area_row_and_unlay_takes_it_out(tmp_path):
    from backlog_capability import lay, unlay
    (tmp_path / "spec" / "capabilities").mkdir(parents=True)
    was = ("---\nid: bounded-context/ex.com/prod/ctx\n---\n\n## Composition\n\n| area | kind | capabilities |\n"
           "|---|---|---|\n| shelf | core | notes |\n| other | supporting | x |\n\n## Upstreams\n")
    (tmp_path / "spec" / "index.md").write_text(was)
    block = Block("shelf", [], [], new=NEW[:1] + ("guarantees",) + NEW[2:])
    files = []
    lay(tmp_path, block, files)
    laid = (tmp_path / "spec" / "index.md").read_text()
    assert "| shelf | core | notes, shelf |\n| other | supporting | x |" in laid, laid
    assert "specifies: the shelf guarantees" in (tmp_path / "spec" / "capabilities" / "shelf.md").read_text()
    unlay(tmp_path, block, files)
    assert (tmp_path / "spec" / "index.md").read_text() == was
