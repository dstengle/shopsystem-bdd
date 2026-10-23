# Plan of w116: design-model-check#r27

## 1. What goes green

design-model-check#r27, four scenarios in features/design-model-check.feature (notes part 1):

- **Outline "a malformed work directory or work file is a file problem"**: 8 of 9 rows pass already. The row "the part p1.md has the kind capability-proposal and the status built" is red: the `malformed_work` step in tests/scenarios/design_model_check_problems.py has no branch for it, so its assertion fails. The code is right already: the work-item lifecycle table in scripts/model_work.py (STATUSES) has no `built` for a capability-proposal, and a probe shows the file problem.
- **"a work-item accepting a requirement no scenario names is a file problem"**: passes today. It stays green.
- **"a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem"**: red twice over. Its Given "a capability thing in the guarantees group with requirement r2 that no scenario names" has no step (StepDefinitionNotFoundError). The code is also wrong: the work-item branch of `read_part` in scripts/model_work.py reports every unnamed accepted requirement and never reads the capability's group (defect D1).
- **"a green work-item accepting a retired id is no file problem"**: red twice over. The Givens "a capability thing whose frontmatter lists r2 as retired" and "a work-item in .shop/work/i1/w1.md with status green that accepts thing#r2" have no steps. The code is also wrong: the same branch never tests retired ids or the status `green` (defect D2).

The work-item retires no deprecated scenarios.

## 2. Where the change lands

- scripts/model_work.py: in the work-item branch of `read_part`, the "accepts …, which no scenario names yet" file problem is no longer raised for a requirement of a guarantees capability, or for a retired id of the capability when the work-item is `green`. The withdrawn exemption stays as it is.
- scripts/model.lp: the `closed` rule for a capability-proposal stops naming built, delivered, ruled, green and refused (decision 3).
- tests/scenarios/design_model_check_given.py: new Given steps: a guarantees capability `thing` with r2 unnamed; a capability `thing` whose frontmatter lists r2 as retired; a work-item at .shop/work/i1/w1.md with a given status that accepts a reference.
- tests/scenarios/design_model_check_problems.py: a `malformed_work` branch for the capability-proposal with status `built` case. The file is 289 lines; keep the branch within the 11 lines of room left, or move steps into a new concern module (and a row in CLAUDE.md's module map) if it would pass 300.

Read but not changed: scripts/model_facts.py (it already writes the capability's group fact and reads the retired set), scripts/model_check.py, scripts/model_parse.py, scripts/model, tests/scripts/test_model_withdrawn.py, tests/scripts/test_work_items.py, tests/scripts/test_model.py.

The researcher listed two files that this plan drops: scripts/work_items.py and scripts/supervise_brief.py. Decision 4 explains why.

## 3. Decisions

1. **The guarantees exemption is decided by the group of the accepted requirement's own capability.** This is read from the group fact the facts reader already writes, not from the work-item's `under`. Rests on design-model-check#r27 ("accepts a requirement of a capability that is not guarantees"). If the capability has not been read when the work directory is read, the implementer orders the reading so it has been. Nothing observable changes because of this.
2. **The retired exemption needs both conditions: the work-item's status is exactly `green`, and the id is in its capability's retired list.** A drafted (or other non-green, non-withdrawn) work-item that accepts a retired id still gets the file problem. A green work-item that accepts an unnamed live id still gets it too. Rests on design-model-check#r27 ("other than a retired id the work-item accepts while `green`") and design-decision/retired-ids-in-capability-frontmatter.
3. **model.lp knows only a capability-proposal's real statuses.** The proposal `closed` rule names built, delivered, ruled, green and refused, and none of them is in the capability-proposal lifecycle (drafted, approved, merged, formulated, withdrawn). It is removed. `formulated` and `withdrawn` stay closed through their own rules, as design-model-check#r36 wants. `merged` stays not closed for a proposal, as the FIX note says. The non-proposal `closed` rule is left alone: the work-item names only the capability-proposal's statuses, and other part kinds keep their lists. This rests on design-model-check#r27 (the work-item's statement of its built row), r36, and design-decision/work-file-forms. The narrator sees no difference, because a proposal in any removed status is already a file problem and exits 1.
4. **`work run --work-item` stays as it is.** The researcher found that `work run --work-item` refuses a work-item when the work-item accepts only guarantees requirements. Nothing changes here: scripts/work_items.py and scripts/supervise_brief.py are not touched. That refusal belongs to another capability (`work run`'s scoping), which w116 does not accept. r27 only settles what `model check` prints, and none of the four scenarios runs `work run`. The case is listed under part 5 for the coordinator.
5. **The `accepts` fact is written as it is today.** The exempted paths add no new `accepts` fact. Today the fact pairs a work-item with a scenario, so there is nothing to write when no scenario names the requirement. The scenarios for r106 ("accepting a requirement no scenario names yet, with no check, is not v_w4") belong to another work-item. w116's scenarios assert only the absence of a file problem naming w1.md, so a `v_w4` warning in these setups does not affect them.

## 4. Tests the decisions break

None. Checked from the notes (part 4), and re-checked against the decisions above:
- tests/scripts/test_model_withdrawn.py (service group; drafted gives 1 file problem, withdrawn gives 0) is unaffected: it is neither guarantees nor retired (decisions 1 and 2).
- tests/scripts/test_work_items.py is unaffected: work_items.py does not change (decision 4).
- tests/scenarios/design_model_check_problems.py, around the drafted work-item that accepts thing#r2 with no scenario, still gets the file problem (decision 2).
- tests/scripts/test_model_reading.py (v15c) and the one-each FIELDS are untouched.
- No test names built, delivered, ruled or refused for a proposal (decision 3).
- No test asserts "no scenario names yet" for a guarantees or a green retired case.

The full suite has not been run. The implementer runs it.

## 5. Open cases

The scenarios do not cover these. The implementer names them and does not choose an answer:
- A work-item that accepts a requirement its capability does not have (defect D3). Today this is the "no scenario names yet" file problem, not an unresolved reference, and the spec does not say which it should be.
- `work run --work-item` refuses a work-item that accepts only guarantees requirements ("accepts none of the scenarios it collected"). This belongs to `work run`'s own requirements, for the coordinator to decide.
- A guarantees or green-retired accepting work-item with no `check` gets `v_w4` today (defect D4). That is r106's work, not this item's.
- A guarantees requirement that a scenario does name: the existing path still writes its `accepts` fact. Whether the exemption should also apply there is not covered.
