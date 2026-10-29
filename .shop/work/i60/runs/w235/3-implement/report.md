## Budget

scripts/work, scripts/workqueue_request.py, scripts/migrate, scripts/migrate_prompt.py, hooks/hooks.json, tests/scenarios/requests_steps.py, tests/scenarios/requests_write_steps.py, tests/scenarios/requests_session_steps.py, tests/scenarios/test_requests.py, CLAUDE.md, README.md (11)

## Changed
- `work delegate <request> <delegation>` (scripts/work, workqueue_request.delegate): writes/replaces JSON-quoted `delegation` field (inserted when absent), committed via `_change`; refuses empty and delivered/refused/withdrawn (naming status); no turn check, status and turn unchanged.
- `migrate prompting` (scripts/migrate_prompt.py) + UserPromptSubmit entry in hooks/hooks.json: tells a session, when an open request exists, to run `work delegate` in the same reply with `The person, <date>: "<words>"`.
- Steps: requests_steps (delegate form of the When), requests_write_steps (Givens/Thens), new requests_session_steps (hook-driven session double), test_requests import. CLAUDE.md row and README line.

## Runs
- Start suite record: 1069 passed, 11 failed (the 11 were this work-item's scenarios among others; see brief).
- Red: `python3 -m pytest -q --work-item w235` -> 11 failed, 180 passed (no `delegate` subcommand; undefined r72 steps), as expected.
- Green (final): `python3 -m pytest -q --work-item w235` -> 191 passed, 1 skipped. tests/scenarios/test_requests.py and test_migration*.py pass.
- `tools size --limit 300`: no output (no file over).

## Tests changed under an allowance
none (the_upstream_runs is a step, extended per plan)

## Open questions
- Refusal wording for r68; unknown request; newline/quotes in delegation text; unreadable frontmatter in the hook; hook with stdin not read. Left unchosen beyond the minimum.

## Plan contained no code; nothing pasted.
## Commits: ed25c279, ab71c3fc
## Files: scripts/work, scripts/workqueue_request.py, scripts/migrate, scripts/migrate_prompt.py, hooks/hooks.json, tests/scenarios/{requests_steps,requests_write_steps,requests_session_steps,test_requests}.py, CLAUDE.md, README.md
