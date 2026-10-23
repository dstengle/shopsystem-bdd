# Plan of w104: model check's own gaps

Work-item `w104`, under `design-model-check`, accepts r27, r106, r111. It retires nothing and has no rulings. The research notes are at `.shop/work/i23-faster-batches-and-a-clean-model-check/runs/w104/1-research/notes.md`.

## 1. What goes green

- **design-model-check#r111**
  - Scenario: "a bounded context with no job gets no unserved-capability warning".
  - Red today on the test side: the step "a bounded context with one capability and no job" is missing, and so is the Then step "the output does not give w_unserved_cap" (no step has that text).
  - Red today in the code: `w_unserved_cap` in `model.lp` fires for every capability, because `serves/2` is never produced (probe P1, defect D1).
- **design-model-check#r27**
  - "a malformed work directory or work file is a file problem": the row "the part p1.md has the kind capability-proposal and the status built" is red on the test side only. `malformed_work` has no branch for it and falls to its final assert. The code already prints the file problem (P12).
  - "a work-item accepting a requirement no scenario names is a file problem": green today. It stays green and guards the service case (P3).
  - "a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem": red.
    - Steps missing: "a capability thing in the guarantees group with requirement r2 that no scenario names", and the Then step "it prints no file problem naming {named}". Only the wording "it does not print a file problem naming" exists today.
    - Code: `read_part` raises the file problem without checking the capability's group (P2, D2).
  - "a green work-item accepting a retired id is no file problem": red.
    - Steps missing: "a capability thing whose frontmatter lists r2 as retired", and "a work-item in .shop/work/i1/w1.md with status green that accepts thing#r2". The Then step is the one above.
    - Code: `read_part` checks neither whether the id is retired nor whether the work-item is green (P4, D3).
- **design-model-check#r106**
  - "a work-item with no accepts and no check is v_w4, unless it is withdrawn": all 4 rows are green today and stay green.
  - "a work-item accepting a requirement no scenario names yet, with no check, is not v_w4": red.
    - Test side: `FIELDS` in `design_model_check_one_each.py` has no key "accepts thing#r2 and no check", so the step raises a KeyError.
    - Code: `read_part` writes an `accepts` fact only for scenarios that name the requirement. With no such scenario, `has_accepts` is false and `v_w4` fires (P8, D4).

No deprecated scenarios are retired.

## 2. Where the change lands

- `scripts/model_work.py`: the accepts loop in `read_part`.
  - It writes an `accepts` fact for every accepted requirement it resolves (Decision 1).
  - It adds the file problem only when all of these hold: the work-item is not `withdrawn`; no scenario names the requirement; the capability is not guarantees; and the requirement is not a retired id accepted while the work-item is `green` (Decision 2).
  - The file is 211 lines, so there is room for this.
- `scripts/model.lp`: `w_unserved_cap` is guarded on the bounded context having a job node (Decision 3).
- `tests/scenarios/design_model_check_given.py` (228 lines; room 72) gets three new Given steps:
  - the bounded context with one capability and no job;
  - the guarantees capability thing with r2 and no scenario;
  - the capability thing that lists r2 as retired.
- `tests/scenarios/design_model_check_problems.py` (289 lines; room 11) gets one new branch in `malformed_work`: a part of kind capability-proposal with status built. That is two lines, so the file needs no split. The other new steps go elsewhere to keep it under 300.
- `tests/scenarios/design_model_check_then.py` (221 lines; room 79) gets two new Then steps:
  - "the output does not give w_unserved_cap";
  - "it prints no file problem naming {named}", with the same meaning as the existing "does not print" step.

  This file is added to the researcher's set because the problems module has too little room for these steps.
- `tests/scenarios/design_model_check_one_each.py`: a new `FIELDS` entry, "accepts thing#r2 and no check" (accepts `[thing#r2]`, no check).
- The step "a work-item in .shop/work/i1/w1.md with status green that accepts thing#r2" goes in `design_model_check_given.py`, next to the retired-capability step. It builds the same observation, initiative and work item as `work_item_accepting`, with the status green.
- `tests/scripts/test_model_output.py`: the setup of `test_check_ends_with_the_four_counts` changes (part 4).

On the path but not edited: `scripts/model`, `scripts/model_check.py`, `scripts/model_facts.py` (it already holds `caps` with their group, and `retired`), `scripts/work_items.py` and `scripts/supervise_brief.py`.

