"""U20 (b60): while this repository is in the workspace of a task, a service that would keep a kept change refuses the
request and names the task. A task's workspace is its branch `batch-<n>-b<j>` (its task read from the batch's plan on
the base), and every command that keeps a change does so through shop_files.committed, which refuses there first
(refuse_task_branch): each command below exits 1 naming the task, and nothing is committed or written."""
import pytest

from backlog_testing import git, state, work, write_item
from test_directive import quote
from test_record_write import body, with_readme

TASK_BRANCH = "batch-1-b1"
PLAN = ("---\nid: batch/ex.com/prod/ctx/batch-1\nkind: batch\nstatus: building\nbase: main\nforked_from: %s\n"
        "branch: batch-1\npull_request:\n---\n\n# batch-1\n\n## Tasks\n\n| task | item | status | branch |\n"
        "|---|---|---|---|\n| t2 | b1 | running | %s |\n" % ("0" * 40, TASK_BRANCH))

COMMANDS = {
    "idea": lambda repo, factory: ("idea", "Another thing"),
    "record": lambda repo, factory: ("record", "What was found", "--kind", "analysis", "--summary", "found",
                                     "--body", body(factory), "--date", "2026-11-05"),
    "decision": lambda repo, factory: ("decision", "Decide the thing", "--summary", "Decided: so.", "--decision",
                                       "So it is.", "--tier", "judgement"),
    "directive": lambda repo, factory: ("directive", "--quote", "quote-1"),
    "line": lambda repo, factory: ("line", "b1", "--capability", "shelf", "--narrator", "n", "Things kept."),
    "annotate": lambda repo, factory: ("annotate", "b1", "A note."),
}


@pytest.fixture
def tasked(ready_repo):
    """ready_repo with an item b1, a records README and a quote, and the plan of batch-1 whose task t2 builds b1 on
    `batch-1-b1`, all committed on main; then `batch-1-b1` checked out."""
    write_item(ready_repo, "b1", status="shaped")
    with_readme(ready_repo)
    quote(ready_repo)
    plan = ready_repo / ".shop" / "batches" / "1" / "plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text(PLAN)
    git(ready_repo, "add", "-A")
    git(ready_repo, "commit", "-q", "-m", "batch-1")
    git(ready_repo, "checkout", "-q", "-b", TASK_BRANCH)
    return ready_repo


@pytest.mark.parametrize("command", sorted(COMMANDS))
def test_a_command_that_keeps_a_change_is_refused_on_a_task_branch_naming_the_task(tasked, tmp_path_factory,
                                                                                   command):
    before = state(tasked)
    done = work(tasked, *COMMANDS[command](tasked, tmp_path_factory))
    assert done.returncode == 1, (done.stdout, done.stderr)
    assert "task t2 of batch-1" in done.stderr and TASK_BRANCH in done.stderr, done.stderr
    assert state(tasked) == before


@pytest.mark.parametrize("command", ["idea", "decision"])
def test_the_same_command_keeps_its_change_on_the_base(tasked, tmp_path_factory, command):
    git(tasked, "checkout", "-q", "main")
    before = state(tasked)
    done = work(tasked, *COMMANDS[command](tasked, tmp_path_factory))
    assert done.returncode == 0, done.stderr
    assert state(tasked)[0] != before[0]
