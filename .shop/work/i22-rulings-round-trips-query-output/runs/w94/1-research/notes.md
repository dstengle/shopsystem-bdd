# w94 research notes

Work-item w94 "measure counts round trips": accepts batch-measurement r41, r42, r53-r56.
Accepted scenarios: 8 (features/batch-measurement.feature). Plugin scripts: /home/vscode/shopsystem-bdd/scripts (tools used).
Tools: `tools tests-of` has no map ("no map: make one with tools map"); map not made, so test coverage by search.
`tools refs` misses read_transcripts and read_session_jsons (0 refs) though measure_build.py imports and calls them (by search: :7, :85, :99).
`tools size --limit 300`: no file over the limit.

## 1. Why each accepted scenario is red today

Run: `python3 -m pytest -q -p no:warnings "tests/scenarios/test_batch_measurement.py::<name>"`, one per scenario. (run)

- r41 deprecated, "awaiting-ruling" (`..._awaitingruling_..._deprecated`): PASSES (run). Keep or retire it: see 4.
- r41 "awaiting-answer" (`..._awaitinganswer_...`): FAILS (run). StepDefinitionNotFoundError, Then "it gives cart-1 1 time to awaiting-answer and 1 time to failed" (batch_measurement_then_steps.py:110, the pattern names awaiting-ruling). Behind it: scripts/measure_build.py:76 counts `to == "awaiting-ruling"` only, so awaiting-answer would count 0; the commit steps are not reached (read).
- r42 deprecated totals: PASSES (run).
- r42 totals "turns and round trips included": FAILS (run). ValueError at Given "the stages' sessions took" (batch_measurement_given_steps.py:108 unpacks 5 columns; the table has 7). Then (read): the transcript step at given_steps:113-116 has no "turns, round trips" pattern; scripts/measure_build.py:102-107 has no turns or round trips total; the totals step (then_steps:127-135) does not assert the turns and round trips columns, so it would pass them silently.
- r53 "each stage is given with its session's round trips": FAILS (run). StepDefinitionNotFoundError at Given "i7-cart's log.jsonl gives work-item cart-1's research stage a start and an end, run in the session s-1" (given_steps:63-70 needs "a start at ... and an end at"). Then (read): "the session s-1 took 14 turns" has no step (given_steps:81 needs tokens); "the transcript of the session s-1 holds 40 assistant messages..." has no step; the stage table's "round trips" column hits NUMBERS (then_steps:73) with no key. Code: scripts/measure_build.py:26-44 stages_of has no round trips; scripts/measure_read.py:76-109 read_transcripts counts no requests per session and reads only the --sessions directory, never Claude Code's store.
- r55 "stage whose session has no transcript is given without round trips": FAILS (run). Same undefined Given as r53 (given_steps:63). Then (read): "took 14 turns", "no transcript of the session s-1 can be found", "gives the stage with 14 turns", "gives no round trips for the stage" have no steps. Code already omits the key (P3, section 2).
- r54 "show prints each stage's round trips beside its turns": FAILS (run). StepDefinitionNotFoundError, Given "the measurement ... that measure wrote, giving work-item cart-1's research stage 14 turns and 31 round trips" (batch_measurement_show_steps.py:19-23 has no "giving" form). Then (read): "the printed stage of cart-1's research shows" has no step. Code: scripts/measure_show.py:11-12 STAGES has no round trips column.
- r56 "show prints the stages of a measurement that gives no round trips without them": FAILS (run). Undefined Given "... that measure wrote, giving no round trips" (show_steps:19). Then (read): "the stages are printed", "no round trips are printed" have no steps. Code already prints without round trips (P8).

## 2. What the system answers today

Probes (run): `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w94-1-research/probe_measure.py` and `..._probe_transcripts.py`. Each builds its repo under .shop/scratch/w94-1-research/ and runs scripts/measure main() there. The probe repos have no .git (commits empty).

