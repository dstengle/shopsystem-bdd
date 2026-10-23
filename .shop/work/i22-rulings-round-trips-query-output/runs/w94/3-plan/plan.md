# Plan of w94: measure counts round trips

Accepts batch-measurement r41, r42, r53-r56. Planned from the research notes (`runs/w94/1-research/notes.md`), the
2-plan's plan, the capability, its rests_on decisions, `features/batch-measurement.feature`, and the person's answer
of 2026-10-23 (reading A) recorded in the work-item's `## Answers`.

Since the 2-plan, w91's rename has landed in this checkout: `workqueue.STATUSES`, `model_work`, `supervise*.py`
and `work answer` all say `awaiting-answer`, and `migrate_upgrade_answers.py` (migration-tools r29) renames old
logs. The only holdouts are `scripts/measure_build.py:76`, `scripts/measure_show.py` ITEMS and the `scripts/measure`
contract text.

## 1. What goes green

- **r41**, "each work-item is given with its transitions, its awaiting-answer and failed counts and the commits its
  merge brought in". Red: the Then "it gives cart-1 1 time to awaiting-answer and 1 time to failed" has no step (the
  step at then_steps:110 names awaiting-ruling) and `measure_build.work_items_of` counts only `awaiting-ruling`.
- **r42**, "the totals are over the stages' sessions, an unended stage included, and span the first transition to the
  last". Red: the Given "the stages' sessions took" unpacks 5 columns and the table has 7; the transcript Given has
  no "turns, round trips" form; the totals give no turns or round trips; the totals step does not assert them.
- **r53**, "each stage is given with its session's round trips". Red: no steps for the "... a start and an end, run
  in the session s-1" log Given, "the session s-1 took 14 turns", "the transcript of the session s-1 holds 40
  assistant messages with 31 distinct request ids"; no "round trips" key in the stage table's NUMBERS; `stages_of`
  gives no round trips and nothing reads Claude Code's store.
- **r55**, "a stage whose session has no transcript to be found is given without its round trips". Red: the same
  undefined Givens, plus no steps for "no transcript of the session s-1 can be found", "gives the stage with 14
  turns", "gives no round trips for the stage". The code already leaves the key out.
- **r54**, "show prints each stage's round trips beside its turns". Red: no "giving ... 14 turns and 31 round trips"
  Given, no "the printed stage of cart-1's research shows" step; `measure_show.STAGES` has no round trips column.
- **r56**, "show prints the stages of a measurement that gives no round trips without them". Red: no "giving no round
  trips" Given, no "the stages are printed" / "no round trips are printed" steps. The code already prints none.

Deprecated scenarios retired: "each work-item is given with its transitions, its awaiting-ruling and failed counts
and the commits its merge brought in (deprecated)" (@r41, feature line 83-84), per the person's answer (reading A).
It passes today and goes red once only awaiting-answer is counted. The deprecated r42 totals scenario is kept green
(D6).

## 2. Where the change lands

The researcher's set, plus the feature file for the retirement:

- `scripts/measure_read.py`: find a session's transcript in Claude Code's store by its id (D2), read it through the
  row checks `read_transcripts` already makes (D4), count its distinct request ids, the session's own rows only (D3).
- `scripts/measure_build.py`: each stage gets its session's round trips when its transcript is found (r53, r55);
  totals gain turns and round trips summed over the stages (r42, D5); the work-item count is of `awaiting-answer`
  transitions only, under an awaiting-answer key (D1).
- `scripts/measure_show.py`: a round trips column beside turns, printed only when the measurement's stages hold round
  trips (r54, r56); totals rows for turns and round trips (also in `compare`); the work-item table's header and key
  renamed to awaiting-answer (D1).
- `scripts/measure`: contract text names round trips, where the transcript is read from, and the awaiting-answer
  count. No new flag (D2).
- `features/batch-measurement.feature`: the deprecated r41 scenario removed with `features retire` (D1). Added by this
  plan: the retirement is the answer's.
- `tests/scenarios/batch_measurement_given_steps.py`: the "run in the session" log form, "took N turns", "no
  transcript ... can be found", the sessions table with or without turns and round trips, the transcript Given with
  turns and round trips.
- `tests/scenarios/batch_measurement_then_steps.py`: the awaiting-ruling step replaced by the awaiting-answer one;
  "round trips" in NUMBERS; "gives the stage with N turns"; "gives no round trips for the stage"; the totals step
  asserting every column its table gives.
- `tests/scenarios/batch_measurement_show_steps.py`: the "giving ... N turns and M round trips" and "giving no round
  trips" Givens; "the printed stage of ... shows"; "the stages are printed"; "no round trips are printed".
