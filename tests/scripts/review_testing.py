"""What the pull request review's script tests share (plan 5, Task 1): a batch published as a pull request, the
scratch findings file `pr-reviewer` would write, and findings texts in D9's form."""
from backlog_testing import git, work
from batch_testing import commit_on, ready_item
from test_backlog_lines import ABANDON
from test_batch_pick import SECOND
from test_batch_tasks import build, resumed

URL = "https://github.com/ex/ctx/pull/1"

FIX_NOW_B1 = """## Verdict

The batch builds both items; one finding to fix.

## Findings

### Important fix now: abandon leaves the initiative started
- item: b1
- where: src/b1.txt:1
The line says `abandoned`; the code writes `started`.

### Minor observation: the message could name the initiative
- item: -
- where: -
A note.
"""

CLEAN = """## Verdict

The batch builds both items.

## Findings

None.
"""

FIXED_F1 = CLEAN + """
## Earlier findings
- f1: fixed
"""


def ok(done):
    assert done.returncode == 0, done.stderr
    return done


def published(repo):
    """`batch_repo` with b1 and b2 ready, a batch started and resumed, both tasks built (b1 with `src/b1.txt`) and
    done, and the batch reviewed: its pull request's URL."""
    ready_item(repo, "b1", "Abandon", ABANDON, value="high-value", urgency="high-urgency", size="small")
    ready_item(repo, "b2", "Exit", SECOND)
    ok(work(repo, "batch", "start"))
    resumed(repo)
    build(repo, "t1", "b1", ["r5"])
    commit_on(repo, "batch-1-b1", "src/b1.txt", "abandoned\n", "b1's code\n\nItem: b1")
    build(repo, "t2", "b2", ["r6"])
    for task in ("t1", "t2"):
        ok(work(repo, "batch", "done", "batch-1", task))
    return ok(work(repo, "batch", "review", "batch-1")).stdout.strip().splitlines()[-1]


def scratch(repo, k=1):
    return repo / ".shop" / "worktrees" / ("batch-1-review-%d" % k)


def findings(repo, k=1):
    """The findings file of review k, its directory made."""
    path = scratch(repo, k) / "findings.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def head(repo, ref="batch-1"):
    return git(repo, "rev-parse", ref).strip()
