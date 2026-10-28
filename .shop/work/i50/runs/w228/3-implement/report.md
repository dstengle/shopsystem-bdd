## Budget

- scripts/supervise_glossary.py
- scripts/supervise_rounds.py
- tests/scenarios/supervision_proposal_steps.py

## Changed

- `supervise_glossary.approval_question(path)`: for a glossary-proposal, one question asking approval of its terms (adds/changes/removes, each by bare name); None otherwise.
- `run_round`: a gate with no question uses it for a glossary-proposal, else the r117 wording.
- New Then step `one question was written for g1, asking the person to approve the terms ...`.

## Red / green

- Red: `python3 -m pytest -q --work-item w228`: `AssertionError: ('ledger', ['Are the lines of g1 approved as drafted? ...'])`. Expected: the old default names no term.
- Green: same command after the change: 182 passed, 1 skipped.
- Suite at start: 1059 passed, 1 failed (this scenario) plus the expected failures in the brief.

## Tests changed under an allowance
none

## Open questions
Empty lists show as left out; a proposal with all three lists empty gets "It ." (unchosen); ids not in `term/<term>` are cut by the same prefix length.

## Other
Plan contained no code. `tools size`: prints nothing (no file over 300).
Commit: 4f878184.
