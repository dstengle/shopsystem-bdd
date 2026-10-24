# Review of w119 (supervision#r63: blocked_by read across initiatives)

**Verdict: DONE.** No Critical finding, none triaged fix now. One Minor observation.

## Commits reviewed

Branch `work/w119` is gone. The commits are those between `362827b` (`work: w119 ready -> claimed`) and `2ad5853` (`work: w119 claimed -> done`) on the checked-out HEAD, less `work run`'s own `work:` commits:

- `fd035f0` work run reads blocked_by across initiatives (r63): scripts/supervise_pool.py (+2 -1), tests/scenarios/supervision_parallel_steps.py (+17)

This matches the implementer's result.json (`commits: ["fd035f0 ..."]`). Both files are in the work-item's `fileset:` and the plan's budget. Nothing under `features/` changed.

## Removed and weakened tests

None. What I searched: the diff of `fd035f0` has no `-` line in either test module. Its only removed line is `statuses = dict(self.items())` in scripts/supervise_pool.py. No test function was deleted, renamed or rewritten, no parametrize case dropped, no assertion loosened and no skip or xfail added. The three steps are new. The existing `blocked_item` step and the `none_started_for` step have no changes.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test changed.

## Cannot verify

- The report's suite figures ("Suite at start: 715 passed, 1 failed"; "140 passed, 1 skipped" under `--work-item w119`). I did not run the whole suite (`work run` runs it before merging). I ran only the two r63 scenarios.
- Plan §5's open cases (blocker green only on another branch, the id-form blocker `work-item/w2`, a blocker absent everywhere, a blocker whose file and log disagree). No line or scenario asks for these, and the commits do not change them. They stay open as the plan named them.

## Findings

### F1 (Minor, observation): with a name in several other initiatives, the last in path order wins

- **Work-item:** w119
- **Where:** scripts/supervise_pool.py:62
- **What's wrong:** `{name: status for _, name, status in workqueue.items(self.root)}` keeps the status of the last initiative in sorted path order when more than one *other* initiative holds a blocker's name. Line 63 makes this initiative's reading win, as plan D1 says. Among other initiatives, though, the result depends on directory order.
- **Why it matters:** Only legacy names can be shared (work-queue#r12 makes new `w<n>` ids unique; migration-tools#r26 renames legacy ones). No client sends this input today, and no line or scenario names the case. That makes it hardening, not a wrong answer.
- **Reproduction:** found by reading, not by a run. `workqueue.items` yields in `sorted(glob("*/*.md"))` order (scripts/workqueue.py:102). The dict comprehension overwrites on a repeated key. Example: i2/w2 green and i3/w2 drafted, with i1/w1 blocked_by [w2], gives w2 → drafted, so w1 is held back. With i3/w2 green and i2/w2 drafted, w1 starts.
- **Fix (if wanted):** treat a name held by several other initiatives as green only when every holder is green, or refuse it as ambiguous. Either one needs a line first.

## Risks checked outside the diff

- **Risk: a different tuple shape from `self.items()` breaks `update`.** I checked scripts/supervise.py:60-61: `Run.items` returns `(name, status)` pairs, so `statuses.update(self.items())` is sound. `workqueue.items` yields `(initiative, name, status)` triples (workqueue.py:100-105), so line 62 unpacks them correctly.
- **Risk: a new crash path from reading every initiative.** `Run.items` already calls `workqueue.items(self.root)` over every initiative on each pull, so no new file read is added. `workqueue` was already imported in supervise_pool.py (line 7).
- **Risk: other initiatives' work-items get started.** The loop that picks work-items (supervise_pool.py:71) still iterates `self.items()`, which holds this initiative's only.
- **Risk: a status-less blocker counts as green.** It does not: `None != "green"`, so the work-item stays blocked (plan D2).

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w119 ready -> claimed$"` → 362827b
- `git log --format='%H %s' -1 --grep="^work: w119 claimed -> done$"` → 2ad5853
- `git log --stat --format='%h %s' 362827b..2ad5853`
- `git show fd035f0`
- grep of scripts/supervise_pool.py, scripts/workqueue.py, scripts/supervise.py, spec/capabilities/supervision.md, features/supervision.feature, tests/scenarios/supervision_world.py
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k blocked_by` → 2 passed
- `python3 <Scripts>/tools check --base 362827b...`:
  - ruff: All checks passed
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300` → nothing printed (no file over the limit)
- `git status --short` → clean
