# report of w196

## Budget

- scripts/supervise_draft.py
- scripts/supervise.py
- scripts/workqueue.py
- features/supervision.feature (only `features retire` of the two listed scenarios)
- tests/scenarios/supervision_proposal_steps.py
- tests/scenarios/supervision_retire_steps.py (new)
- tests/scenarios/test_supervision.py

## What changed

- `Drafts.retires(accepts)` follows each deprecated scenario's `Deprecated for:` line to its replacement (any feature file) and lists the scenario once when the replacement carries an accepted requirement's tag (r73). New `Drafts.deprecated()` reads the lines.
- `Drafts.draft_retires()` (r123): one work-item, in the run's initiative, retiring each deprecated scenario whose replacement's non-withdrawn work-items (any initiative) are all green and that no non-withdrawn work-item lists under Retires already. `part_of`, `under`, `accepts` are copied from the highest-numbered of those work-items.
- `Run.pull_through` calls it after the pull when all items are green or withdrawn, before the branch review; it pushes and pulls again (r124).
- `workqueue.add` writes each Retires entry as `(capability @tag)` from the requirement `cap#rN` the entry carries.
- Retired the two r73 `(deprecated)` scenarios with `features retire`; removed their steps `thing_feature_deprecated` and `retires_listed`.
- New `tests/scenarios/supervision_retire_steps.py` with the steps of the four scenarios.

## Red and green

- Suite at the start (brief): 922 passed, 4 failed at 00964b0e; the four were this work-item's scenarios.
- Red: `python3 -m pytest -q -p no:warnings -n 0 --work-item w196` with the steps written, before any code: 4 failed on the Then lines (1041/1052: `- "it used to answer" (thing @r2)` listed; 1063/1076: no retire work-item drafted: `[]`). Expected: old tag-based rule, no retire drafting.
- Green: same command after the code: 148 passed, 1 skipped. Also `--work-item w196 --whole-suite tests/scenarios/test_supervision.py tests/scripts`: 365 passed, 1 skipped.
- 1076's second Then checks the measurement file is newer than the review brief whose `Head:` holds the drafting commit (the measurement is not committed in that scenario, since no analysis record is written).

## Tests changed under an allowance

none (the two steps removed served only the retired scenarios, which the work-item retires).

## Open questions

- A `Deprecated for:` title matching no scenario or several (in two files): the deprecated scenario is left out of every list.
- A replacement with several @r tags: the first accepted (r73) or first green (r123) one is named.
- A deprecated scenario whose title is in two files (`features retire` refuses it).
- A replacement that is itself deprecated.

## Other

- The plan held no code to paste.
- Outside the file set: none. `tools size --limit 300`: no output (no file over).
- Now: `work run` drafts a work-item retiring deprecated scenarios once their replacements are green, before the branch review.
- Commit: 45922c8e.
- Concern: the retire work-item copies `accepts` of a green work-item, so it re-accepts those requirements (plan decision 5).
