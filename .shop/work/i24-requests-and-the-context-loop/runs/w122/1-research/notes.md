# w122 research notes

Tools: `tools refs` ran but missed from-imports (0 refs for `read_transcripts`, `round_trips`, `compare`, `show`); counts below are `by search`. `tools tests-of` and `untested`: no map, not made (brief); so test lists are `by search` or `read`. `tools size --limit 300`: no file over the limit.
Pytest: `addopts` (`-n auto`) and the work-item filter deselect non-accepted scenarios (24 deselected even with `-o addopts=""`), so they are `read`, not run.
Probes: `.shop/scratch/w122-1-research/probe_sessions.py`, run `python3 -m pytest -q -s -n 0 .shop/scratch/w122-1-research/probe_sessions.py`.

## 1. Why each accepted scenario is red today

Run each by node id, `python3 -m pytest -q "<node id>"`, under `tests/scenarios/test_batch_measurement.py`.

- **r43 deprecated** `test_sessions_gives_the_sessions_that_start_inside_the_window_..._deprecated`: **passes** (run). Retired by w122; after the r43 rule it fails (see 4).
- **r43 active** `test_sessions_gives_the_sessions_active_inside_the_window_...`: **fails** (run) at `then_steps.py:167` `gives_sessions`, FileNotFoundError: no record. Cause: the When's `measure` refused. `given_steps.py:169-172` `directory_holds` reads the table's 'messages at' cell as the end time; `stamp()` writes `2026-10-22T09:00, 09:20, 12:00:00+00:00`; `measure_read.moment` refuses (probe P2, run). Missing: `directory_holds` must take a list of message times; `slim_session` one row per time (`batch_measurement_transcripts.py:12`); `measure_build.sessions_found:104` tests start only, needs "any message inside window"; `measure_read.read_transcripts:126` keeps only the minimum start per session (no message times).
- **r60** `test_each_session_..._round_trips_tool_uses_..._compactions`: **fails** (run) at `given_steps.py:170`, `directory_holds`: "not enough values to unpack (expected 7, got 3)": the table has no tokens columns. Read, not run: steps "holds the tool uses Read 5 times, Grep 3 times and Agent once", "holds 2 compactions", "holds no compaction", "holds the tool uses Read twice" are undefined (no step matches them, `by search` of step files). Missing in code: per-session round trips (`measure_build.sessions_found` never calls `measure_read.round_trips`), tool uses by name, dispatched list (only `dispatched_by` exists), compactions (no reader). Then `gives_sessions` (`then_steps.py:165`) checks only the three token columns, so it would not check the new columns even if the Givens worked.
- **r61** `test_show_prints_each_session's_..._beside_its_tokens`: **fails** (run): `StepDefinitionNotFoundError` for `Given "the measurement .shop/records/measurements/2026-10-24-i7-cart.md that measure wrote, giving the sessions"`, line 246. `show_steps.py:19` (`the measurement {path} that measure wrote`) cannot match the trailing `, giving the sessions`. Read, not run: "the printed sessions show" (Then) is undefined. Code: `measure_show.py:14` `SESSIONS` has no round trips, tool uses, dispatched or compactions columns; `measure_show.py:35` `cell()` prints a dict as its length (`tool uses` would print a count).
- **r62** `test_compare_prints_the_totals_over_the_sessions_...`: **fails** (run): `StepDefinitionNotFoundError` for `Given "the measurement a for i6-pay that measure wrote, giving the sessions"`, line 271 (same cause as r61). Read, not run: "the totals over the sessions are printed side by side" (Then) is undefined. Code: `measure_show.py:77` `compare` and `:17` `totals_of` print only `totals` rows; no sessions totals.

## 2. What the system answers today

Probes (run, `python3 -m pytest -q -s -n 0 .shop/scratch/w122-1-research/probe_sessions.py`, each builds its own repo in the scratch dir and runs `scripts/measure` as a subprocess):

