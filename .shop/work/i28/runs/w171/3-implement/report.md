## Budget
- scripts/supervise_drafts.py
- tests/scenarios/supervision_integrate_steps.py

## Changed
- `supervise_drafts.py`: `last_integrate` replaced by `kept_drafts`, reading every round of every integrate stage under `drafts/round-*/spec/capabilities/`; old layout no longer read.
- Steps: two new Givens (started initiative with proposal; "iN keeps a draft of …"); the old `other_initiative` step now writes its draft under `round-1`.

## Red / green
- Red: `python3 -m pytest -q --work-item w171` -> 2 failed (new r102 scenario and the deprecated one, after the step's layout change): the brief lacked the ids because the code read `drafts/spec/capabilities/`. Expected.
- Green: same command -> 144 passed, 1 skipped. `tests/scenarios/test_supervision.py` -> passes.
- Suite at start: 865 passed, 2 failed (the not-a-git-repository scenario and the r102 scenario); I did not run the whole suite.
- `tools size --limit 300`: no output; no file over.

## Tests changed under an allowance
- Deprecated @r102 scenario, step `other_initiative` in tests/scenarios/supervision_integrate_steps.py: setup only (draft path now under round-1), as the plan lists it. Interim.

## Open questions
- Same capability with different ids across rounds/stages: both rounds' ids are given.
- "not yet applied" (r102 text) vs "spec/ does not hold" (code): differ for ids held by spec whose proposal is not applied.
- Drafts only on another initiative's branch are not read.

## Other
The plan contained no code. Commit: a414d2bd.
