"""The live spec's `model logic`, solved once per session (once per xdist worker) for every test that asks for it
(design-r3 §7): `live_logic` is `spec_solve.run` of this repository, its findings. A test that uses it is marked
`@pytest.mark.live_logic`, so `-m "not live_logic"` leaves out every test that solves the live spec.

`EXPECTED` is {"<code> <id> <id>": why} of the live findings that are known and open; the tests pass over them. A
finding is keyed by its code and ids, not its text, whose witness pre-state is one model of many (plan-r3 S12). Each
why is a question for the person (plan-r3 S11, `report-S11.md`); answering one removes its findings from here."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]

# the questions of the live findings (report-S11.md, report-checker-gaps.md); Q_STAGE, Q_RELEASE, Q_LINES and Q_CLOSED
# were answered (report-answers.md)
Q_CODIFIED = ("question: codified and uncodified (of a change list) stay prose, so one change list may be both: the "
              "lexicon has no relation from a capability to a change list (report-answers.md); add a row `capability "
              "| named in | change list` and define them with `codified` of a capability?")
Q_RESULT = ("question: one stage is with one result (the check reads `stage with result` as functional), so the "
            "pair fires only on a DONE result that is also fixing, strange, unparsing or unheld; are those "
            "exclusive of DONE (define the condition, or name the exception in r43, r57, r63, r76)?")


EXPECTED: dict[str, str] = {
    "L6 supervision#r42 supervision#r43": Q_RESULT,
    "L6 supervision#r57 supervision#r61": Q_RESULT,
    "L6 supervision#r62 supervision#r63": Q_RESULT,
    "L6 supervision#r73 supervision#r76": Q_RESULT,
    "L6 supervision#r76 supervision#r77": Q_CODIFIED,
}


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
