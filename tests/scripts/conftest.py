"""The live spec's `model logic`, solved once per session (once per xdist worker) for every test that asks for it
(design-r3 §7): `live_logic` is `spec_solve.run` of this repository, its findings. A test that uses it is marked
`@pytest.mark.live_logic`, so `-m "not live_logic"` leaves out every test that solves the live spec.

`EXPECTED` is {finding text: why} of the live findings that are known and open; the tests pass over them. Each why
is a question for the person (plan-r3 S11, `report-S11.md`); answering one removes its findings from here."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import toolchain

REPO = pathlib.Path(__file__).resolve().parents[2]

# the questions of the live findings (report-S11.md)
Q_STAGE = ("question: `include` is measurement-wide, so a stage's figure given for one stage and withheld for "
           "another clashes; say it per stage, or drop the negative Then?")
Q_RELEASE = ("question: define a repository's release in the controlled language (one value of behind, outdated, "
             "uncodified, current), so `current` excludes the pending steps?")
Q_LINES = ("question: \"every line settled\" needs `no request line is not settled`, which the translation "
           "refuses; allow `no K is not C`, or reword r20-r22?")
Q_CLOSED = ("question: should r26 read \"no work-item of the initiative is open\" and yield to r29 and r34; and "
            "should the check expand `open` under `no`?")
Q_ONE = ("question: the condition's noun phrase is not tied to the trigger's (the initiative's branch, its "
         "work-items, the result's change list, the work-item's question); is it one per trigger, and how is "
         "that said?")
Q_RESULT = ("question: a stage ends with one result and is for one node; give `stage with result` and `stage for "
            "node` cardinality one, and the check read it, then name the exceptions in r43, r57, r63, r76?")
Q_COMPLETE = ("question: `complete` is defined with \"every\", which the check does not expand; expand it, or have "
              "r5 name the closed capability-proposals?")


EXPECTED: dict[str, str] = {
    ("batch-measurement#r8 and #r14 clash: on \"the person runs `measure initiative i7-cart`\" with a "
     "transcript that is `found`, a transcript that is `lost`, r8 obliges and r14 forbids `measure` to "
     "include round_trips"): Q_STAGE,
    ("batch-measurement#r12 and #r13 clash: on \"the person runs `measure initiative i7-cart`\" with a session "
     "file that is `empty`, a logged stage that is `unended`, r12 obliges and r13 forbids `measure` to "
     "include turns"): Q_STAGE,
    ("migration-tools#r13 and #r14 clash: on \"the person runs `migrate upgrade`\", r13 obliges `migrate` to "
     "rewrite `.shop/plugin-version` and r14 changes nothing"): Q_RELEASE,
    ("migration-tools#r14 and #r15 clash: on \"the person runs `migrate upgrade`\", r14 changes nothing and r15 "
     "obliges `migrate` to rewrite `.shop/work/i1/w1.md`"): Q_RELEASE,
    ("migration-tools#r14 and #r16 clash: on \"the person runs `migrate upgrade`\", r14 changes nothing and r16 "
     "obliges `migrate` to rewrite `spec/capabilities/cart.md`"): Q_RELEASE,
    ("requests#r20 and #r21 clash: on \"the person runs `work turn` on a request that is `open`\" with a "
     "request line that is `accepted`, a request that is `open`, r20 sets the status of a request to "
     "`awaiting-asker` and r21 to `accepted`"): Q_LINES,
    ("requests#r20 and #r22 clash: on \"the person runs `work turn` on a request that is `open`\" with a "
     "request line that is `refused`, a request that is `open`, r20 sets the status of a request to "
     "`awaiting-asker` and r22 to `refused`"): Q_LINES,
    ("requests#r21 and #r22 clash: on \"the person runs `work turn` on a request that is `open`\" with a "
     "request line that is `refused`, a request line that is `accepted`, a request that is `open`, r21 sets "
     "the status of a request to `accepted` and r22 to `refused`"): Q_LINES,
    ("supervision#r26 and #r27 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "work-item that is `awaiting-answer`, a work-item that is `green`, an initiative that is `started`, r26 "
     "exits successfully and r27 with an error"): Q_CLOSED,
    ("supervision#r26 and #r28 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "work-item that is `failed`, a work-item that is `green`, an initiative that is `started`, r26 exits "
     "successfully and r28 with an error"): Q_CLOSED,
    ("supervision#r26 and #r29 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "request that is `asker`, a work-item that is `green`, an initiative that is `started`, r26 exits "
     "successfully and r29 with an error"): Q_CLOSED,
    ("supervision#r26 and #r34 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "work-item that is `green`, a work-item that is `green`, an initiative that is `started`, r26 exits "
     "successfully and r34 with an error"): Q_CLOSED,
    ("supervision#r39 and #r40 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "work-item that is `green`, a work-item that is `green`, an initiative that is `started`, r39 obliges "
     "and r40 forbids `work run` to start a stage"): Q_ONE,
    ("supervision#r39 and #r41 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "work-item that is `green`, an initiative that is `started`, r39 obliges and r41 forbids `work run` to "
     "start a stage"): Q_ONE,
    ("supervision#r42 and #r43 clash: on \"a session ends a `branch review` stage for a `started` initiative "
     "with the result\" with a work-item that is `green`, an initiative that is `started`, a result that is "
     "`DONE`, a work-item that is `green`, a stage that is `branch review`, an initiative that is `started`, "
     "r42 obliges and r43 forbids `work run` to draft a work-item"): Q_RESULT,
    ("supervision#r46 and #r47 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "delegation that is `written`, a glossary-proposal that is `awaiting-answer`, a delegation that is "
     "`written`, a work-item that is `awaiting-answer`, an initiative that is `started`, r46 obliges and r47 "
     "forbids `work run` to start a stage"): Q_RESULT,
    ("supervision#r57 and #r61 clash: on \"a session ends an `integrate` stage for a `started` initiative with "
     "a result that is `DONE`\" with an initiative that is `started`, a stage that is `integrate`, an "
     "initiative that is `started`, a result that is `DONE`, r57 obliges and r61 forbids `work run` to draft "
     "a capability-proposal"): Q_RESULT,
    ("supervision#r57 and #r63 clash: on \"a session ends an `integrate` stage for a `started` initiative with "
     "a result that is `DONE`\" with a result that is `DONE`, a stage that is `integrate`, an initiative that "
     "is `started`, a result that is `DONE`, r57 obliges and r63 forbids `work run` to draft a "
     "capability-proposal"): Q_RESULT,
    ("supervision#r62 and #r63 clash: on \"a session ends an `integrate` stage for a capability-proposal with "
     "the result\" with a result that is `DONE`, a stage that is `integrate`, r62 sets the status of a "
     "capability-proposal to `awaiting-answer` and r63 to `drafted`"): Q_RESULT,
    ("supervision#r71 and #r72 clash: on \"the person runs `work run` on a `started` initiative\" with a "
     "glossary-proposal that is `awaiting-answer`, an initiative that is `started`, r71 obliges and r72 "
     "forbids `work run` to start a stage"): Q_ONE,
    ("supervision#r73 and #r76 clash: on \"a session ends an `apply` stage for a capability-proposal with the "
     "result\" with a result that is `DONE`, a stage that is `apply`, r73 forbids and r76 obliges `work run` "
     "to start a stage"): Q_RESULT,
    ("supervision#r76 and #r77 clash: on \"a session ends an `apply` stage for a capability-proposal with a "
     "result that is `DONE`\" with a result that is `DONE`, a stage that is `apply`, a result that is `DONE`, "
     "r76 sets the status of a capability-proposal to `formulated` and r77 to `approved`"): Q_ONE,
    ("work-queue#r5 and #r7 clash: on \"the person runs `work withdraw` on a work-item that is `ready`\" with "
     "an initiative that is `started`, a work-item that is `green`, a work-item that is `green`, a "
     "capability-proposal that is `formulated`, a work-item that is `ready`, r5 obliges and r7 forbids `work` "
     "to set the status of an initiative to `done`"): Q_COMPLETE,
    ("work-queue#r20 and #r21 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `plan`, a question that is `research`, a work-item that is "
     "`awaiting-answer`, r20 sets the status of a work-item to `drafted` and r21 to `researched`"): Q_ONE,
    ("work-queue#r20 and #r22 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `implement`, a question that is `research`, a work-item that "
     "is `awaiting-answer`, r20 sets the status of a work-item to `drafted` and r22 to `ready`"): Q_ONE,
    ("work-queue#r20 and #r23 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `review`, an answer that is `--change`, a question that is "
     "`research`, a work-item that is `awaiting-answer`, r20 sets the status of a work-item to `drafted` and "
     "r23 to `ready`"): Q_ONE,
    ("work-queue#r20 and #r24 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `review`, an answer that is `--accept`, a question that is "
     "`research`, a work-item that is `awaiting-answer`, r20 sets the status of a work-item to `drafted` and "
     "r24 to `done`"): Q_ONE,
    ("work-queue#r21 and #r22 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `implement`, a question that is `plan`, a work-item that is "
     "`awaiting-answer`, r21 sets the status of a work-item to `researched` and r22 to `ready`"): Q_ONE,
    ("work-queue#r21 and #r23 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `review`, an answer that is `--change`, a question that is "
     "`plan`, a work-item that is `awaiting-answer`, r21 sets the status of a work-item to `researched` and "
     "r23 to `ready`"): Q_ONE,
    ("work-queue#r21 and #r24 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `review`, an answer that is `--accept`, a question that is "
     "`plan`, a work-item that is `awaiting-answer`, r21 sets the status of a work-item to `researched` and "
     "r24 to `done`"): Q_ONE,
    ("work-queue#r22 and #r24 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `review`, an answer that is `--accept`, a question that is "
     "`implement`, a work-item that is `awaiting-answer`, r22 sets the status of a work-item to `ready` and "
     "r24 to `done`"): Q_ONE,
    ("work-queue#r23 and #r24 clash: on \"the person runs `work answer` on a work-item that is "
     "`awaiting-answer`\" with a question that is `review`, an answer that is `--accept`, a question that is "
     "`review`, an answer that is `--change`, a work-item that is `awaiting-answer`, r23 sets the status of a "
     "work-item to `ready` and r24 to `done`"): Q_ONE,
}


@pytest.fixture(scope="session")
def live_logic():
    import spec_solve
    toolchain.require()
    return spec_solve.run(REPO)


@pytest.fixture(scope="session")
def live_expected():
    """`EXPECTED`, for a test module, which cannot import this conftest by name."""
    return EXPECTED
