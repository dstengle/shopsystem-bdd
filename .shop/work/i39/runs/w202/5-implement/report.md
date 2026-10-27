## Budget
skills/integrating-a-proposal/SKILL.md, tests/scenarios/spec_integration_steps.py, tests/scenarios/test_spec_integration.py

## Changed
- Question Template: removed the parenthesis asking the writer for request lines in the upstream's glossary terms (finding 1, per the person's answer). The round drafts the lines itself, as initiative-round.md says.
- Lint (finding 2): unused imports `parsers`, `CONTEXT` removed; test_spec_integration.py import block sorted, unused noqa dropped.
- Finding 3 was dropped by the reviewer; untouched.

## Runs
Suite record at start: 948 passed, 0 failed (with listed expected failures). No red run: a template wording and lint fix, no scenario changed.
Final: `python3 -m pytest -q --work-item w202` -> 145 passed, 1 skipped.
`tools size --limit 300`: no output.

## Tests changed under an allowance
none (imports only in the tests this initiative wrote)

## Open questions
r44 and the scenario still say "in the upstream's terms" and the round's brief/agent/docs still tell the round to word lines in the upstream's glossary terms. The person's answer says r44 is to be retired and replaced (raised as q17); I left that untouched as the scenario still demands it.

Plan contained code: not applicable. Commit: fe844bb3.
