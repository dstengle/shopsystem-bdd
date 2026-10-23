# w102 research notes

Tools: plugin `tools` 0.24.0; `refs` run. `tests-of`/`untested` not usable: no map (`.shop/scratch/tools/coverage` absent), so tests are listed `by search`. Counts marked `refs`, `run`, `read` or `by search`.

Accepted: r47 (2 scenarios, plus the @deprecated copy), r57, r58, r59. No Retires section.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q -p no:warnings <10 node ids of tests/scenarios/test_batch_measurement.py>` (run). 4 passed (r47 and the deprecated r47 rows, by elimination from the summary); 6 failed with StepDefinitionNotFoundError:

- r58, U+2028 / U+2029 / U+0085 rows: `Given "the text of one of those messages holds U+2028 inside its JSON string"`, no step (batch_measurement_given_steps.py). `store_session` (batch_measurement_transcripts.py) takes no text. Behind it, code: `measure_read.json_rows` splits on `splitlines()` (run, probe 1).
- r59, log.jsonl and transcript rows: `Given "the session's local time zone is UTC+05:00"`, no step (line 72). Behind it, read: `"the directory sessions holds the transcript s-9, starting at ..."` (line 74; existing step is `...holds the transcripts`), `"the measurement gives the session s-9"` (line 80), no step; `"the measurement gives the totals"` with a time-only table: `gives_totals` (batch_measurement_then_steps.py:139) reads `wanted["stages"]`, KeyError. Code: works (run, probe 2).
- r57: `Given "that stage was run as the agent researcher"`, no step (existing one needs `in the session {session}`, given_steps.py:73). Read: `"that stage's session.json is empty"`, `"the measurement gives no turns, ... for the stage"` and `"the measurement names the stage as a stage whose session.json is empty"` also have no step. Code: `measure_read.read_session_json` refuses the empty file (run, probe 3).

## 2. What the system answers today

Probes (run), files `.shop/scratch/w102-1-research/probe_measure.py`, `probe_measure_nearest.py`, `probe_escape.py`; `python3 -m pytest -q -s -n 0 -p no:warnings <file>`; each case is its own repo under scratch, `scripts/measure` run as a subprocess with `CLAUDE_CONFIG_DIR` in the repo.

1. r58 store transcript (`claude-store`, 3 messages, 3 request ids), one text holding a break: U+2028, U+2029, U+0085 each exit 1, `s-1.jsonl:1 is not a JSON object; the shape of s-1.jsonl is not known`, nothing written. Control with no break: exit 0, stage `round_trips: 3`.
2. r58 `--sessions sessions` transcript with U+2028 or U+0085: exit 1, `sessions/s-9.jsonl:1 is not a JSON object`.
3. r59 log.jsonl times `07:55Z` and `11:40+02:00`, s-9 at `08:30+00:00`, with `TZ=XXX-5` (UTC+5) and with TZ unset: exit 0, totals `time: 1 hour 45 minutes`, session s-9 given. Transcript-Z variant with TZ=+5: same.
4. r59 date: the same run under TZ=+5 wrote `2026-10-24-i7-cart.md`, without TZ `2026-10-23-i7-cart.md`: the file day is the local day.
5. r57 `session.json` zero bytes, or `" \n"`, stage with or without end: exit 1, `...session.json is not a session.json of a shape measure knows (no usage with input and output tokens)`, nothing written.
6. r57 empty research beside a good plan stage: whole run refused (exit 1, nothing written).
7. r57 empty session.json with a 3-request store transcript: refused before round trips are read.
8. r47 control, `["not","a","session"]`: exit 1 naming the file (passes).
9. Nearest: log.jsonl row with a raw U+2028 in its agent string: exit 1, `log.jsonl:1 is not a JSON object`. Same reader as the transcript.
10. Nearest: `--sessions nosuch` (missing dir): exit 0, `sessions: []`, no warning.
11. Nearest: zero-byte `--sessions` transcript: exit 0, `sessions: []`.
12. Nearest: zero-byte store transcript: stage gets `round_trips: 0`. No transcript at all: key absent. Two different answers.
13. Nearest: two stages naming session s-1, each with its own session.json: both get its figures, totals `turns: 28`, `cost: 0.84` (double count).
14. `json.dumps` (default `ensure_ascii`) escapes U+2028 to ` ` in a line: raw char absent, `splitlines` count 1 (run, `probe_escape.py`). The scenario helper `store_session` uses that default (read), so the r58 scenario would not exercise a raw break unless it writes with `ensure_ascii=False`.
15. `datetime.fromisoformat('2026-10-22T07:55:00Z')` works on this interpreter, Python 3.11.15 (run). `pyproject.toml` states no `requires-python` (by grep).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| measure_read.py:json_rows | splits text on `splitlines()`, so U+2028/U+2029/U+0085 end a line; a fragment is refused | r58: split on `\n` only; the other refusals stay | by search: the 27 scenario tests of test_batch_measurement.py (in-process load) | refs (2 callers), run |
| measure_read.py:read_log | reads log.jsonl through json_rows | r58 names transcript lines; a raw break in log.jsonl is refused (run, nearest 9): a decision | by search: r40, r41, r42, r51, r59 scenarios | refs, run |
| measure_read.py:assistant_rows | reads transcript rows through json_rows; refuses rows without type, time, session or usage | r58 same reader; round trips (r53, r55) read through it | by search: r53, r55, r58 scenarios | refs, read |
| measure_read.py:read_session_json | `json.loads('')` fails, usage is None, refuses naming the file | r57: empty file → no figures, stage named; non-empty unknown stays refused (r47) | by search: r47 rows (non-empty), r57 (red) | read, run |
| measure_read.py:read_session_jsons | globs `runs/*/*/session.json`, keys each file by its `session_id` | r57: an empty file has no id; key must be the run directory (`<k>-<stage>` under the work-item, supervise_worker.py:96-100); a stage with several runs makes the match a question | by search: r40, r51 scenarios | read; `refs` reports 0 callers, but measure_build.py:108 calls it (tool miss, found by search) |
| measure_build.py:stages_of | figures only when `sessions.get(session)` finds a file; round_trips read regardless | r57: the stage gets a named empty marker and no figures; round trips from the store: kept or dropped (question B) | by search: r40, r51, r57 scenarios | refs, read |
| measure_build.py:figures_of (`sessions` total) | counts stages that have `turns` | r57 stage has no turns, so not counted; r42 says totals are over the stages' sessions (question C) | by search: r42, r43 scenarios | read |
| measure_read.py:moment | naive time = UTC; Z parsed by `fromisoformat` (Python ≥3.11) | r59 already reads Z (run); no change needed; below 3.11 a Z would be refused (read) | by search: r40, r42, r59 scenarios | run |
| measure_build.py:merged_commits | `splitlines()` on git output | not a transcript: r58 does not cover it; a subject with U+2028 would split (read) | by search: r41 scenario (ASCII subjects) | read |
| measure_write.py:today | `date.today()`, local zone | r59 is about times in files; the file day follows the local zone (run, probe 4); scenarios monkeypatch `today` | by search: World.run (batch_measurement_world.py) | run |
| measure_read.py:round_trips | None when no transcript; 0 when a zero-byte transcript (run, nearest 12) | not changed; r55 | by search: r53, r55 | run |

## 4. Tests the requirements make impossible to keep

By search (no map). `grep` of tests for JSON-object refusals, empty session.json, line breaks, and `measure_read|measure_build|...` callers: only batch_measurement_* and test_batch_measurement.py touch measure. The other "empty" hits are cart and title tests, unrelated.

- none among the scenario tests that can no longer pass as they are. Verified sound (read): the r47 rows keep passing after r57/r58: their files are `["not","a","session"]` and `this is not a transcript`, still refused.
- step `gives_totals` (batch_measurement_then_steps.py:139-147): cannot take the time-only table of r59 as written (KeyError `stages`). It must read only the columns given. A step change, not a test.
- helper `store_session` (batch_measurement_transcripts.py:21-27): `json.dumps` default escapes the break, so the r58 scenario would pass for the wrong reason. A helper change, not a test.
- r53, r55 tests keep passing with `store_session` if its default output stays (read).

## 5. A step the work-item skips

- r57 path, the empty file skips `read_session_json`'s two checks: `no usage with input and output tokens` and `no total_cost_usd and num_turns`. Only that step produces these refusals (run, probe 5). After the change they land only for non-empty files; for an empty file the stage is given without figures. Nothing else reads the empty file (read).
- r57 round trips: `round_trips(session)` runs from the store whatever session.json holds (read). The stage keeps round trips under the new path unless the plan drops them.
- r58 path, the same reader: refusal line numbers change when the line count changes (read).

## 6. Defects

Each: command run, what came back. Probe files are in the scratch directory.

D1. A transcript line with a U+2028, U+2029 or U+0085 in a JSON string is refused as not a JSON object (r58 case). Repro: `probe_measure.py::test_r58_store_transcript_with_line_break[U+2028]` (and `[U+2029]`, `[U+0085]`): exit 1, `...s-1.jsonl:1 is not a JSON object`. Control `[control]`: exit 0, `round_trips: 3`. Same for `--sessions`: `test_r58_sessions_transcript_with_line_break`.

D2. An empty session.json refuses the whole measurement, naming the file (r57 case). Repro: `probe_measure.py::test_r57_empty_session_json[*]`: exit 1, no record. With a good stage beside it, `test_r57_empty_next_to_good_stage`: exit 1, nothing written.

D3. A log.jsonl row with a raw U+2028 is refused (nearest). Repro: `probe_measure_nearest.py::test_log_row_with_raw_line_break`: exit 1, `log.jsonl:1 is not a JSON object`. The requirement names transcript lines only (decision).

D4. Two stages naming one session both take its figures, so totals double count. Repro: `probe_measure_nearest.py::test_two_stages_same_session_id_json`: stages 2, `turns: 28`, `output_tokens: 6000`. Whether `work run` can write this is not checked (read).

D5. `--sessions` naming a missing directory exits 0 with no sessions and no warning. Repro: `probe_measure_nearest.py::test_missing_sessions_directory_fresh`: exit 0, `sessions: []`.

D6 (observation, may be intended). The measurement file's day is the local day: under TZ=+5 the run wrote `2026-10-24`, without it `2026-10-23` (`probe_measure.py::test_r59_z_in_log_with_local_zone`).

## 7. The file set

Production, must change:
- `scripts/measure_read.py` (137 lines, room 163): `json_rows` split on `\n` (r58); `read_session_json` returns a named empty marker for an empty file (r57); `read_session_jsons` keys an empty file by its run directory.
- `scripts/measure_build.py` (123, room 177): `stages_of` gives the stage the empty marker and no figures (r57); `figures_of` sessions total per question C.
Production, on the path, not edited:
- `scripts/measure` (89, room 211): entry; its CONTRACT text says "a file whose shape is not known is refused": doc update optional.
- `scripts/measure_show.py` (87, room 213): show prints stages; accepted scenarios need no change (read).
- `scripts/measure_write.py` (41, room 259): writes the record (`today`, `text_of`); no change for accepted requirements (read).
- `scripts/workqueue.py` (262, room 38): `context_path` via `text_of`; no change (read).
Tests, must change:
- `tests/scenarios/batch_measurement_given_steps.py` (213, room 87): steps for `that stage was run as the agent {agent}`, `that stage's session.json is empty`, `the session's local time zone is UTC+05:00`, the r59 transcript line, `the text of one of those messages holds {char} inside its JSON string`.
- `tests/scenarios/batch_measurement_then_steps.py` (170, room 130): empty-marker and no-figures Thens, `the measurement gives the session {name}`, `gives_totals` for a time-only table.
- `tests/scenarios/batch_measurement_transcripts.py` (39, room 261): `store_session` takes the text, writes `ensure_ascii=False` (r58); default output unchanged for r53, r55.
- `tests/scenarios/batch_measurement_world.py` (138, room 162): `session()` may write empty text; `run` sets `TZ` for the local-zone Given.
Must keep passing, no edit: `tests/scenarios/test_batch_measurement.py` (14, room 286), all 27 tests; and the rest of batch_measurement's scenario tests (r40–r56).

Questions for the plan:
- A. Which run directory an empty session.json belongs to when a stage has several runs (`<k>-<stage>`): the file has no session id.
- B. Round trips for a stage whose session.json is empty: keep (store, r53) or drop?
- C. Totals `sessions` count and r42 totals when a stage's session.json is empty.
- D. Whitespace-only session.json: "empty" (r57) or refused (today)?
- E. Date of the file in local or UTC (D6), if r39 is to follow r59's rule.
