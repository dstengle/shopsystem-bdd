# w228 research: supervision#r173

Method: `tools map` absent (no coverage map; not made). `tools tests-of` and `tools refs` used where a name fits; the rest by search.

## 1. Why the scenario is red today

Run (`run`): `python3 -m pytest -q --work-item w228 -k "approve or gate or r173"`. Result: 1 failed, 1 passed.
- Failing: `features/supervision.feature:1837` (r173, glossary gate with no question).
- Error (`run`): `StepDefinitionNotFoundError` for Then `one question was written for g1, asking the person to approve the terms "ledger", "shelf" and "loan"`.
- Missing: a Then step definition in `tests/scenarios/` for that wording. No step matches it (search).
- Code: `scripts/supervise_rounds.py` `run_round`, lines 158-161 (`read`), writes the capability wording "Are the lines of g1 approved as drafted?" for any gate with no question. It does not name the glossary terms. The r173 wording is not produced for g1, so the step would fail even if defined.
- Given steps exist: `g1 is drafted` (`supervision_proposal_steps.py:169`), `gate round's result gives no question` (`supervision_rounds_steps.py:66`), `a round of the kind gate was started for g1` (`supervision_rounds_steps.py:97`).
- The passing test in the run was the r117 capability scenario (name matches `gate`).

## 2. Old assumptions

Requirement r173 adds a glossary branch to the no-question default, which is written for capabilities only.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:run_round, lines 158-161 | a gate with no question gets "Are the lines of <name> approved as drafted?" for every kind of proposal | for a glossary-proposal (`supervise_glossary.statuses` names it), ask for approval of the terms its adds, changes and removes name | r117 capability scenario (p1), `supervision_rounds_steps.py` questions_hold_approval; g1 path only by the r173 scenario, red at its Then | search |
| scripts/supervise_brief.py:76-77 (gate brief) | gate brief asks for questions only, one string each | no change: the gate brief already covers r164 | `supervision_proposal_steps.py:179` (g1 gate brief scenario) | search |
| scripts/supervise.py:move, lines 113-117 | writes each question under `## Questions` | no change; it writes the new question as any other | r117 and r85 scenarios | search |

## 3. Tests the requirement makes impossible to keep

`tools tests-of` could not run (no map). Searched by text (`by search`).
- `tests/scenarios/supervision_rounds_steps.py:questions_hold_approval` asserts "approv", "p1" and "as drafted" for p1. It is sound: the capability branch is unchanged. Kept.
- The r117 feature scenario (`features/supervision.feature:1828`) is sound for the same reason.
- No test asserts that a glossary gate with no question writes the lines wording. Searched `approved as drafted`, `gives no question`, `ends with no question`: only the p1 scenario and the r173 scenario match.
- Result: none that cannot pass as is.

## 4. The file set

- `scripts/supervise_rounds.py` (274 lines, room 26): in `run_round`, lines 158-161, for a glossary-proposal write the terms question instead of the lines question.
- `scripts/supervise_glossary.py` (103 lines, room 197): new helper building the terms question from the proposal's `adds`, `changes`, `removes` (ids `term/<term>`, as `withheld` reads them).
- `tests/scenarios/supervision_proposal_steps.py` (195 lines, room 105): new Then for g1's gate question, beside the g1 gate-brief Then at line 179. (Alternative: `supervision_rounds_steps.py`, 274 lines, room 26.)

Modules on the change's path, edited or not:
- `scripts/supervise.py`: 295 lines, room 5. `move` writes the question; unchanged.
- `scripts/workqueue.py`: 294 lines, room 6. `frontmatter` reads the proposal; unchanged.
- `scripts/supervise_brief.py`: 216 lines, room 84. Gate brief; unchanged.
- `scripts/supervise_glossary.py`, `scripts/supervise_rounds.py`: listed above.

Size limit: 300 (`CLAUDE.md`). `tools size --limit 300` printed no file over it.
