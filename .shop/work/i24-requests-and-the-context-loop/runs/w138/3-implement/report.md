# w138 implement report

## Budget

scripts/supervise_draft.py (new), scripts/supervise.py, scripts/supervise_review.py, scripts/workqueue.py, CLAUDE.md,
tests/scenarios/supervision_proposal_steps.py (new), tests/scenarios/test_supervision.py. (supervision_review_steps.py not touched.)

## Suite at the start
Brief's record: 774 passed, 3 failed at 7a341cf; the 3 failing included this work-item's three scenarios (plus listed expected failures of other items).

## What changed
- `scripts/supervise_draft.py` (new, row added to CLAUDE.md): `Drafts`, a part of `Run`. `draft_proposals` drafts one work-item per capability of each formulated proposal (adds + changes, grouped by capability, `part_of` the proposal's id), skipping a capability that already has a work-item of that proposal; `retires` reads deprecated scenarios from `features/<cap>.feature` by their own `@r` tags; `fix_work_item` reads the kept review's `result.json` `questions`, and drafts one work-item (part_of/under/accepts from the first work-item the lines name, `findings:` the kept `findings.md`), once per kept review.
- `scripts/workqueue.py` `add`: keyword params `retires`, `findings` (writes `## Retires` bullets and `findings:`).
- `scripts/supervise.py` `Run.run`: drafts first, pulls, reviews; after a review that yields a fix work-item it pushes and pulls again (no second review in the same run, so a reviewer that lists findings every time cannot loop). `draft` pushes after drafting.
- `scripts/supervise_review.py`: `branch_review` returns the kept directory (None if none due).
- `tests/scenarios/supervision_proposal_steps.py` (new) + one import in `test_supervision.py`: the Givens and Thens of the three scenarios.

## Red and green
- Red: `python3 -m pytest -q -p no:warnings -n 0 --work-item w138` -> 3 failed (r72, r74 on their Then assertion `AssertionError: ([], '')` — nothing drafted; r73 on its undefined three-scenario Given, then the same Then). Expected: no drafting code existed. (I wrote the drafting module before the red run but had not wired it into `Run`, so the run was still red for the right reason.)
- Green: same command -> `145 passed, 1 skipped, 687 deselected`. Test modules touched (test_supervision, test_work_queue, test_work_item_ids, test_work_add_title) pass.
- A first wiring that reviewed again after the fix draft looped (the stub reviewer lists findings at every review); changed to one review a run.

## Tests changed under an allowance
none

## Open questions
- Findings lines naming work-items of different proposals, no work-item of the initiative, or one with no `part_of`: the first line that names a work-item of the initiative decides; if none does, nothing is drafted (unchosen).
- A reviewer that lists findings at every review: a later `work run` drafts a further fix work-item for each new review.
- A failed push after drafting: `self.push()` as after any commit; behaviour is that function's.
- A review with no result file or non-list `questions`: lists nothing.
- An `adds`/`changes` range (`thing#r3-r6`): grouped as written, but matched against a deprecated scenario's single `@r` tag by equality only, so a range retires nothing.
- A draft with nothing to retire has no `## Retires` section.

## Other
The plan contained no code; nothing was pasted.
`tools size --limit 300`: printed nothing (no file over). 
What someone can now do: `work run` turns a formulated capability-proposal into work-items with their Retires, and turns a kept branch review's fix-now findings into a fix work-item.
Surprise: draft items run through the stages in the same run (stub workers DONE).
Commit: 9277e80.

## Files changed
CLAUDE.md, scripts/supervise.py, scripts/supervise_draft.py, scripts/supervise_review.py, scripts/workqueue.py, tests/scenarios/supervision_proposal_steps.py, tests/scenarios/test_supervision.py.
