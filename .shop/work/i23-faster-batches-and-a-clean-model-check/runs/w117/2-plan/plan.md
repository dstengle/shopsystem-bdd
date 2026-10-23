# Plan of w117: v_w4 reads a work-item's accepts from its field

## 1. What goes green

`design-model-check#r106` (v_w4: a work-item that is not `withdrawn` has no `accepts` and no `check`).

- Scenario Outline "a work-item with no accepts and no check is v_w4, unless it is withdrawn" (4 rows): green today (notes §1, run: 4 passed); it stays green.
- Scenario "a work-item accepting a requirement no scenario names yet, with no check, is not v_w4": red today at its second Given, a KeyError in the step `work_item_with` of `tests/scenarios/design_model_check_one_each.py`, since `FIELDS` has no entry for "accepts thing#r2 and no check". With that entry it would still be red at the Then: `read_part` in `scripts/model_work.py` writes an `accepts` fact only for the scenarios found naming the accepted requirement, so `has_accepts` in `scripts/model.lp` is false and v_w4 prints w1 (notes §1, probe A).

No deprecated scenarios; the work-item retires nothing.

## 2. Where the change lands

- `scripts/model_work.py`: `read_part` writes one `accepts` fact for each requirement the work-item's `accepts` field names, after expansion and resolution, whether or not a scenario names it. The scenario lookup stays, only to drive the r27 file problem and its exemptions (guarantees, green with a retired id, withdrawn). Nothing else changes there.
- `scripts/model.lp`: the `accepts/2` declaration and `has_accepts` get a FIX note saying the second argument is now a requirement, not grammar.md's acceptance-scenario. The `v_w4` rule text stays as it is. This is not a tracked Python file, so the 300-line limit does not apply.
- `tests/scenarios/design_model_check_one_each.py`: a `FIELDS` entry "accepts thing#r2 and no check", accepting `[thing#r2]` with no check. The Given "a capability thing with requirement r2 that no scenario names" is already bound (the r27 scenarios use it, `design_model_check_problems.py`). The implementer checks that it binds here and that it builds a world the Then can read.

This is the researcher's set, with no file added or removed.

## 3. Decisions

1. **What an `accepts` fact holds.** grammar.md gives `accepts(W, S)` with S an acceptance-scenario. A requirement no scenario names has no scenario to put there. So each `accepts` fact becomes `accepts(<work-item>, <requirement id>)`, one for each accepted requirement. It is written from the field, and it replaces the scenario-valued facts; one relation does not mix the two meanings. Rests on r106 and the capability's "Implementation, may change" line: "A work-item's `accepts` facts are written from its `accepts` field, whether or not a scenario names the requirement (r106)". The deviation from grammar.md is recorded the way `model.lp` records the others, as a FIX note (Implementation: "with FIX notes where grammar.md does not compile as written"). In `model check` only v_w4 changes. In `model facts` (r13), a work-item's `accepts` lines name requirements, not scenarios. No requirement or scenario pins those lines (notes §4: no test asserts an `accepts(` line).
2. **The r27 file problem stays.** A drafted work-item that accepts a requirement no scenario names still gets the file problem "accepts …, which no scenario names yet", and `model check` still exits 1. The only change is that v_w4 no longer prints for it. This rests on r27 (feature scenario "a work-item accepting a requirement no scenario names is a file problem" and `tests/scripts/test_model_withdrawn.py`) and on r106. The two do not conflict: one is a file problem, the other a violation.
3. **An accepted requirement no capability has (notes D2).** Under decision 1 such a work-item has an `accepts` fact too, so it is not v_w4. r106 asks only whether the work-item has an `accepts`. The r27 file problem for it is unchanged. Rests on r106.

## 4. Tests the decisions break

None. Verified from the notes §4. The search over `tests/` finds `accepts(`, `has_accepts` and `v_w4` only in `tests/scenarios/design_model_check_one_each.py`, whose Then reads v_w4 rows only. Outline row 3 ("accepts thing#r1 and no check") asserts no v_w4, which still holds when the fact names a requirement. `tests/scripts/test_model_withdrawn.py` and the r27 scenarios (feature lines 309, 317, 325) assert the file problem, which decision 2 keeps. No unit test asserts the second argument of an `accepts` fact.

## 5. Open cases

- The wording of the r27 file problem for an accepted requirement no capability has ("which no scenario names yet", notes D2). The scenarios do not cover it, and r106 does not change it. The implementer names it and leaves it as it is.
- Whether a work-item's `accepts` naming a requirement its capability does not have should be an unresolved reference (r9/r22). No accepted scenario covers it. The implementer names it and does not change it.
- An accepted reference that `resolve_req` refuses gives no fact, as today. Such a work-item with no check would be v_w4. The implementer names it, as no scenario covers it.
- Two entries in one `accepts` field naming the same requirement (for example a range and a single id) give one fact or two: clingo sees one, either way.
