# plan of w153: measure and analyse only after a branch review that ended DONE with nothing to fix; no analysis kept from a session cut short

## 1. What goes green

- **supervision#r75**
  - "a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run". Red today because its Given ("every worker gives DONE, and the branch reviewer's result gives PARTIAL, with no question and no finding") has no step definition (StepDefinitionNotFoundError). Under that step it would still be red: `lists_nothing` in `scripts/supervise_analysis.py` reads only `questions`, so a PARTIAL review with none counts as nothing to fix (notes §1, probe P1).
  - "when every work-item is green or withdrawn and the kept branch review lists nothing to fix now, `measure initiative` is run on the initiative". It passes today and must keep passing. Its review is DONE with no questions.
- **supervision#r76**
  - "an analyzing-a-batch session that ends at its turn limit leaves no analysis record of the initiative, even though it wrote an analysis file". Red today because its Given ("... the analyzing-a-batch session writes an analysis file of i1 and ends at its turn limit") has no step definition. Under that step it would still be red: `analyse` ignores how the session ended and copies `analysis.md` into `.shop/records/` whatever happened (notes §1, probe P2).
  - "once `measure initiative` has written the initiative's measurement, a session of analyzing-a-batch writes its analysis record". It passes today and must keep passing. The stub's default result is DONE, the session ends with `success` and the analysis file is written.
- Retired scenarios: none. The work-item has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise_analysis.py`:
  - `lists_nothing` also requires that the kept review's result status is DONE (D1).
  - `analyse` takes what the analysis session returns and copies no record when the session was cut short or left no readable result (D2). It reuses the cut-short test from `scripts/supervise_faults.py`, which is an import only.
  - The module docstring and the method docstrings say the new conditions.
- `tests/scenarios/supervision_analysis_steps.py`: the two missing Givens.
  - The PARTIAL branch review: a stub plan where `bdd-branch-reviewer` gives status PARTIAL, no questions and no notes.
  - The analyst at its turn limit: a stub plan where `batch-analyst` writes `analysis.md` and ends with subtype `error_max_turns`.
  - Each binds the scenario's text word for word and follows the existing Givens in that module.

This is the researcher's file set unchanged. Read, no change: `scripts/supervise.py` (the call at l.202 keeps its form), `scripts/supervise_faults.py`, `scripts/supervise_worker.py`, `scripts/supervise_draft.py`, `tests/scripts/stub_claude.py` (its plan keys `status` and `subtype` already cover both cases) and `tests/scenarios/test_supervision.py`. All files stay well under 300 lines (notes §7).

## 3. Decisions

- **D1. A kept branch review "lists nothing to fix now" only when its result is readable, its status is DONE and its `questions` is empty.**
  - Any other status counts as not listing nothing, whether or not it has questions: PARTIAL, NEEDS_CONTEXT, BLOCKED, DONE_WITH_CONCERNS or QUESTION. This takes the notes' reading (a).
  - Rests on:
    - supervision#r75 and its PARTIAL scenario;
    - the work-item's own statement of the fix ("only after a branch review that ended DONE with nothing to fix");
    - design-decision/work-item-lifecycle-as-run (0039), where a reviewer's result other than DONE is never taken as success;
    - supervision#r3, which makes a transition only on DONE.
  - r74's branch at `supervise.py:202` is untouched. It is tested first, so a review of any status that has questions still drafts its fix work-item. The status check applies only to the r75 test.
- **D2. `analyse` keeps the analysis record only when the analysis session was not cut short and left a readable result file.**
  - Cut short means what r45 names: an error, the turn limit, an exit with an error, or output with no JSON result. It is judged by the same test the worker faults use.
  - A missing or malformed `result.json` is a failed stage.
  - Either way, no file is copied into `.shop/records/`, and `work run` says on stderr that the analysis of the initiative was cut short or left no result. That stays a message, not a fault, as today's refusals are.
  - Rests on supervision#r76 and its turn-limit scenario, supervision#r45, and design-decision/worker-results-are-files (0038: "A missing or malformed result is a failed stage").
- **D3. No change to `measure initiative`, to the commit of the measurement or record, or to push verification or logging for the analysis session.** These are notes §5 and defects D3/D4. r75 and r76 do not ask for them, and the work-item names only the two review findings. They are left as they are, not taken here.

## 4. Tests the decisions break

None.

- Checked against the notes' search (§4): every existing branch-reviewer plan in `tests/scenarios` gives DONE.
  - `supervision_review_steps.py` l.24, `supervision_proposal_steps.py` l.47 (DONE with questions, so the r74 branch), `supervision_faults_steps.py` l.170 and `supervision_analysis_steps.py` l.19.
  - So D1 changes no outcome of theirs.
- Checked in `tests/scripts/stub_claude.py` (l.240-254): the stub writes `result.json` with status DONE by default and ends with `success`.
  - So the green scenarios that reach `analyse` with the default stub keep their behaviour under D2. That includes the r76 positive scenario.
  - Those that write no `analysis.md` still print the "wrote no analysis record" message.
- No supervision test asserts on `.shop/records` being clean (notes §4).

## 5. Open cases

Left for the implementer to name in the report, not to choose:

- An analysis session that ends with `success` and a readable result whose status is not DONE (e.g. PARTIAL or NEEDS_CONTEXT) while it wrote `analysis.md`. No scenario covers it, and D2 does not decide it. Today's copy stands for it.
- A second `measure initiative` on the same day is refused (notes D3, P3), so no analysis follows.
- The measurement and analysis record are left uncommitted in the main checkout (notes D4).
- The analysis session has no push verification and no `log.jsonl` lines (notes §5).
