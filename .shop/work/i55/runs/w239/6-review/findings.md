# Review of w239 (requests r64), round 6

**Verdict: DONE.** The one commit restores `  # formulates [r64] of spec/capabilities/requests.md` directly above
`@r64` in features/requests.feature, exactly as the person's answer rules, and changes nothing else. The earlier
Critical finding (4-review, finding 1) is resolved. No finding is Critical or fix now.

## Commits reviewed

- `fce410f4` Restore the r64 formulates comment swept up by retiring r14's scenario: features/requests.feature, +1 line.
  The brief's `Commits:` gives this one commit; the implementer's result (5-implement/result.json) lists the same
  commit. No difference.
- Suite taken from the brief's record: 1088 passed, 0 failed at fce410f4. The listed expected failures are other
  work-items' (requests between repositories, supervision redraft, work-queue done); none is an r64 scenario.

Verified:
- The restored line and its placement match the formulate commit `0e9fa09f` (comment at the line before `@r64`,
  preceded by a blank line).
- `git diff cae12e0c~1 fce410f4 -- features/requests.feature` (the whole of w239's change to the file) now removes only
  the @r14 @deprecated scenario the Retires section names; the r64 provenance comment is intact.

## Removed and weakened tests

None. Searched the diff of `fce410f4` for deleted test functions, scenarios, parametrize cases, assertions, skips and
xfails: the commit touches no file under tests/ and adds one comment line under features/.

## Allowances

The report's `## Tests changed under an allowance` says "none". No test changed, so it holds.

## Cannot verify

Nothing material. The report states no tests run (a comment-only change); the brief's suite record covers it.

## Findings

No new findings.

- 4-review finding 1 (Critical / fix now, features/requests.feature before @r64): resolved by `fce410f4`.
- 4-review finding 2 (Minor / observation, scripts/workqueue_list.py:53/:78, an observation with no `date:` prints
  "None"): unchanged by this round; it stays an observation, not in this commit.

## Checks

- `tools check --base 2a17f3b1`:
  - ruff: All checks passed.
  - vulture: `tests/scenarios/work_queue_status_steps.py:100: unused variable 'notes'`; not touched by this commit
    (it touches only a .feature file), so already present, not this work-item's.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: no output, no tracked Python file over the limit.
- `features bindings`: every binding names a scenario.

## Commands run

- `git log --oneline -8`; `git show --stat fce410f4`; `git show fce410f4 -- features/requests.feature`
- `git show 0e9fa09f:features/requests.feature | grep -n -B3 -A2 "@r64"`
- `git diff cae12e0c~1 fce410f4 -- features/requests.feature`; `git diff 2a17f3b1 fce410f4 --stat`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 2a17f3b1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 /home/vscode/shopsystem-bdd/scripts/features bindings`
