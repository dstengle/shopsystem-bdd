# Plan of w171 (supervision#r102)

## 1. What goes green

- **supervision#r102**: scenario "an integrate round is given every requirement id another initiative's kept drafts add that spec/ on the branch it starts from does not hold, whatever that initiative's capability-proposal's status" (features/supervision.feature, line 1252).
  - Red today, by run: the first undefined step is "an initiative i2 under .shop/work/, started, whose capability-proposal p2 is formulated". Also undefined: "i2 keeps a draft of thing adding … at <path>", the p3 `drafted` form with "started,", and "i3 keeps a draft of other adding … at <path>".
  - With those steps in place, the Then would still fail. `supervise_drafts.added_by_others` globs only `drafts/spec/capabilities/*.md` under the last `<k>-integrate` stage. Integrate rounds actually keep drafts at `drafts/round-<m>/spec/capabilities/`, so it returns none. The researcher's probe showed this (defect D1). The real kept drafts of i25 and i26 are under `round-1`, so today they are never read.
- The deprecated `@r102` scenario (line 1239, title ending "(deprecated)") passes today and must stay green (part 4).
- Retires: the work-item has no `## Retires` section, so it retires no scenario. This plan retires none either.

## 2. Where the change lands

- `scripts/supervise_drafts.py`: `added_by_others` (and the stage helper it uses, `last_integrate`) read the kept drafts at `<k>-integrate/drafts/round-<m>/spec/capabilities/*.md`, for every round and every integrate stage of each other initiative (decisions 1 and 2). They stop reading the old `drafts/spec/capabilities/` layout (decision 3). The module docstring and the function docstring are updated to match. The ID regex, the dedupe, the exclusion of i1's own initiative and the held check stay as they are.
- `tests/scenarios/supervision_integrate_steps.py`: gets the two new Given steps, each written so that it parses the scenario's own wording:
  - an initiative under `.shop/work/`, started, whose capability-proposal is `<status>`, with no drafts.
  - an initiative that keeps a draft of a capability adding the given ids at the given path.
  The old step "… whose kept drafts add … and whose capability-proposal … for them is …" writes its draft at the round layout (part 4).

Removed from the researcher's set:
- `scripts/supervise_brief.py`: the call at line 76 is unchanged because the signature stays.
- `scripts/workqueue.py`: on the path only; `WORK` is unchanged.
- `tests/scenarios/test_supervision.py`: both r102 scenarios are already bound.
- `features/supervision.feature`: nothing is retired or edited.
- `spec/capabilities/supervision.md`: the planner writes no spec. The difference between "not yet applied" and "spec/ does not hold" is in part 5.

## 3. Decisions

1. **Every round's drafts are read.** Inside an integrate stage, every `round-<m>` directory's capability files are read. The result is the union of their ids, deduplicated as today and in the order found. Rests on supervision#r102 ("every requirement id that the kept drafts of another initiative … add") and on supervision#r91 (each round's drafts are kept). The scenario needs this: i3's only draft is in `round-2`.
2. **Every integrate stage is read, not only the highest-numbered one.** An integrate round that runs again with no writer leaves a later stage with no drafts; the ledger records that this happens. Reading only the last stage would then hide drafts that are still kept, which is the collision r102 exists to prevent. Rests on supervision#r102 ("every requirement id … the kept drafts … add"). `last_integrate` is either replaced by a reader that walks every stage or removed. If it has no other caller (the notes say it has none outside its module), it goes.
3. **The old layout `<k>-integrate/drafts/spec/capabilities/` is no longer read.** No real run writes it; the notes found real drafts only under `round-<m>`. The work-item's title names the round layout as where integrate rounds keep their drafts. Rests on supervision#r91 and r102, and on the work-item's title.
4. **The held check is unchanged.** It still reads `spec/capabilities/<capability>.md` in the checkout `root`, and a capability spec/ does not have holds nothing. The scenario's Given writes and commits thing.md in the repository `work run` runs from, so this is the branch the round starts from. Rests on supervision#r102.

## 4. Tests the decisions break

- `tests/scenarios/test_supervision.py`, the deprecated `@r102` scenario (feature line 1239), through its step `other_initiative` in `tests/scenarios/supervision_integrate_steps.py` (lines 144-154).
  - Broken by decision 3: the step writes its draft at `runs/<name>/1-integrate/drafts/spec/capabilities/<capability>.md`, which is no longer read, so the Then "given thing#r4 and other#r1" would fail.
  - What becomes of it: the step is rewritten to keep its draft where integrate rounds keep them, under a `round-1` directory of an integrate stage. The scenario still asserts the same thing: the round is given thing#r4 and other#r1 and not thing#r1, r2 or r5.
  - Why not remove it: the feature text names no path, the work-item retires nothing, and supervision#r73 retires a scenario only through a work-item's `## Retires`, which this work-item does not have.
- The other tests are kept, checked by the notes' search and by my reading of the step file:
  - `drafts_committed` (lines 79-85, r91) asserts only the keeping, not the reading.
  - The r91 and r92 assertions at lines 96-130 do not touch `supervise_drafts`.
  - `integrate_not_given` (lines 165-169) reads only the brief.
  - No other test names `supervise_drafts` or the brief's sentence on other initiatives' ids.

## 5. Open cases

- Two rounds or stages of one initiative may hold the same capability with different ids, for example when a later round drops an id an earlier one added. Under decision 1 both rounds' ids are given. The scenarios do not cover this; the implementer names the case in a test or in the report.
- r102's text says "not yet applied", while the code and the scenarios check "spec/ does not hold". These differ for an id spec/ holds whose proposal is not applied. No scenario covers it; the implementer names it.
- Drafts that exist only on another initiative's branch and not in the checkout are not read (notes, part 5). No scenario covers this, and it is left as found.
- The new step "an initiative iN under .shop/work/, started, whose capability-proposal pN is <status>" resembles existing patterns in `supervision_all_steps.py` (lines 68 and 90). The implementer makes sure no two step patterns match the same line.
- `tools refs` misses the call `supervise_drafts.added_by_others` (notes, D2). This is noted, not acted on.