- P1 r40 baseline: stage cart-1 research, start 10:00, end 10:12, session.json (14 turns, 3000 out, 2000 in, 50000 cache-read, 0.42). Stage has turns, tokens, cost, took. No round-trip key. Totals sessions 1.
- P2 r53 nearest: transcript sessions/s-1.jsonl with 40 assistant rows, 31 requestIds. Without --sessions: no transcript read, stage has no round trips, exit 0. With --sessions sessions: stage still has no round trips; sessions entry (s-1) gives output 155 (31x5, deduped by requestId) and no request count; exit 0.
- P3 r55 nearest: session.json present, empty sessions dir: exit 0, stage given with 14 turns and no round trips.
- P4 absent: --sessions nowhere (directory missing): exit 0, sessions []. No message (defect D1).
- P5 r41 with awaiting-answer in log: work_items awaiting_ruling 0, failed 1, transitions listed. Same log with awaiting-ruling: awaiting_ruling 1.
- P6 absent: stage with start and end, no session.json: stage has no turns or tokens; totals stages 1, sessions 0, tokens 0.
- P7 empty: log with transitions only: stages [], totals stages 0, time "1 hour 45 minutes" (from transitions).
- P8 show today of a fresh measurement: stage table columns work-item, stage, agent, session, took, turns, output, new input, cache read, cost. No round trips. The totals list has no turns or round trips.
- P9 r42 numbers: s-1 (ended) and s-2 (unended) plus sessions/s-9.jsonl (45 rows) inside window: totals stages 2, sessions 2, output 4000, new input 2500, cache-read 70000, cost 0.60, time 1 hour 45 minutes; s-9 is not in the totals, listed under sessions. Consistent with r42 (its 20 turns are not counted in the totals).
- T1-T3 (probe_transcripts.py, run): a non-JSON line, a row with no type, an assistant row with no usage: each exit 1, names the file and line, nothing written. See 5.
- T4 (run): subagent rows attributed to the dispatching session. See 5.
- Not probed: a session id in two transcript files; a stage id twice.

## 3. Old assumptions

