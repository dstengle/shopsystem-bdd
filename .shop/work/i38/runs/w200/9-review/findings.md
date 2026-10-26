# Review 9 of w200: DONE

Verdict: no Critical finding, nothing triaged fix now. The commit does what review 7's finding and the person's answer asked: `unformulated` skips ids with no `#r` (term/<term> ids), so a proposal that adds or changes a term is no longer asked forever.

## Commits reviewed

The branch `work/w200` is gone. Commits between `56c39faa work: w200 ready -> claimed` and `80bd7cf6 work: w200 claimed -> done` on HEAD:

- `684f1409` supervise_outputs: the formulate check takes only <capability>#r<n> ids, not term ids (r132). Changes `scripts/supervise_outputs.py`, +2 lines.

This matches the one commit listed in `8-implement/result.json`. `80bd7cf6` is `work run`'s own commit. Earlier commits (`1e0eabf6`, `5e486d94`, `5b198dc9`) were covered by review 7 and come before this claim.

## Removed and weakened tests

None. The diff touches no test file and nothing under `features/`. I checked `git log --stat 56c39faa..80bd7cf6` for any path under tests/ or features/.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commits agree. The four setup allowances from earlier stages were checked by review 7 and are not touched here.

## Cannot verify

- The report says `--work-item w200` gave 208 passed, 1 skipped, and test_supervision.py gave 64 passed. I did not rerun the suite, because `work run` runs it before it merges.

## Findings

1. **Minor, observation**, scripts/supervise_outputs.py:49. No test covers the new skip of term ids, so taking the guard out would leave every test green. Why it matters: the bug review 7 found could come back without a test failing. Fix: add a formulate-round case whose change list holds a `term/<term>` id; r132 already covers it, since a term is no requirement. Reproduction: a grep for `term/` in tests/scenarios/ finds term ids only in design_model_check_*, supervision_integrate_steps.py and supervision_proposal_steps.py (integrate/proposal change lists). It finds none in a formulate-round stand-in, so no formulate scenario gives a term id. The guard also holds for qualified term ids such as `term/ex.com/prod/ctx/suite-record`, which contain no `#r`.
2. Carried over from review 7, not in these commits: ranges such as `thing#r1-r3` are still not expanded (observation, unchanged).

## Checks

- `tools check --base 56c39faa`: ruff passed all checks; vulture clean; import-linter: the project states no import contracts. The ruff I001 that review 7 reported is gone.
- `tools size --limit 300`: printed nothing, so no file is over the limit.

## Commands run

- `git log --oneline -1 --grep="^work: w200 ready -> claimed$"` / `claimed -> done`
- `git log --stat 56c39faa..80bd7cf6`, `git show 684f1409`
- `cat scripts/supervise_outputs.py`, the 8-implement result and report, the 7-review result
- grep for `r132|unformulated(` in the capability and scripts (one caller, supervise_rounds.py:152, which passes adds + changes)
- grep for `term/` in tests/scenarios/
- `tools check --base 56c39faa`, `tools size --limit 300`
