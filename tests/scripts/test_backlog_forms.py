"""The spec pieces beside an item's lines (b43, readiness r5-r11): `work line --relation`, `--given`, `--universal` and
`--upstream` written onto an item, read and rendered back, laid into a copy of `spec/` and taken out again, and the
universal conditions renumbered past `spec/universal.md`'s and the items picked before."""
import shutil

import backlog_forms
import backlog_items
import backlog_lines
import pytest
import spec_read
import spec_relations
from backlog_testing import git, state, work, write_item

ABANDON = ("While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set the status of the initiative to "
           "`abandoned`.")
ROW = "| initiative | holds | work-item | many |"
GIVEN = "the file `notes.md` holds:\n  The first line.\n  The second line."
UNIVERSAL = "`work` shall commit every transition."
UPSTREAM = "bounded-context/ex.com/prod/up: the upstream, github: ex/up"
CAP = "spec/capabilities/work-queue.md"


def all_pieces(repo):
    write_item(repo, "b1", status="shaped")
    for args in (("--into", "work-queue", ABANDON), ("--into", "work-queue", "--relation", ROW),
                 ("--into", "work-queue", "--given", "g4", GIVEN), ("--universal", UNIVERSAL),
                 ("--upstream", UPSTREAM)):
        done = work(repo, "line", "b1", *args)
        assert done.returncode == 0, (args, done.stderr)
    return backlog_items.find(repo, "b1")


def test_each_piece_is_written_and_read_back(ready_repo):
    item = all_pieces(ready_repo)
    blocks = backlog_lines.read(item, "b1")
    assert blocks[0].relations == (ROW,)
    assert blocks[0].groups[0].given == tuple(GIVEN.split("\n"))
    assert blocks.universal == [("U1", UNIVERSAL)] and blocks.upstreams == [UPSTREAM]
    assert backlog_lines.read(item, "b1") == blocks
    copy = backlog_items.Item("b1", "item/x/b1", "T", "shaped", "own",
                              sections={"Requirements": backlog_lines.render(blocks)})
    assert backlog_lines.render(backlog_lines.read(copy, "b1")) == item.sections["Requirements"]
    assert git(ready_repo, "log", "-1", "--format=%s").strip() == 'work line: b1 "Fix the parser" an upstream entry ' \
                                                                  'bounded-context/ex.com/prod/up'


@pytest.mark.parametrize("args, named", [
    (("--into", "work-queue", "--relation", "| initiative | holds | frobnicator | one |"), "frobnicator"),
    (("--into", "work-queue", "--relation", "| initiative | holds | work-item |"), "four cells"),
    (("--upstream", "the upstream"), "bounded-context id"),
    (("--upstream", "bounded-context/ex.com/prod/up: github: ex"), "github: ex"),
    (("--into", "work-queue", "--given", "g4", "an initiative i1 that is `proposed`"), "is not example data"),
    (("--into", "work-queue", "--given", "g4", "  The first line."), "under no line ending"),
    (("--into", "work-queue", "--given", "g9", GIVEN), "has no group g9"),
    (("--universal", UNIVERSAL, "--into", "work-queue"), "takes no --into"),
    (("--relation", ROW), "takes --into"),
])
def test_a_malformed_piece_is_refused_and_nothing_changes(ready_repo, args, named):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--into", "work-queue", ABANDON).returncode == 0
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", *args)
    assert done.returncode == 1 and named in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_an_upstream_already_in_the_index_is_refused(ready_repo):
    index = ready_repo / "spec" / "index.md"
    index.write_text(index.read_text() + "\n## Upstreams\n- %s\n" % UPSTREAM)
    git(ready_repo, "commit", "-qam", "an upstream")
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--upstream", UPSTREAM)
    assert done.returncode == 1 and "is an upstream already" in done.stderr, done.stderr


def test_lay_and_unlay_carry_every_piece(ready_repo, tmp_path):
    item = all_pieces(ready_repo)
    into = tmp_path / "copy"
    shutil.copytree(ready_repo / "spec", into / "spec")
    before = {p: (into / p).read_text() for p in (CAP, "spec/index.md")}
    files = []
    assert backlog_lines.lay_onto(into, item, files) == ["work-queue"]
    assert files == ["spec/universal.md", "spec/index.md"]
    cap = spec_read.capability(into / CAP)
    assert cap.problems == []
    g4 = next(g for g in cap.groups if g.id == "g4")
    assert [line for line, _ in g4.given] == ["the file `notes.md` holds:"]
    assert ("initiative", "holds", "work-item", "many") in [r[:4] for r in spec_relations.rows((into / CAP).read_text(),
                                                                                                CAP)]
    universal = spec_read.read_universal(into)
    assert universal.problems == [] and [(u.id, u.text) for u in universal.conditions] == [("U1", UNIVERSAL)]
    assert "## Upstreams\n\n- %s\n" % UPSTREAM in (into / "spec" / "index.md").read_text()
    files = []
    assert backlog_lines.unlay(into, item, files) == ["work-queue"]
    assert sorted(files) == ["spec/index.md", "spec/universal.md"]
    assert {p: (into / p).read_text() for p in before} == before
    assert spec_read.read_universal(into).conditions == []


def test_a_row_joins_an_existing_table_and_a_bullet_the_upstreams():
    text = "## Relations\n\n%s\n%s\n| a | b | c | one |\n\n## Upstreams\n- bounded-context/x/y: one\n\n## Behaviour\n" \
        % backlog_forms.HEADER
    text = backlog_forms.with_lines(text, "Relations", [ROW], backlog_forms.HEADER)
    text = backlog_forms.with_lines(text, "Upstreams", ["- %s" % UPSTREAM])
    assert "| a | b | c | one |\n%s\n\n## Upstreams\n- bounded-context/x/y: one\n- %s\n\n## Behaviour" % (ROW, UPSTREAM) \
        in text
    made = backlog_forms.with_lines("# T\n\n## Terms\n\n## Behaviour\n", "Relations", [ROW], backlog_forms.HEADER,
                                    "Behaviour")
    assert made == "# T\n\n## Terms\n\n## Relations\n\n%s\n%s\n%s\n\n## Behaviour\n" % (*backlog_forms.HEADER, ROW)
    assert backlog_forms.without_lines(made, "Relations", [ROW], backlog_forms.HEADER) == \
        "# T\n\n## Terms\n\n## Behaviour\n"


def test_renumber_moves_a_universal_condition_past_spec_and_taken(ready_repo):
    item = all_pieces(ready_repo)
    (ready_repo / "spec" / "universal.md").write_text(
        "---\nid: capability/ex.com/prod/ctx/universal\nlanguage: codified-1\nretired: [U2]\n---\n\n# U\n\n"
        "## Behaviour\n\n- [U1] %s\n" % UNIVERSAL)
    taken = {"work-queue": set(), "universal": {"U3"}}
    pairs = backlog_lines.renumber(ready_repo, item, taken)
    assert ("universal#U1", "universal#U4") in pairs
    blocks = backlog_lines.read(item, "b1")
    assert blocks.universal == [("U4", UNIVERSAL)] and blocks.upstreams == [UPSTREAM]
    assert blocks[0].relations == (ROW,) and blocks[0].groups[0].given
    assert taken["universal"] == {"U3", "U4"}