Requirement r41 renames the awaiting status to awaiting-answer; r53 adds the round trips source (Claude Code's store, by session id); r54/r56 change the show columns.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/measure_build.py:work_items_of (line 76-77) | counts `to == "awaiting-ruling"` into key awaiting_ruling | must count awaiting-answer; deprecated scenario expects awaiting-ruling | `..._awaitingruling_..._deprecated` (passes); awaiting-answer scenario (fails earlier, at its step) | read, run |
| scripts/measure_show.py:13 ITEMS | header and key "awaiting_ruling" | renamed with r41 | show scenarios (r44 and r54/r56 ones); show of a fresh record (P8) | read, run |
| scripts/measure:22-23 CONTRACT | text "awaiting-ruling" | renamed | none (help text) | read |
| scripts/workqueue.py:16 STATUSES | status set has "awaiting-ruling", no awaiting-answer | the log writes awaiting-ruling today (w93 in this initiative's log); the count of awaiting-answer reads 0 on real logs until the status is renamed | none in measure's tests; tests/scenarios/test_supervision.py:108,110 and supervision_*_steps.py (by search) | read, grep |
| scripts/model_work.py:12 | work-item statuses include awaiting-ruling | same | none for measure (by search) | read |
| scripts/supervise.py:156,237,245; scripts/supervise_merge.py:71,82,88,106 | write or test awaiting-ruling | same (writers of the log's transitions) | supervision scenarios (by search) | read |
| spec/index.md:123, features/work-queue.feature:206-218 | spec already says awaiting-answer | the spec and the code disagree today | none (not run) | grep |
| scripts/measure_build.py:stages_of (line 33-35) | takes turns and tokens from session.json only | round trips come from the transcript, not session.json | every stage scenario: the r42 deprecated one (run, passes) and r42/r53/r55 (read, through the step) | read, run |
| scripts/measure_build.py:figures_of totals (line 102-107) | totals sessions = stages with turns; tokens and cost summed | round_trips total must sum the stages' round trips, not sessions | r42 scenarios (run) | read, run |
| scripts/measure_build.py:figures_of (line 110-111) | sessions only from --sessions dir | round trips read from Claude Code's store without --sessions | r43/r49 scenarios (read; not run) | read |
| scripts/measure_read.py:read_transcripts (line 76-109) | one dict per session id, requests deduped by requestId, no count returned; scans a given directory | a count of distinct requestIds per session id, found by session id in the store | r42 new, r53, r55 (fail earlier); r43, r49 (read) | read, run (P2, T4) |
| scripts/measure_read.py:read_transcripts subagents (line 96-105) | a subagent's rows (agentId) become their own session, dispatched_by the parent | round trips of the stage's session: subagent messages in or out is open | none executes it in the accepted scenarios | run (T4) |
| scripts/measure_show.py:STAGES (line 11-12), TOTALS (line 8-10) | fixed columns; a missing key prints empty | round trips column printed only when the record holds them; totals row added | r44 show scenario (read); r45 compare scenario (read); r54/r56 (fail earlier) | read, run (P8) |
| scripts/measure_show.py:compare (line 66-76) | prints TOTALS rows | a new round trips total row | r45 (read) | read |

## 4. Tests the requirements make impossible to keep

Coverage map absent; search by text, marked `by search`. Run: the 8 accepted. The file's other 13 scenarios were not collected by the default selection (pytest.ini `-m "not fixture"` plus the work-item plugin); `-m ""` gave the same 8. Not run.

- `..._awaitingruling_..._deprecated` (r41, run passes): impossible to keep if measure counts only awaiting-answer, because its log writes awaiting-ruling and it expects 1. It needs both names counted, or a retirement. The work-item has no Retires section. Both readings: (a) keep both: count both names; (b) retire it as deprecated.
- `..._totals_..._deprecated` (r42, run passes): keeps passing only if the step "the stages' sessions took" accepts its 5-column table and the new 7-column one. Changing that step to 7 columns alone breaks it (read).
- `..._totals_...` (r42 current, run fails): not kept, it is red.
- `gives the totals` step (then_steps:127-135) asserts stages, sessions, tokens, cost, time only. It stays green with turns and round trips added, so the new scenario's 20 and 43 are not checked unless the step asserts them (read).
- r44 show test (by search: batch_measurement_show_steps.py:53-60): checks headers and one row; keeps passing with a round trips column added (read).
- r45 compare test (by search: show_steps:63-68): checks listed rows only; keeps passing with a new totals row (read).
- r40, r51, r43, r49 (not run, read): their Then steps check named fields only; keep passing.
- Verified sound (read): r46, r47, r48, r50, r52 refusal and replace steps do not touch the new code.

## 5. A step the work-item skips

The existing way (read_transcripts, via --sessions) makes these refusals and effects; a store lookup by session id that does not reuse it skips them:

- a line that is not a JSON object: refused, naming file:line, nothing written (T1, run). "sessions/s-9.jsonl:1 is not a JSON object".
- a row with no type: refused (T2, run).
- an assistant row with no time, session or usage: refused (T3, run).
- effect only this step: requests deduped by requestId (P2, run: 40 rows, 31 requestIds, output 155 = 31x5).
- effect only this step: a subagent row (agent set) is its own session, dispatched_by the parent (T4, run).
- effect only this step: session start = earliest request; window gating by sessions_found (read, measure_build.py:82-89).
- the store path as written in the work-item (Claude Code's store by session id) has no existing equivalent: read_transcripts scans a directory, never looks up by id (read).

## 6. Defects

### D1 --sessions with a directory that does not exist
Reproduction: P4 in probe_measure.py (run). Transitions in log, one stage, `measure initiative i7-cart --sessions nowhere`: exit 0, measurement written, sessions []. No message. Not judged.

## 7. The file set

Production (must change for the 8 scenarios):
- scripts/measure_read.py (109 lines, room 191): read a session's transcript by id; count distinct requestIds per session; the store location.
- scripts/measure_build.py (112, room 188): stage round trips, totals round_trips, awaiting-answer count; pass the store to stages.
- scripts/measure_show.py (76, room 224): round trips column when present; ITEMS awaiting-answer key and header.
- scripts/measure (86, room 214): CONTRACT text on round trips and awaiting-answer; a flag only if the store needs one (read).
- scripts/measure_write.py (41, room 259): none expected; on the path (writes the figures) but unchanged.

Tests (must change for the scenarios to be green and the passing ones to stay):
- tests/scenarios/batch_measurement_given_steps.py (177, room 123): log patterns with "run in the session", "took N turns", "no transcript", 7-column session table, transcripts with round trips.
- tests/scenarios/batch_measurement_then_steps.py (158, room 142): awaiting-answer step; NUMBERS round trips; stage gives "with N turns" and "no round trips"; totals asserts turns and round trips.
- tests/scenarios/batch_measurement_show_steps.py (68, room 232): "giving ... N turns and M round trips" and "giving no round trips" Givens; "the printed stage shows"; "stages are printed"; "no round trips are printed".
- tests/scenarios/batch_measurement_world.py (132, room 168): where the store lives for the test (HOME or a store setting) and a session's transcript with N requests.
- tests/scenarios/batch_measurement_transcripts.py (30, room 270): helper writing N assistant messages with M requestIds in Claude Code's own rows.
- tests/scenarios/test_batch_measurement.py (14): none expected.

Not in the file set (unless the status rename is taken on): scripts/workqueue.py (255), scripts/model_work.py (211), scripts/supervise.py, scripts/supervise_merge.py: they write awaiting-ruling (section 3).

Open questions for the planner:
- Where Claude Code's store is, and how a test points measure at it (no path in the work-item; no override in code).
- Whether subagent messages count in a stage's round trips.
- Keep or retire the deprecated r41 and r42 scenarios (no Retires section; both accepted, same requirement).
- A stage whose session has a transcript but no session.json: unspecified.
- Whether the awaiting-answer rename of the status is in this work-item (real logs say awaiting-ruling).
- The transcript "with 20 turns, 45 round trips" in r42: those are not in the totals (20 = 14+6). A planner must not add them.
