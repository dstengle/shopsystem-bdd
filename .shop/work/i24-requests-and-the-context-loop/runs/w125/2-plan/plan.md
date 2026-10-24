# Plan of w125 (supervision r56, r64, r65)

## 1. What goes green

- supervision#r56: scenario "refused ..." (`tests/scenarios/test_supervision.py`).
- supervision#r64: scenario "deselects ...".
- supervision#r65: scenario "left with no test ...".

None of the three is red today: the notes ran them (`3 passed` serial, and with `-n auto`). They stay green. What the work-item adds is the case the scenarios do not reach: r65 under xdist. A `--work-item` run for a guarantees-only work-item that is left with no test exits 5 under `-n 2` (notes, part 6 D1, probes 2 and 9). The cause is that the exit-0 decision reads a stash set in `pytest_collection_modifyitems`, and the xdist controller never runs that hook. So `work run`'s merge check (`-n auto`, `scripts/supervise_merge.py`) refuses such a work-item. The new test in part 4 is red today for that reason.

No deprecated scenarios are retired (the work-item has no Retires section).

## 2. Where the change lands

- `scripts/work_items.py`: `pytest_sessionfinish` decides "every accepted requirement is of a guarantees capability" from the `--work-item` option, through the existing `accepted` and `guarantees` functions, not from the stash. It does so on the controller and on each worker. The `GUARANTEES` stash key, and the place in `pytest_collection_modifyitems` that sets it, are removed. Deselection and the r56 refusal in collection stay as they are.
- `tests/scripts/test_work_items.py`: one new test. It runs pytest with `-n 2 --work-item w1` on a guarantees-only consumer, built like the one in the existing test `test_a_guarantees_work_item_has_its_scenarios_deselected_and_exits_successfully`, and asserts exit 0.

This is the researcher's set, unchanged. These files are read but not edited, and must keep passing: `scripts/supervise_merge.py`, `conftest.py`, `pytest.ini`, `tests/scenarios/test_supervision.py` and `tests/scenarios/supervision_tests_steps.py`. Both edited files have room under the 300-line limit (131 and 127 lines).

## 3. Decisions

- **D-a: r65 is decided at session end from the work-item and the spec alone, in every process.** No state is carried over from collection. Rests on supervision#r65 ("the command shall exit successfully") and on the work-item's own text, which asks for exactly this. It also rests on design-decision/workflow-capabilities-are-guarantees, which gives "guarantees" as `group: guarantees` in the capability's frontmatter; the capability's notes say the same for r56, r64 and r65.
- **D-b: session end changes only an exit of "no tests collected" (5), and changes it to success, only when the option is given and every accepted requirement's capability is guarantees.** Any other exit is left alone. In particular, the exit-3 refusals raised in collection (no such work-item; r56's "accepts none") are not re-raised or re-read at session end, so nothing is refused twice (notes, part 5). Rests on supervision#r65 and supervision#r56, and on design-decision/exits-are-successful-or-errors.
- **D-c: a mixed work-item that is left with no test still exits 5** (notes, case 11). r65 covers only work-items whose every requirement is of a guarantees capability. Rests on supervision#r65.
- **D-d: an accepted capability with no capability file counts as not guarantees** (today's behaviour of `guarantees`, case 6). It stays that way. Rests on design-decision/workflow-capabilities-are-guarantees: the frontmatter is the only source.

## 4. Tests the decisions break

None. Checked against the notes' part 4, which was found by search because `tools` has no map:
- `tests/scripts/test_work_items.py` tests at lines 62, 67, 79, 93, 100 and 108 test the refusals, the deselection and the serial exit 0. They keep passing, because D-a gives the same answer serially as the stash did.
- The r56, r64 and r65 scenario nodes check only exit codes and output that D-a and D-b leave unchanged.
- No test asserts exit 5, and no test reads the `GUARANTEES` key (the notes ran `tools refs GUARANTEES` and found 0 test references).

New test, red today: under `-n 2`, a guarantees-only work-item with no test left exits 0. The model is the notes' probe 2 (scenarios present, all deselected). The notes' probe 9 (the repository holds no test at all) may be added as a second case, at the implementer's choice.

## 5. Open cases

- What the merge check does end to end for a guarantees-only work-item under `-n auto`. The notes did not run it, and no test in the set drives `supervise_merge`. The implementer names whether the new unit test is enough evidence.
- Under xdist, a refusal at collection shows on the controller as INTERNALERROR exit 3, and the worker's message may not be shown (notes, cases 12 and 14). The scenarios do not cover this. Leave it unchanged, and name it if it gets in the way.
- How the new test gets `-n 2`: xdist is present here, because `pytest.ini` sets `-n auto`. The implementer names whether the test needs a guard for when xdist is missing.
