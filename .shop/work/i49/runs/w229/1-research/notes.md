# w229 research: supervision r180

Accepted: supervision#r180 (scenario in features/supervision.feature:1414, test in tests/scenarios/test_supervision.py). No coverage map: `tools tests-of` refused (`no map`), so every test list below is `by search`.

## 1. Why each scenario is red today

Command: `python3 -m pytest -q --work-item w229` (run).
Result: 182 passed, 1 skipped, 56 subtests passed. The r180 scenario ran and passed. Nothing is red today.

Read: the Given (tests/scenarios/supervision_integrate_steps.py:22, calling supervision_rounds_steps.py:155 `proposed_fulfilling`) writes only `initiative.md` (status started) and `q1.md`. It writes no glossary-proposal. So the scenario cannot fail on the glossary clause that r180 adds.

Read: the code already implements r180. scripts/supervise_rounds.py:47-48 (`Rounds.due`) gives the integrate round to a started initiative with `fulfils` and no capability-proposal, no glossary-proposal and no work-item.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:Rounds.due (l.47-48) | started initiative: integrate round when no proposal, no glossary-proposal, no work-item | already r180; no change | r180 and @r93 scenarios in tests/scenarios/test_supervision.py | read, tools refs, by search |
| scripts/supervise_rounds.py:l.48 comment `# r93` | cites the retired r93 | should cite r180 | none | read |
| scripts/supervise_rounds.py:l.1-6 docstring | "started initiative with neither proposal nor work-item" | omits the glossary-proposal clause | none | read |
| scripts/supervise_rounds.py:Rounds.rounds (l.94-104) | loops `due` until none is due | no change; caller of due | none | tools refs (4 refs to due) |
| scripts/supervise_intake.py:due (l.18) | lists open requests; a different `due` | no change; not the same function | none | tools refs, read |
| features/supervision.feature:1406 (@r93 @deprecated) | started, no proposal, no work-item: integrate round | the old form; same outcome when no glossary-proposal | integrate_started, tests/scenarios/supervision_rounds_steps.py:214 (by search) | read |
| tests/scenarios/supervision_done_steps.py:28 (Given) | started, no proposal, no work-item, approved glossary-proposal g1: no integrate round | its wording is the r93 form but it holds a glossary-proposal, which r180 excludes; still gives no round | r161 done scenario, feature:1821 (by search) | read |

## 3. Tests the requirements make impossible to keep

none. The r180 change only adds a clause the code already has. By search, no test expects an integrate round for a started initiative that holds a glossary-proposal. The r93 scenario and the done scenario both pass under r180 unchanged. Not checked: test_supervision.py's other integrate scenarios, by search only.

## 4. The file set

- scripts/supervise_rounds.py: comment and docstring only, r93 to r180 (l.1-6, l.48). Read.
- Read, not changed: scripts/supervise.py (295 lines, room 5; `Run` mixes `Rounds`, `items()` l.71).
- Read, not changed: scripts/supervise_intake.py (118 lines, room 182).
- Read, not changed: scripts/workqueue.py (294 lines, room 6; `items`).
- Read, not changed: scripts/workqueue_request.py (228 lines, room 72; `accepted_lines`).
- Read, not changed: scripts/supervise_glossary.py (115 lines, room 185).
- Test file, not changed: tests/scenarios/supervision_rounds_steps.py (274 lines, room 26; `proposed_fulfilling` writes no glossary-proposal).
- Test file, not changed: tests/scenarios/supervision_integrate_steps.py (252 lines, room 48; the r180 Given at l.22).
- Test file, not changed: tests/scenarios/test_supervision.py (268 lines, room 32).

Size limit: 300 (CLAUDE.md). `tools size --limit 300` printed nothing: no tracked Python file is over it.

Open for the planner, two readings (not a question to the person):
- A: change nothing for r180 except the comment in scripts/supervise_rounds.py.
- B: also make `proposed_fulfilling`'s started case write a glossary-proposal, so the r180 scenario pins the glossary clause. This is a test-design choice.
