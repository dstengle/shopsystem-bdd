"""The core lines a port line of an item supports (b705): `work line --relied-on-by` on the last line of a group
(`--in`), the `Relied on by:` line laid into the capability file as spec_read reads it and taken out by the unlay, and
renumber carrying the item's own ids in it."""
import backlog_items
import backlog_lines
import spec_read
from backlog_section import read
from backlog_testing import git, work, write_item

CAP = "work-queue"
LINE = "When the person runs `work start` on an initiative, `work` shall commit the initiative."


def _line(repo, *args):
    done = work(repo, "line", "b1", "--into", CAP, *args)
    assert done.returncode == 0, done.stderr
    return done


def test_a_group_s_last_line_is_given_the_ids_and_the_lay_writes_them(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    _line(ready_repo, LINE)
    item = backlog_items.find(ready_repo, "b1")
    group = read(item, "b1")[0].groups[0]
    _line(ready_repo, "--in", group.id, "--relied-on-by", "%s#r1,%s#r2" % (CAP, CAP))
    item = backlog_items.find(ready_repo, "b1")
    rid = group.requirements[0][0]
    assert read(item, "b1")[0].groups[0].relied == ((rid, ("%s#r1" % CAP, "%s#r2" % CAP)),)
    path = ready_repo / "spec" / "capabilities" / ("%s.md" % CAP)
    held = path.read_text()
    backlog_lines.lay_onto(ready_repo, item)
    laid = {r.id: r for g in spec_read.capability(path).groups for r in g.requirements}
    assert laid[rid].supports == ("%s#r1" % CAP, "%s#r2" % CAP)
    backlog_lines.unlay(ready_repo, item, [], git(ready_repo, "rev-parse", "HEAD").strip())
    assert path.read_text() == held


def test_renumber_carries_the_item_s_own_ids(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    _line(ready_repo, LINE)
    rid = read(backlog_items.find(ready_repo, "b1"), "b1")[0].groups[0].requirements[0][0]
    _line(ready_repo, "--relied-on-by", "%s#%s" % (CAP, rid), LINE.replace("commit", "push"))
    item = backlog_items.find(ready_repo, "b1")
    taken = {CAP: {rid, "r%d" % (int(rid[1:]) + 1), "g%d" % (int(rid[1:]) + 9)}}
    pairs = dict(backlog_lines.renumber(ready_repo, item, taken))
    group = read(item, "b1")[0].groups[0]
    second = group.requirements[1][0]
    assert dict(group.relied) == {second: (pairs["%s#%s" % (CAP, rid)],)}, (group, pairs)


def test_an_id_no_requirement_has_is_refused_naming_it(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    before = (ready_repo / backlog_items.rel_of("b1")).read_text()
    done = work(ready_repo, "line", "b1", "--into", CAP, "--relied-on-by", "%s#r99" % CAP, LINE)
    assert done.returncode == 1 and "%s#r99" % CAP in done.stderr, done.stderr
    assert (ready_repo / backlog_items.rel_of("b1")).read_text() == before
