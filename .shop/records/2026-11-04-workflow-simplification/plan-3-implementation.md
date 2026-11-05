# Plan 3 of the workflow simplification: implementation report

This is the report of the one implementer agent that executed `plan-3-readiness-intake.md` on 2026-11-04 and
2026-11-05. It used superpowers:executing-plans, with one commit per task.

All 6 tasks are done. The `readiness` and `intake` capabilities are built: all 4 of readiness's and all 6 of intake's
requirements are out of `unbuilt:`, and each one's scenario passes. `brainstorming` r1 and r2 are met by the skill
`shaping-items` and its test; r3 stays unbuilt (D15). The commits are on `workflow-simplification`, from `3fab8af5`
to this report's commit. They are not pushed. No baseline got worse.

## Final state

| Check | Result |
|---|---|
| Suite (`python3 -m pytest -q`) | 1143 passed, 1 skipped, 27 xfailed, 131 subtests passed. The start was 1067 passed, 37 xfailed, 129 subtests. The 76 new passes are the 10 readiness and intake scenarios, 59 new script tests, and 7 new rows of `test_a_move_from_another_status_is_refused_naming_it` (`work ready` from each status but `shaped`). The 2 new subtests are `test_agents.py`'s formulator check over the two new skills. In 6 of the 10 full runs this session, the known flake `test_model_logic_on_the_live_spec_is_fast` failed under xdist. It passed each time it was run alone, and the final run had no failure. |
| Unbuilt ids | `False False ['r3'] 36 []`: readiness and intake are not in `spec_unbuilt.unbuilt()`, brainstorming keeps r3, 36 ids remain, and there are no problems. |
| `model check` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems (at its baseline) |
| `model logic` | `11 findings: 6 L5, 5 L6` (at its baseline) |
| `model lexicon --check` | 401 terms, 0 problems |
| `features generate --check` | exit 0. No feature file was touched. |
| `features vocab --check` | `every step has one handler` |
| `features bindings --unbound` | `every binding names a scenario` |
| `tools size --limit 300` | silent. `scripts/work` is at 211 lines (limit 222), `workqueue_request.py` is unchanged at 252, and `backlog_handlers.py` is at 261. |
| `tools check` over the branch's Python files and `scripts/work` | ruff, vulture and import-linter are clean |
| Smoke run (Task 6, Step 3, in bash) | Printed `b1 "Abandon a started initiative" ready`. `work ready` took **0.13 s** with a warm cache, and 0.32 s with an empty `XDG_CACHE_HOME`. The first `W ready b2` was refused naming `line 1 of request q1 is unanswered` and `work line`. After `outcome … accepted --into work-queue` and `turn`, the second readied b2. `work backlog`'s `ready (2)` table holds b1 (`own`) and b2 (`peer`). `status --porcelain` is empty, and `spec/` shows no diff since the root commit. |

## Commits

| Task | Commit | What was done | Verification |
|---|---|---|---|
| 1 | `0b793937` | Created `backlog_lines.py`. It reads and renders the `## Requirements` blocks, gives the next ids (D3), and has `add_line`, `add_line_to`, `add_term` and `lay`. Added the `work line` parser and `cmd_line`, the `ready_repo` fixture, and a module-map row. | `test_backlog_lines.py` failed first (no module), then 10 passed. Backlog tests: 80 passed. Suite: 1077 passed, 37 xfailed, with the flake rerun alone and passing. |
| 2 | `5064a694` | Created `readiness_bar.py` (`request_lines`, `unsettled`, `well_formed`, `check`). Added `backlog_moves.ready` with `work ready` in `TRANSITIONS`, and `cmd_ready`, which prints warnings on stderr. `backlog_world` gained `sections`, `request` and run kwargs. Created `readiness_world.py` and `readiness_handlers.py`, and `test_readiness.py` now binds with `bind_all`. `readiness.md` has `unbuilt: []` and the two prose sections. | `test_readiness_bar.py` failed first, then 14 passed. With the `ready` command removed, the 4 scenarios xfailed. With it, they passed. Mutation: when `cmd_ready` printed `Ready it anyway?`, r4 failed, and the mutation was reverted. Suite: 1102 passed, 33 xfailed. |
| 3 | `2aa654f8` | `Item` gained `request` and `asked_by`, rendered only when set. Created `intake_moves.py` (`provenance_of`, `linked`, `intake`) and the `work intake` parser. `OF_GIVENS` moved to `backlog_world` (D18). Added `link_request` to `readiness_world`, created `intake_handlers.py`, and `test_intake.py` now binds with `bind_all`. Added `write_request` and `request_text` to `backlog_testing`. intake has `unbuilt: [r2, r3, r4]`. | `test_intake_moves.py` failed first, then 19 passed. With `intake` removed and `unsettled` left out of `check`, the scenarios r1, r5 and r6 xfailed. With them, they passed. Suite: 1124 passed, 30 xfailed. |
| 4 | `f29691d8` | Added `intake_moves.handles` and `outcome` (D12). The `outcome` parser of `scripts/work` gained `--into`, `--group`, `--reason` and `--line`. `model_requests.SECTIONS` gained `Reasons`. Added the handlers for r2-r4. intake has `unbuilt: []` and the two prose sections. | `test_intake_outcome.py` failed first (`test_old_outcome_is_unchanged` passed already, as it should). Then 10 passed. With `handles` disabled, r2-r4 failed on their points (the item not committed, the reason not written, no line written). With it enabled, all 6 intake scenarios passed. Suite: 1136 passed, 27 xfailed, with the flake rerun alone and passing. |
| 5 | `e3012666` | Created `skills/shaping-items/SKILL.md`, `skills/taking-in-a-request/SKILL.md` and `tests/scripts/test_skill_shaping_items.py`. brainstorming has `unbuilt: [r3]` and a `## Not yet`. README's skills list gained the two skills. | The test failed first (no skills), then 6 passed, along with `test_agents.py`. Mutation: a Process step 5 that read "Wait for the person to approve" failed r2, and was reverted. `model check` is at its baseline. |
| 6 | this report | Ran the whole-plan verification and the smoke run, wrote this report and its row in `.shop/records/README.md`, and ticked every box of the plan. | See Final state. |

