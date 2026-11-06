"""`work names` (conversation r4, plan 8 D8): every item and batch with its name beside its id, and the SessionStart
hook's `work names --hook`, silent with nothing to show, never failing and fast on a large backlog."""
import json
import statistics
import subprocess
import time

import backlog_items
import batch_plan
import pytest
import transcript_testing as T
from backlog_testing import git, work

HEAD = ["| id | name | status |", "|---|---|---|"]


def item(repo, n, title, status):
    found = backlog_items.Item("b%d" % n, "item/ex.com/prod/ctx/b%d" % n, title, status, "own")
    path = repo / backlog_items.rel_of(found.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(backlog_items.render(found))


def batch(repo, n, *items, status="building"):
    tasks = [batch_plan.Task("t%d" % k, b, "pending", "batch-%d-%s" % (n, b)) for k, b in enumerate(items, 1)]
    found = batch_plan.Batch("batch-%d" % n, "batch/ex.com/prod/ctx/batch-%d" % n, status, "main", "0" * 40,
                             "batch-%d" % n, None, tasks)
    path = repo / batch_plan.rel_of(found.name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(batch_plan.render(found))


def commit(repo):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "items and batches")
    return repo


@pytest.fixture
def named(backlog_repo):
    item(backlog_repo, 1, "Fix the parser", "shaped")
    item(backlog_repo, 2, "Exit", "delivered")
    batch(backlog_repo, 1, "b1")
    return commit(backlog_repo)


def hook(cwd):
    return subprocess.run(T.hook_command("SessionStart", "names"), cwd=cwd, input=json.dumps(
        {"session_id": "s-1", "hook_event_name": "SessionStart", "source": "startup"}), capture_output=True, text=True,
        timeout=30)


def test_the_table_names_every_item_and_batch(named):
    done = work(named, "names")
    assert done.returncode == 0, done.stderr
    assert done.stdout.splitlines() == HEAD + ['| b1 | Fix the parser | shaped |', '| b2 | Exit | delivered |',
                                               '| batch-1 | b1 "Fix the parser" | building |']


def test_a_batch_of_a_missing_item_names_it_missing(named):
    batch(named, 2, "b2", "b9", status="merged")
    commit(named)
    assert '| batch-2 | b2 "Exit", b9 (missing) | merged |' in work(named, "names").stdout.splitlines()


def test_a_title_with_a_bar_is_escaped(backlog_repo):
    item(backlog_repo, 1, "a | b", "idea")
    commit(backlog_repo)
    assert "| b1 | a \\| b | idea |" in work(backlog_repo, "names").stdout.splitlines()


def test_the_hook_says_why_before_the_table(named):
    done = hook(named)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    lines = done.stdout.splitlines()
    assert lines[0] == ("The names of this repository's items and batches: tell the person each by its name beside "
                        'its id (b3 "Fix the parser"), never by its id alone.')
    assert lines[1:] == work(named, "names").stdout.splitlines()


def test_nothing_to_name_is_silent_in_the_hook(backlog_repo):
    (backlog_repo / ".shop").mkdir()
    (backlog_repo / ".shop" / "delivery.toml").write_text("")
    commit(backlog_repo)
    done = hook(backlog_repo)
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
    done = work(backlog_repo, "names")
    assert done.returncode == 0
    assert done.stdout == "there is no item in .shop/backlog/ and no batch in .shop/batches/\n"


def malformed(repo):
    item(repo, 1, "Fix the parser", "shaped")
    path = repo / ".shop/backlog/b1.md"
    path.write_text(path.read_text().replace("kind: item", "kind: thing"))
    return repo, "work names: .shop/backlog/b1.md: kind"


def outside_git(repo):
    return repo.parent / ("%s-outside" % repo.name), ""


def no_shop(repo):
    return repo, ""


def subdirectory(repo):
    item(repo, 1, "Fix the parser", "shaped")
    (repo / "spec" / "deeper").mkdir()
    return repo / "spec" / "deeper", '| b1 | Fix the parser | shaped |'


@pytest.mark.parametrize("case", [malformed, outside_git, no_shop, subdirectory], ids=lambda f: f.__name__)
def test_the_names_hook_never_fails(backlog_repo, case):
    """Review Focus 3."""
    cwd, said = case(backlog_repo)
    cwd.mkdir(exist_ok=True)
    commit(backlog_repo) if git(backlog_repo, "status", "--porcelain") else None
    status = git(backlog_repo, "status", "--porcelain")
    done = hook(cwd)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    if case is subdirectory:
        assert said in done.stdout.splitlines()
    else:
        assert len(done.stdout.splitlines()) <= 1 and done.stdout.startswith(said), done.stdout
        assert bool(done.stdout) == bool(said), done.stdout
    assert git(backlog_repo, "status", "--porcelain") == status


def test_the_hook_is_wired():
    hooks = json.loads((T.Path(__file__).resolve().parents[2] / "hooks/hooks.json").read_text())["hooks"]
    commands = [h["command"] for group in hooks["SessionStart"] for h in group["hooks"]]
    assert len(commands) == 3       # the third, the requests' `request_hook watch` (b79, r54-r56)
    assert commands[0].endswith('migrate" status --hook') and commands[1].endswith('conversation_hook" names'), commands
    assert commands[2].endswith('request_hook" watch'), commands


@pytest.mark.timing
def test_the_names_hook_is_fast(backlog_repo):
    """Review Focus 3: the hook's wall time on 200 items and 20 batches, the median of three runs."""
    T.crowded(backlog_repo)
    took = []
    for _ in range(3):
        start = time.monotonic()
        done = hook(backlog_repo)
        took.append(time.monotonic() - start)
        assert done.returncode == 0, done.stderr
    rows = [line for line in done.stdout.splitlines() if line.startswith("| b")]
    assert len(rows) == 220 and len([line for line in done.stdout.splitlines() if line.startswith("|")]) == 222
    print("the names hook's median: %.2f s" % statistics.median(took))
    assert statistics.median(took) < 1.0, took
