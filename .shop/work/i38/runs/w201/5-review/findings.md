# Review of w201 (i38, supervision)

**Verdict: DONE.** No Critical finding, none triaged fix now. The commits do what the plan asks (decisions 1, 2 and 4) and turn the new r132 guarantees row green. They remove and weaken no test, and they change nothing under `features/`.

## Commits reviewed

The branch `work/w201` is gone. The commits are taken from HEAD, between `773c0199 work: w201 ready -> claimed` and `2c2171fe work: w201 claimed -> done`:

- `d0d62cdd supervise_rounds: order imports (ruff I001)`: `scripts/supervise_rounds.py`, 1 line moved.
- `dcba3f4a formulate round: a guarantees capability's requirements ask for no scenario`: `scripts/supervise_outputs.py`, `scripts/work_items.py`, `tests/scenarios/supervision_session_faults_steps.py`.

The implementers' results list `32a16402` (3-implement) and `b27e0e2c` (4-implement). Both commits still exist in the repository, and their subjects and per-file stats match `d0d62cdd` and `dcba3f4a`. The commits were rewritten when the branch was merged, and their content is the same (Minor finding 2).

An earlier claim, `d3cd55f0 work: w201 ready -> claimed`, is followed by the hand-back. `7b081400` (the r132 outline's guarantees row, under `features/`) comes before the final claim. It is the feature-formulator's commit asked for by the person's answer, not the implementer's, so it is not in the reviewed range.

## Removed and weakened tests

None. I searched the diff `773c0199..dcba3f4a` for:
- removed `def test_`, `@given`, `@when` and `@then`;
- removed `assert` lines;
- changed parametrize lists or Examples rows;
- added `skip` or `xfail`.

The only test change is one new `@given`, `guarantees_then_answered_proposal`, in `supervision_session_faults_steps.py`, which composes the existing `capability` and `answered_proposal` helpers.

## Allowances

The 4-implement report's `## Tests changed under an allowance` says "none". The 3-implement report says the same. There are no rows to verify.

## Cannot verify

- The 4-implement report's figures "`--work-item w201`: 209 passed, 1 skipped; tests/scripts 143 passed" and its red step (that p1 first stayed awaiting-answer with "the formulate round's scenario for steady#r4 is missing"). I did not run the whole suite, because `work run` runs it before merging. The focused run below passes.

## Findings

1. **Minor, observation**: `scripts/supervise_outputs.py:45-49`, `is_guarantees`. It matches only the exact line `group: guarantees`. A frontmatter that quotes the value (`group: "guarantees"`) or has trailing spaces is read as not guarantees, so the formulate round then asks for a scenario of that requirement. This is the same reading `work_items.guarantees` had before, now shared, and plan section 5 names it as an open case. No capability in the repository writes the group differently. Reproduction: `grep -rn "^group:" spec/capabilities/` shows only the plain form. No fix needed now.
2. **Minor, drop**: the reported commit ids (`32a16402`, `b27e0e2c`) differ from those on HEAD (`d0d62cdd`, `dcba3f4a`). The merge rewrote them; the subjects and stats are the same.

Risks I checked and found clear:

- **`work_items.guarantees` gives the root it resolved.** It still resolves `.../spec/capabilities/<cap>.md` and passes `path.parent.parent.parent`, which is the root it resolved before. The r56/r64/r65 behaviour is unchanged.
- **`import re` in `work_items.py`.** It is still used, at lines 40-83.
- **pytest in `work run`.** `supervise_outputs` does not import pytest, so `work run` does not pull pytest in through it (plan decision 2).
- **Code no line asks for.** None. Skipping guarantees ids is what the new r132 row asks for, read with design-decision 0065. The shared reader is mechanism.
- **Clash of the new step with the existing "i1's capability-proposal p1 is awaiting-answer, ..." step.** None: both formulate rows of the outline pass.

## Checks

- `tools check --base 773c0199`:
  - **ruff**: all checks passed.
  - **vulture**: `tests/scenarios/supervision_session_faults_steps.py:57: unused variable 'node'`. This was there before the commits (`git show 773c0199:...` shows `node` at lines 53-55), so it is not a finding against w201.
  - **import-linter**: the project states no import contracts.
- `tools size --limit 300`: prints nothing. The touched files have 73, 150, 128 and 198 lines.

## Commands run

- `git log --format='%h %s' -40 HEAD`
- `git diff 773c0199 dcba3f4a`
- `git show --stat 32a16402 b27e0e2c`
- `git show 7b081400`
- `git show dcba3f4a:tests/scenarios/supervision_session_faults_steps.py`
- `grep` of the `capability` and `answered_proposal` helpers
- `grep -n "re\." scripts/work_items.py`
- `wc -l` of the touched files
- `python3 <Scripts>/tools check --base 773c0199`
- `python3 <Scripts>/tools size --limit 300`
- `git show 773c0199:tests/scenarios/supervision_session_faults_steps.py | grep -n node`
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "guarantees or formulate"`: 4 passed.
