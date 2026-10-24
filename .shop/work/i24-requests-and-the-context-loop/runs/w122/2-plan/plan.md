# Plan of w122: the sessions active in the window, with their round trips, tool uses, dispatches and compactions

From the research notes (`runs/w122/1-research/notes.md`); scenarios in `features/batch-measurement.feature`, run through `tests/scenarios/test_batch_measurement.py`.

## 1. What goes green

- **batch-measurement#r43**: "--sessions gives the sessions active inside the window, starting inside it or before it with a message inside it, and every session they dispatched". Red today: the Given `directory_holds` reads the 'messages at' cell as one end time, so `measure` refuses it as not an ISO time (probe P2). Behind that, `measure_build.sessions_found` keeps sessions by their start only (P1 drops s-8, which has a message at 10:05), and `measure_read.read_transcripts` keeps only each session's earliest time.
- **batch-measurement#r60**: "each session --sessions gives is given with its round trips, tool uses by tool name, dispatches and compactions". Red today: `directory_holds` expects seven columns and gets three. The steps for tool uses and compactions do not exist. No code counts round trips, tool uses or compactions for a `--sessions` session, and none lists the sessions it dispatched. `gives_sessions` checks only the token columns.
- **batch-measurement#r61**: "show prints each session's round trips, tool uses by tool name, dispatches and compactions beside its tokens". Red today: no step defines the Given "… that measure wrote, giving the sessions" or the Then "the printed sessions show". `measure_show.SESSIONS` has none of the four columns, and `cell` would print the tool-uses mapping as its length.
- **batch-measurement#r62**: "compare prints the totals over the sessions of round trips, tool uses and compactions side by side with the ratio of the second to the first". Red today: no step defines the Given "the measurement a for i6-pay that measure wrote, giving the sessions" or the Then "the totals over the sessions are printed side by side". `compare` prints only the `totals` rows.
- **Retired:** "--sessions gives the sessions that start inside the window and every session they dispatched (deprecated)". It passes today and cannot pass once the r43 rule is in, because s-8 becomes active. Delete it from the feature.

## 2. Where the change lands

- `scripts/measure_read.py`: `read_transcripts` keeps every message time of each session. It also counts, from each session's own rows, its round trips (distinct request ids), its tool uses by tool name and its compactions. It refuses a row it cannot read and names the file.
- `scripts/measure_build.py`: `sessions_found` keeps a session when any of its messages falls in the window, plus every session such a session dispatched. Each session entry gains its round trips, tool uses, the list of sessions it dispatched and its compactions.
- `scripts/measure_show.py`: the sessions table gains four columns (round trips, tool uses written as name and count, dispatched, compactions). `compare` gains a second side-by-side table of the totals over the sessions.
- `scripts/measure`: the CONTRACT text and the `--sessions` help say "active inside the window" instead of "starts inside".
- `features/batch-measurement.feature`: remove the deprecated r43 scenario.
- `tests/scenarios/batch_measurement_given_steps.py`: `directory_holds` takes either table shape (a 'messages at' list, or the three-column table). The transcript Givens of r60 write into the directory transcript. New Givens for tool uses and compactions.
- `tests/scenarios/batch_measurement_transcripts.py`: helpers that write one row per message time, plus rows carrying request ids, tool-use blocks and a compaction marker.
- `tests/scenarios/batch_measurement_show_steps.py`: the Given "… that measure wrote, giving the sessions" (r61 and r62 both use it), and the Thens "the printed sessions show" and "the totals over the sessions are printed side by side".
- `tests/scenarios/batch_measurement_then_steps.py`: `gives_sessions` checks every column its table names.

Removed from the researcher's set: `tests/scenarios/batch_measurement_world.py`. Decision 1 puts the r60 figures in the directory transcript, and `world.transcripts` already holds that. The store does not need tool-use or compaction rows. If the implementer finds the world must change after all, that is a finding to report.

## 3. Decisions

