# Review of w152: DONE

Verdict: no Critical finding and nothing to fix now. The commit adds one Given binding for supervision#r69's scenario, and that scenario passes. No production code, feature file or test was changed beyond that binding.

## Commits reviewed

The branch `work/w152` no longer exists. I took the commits between `f1a315f work: w152 ready -> claimed` and `6b7cdf6 work: w152 claimed -> done` on HEAD, leaving out work run's `work:` commits (01e8daa, b7bfe50, 1996a4d belong to w151 and w153):

- `aedf564 Bind the gate round's single-question Given (supervision#r69)`: tests/scenarios/supervision_rounds_steps.py, +5.

The implementer's result names `c5a7bb1`, which is a different hash. `git diff c5a7bb1 aedf564 -- tests/scenarios/supervision_rounds_steps.py` printed nothing: the content, author, date and message are the same. It is the same commit, re-applied when the branch was merged (see Finding 1).

## Removed and weakened tests

None. I looked for deleted test functions, dropped parametrize cases, removed or loosened asserts, and added skip or xfail markers. The diff only adds lines: one `@given` and a two-line function. No existing binding was changed.

I also checked whether the new binding takes over another step. Its regex needs the exact text `the gate round gives the question "..." on p1, and every round ends`. `gate_result` needs `the gate round's result gives ...`. The two cannot match the same step, so r85's scenario (feature line 1017) still uses `gate_result`.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test changed.

## Cannot verify

- The report's red run (1 failed, 142 passed) and suite at start (816 passed, 1 failed): these are past runs, and I did not re-run the suite. The current green state of the r69 scenario I did verify (below).

## Findings

1. **Minor** (observation), w152, result.json `commits`: the result lists `c5a7bb1`, but the commit on HEAD is `aedf564`. The content is identical; the commit was re-applied at the merge. Reproduction: `git diff c5a7bb1 aedf564 -- tests/scenarios/supervision_rounds_steps.py` printed nothing. Nothing to fix in w152.

Checked with no finding:
- Nothing under `features/` was changed.
- No Behaviour line is contradicted. The binding only sets the stand-in's gate result to DONE with the one question. r69's Then lines are checked against what `work run` actually does.
- No new code goes beyond what a line asks for: the binding is test code that serves r69.
- The open cases the plan lists (D1 to D4, and a failure between move and the Questions write) were left alone, as the plan's decisions P3 to P5 say. D1 and D4 are already raised under w146.

## Checks

- `tools check --base f1a315f`: ruff "All checks passed!"; vulture clean; import-linter "the project states no import contracts".
- `tools size --limit 300`: printed nothing. supervision_rounds_steps.py is 128 lines.

## Commands run

- `git log --format='%H %s' --grep="^work: w152 " HEAD`, `git log --oneline -15`
- `git log --format='%H %s' f1a315f..6b7cdf6`
- `git show aedf564`, `git show --stat c5a7bb1`, `git diff c5a7bb1 aedf564 -- tests/scenarios/supervision_rounds_steps.py`
- `git diff f1a315f aedf564 --stat`
- `grep -n "every round ends" -r tests/scenarios features/supervision.feature`
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k gate -p no:cacheprovider -rA`: PASSED test_when_the_gate_round_work_run_started_for_a_capabilityproposal_ends_the_proposal_is_awaitinganswer
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base f1a315f4a22a1a1f43ab12facdaeab62cfc21d95`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
