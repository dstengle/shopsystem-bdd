# Review of w121: --work-item delivers a work-item whose requirements are all guarantees

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now. r65 is not met under `-n auto`, which is how work run's own work-item test command runs `--work-item` when pytest-xdist is installed. Running in one process, the change does what r56, r64 and r65 ask. Lint and size are clean.

## Commits reviewed

The branch `work/w121` is gone. The commits are the ones between `25b2223 work: w121 ready -> claimed` and `2a21ecb work: w121 claimed -> done` on the checked-out branch:

- `3593951` --work-item delivers a work-item whose requirements are all guarantees: features/supervision.feature, scripts/work_items.py, tests/scenarios/supervision_tests_steps.py, tests/scripts/test_work_items.py.
- `82ad81f` supervision steps: the scenario's work run does not inherit another copy of the plugin's scripts: tests/scenarios/test_supervision.py.

The implementers' results list different ids: `975b45d` (3-implement) and `5652908` (4-implement), and 5652908's parent is `9492062`. These are earlier copies of the same changes on a branch that has since been rebased. `git diff 975b45d^ 975b45d` has the same content as 3593951. 82ad81f has the same 4-line stat as 5652908, and its diff shows the change the 4-implement report describes. The rebased copies dropped the `Co-Authored-By` trailers. This is a difference in ids only, not in content (Minor, drop).

## Removed and weakened tests

I searched the diff for removed `def test_`, removed or changed `assert`, parametrize cases, skip/xfail, and removed scenarios or steps.

- **The scenario "a worker's pytest run that collects scenarios, none of which its work-item accepts, is refused (deprecated)"** (`@r56 @deprecated`) was removed from features/supervision.feature. It proved that a run accepting only `other#r1` was refused. The work-item lists it under Retires, and the plan names it in §1. It was removed with its binding (test_supervision.py binds by `scenarios()`). This removal is allowed.
- **The step `ready_accepting_other`** ("i1's work-item w1 is ready, accepting other#r1") was replaced by the regex step `ready_accepting`. That step still matches the old literal and also matches two ids joined by "and". It writes the same `accepts:` line, so this is a renamed and generalised step, not a weakened one. Only the retired scenario used it (plan §4).
- No other test was removed or weakened. No assertion was loosened and no skip or xfail was added.

## Allowances

- **3-implement report: "none".** This holds. The retired step was generalised, not weakened (see above).
- **4-implement report: `tests/scenarios/test_supervision.py::run_work` (setup).** This holds. The diff adds `from pathlib import Path` and two lines that filter PYTHONPATH. It adds, removes or changes no `assert`, no expected value and no parametrize case. It is the change the coordinator's answer asked for.

## Cannot verify

- 4-implement says the scenarios pass with the main checkout's scripts on PYTHONPATH, the way work run runs them. The implementer could not run that, and I did not either (an env-prefix command is not allowed here, and I don't run the full suite). work run's merge check is what proves it.
- Whether a real guarantees-only work-item now merges through work run. That has not been exercised, and Finding 1 says it would not merge where xdist is installed.

## Findings

### 1. Important — fix now — r65 fails under `-n auto` (scripts/work_items.py:112-113, 128-131)

- **What is wrong.** The success exit depends on `config.stash[GUARANTEES]`. Only `pytest_collection_modifyitems` sets it. Under pytest-xdist that hook runs in the worker processes, not in the controller, but the session's exit status is decided in the controller. So when a guarantees-only work-item's run is left with no test under `-n`, the stash is empty where it is read, and pytest still exits 5.
- **Reproduction.** I wrote the probe `.shop/scratch/w121-5-review/probe_guarantees.py`: a consumer repository whose w1 accepts `steady#r1`, where `steady` has `group: guarantees`, and whose only test file holds two thing scenarios. I ran `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w121-5-review/probe_guarantees.py`.
  - `--work-item w1`: exit 0, "2 deselected".
  - `-n 2 --work-item w1`: **exit 5**, "4 warnings in 0.44s".
