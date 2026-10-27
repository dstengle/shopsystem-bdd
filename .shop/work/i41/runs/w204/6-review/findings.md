# Review of w204, fix round (5-implement)

**Verdict: DONE.** The one commit fixes F1 from 4-review as the answer of 2026-10-27 asks. When a proposal's trailing integrate rounds failed, `applied_nothing` now judges by the round before them, so an answered proposal whose redraft integrate round faulted or gave no change list is routed to integrate again, not to apply. No finding is Critical and none is fix now.

## Commits reviewed

- The branch `work/w204` is gone.
- `git log -1 --grep="^work: w204 ready -> claimed$"` gives `a73ea6b2`. That is the second claim, after the answer `f32a423e`.
- Between `a73ea6b2` and `68829a60` (`work: w204 claimed -> done`), the only commit that is not one of `work run`'s own `work:` commits is:
  - `d6667395` supervision: a failed integrate round for a proposal is followed by an integrate round again, not an apply round (r86, r96, r140). It changes `scripts/supervise_rounds.py`, +4 -1.
- This matches the one commit the implementer's `5-implement/result.json` lists.
- The first round's commit `d076baa8` (between `be28c607` and `9a7de712`) was reviewed in `4-review/findings.md` and is not reviewed again here.

## Removed and weakened tests

None. The commit touches no file under `tests/` and none under `features/`. I checked with `git diff --stat a73ea6b2 68829a60`.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds, because no test changed.

## Cannot verify

- The report's run figures: `--work-item w204` gives 153 passed and 1 skipped, and `test_supervision.py` gives 9 passed. I did not run the suite; `work run` ran it before the merge.
- That the fixed path is exercised by any run. No scenario drives it (see F1 below).

## Findings

### F1. Minor, observation: the retry the fix makes has no scenario
- Where: `scripts/supervise_rounds.py:79-80`. Work-item w204.
- What is wrong: no scenario drives the new loop that skips trailing `-integrate` stages. If the loop were removed, the suite would still pass. The implementer says so in the report's Open questions.
- Why it matters: the regression that 4-review F1 found could come back without anything failing.
- Fix: formulate a scenario under r86/r96 with r140: an answered proposal whose redraft integrate round faulted is given an integrate round again on the next `work run`. Then bind it.
- Reproduction: `git show --stat d6667395` lists no file under tests/ or features/.

### Risk checked: is a successful integrate round ever mistaken for a failed one?
- The risk: the loop drops every trailing `-integrate` stage. The comment says such an integrate "left it awaiting an answer", and so failed. That would be wrong if a successful redraft integrate (which moves p1 to drafted, r142) could be followed by awaiting-answer with no later stage directory under `runs/p1/`.
- What I verified: every round, gate included, takes its directory from `run_dir(name, kind)` under `runs/<name>/` (`supervise_rounds.py:117`, `supervise_worker.py:127-131`). `route` consults `applied_nothing` only for an awaiting-answer proposal (`:64-65`). A successful integrate leaves p1 drafted, and the only way from drafted to awaiting-answer is a gate round, which writes `<k>-gate` after it. So a successful integrate is never the trailing stage of an awaiting-answer proposal, and the fix holds for the paths `work run` makes.
- One unhandled case: a hand-made status edit outside `work run` is not covered. No line names that case. Not a finding.

### Carried from 4-review, not part of this fix
F2 (observation), F3 (Minor observation), F4 and F5 (Minor drop) of `4-review/findings.md` stand as triaged there. This round addressed only F1. F4's ruff findings no longer show: `tools check` is clean at HEAD.

## Code no line asks for

None. The change narrows an existing route to what r86, r96 and r140 together give.

## Commands run

- `git log --format='%h %s' -1 --grep="^work: w204 ready -> claimed$"` → a73ea6b2
- `git log --oneline -15`; `git log --oneline --grep=w204`
- `git log -1 work/w204`: unknown revision (the branch is gone)
- `git show --stat d6667395`; `git show d6667395`
- `git diff --stat a73ea6b2 68829a60`
- `sed -n 40,240p scripts/supervise_rounds.py`; `sed -n 120,140p scripts/supervise_worker.py`
- Grep of `r86|r96|r140|r143` in spec/capabilities/supervision.md
- `python3 <Scripts>/tools check --base a73ea6b2`
  - ruff: all checks passed
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300`: nothing printed (no file over; supervise_rounds.py is within the limit)
