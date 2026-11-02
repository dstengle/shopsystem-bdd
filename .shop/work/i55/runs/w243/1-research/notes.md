# Research of w243 (supervision r184, r185, r186)

Tools: `tools refs` ran (no map needed). `tools tests-of` refused: no map, and I did not make one. Test lists below are **by search**. `refs` missed module-attribute uses (`supervise_outputs.formulated_nothing` at supervise_rounds.py:183, `outputs.missing` at supervise_worker.py:258); those were found by search.

## 1. Why each accepted scenario is red today

Command: `python3 -m pytest -q --work-item w243` (run). Result: 4 failed, 181 passed, 1 skipped. Pytest-bdd stops each scenario at its first undefined step, so later steps are unverified.

- **r184, p1 example** (`features/supervision.feature:2100-2111`): `StepDefinitionNotFoundError` on the Given "i1's capability-proposal p1 is awaiting-answer, its ## Questions section with ... given by its gate round, and its Answers section answering only ... with "Yes."". Existing patterns: supervision_reintegrate_steps.py:46 (no "answering only"), supervision_delegation_steps.py:63 (needs "and no answer"). Code behind: none found (read).
- **r184, w2 example**: `StepDefinitionNotFoundError` on the Given "i1's work-item w2 is awaiting-answer, ... and its Answers section answering only ...". Existing: supervision_delegation_steps.py:90 (needs "each with no answer").
- **r184, Thens not yet reached** (read): "`work run` prints <node> with the question "..."" has no step (test_supervision.py:195 needs "and the question"; supervision_request_steps.py:26 is q2 only). "it prints neither ... nor ... with <node>" does not match test_supervision.py:255 (its `$` anchor forbids "with <node>"). "it exits with an error" exists (test_supervision.py:119).
- **r186** (`:2090-2097`): `StepDefinitionNotFoundError` on Then "a round of the kind integrate was started for p1 after the formulate round **for p1** had ended". Step exists at supervision_reintegrate_steps.py:76 but reads "after the formulate round had ended" (no "for p1"). Givens at :2092-2095 resolve (supervision_formulate_steps.py:21-25 sets `nothing_formulated`). Code behind present (read): supervise_rounds.py:183-186 (formulate nothing: commit, no move), :68-69 and supervise_outputs.py:47-56 (`sent_back` → integrate).
- **r185** (`:2081-2087`): `StepDefinitionNotFoundError` on Then "`work run` wrote no question naming the researcher's file set as missing". Existing similar step: supervision_outputs_steps.py:131 ("...naming a missing output"). Also the Given "the researcher's result gives no question and an empty file set..." matches supervision_outputs_steps.py:23 but the stand-in never gets `fileset: []`: its regex (:37-42) knows "no file set" and "file set of X" only, so the default `scripts/thing.py` (tests/scripts/stub_claude.py:69) is given. Code behind present (read): supervise_outputs.py:17 treats `[]` as given; tests/scripts/test_supervise_outputs.py:1-2 asserts it.

## 2. Old assumptions

No row where production code still treats a researcher's `[]` as missing: the only production check (supervise_outputs.py:17) already exempts `[]`. Rows below are the places that touch the r184/r186 behaviour.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_outputs.py:missing (:17) | `[]` researcher file set is given; no question | r185: keep as is | tests/scripts/test_supervise_outputs.py (its docstring; not run) | search |
| supervision_outputs_steps.py:result_gives (:37-42) | no `[]` branch; default file set given | r185: must give `fileset: []` | scenario r185 only | search |
| supervise_rounds.py:Rounds.route (:68-75) | awaiting/approved sent back → integrate; formulate-from-approved (r116) | r186: already routes to integrate; keep | features r149/r152/r186 (none under pytest) | search |
| supervise_rounds.py:run_round (:183-186) | formulate with `nothing_formulated`: commit, no move | r186, r152: keep; integrate follows | features/supervision.feature:1622 (r152), :2090 (r186) | search |
| supervise_outputs.py:sent_back / formulated_nothing (:41-56) | reads `nothing_formulated` | r186: keep | none executes it directly (refs: 1 production ref) | refs + search |
| supervise_brief.py:NOTHING_FORMULATED (:87-88) and agents/initiative-round.md:40 | tell the session to give `nothing_formulated` | consistent with r186 | none (text) | search |
| supervision_reintegrate_steps.py:76 Then | "after the formulate round had ended" | r186 wording "for p1"; deprecated r149 (features:1619) uses the old wording | scenarios r149 (deprecated), r186 | search |
| supervise.py:Run.show (:254-268) | prints open questions of awaiting-answer nodes; returns 3 | r184: exit with an error; 3 is nonzero | tests/scripts/test_supervise_show.py:29-31 (by search) | search |
| supervise.py:Run.run (:209) | `asked(root, show())` | r184 path | none found separately | read |
| supervise_all.py (:82) | code 3 when a node is awaiting-answer | r184 per initiative only; same exit reading | not checked | read |

