# Plan of w118: no w_unserved_cap while the context has no job

## 1. What goes green

- `design-model-check#r111`: scenario "a bounded context with no job gets no unserved-capability warning" (`features/design-model-check.feature:75`).
  Red today because:
  - its Given "a bounded context with one capability and no job" has no step definition;
  - its Then "the output does not give w_unserved_cap" has no step definition either;
  - once the steps exist, the assertion still fails. `scripts/model.lp:276` warns `w_unserved_cap` for every capability with no `serves` fact, and nothing emits `serves`. So one capability gives `warning w_unserved_cap  a capability serves no job  (1)` (probe A in the notes).
- Retires: none. The work-item has no `Retires` section.

## 2. Where the change lands

- `scripts/model.lp`: the `w_unserved_cap` rule (line 276) holds only when the bounded context has a job, meaning some `node(_, "job")` fact exists. The label fact at line 275 stays as it is. The file is 304 lines, but it is not a tracked `.py`, so the size limit does not apply. Add no lines beyond the gate.
- `tests/scenarios/design_model_check_given.py`: a new Given, "a bounded context with one capability and no job". It builds the same repository as the existing "a bounded context with one capability" step (`world.good()`).
- `tests/scenarios/design_model_check_then.py`: a new parameterised Then, "the output does not give {code}". It asserts the code does not appear in the command's stdout.
- `tests/scripts/test_model_output.py`: change the fixture of `test_check_ends_with_the_four_counts` (section 4).
- `docs/design-model/grammar.md`: line 198, the grammar's copy of the rule, gets the same gate. This keeps grammar.md and `model.lp` in agreement, since `model.lp` is grammar.md in clingo (Implementation section). The change is to docs only.

The researcher's "on the path, unchanged" files stay unchanged: `scripts/model_check.py`, `scripts/model_facts.py`, `scripts/model` and `tests/scenarios/test_design_model_check.py`. No job fact is added: r19 lists no job file among the files `model` reads.

## 3. Decisions

- **D1: the rule is gated on a job, not removed** (`design-model-check#r111`).
  - r111 is worded "While the bounded context has no job". So the literal reading wins: the rule holds only while at least one job node exists, and is otherwise kept as it is. This is the researcher's reading A.
  - The narrator sees the same thing under reading B, which drops the warning outright. Under r19 no job is ever read, so neither reading ever prints `w_unserved_cap` today, and this is no question for the person.
  - Gating keeps the rule correct for the "Not yet" trigger: product-level jobs read when a second bounded context is verified together with this one.
  - Also rests on `design-decision/model-check-solves-with-clingo`: the gate is a clingo condition in `model.lp`, not a filter in Python.
- **D2: the label stays** (`design-model-check#r65`, `#r109`). `model rules` still lists `w_unserved_cap` with its label and kind. The existing unit test that every shown relation has one label stays sound.
- **D3: the new Then is generic over the code** ("the output does not give {code}"), alongside the existing "gives" steps of `design_model_check_then.py`. This is a test-side choice and is not observable by the narrator.

## 4. Tests the decisions break

- `tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts`. Broken by D1.
  - Today its one warning is `w_unserved_cap`: one capability `thing`, no job. After D1 the last line would read `0 warnings`.
  - It is rewritten by changing the fixture, not the assertion. Add an uncited observation (the `observation()` helper that `test_exit_codes_of_check` already uses in the same class), which gives one `w_uncited_obs` warning.
  - The test then still asserts `1 violations, 1 warnings, 1 unresolved references, 1 file problems`. This keeps what it pins: each of the four counts is printed, non-zero.
  - Before relying on it, the implementer confirms that the observation adds no violation, unresolved reference or file problem. In `test_exit_codes_of_check` it exits 0, so it adds none.
- Checked and not broken (from the notes):
  - `test_exit_codes_of_check`: its warning is `w_uncited_obs`.
  - `design_model_check_problems.py:297-300`: an `in` assertion on `w_uncited_obs`.
  - `design_model_check_reading.py:156-168`: the JSON key set is unchanged, and labels cover only printed codes.
  - The `model rules` scenarios in `design_model_check_trace.py`: the label stays (D2).
  - `tests/scripts/test_model.py`: no warning text.

## 5. Open cases

- A bounded context that has a job, where a capability serves none: no scenario covers it, and no job can be read under r19. The gate leaves the warning in place for that case. The implementer names it but does not add a test that fakes a job fact.
- `w_unserved_job` (`model.lp:278`) can never fire, since no job node is emitted (defect D2 in the notes). It is outside r111 and left as it is.
- The repository's own `model check`: its `w_unserved_cap` warnings disappear. The implementer notes the new warning count when running it.
