---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-2-implementation
kind: report
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
---

# Plan 2 of the workflow simplification: implementation report

This is the report of the one implementer agent that executed `plan-2-backlog.md` on 2026-11-04. It used
superpowers:executing-plans, with one commit per task.

All 5 tasks are done. The `backlog` capability is built: all 17 of its requirements are out of `unbuilt:`, and each
one's scenario passes. The commits are on `workflow-simplification`, from `391612df` to this report's commit. They are
not pushed. No baseline got worse.

## Final state

| Check | Result |
|---|---|
| Suite (`python3 -m pytest -q`) | 1059 passed, 1 skipped, 37 xfailed, 129 subtests passed. The start was 951 passed, 1 skipped, 54 xfailed. The 108 new passes are the 17 backlog scenarios and 91 new script tests. In one full run the known flake `test_model_logic_on_the_live_spec_is_fast` failed under xdist; run alone, it passed. |
| `model check` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems (at its baseline) |
| `model logic` | `11 findings: 6 L5, 5 L6` (at its baseline) |
| `model lexicon --check` | 401 terms, 0 problems |
| `features generate --check` | exit 0. `features/backlog.feature` was not touched. |
| `features vocab --check` | `every step has one handler` |
| `features bindings --unbound` | `every binding names a scenario` |
| `tools size --limit 300` | silent |
| `tools check` over the branch's Python files | ruff, vulture and import-linter are clean, except for `scripts/work`'s RUF100 "unused noqa E402", which was already there at `391612df` (see Deviations) |
| Unbuilt ids | `backlog` is not in `spec_unbuilt.unbuilt()`. 48 ids remain unbuilt, with no problems (see Deviations). |
| Smoke run (Task 5, Step 3) | Two tables, `shaped` then `idea`. b1 scores `5.00`. b2's row reads `blocked by b1 "Parse the item lines" (shaped)` and keeps 10 unescaped `\|`. The log has 6 commits. |

## Commits

| Task | Commit | What was done | Verification |
|---|---|---|---|
| 1 | `bfc07c3c` | Created `backlog_items.py`: the item file, parse and render, the label, numbering and commit. Created `backlog_moves.idea` and `backlog_cli.py`, and wired `scripts/work` (`work idea`, and `work show b<n>`). Added the scenario world `backlog_world.py`, the handlers in `backlog_handlers.py`, and `test_backlog.py` binding with `bind_all`. Added the fixture `backlog_repo` and the helper module `tests/scripts/backlog_testing.py`. r1 and r15 are built. | The script tests failed first (no module), then 23 passed with the show and list tests. Backlog scenarios: 2 passed, 15 xfailed. Suite: 971 passed, 52 xfailed. |
| 2 | `e5aa5231` | Added `TRANSITIONS` and `move`, plus `shape`, `refuse`, `withdraw` and `answer`, with their parsers. `work withdraw` and `work answer` route an item `b<n>` to the backlog, and a reviewer's flag on an item is refused. r2, r3, r9-r14 and r16 are built. | `test_backlog_moves.py` failed first, then 46 passed. The old work-queue and requests scenarios pass. Backlog scenarios: 11 passed, 6 xfailed. Suite: 1025 passed, 43 xfailed, with one flake, rerun alone and passing. |
| 3 | `a5bfe3cb` | Added `rate`, `depend` and `cycle`, with their parsers. r4 and r5 are built. | `test_backlog_ratings.py` failed first, then passed. Backlog scenarios: 13 passed, 4 xfailed. Suite: 1041 passed, 41 xfailed. |
| 4 | `e1f04d2e` | Created `backlog_view.py`: score, rank, blockers, tables and JSON. Added `work backlog`, and `work show --json` now uses `row_json`. Added the handlers for r6-r8 and r17. In `backlog.md`, set `unbuilt: []`, added `## Implementation, may change` and rewrote `## Not yet`. | `test_backlog_view.py` failed first, then 32 passed. Backlog scenarios: 17 passed. Suite: 1059 passed, 37 xfailed. `model logic`: 11 findings. |
| 5 | this report | Ran the whole-plan verification and the smoke run, and wrote this report and its row in `.shop/records/README.md`. | See Final state. |

## Deviations from the plan

### Branch
- **D1 overridden.** The main session ruled that every plan goes on `workflow-simplification`. There is no branch
  `plan-2-backlog`, and D1's row in the plan says so. The end-of-branch review should read `391612df..HEAD`, not
  `workflow-simplification..plan-2-backlog`.

### Plan figures
- **Task 5, Step 1 expects `False 37 []`.** It measured `False 48 []`. The plan treated the count of unbuilt ids as if
  it were the count of xfailed scenarios. Of the 48 ids, 11 belong to `brainstorming` (3) and `pr-review` (8), which
  have no feature file and so no scenarios. 48 − 11 = 37 xfailed scenarios, as the plan expected for the suite.

### Vacuous XPASSes and handler fixes
Each of these was found by the suite and fixed so that the scenario tests its point.
- **readiness#r3 passed vacuously in Task 1.** Once items had Givens, its registry `ThenExitsErr` named nothing about
  the item, so the scenario passed against a `work ready` that does not exist. The fix: `backlog_world.write_item`
  records each item's label in `context["says"]`. Any registry Then about an item must then name its label (goal 10),
  and readiness#r3 stays an expected failure until plan 3 builds it.
