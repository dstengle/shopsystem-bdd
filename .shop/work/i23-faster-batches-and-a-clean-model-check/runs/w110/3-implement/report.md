## Budget

scripts/measure_read.py, scripts/measure_build.py, scripts/measure, tests/scenarios/batch_measurement_given_steps.py, tests/scenarios/batch_measurement_then_steps.py, tests/scenarios/batch_measurement_reading_steps.py (new), tests/scenarios/test_batch_measurement.py, tests/scenarios/batch_measurement_world.py, tests/scenarios/batch_measurement_transcripts.py, features/batch-measurement.feature (retire only)

## What changed
- measure_read: `json_rows` splits on "\n" only (r58); `read_session_jsons` returns (figures, empty stages), a zero-byte session.json gives no figures and no refusal (r57).
- measure_build: stage with empty session.json gets `"session_json": "empty"`; totals unchanged.
- scripts/measure contract text; deprecated @r47 outline retired with `features retire`.
- Steps: given/then (r57), new batch_measurement_reading_steps.py (r58, r59), `stamp` in the world takes a full ISO time as given (replaces the planned transitions_between change), `gives_totals` compares only the columns the table names. batch_measurement_transcripts.py not touched.

## Red and green
- Red: `python3 -m pytest -q --work-item w110`: 6 failed (undefined steps for r57/r58/r59). After r57 steps: refused, no measurement written (FileNotFoundError on record). After r58 steps: "s-1.jsonl:1 is not a JSON object". r59 red at undefined steps only; code already read Z as UTC (as the plan said), so it went green with steps alone.
- Final: `python3 -m pytest -q --work-item w110 tests/scenarios/test_batch_measurement.py`: 8 passed.
- Suite at start: 690 passed, 6 failed (the brief's record; failing ones were this work-item's measure scenarios plus listed expected ones).
- `tools size --limit 300`: no output; no file over.

## Tests changed under an allowance
none (gives_totals rewritten as the plan lists under "Tests the decisions break"; the deprecated outline retired per Retires)

## Open questions
Whitespace-only session.json refused; empty transcript under --sessions; absent session.json unnamed; empty session.json with no log start; U+2028 in log.jsonl also split on "\n" now (plan's open cases) — none chosen beyond the plan.

## Plan code
The plan contained no code. Commits: 5d88909, aecf1e7, 2e956ab. `measure show` unchanged (plan decision 5).
