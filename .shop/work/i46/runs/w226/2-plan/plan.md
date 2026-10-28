# plan of w226: retire the deprecated scenarios of i46

## 1. What goes green

- supervision#r159: "an integrate round that ends with a change list gives one drafted capability-proposal for each capability it names, with the requirement ids it adds, changes and removes on that capability" (features/supervision.feature:1507). Already green (research: `pytest --work-item w226` gave 183 passed, 0 failed). `Changes.write_proposals` in scripts/supervise_change.py already does it.
- supervision#r168: "the gate round of a capability-proposal is asked only for the questions on the lines that proposal adds, changes or removes" (features/supervision.feature:1757). Already green. The gate-question limit in `brief` in scripts/supervise_brief.py already does it.

Neither scenario is red. The work-item exists only to retire these deprecated scenarios (its `## Retires`):

- the @r77 outline "under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply> (deprecated)" (line 1301 to the end of its Examples, about 1318). It is deprecated for the r163 outline.
- the @r92 scenario "an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability (deprecated)" (lines 1474–1483). It is deprecated for the r159 scenario.
- the @r104 scenario "the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes (deprecated)" (lines 1706–1716). It is deprecated for the r168 scenario.

"Done" means: the three are gone from features/supervision.feature, and the suite, `features bindings --unbound` and `tools check` stay as clean as they are today.

## 2. Where the change lands

- features/supervision.feature: delete the three deprecated scenarios above, each with its tag line, its `Deprecated for:` line and, for the outline, its Examples table. Nothing else in the file changes.

This is the researcher's file set, unchanged. No decision below adds a file. No code changes, because both requirements already hold. Some comments in scripts/ still cite retired ids:
- r92 in supervise_change.py, supervise_rounds.py and supervise_brief.py;
- r104 in supervise_brief.py;
- r77 in supervise_brief.py and supervise_answers.py.

These comments are left alone: this work-item does not need them changed, and leaving them keeps the file set to the claim (design-decision/the-file-set-is-the-claim).

## 3. Decisions

- **D1. Keep Retires bullet 1 (the @r77 outline, research conflict A).** Rests on supervision#r123: once every work-item of the initiative is green or withdrawn, the work-item r123 drafts retires each deprecated scenario whose replacement's work-item is `green`. The replacement is the r163 outline, accepted by w223, which is `green`. r73 covers the drafting of a work-item by its accepted requirements. It does not limit r123's retiring work-item, so its retirement is in scope even though w226 does not accept r163.
- **D2. Leave the @r92 scenario at line 1484 ("the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids (deprecated)", `Deprecated for: removal`) in place (research conflict B).** Rests on supervision#r123 and supervision#r73: both name only deprecated scenarios that have a replacement scenario. A scenario deprecated for removal has none, so neither requirement puts it in this work-item's Retires. The other "removal" scenarios (r3, r5, r16, r77 at 1319, r112, r113) stay for the same reason.
- **D3. The overlap with w224 (research conflict C) changes nothing here.** w224 accepted r159 and r168 and is green. Under supervision#r123, w226 restates those accepted ids only to name the replacements whose deprecated scenarios it retires. It builds nothing a second time.
- **D4. No step definitions are removed.** The work-item asks only for the scenarios to be retired. pytest-bdd does not fail on an unused step. See open case 2.

## 4. Tests the decisions break

None. What was checked (from the research notes):
- The only test the three scenarios have is the one tests/scenarios/test_supervision.py generates through its `scenarios` call on supervision.feature. Deleting a scenario removes its generated test and nothing else.
- No hand-written test names any of the three titles: a search of tests/ found them only in the feature file.
- The "Deprecated for" tests (tests/scripts/test_features_scenarios.py, test_features_deprecating.py) use their own fixtures, not supervision.feature.
- tests/scripts/test_supervise_change.py tests code that does not change.
- tests/scripts/test_bound.py runs `features bindings --unbound` on supervision.feature. Removing scenarios cannot leave a scenario unbound.

## 5. Open cases

1. The outline's exact extent: where its Examples table ends, and whether a blank line or comment between it and the next scenario goes with it. For the implementer to name.
2. If `tools check` (vulture) or `features bindings` reports a step definition in tests/scenarios/supervision_*_steps.py that only the removed scenarios used, the implementer names it, and whether removing it is part of this work.
3. Whether the two @r77 and two @r92 scenarios sharing a tag need anything (they are independent scenarios today). The scenarios do not say. For the implementer to name if a tool objects.
