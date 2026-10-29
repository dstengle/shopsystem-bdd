# w231 plan: supervision r187

## 1. What goes green

- **supervision#r187**, scenario (features/supervision.feature:1518): "an integrate round started for a capability-proposal whose change list names another capability the initiative holds a capability-proposal for adds the round's ids for that capability to that proposal, keeping the ids it holds".
  Why it is red today (notes part 1, run): it stops with `StepDefinitionNotFoundError` on the Given at line 1523 (p2, for other, awaiting-answer, with its adds, changes and removes). Read but not reached: the Given at line 1525 (an integrate change list on two capabilities) does not match, because the reintegrate step matches only `... on thing`. The Then at line 1528 (p2's three lists) has no definition.
  The production behaviour is already there (notes part 1): `Changes.write_proposals` in `scripts/supervise_change.py` merges a non-own held proposal through `merge_lists` (commit e4e61321). No scenario has run it yet.

The work-item retires nothing and has no rulings.

## 2. Where the change lands

- `tests/scenarios/supervision_merge_steps.py` (new, about 60–80 lines): the three missing steps.
  - a Given for a capability-proposal for a named capability, awaiting-answer, with its adds, changes and removes written in its frontmatter;
  - a Given for the integrate round of p1 whose DONE change list gives ids on more than one capability, split by its "on <capability>" phrases;
  - a Then that reads p2's three lists back from its file.
  It reuses the world helpers and the formulate module's `entry()` where they fit.
- `tests/scenarios/test_supervision.py`: one star-import of the new module, next to the other step modules. Steps reach the scenarios only through these imports (lines 25–48). The researcher's set left this file out. It has 268 lines, so room for the line.

No production file is expected to change (notes part 4). If the scenario is still red once the steps exist, and the cause is in `scripts/supervise_change.py` or the integrate branch of `scripts/supervise_rounds.py` (which has only 25 lines of room), the implementer fixes it there and names the file.

## 3. Decisions

- **Steps go in a new module, not in `supervision_reintegrate_steps.py`.** This follows the module-map rule of one `<capability>_*_steps.py` module per concern: merging into another proposal is a separate concern from the own-proposal rewrite (r142/r148). It rests on supervision#r187.
- **The two-capability Given gets its own pattern, ending in "on other".** The existing `... on thing` step stays as it is, so the r142/r148 scenarios that use it do not change. The new pattern must not also match those single-capability lines. Rests on supervision#r187.
- **The Then compares the lists as sets of ids, not in order.** r187 says "add ... keeping the ids it holds" and says nothing about order. Rests on supervision#r187.
- **The p2 Given gives the integrate round a way to reach p2.** The initiative must hold p2 as a capability-proposal for `other` (it argues `other`), so `write_proposals` finds it as a held proposal of that capability. Rests on supervision#r187 ("for which the initiative holds a capability-proposal") and design-decision/worker-results-are-files (the round's change list comes from its result file).

## 4. Tests the decisions break

None. Per the notes (part 3, by search): the unit tests in `tests/scripts/test_supervise_change.py` (lines 26, 44 and 56) already assert the merge, and no step module defines the new phrases. The existing `... on thing` reintegrate step and the p1-only Then in `supervision_formulate_steps.py:87` are left unchanged, so the r142/r148 scenarios keep their steps. The notes did not run those scenarios. The implementer runs them once after adding the module, to confirm no new pattern also matches their lines.

## 5. Open cases

The scenario does not cover these. The implementer names them and does not choose:

- an id the round gives that p2 already holds in the same list (repeated, or kept once);
- an id the round gives in one list that p2 holds in another, e.g. an id in p2's `changes` that the round `removes`;
- whether p2's status (awaiting-answer) or its Questions and Answers change when ids are merged into it;
- a change list naming a capability for which the initiative holds more than one capability-proposal;
- a change list naming a capability the initiative holds no proposal for (the drafting r91/r96 covers that; not this scenario).
