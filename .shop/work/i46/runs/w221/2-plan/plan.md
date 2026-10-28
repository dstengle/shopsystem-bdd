# Plan of w221: design-model-check r122, r123, r124

## 1. What goes green

From the research notes (run: `python3 -m pytest -q --work-item w221`, 23 red, 188 passed, 1 skipped).

- **design-model-check#r122**, "a glossary-proposal's list naming a term the glossary lacks is unresolved, unless an approved glossary-proposal removes it" (12 rows, all red). Red because no step matches "a <status> glossary-proposal whose <list> names term/<term>" nor the remover Givens ("no other glossary-proposal", "an approved / awaiting-answer / withdrawn glossary-proposal whose removes names term/shelf"); and in code a glossary-proposal is not a part kind and its `term/` references are never read (`scripts/model_work.py`, `read_part` reads them for capability-proposals only).
- **design-model-check#r123**, "an initiative may be `done` when its glossary-proposal is approved" (1 scenario, red). Red because the Given "under it a glossary-proposal with status approved" has no step, and `closed()` in `scripts/model.lp` does not count `approved`, so `v_d1` would still name the initiative.
- **design-model-check#r124**, "a malformed work directory or work file is a file problem" (18 rows, 10 red). Red at the else branch of the step `malformed_work` (`tests/scenarios/design_model_check_problems.py`), which has no branch for: initiative.md has no status; capability-proposal with status awaiting-answer; glossary-proposal with status drafted, formulated, approved; the five work-item rows (drafted, withdrawn, drafted of a guarantees capability, green accepting a retired id, done accepting a retired id). Of those, the code already does what the initiative-status, awaiting-answer and five work-item rows want; the three glossary-proposal rows need glossary-proposal as a part kind with its own lifecycle.

Retired by this work-item (deprecated scenarios of @r124, removed from `features/design-model-check.feature` with their now-unused steps, if any step is used by no other scenario):
- "a malformed work directory or work file is a file problem (deprecated)"
- "a work-item accepting a requirement no scenario names is a file problem (deprecated)"
- "a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem (deprecated)"
- "a green work-item accepting a retired id is no file problem (deprecated)"
- "a status in its kind's lifecycle is no file problem (deprecated)"

## 2. Where the change lands

- `scripts/model_work.py`: glossary-proposal added as a part kind and given its lifecycle in the status table; a glossary-proposal's `adds`, `changes` and `removes` read for `term/` references; those references judged after all of `.shop/work/` is read, against the glossary and the set of terms any approved glossary-proposal removes (decisions 1, 2, 3).
- `scripts/model.lp`: `approved` counted as closed for a glossary-proposal only (decision 4).
- `tests/scenarios/conftest.py`: a writer of a glossary-proposal part, beside the capability-proposal writer `proposal()`.
- `tests/scenarios/design_model_check_given.py`: the r122 Givens (the glossary-proposal with a status and a list naming a term; the three remover Givens and "no other glossary-proposal"), beside the r66 step.
- `tests/scenarios/design_model_check_trace.py`: the r123 Given "under it a glossary-proposal with status approved".
- `tests/scenarios/design_model_check_problems.py`: the step `malformed_work` moved out (decision 6); the file is 270 lines and the ten new branches would take it near or past 300.
- `tests/scenarios/design_model_check_work.py` (new): the step `malformed_work`, with a branch for each of the 18 r124 rows; the dead branch "a status not in its kind's lifecycle" (its row is deprecated) dropped.
- `tests/scenarios/test_design_model_check.py`: imports the new step module beside the others.
- `features/design-model-check.feature`: the five deprecated scenarios of the Retires section removed.

Not changed: `scripts/model_facts.py` (WORK_KINDS is built from PART_KINDS, so glossary-proposal ids become r121-checked without an edit), `scripts/workqueue_done.py` (decision 5).

## 3. Decisions