- **Why it matters.** `scripts/supervise_merge.py:20,31` runs the work-item's tests as `python3 -m pytest -q -n auto -p work_items --work-item <w>` wherever xdist is installed, as it is here. A guarantees-only work-item's test run would still exit non-zero, and merge treats a non-zero exit as a failure (merge:128-130). So the work-item cannot be delivered, which is the case this work-item exists for. r65 says "the command shall exit successfully" and has no exception for a parallel run. The r65 scenario passes only because its stub implementer runs `python3 -m pytest -q` without `-n`. The unit tests do not use `-n` either. The plan's §5 left this open ("whether the exit-status change takes effect in the controller process"), and neither report answers it.
- **Fix.** In `pytest_sessionfinish`, decide from the configuration rather than from state set during collection:
  - when `--work-item` is given, `--whole-suite` is not, and every accepted requirement `accepted(name, …)` is of a guarantees capability, turn exit 5 into 0;
  - or set the flag in `pytest_configure` as well, so the controller has it too.
- **Test.** Add a unit case to tests/scripts/test_work_items.py that runs the guarantees consumer with `-n 2` and expects exit 0.

### 2. Minor — observation — an empty or unparsable `accepts:` now deselects everything and exits 0 (scripts/work_items.py:108, 112)

- **What is wrong.** `all(guarantees(config, c) for c, _ in want)` is true when `want` is empty. That happens with `accepts: []`, or with an `accepts:` whose ids `requirements()` cannot parse (e.g. `thing-r1`). Before this change, such a run was refused ("accepts none of the scenarios it collected"). Now it deselects every scenario and exits 0, so it reports success having tested nothing.
- **Reproduction.** Same probe file. `accepts: []` → exit 0, "2 deselected". `accepts: [thing-r1]` → exit 0, "2 deselected".
- **Why it is only an observation.** No Behaviour line names an empty or malformed `accepts:`, and r64 read literally is vacuously true for it. The model check is expected to reject such a work-item before work run sees it.
- **Fix.** Require `want` to be non-empty for the guarantees path: `want and all(...)`.

### 3. Minor — observation — a file outside the work-item's file set was edited (tests/scenarios/test_supervision.py)

- **What is wrong.** 82ad81f edits tests/scenarios/test_supervision.py, but the work-item's `fileset:` does not list it (design-decision/the-file-set-is-the-claim).
- **Why it is only an observation.** The person's answer asked for exactly this edit ("make the supervision steps that start work run … run it with an environment whose PYTHONPATH holds no other copy"), and the 4-implement report names it in its Budget. It is recorded so that the file-set claim can be corrected, not to undo the edit.

### 4. Minor — drop — the rebased commit ids differ from the ids the results list

See "Commits reviewed" above.

### Checked and not a finding

- **Fixture repositories.** `guarantees()` resolves `spec/capabilities/` as the parent of `.shop/`, from `work_dir(invocation dir)`. It is correct for the scenario's fixture repository and for the unit consumer.
- **Missing capability file.** It counts as not guarantees (plan decision 2), so the existing refusal tests still hold.
- **Normal path.** The guarantees path does not touch a guarantees work-item that does collect accepted scenarios: the stash only changes exit 5.
- **`--whole-suite`.** It returns before any of the new code runs.
- **Code no line asks for.** I found none. The docstring change and the frontmatter read serve r56, r64 and r65 and the capability's Implementation line.

## Checks

- `tools check --base 25b2223`:
  - ruff: All checks passed.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: nothing printed. Files the commits touched: work_items.py 131, supervision_tests_steps.py 208, test_supervision.py 246, test_work_items.py 127 lines.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w121 ready -> claimed$"` (and the same for `claimed -> done`); `git log --oneline f890f2f..HEAD`
- `git show --stat 975b45d 5652908 3593951 82ad81f`; `git log --oneline -4 5652908`
- `git diff 975b45d^ 975b45d`; `git diff 25b2223 82ad81f`
- `grep -n ... spec/capabilities/supervision.md`; `wc -l` on the touched files; reading `scripts/work_items.py`, `tests/scripts/test_work_items.py:1-60` and `grep` of `scripts/supervise_merge.py`, `scripts/supervise_worker.py`
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w121-5-review/probe_guarantees.py` (4 probes: serial, `-n 2`, empty accepts, unparsable accepts)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 25b2223`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
