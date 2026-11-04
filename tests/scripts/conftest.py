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

# the questions of the live findings (report-S11.md, report-checker-gaps.md)
Q_STAGE = ("question: `include` is measurement-wide, so a stage's figure given for one stage and withheld for "
           "another clashes; say it per stage, or drop the negative Then?")
Q_RELEASE = ("question: \"a repository\" in r13-r16 is not the repository `migrate upgrade` runs in, so two "
             "repositories (one behind, one current) fire both; say \"the repository\", and define its release in "
             "the controlled language (one value of behind, outdated, uncodified, current) so `current` excludes "
             "the pending steps?")
Q_LINES = ("question: \"every line settled\" needs `no request line is not settled`, which the translation "
           "refuses; allow `no K is not C`, or reword r20-r22?")
Q_CLOSED = ("question: should r26 read \"no work-item of the initiative is open\" and yield to r29 and r34? (the "
            "check now reads `open` through its definition under `no`)")
Q_ONE = ("question: the condition's noun phrase is an indefinite with no tie to the trigger's (the initiative's "
         "branch, its work-items, the result's change list, the work-item's question, the glossary-proposal's "
         "questions), so two of them may differ; tie it (\"a question on the work-item\", \"a change list the "
         "result gives\") or say \"the K\", which the check reads as the one K?")
Q_RESULT = ("question: one stage is with one result (the check reads `stage with result` as functional), so the "
            "pair fires only on a DONE result that is also fixing, strange, unparsing or unheld; are those "
            "exclusive of DONE (define the condition, or name the exception in r43, r57, r63, r76)?")


EXPECTED: dict[str, str] = {
    "L1 batch-measurement#r8 batch-measurement#r14": Q_STAGE,
    "L1 batch-measurement#r12 batch-measurement#r13": Q_STAGE,
    "L1 migration-tools#r13 migration-tools#r14": Q_RELEASE,
    "L1 migration-tools#r14 migration-tools#r15": Q_RELEASE,
    "L1 migration-tools#r14 migration-tools#r16": Q_RELEASE,
    "L1 requests#r20 requests#r21": Q_LINES,
    "L1 requests#r20 requests#r22": Q_LINES,
    "L1 requests#r21 requests#r22": Q_LINES,
    "L1 supervision#r26 supervision#r27": Q_CLOSED,
    "L1 supervision#r26 supervision#r28": Q_CLOSED,
    "L1 supervision#r26 supervision#r29": Q_CLOSED,
    "L1 supervision#r26 supervision#r34": Q_CLOSED,
    "L1 supervision#r39 supervision#r40": Q_ONE,
    "L1 supervision#r39 supervision#r41": Q_ONE,
    "L6 supervision#r42 supervision#r43": Q_RESULT,
    "L6 supervision#r57 supervision#r61": Q_RESULT,
    "L6 supervision#r62 supervision#r63": Q_RESULT,
    "L1 supervision#r71 supervision#r72": Q_ONE,
    "L6 supervision#r73 supervision#r76": Q_RESULT,
    "L1 supervision#r76 supervision#r77": Q_ONE,
    "L1 work-queue#r20 work-queue#r21": Q_ONE,
    "L1 work-queue#r20 work-queue#r22": Q_ONE,
    "L1 work-queue#r20 work-queue#r23": Q_ONE,
    "L1 work-queue#r20 work-queue#r24": Q_ONE,
    "L1 work-queue#r21 work-queue#r22": Q_ONE,
    "L1 work-queue#r21 work-queue#r23": Q_ONE,
    "L1 work-queue#r21 work-queue#r24": Q_ONE,
    "L1 work-queue#r22 work-queue#r24": Q_ONE,
    "L1 work-queue#r23 work-queue#r24": Q_ONE,
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
