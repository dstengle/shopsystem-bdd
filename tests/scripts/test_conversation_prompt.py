"""The UserPromptSubmit hook's `work quote --hook` (conversation r2, plan 8 D5): the session and its transcript kept
in the git dir for `work quote`, never committed, nothing printed, never failing, and fast on a large backlog."""
import json
import statistics
import subprocess
import time

import conversation_prompt as P
import pytest
import transcript_testing as T
from backlog_testing import git, work
from measure_batch_read import project_dir


@pytest.fixture
def store(tmp_path, monkeypatch):
    path = tmp_path / "store"
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(path))
    return path


def hook(cwd, stdin):
    return subprocess.run(T.hook_command("UserPromptSubmit", "quote"), cwd=cwd, input=stdin, capture_output=True,
                          text=True, timeout=30)


def prompt(session, path, **more):
    return json.dumps({"session_id": session, "transcript_path": str(path), "hook_event_name": "UserPromptSubmit",
                       "prompt": "x", **more})


def shopped(repo):
    """The repository with a `.shop/` (a backlog item), committed."""
    T.crowded(repo, items=1, batches=0)
    return repo


def test_the_hook_keeps_the_session_for_work_quote(backlog_repo, store):
    shopped(backlog_repo)
    path = T.write(project_dir(backlog_repo), "s-1", T.CONVERSATION)
    done = hook(backlog_repo, prompt("s-1", path))
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
    assert P.kept(backlog_repo) == ("s-1", str(path))
    done = work(backlog_repo, "quote", T.TEXTS[2])
    assert done.returncode == 0, done.stderr
    assert done.stdout.startswith('quote-1 "')
    assert "\nsession: s-1\n" in (backlog_repo / ".shop/quotes/1.md").read_text()


def gitdir_file(repo):
    (repo / ".git" / "shopsystem").write_text("not a directory")


CASES = {
    "not json": ("not json", "repo", None),
    "no keys": ("{}", "repo", None),
    "not strings": ('{"session_id": 3, "transcript_path": "x"}', "repo", None),
    "outside git": (prompt("s-1", "x"), "outside", None),
    "no .shop": (prompt("s-1", "x"), "bare", None),
    "git dir unwritable": (prompt("s-1", "x"), "repo", gitdir_file),
}


@pytest.mark.parametrize("case", sorted(CASES))
def test_the_prompt_hook_never_fails(backlog_repo, tmp_path_factory, case):
    """Review Focus 3."""
    stdin, where, spoil = CASES[case]
    if where == "repo":
        shopped(backlog_repo)
    cwd = tmp_path_factory.mktemp("outside") if where == "outside" else backlog_repo
    if spoil:
        spoil(backlog_repo)
    status = git(backlog_repo, "status", "--porcelain")
    done = hook(cwd, stdin)
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
    assert git(backlog_repo, "status", "--porcelain") == status
    assert not (backlog_repo / ".git" / "shopsystem" / "prompt.json").exists()
    assert not (cwd / "shopsystem").exists() and not (backlog_repo / "shopsystem").exists()


def test_the_pointer_is_the_last_prompts_session(backlog_repo, store):
    """Review Focus 5."""
    shopped(backlog_repo)
    one = T.write(project_dir(backlog_repo), "s-1", T.CONVERSATION)
    two = T.write(project_dir(backlog_repo), "s-2", [T.person("Something else entirely.", "v1", T.at(9), "s-2")])
    assert hook(backlog_repo, prompt("s-1", one)).returncode == 0
    assert hook(backlog_repo, prompt("s-2", two)).returncode == 0
    assert P.kept(backlog_repo) == ("s-2", str(two))
    done = work(backlog_repo, "quote", T.TEXTS[2])
    assert done.returncode == 1 and "s-2" in done.stderr and "--session" in done.stderr, done.stderr
    done = work(backlog_repo, "quote", T.TEXTS[2], "--session", "s-1")
    assert done.returncode == 0, done.stderr


def test_a_stale_pointer_is_refused_naming_its_path(backlog_repo, store):
    """Review Focus 5."""
    shopped(backlog_repo)
    path = T.write(project_dir(backlog_repo), "s-1", T.CONVERSATION)
    assert hook(backlog_repo, prompt("s-1", path)).returncode == 0
    path.unlink()
    done = work(backlog_repo, "quote", T.TEXTS[2])
    assert done.returncode == 1 and str(path) in done.stderr, done.stderr


def test_no_session_known_is_refused(backlog_repo, store):
    done = work(backlog_repo, "quote", T.TEXTS[2])
    assert done.returncode == 1
    assert "work quote --hook" in done.stderr and "--session" in done.stderr, done.stderr


def test_a_failed_rename_leaves_nothing_behind(backlog_repo):
    """Review M4."""
    shopped(backlog_repo)
    (backlog_repo / ".git" / "shopsystem" / "prompt.json").mkdir(parents=True)
    done = hook(backlog_repo, prompt("s-1", "x"))
    assert (done.returncode, done.stdout, done.stderr) == (0, "", "")
    assert sorted(p.name for p in (backlog_repo / ".git" / "shopsystem").iterdir()) == ["prompt.json"]


def test_a_prompt_from_outside_the_repository_is_ignored(backlog_repo, tmp_path_factory):
    """Review Q3: the pointer is the session's whose cwd is in this repository."""
    shopped(backlog_repo)
    elsewhere = tmp_path_factory.mktemp("elsewhere")
    assert hook(backlog_repo, prompt("s-1", "x", cwd=str(elsewhere))).returncode == 0
    assert P.kept(backlog_repo) is None
    (backlog_repo / "sub").mkdir()
    assert hook(backlog_repo, prompt("s-2", "y", cwd=str(backlog_repo / "sub"))).returncode == 0
    assert P.kept(backlog_repo) == ("s-2", "y")


@pytest.mark.usefixtures("store")
@pytest.mark.parametrize("spoil", ["{not json", "[]"])
def test_an_unreadable_pointer_is_refused_naming_it(backlog_repo, spoil):
    """Review M3: not the refusal of no pointer at all."""
    target = backlog_repo / ".git" / "shopsystem" / "prompt.json"
    target.parent.mkdir()
    target.write_text(spoil)
    done = work(backlog_repo, "quote", T.TEXTS[2])
    assert done.returncode == 1
    assert "the pointer %s the UserPromptSubmit hook keeps cannot be read; give --session <id>" % target in \
        done.stderr, done.stderr


def test_hook_takes_no_words(backlog_repo):
    done = work(backlog_repo, "quote", "some words", "--hook")
    assert done.returncode == 1 and "work quote: --hook takes no words" in done.stderr, done.stderr


def test_the_hook_is_wired():
    hooks = json.loads((T.Path(__file__).resolve().parents[2] / "hooks/hooks.json").read_text())["hooks"]
    commands = [h["command"] for group in hooks["UserPromptSubmit"] for h in group["hooks"]]
    assert len(commands) == 2
    assert commands[0].endswith('migrate" prompting') and commands[1].endswith('work" quote --hook'), commands


@pytest.mark.timing
def test_the_prompt_hook_is_fast(backlog_repo, store):
    """Review Focus 3: the hook's wall time on 200 items and 20 batches, the median of three runs."""
    T.crowded(backlog_repo)
    path = T.write(project_dir(backlog_repo), "s-1", T.CONVERSATION)
    took = []
    for _ in range(3):
        start = time.monotonic()
        assert hook(backlog_repo, prompt("s-1", path)).returncode == 0
        took.append(time.monotonic() - start)
    print("the prompt hook's median: %.2f s" % statistics.median(took))
    assert statistics.median(took) < 1.0, took
