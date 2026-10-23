# Plan of w94: measure counts round trips

Accepts batch-measurement r41, r42, r53-r56. The work-item has no Retires section and no Rulings. Planned from the
research notes (`runs/w94/1-research/notes.md`), the capability, decisions 0018, 0060 and 0064, and
`features/batch-measurement.feature`.

## 1. What goes green

- **r41**, "each work-item is given with its transitions, its awaiting-answer and failed counts and the commits its
  merge brought in". Red: the Then "it gives cart-1 1 time to awaiting-answer and 1 time to failed" has no step
  (the existing step names awaiting-ruling), and `measure_build.work_items_of` counts only `awaiting-ruling`.
  The deprecated r41 scenario ("... awaiting-ruling and failed counts ... (deprecated)") passes today; what becomes
  of it is the open question (part 3, D1).
- **r42**, "the totals are over the stages' sessions, an unended stage included, and span the first transition to
  the last". Red: the Given "the stages' sessions took" unpacks 5 columns and the table has 7; the transcript Given
  has no "turns, round trips" form; the totals have no turns or round trips; the totals step does not assert them.
  The deprecated r42 scenario passes today and is kept green (part 3, D7).
- **r53**, "each stage is given with its session's round trips". Red: no step for "i7-cart's log.jsonl gives ...
  a start and an end, run in the session s-1", "the session s-1 took 14 turns", "the transcript of the session s-1
  holds 40 assistant messages with 31 distinct request ids"; no "round trips" key in the stage table's NUMBERS;
  `stages_of` gives no round trips and nothing reads Claude Code's store.
- **r55**, "a stage whose session has no transcript to be found is given without its round trips". Red: the same
  undefined Givens, and no steps for "no transcript of the session s-1 can be found", "gives the stage with 14
  turns", "gives no round trips for the stage". The code already leaves the key out.
- **r54**, "show prints each stage's round trips beside its turns". Red: no "giving ... 14 turns and 31 round trips"
  Given, no "the printed stage of cart-1's research shows" step; `measure_show.STAGES` has no round trips column.
- **r56**, "show prints the stages of a measurement that gives no round trips without them". Red: no "giving no
  round trips" Given, no "the stages are printed" / "no round trips are printed" steps. The code already prints
  without round trips (it prints no such column at all today).

Deprecated scenarios retired: none named by the work-item; the r41 one hangs on question D1.

## 2. Where the change lands

The researcher's set, unchanged:

- `scripts/measure_read.py`: find a session's transcript in Claude Code's store by its id (D2), read it through the
  same row checks `read_transcripts` makes (refusing unknown shapes), and count its distinct request ids, the
  session's own rows only (D3).
- `scripts/measure_build.py`: each stage gets its session's round trips when its transcript is found (r53, r55);
  totals gain turns and round trips summed over the stages (r42); the awaiting count per D1.
- `scripts/measure_show.py`: a round trips column beside turns, printed only when the measurement's stages hold
  round trips (r54, r56); totals rows for turns and round trips; the work-item table's awaiting header and key per D1.
- `scripts/measure`: the contract text names round trips, where the transcript is read from, and the awaiting-answer
  count. No new flag (D2).
- `tests/scenarios/batch_measurement_given_steps.py`: the "i7-cart's log.jsonl gives ... run in the session" form,
  "took N turns", "no transcript ... can be found", the sessions table with or without turns and round trips, the
  transcript Given with turns and round trips.
- `tests/scenarios/batch_measurement_then_steps.py`: the awaiting-answer step; "round trips" in NUMBERS; "gives the
  stage with N turns"; "gives no round trips for the stage"; the totals step asserting every column its table gives.
- `tests/scenarios/batch_measurement_show_steps.py`: the "giving ... N turns and M round trips" and "giving no round
  trips" Givens; "the printed stage of ... shows"; "the stages are printed"; "no round trips are printed".
- `tests/scenarios/batch_measurement_world.py`: the test's Claude Code store, a scratch directory the world points
  measure at through the environment (D2), and writing a session's transcript into it.
- `tests/scenarios/batch_measurement_transcripts.py`: writing N assistant messages with M distinct request ids in
  Claude Code's row shape.

