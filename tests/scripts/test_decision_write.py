"""`work decision` (decision-tiers r7, r8): the decision's file in the form `model` reads, numbered after the highest,
the index rewritten as `model decisions` writes it, both committed alone; refused with no tier, or on an id already
taken, changing nothing."""
import subprocess
import sys

from backlog_testing import SCRIPTS, git, state, work
from shop_files import frontmatter


def decide(repo, *more, title="Decide the thing"):
    return work(repo, "decision", title, "--summary", "The thing is decided: so.", "--decision", "So it is.", *more)


def test_the_decision_is_written_whole(backlog_repo, tmp_path_factory):
    alternatives = tmp_path_factory.mktemp("text") / "alternatives.md"
    alternatives.write_text("- Not deciding.\n- Deciding later.\n")
    done = decide(backlog_repo, "--tier", "judgement", "--context", "It came up.", "--alternatives",
                  "@%s" % alternatives, "--source", "record/one", "--by", "the person, 2026-11-05",
                  "--date", "2026-11-05")
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "spec/decisions/0001-decide-the-thing.md"
    text = (backlog_repo / "spec/decisions/0001-decide-the-thing.md").read_text()
    data, body = frontmatter(text)
    assert data == {"id": "design-decision/ex.com/prod/ctx/decide-the-thing", "summary": "The thing is decided: so.",
                    "date": "2026-11-05", "status": "accepted", "tier": "judgement", "source": ["record/one"],
                    "by": "the person, 2026-11-05"}
    assert body == ("# 0001. Decide the thing\n\n## Context\n\nIt came up.\n\n## Decision\n\nSo it is.\n\n"
                    "## Alternatives\n\n- Not deciding.\n- Deciding later.\n")


def test_the_index_is_rewritten_and_both_committed(backlog_repo):
    before = git(backlog_repo, "rev-parse", "HEAD")
    assert decide(backlog_repo, "--tier", "judgement").returncode == 0
    assert git(backlog_repo, "rev-parse", "HEAD~1").strip() == before.strip()
    files = git(backlog_repo, "show", "--name-only", "--format=", "HEAD").split()
    assert sorted(files) == ["spec/decisions/0001-decide-the-thing.md", "spec/decisions/index.md"]
    assert git(backlog_repo, "log", "-1", "--format=%s") == "work decision: 0001. Decide the thing\n"
    assert git(backlog_repo, "status", "--porcelain") == ""
    index = (backlog_repo / "spec/decisions/index.md").read_text()
    assert "[design-decision/ex.com/prod/ctx/decide-the-thing](0001-decide-the-thing.md)" in index


def test_model_decisions_check_holds_after_it(backlog_repo):
    assert decide(backlog_repo, "--tier", "judgement").returncode == 0
    done = subprocess.run([sys.executable, str(SCRIPTS / "model"), "--root", str(backlog_repo), "decisions",
                           "--check"], capture_output=True, text=True, timeout=120)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "spec/decisions/index.md is current" in done.stdout


def test_the_number_follows_the_highest(backlog_repo):
    (backlog_repo / "spec/decisions").mkdir()
    (backlog_repo / "spec/decisions/0041-old.md").write_text("---\nid: design-decision/ex.com/prod/ctx/old\n---\n")
    git(backlog_repo, "add", "-A")
    git(backlog_repo, "commit", "-q", "-m", "old")
    done = decide(backlog_repo, "--tier", "check", "--enforced-by", "tests/test_x.py::test_x")
    assert done.stdout.strip() == "spec/decisions/0042-decide-the-thing.md", done.stderr
    data, _ = frontmatter((backlog_repo / done.stdout.strip()).read_text())
    assert data["enforced_by"] == ["tests/test_x.py::test_x"]


def test_no_tier_is_refused_naming_it(backlog_repo):
    before = state(backlog_repo)
    done = decide(backlog_repo)
    assert done.returncode == 1
    assert "--tier" in done.stderr
    assert state(backlog_repo) == before
    assert not (backlog_repo / "spec/decisions").exists()


def test_every_absent_argument_is_named_at_once(backlog_repo):
    before = state(backlog_repo)
    done = work(backlog_repo, "decision", "Decide the thing")
    assert done.returncode == 1
    assert all(option in done.stderr for option in ("--summary", "--decision", "--tier")), done.stderr
    assert "--tier" not in work(backlog_repo, "decision", "Decide it", "--tier", "check").stderr
    assert state(backlog_repo) == before


def test_an_id_taken_is_refused(backlog_repo):
    assert decide(backlog_repo, "--tier", "judgement").returncode == 0
    before = state(backlog_repo)
    done = decide(backlog_repo, "--tier", "judgement")
    assert done.returncode == 1 and "decide-the-thing" in done.stderr and "--slug" in done.stderr
    assert state(backlog_repo) == before
    assert decide(backlog_repo, "--tier", "judgement", "--slug", "decide-it-again").returncode == 0


def test_help_says_what_it_writes():
    done = subprocess.run([sys.executable, str(SCRIPTS / "work"), "decision", "--help"], capture_output=True,
                          text=True)
    assert done.returncode == 0
    for word in ("spec/decisions/<nnnn>-<slug>.md", "spec/decisions/index.md", "--tier", "@<file>", "commit"):
        assert word in done.stdout, word