## 3. Tests the requirements make impossible to keep

Map absent, so by search: `grep` for `== 3`, `returncode == 3` and "exit 3" in tests. Found only tests/scripts/test_supervise_show.py:29-31 (`== 3` for an awaiting-answer proposal).
- tests/scripts/test_supervise_show.py:29 `test_a_proposal_awaiting_an_answer_..._exits_3`: keeps 3. Sound under reading A (3 is an error exit; the scenario checks `!= 0`). Breaks only under reading B (below).
- Features r149 (deprecated, :1610-1619) and r186 (:2090-2097) share one Then step. A step text fixed to "for p1" breaks r149's line. Any fix must accept both forms.
- Sound on read: features r83 (:1602), r152 (:1622), r153 (:1633). They do not forbid the integrate round r186 starts.
- No test asserts "no integrate round" for p1 after a formulate round. `no round of the kind integrate was started for i1` (supervision_rounds_steps.py:180) concerns i1.
- Conclusion: none of the tests above must change, provided the Then fix accepts both wordings.

## 4. The file set

Production files: none needed on reading. Code for r184, r185, r186 is present (section 1). Reading B for r184 would change this (below).

Test files to change:
- tests/scenarios/supervision_outputs_steps.py (134 lines): parse "an empty file set" into `fileset: []`; add the Then for r185 (or reuse :131 with a pattern).
- tests/scenarios/supervision_reintegrate_steps.py (175): Then :76 accepts optional "for p1" (also keeps r149 passing).
- new tests/scenarios/supervision_awaiting_steps.py (under the existing `tests/scenarios/ | step definitions` row of CLAUDE.md): Givens "answering only ... with ..." for p1 (gate round) and w2; Thens "`work run` prints <node> with the question", "it prints neither ... nor ... with <node>".
- tests/scenarios/test_supervision.py (269 lines, room 31): one import line for the new module.

Module path (line count; room under 300, CLAUDE.md gives the 300 limit; `tools size --limit 300` printed nothing):
- scripts/supervise_outputs.py 103 (room 197)
- scripts/supervise_rounds.py 275 (room 25)
- scripts/supervise.py 295 (room 5)
- scripts/supervise_worker.py 259 (room 41)
- scripts/supervise_all.py 83 (room 217)
- scripts/supervise_brief.py 216 (room 84)
- tests/scenarios/supervision_outputs_steps.py 134 (room 166)
- tests/scenarios/supervision_reintegrate_steps.py 175 (room 125)
- tests/scenarios/supervision_delegation_steps.py 258 (room 42)
- tests/scenarios/test_supervision.py 269 (room 31)

## Readings for the person (not decided here)

- Reading A (used above): "exit with an error" = any nonzero exit; show() returns 3, which stands.
- Reading B: "error" = exit 1. Then show() (supervise.py:268), asked() (:291), supervise_all.py:82 and test_supervise_show.py:31 change.
- Then wording (r186): the feature says "for p1"; the step says no "for p1". Fix the step (accept both) or the feature line. The step must keep the deprecated r149 wording working.
