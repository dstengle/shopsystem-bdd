## Budget
scripts/supervise_rounds.py (only)

## Outcome: HAND-BACK
Stop condition: no scenario of the work-item is red for the guarantees finding. Plan section 1: "Nothing is red today"; the plan says the red row must come from a feature-formulator hand-back. `grep guarantees features/supervision.feature` shows only the r56/r64/r65 scenarios; none covers a formulate round on a proposal naming a guarantees requirement.
Needed: an r132/r83 row: proposal p1 whose `adds` names a requirement of a `group: guarantees` capability; formulate round gives no scenario and no question; Then p1 transitions to formulated.

## Done
- Decision 4: import order in scripts/supervise_rounds.py (no behaviour change). Check: `pytest -q -k formulate tests/scenarios/test_supervision.py`: 3 passed. Commit 32a16402.
- Not done: decisions 1 and 2 (supervise_outputs.unformulated skipping guarantees ids; shared reader with work_items.guarantees), pending the scenario. No code was written for them, per "code only what a scenario asserts".

Suite at start: 946 passed, 0 failed at d3cd55f0. `tools size --limit 300`: prints nothing.
Tests changed under an allowance: none. Open questions: the plan's section 5 cases (mixed ids, quoted group line, range ids, row vs own scenario) remain unchosen.
The plan contained no code.
Files changed: scripts/supervise_rounds.py