- `tests/scenarios/batch_measurement_world.py`: the test's Claude Code store, a scratch directory the world points
  measure at through the environment (D2), and writing a session's transcript into it.
- `tests/scenarios/batch_measurement_transcripts.py`: writing N assistant messages with M distinct request ids in
  Claude Code's row shape.

Not in the set: `scripts/measure_write.py` (writes figures as given); `scripts/workqueue.py`, `model_work.py`,
`supervise*.py` (already renamed by w91); `tests/scenarios/test_batch_measurement.py`. Every file has room under
the 300-line limit (notes, part 7).

## 3. Decisions

- **D1, measure counts `awaiting-answer` only; the deprecated r41 scenario is retired.** Taken by the person's answer
  of 2026-10-23 (reading A, in the work-item's `## Answers`), on r41. A log still holding `awaiting-ruling` gives 0;
  the r29 upgrade step (`migrate_upgrade_answers.py`) renames such logs. The work-item has no `## Retires` section;
  the answer names the retirement, and the planner writes no file but the plan, so the coordinator may want to
  record it there.
- **D2, where the store is.** A stage's transcript is the file named by its session id with the `.jsonl` suffix under
  any project directory of the store's `projects` directory; the store is the directory `CLAUDE_CONFIG_DIR` names,
  else `.claude` in the home directory. Any project directory, because a stage runs in its own worktree and its
  project directory is named after that path. Tests set the variable to a scratch directory in the world. Read
  whether or not `--sessions` is given; `--sessions` stays the source of r43 only. Rests on the Implementation note
  "r53: a stage's session's transcript is read from Claude Code's own store by the session's id" and r55 (not
  found: given without round trips, no refusal).
- **D3, subagent rows are not the stage's round trips.** A row a subagent wrote (agent id set, a sidechain row, or a
  subagent's own file) does not count toward its dispatching session's round trips. Rests on r53 ("the session's
  transcript") and the Implementation note that round trips are the unit `--max-turns` limits, the session's own
  turns; it matches `read_transcripts` making a subagent its own session.
- **D4, a store transcript is checked as a `--sessions` one is.** An unknown row shape is refused naming the file and
  line, writing nothing (r47, r50, design-decision/measure-refuses-unknown-shapes); the lookup reuses those checks.
- **D5, totals.** The turns total is the stages' turns summed, the round trips total the stages' round trips summed;
  sessions found only by `--sessions` are left out (r42 and its Implementation note), so the s-9 transcript's
  20 turns and 45 round trips never enter the totals (14+6=20, 31+12=43).
- **D6, the deprecated r42 scenario is kept green.** Its sessions table has 5 columns, the new one 7; the step takes
  both (turns and round trips written only when the table gives them) and the totals step asserts the columns its
  table gives. Test-only; rests on r42, which both scenarios carry, and on the work-item retiring only the r41 one.

## 4. Tests the decisions break

- Deprecated r41 scenario (`..._awaitingruling_..._deprecated`) in `features/batch-measurement.feature`: D1 makes it
  red; removed with `features retire`, as the person's answer rules.
- `then_steps` awaiting-ruling step (line 110): used only by that scenario; rewritten to assert the awaiting-answer
  count and failed count (D1), which the current r41 scenario uses. The commit steps the two scenarios share stay.
- `given_steps` "the stages' sessions took" (line 108): rewritten to take the 5- or 7-column table (D6).
- `then_steps` "gives the totals" (127-135): rewritten to assert each column its table names, turns and round trips
  included (D5), so the new r42 scenario's 20 and 43 are checked; the deprecated one still asserts its columns.
- r44 show and r45 compare steps (show_steps 53-60, 63-68): per the notes they assert headers and listed rows only
  and stay green with a round trips column and new totals rows; if the r44 one names the awaiting_ruling header it
  follows D1's rename. r40, r43, r46-r52 steps: per the notes, named fields or refusals; they stay green. No
  supervision or work-queue test is touched.

## 5. Open cases (for the implementer to name, not choose)

- A session id found in more than one project directory of the store.
- A stage with a transcript in the store but no `session.json` (turns absent, round trips present).
- The round trips total when some stages have round trips and some do not, and when none do (0 or left out).
- `show` and `compare` on a measurement written before this change: no turns or round trips totals, and a work-item
  key under the old awaiting_ruling name.
- The s-9 transcript Given's "20 turns": a transcript has no turn count; what the step writes for it.
- The notes' defect D1: `--sessions` naming a missing directory exits 0 silently; not in this work-item.
