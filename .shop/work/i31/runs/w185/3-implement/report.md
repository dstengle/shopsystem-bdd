# w185 implementation report

## Budget

1. scripts/supervise_rounds.py
2. scripts/supervise_change.py
3. scripts/supervise.py
4. features/supervision.feature (retire only)
5. tests/scenarios/supervision_rounds_steps.py
6. tests/scenarios/supervision_formulate_steps.py (new)
7. tests/scenarios/supervision_done_steps.py
8. tests/scenarios/test_supervision.py
9. CLAUDE.md (a row, if judged needed)

Suite at the start (brief): 888 passed, 10 failed at 81b7d67e; the 10 failing are w185's scenarios.

## Outside the file set

- tests/scripts/stub_claude.py: its result JSON now carries `usage` (input_tokens, output_tokens). Without it `measure initiative` refuses the stand-in's session.json for w1's implement stage and r111's initiative is never set done. Committed (c0b69237).

## What I did

- r111 (c0b69237): Given "i1 is started and its work-item w1 is ready" and the Then "i1's transition to done was made after w1's transition to green…" added in supervision_done_steps.py. Red run: Then assertion failed, `green` was found but `done` empty, stderr "`measure initiative i1` was refused … no usage with input and output tokens". After the stub change, passes with no change in scripts/.
- r70 stays green (run).
- r116 (159c7530): widened `apply_started` to `apply|formulate` and `answered_proposal` to read "its adds naming …" and "given by its gate/formulate round" (writes that round's move into awaiting-answer to log.jsonl; setup only).

## Stop: HAND-BACK on supervision#r116

Stop condition: a scenario can't be made to fail on its Then line, only on an undefined step.

Run: `python3 -m pytest -q -n 0 -k every_question_from_its_formulate_round` after only the Then step was defined (widened): `1 passed`. No production code was changed.

Why: today's code sends the answered proposal to an apply round, then (every round ends) approved, then a formulate round, whose brief carries the answer. The Then says only "a round of the kind formulate was started for p1, given the answer "One place."", which that chain satisfies. The scenario does not assert that no apply round started, so the code defect the plan names (D2, apply instead of formulate) is not observable by its Then.

The ruling needed: either the scenario gets a Then (or a line) saying no apply round is started / the formulate round is the first round started, or r116 is accepted as already met by this chain and D1 is dropped.

Green: r111, r70 (and r80, r71 unchanged). Red / not started: r116 (passes, stopped), r114, r83, r112, r113, r115. Retire of the @r83 @deprecated scenario not done.

## Tests changed under an allowance

- tests/scenarios/supervision_rounds_steps.py `answered_proposal` (setup): the regex takes an optional "its adds naming …" and writes the log move for "given by its … round"; no assert changed.

## Open questions

none beyond the ruling above.

Plan contained no code. Suite at start: 888 passed, 10 failed (w185's scenarios). Final work-item run: not repeated; see above. Size check printed no file.
