# plan of w196

Work-item `.shop/work/i35/w196.md`, under `supervision`, accepts supervision#r73, supervision#r123, supervision#r124. Built from the notes at `.shop/work/i35/runs/w196/1-research/notes.md`.

## 1. What goes green

- **supervision#r73**
  - "a work-item lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement it accepts" (line 1041). Red today: the Givens at 1045 and 1046 have no step definition (only the `tagged @deprecated and @rN, the scenario ...` shape exists), and neither does the Then at 1049 (it has a different "neither …, … nor …" wording). Once the steps exist the behaviour is still wrong. `Drafts.retires` matches a deprecated scenario by its own tag, so probe a returns `it used to answer` and leaves out `it used to wait` (D1).
  - "a work-item that accepts a range lists under its Retires each deprecated scenario whose Deprecated for line names a scenario of a requirement in the range" (line 1052). Red for the same reasons (undefined steps at 1056, 1057, 1060; matched by own tag).
- **supervision#r123**: "when every work-item is green or withdrawn, one work-item is drafted retiring each deprecated scenario whose replacement's work-item is green" (line 1063). Red today: its Givens at 1065 to 1070 and its Then at 1073 have no step definitions, and no retire drafting exists anywhere (`Run.draft()` only calls `draft_proposals`).
- **supervision#r124**: "the work-item retiring deprecated scenarios is drafted before the branch review starts and before measure initiative runs" (line 1076). Red today: the Given at 1078 (its wording differs from `green_and_withdrawn`), the Given at 1079 and the Thens at 1082 and 1083 have no step definitions, and the drafting code is missing, as for r123.
- **Retired** (the work-item's Retires): the two deprecated r73 scenarios at lines 1021 and 1031, "… lists under its Retires each deprecated scenario of a requirement it accepts (deprecated)" and "… whose changes name a range … (deprecated)". Both pass today, by tag. The implementer removes them with `features retire`.

## 2. Where the change lands

- `scripts/supervise_draft.py`:
  - `retires` is rewritten to follow each deprecated scenario's `Deprecated for:` line to its replacement and to list each deprecated scenario once.
  - A new function for r123 drafts the retire work-item and guards against drafting it twice.
  - The module docstring names r123.
- `scripts/supervise.py`: `pull_through` calls the retire drafting after the pull and before the branch-review check, pushes what it drafted, and pulls again (r124, r38).
- `scripts/workqueue.py`: the `## Retires` line that `add` writes takes the capability and tag from each entry, not from the work-item's `under`. This is a one-expression change at line 103, and the file stays at 294 lines. It is added to the researcher's set by decision 3.
- `features/supervision.feature`: the two retired scenarios are removed with `features retire`.
- `tests/scenarios/supervision_proposal_steps.py`:
  - `thing_feature_deprecated` and `retires_listed` are removed. Their only scenarios are the retired ones.
  - The `drafted` helper is unchanged.
- `tests/scenarios/supervision_retire_steps.py` (new, under 300 lines): the steps of 1041, 1052, 1063 and 1076.
  - The Givens that write a scenario with `Deprecated for:` (with and without an @r tag, in thing and other).
  - The work-item Givens of 1065 to 1067 and 1078.
  - The Thens of 1049/1060, 1073, 1082 and 1083.
- `tests/scenarios/test_supervision.py`: one import line for the new module.

Removed from the researcher's set:
- `tests/scenarios/supervision_given.py`. It has only 35 lines of room, so the new steps go to the new module.
- `tests/scenarios/supervision_analysis_steps.py`. The r124 Thens go to the new module, and `nothing_drafted` is kept as it is (part 4).

## 3. Decisions

1. **How r73 links a deprecated scenario to a requirement**
   - A deprecated scenario is listed when the scenario that its `Deprecated for:` line names, found by title in any feature file, carries the @r tag of a requirement the work-item accepts. That requirement is the capability of the replacement's feature file plus the tag, with ranges expanded.
   - The deprecated scenario's own tags count for nothing.
   - A deprecated scenario with no `Deprecated for:` line is listed by no work-item.
   - The reading reuses what `features_report.deprecated_entry` already resolves (probe d).
   - Rests on supervision#r73.
2. **Each deprecated scenario is listed once**, however many of its replacement's tags are accepted (fixes D2). Rests on supervision#r73 ("each deprecated scenario").
3. **What a Retires line names in its parentheses**: the requirement through which the scenario is retired. That is the capability of the replacement's feature file and the first replacement tag that is accepted (r73) or that has a green work-item (r123). It is no longer the drafted work-item's `under`.
   - Reason: a retire work-item under r123 can span capabilities. In 1063 it is under `other` and retires a scenario of `thing`.
   - The agents read only the titles (notes part 3), so nothing downstream changes.
   - Rests on supervision#r73 and supervision#r123.
4. **When a replacement's work-item counts as green**
   - A replacement's work-items are the work-items, of any initiative, that are not withdrawn and that accept the replacement's requirement (ranges expanded).
   - The replacement counts as green when it has at least one such work-item and every one of them is green.
   - A requirement that a later work-item is still changing therefore holds its deprecated scenarios back.
   - Rests on supervision#r123 ("of any initiative") and design-decision/work-item-lifecycle-as-run.
5. **What the retire work-item is**
   - It is drafted with `workqueue.add` in the initiative being run (r124: "work of the initiative"; 1073: "drafted in i1").
   - `part_of`, `under` and `accepts` are copied from the last-drafted of the green replacements' work-items. "Last-drafted" means the highest work-item number, since `add` numbers across the whole store. This mirrors the r74 fix work-item in `fix_work_item`.
   - The title names the retiring of deprecated scenarios and the initiative.
   - The Retires section lists each deprecated scenario whose replacement is green (decision 4).
   - Rests on supervision#r123 and supervision#r74.
6. **Guard against drafting again**
   - A deprecated scenario that is already listed under the `## Retires` of any non-withdrawn work-item, in any initiative, is not drafted again.
   - When no deprecated scenario is left after this guard, nothing is drafted.
   - Why the guard is needed:
     - It keeps r73's accepting work-item and the r123 work-item from overlapping (in 1041 the accepting work-item already lists `it used to wait`).
     - It stops a second initiative from retiring the same scenario.
     - It stops the run from looping: a green retire work-item whose scenario is still in `features/` must not be drafted again.
   - Rests on supervision#r123 ("one work-item") and supervision#r111.
7. **Where the drafting happens in the run**
   - In `pull_through`, once the pull has left every work-item green or withdrawn, the retire drafting runs before the branch-review check and before `measure initiative`.
   - If it drafted, `work run` pushes and pulls again, so the new work-item goes through research to review in the same run.
   - The branch review then starts only when that work-item is green.
   - It does not run inside `Run.draft()`, which runs before the pull and would miss work-items that turn green in the same run.
   - Rests on supervision#r124, supervision#r111 and supervision#r38.
8. **A refusal from `workqueue.add` on this path** (a `done` or `abandoned` initiative) reaches the run's exit the same way as on the `draft_proposals` path, and is not caught separately. Rests on design-decision/exits-are-successful-or-errors.

## 4. Tests the decisions break

- `features/supervision.feature` lines 1021 and 1031, through `thing_feature_deprecated` and `retires_listed` in `tests/scenarios/supervision_proposal_steps.py`. They pass today and would fail under decision 1, because their Given writes no `Deprecated for:` line. They are the work-item's Retires, so they are **removed** with `features retire`, and both step definitions go with them (no other scenario uses them, checked by grep for `tagged @deprecated` in `features/`).
- Kept, verified from the notes and by reading:
  - `two_drafted` (1017): no deprecated scenario, so `retires` returns nothing and no retire work-item is drafted.
  - `nothing_drafted` (1099, r121), `fix_drafted` (1091, r74) and `fix_drafted_green` (r110): their fixtures write no deprecated scenario, so no retire work-item is drafted and their counts of `work add: i1/wN drafted` commits hold.
  - The implementer confirms these by running them.
- No test in `tests/scripts/` names `retires`, `Drafts` or `supervise_draft` (notes part 4).
- Callers of the Retires line in `workqueue.add` (decision 3): its only caller is `supervise_draft`, since `work add` passes no retires. No test asserts the parenthesis text; 1017, 1021 and 1031 check titles only.

## 5. Open cases

- A `Deprecated for:` line whose title matches no scenario, or a scenario in two feature files.
- A deprecated scenario whose title is in two feature files, which `features retire` refuses (notes part 3). A cross-capability retire work-item can hit this.
- A replacement with several @r tags, where some are accepted or green and some are not.
- A retire work-item whose replacements' last-drafted work-item belongs to another initiative. Its `part_of` then names that initiative's proposal.
- A deprecated scenario whose replacement is itself deprecated.