1. **The r60 figures come from the session's transcript in `--sessions <dir>`, not from Claude Code's store.** The notes give two readings: read them from the store, as stage round trips are, or from the directory. r43 gives "each session found there", in the directory. r60 counts what "its transcript holds", and for such a session that transcript is the one found there. The capability's note says `--sessions` reads raw transcripts or the slim export. So the code never looks up the store for a `--sessions` session. In the tests, the shared Given "the transcript of the session X holds N assistant messages with M distinct request ids" writes into that session's directory transcript when the directory holds the session. Otherwise it writes into the store as today, which keeps r53, r55 and r58 as they are. (r43, r60)
2. **A session is active when any of its messages falls inside the window.** The window runs from the first transition to the last. A session whose messages fall only before and after the window is not active (s-7). The sessions an active session dispatched are given whenever they ran (s-11). A session dispatched by an inactive session is not given (s-12). (r43, and its note on dispatched sessions)
3. **Each session's figures count its own rows only.** Its round trips are the distinct request ids among its own assistant messages, as r53 defines them. Rows of a session it dispatched (subagent rows) count toward that session, never toward the one that dispatched it. This brings the store path's subagent exclusion, the step the notes found skipped, to the directory path. (r53, r60)
4. **What a session entry in the record holds.** Its round trips as a number. Its tool uses as a mapping from tool name to count: the name only, never the tool's input. The ids of the sessions it dispatched, as a list. Its compactions as a number, 0 when the transcript holds none. `started` and `dispatched_by` stay. (r60, r49, design-decision/measure-an-initiative)
5. **Rows the counting cannot read are refused.** A tool-use block with no name, a request id or compaction marker of an unknown shape, or a row with no time all make `measure` refuse, naming the file. It never counts around them. (r47, design-decision/measure-refuses-unknown-shapes)
6. **How show prints the new columns.** Tool uses print as the tool name and its count, pairs separated by ", ", in the record's order. Dispatched prints as the ids separated by ", ", and as an empty cell when there are none. Compactions print as a number. The four columns follow the tokens. (r61)
7. **How compare prints the session totals.** A second table after the totals table, with the same columns `total | a | b | ratio`. Its rows are round trips, tool uses (every count of every tool over every session given, dispatched sessions included) and compactions. The ratio is formatted as the existing totals format it (1.5, 1.25, 3). This table's "round trips" is a different row from the stage round trips in the totals table. The Then reads this table only. (r62)
8. **The step "… that measure wrote, giving the sessions" writes a record of the shape `measure initiative` writes.** The record has the measurement JSON block, with the table's columns as session entries (shaped as in decision 4) and empty stages and work-items. One step serves both the path form (r61) and the "<name> for <initiative>" form (r62). Two parse patterns would collide, because a path parameter also matches "a for i6-pay". (r61, r62)
9. **`gives_sessions` compares only the columns its table names.** It reads tool uses as a mapping, so their order is not asserted there, and dispatched as a list. This keeps the r43 table as it is and checks every r60 column. (r43, r60)

## 4. Tests the decisions break

- `features/batch-measurement.feature`, the deprecated scenario "--sessions gives the sessions that start inside the window and every session they dispatched (deprecated)": decision 2 breaks it (s-8 is given). It is **removed**, as the work-item's `Retires` says.
- Nothing else. The notes and `tests/` were checked, and they hold one other caller of the measure modules: `tests/scripts/test_measure_runs.py`. It calls `measure_build.figures_of` on stage runs only and asserts the stage totals, which no decision changes. The r44 `printed_as_tables`, r45 `totals_side_by_side` and r49 `holds_none` steps keep passing under decisions 6, 7 and 4. They check headers, totals rows and absent content, and none of these changes. Under decision 1 the r53, r55 and r58 stage scenarios keep their store transcripts, because those scenarios have no directory.

## 5. Open cases (the scenarios are silent; the implementer names what the code does)

- A message exactly at the window's first or last transition: whether it counts as inside.
- A dispatched session with messages inside the window whose dispatcher has none.
- An initiative whose log gives no transitions, so there is no window.
- A transcript in the slim export's shape, which may carry no request ids, no tool-use names and no compaction markers. Name what a session from it is given: the figure left out, 0, or a refusal.
- How a compaction is recognised in a raw transcript (which row marks it), checked against a real Claude Code transcript.
- The order of tool names in the record, and so in show's cell: first use, or count.
- Records written before this change, whose sessions lack the new keys: what show prints in those cells, and what compare totals when one or both measurements give no such figure. The notes' D2 shows a missing figure printed as 0.
- `compare` of one measurement that gives sessions with one that does not.
- Defects D1 (a missing or empty `--sessions` directory is accepted), D2 (a total of round trips of 0 when no transcript was found) and D3 (input and cache tokens taken from a request's last row) are outside r43 and r60–r62. Leave them as they are and report them.
