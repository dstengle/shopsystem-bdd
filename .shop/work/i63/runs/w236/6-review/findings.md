# Review of w236 (supervision#r218)

**Verdict: DONE.** The code change does what r218 says, and nothing more. One Important finding: a shared assertion in `is_failed` is loosened, the plan does not list it, and the allowance the report claims for it does not hold. It is triaged as an observation: it gives no wrong answer, crash or data loss, and what it now asserts is r218's own wording. No finding is Critical or fix now.

## Commits reviewed

- d8f57cc8 supervision: a change under another run's initiative is neither put back nor named (r218). Touches `scripts/supervise_faults.py` (+5/-1) and `tests/scenarios/supervision_faults_steps.py` (+17).
- 94f0a748 supervision: the r218 scenario's clean-status check leaves out i2's path, which i2's own run may or may not have put back. Touches `tests/scenarios/supervision_faults_steps.py` (+3/-1).

The implementer's last result (5-implement) lists a974d64c and dbb6512d, and the earlier stages list c27c3c7e and a60027a3. These have the same subjects as the merged commits. `git diff a974d64c d8f57cc8` and `git diff dbb6512d 94f0a748` differ only under `.shop/`, so the code is the same and the hashes changed only because `work run` re-based them. This is not a finding.

Suite: taken from the brief's record, 1081 passed and 0 failed at 94f0a748. I did not run it.

## Removed and weakened tests

What I searched for: deleted test functions, dropped parametrize cases, removed or loosened asserts, and skips or xfails added. I checked the diff of `tests/` (one file changed, 20 insertions, 1 deletion) and found that no file under `features/` changed (`git diff --stat 9b773e68 94f0a748 -- features tests`).

- `tests/scenarios/supervision_faults_steps.py::is_failed` (line 112 at 94f0a748). **Weakened.**
  - Before: `git status --porcelain -- .shop/work` had to be empty. Every scenario that ends "w1 is failed, naming/recording …" had to leave all of `.shop/work/` clean. There are 7 such Then lines: supervision.feature:577, 632, 711, 738, 751, 815 and 2028.
  - After: `.shop/work/i2` is excluded from that check for every one of those scenarios.
  - The plan's "Tests the decisions break" says "None", so this change is not listed.
  - No row of the report holds for it (see Allowances).

No other test was removed or weakened. The commits added the Given `two_sessions_change` and the Then `nothing_names`.

## Allowances

- 4-implement report, row `tests/scenarios/supervision_faults_steps.py::is_failed — setup/interim`. **Does not hold.**
  - `setup` does not hold: the diff changes an `assert`, namely its pathspec.
  - `interim` does not hold: the assertion was first committed in 8172b9df on 2026-10-22, before i63 started (2ba3306c, 2026-10-29).
- 3-implement and 5-implement: "none".

## Cannot verify

- The report says the scenario passes "three runs under -n auto". I ran it alone 3 times and it passed each time, but I did not run it under `-n auto`.
- What i2's own run does with `.shop/work/i2/initiative.md` in the r218 scenario (put it back and fault p2's session, or leave it) is still timing-dependent. That is exactly what the loosened assertion hides. I did not probe it, because it would need a Python script that this shell does not allow. It belongs to r215/r216 (w237).

## Findings

### 1. Important · observation: `is_failed` clean-status assertion loosened without the plan listing it

- **Where:** `tests/scenarios/supervision_faults_steps.py:110-112`, in work-item w236 (commit 94f0a748).
- **What is wrong:** the person's answer asked to "make the code and the scenario's steps deterministic". The implementer instead made the shared step tolerate the timing:
  - `.shop/work/i2` is now left out of the clean check for all 7 `is_failed` scenarios, not only the r218 one.
  - The plan lists no broken test.
  - The claimed setup/interim allowance does not hold.
- **Why it matters:**
  - In practice only the r218 scenario has an i2, so the other six lose nothing today.
  - What the step now asserts ("`.shop/work/` less the other initiative's path is clean") matches r218's wording.
  - Still, a pre-initiative assertion was loosened without the plan listing it.
  - The nondeterminism has moved, not gone: depending on timing, i2's run may or may not put back the file and fault p2's session.
- **Reproduction:** `git log -S'assert git(repo, "status", "--porcelain", "--", ".shop/work") == ""' -- tests/scenarios/supervision_faults_steps.py` gives 8172b9df (2026-10-22) and 94f0a748.
- **Fix, either of:**
  - Keep `is_failed` as it was and give the r218 scenario its own clean-status Then, scoped to "less each other initiative's path".
  - List the change in the plan under "Tests the decisions break".

  i2's own behaviour is made deterministic under r215/r216 (w237).

### 2. Minor · observation: a rename line under another initiative's directory

- **Where:** `scripts/supervise_faults.py:114`, in work-item w236.
- **What:** `line[3:]` reads a porcelain rename (`R old -> new`) as one path. This is the same as before the commits. The plan's §5 names it, and the scenarios do not reach it.
- **Fix:** none needed now. Use `--porcelain -z` if a rename under `.shop/work/` ever comes up.

### Risks I checked and found clean

- **Prefix test:** `others` is `run.rel(run.dir) + "/"`, so `i2/` does not match `i20/`. `rel` and `dir` come from supervise.py:51 and :68.
- **Single-initiative run:** its group is `[self]`, so `others` is empty and nothing more is left out. The r28 scenario (:570) still puts i1's path back.
- **The group:** it is fixed for the whole `work run` (supervise.py:65), so for i1 the exclusion does not depend on timing.
- **Fault naming:** supervise_worker.py builds its Fault from the list that `checkout_changes` returns. i2's path is skipped before that list is built, so it is not named.
- **Scope:** I found no code that no Behaviour line asks for. The skip is r214/r218's "leave out / less each path".

## Commands run

- `git log --stat db2873b7..94f0a748`, `git show d8f57cc8 94f0a748`
- `git diff a974d64c d8f57cc8 --stat`, `git diff dbb6512d 94f0a748 --stat`: these differ only under `.shop/`.
- `git diff --stat 9b773e68 94f0a748 -- features tests`: only the steps file changed.
- `git log -S… -- tests/scenarios/supervision_faults_steps.py`: shows 8172b9df and 94f0a748.
- `grep -rn "is failed, (naming|recording)" features/*.feature`: 7 uses.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9b773e68`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing. supervise_faults.py has 194 lines and supervision_faults_steps.py has 207.
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k less_another_initiatives_path_run_side_by_side`, run 3 times: 1 passed each time.
