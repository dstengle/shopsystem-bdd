# Review of w224 (supervision r159, r168)

**Verdict: DONE.** Nothing is Critical and nothing is to fix now. Two step regexes were widened so the accepted r159 and r168 Thens bind. The deprecated r92 and r104 Thens still bind to the same steps and assert exactly what they asserted before. Nothing changed in `scripts/` or `features/`.

## Commits reviewed

- `87f21656` "Bind the r159 and r168 Thens: the term clause is optional": the commit as `work run` merged it (brief `Commits:`). It touches `tests/scenarios/supervision_integrate_steps.py` (+4/-4) and `tests/scenarios/supervision_proposal_steps.py` (+4/-4).
- The implementer's result lists `2b992dad`. `git diff 2b992dad 87f21656 -- tests/` is empty and both commits have the same message, author and stat. 87f21656 is 2b992dad rebased by the merge. Its hash differs, its change does not. I do not count this as a finding.
- The suite comes from the brief's record: 1055 passed, 0 failed at 87f21656. Neither w224 scenario is in its expected-failure list.

## Removed and weakened tests

None. What I looked for in the diff:
- deleted test functions or steps: none;
- dropped parametrize cases: none;
- removed or loosened `assert`s: none;
- added skips or xfails: none;
- steps rewritten to assert something else: none.

Each changed step, before and after:
- `proposals_written`:
  - Before, it proved that thing's adds are `[thing#r4, term/ledger]`, its changes `[thing#r2]` and its removes `[thing#r3]`, and that other's adds are `[other#r1]` with its changes and removes empty.
  - Now, when the step text has `and the term "ledger"` (the deprecated r92 Then), the expected lists are exactly the old ones.
  - When the clause is absent (the r159 Then), thing's adds are expected to be exactly `[thing#r4]`.
  - The old case is not weakened.
- `gate_names_its_ids`:
  - Before, it asserted that the brief has `thing#r4`, `thing#r2`, `thing#r3` and `term/ledger`.
  - With the term clause it still asserts all four.
  - Without the clause (the r168 Then) it asserts the three ids.
  - The regex now accepts `thing#r2, thing#r3` (r104) and `thing#r2 and thing#r3` (r168). That is only a change of wording, and the asserts are unchanged.

The plan lists no test under "Tests the decisions break", and none was broken.

## Allowances

The report's `## Tests changed under an allowance` says "none", so there are no rows to check. That matches the diff: no assert, expected value or parametrize case of an existing scenario changed.

## Cannot verify

- The report says the work-item's tests went red (2 failed, undefined Then), then green (182 passed, 1 skipped). I did not re-run that, because the brief's suite record covers the merged commit.
- The notes and plan (D3) say production already does what r159 and r168 ask: `supervise_change.write_proposals` leaves glossary entries out, and the gate brief lists only the proposal's own lists. I did not re-read that code. The green r159 and r168 scenarios in the suite record are the evidence for it.

## Findings

None at Critical or Important.

- **Minor, observation**:
  - What: in `tests/scenarios/supervision_integrate_steps.py:195`, the edited `expected = {...}` line is now about 130 characters. That is longer than the lines around it.
  - Why it matters: `tools check` does not flag it (ruff reports nothing on the lines this commit touched), so this is style only.
  - Fix: wrap the line when the deprecated r92 step is removed under r123.
  - Triage: drop.
- Already in the files the commit touched, but not on lines it changed (`tools check`):
  - `supervision_integrate_steps.py:81` RUF059;
  - `supervision_proposal_steps.py:102` and `:137` RUF100.

  The diff's hunks are at lines 183-198 and 153-164, so these come from earlier commits. They are not w224's.

## Checks

- **ruff**: 5 errors. None is on a line w224 changed: three are listed above, and two are in `tests/scripts/test_supervise_answers.py`, which w224 did not touch.
- **vulture**: 2 unused `args` in `tests/scripts/test_supervise_answers.py`. That file is not w224's.
- **import-linter**: the project states no import contracts.
- **size (`--limit 300`)**: no file is over the limit.

## Commands run

- `git show 87f21656`
- `git log --oneline -5`
- `git log --format=%H -1 --grep="^work: w224 ready -> claimed$"` (gave e4f50825)
- `git log work/w224` (the branch is gone)
- `git show 2b992dad --stat`
- `git diff 2b992dad 87f21656 -- tests/` (empty)
- `grep` of the @r92, @r104, @r159 and @r168 scenarios in `features/supervision.feature`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base e4f508255a2a6b9d955326df4542d638a0d38ee5`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