## 3. Decisions

1. **Which `accepts` fact is written for a requirement**
   - When scenarios name the requirement, `accepts(W, scenario)` is written as today.
   - When no scenario names it, `accepts(W, requirement)` is written instead, using the requirement's id.
   - Why: r106 counts an accept toward `v_w4` whether or not a scenario names the requirement. The capability's Implementation section already says "A work-item's accepts facts are written from its accepts field, whether or not a scenario names the requirement (r106)."
   - `model.lp`'s `has_accepts` and `v_w4` stay as they are. Nothing else in `model.lp` or `scripts/` reads `accepts/2`; I searched for this.
   - This answers the researcher's question 1.
2. **When an accepted requirement no scenario names is a file problem**
   - It is one only when all four hold: the work-item is not `withdrawn`; the capability is known and its group is not guarantees; the id is not in the capability's `retired` list while the work-item's status is `green`; and no scenario names the requirement. This rests on design-model-check#r27, read as written.
   - A retired id accepted by a work-item that is not green stays a file problem (P5, correct under r27).
   - The retired id is read from the ledger, as design-decision `retired-ids-in-capability-frontmatter` says.
3. **The r111 guard is on job nodes, not a fixed silence**
   - `w_unserved_cap` fires only when the context has at least one node of kind job. This rests on design-model-check#r111 ("While the bounded context has no job").
   - Under r19 and the capability's "Not yet" section, no job is ever read today. So the narrator sees no `w_unserved_cap` under either reading, and choosing between them changes nothing the narrator observes.
   - The guard keeps the rule alive for the day jobs are read. This answers the researcher's question 3.
4. **D5: accepting a requirement of a capability that does not exist stays as it is today**
   - It stays a file problem with today's message, and it gets an `accepts` fact like any other resolved accept. It does not become an unresolved reference.
   - Why: r24 does not list `accepts` among the fields it resolves, and r27's file problem covers "a capability that is not guarantees". An unknown capability is not guarantees, so the problem stands.
   - No accepted scenario covers this case. Changing it would change what the narrator observes with nothing to settle it, so the plan keeps today's behaviour. The implementer must make the group lookup tolerate an unknown capability, without raising an error.
   - This answers the researcher's question 2.
5. **The test whose warning r111 removes**
   - `test_check_ends_with_the_four_counts` keeps its expected line, "1 violations, 1 warnings, 1 unresolved references, 1 file problems".
   - Its setup gains one observation that no initiative cites, using the same `observation` helper as `test_exit_codes_of_check`, where that observation alone is one `w_uncited_obs` warning.
   - Why: the test checks that all four counts are printed, so a nonzero warning count is the better check. This decision rests on design-model-check#r111 and on the Implementation section's "ends with the counts". It answers the researcher's question 4.

## 4. Tests the decisions break

- `tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts` is broken by Decision 3: its only warning today is `w_unserved_cap` (P16). Its setup is rewritten as Decision 5 says, and it still asserts the same four-count line.
- I checked the other tests the notes name. The notes found each one sound, and none of my decisions changes that:
  - `test_exit_codes_of_check` uses the `w_uncited_obs` warning, not `w_unserved_cap`.
  - `test_model_withdrawn.py`'s r27 test: its capability is a service capability with no retired ids. Drafted still gives one problem and withdrawn none.
  - `test_work_items.py`: the plugin is not edited.
  - The service-case r27 scenario.
- Decision 1 adds `accepts` facts with requirement ids. No test asserts the `accepts(` facts; I checked by search.

## 5. Open cases

These are for the implementer to name, not to choose:

- `pytest --work-item` refuses a run for a work-item that accepts only requirements no scenario names (rc 3, "accepts none of the scenarios it collected"). The same goes for a green work-item whose only accept is a retired id. `model check` will now pass such a work-item through `v_w4` while its test step cannot run. No scenario of r27 or r106 speaks to this.
- `supervise_brief.accepted_scenarios` gives no "Accepted scenarios" line for an accept that no scenario names.
- A range such as `thing#r1-r2` on a guarantees capability, where some ids are named and some are not (P13). Decision 2 applies to each id, but no scenario covers it.
- Two capabilities and no job: the same rule applies, but it was not probed.
