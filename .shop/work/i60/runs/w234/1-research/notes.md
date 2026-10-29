# w234 research: requests r72

Tools: `Scripts` given; `tools refs` used (`by refs`). `tools tests-of` has no map ("no map: make one with tools map"), so test lists are `by search`. Not made: `tools map` runs the suite.

## 1. Why the scenario is red today

Command: `python3 -m pytest -q --work-item w234` (run). Result: 1 failed, 180 passed, 1 skipped, 56 subtests passed.

Scenario: "a session the person gives a delegation for a request writes it, in the same reply, through delegate as the person's words with the date" (features/requests.feature:129, tag @r72).

First failure: `StepDefinitionNotFoundError: Given "q1 holds no delegation"` (feature line 132). By search, the later steps are also undefined:
- When "the person tells a session, on 2026-10-29, that for q1 it may ..." (line 133): no step text matches.
- Then "in its reply to that message the session runs `work delegate`, giving q1 and the delegation ..." (line 134): no step; no harness reads a session's reply.
- Then "when that reply ends, q1's delegation is ..." (line 135): no step; `requests_write_steps.py:48` `its delegation is "{text}"` has a different form (double quotes, no "when that reply ends").

Missing in step definitions: the four steps above, in `tests/scenarios/` (none exists).
Missing in code: `scripts/work` has no `delegate` subcommand (argparse block lines 145-171; dispatch map lines 174-177). `scripts/workqueue_request.py` has no `delegate` function. Read by search: `delegate` appears nowhere in `scripts/`.
The given "a request q1 ... that has no line outcome" is defined (`requests_steps.py:44-49`).

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_request.py:request (130-163) | writes `delegation:` once, JSON-quoted (json.dumps, line 153), at creation only | the same quoting must hold for delegate's writes, or the readers below mis-read it; no change to request needed | none (no test passes `--delegation` to `work`) | by search (grep `--delegation` in tests: none); refs |
| scripts/workqueue_request.py:_with_field (71-73) | replaces an existing `<field>:` line only; a missing field is silently not written | a request with no delegation (q1 in the scenario) needs the line inserted, so delegate cannot reuse `_with_field` as is | by search: `requests_*_steps.py` through turn/outcome/reply, all on fields that exist; none for an absent field | refs (6 refs in 1 production file) |
| scripts/supervise_answers.py:Answers.delegation (37-49) | reads `delegation` at each run; JSON-decodes a quoted value | reads what delegate writes, if delegate quotes it as request does; no change | by search: tests/scripts/test_supervise_answers.py, tests/scenarios/supervision_delegation_steps.py (they write the field directly) | by search |
| scripts/supervise_raise.py (33-45) | calls `self.delegation()` for each raised request | reads the delegation at raise time; no change | by search: tests/scenarios/supervision_raise_steps.py:52-55 (writes the field directly) | by search |
| scripts/work:parser (line 152 `--delegation`, only on `request`) | delegation is an argument of `request` only | a `delegate` subcommand with a request and a delegation is added | none | by search |
| scripts/work:dispatch map (174-177) | no `delegate` key | a `delegate` key is needed | none | by search |
| tests/scenarios/requests_flow_steps.py:14 WORK_COMMANDS | the set of commands of work's request set, without `delegate` | r25 "one set of commands"; a flow scenario using delegate would fail the set check; no current flow uses delegate | requests r25 flow scenario (`each_one_command`) | by search |

Session-level: no skill, agent, CLAUDE.md or README text tells a session to run `work delegate` (search of skills/, agents/, CLAUDE.md, README.md for "delegat": only supervision and delegation-answerer text). Old assumption: none.

## 3. Tests the requirement makes impossible to keep

None found by search. The requests tests that touch delegation (`tests/scenarios/requests_write_steps.py:48-69`: "its delegation is", "the command is refused because the delegation is empty") still hold: the change adds a command and leaves `request` as it is. Also `tests/scenarios/requests_world_steps.py` and `requests_flow_steps.py` do not assert delegation absent. Verified sound: the `work request` delegation tests (r19, r22).

## 4. The file set

Production:
- `scripts/work` (184 lines): add `delegate` subcommand (request, delegation args), its cmd and dispatch key. Found by read; refs.
- `scripts/workqueue_request.py` (235 lines): add `delegate(root, ident, text)`: refuse empty delegation (r67 wording), insert or replace the `delegation:` line (JSON-quoted), commit through `_change` (r66). Found by read; refs of `_with_field`.

Tests:
- `tests/scenarios/requests_write_steps.py` (145 lines) or a new `tests/scenarios/requests_delegate_steps.py`: Given "q1 holds no delegation"; When "the person tells a session, on <date>, that for q1 it may ..."; Thens for the session's reply and the stored delegation. Found by the run and by reading `requests_steps.py`.
- `tests/scenarios/test_requests.py` (11 lines): import the new module if one is made.
- `tests/scenarios/requests_flow_steps.py` (99 lines): WORK_COMMANDS gets `delegate` only if a flow uses it. Not required for r72.

Not changed: `scripts/workqueue.py` (294 lines, room 6; it holds `committed`, `read`, `Refused`; `delegate` needs no change there), `scripts/supervise_answers.py` (147), `scripts/supervise_raise.py` (84).

Modules on the change's path, with lines and room under 300:
- scripts/work: 184, room 116
- scripts/workqueue_request.py: 235, room 65
- scripts/workqueue.py: 294, room 6 (on path, not edited)
- scripts/supervise_answers.py: 147, room 153 (reader, not edited)
- tests/scenarios/requests_write_steps.py: 145, room 155
- tests/scenarios/requests_steps.py: 112, room 188
- tests/scenarios/requests_world_steps.py: 159, room 141 (run_as, the `run` fixture in conftest.py:27, 183 lines, room 117)
- `tools size --limit 300`: printed nothing (no tracked Python file over 300).

## Open for the planner (both readings)

- Dependency: r65-r68, r70, r71 (`work delegate`'s own rules) are accepted by no work-item (search of `.shop/work` for `requests#r65`..`r71`: none). r72 names `work delegate`, so either this item adds the command with r72's scenario only, or a work-item for r65-r71 comes first. This item accepts r72 alone.
- Testability: the Then "in its reply ... the session runs `work delegate`" is a claim about a session's reply, not about code. Reading A: the When runs `work delegate` as the session's stand-in and the Then checks the argv. Reading B: a transcript fixture like `tests/scenarios/batch_measurement_transcripts.py` and the instruction text, which the plugin does not have.
- Delegation's date: the When gives "2026-10-29"; the stored text is `The person, 2026-10-29: "answer any question on line 1"`, which the delegate command stores as given.