1. **The lifecycle of a glossary-proposal is `drafted`, `awaiting-answer`, `approved`, `withdrawn`**, no other. Rests on the glossary's term `status` in `spec/index.md`, which lists exactly these four, and on design-model-check#r124 ("a status ... not in its kind's lifecycle"). It gives the r124 rows: drafted and approved print nothing, formulated is a file problem. Settles the researcher's question 3.
2. **glossary-proposal is a part kind** read like the other parts (id, kind, status, `part_of`), and not entered in the capability-proposals that `model why` and the v15 rules read. Rests on design-model-check#r124 ("`glossary-proposal` being one") and decision 0073 (`design-decision/the-glossary-is-a-target-of-spec-work`), where it is a proposal of terms, not of requirements.
3. **An approved glossary-proposal's `removes` excuses the term wherever in the bounded context a glossary-proposal names it**, whatever initiative either is under; an approved glossary-proposal's own `removes` is excused by the same rule (the row "approved, removes, shelf"). An awaiting-answer or withdrawn remover excuses nothing, and a glossary-proposal's `adds` or `changes` of a missing term is unresolved whatever its own status. Rests on design-model-check#r122, which names "an `approved` glossary-proposal" with no scope, its scenario's description ("excused wherever a glossary-proposal names it, a drafted one included"), and the capability's Purpose (`model check` verifies one bounded context). Because a remover may sort after the proposal it excuses, the excusing set is gathered over all of `.shop/work/` before any glossary-proposal term reference is judged. Settles the researcher's question 1.
4. **`approved` closes a glossary-proposal and no other kind.** An approved capability-proposal stays open. Rests on design-model-check#r123 (glossary-proposal) and design-model-check#r36 (only `formulated` and `withdrawn` close a capability-proposal). `v_d1` and `v_d2` follow from `closed()` with no edit of their own; a drafted or awaiting-answer glossary-proposal still blocks `done`.
5. **The work queue's own `done` condition (`scripts/workqueue_done.py`) is not touched.** r123 is model check's rule; the queue's is work-queue's capability, outside this work-item's `under:`. Settles the researcher's question 2 for this work-item; the difference stays (see open cases).
6. **The r124 step moves to a new step module**, so that `design_model_check_problems.py` keeps under the 300-line limit. Rests on CLAUDE.md's size limit and module map (one step module a concern in `tests/scenarios/`).

## 4. Tests the decisions break

None. Verified from the notes and by search:
- `tests/scripts/test_model_glossary.py` (r66 rows, capability-proposal terms): unchanged; decision 3 reads only glossary-proposals and leaves the capability-proposal excuse as it is.
- `tests/scripts/test_workqueue_done.py`: unchanged by decision 5.
- `tests/scripts/test_model_reading.py:56` asserts only that `failed` is a work-item status; untouched by decision 1.
- No test asserts the text of the "needs an id and a kind among ..." problem, whose kind list grows by one (searched `tests/` for it and for `is not one of`).
- The `v_d1`/`v_d2` rows of `design_model_check_trace.py` and `design_model_check_glossary.py` use capability-proposals and work-items, whose closing decision 4 leaves as it is.
- The deprecated @r124 scenarios are retired by the work-item, not broken.

## 5. Open cases

- A glossary-proposal whose `adds`, `changes` or `removes` names something other than `term/<term>` (a requirement reference): the scenarios are silent; the implementer names what model check does with it.
- Whether an approved glossary-proposal's `removes` also excuses a capability-proposal's `term/` reference (r66), or a merged/formulated capability-proposal's `removes` a glossary-proposal's: neither r66 nor r122 says; this plan changes neither.
- A drafted or awaiting-answer glossary-proposal under a `done` initiative: model check names it (`v_d1`), while `work status`/the queue's done condition ignores glossary-proposals; a follow-up for work-queue, not for this work-item.
- A glossary-proposal with an `argues`: the scenarios are silent on whether it is read or refused.