Not in the set: `scripts/measure_write.py` (writes the figures as given, unchanged); `scripts/workqueue.py`,
`scripts/model_work.py`, `scripts/supervise*.py` (the status rename, D4); `tests/scenarios/test_batch_measurement.py`.
All files have room under the 300-line limit (notes, part 7).

## 3. Decisions

- **D1, the awaiting count: QUESTION.** r41 says "to `awaiting-answer`"; every log written so far, this
  initiative's included, says `awaiting-ruling`, and the deprecated r41 scenario expects "1 time to awaiting-ruling".
  Decision 0064 (proposed, not in the capability's rests_on) says the status is renamed and an upgrade step renames
  logs. Which count measure gives changes what the narrator sees and nothing accepted settles it; asked in the result.
- **D2, where the store is.** A stage's transcript is the file named by its session id with the `.jsonl` suffix
  under any project directory of Claude Code's store's `projects` directory; the store is the directory
  `CLAUDE_CONFIG_DIR` names, else `.claude` in the home directory. Any project directory, because a stage runs in its
  own worktree and its project directory is named after that path. Tests set the variable to a scratch directory in
  the world. Rests on the Implementation note "r53: a stage's session's transcript is read from Claude Code's own
  store by the session's id" and r55 (not found: no round trips, no refusal). The store is read whether or not
  `--sessions` is given; `--sessions` stays the source of r43 only.
- **D3, subagent rows are not the stage's round trips.** A row a subagent wrote (agent id set, or a sidechain row,
  or a subagent's own file) does not count in its dispatching session's round trips. Rests on r53 ("the session's
  transcript") and the Implementation note that round trips are the unit `--max-turns` limits, which is the
  session's own turns; it matches how `read_transcripts` already makes a subagent its own session.
- **D4, the status rename is out of scope.** Renaming `awaiting-ruling` in `workqueue`, `model_work` and `supervise`
  is w91's (work-queue r9, r13, r14, "work answer, and the status awaiting-answer") and decision 0064's upgrade step;
  w94 does not touch them.
- **D5, a transcript in the store is checked as one in `--sessions` is.** An unknown row shape is refused naming
  the file and line, writing nothing (r47, decision 0018); the store lookup reuses those checks, not a looser count.
- **D6, totals.** Turns total is the stages' turns summed; round trips total is the stages' round trips summed;
  sessions found only by `--sessions` are left out (r42 and its Implementation note), so the s-9 transcript's
  20 turns and 45 round trips never enter the totals (14+6=20, 31+12=43).
- **D7, the deprecated r42 scenario is kept green.** Its sessions table has 5 columns, the new one 7; the step
  accepts both (turns and round trips written only when the table gives them) and the totals step asserts the
  columns its table gives. Test-only; rests on r42, which both scenarios carry.

## 4. Tests the decisions break

- `then_steps` awaiting-ruling step (line 110) and the deprecated r41 scenario: under D1, whichever answer; kept,
  rewritten or retired per the answer.
- `given_steps` "the stages' sessions took" (line 108): rewritten to take the 5- or 7-column table (D7); the
  deprecated r42 scenario stays green.
- `then_steps` "gives the totals" (127-135): rewritten to assert each column its table names, turns and round trips
  included (D6), so the new r42 scenario's 20 and 43 are checked; the deprecated one still asserts its 7 columns.
- r44 show and r45 compare steps (show_steps 53-60, 63-68): checked from the notes, they assert headers and listed
  rows only and stay green with a round trips column and new totals rows. r40, r43, r46-r52 steps: per the notes,
  they check named fields or refusals and stay green. No supervision or work-queue test is touched (D4).

## 5. Open cases (for the implementer to name, not choose)

- A session id found in more than one project directory of the store.
- A stage with a transcript in the store but no `session.json` (turns absent, round trips present).
- The round trips total when some stages have round trips and some do not, and when none do (given as 0 or left out).
- `show` and `compare` on a measurement written before this change: no turns or round trips totals, and a work-item
  key under the old awaiting name.
- The s-9 transcript Given's "20 turns": a transcript has no turn count; what the step writes for it.
- D1 of the notes' defects: `--sessions` naming a missing directory exits 0 silently; not in this work-item.
