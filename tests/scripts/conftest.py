"""The live spec's `model logic`, solved once per session (once per xdist worker) for every test that asks for it
(design-r3 §7): `live_logic` is `spec_solve.run` of this repository, its findings. A test that uses it is marked
`@pytest.mark.live_logic`, so `-m "not live_logic"` leaves out every test that solves the live spec.

`EXPECTED` is {"<code> <id> <id>": why} of the live findings that are known and open; the tests pass over them. A
finding is keyed by its code and ids, not its text, whose witness pre-state is one model of many (plan-r3 S12). Each
why is a question for the person (plan-r3 S11, `report-S11.md`); answering one removes its findings from here."""
import os
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]

# The tests against GitHub run only when they are given a repository to write to (requests r27-r41).
collect_ignore = [] if os.environ.get("SHOPSYSTEM_TEST_GITHUB_REPO") else ["test_request_github.py"]

# the questions of the live findings (report-S11.md, report-checker-gaps.md); every one was answered
# (report-answers.md) or went with supervision, retired in 0.31.0 (workflow simplification plan 9)
EXPECTED: dict[str, str] = {}


@pytest.fixture(scope="session")
def live_logic():
    import spec_solve
    toolchain.require()
    return spec_solve.run(REPO)


def expected(finding):
    """The why of a known open finding (`EXPECTED`), or None."""
    return EXPECTED.get(" ".join([finding.code] + list(finding.ids)))


@pytest.fixture(scope="session")
def live_expected():
    """`expected`, for a test module, which cannot import this conftest by name."""
    return expected


@pytest.fixture
def backlog_repo(tmp_path):
    """A git repository with an identity whose spec/index.md names the context `ex.com/prod/ctx`, all committed: the
    repository the backlog's script tests run `work` in."""
    import subprocess

    def git(*args):
        subprocess.run(["git", *args], cwd=tmp_path, capture_output=True, text=True, check=True)
    git("init", "-q", "-b", "main")
    for key, value in (("user.name", "T"), ("user.email", "t@example.com"), ("commit.gpgsign", "false")):
        git("config", key, value)
    (tmp_path / "spec").mkdir()
    (tmp_path / "spec/index.md").write_text("---\nid: bounded-context/ex.com/prod/ctx\n---\n# ctx\n")
    git("add", "-A")
    git("commit", "-q", "-m", "init")
    return tmp_path


GENERATE_SPEC = pathlib.Path(__file__).resolve().parent / "fixtures" / "generate" / "repo" / "spec"


@pytest.fixture
def ready_repo(backlog_repo):
    """`backlog_repo` with the codified spec of fixtures/generate/repo/ over its spec/, less the uncodified
    `legacy.md`, its index naming the context `ex.com/prod/ctx`, all committed (plan 3, D17): the repository an item's
    lines are written and readied in."""
    import re
    import shutil
    import subprocess
    shutil.copytree(GENERATE_SPEC, backlog_repo / "spec", dirs_exist_ok=True)
    (backlog_repo / "spec" / "capabilities" / "legacy.md").unlink()
    index = backlog_repo / "spec" / "index.md"
    index.write_text(re.sub(r"(?m)^id: .*$", "id: bounded-context/ex.com/prod/ctx", index.read_text(), count=1))
    for args in (("add", "-A"), ("commit", "-q", "-m", "a codified spec")):
        subprocess.run(["git", *args], cwd=backlog_repo, capture_output=True, text=True, check=True)
    return backlog_repo


@pytest.fixture
def batch_outside(tmp_path_factory):
    """The directory beside a batch repository: its bare remote, the stand-in gh and the stand-in's files."""
    return tmp_path_factory.mktemp("outside")


@pytest.fixture
def batch_repo(ready_repo, batch_outside, monkeypatch):
    """`ready_repo` with a bare repository in `batch_outside` as its `origin` (`main` pushed) and a committed
    `.shop/delivery.toml` whose `[batch] tests` is `python3 -c pass` and whose `[review] checks` is empty (a test of
    the brief's runs sets its own: test_batch_brief's `configure`); `gh` is the stand-in (D20), and no git or gh
    reaches a network or asks for a password (plan 4, Task 1)."""
    import subprocess

    from batch_testing import gh_env

    def git(*args):
        subprocess.run(["git", *args], cwd=ready_repo, capture_output=True, text=True, check=True)
    (ready_repo / ".shop").mkdir(exist_ok=True)
    (ready_repo / ".shop" / "delivery.toml").write_text('[batch]\ntests = "python3 -c pass"\n\n[review]\nchecks = []\n')
    git("add", "-A")
    git("commit", "-q", "-m", "delivery")
    subprocess.run(["git", "init", "-q", "--bare", str(batch_outside / "origin.git")], check=True, capture_output=True)
    git("remote", "add", "origin", str(batch_outside / "origin.git"))
    git("push", "-q", "origin", "main")
    for key, value in gh_env(batch_outside).items():
        monkeypatch.setenv(key, value)
    return ready_repo