- **P1** r43 sessions with all messages, `measure initiative i7-cart --sessions sessions`: exit 0. Given: s-7 (09:00, 09:20, 12:00), s-8 (09:30, 09:50, 10:05), s-9 (11:00, 12:30, 9000 output), s-11 (12:00, 12:20; dispatched by s-9), s-10 (11:50, 12:10), s-12 (12:05, 12:08; by s-10). Window 09:55–11:40 (the log's transitions). Output: only `s-9` and `s-11`. s-8 (inside at 10:05) is excluded: today's rule is start-only.
- **P2** the r43 active Given as the step writes it (a time cell `09:00, 09:20, 12:00`): exit 1, stderr `measure: sessions/s-7.jsonl: '2026-10-22T09:00, 09:20, 12:00:00+00:00' is not an ISO time`, nothing written.
- **P3** `--sessions nosuch` (missing directory): exit 0, record written, `sessions: []`. Empty directory: exit 0, `sessions: []`.
- **P4** raw Claude Code rows (user row, two assistant rows with one `requestId` split over two content blocks, one `tool_use` Read, a subagent file with `agentId` a1 under `sessions/s-9/subagents/`): s-9 output 50 (max of the two rows), new input 20, cache-read 300; `a1` dispatched by s-9 with 7/1/2 tokens. No tool uses, no round trips, no compactions keys.
- **P5** s-9 in the directory with a Claude Code store transcript at `claude-store/projects/-w/s-9.jsonl` (3 rows, 2 request ids): `sessions` entry for s-9 has `round_trips: None`. The store is not read for `--sessions` sessions.
- **P6** `show` of a written record: prints stages, work-items, totals and a `sessions` table with columns session, started, dispatched by, output, new input, cache-read only. `compare` of that record with a hand-shaped record `{"sessions": [...]}` (no totals, the shape r62's Given needs): the `b` column is blank and ratio `-`, no sessions rows. Totals print `round trips | 0` with no stage round trips (no store transcript).

Nearest cases not given by the scenarios: the window's start with no transitions (`sessions_found` returns none when `first` is None, read); a subagent whose parent is outside the window (included via `dispatched_by`, read: `sessions_found:109`).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| measure_build.py:sessions_found (line 104-111) | keeps sessions whose start is in window, plus their dispatched sessions | r43: a session active in window (any message inside), whenever it started | r43 deprecated (passes); r43 active (red) | search (1 call site, figures_of:135), run P1 |
| measure_read.py:read_transcripts (126-150) | per session keeps min start and summed tokens; no message times kept | r43 needs per-message times to know activity; r60 needs tool uses and compactions per session | r43 deprecated, r43 active, r60 (all via directory); none other by search | search (call at measure_build:107), read |
| measure_read.py:read_transcripts (`dispatched_by`) | one parent per session (the session that dispatched it) | r60, r61: the sessions a session dispatched (inverse, children list) | none asserts dispatched lists | search (`dispatched_by`: build, read, show, record JSON) |
| measure_show.py:SESSIONS, section (14, 51) | sessions table columns: session, started, dispatched by, three token kinds | r61: add round trips, tool uses, dispatched, compactions | r61 (red); r44 prints a record with no sessions | search |
| measure_show.py:cell (35-40) | a dict prints as its length, a list as its length | tool uses as `Read 5, Grep 3, Agent 1` would print as `3` if passed through `cell` | none | search, read |
| measure_show.py:compare, totals_of (17-21, 77-87) | rows only from `totals` (plus turns, round trips when totals hold them) | r62: totals over `sessions` of round trips, tool uses, compactions | r45 (read: passes), r62 (red) | search, run P6 |
| measure_show.py:show (56-68) | adds a sessions section when figures hold `sessions` | r61 on records written before this change: they hold sessions without round trips and tool uses | none (no test reads an old record) | search (old record: `.shop/records/measurements/2026-10-23-i22-rulings-round-trips-query-output.md`, sessions with `dispatched_by`) |
| measure_build.py:figures_of (134-135) | `sessions` = sessions_found output | sessions list gains keys; shape changes for records | r43 (both), r60 | search |
| measure_read.py:round_trips (114-123) | stage round trips from the store, excluding subagent and sidechain rows | r60 wants the same for `--sessions` sessions; P5 shows it is not used there | r53, r55 (read, not run) | search, run P5 |
| scripts/measure CONTRACT (lines 28-30) and `--sessions` help (line 70) | "each session that starts inside the initiative's window" | r43 changes the rule; help text goes stale | none | search (`starts inside`) |
| skills/analyzing-a-batch/SKILL.md:16 | "the person's own, and those they dispatched" | describes the rule loosely; no change required by a test | none | search |

## 4. Tests the requirements make impossible to keep

Tests by search: the batch-measurement feature (`tests/scenarios/test_batch_measurement.py`, 29 scenarios). `tools tests-of` had no map.

- **r43 deprecated** (`test_sessions_gives_..._deprecated`, feature line 170): passes today. Impossible to keep after r43: s-8 has a message at 10:05 inside the window, so it is given and "it gives neither s-8 nor s-10" fails. Retired by w122's `Retires`; remove the scenario from `features/batch-measurement.feature` lines 170-186.
- **r60 / r61 / r62 Givens and Thens**: not impossible, but red; see 1.
- **`then_steps.py:165` gives_sessions**: keeps passing after the change, but checks only the three token columns: the new r60 columns would go unchecked. Test weakness, not a break. Read.
- **`tests/scripts/test_measure_runs.py`** (two tests, `figures_of` on stage runs, `totals.sessions == 1`): sound, unaffected if `totals` and stages are unchanged. Read.
- **r45** `compare` scenario (feature 256-266): sound if the totals rows keep their names and cells. Read.
- **r44** `printed_as_tables` (`show_steps.py:104`): sound, checks headers and one stage row only. Read.
- **r49** `holds_none` (`then_steps.py:181`): sound if tool uses are counted by name and tool input is not copied (the scenario's Bash call text is the input). Read.
- **Conflict for the plan (two readings):** the r60 Givens write the tool uses and compactions into the Claude Code store (`world.store`, through `store_transcript`), but the sessions come from the directory (`directory_holds`, slim rows). Reading A: tool uses and compactions are read from the store as round trips are. Reading B: from the directory transcript. The Givens support A for round trips only.

## 5. A step the work-item skips

Existing way for a stage session's round trips: `measure_read.round_trips` looks the session up in Claude Code's store (`projects/*/<session>.jsonl`), keeps rows of that session only, excludes `agentId`, `agent` and `isSidechain` rows, and dedupes by request key. The `--sessions` path (`read_transcripts`) reads the directory instead, never calls `round_trips`, and never excludes subagent rows (it attributes them to their own session). Effects only the existing way produces, shown:

- Round trips for a session found in the directory: none (P5, run). Counting them from the directory would count subagent rows unless the sidechain exclusion is repeated (P4 shows subagent rows arrive as their own sessions, read).
- The existing way refuses a row with no `type`, or an assistant row with no `usage`, `session` or `timestamp` (`assistant_rows`, read); a new tool-use or compaction reader on the same rows inherits that refusal, which would stop the whole `--sessions` measurement (read, not run).
- The store path (`*/<session>.jsonl` in any project) and the spec's implementation note (`batch-measurement.md:57`: "read from the path its session.json records") differ: `round_trips` does not read the path the stage's `session.json` records (read).

## 6. Defects

**D1. `--sessions` with a missing or empty directory is accepted.**
Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w122-1-research/probe_sessions.py::test_p3_missing_and_empty_directories`
Came back: `missing dir: exit 0`, record written, `sessions: []`; empty dir: `exit 0`, `sessions: []`.

**D2. Totals print `round trips 0` where no transcript was found.**
Command: `...probe_sessions.py::test_p6_show_and_compare_of_a_record_with_sessions`
Came back: the stage has no `round_trips` (no store transcript), and `totals.round_trips` is 0 (`measure_build.py:126` sums with default 0), printed as `round trips | 0`. r55 gives such a stage without round trips; the total reads as counted.

**D3 (read, not run). `read_transcripts` keeps the last row's input and cache tokens of a request, not the maximum.** `measure_read.py:136-141` overwrites `new_input_tokens` and `cache_read_tokens` per row, while `output_tokens` takes the max. Rows of one request with differing usage would give a different total from the output's rule. P4 used equal usage, so it does not show it.

## 7. The file set

Production and test files the work-item changes:

- `scripts/measure_build.py` (136): `sessions_found` active-in-window rule; per-session round trips, tool uses by name, dispatched list, compactions. Search and run P1, P5.
- `scripts/measure_read.py` (150): `read_transcripts` keeps message times and tool-use names; new compaction count; round trips for directory sessions. Search, read, P4, P5.
- `scripts/measure_show.py` (87): `SESSIONS` columns; tool-uses text; `compare` sessions totals. Search, run P6, r61 and r62 reads.
- `scripts/measure` (90): CONTRACT text lines 28-30 and `--sessions` help. Search.
- `features/batch-measurement.feature` (322, not Python, no size rule): delete the deprecated r43 scenario (lines 170-186). Search, run.
- `tests/scenarios/batch_measurement_given_steps.py` (226): `directory_holds` for 'messages at' and a 3-column table; Givens for tool uses and compactions. Run r43 active and r60.
- `tests/scenarios/batch_measurement_transcripts.py` (39): slim rows per message time; tool-use blocks; compaction marker. Read.
- `tests/scenarios/batch_measurement_show_steps.py` (119): Givens "that measure wrote, giving the sessions" (r61, r62); Thens "the printed sessions show", "the totals over the sessions are printed side by side". Run r61, r62.
- `tests/scenarios/batch_measurement_then_steps.py` (185): `gives_sessions` checks the new columns. Read.
- `tests/scenarios/batch_measurement_world.py` (140): only if the store is written with tool-use and compaction rows. Read.

Modules on the change's path, edited or not, with line count and room under 300:

- `scripts/measure` (90): room 210; edited.
- `scripts/measure_build.py` (136): room 164; edited.
- `scripts/measure_read.py` (150): room 150; edited.
- `scripts/measure_show.py` (87): room 213; edited.
- `scripts/measure_write.py` (41): room 259; not edited (writes the record; figures shape only; imports `workqueue`, not edited).
- `tests/scenarios/batch_measurement_given_steps.py` (226): room 74; edited.
- `tests/scenarios/batch_measurement_show_steps.py` (119): room 181; edited.
- `tests/scenarios/batch_measurement_then_steps.py` (185): room 115; edited.
- `tests/scenarios/batch_measurement_transcripts.py` (39): room 261; edited.
- `tests/scenarios/batch_measurement_world.py` (140): room 160; maybe edited.
- `tests/scripts/test_measure_runs.py` (43): room 257; not edited, must keep passing.
