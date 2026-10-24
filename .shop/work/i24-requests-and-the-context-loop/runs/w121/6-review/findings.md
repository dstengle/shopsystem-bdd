# Review 6 of w121: --work-item delivers a work-item whose requirements are all guarantees

**Verdict: DONE_WITH_CONCERNS.** The person's answer of 2026-10-24 asked for review 5's Important finding to be fixed: decide r65 in `pytest_sessionfinish` from the work-item and the spec, not from a stash set during collection, and add an `-n 2` test. No commit made that fix. Commit `a90f980 work answer: w121 awaiting-answer -> done` moved w121 to done and changed only the work-item file and the log. `scripts/work_items.py` is the same as it was at review 5. I reproduced the defect again: a guarantees-only `--work-item` run under `-n 2` exits 5. Lint and size are clean.

## Commits reviewed

The branch `work/w121` is gone. The commits are the ones between `25b2223 work: w121 ready -> claimed` and `2a21ecb work: w121 claimed -> done`:

- `3593951` --work-item delivers a work-item whose requirements are all guarantees. It touches features/supervision.feature, scripts/work_items.py, tests/scenarios/supervision_tests_steps.py and tests/scripts/test_work_items.py.
- `82ad81f` supervision steps: the scenario's work run does not inherit another copy of the plugin's scripts. It touches tests/scenarios/test_supervision.py.

Since `2a21ecb`, no commit touches scripts/work_items.py, tests/scripts/test_work_items.py, tests/scenarios/ or features/supervision.feature (`git log 2a21ecb..HEAD -- …` is empty). The commit ids the implementers' results list (`975b45d`, `5652908`) are copies of these two from before a rebase, with the same content (verified at review 5). That is a difference in ids only (Minor, drop).

No implement stage follows 5-review. The answer to review 5's finding has not been carried out.

## Removed and weakened tests

I searched the diff `25b2223..2a21ecb` for removed `def test_`, removed or changed `assert`, parametrize cases, skip/xfail, and removed scenarios or steps.

- **The scenario "a worker's pytest run that collects scenarios, none of which its work-item accepts, is refused (deprecated)"** (`@r56 @deprecated`) was removed. It proved that a run accepting only `other#r1` was refused. The work-item lists it under Retires. Its binding is `scenarios("supervision.feature")`, so the binding went with it. The removal is allowed.
- **The step `ready_accepting_other`** was generalised into the regex step `ready_accepting`. That step still matches the old literal and writes the same `accepts:` line. Only the retired scenario used the old step. It is not weakened.
- Nothing else was removed or weakened.

## Allowances

- 3-implement: "none". This holds.
- 4-implement: `tests/scenarios/test_supervision.py::run_work (setup)`. This holds. The change is an import and a PYTHONPATH filter, with no assert, expected value or parametrize case touched.

## Cannot verify

- That the scenarios pass with the main checkout's scripts on PYTHONPATH, as work run runs them. 4-implement could not run this, and I do not run the suite. work run's merge check is what shows it.
- That a real guarantees-only work-item merges through work run. Finding 1 shows it would not merge wherever xdist is installed.

## Findings

### 1. Important — fix now — r65 still fails under `-n auto`, and the fix the person asked for was not made (scripts/work_items.py:112-113, 128-131)

- **What is wrong.** `pytest_sessionfinish` turns exit 5 into 0 only when `config.stash[GUARANTEES]` is set. Only `pytest_collection_modifyitems` sets it. Under xdist that hook runs in the workers, but the exit status is decided in the controller. So under `-n`, a run for a work-item whose requirements are all of guarantees capabilities, left with no test, still exits 5.
- **Reproduction.** I wrote `.shop/scratch/w121-6-review/probe_xdist.py`. It reuses `consumer` and `capabilities` from tests/scripts/test_work_items.py, with w1 accepting `steady#r1` and `steady` given `group: guarantees`. I ran `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w121-6-review/probe_xdist.py`:
  - serial: exit 0, "2 deselected";
  - `-n 2`: **exit 5**, "4 warnings in 0.40s".
- **Why it matters.**
  - r65 says "the command shall exit successfully", with no exception for parallel runs.
  - The capability's Implementation section (supervision.md:86, :99) runs the work-item's scenarios with `-n auto` where xdist is there, and scripts/supervise_merge.py:30-31 does so.
  - So a guarantees-only work-item still fails work run's merge check. That is the case this work-item exists for.
  - The r65 scenario and the unit tests pass only because they run pytest without `-n`.
  - The person's answer of 2026-10-24 asked for exactly this fix, and the work-item was moved to done without it.
- **Fix.** This is the person's answer.
  - In `pytest_sessionfinish`, when `--work-item` is given without `--whole-suite`, decide from `accepted(name, …)` and `guarantees()` whether every accepted requirement is of a guarantees capability. If so, and the exit status is 5, set it to 0. This runs on the controller and on each worker, with no stash read.
  - Add a test to tests/scripts/test_work_items.py that runs the guarantees consumer with `-n 2` and asserts exit 0.

### 2. Minor — observation — an empty or unparsable `accepts:` deselects everything and exits 0 (scripts/work_items.py:108, 112)

- **What is wrong.** `all(guarantees(...) for c, _ in want)` is vacuously true when `want` is empty. Such a run used to be refused. Now it reports success having tested nothing.
- **Reproduction.** Same probe, `test_empty`:
  - `accepts: []`: exit 0, "2 deselected";
  - `accepts: [thing-r1]`: exit 0, "2 deselected".
- **Why it is only an observation.** No Behaviour line names an empty or malformed `accepts:`, and the model check should reject such a work-item before work run sees it.
- **Fix.** Guard the guarantees path with `want and all(...)`.

### 3. Minor — observation — tests/scenarios/test_supervision.py is outside the work-item's `fileset:`

82ad81f edits it, as the person's first answer asked. The file-set claim should list it (design-decision/the-file-set-is-the-claim). The edit itself stands.

### 4. Minor — drop — the implementers' results list commit ids from before the rebase

See "Commits reviewed".

### Checked and not a finding

- **Code no line asks for.** There is none. The frontmatter read, the conditional refusal, the deselection and the exit change serve r56, r64, r65 and Implementation line :100.
- **Missing capability file.** It counts as not a guarantees capability, so the existing refusal tests hold.
- **`--whole-suite`.** It returns before the new code runs.

## Checks

- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 25b2223`:
  - ruff: All checks passed.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: nothing printed. The touched files are work_items.py 131, supervision_tests_steps.py 208, test_supervision.py 246 and test_work_items.py 127 lines.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w121 ready -> claimed$"`; `git log --format='%H %s' --grep=w121`; `git branch -a --list work/w121`; `git log --oneline -15`
- `git show --stat a90f980`; `git log --oneline 2a21ecb..HEAD -- scripts/work_items.py tests/scripts/test_work_items.py tests/scenarios/`; `git diff 25b2223 HEAD --stat -- …`
- `git diff 25b2223 2a21ecb -- scripts tests features`
- grep of spec/capabilities/supervision.md for r56/r64/r65/-n auto; grep of scripts/supervise_merge.py for xdist
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w121-6-review/probe_xdist.py`
- `tools check --base 25b2223`; `tools size --limit 300`; `wc -l` of the touched files
