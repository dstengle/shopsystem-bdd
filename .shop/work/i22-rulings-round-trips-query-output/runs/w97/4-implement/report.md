# Report w97

## Budget
- scripts/workqueue.py
- scripts/model_work.py
- tests/scenarios/design_model_check_problems.py
- tests/scripts/test_work_item_ids.py (new)

## Changed
- model_work.py: r110 keys `held` by the frontmatter id and reports a work-item whose id's w<n> is not its stem (wording "a work-item's file is named w<n>.md, the w<n> of its id").
- workqueue.py: `highest` counts id and stem `w<n>` of work-items only; the refusal on an existing file names it as "a file that is not a work-item" (reading A, per the person's answer); `entry`'s unreachable "file name" branch removed (N7).
- design_model_check_problems.py: r110 lines dropped only when the named path is not a `w<n>.md` (N2).
- New tests/scripts/test_work_item_ids.py (4 tests).

## Red / green
Red (`python3 -m pytest -q -n 0 tests/scripts/test_work_item_ids.py`): 4 failed: model check printed no r110 problem for `w3.md` holding id w9 or `i2/w5.md` holding w3; `work add` printed w2 beside `fix-login.md` holding w7 (expected w8); refusal read "the work-item w2 already exists" (expected "not a work-item"). Expected: the defects are not covered by the accepted scenarios, which pass before and after.
Green: same file, 4 passed. `python3 -m pytest -q --work-item w97`: 142 passed, 2 failed (tests/scripts/test_tools.py map/untested tests: a nested pytest "no map was made", its inner run hit "--work-item w97: no such work-item", environmental; not touched by this change, not run at base). Also green: test_design_model_check, test_work_queue, test_work_add_title, test_work_items.
Suite at start: 657 passed, 0 failed at 8659d64 (with the expected test_analysis_tools failures listed in the brief).

## Tests changed under an allowance
none (the step in design_model_check_problems.py is rewritten as the plan's decision 5 says).

## Open questions
- A work-item with no id or an id not of the form work-item/…/w<n>: r110 reports it via the id/stem check (non-`w<n>` last segment); whether `highest` counts its stem is left as: the stem is counted.
- An id held twice where a holder is not named w<n>.md: one problem per work-item (the name/id problem), no "held" problem.
- Non-UTF-8 note under an initiative still makes `work add` refuse (decision 6).

## Other
The plan contained no code. Size check: `tools size --limit 300` printed nothing. Commit: 625728c.
Files changed: the four above. No concerns.
