# Review of w139: work run measures a finished initiative and starts its analysis

**Verdict: DONE_WITH_CONCERNS.** r75 and r76 are implemented as the plan says, the checks pass and no test is removed or weakened. There are two Important findings, both triaged fix now. Each is a wrong answer from a session's result that `work run` reads, or does not read, against design-decision/worker-results-are-files (0038).

## Commits reviewed

- Branch `work/w139` is gone. The commits between `ff2a18e work: w139 ready -> claimed` and `971acb5 work: w139 claimed -> done`, less the `work:` commits, are:
  - `470de51 work run measures a finished initiative and starts its analysis (r75, r76)`: w139's commit;
  - `36ecb74 delivering-an-initiative: ...`: this one is w141's (it falls between `a102fce w141 ready -> claimed` and `337f609 w141 claimed -> done`), not w139's.
- The implementer's result lists `2fba3c1`. `git diff 2fba3c1 470de51` over the seven files is empty, so 470de51 is that commit merged under a new hash. No difference in content.
- Files changed: CLAUDE.md, agents/batch-analyst.md (new), scripts/supervise.py, scripts/supervise_analysis.py (new), scripts/supervise_worker.py, tests/scenarios/supervision_analysis_steps.py (new), tests/scenarios/test_supervision.py. All are in the fileset. No file under `features/` changed.

## Removed and weakened tests

None. I searched the diff for removed lines in test files. test_supervision.py only gains one import line, and supervision_analysis_steps.py is new. No `skip`/`xfail` was added, no parametrize case dropped and no assert loosened. The plan's "Tests the decisions break" says none, which matches.

## Allowances

The report's `## Tests changed under an allowance` says "none". No test was changed, so this holds.

## Cannot verify

- That a real `claude -p --agent shopsystem-bdd:batch-analyst` session can run the analyzing-a-batch skill with the `analysis` tools (Read, Glob, Grep, `measure` by path, `Skill(...)`). The skill's other steps may want commands this list refuses, such as git log. Only a real run shows this.
- The report's suite figures: 144 passed for `--work-item w139`, and 134 passed / 16 xfailed / 5 xpassed for the whole-suite run. I did not re-run the suite, as instructed.

## Findings

### 1. Important, fix now: the analysis session's result is never read, and its record is kept whatever the session ended with (w139)

- **Where:** `scripts/supervise_analysis.py:52-58`.
- **What is wrong:** `analyse` ignores the return value of `self.session(...)`. It never reads `result.json` and never calls `cut_short`. Whenever an `analysis.md` exists in the run directory, it is copied to `.shop/records/<date>-<i>-analysis.md`. Two cases show the problem:
  - A session that ended at an error, or with `PARTIAL`, leaves a half-written `analysis.md`. That file is kept as the initiative's analysis record and nothing is said.
  - A session that wrote the record but then gave NEEDS_CONTEXT or BLOCKED is treated the same as a DONE one.
- **Why it matters:** 0038 says a worker's outcome is its result file, and a missing or malformed result is a failed stage. r45's rule is that a session cut short gives no outcome, whatever its result says. The agent's own text says "give `DONE` only when the analysis record is written", and `work run` never looks at that `DONE`. r76 asks for "the initiative's analysis record", and a partial file kept under that name is a wrong answer.
- **Fix:** read the session's `result.json` and check `cut_short(done.stdout, done.returncode)`. Keep the record only when the session was not cut short and its status is DONE. Otherwise tell stderr which it was and that no record was kept, as decision 6 already does for a refused measure.

### 2. Important, fix now: an unfinished branch review counts as "lists nothing to fix now" (w139)

- **Where:** `scripts/supervise_analysis.py:19-25` (`lists_nothing`), called from `scripts/supervise.py:200`.
- **What is wrong:** `lists_nothing` checks only `questions` and ignores `status` and how the session ended. Two kinds of review count as finished with nothing to fix now:
  - a branch reviewer that stopped part-way, whose result still says `PARTIAL` with `questions: []` (its brief tells it to write that first);
  - one that gave NEEDS_CONTEXT with no questions.

  `work run` then measures the initiative as finished and starts the analysis. Because the measure runs once (decision 2) and a later run has no unread commits to review, nothing re-reviews or re-measures. The unfinished review stands as the initiative's last word.
- **Reproduction:** `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w139-5-review/test_probe.py` printed:
  - `PARTIAL -> True` for `{"status":"PARTIAL","summary":"stopped","questions":[]}`;
  - `NEEDS_CONTEXT -> True` for `{"status":"NEEDS_CONTEXT","summary":"no commits"}`.
- **Why it matters:** r75 asks for a kept review that *lists* nothing to fix now. A review that never finished has not done that. Decision 1 of the plan rests on 0038, and 0038 does not let a result's fields stand in for an outcome the session never reached.
- **Fix:**
  - require `status` in (DONE, DONE_WITH_CONCERNS) as well as empty `questions`;
  - also require that the review's session was not cut short. Read the kept `session.json` with `cut_short`; `branch_review` writes it beside the result;
  - otherwise tell stderr why there is no measure.

### 3. Minor, drop: the analysis session's environment says it is the branch review

- **Where:** `scripts/supervise_analysis.py:52` → `supervise_worker.with_scripts(plugin=True, work_item=None)`.
- **What is wrong:** this sets `SHOPSYSTEM_WORK_RUN_WORKER="the branch review"` for the analyst. The r21 refusal still works, so the only effect is that its message names the wrong session.
- **Fix:** pass a label. This is not cheap, because it changes `session`'s signature.

### Already over the size limit

None. `tools size --limit 300` printed nothing.

## Checks

- ruff: All checks passed!
- vulture: clean
- import-linter: the project states no import contracts
- size --limit 300: no file over the limit

## Commands run

- `git log --format='%h %s' -15`
- `git show --stat 470de51 36ecb74`
- `git log --grep=w141`
- `git show 470de51`
- `git show --stat 2fba3c1`
- `git diff 2fba3c1 470de51 --stat -- <files>`
- read `scripts/supervise_worker.py`, `scripts/supervise.py:186-205`, `scripts/supervise_review.py:35-75`, `scripts/supervise_draft.py:57-80`, `scripts/measure:50-57` and `spec/decisions/0038-worker-results-are-files.md`
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w139-5-review/test_probe.py` (the probe of `lists_nothing`)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base ff2a18e`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
