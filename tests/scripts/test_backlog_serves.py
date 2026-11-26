"""A requirement group dedicated to a job on an item (b641): `work line --serves` refuses a
pair the capability's live group serves already, or that another open item holds, naming the group and the job; and
the unlay leaves on a group's `serves:` line a job the file at the batch's base held."""
import re

import backlog_items
import backlog_lines
from backlog_testing import git, state, work, write_item

CAP = "work-queue"


def _serve(repo, job="start-work"):
    """work-queue's live g1 given the line `serves: <job>` under its heading, committed."""
    path = repo / "spec" / "capabilities" / ("%s.md" % CAP)
    path.write_text(re.sub(r"(?m)^(### \[g1\] .*)$", r"\1\nserves: %s" % job, path.read_text(), count=1))
    git(repo, "commit", "-qam", "g1 serves %s" % job)
    return path


def test_the_unlay_leaves_a_job_the_base_held(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--serves", "%s#g1" % CAP, "start-work").returncode == 0
    path = _serve(ready_repo)
    held = path.read_text()
    item = backlog_items.find(ready_repo, "b1")
    backlog_lines.lay_onto(ready_repo, item)
    assert path.read_text() == held
    backlog_lines.unlay(ready_repo, item, [], git(ready_repo, "rev-parse", "HEAD").strip())
    assert "serves: start-work" in path.read_text().split("\n")
    assert path.read_text() == held


def test_the_unlay_takes_off_the_job_it_laid(ready_repo):
    path = ready_repo / "spec" / "capabilities" / ("%s.md" % CAP)
    held = path.read_text()
    write_item(ready_repo, "b1", status="shaped")
    assert work(ready_repo, "line", "b1", "--serves", "%s#g1" % CAP, "start-work").returncode == 0
    item = backlog_items.find(ready_repo, "b1")
    backlog_lines.lay_onto(ready_repo, item)
    assert "serves: start-work" in path.read_text().split("\n")
    backlog_lines.unlay(ready_repo, item, [], git(ready_repo, "rev-parse", "HEAD").strip())
    assert path.read_text() == held


def test_serves_refuses_a_job_the_live_group_serves(ready_repo):
    _serve(ready_repo)
    write_item(ready_repo, "b1", status="shaped")
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", "--serves", "%s#g1" % CAP, "start-work")
    assert done.returncode == 1, done.stdout
    assert "%s#g1" % CAP in done.stderr and "start-work" in done.stderr, done.stderr
    assert state(ready_repo) == before


def test_serves_refuses_a_pair_another_open_item_holds(ready_repo):
    write_item(ready_repo, "b1", status="shaped")
    write_item(ready_repo, "b2", status="shaped")
    assert work(ready_repo, "line", "b1", "--serves", "%s#g1" % CAP, "start-work").returncode == 0
    before = state(ready_repo)
    done = work(ready_repo, "line", "b2", "--serves", "%s#g1" % CAP, "start-work")
    assert done.returncode == 1, done.stdout
    assert "%s#g1" % CAP in done.stderr and "start-work" in done.stderr and "b1" in done.stderr, done.stderr
    assert state(ready_repo) == before


LINE = ("While an initiative is `started`, when the person runs `work abandon` on the initiative, `work` shall set "
        "the status of the initiative to `abandoned`.")


def test_serves_before_the_line_takes_the_job(ready_repo):
    """`--serves <job>` given before the line's text (b839): one argument, the job, the line the requirement added."""
    write_item(ready_repo, "b1", status="shaped")
    done = work(ready_repo, "line", "b1", "--into", CAP, "--group", "Abandoning", "--serves", "start-work", LINE)
    assert done.returncode == 0, (done.stdout, done.stderr)
    assert LINE in done.stdout and "serves start-work" in done.stdout, done.stdout
    text = (ready_repo / ".shop" / "backlog" / "b1.md").read_text()
    assert LINE in text and "start-work" in text, text


def test_serves_before_the_line_with_a_group_and_a_line_refused(ready_repo):
    """`--serves <cap>#g<n> <job>` takes two arguments; a line after them is refused, the item left as it was."""
    write_item(ready_repo, "b1", status="shaped")
    before = state(ready_repo)
    done = work(ready_repo, "line", "b1", "--into", CAP, "--serves", "%s#g1" % CAP, "start-work", LINE)
    assert done.returncode == 1 and "usage:" not in done.stderr, (done.stdout, done.stderr)
    assert state(ready_repo) == before