- **batches#r3 passed vacuously in Task 4.** `the item i1 is not `in-batch`` held after a `work batch start` that is
  not a command. The fix: a negated `ThenK_A` on an item now requires that the last run exited 0.
- **`ThenExitsErr` on an item was added in Task 1, not Task 2.** Without it, backlog#r3 passed vacuously against the
  argparse error before `work shape` existed.
- **The `question` locals return False outside a scenario that keeps items.** Without that, supervision's questions on
  work-items failed through them.

### Format choices
- **`work show --json` in Task 1** gave the item's own keys (`backlog_items.as_dict`). Task 4 switched it to
  `row_json`, which adds `score`, `rank` and `blocked_by`.
- **`blocked_by` in the JSON** is `[{"id", "status"}]`. The plan named the key but not its shape.
- **An answer to a `needs-input` item with no `## Question`** is written as `- A: <text>` alone, because D17 assumes
  there is a question.
- **A note, reason or answer that starts with `#` is refused**, because it would read as a heading and make the file
  malformed (D16).

### Tests and code style
- **The hand-written cycle test.** pytest-timeout is not installed, so the test bounds `work` with a 60 s subprocess
  timeout in `backlog_testing.work`.
- **The test helpers** are in `tests/scripts/backlog_testing.py`, which four test files share. The existing
  `tests/scripts/` row of the module map covers it, so it has no row of its own.
- **`scripts/work`'s RUF100.** Every import already carried an unused `# noqa: E402` before this plan. The two new
  imports follow the file's convention. The file grew from 192 to 202 lines, within the limit of 25.

## D1-D18

| # | Kept or changed |
|---|---|
| D1 | Changed: built on `workflow-simplification`, by the main session's ruling. |
| D2 | Kept. The file format is as pinned, an unrated field is written empty, and `parse(render(i))` round-trips. |
| D3 | Kept. Each move is one commit of one path, and there is no log file. |
| D4 | Kept. A new item is `b<highest + 1>` by the files' names. |
| D5 | Kept, all of the commands. `work answer` on an item refuses `--change` and `--accept`. |
| D6 | Kept. A value outside the glossary's is refused with exit 1, naming the values allowed. |
| D7 | Kept. |
| D8 | Kept. |
| D9 | Kept. A missing item is printed `missing`, and an item that is withdrawn or refused still blocks, with its status. |
| D10 | Kept: risk and likelihood are in `## Not yet`. |
| D11 | Kept: `## Not yet` names plan 4. |
| D12 | Kept: the rank order and the tables by state are prose under `## Implementation, may change` and pinned by script tests. |
| D13 | Kept: `spec_steps` is unchanged. |
| D14 | Kept: the scenario's `i<n>` is the file `b<n>`. |
| D15 | Kept. The world's own items for a dependency are `i90` and `i91`, titled `an item the scenario does not name`. |
| D16 | Kept. A malformed file is refused naming the file and the field (`status`, `provenance`, `value`, `urgency`, `size`, `title`, `depends_on` or `id`), by every command that reads it. |
| D17 | Kept, with the `- A:` form for a missing question (see Deviations). |
| D18 | Kept. Empty or multi-line text is refused, and so is a title, note, reason or answer that is not one line. |

## Open problems for plan 3 and later

- **The end-of-branch review has not run.** The plan gives it to a separate reviewer, writing `plan-2-review.md` and
  reading `391612df..HEAD` against the plan's Review Focus.
- **Registry Thens about an item must name its label.** readiness and batches inherit the backlog's item Givens, and
  their registry `ThenExitsErr` and `ThenPrints` with `` `work` `` now need the item's label in the output. Plans 3
  and 4 should give their item steps `local` handlers, as the backlog's are, binding with `bind_all`.
- **The rule for negated item Thens.** `ThenK_A` on an item, negated, requires a successful last run. If plan 4 writes
  a line whose negated Then follows a refusal, it needs another way to check it.
- **Two branches can add the same `b<n>`** (D4). Nothing prevents that collision, and it surfaces as a git conflict.
- **No command removes a dependency** (D5). It has to be edited in the file by hand.
- **The `blocked` exception for an item in the same batch** waits for plan 4.

## Files

- Created:
  - `scripts/backlog_items.py`, `scripts/backlog_moves.py`, `scripts/backlog_cli.py`, `scripts/backlog_view.py`
  - `tests/scenarios/backlog_world.py`, `tests/scenarios/backlog_handlers.py`
  - `tests/scripts/backlog_testing.py`, `tests/scripts/test_backlog_items.py`, `tests/scripts/test_backlog_moves.py`,
    `tests/scripts/test_backlog_ratings.py`, `tests/scripts/test_backlog_view.py`
  - this report
- Modified:
  - `scripts/work`, `tests/scenarios/test_backlog.py`, `tests/scripts/conftest.py`
  - `spec/capabilities/backlog.md`: `unbuilt:`, `## Implementation, may change` and `## Not yet` only
  - `CLAUDE.md`: four module rows, and `backlog` added to two rows
  - `.shop/records/README.md`, `plan-2-backlog.md`: every box ticked, and D1's row
