# Review of w245 (supervision#r219@0.29, r220, r222)

**Verdict: DONE_WITH_CONCERNS.** The scenarios are bound and green and no test or feature was weakened. But `Merge.taken_back` has three ways to give a wrong merge decision: it reruns a scenario twice, it lets an erroring test through, and it takes back failures that are not scenarios. All three are triaged fix now.

## Commits reviewed

- `b274fa52` work run: a scenario failing before a merge gets one second run, alone (r222). Files: `scripts/supervise_merge.py`, `tests/scenarios/supervision_tests_steps.py`.
- `83e3b8ee` work run: r219 and r220 bound; the refused merge's question gives the second run (w245). Files: `scripts/supervise_merge.py`, new `tests/scenarios/supervision_rerun_steps.py`, `tests/scenarios/test_supervision.py` (one import).

These match the implementers' results by message: `397c0f2d` became `b274fa52` and `7b6b0ab9` became `83e3b8ee`. The hashes differ only because `work run` rebased the branch before merging.

Suite (from the brief's record): 1090 passed, 0 failed at 83e3b8ee.

## Removed and weakened tests

None. I searched both diffs for removed lines under `tests/` and `features/`, for removed `def test_`, removed asserts, parametrize, skip and xfail. Both commits only add lines under `tests/`, except one import line in `test_supervision.py`. Nothing under `features/` changed.

## Allowances

Both reports say "none". There are no rows to verify.

## Cannot verify

- The person's answer adds r219 and r220 to w245. `accepts:` in `.shop/work/i62/w245.md` now names all three. That change is `work run`'s own, so it is not in these commits.
- 4-implement's claim that r220 was red before its fix. Its report records the assertion that failed. I did not re-run it red.

## Findings

### 1. Important, fix now: a scenario failing in both runs before a merge is run alone twice
`scripts/supervise_merge.py:150-151`. The loop `for done in (scenarios, suite)` calls `taken_back(..., (scenarios, suite))` once for each failing run. Each call reruns every scenario that either run names. So a scenario that fails in both the work-item's run and the whole-suite run gets two second runs. This contradicts r219 ("run that scenario again once") and the plan's decision 2.

It can also give a wrong answer. Suppose the scenario passes on its first run alone and fails on its second. The merge is then refused, although r222 says a scenario whose second run passes is taken as passing.

Verified by running the r222 scenario with `--basetemp` in scratch. Its repository's `log.jsonl` holds two `rerun` lines for `tests/test_thing.py::test_it_closes`, both `"passed": true`. The r219 scenario does not show this: it refuses after the first call, so its `len(reruns) == 1` assertion holds.

**Fix:** call `taken_back` once, before the loop, when either run failed, and refuse on that one result. Make r222's Then (or a new step) assert exactly one `rerun` line.

### 2. Important, fix now: a failing run with an ERROR test is taken back, and the merge goes ahead
`scripts/supervise_merge.py:121-125`. `taken_back` collects only `FAILED <node>` lines. A run with a non-zero exit, one `FAILED` line and one `ERROR <node>` line (for example a fixture whose setup fails) counts as taken back once the FAILED node passes alone. The erroring test is never rerun and never counted. The merge then goes ahead on a suite that does not pass, which contradicts r4.

Reproduction: `.shop/scratch/w245-5-review/proj/test_mix.py` has one test that fails unless run by its node id and one test whose fixture raises. Command:

    python3 -m pytest -q -s -p no:cacheprovider --rootdir .shop/scratch/w245-5-review -c /dev/null .shop/scratch/w245-5-review/probe_taken_back.py

The probed run printed `FAILED test_mix.py::test_flaky`, `ERROR test_mix.py::test_errors` and "1 failed, 1 error". Then `taken_back` returned `True`.

**Fix:** a failing run with any `ERROR` line (or any outcome other than FAILED scenarios) is not taken back. For example, refuse when the run's summary counts errors, using `suite_record`'s counting.

### 3. Important, fix now (code no line asks for): failing tests that are not scenarios are taken back, and so is any scenario for a guarantees work-item
`scripts/supervise_merge.py:121-122`. Any `FAILED` line with `::` is rerun, whether or not it is a scenario. r219 and r222 name scenarios only. The plan's open case 1 asked the implementer to name how a scenario's node id is told from another test's. The report says every `FAILED ...::` id is rerun.

- `scripts/work_items.py:1-2,137-138` keeps every test that is not a scenario under `--work-item`. So a failing script test (for example under `tests/scripts/`) that passes alone lets the merge go ahead. No Behaviour line asks for that.
- A worse case: when every requirement the work-item accepts is under a guarantees capability, `work_items.py:139-140` and `:160-170` deselect the rerun scenario and turn "no tests collected" into exit 0. The rerun of *any* scenario that failed in the whole-suite run then "passes", so a real regression in another capability's scenario is taken back and merged. This repository has 11 guarantees capabilities (`grep -l '^group: guarantees' spec/capabilities/*.md`).

I verified this by reading `work_items.py`. I did not reproduce it end to end, because that needs a repository with a guarantees work-item.

**Fix:** rerun only node ids that are scenarios the work-item's command selects (pytest-bdd items of the work-item's or the suite's scenarios). A rerun that ran no test counts as failed, not passed. If tests that are not scenarios should get a second run too, write that Behaviour line first, through integrating-a-proposal.

### 4. Minor, observation: the node id is cut at " - ", and only `-n` is stripped from the command
`scripts/supervise_merge.py:121,126`.

- A parametrized id containing " - " is cut short. The rerun of that wrong id fails, so the merge is refused: wrong, but on the safe side.
- Only `-n <x>` is removed from the command. A `[tests]` override using `-nauto` or `--numprocesses` keeps its workers, and one whose work-item command takes no node id runs more than the scenario.

No client sends these today. I did not reproduce them.

### 5. Minor, drop: new lint warning, duplicated fixture, file set
- `tools check` reports `scripts/supervise_merge.py:127:13 PLC0206` (`for node in failing:` without `.items()`). The line is new in these commits.
- `CLOSES_FEATURE` (`supervision_tests_steps.py`) and `ALWAYS_FEATURE` (`supervision_rerun_steps.py`) are the same text.
- `supervision_rerun_steps.py` and `test_supervision.py` are outside the work-item's `fileset:`. The report says so, and the person's answer widened the work.

## Checks

- `tools check --base 955ad466`:
  - ruff: 20 findings across the repository. One is new in these commits (`supervise_merge.py:127 PLC0206`). The `test_supervision.py:14 I001` was already there: the block was already out of order at `branch`/`answers`, and the new import is in alphabetical order.
  - vulture: two findings, neither in these commits.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: prints nothing. The touched files have 160, 252 and 76 lines.

## Commands run

- `git show b274fa52 83e3b8ee`, `git log --stat -2 83e3b8ee`
- `grep` of r4/r43/r219/r220/r222 in `spec/capabilities/supervision.md`; `sed -n 2055,2095p features/supervision.feature`
- `python3 <Scripts>/tools check --base 955ad466...`; `python3 <Scripts>/tools size --limit 300`; `wc -l`
- `sed -n 116,160p scripts/supervise_merge.py`; reads of `scripts/work_items.py` (1-12, 125-170); `grep` for the merge lock
- `python3 -m pytest ... .shop/scratch/w245-5-review/probe_taken_back.py` (finding 2)
- `python3 -m pytest -q -n 0 --basetemp=.shop/scratch/w245-5-review/bt tests/scenarios/test_supervision.py -k passes_on_its_second_run_alone_lets` followed by a `grep` for `"rerun"` in its `log.jsonl` (finding 1)
