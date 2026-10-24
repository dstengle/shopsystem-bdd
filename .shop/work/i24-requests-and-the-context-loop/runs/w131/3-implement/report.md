## Budget
scripts/model_work.py, scripts/model_facts.py, scripts/model_requests.py (new), CLAUDE.md, scripts/model,
tests/scenarios/design_model_check_reading.py, tests/scenarios/design_model_check_requests.py (new),
tests/scenarios/test_design_model_check.py, features/design-model-check.feature (retire only).

## Changed
- model_requests.py: reads `.shop/work/requests/*.md` (D2 form: file q<n>.md matching id, kind request, asker, part_of or source, status, turn, `## Lines`, only known sections); emits node + status; else one file problem naming the file.
- model_work.py: `requests/` is never an initiative folder; `request` status list; job/job-path initiative gets a file problem naming initiative.md.
- model_facts.py: `request` kind, reader called. scripts/model help text, CLAUDE.md row.
- Tests: Givens in design_model_check_requests.py; q1.md row in the r19 table; import. Deprecated r19 outline retired with `features retire`.

## Red / green
Red: `python3 -m pytest -q --work-item w131 -n 0` before code (after steps written): 4 failed. r19 row: marker node fact absent
(`AssertionError: node(...)`); r112: `problems: ['.shop/work/requests: no initiative.md']` (q1.md not named); r118 job/job-path: `problems: []`. Expected: no request reader, no kind check.
Before steps: 5 failed (KeyError / undefined steps).
Green: same command after code: 160 passed, 1 skipped. Also tests/scenarios/test_design_model_check.py + tests/scripts/test_model*.py: pass.

Suite at start: 757 passed, 5 failed (the 5 are this work-item's scenarios, plus expected-failures of other items).
## Tests changed under an allowance
none (the deprecated outline's tests were removed by the Retires).
## Open questions
- Both part_of and source on a request: not a problem in code.
- Non-`q<n>.md` .md files: a file problem; subdirectories/non-md ignored.
- Duplicate request ids: not checked beyond the node kind check.
- job/job-path: v_k1/v_k2 left as they were; problem text names the kind.
## Plan code
The plan contained no code.
## size
`tools size --limit 300` printed nothing.
## Outside the file set
none.
## Commits
05d6b56
