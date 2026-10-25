# Report w170

## Budget
scripts/supervise_all.py, scripts/supervise_drafts.py (new), scripts/supervise_brief.py, CLAUDE.md,
tests/scenarios/supervision_intake_steps.py, tests/scenarios/supervision_integrate_steps.py,
tests/scenarios/supervision_proposal_steps.py. (7 files.)

## Changed
- r103: `supervise_all.run_all` runs the Run checks and `Intake.check` (worker marker, detached HEAD, loose changes under
  .shop/work/) before any start, then `workqueue_start.start` for each accepted request no initiative (any status) fulfils,
  then takes the runs, new initiative included.
- r102: new `supervise_drafts.py` (ids of other initiatives' last integrate round drafts that spec/capabilities/<cap>.md in
  the checkout lacks); `integrate_lines` gives them in a line of their own ("none" when empty).
- r104: gate brief lists the proposal's Adds/Changes/Removes and asks for questions on those only; r68 sentence kept.
- CLAUDE.md module-map row for supervise_drafts.py.

## Red and green
Suite at start: 863 passed, 3 failed (the three scenarios of this work-item).
Red, each: `python3 -m pytest -q tests/scenarios/test_supervision.py -k <title words>`: r103 failed on the assertion that
no initiative fulfils q1 (after step definitions written; before them StepDefinitionNotFoundError); r102 failed on
"thing#r4" absent from the integrate brief; r104 failed on "thing#r4" absent from the gate brief. Green after the code.
Final: `python3 -m pytest -q --work-item w170`: 145 passed, 1 skipped. `--whole-suite` on test_supervision.py,
test_work_queue.py, test_requests.py: 271 passed.
`tools size --limit 300`: prints nothing.

## Tests changed under an allowance
none

## Open questions
- Accepted request whose only initiative is abandoned: gets no new start (plan decision 3).
- A request an intake round turns accepted in the same run: started on the next run.
- Order/numbering of several unfulfilled requests: queue order.
- Done/abandoned initiatives' kept drafts count in r102.
- A draft for a capability with no spec file: all its ids count as added.
- Refusal of `work start` inside `work run` (no spec/index.md etc.): raises Refused from run_all, as other refusals.

The plan contained no code; nothing pasted.

## Now possible
`work run` starts the initiative of an accepted request itself; integrate rounds are told ids other drafts took; gate
briefs name only their own proposal's ids.
Surprise: `fulfils` is stored as a full id, so the step matches the last segment.

Files: the 7 above. No concerns.
