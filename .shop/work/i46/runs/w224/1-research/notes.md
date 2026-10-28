# Research of w224 (supervision r159, r168)

Method: `tools map` has no map here, so `tests-of` and `untested` could not run ("no map"); every test list below is `by search`. `tools refs` ran for names. `tools size --limit 300` printed nothing: no tracked file is over the limit.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q --work-item w224`. Result: 2 failed, 180 passed, 1 skipped. Both failures are `StepDefinitionNotFoundError` on a Then; the Givens and Whens ran.

- **r159**, features/supervision.feature:1506, "an integrate round that ends with a change list gives one drafted capability-proposal…". Undefined Then at line 1513: "the commit that wrote i1's capability-proposals wrote two, each drafted: one for thing, its adds naming thing#r4, …". The step that exists (tests/scenarios/supervision_integrate_steps.py:140-154, `proposals_written`) requires `thing#r4 and the term "ledger"` and expects `term/ledger` in thing's adds. The accepted text has no ledger term, so the regex does not match. The regex matches the deprecated r92 scenario (features:1474-1482) instead.
- **r168**, features/supervision.feature:1756, "the gate round of a capability-proposal is asked only for the questions on the lines…". Undefined Then at line 1764: "the brief of the gate round for p1 asks only for the questions on thing#r4, thing#r2 and thing#r3". The existing step (tests/scenarios/supervision_proposal_steps.py:140-146, `gate_names_its_ids`) requires `… and the term "ledger"` and `term/ledger` in the brief. Again it matches only the deprecated r104 scenario (features:1706-1715).
- Production code: nothing is missing in scripts/ for either scenario, as far as reading shows (`read`, not exercised by the run). `supervise_change.py:write_proposals` (lines 93-128) writes one proposal per capability and skips glossary entries (line 102). `supervise_brief.py` lines 79-82 list only the proposal's own adds, changes and removes in the gate brief.

## 2. Old assumptions

Old assumption: a capability-proposal's lists may hold glossary terms as `term/<term>` ids. The requirements (r159, r171) move terms to glossary entries.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| tests/scenarios/supervision_integrate_steps.py:entry (32-38) | builds `term/<word>` into a capability's change-list entry from "and the term" text | r159 entries carry ids only; terms go to a glossary entry (r171) | the given of deprecated r92 (features:1479); no map | by search |
| tests/scenarios/supervision_integrate_steps.py:proposals_written (140-154) | expects `term/ledger` in thing's adds; the regex is the deprecated r92 Then | r159's Then has no term; this step must also match the new text | the Then of deprecated r92; no map | by search |
| tests/scenarios/supervision_proposal_steps.py:drafted_with (99-106) | writes `term/` into a drafted proposal's adds when given "and the term" | r168's Given has no term; kept for deprecated r104 | the Given of deprecated r104 (features:1711); no map | by search |
| tests/scenarios/supervision_proposal_steps.py:gate_names_its_ids (140-146) | expects `term/ledger` in the gate brief; the regex is the deprecated r104 Then | r168's Then has no term; must also match the new text | the Then of deprecated r104 (features:1715); no map | by search |
| scripts/supervise_change.py:write_proposals (102) | skips glossary entries, so no term ids enter a proposal | already the new form | the r159 scenario (not executed to its Then) | read |
| scripts/supervise_brief.py:gate (79-82) | gate brief lists the proposal's own lists and asks only on them | already the new form (r168) | none in the run; no map | read |
| scripts/supervise_outputs.py:88 | skips `term/` ids when reading requirement ids | sound for both forms | none; no map | read |

No script or test outside tests/scenarios/supervision_*_steps.py refers to a `term/` id in a capability proposal (`grep term/` over tests/scripts found only model glossary tests).

## 3. Tests the requirements make impossible to keep

- Nothing currently passing becomes impossible. The two deprecated scenarios (r92 at features:1474, r104 at features:1706) still bind the two step regexes above. They remain until a work-item retires them (r123), so they must keep passing.
- Reading A (recommended): add a new step beside each existing one, matching the accepted Then text with no term clause; keep the old regexes for the deprecated scenarios. Both families then pass.
- Reading B: narrow the existing regexes to the new text. This makes the deprecated r92 and r104 Thens undefined and breaks them.
- Verified sound by reading: the Givens of both accepted scenarios bind (the run passed them); `drafted_with` accepts the term-less form; `thing` is present in the Background (tests/scenarios/supervision_given.py:34), so `unknown()` does not drop it.

## 4. The file set

Production: none. Read: no change in scripts/ is needed for r159 or r168.

Test files to change:
- tests/scenarios/supervision_integrate_steps.py: add the r159 Then (no term clause) beside `proposals_written`, expecting thing `adds [thing#r4]`, `changes [thing#r2]`, `removes [thing#r3]`, and other `adds [other#r1]`; keep the old step for r92. Found by: the pytest run and reading lines 140-154.
- tests/scenarios/supervision_proposal_steps.py: add the r168 Then (`thing#r4, thing#r2, thing#r3`, no term) beside `gate_names_its_ids`; keep the old step for r104. Found by: the pytest run and reading lines 140-152.

Module line counts and room under the 300-line limit (CLAUDE.md gives it):
- scripts/supervise_brief.py: 216 lines, room 84
- scripts/supervise_change.py: 128 lines, room 172
- scripts/supervise_rounds.py: 265 lines, room 35 (on the change path, write_proposals called at line 196)
- scripts/supervise_outputs.py: 103 lines, room 197
- scripts/supervise_glossary.py: 27 lines, room 273
- tests/scenarios/supervision_integrate_steps.py: 201 lines, room 99
- tests/scenarios/supervision_proposal_steps.py: 152 lines, room 148