## Deviations from the plan

Every deviation is a ruling, decided by the implementer; revisit.

### Tests the plan's text did not fit
- **`test_backlog_moves.py` was changed by one line.** `test_each_move_follows_its_row` is parametrised over
  `TRANSITIONS`, so the new `work ready` row ran on an item with no lines and failed, by D7. That one row is left out
  there, with a comment; `test_ready_readies_a_passing_item` tests the move. The rest of the file is unchanged, and
  the 7 refusal rows `work ready` adds pass.
- **The fixture's `DONE` statement gives an L1 as well as an L3.** It clashes with `work-queue#r1` on the same
  trigger. `test_an_l3_is_a_warning` therefore uses a statement that gives an L3 alone: `work abandon` on a `proposed`
  initiative, which no transition allows. `DONE` is kept as `test_an_l1_naming_the_items_line_refuses`.
- **`work turn` is run once, not twice, in `test_the_rewritten_line_is_not_the_items`.** A counter-proposal already
  passes the turn to the asker, so one `work turn` (the asker's) brings it back to the upstream. A second would put
  it in the asker's turn again, and the outcome would be refused.
- **`as_dict` gives `request` and `asked_by` only for an item taken in from a request.**
  `test_backlog_view.py::test_json_is_one_object_in_table_order` pins every row's keys and has to pass unchanged.

### Interfaces
- **`work line`'s parser** is a small `argparse.ArgumentParser` subclass (`_LineParser`). On Python 3.11, argparse
  gives the optional positional TEXT nothing at `b1`, and then finds TEXT left over after `--into CAP`. The subclass
  takes one leftover non-option word as TEXT. `TEXT` and `--term` are checked as exactly one in `cmd_line`.
- **The dest of `--line` is `text`,** because the positional `line` is the line's number. `handles(args)` reads
  `into`, `group`, `reason` and `text`. `test_old_outcome_is_unchanged` caught the first version, which read the
  number.
- **The rewritten outcome sets `awaiting-asker` and `turn: asker` itself** and does not call `work turn`'s edit. That
  edit is a closure inside `workqueue_request.turn`, and the file may not change. A rewritten line is never settled,
  so `turn` from the upstream always takes this branch (requests r17). The rule is now written in two places.
- **The bar runs `spec_solve.run(copy)` once,** over the whole copy, and keeps each L0 and each L1 or L3 that names
  one of the item's ids. It does not run once per capability. The solve covers the whole context either way.
- **The scenario handlers:**
  - `ThenK_A` for `request line` is a registry handler, not a `local`. No capability claimed it, and `features vocab
    --check` reads only the registry.
  - `local("ThenExitsErr", "reason")` returns False when no readiness Given kept a reason. Without that, supervision's
    `work run … naming the reason r1` failed through it.
- **The counter-proposal** in the scenarios and the script tests is the fixture's `ABANDON`. The script tests' asked
  line is a `proposed` initiative abandoned, which the counter-proposal fixes.

### Files outside the plan's lists
- **The skill names the quote command in words:** "until `work` keeps quotes (brainstorming r3)". A backticked
  `` `work quote` `` would fail `test_the_skills_name_only_commands_work_has`. The test reads a command as
  `` `work <sub> `` or `/work <sub>`, since the skills write `python3 <scripts>/work …`.
- **README's skills list** gained `shaping-items` and `taking-in-a-request`.
- **`test_intake_moves.py` has three tests the plan did not name:** `test_intake_refuses_a_request_there_is_not`,
  `test_request_fields_round_trip_and_a_bad_request_is_refused` and `test_json_names_the_request_of_an_item_taken_in`.
  **`test_intake_outcome.py` has one:** `test_line_only_with_rewritten_and_into_only_with_accepted`.

## The planner's decisions, D1-D19

| # | Kept or changed |
|---|---|
| D1 | Kept: built on `workflow-simplification`. |
| D2 | Kept: the `## Requirements` block, in exactly the plan's shape. |
| D3 | Kept. Retired ids count. Two items given the same id are left for plan 4. |
| D4 | Kept. `work line` refuses a capability with no file and an uncodified one, naming it. Glossary terms and new capabilities are in readiness's `## Not yet`. |
| D5 | Kept. `--group` and `--in` are mutually exclusive. It takes an item that is `idea` or `shaped`. |
| D6 | Kept. An L3 naming the item is printed as `work ready: warning: L3 …`. |
| D7 | Kept. The reason reads `it has no requirement line: give it one with \`work line\``. |
| D8 | Kept. The status is refused first, by the move's own message, with no check run. |
| D9 | Kept. The reason for a group with no step words is read from `features generate`'s own warning. A logic-only group is not a reason. |
| D10 | Kept. Refusals come in this order: no such request, already taken in (naming the item), out of turn (naming the status). |
| D11 | Kept. |
| D12 | Kept, with the refusals in the Interfaces list. A reason given with `rewritten --line` replaces the default `rewritten as line <m>`. |
| D13 | Kept. |
| D14 | Kept. intake's `## Not yet` names the session `work backlog` starts, for plan 4. |
| D15 | Kept. |
| D16 | Kept: `NO_INPUT` and the `ThenDoesNot ask` handler. A question is a `## Question` gained, a `## Questions` entry added, a move to `needs-input` or `awaiting-asker`, or an output line ending in `?`. |
| D17 | Kept. |
| D18 | Kept. `backlog_world.OF_GIVENS` starts empty; the backlog adds `dependency` and intake adds `request line`. |
| D19 | Kept. |

## Open problems for plan 4 and later

- **The end-of-branch review has not run.** The plan gives it to a separate reviewer, writing `plan-3-review.md` and
  reading `3fab8af5..HEAD` against the plan's Review Focus.
- **No command removes or rewords an item's line.** `work line` only adds. A line the bar refuses is fixed by editing
  the item's `## Requirements` by hand, or by withdrawing the item. The shaping-items skill says to reword, but no
  command does it yet.
- **Two items can take the same `<cap>#r<n>`** (D3). Plan 4's batch check must catch the duplicate and renumber.
- **A taken-in request's plain `work outcome q<n> <k> accepted`** (without `--into`) is now refused, as D12 says. A
  session used to the old command meets this refusal, which names `--into`.
- **The rewritten outcome's turn rule is written twice** (`intake_moves.outcome` and `workqueue_request.turn`). If
  requests r17 changes, both must change.
- **The bar's time on the live spec has not been measured.** On the fixture it is under a second. On this
  repository's spec, `model logic` takes several seconds, and `test_model_logic_on_the_live_spec_is_fast` measures it.
- **The flake failed in 6 of the 10 full runs this session.** That is more often than the 1 in 3 noted before.

## Files

- Created:
  - `scripts/backlog_lines.py`, `scripts/readiness_bar.py`, `scripts/intake_moves.py`
  - `tests/scenarios/readiness_world.py`, `tests/scenarios/readiness_handlers.py`,
    `tests/scenarios/intake_handlers.py`
  - `tests/scripts/test_backlog_lines.py`, `tests/scripts/test_readiness_bar.py`,
    `tests/scripts/test_intake_moves.py`, `tests/scripts/test_intake_outcome.py`,
    `tests/scripts/test_skill_shaping_items.py`
  - `skills/shaping-items/SKILL.md`, `skills/taking-in-a-request/SKILL.md`
  - this report
- Modified:
  - `scripts/backlog_items.py`, `scripts/backlog_moves.py`, `scripts/backlog_cli.py`, `scripts/work`,
    `scripts/model_requests.py`
  - `tests/scenarios/backlog_world.py`, `tests/scenarios/backlog_handlers.py`, `tests/scenarios/test_readiness.py`,
    `tests/scenarios/test_intake.py`
  - `tests/scripts/conftest.py` (`ready_repo`), `tests/scripts/backlog_testing.py`,
    `tests/scripts/test_backlog_moves.py` (one line)
  - `spec/capabilities/readiness.md`, `intake.md` and `brainstorming.md`: only `unbuilt:`, `## Implementation, may
    change` and `## Not yet`
  - `CLAUDE.md`: three module rows, and `readiness` and `intake` added to the handlers and world rows
  - `README.md`: the skills list
  - `.shop/records/README.md`, and `plan-3-readiness-intake.md` with every box ticked
