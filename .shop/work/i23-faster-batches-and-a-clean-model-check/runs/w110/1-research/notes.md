# w110 research notes

Work-item `w110` accepts batch-measurement#r47, #r57, #r58, #r59. Accepted scenarios: 10 tests in `tests/scenarios/test_batch_measurement.py` (deprecated ×2, r47 ×2, r58 ×3, r59 ×2, r57 ×1). Tools: `Scripts:` plugin 0.24.0. `tools refs` used for names. `tools tests-of` and `untested` refuse: no map, and making one runs the whole suite (not run). So every "tests" column below is `by search` or `read`.

Probe script: `.shop/scratch/w110-1-research/probe_measure.py`, run as `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w110-1-research/probe_measure.py`. Each case is a scratch repo under `repos/`, driven through `scripts/measure` (worktree copy) as a subprocess.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_batch_measurement.py` → 6 failed, 4 passed (run).

- **r47 deprecated, two examples** (`... (deprecated)`): PASS (run). Retired by the work-item.
- **r47, two examples** (non-empty unknown session.json / transcript): PASS (run). Already refused, naming the file.
- **r58, U+2028 / U+2029 / U+0085** (3 tests): FAIL, `StepDefinitionNotFoundError: Given "the text of one of those messages holds U+2028 inside its JSON string"`. Also undefined (read): Then "measure exits successfully". Code behind it: `measure_read.json_rows` (line 25) uses `str.splitlines()`, which splits on U+2028/2029/0085; the first half is not JSON and is refused (probe). Steps to add: in `batch_measurement_given_steps.py`, a step that puts the character into one message's text in `world.store`.
- **r59, log.jsonl and transcript** (2 tests): FAIL, `StepDefinitionNotFoundError: Given "the session's local time zone is UTC+05:00"`. Further undefined (read): Given "the directory sessions holds the transcript s-9, starting at ... and ending at ..." (only the plural "the directory sessions holds the transcripts" exists); Then "the measurement gives the session s-9"; Then "measure exits successfully". Test-step defects (read, not run): `given_steps.transitions_between` (lines 88-91) passes a full ISO time to `world.stamp()`, which formats `DAY T{clock}:00+00:00`, giving `2026-10-22T2026-10-22T07:55:00Z:00+00:00`; Then `gives_totals` (then_steps 139-147) reads `wanted["stages"]` and `["sessions"]`, so the r59 one-column table `| time |` raises KeyError. `measure_build`/`measure_read` already read Z as UTC (see part 2), so r59 needs steps, not code.
- **r57** (1 test): FAIL, `StepDefinitionNotFoundError: Given "that stage was run as the agent researcher"` (given_steps has only "... in the session {session}"). Also undefined (read): Given "that stage's session.json is empty"; Then "the measurement gives no turns, output tokens, new input tokens, cache-read tokens or cost for the stage"; Then "the measurement names the stage as a stage whose session.json is empty". Code behind it, once the steps exist: `measure_read.read_session_json` (lines 50-65) refuses an empty file (json fails, `usage` None, "is not a session.json of a shape measure knows") — probe: rc 1, nothing written. `measure_build.stages_of` (lines 32-53) gives figures only `if figures:`, with no mark that says why a stage has none.

## 2. What the system answers today

Probes (run, `-n0`):

- **r57, session.json empty** (`""`): rc=1, stderr `.../runs/cart-1/1-research/session.json is not a session.json of a shape measure knows (no usage with input and output tokens)`, written=[]. Same for `"\n"`. Scenario's Given/When today: refused, nothing written. Requirement wants: given without figures, named.
- **r57 nearest, session.json absent** (no file): rc=0, stage given with `took 12 minutes`, no turns, `sessions 0`, no name for why. Same for `stages` totals: stages 1, sessions 0.
- **r58, store transcript with U+2028, U+2029, U+0085** in one message's text (3 distinct request ids): rc=1 each, `.../claude-store/projects/-work-tree/s-1.jsonl:1 is not a JSON object`. Requirement: one line, round trips 3.
- **r58, --sessions slim transcript with U+2028 in a string**: rc=1, `sessions/s-9.jsonl:1 is not a JSON object`.
- **r59, log.jsonl first `07:55:00Z`, last `11:40:00+02:00`, TZ=UTC-5**: rc=0, window `2026-10-22T07:55:00+00:00` to `...11:40:00+02:00`, time `1 hour 45 minutes`. Requirement met.
- **r59, transcript start `08:30:00Z`, log `09:55:00+02:00` to `11:40:00+02:00`, --sessions, TZ=UTC-5**: rc=0, time `1 hour 45 minutes`, session s-9 `started 2026-10-22T08:30:00+00:00`, included. Requirement met.
- **r59 nearest, lowercase `z`**: rc=1 `'2026-10-22T07:55:00z' is not an ISO time`. Not in the requirement (it says `Z`).
- **r59 nearest, fractional `.500Z`**: rc=0, window `07:55:00.500`, time `1 hour 45 minutes`.
- **r59 nearest, no offset**: rc=0, read as UTC (`+00:00`).
- **nearest, empty slim transcript under --sessions**: rc=0, stage kept with figures, `sessions []`. An empty transcript is silently a zero-session file; an empty session.json is refused.
- **nearest, session.json with usage but no num_turns**: rc=1, refused naming the file (r47 shape, unchanged).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `measure_read.py:read_session_json` (50-65) | refuses empty / non-usage session.json, "not a session.json of a shape measure knows" | r57: empty is not refused; stage is given without figures and named. Non-empty unknown is still refused (r47) | by search: r47 scenarios (non-empty input, pass); none execute the empty case | refs (1 ref, line 72); probe |
| `measure_read.py:read_session_jsons` (68-74) | calls read_session_json for every runs/*/*/session.json, so one empty file stops the whole measurement | the empty one must yield no entry and no stop | by search: r40/r41/r42 scenarios call measure initiative with session.json present | read |
| `measure_build.py:stages_of` (32-53) | adds figures `if figures:`; a stage with none gets no mark | r57: name the stage as one whose session.json is empty (absent gets no name by the feature) | by search: r57 (red at a step); r40, r51 (figures present) | read; probe absent case |
| `measure_read.py:json_rows` (22-35) | `str.splitlines()`, which also splits on U+2028/2029/0085 | r58: a line is split on "\n" only | by search: r58 (3, red); r53, r55, r43, r49 (round trips, sessions, valid lines) | refs (2 refs: read_log line 40, assistant_rows line 79) |
| `measure_read.py:assistant_rows` (77-89) and its callers `round_trips` (101-110), `read_transcripts` (113-137) | read each line through json_rows; round trips and --sessions depend on it | same change as json_rows, reached through these | by search: r53, r55, r58, r43, r49 | refs |
| `measure_read.py:moment` (13-19) | fromisoformat (accepts `Z` on 3.11+), no offset read as UTC | r59: Z is UTC. Already so (probe). Lowercase z refused (not in r59) | by search: r59 (red at steps only), r42, r43 | refs (2 refs); probe |
| `measure_build.py:figures_of` totals `sessions` = stages with `turns` (line 111) | counts only sessions that gave figures | r42 ruling reading B: keep. Empty session.json gives no turns, so not counted | by search: r42 | read |
| `measure_show.py` STAGES (11-12) and `show` | prints fixed stage columns; a new mark field would not print | not required by any accepted requirement; the plan decides whether show prints it | by search: r44, r54, r56 show steps; none executes an empty-session stage | read |
| `scripts/measure` CONTRACT (13-38) | states only "a file whose shape is not known is refused" | r57 adds the empty rule, so the contract text is out of date | none (text only) | read |

## 4. Tests the requirements make impossible to keep

Searched by name and by text (`tools tests-of` not available). Found by search: no test in `tests/scripts/` imports or drives `measure_read`, `measure_build`, `measure_show` or `measure_write` (grep for those names and `scripts/measure` returned no files). Everything measure-related is in `tests/scenarios/batch_measurement_*` and `test_batch_measurement.py`.

- `tests/scenarios/test_batch_measurement.py`, the two `...(deprecated)` tests: pass today and would pass under r47 (their input is non-empty). Retired by the work-item (`Retires`: delivery#r17), so the plan removes them with the feature's Scenario Outline (features/batch-measurement.feature lines 22-35). Verified by run and by reading their Givens.
- `batch_measurement_then_steps.py:gives_totals` (139-147): cannot pass the r59 table (`| time |` only) — KeyError `stages`. Read. Must accept a table without stages/sessions (plan's choice how).
- `batch_measurement_given_steps.py:transitions_between` (88-91): wrong with the r59 ISO examples (see part 1). Read.
- Expected test of empty session.json refusal: none found (by search: the r47 steps write non-empty JSON; `then_steps.refuses_naming` only checks the name). Nothing to keep or drop beyond the deprecated pair.
- `measure_read` tests of splitlines behaviour: none found by search. Nothing to keep.
- Checked: the r47 non-deprecated pair (run, pass), kept as is. `then_steps.refuses_naming` (36-37) matches the name `session.json` for both kinds; still valid after r57 for the non-empty cases.

## 5. A step the work-item skips

**r57 empty session.json** skips the refusal in `read_session_json` (the step that validates usage and cost). Refusals and effects that only that step gives, shown by probe (run) or read:
- empty or whitespace file: refusal "is not a session.json of a shape measure knows (no usage with input and output tokens)", rc 1, nothing written (run: r57 empty, newline-only).
- usage missing input/output tokens: same refusal (read, same branch).
- no total_cost_usd or num_turns: refusal "(no total_cost_usd and num_turns)", rc 1, nothing written (run: nearest no-turns).
- Effect only this step produces: the `figures` dict keyed by session id in `read_session_jsons`. An empty file has no id, so no entry: the stage gets no figures, which is what r57 wants, but the entry-by-id path is also skipped (read).
- Effect: the "nothing written" guarantee on a refusal is not reached on the new path (read).

**r58 line split** changes `json_rows`. Refusals and effects it gives today, shown by probe or read:
- a non-object line refused with `file:line is not a JSON object` (run: r58 cases show the message for the split halves; read for the non-split case).
- blank lines skipped (read, line 26-27): the new split must still skip blank lines.
- a CRLF file: `splitlines` strips `\r`; split on `\n` leaves `\r`, which `json.loads` accepts as whitespace (read, not run).

**r59**: no step skipped; `moment` refusal "is not an ISO time" (run: lowercase z) stays.

## 6. Defects

### D1: a JSON string holding U+2028, U+2029 or U+0085 is split into two lines and refused
Command: `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w110-1-research/probe_measure.py -k r58` (the probe's r58 cases).
Came back: rc=1, `.../claude-store/projects/-work-tree/s-1.jsonl:1 is not a JSON object; the shape of s-1.jsonl is not known`, for each of the three characters. With `--sessions sessions` and a slim row with `"a b"`: rc=1, `sessions/s-9.jsonl:1 is not a JSON object`.

### D2 (candidate): an empty transcript under --sessions is silently read as no session
Command: probe case "nearest: empty slim transcript under --sessions".
Came back: rc=0, `sessions []`, one stage kept. An empty session.json is refused in the same run's style. Not judged here.

### D3 (candidate): a stage whose session.json is absent is given with no figures and no note
Command: probe case "r57 session.json absent".
Came back: rc=0, `stages` lists the stage with `took 12 minutes`, no turns or tokens, and nothing says why. The feature names only the empty case. Not judged here.

## 7. The file set

Must change for the 10 scenarios to pass, and for passing ones to keep passing:
- `scripts/measure_read.py` (137 lines; room 163): `json_rows` splits on "\n" (r58); `read_session_json` returns no figures for an empty file, not a refusal (r57). Found by refs, probe.
- `scripts/measure_build.py` (123 lines; room 177): `stages_of` names a stage whose session.json is empty (r57). Found by read, probe.
- `scripts/measure` (89 lines; room 211): CONTRACT text on the empty rule (documentation; needed for the requirement text, not the tests). Found by read.
- `tests/scenarios/batch_measurement_given_steps.py` (213 lines; room 87): new steps: "that stage was run as the agent {agent}", "that stage's session.json is empty", "the text of one of those messages holds {ch} inside its JSON string", "the directory sessions holds the transcript {path}, starting at ... and ending at ...", "the session's local time zone is UTC+05:00" (set TZ and tzset); `transitions_between` takes ISO times verbatim. Found by run (undefined steps) and read.
- `tests/scenarios/batch_measurement_then_steps.py` (170 lines; room 130): "measure exits successfully", "the measurement gives the session {name}", "the measurement names the stage as ...", "the measurement gives no turns ... for the stage"; `gives_totals` accepts the r59 table. Found by run and read.
- `tests/scenarios/batch_measurement_world.py` (138 lines; room 162): may need a raw empty session.json text and a TZ hook. Found by read.
- `tests/scenarios/batch_measurement_transcripts.py` (39 lines; room 261): may need a helper that puts U+2028 into a store row's text. Found by read.
- `features/batch-measurement.feature` (267 lines; not Python, so no limit): remove the deprecated Scenario Outline (lines 22-35), per `Retires`. Found by read of the brief and the file.

On the change's path, not edited:
- `scripts/measure_show.py` (87 lines; room 213): prints stage columns; edit only if the plan prints the new mark. Found by read.
- `scripts/measure_write.py` (41 lines; room 259): writes the record; calls workqueue.context_path (not counted, not changed). Found by read.
- `tests/scenarios/batch_measurement_show_steps.py` (119 lines; room 181): show scenarios; not edited. Found by read.
- `tests/scenarios/test_batch_measurement.py` (14 lines; room 286): unchanged.

Size: `tools size --limit 300` printed nothing (run): no tracked Python file over 300 lines.

Worktree: `git status --porcelain` empty before and after (run). The scratch dir is not listed (ignored under `.shop/`). Worktree HEAD `7baf1910`; the brief's Base `1ad62818` not compared.
