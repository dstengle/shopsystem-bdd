# Review of w135 (supervision#r67: intake round)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. There are three Minor findings: two observations and one drop.

## Commits reviewed
- The branch `work/w135` is gone. The commits are those between `b9a4f50 work: w135 ready -> claimed` and `25f47d5 work: w135 claimed -> done` on the checked-out HEAD, less `work run`'s `work:` commits.
- That leaves one commit: `3b24b69 work run: an intake round for each request this context is the upstream of (supervision r67)`. It matches the implementer's `result.json` `commits` exactly.
- It changes 7 files: CLAUDE.md, agents/initiative-round.md, scripts/supervise_all.py, scripts/supervise_intake.py (new), scripts/supervise_worker.py, tests/scenarios/supervision_intake_steps.py (new), tests/scenarios/test_supervision.py.
- All of them are in the work-item's fileset. The commit does not touch scripts/supervise_brief.py, which the fileset lists; the report says why (`Intake` overrides `brief`).

## Removed and weakened tests
None.
- I searched with `git diff --stat b9a4f50 25f47d5 -- features tests`. Only two test files changed: a new 38-line steps module, and one added import line in test_supervision.py.
- Nothing under `tests/` was deleted, and no assert, parametrize case, skip or xfail changed. The plan's "Tests the decisions break" says none.
- Nothing under `features/` changed.

## Allowances
The report's `## Tests changed under an allowance` says "none", and none is needed.

## Cannot verify
- **The fault path of answer 2, Q1** (an intake round that does not end DONE prints the fault and makes the exit 1, and the other requests and initiatives are still taken). No scenario covers it, as the report says. What I verified by reading the code:
  - `Intake.take` raises `Refused` naming the round, its run directory and how it ended. It does this both for a fault and for an outcome other than DONE, and it merges nothing.
  - `run_all` catches that per request, so the other requests are still taken. It then starts the initiatives' threads.
  - `run_all` prints `work: q1: …` on stderr and returns 1 when `refused` is non-empty, whatever the initiatives' nodes are.
- **The real `initiative-round` session's behaviour on the `intake` job**: whether it writes `question` for a line it cannot judge, and gives the question's text in its result. Only the stand-in session is exercised.

## Findings

### 1. Minor (observation): a failed push after a DONE intake round is silently ignored
- **Where:** scripts/supervise_intake.py:112 (`keep` → `self.git_push()`, its return value discarded).
- **What is wrong:** on the DONE path, the merge and the record commit are followed by a push whose failure is dropped. The proposal rounds' DONE path pushes through `move`/`commit`, which makes a failed push a fault (r38/r41). Here the run exits 0 with the commits unpushed.
- **Why it is not fix now:** no data is lost. The commits are local, and the next `work run` pushes them through `push_unpushed` (r54). The push was also verified before the session started (r35).
- **Reproduction:** none run. It needs a remote that accepts `--dry-run` and then refuses the push.
- **Fix:** on the DONE path, raise a `Fault`/`Refused` when `git_push()` returns a reason.

### 2. Minor (observation): the intake brief and the agent offer only three of the glossary's five line outcomes
- **Where:** scripts/supervise_intake.py:61 and agents/initiative-round.md:36.
- **What is wrong:** both give `<accepted|refused|withdrawn>` (plus `question`) and leave out `rewritten`, which spec/index.md:110 lists as a line outcome.
- **Why it is not fix now:** r67 says "each line's line outcome". No scenario or client today needs `rewritten` from an intake. The requests capability may also need rewritten text that `work outcome` does not take.
- **Reproduction:** `grep -n "accepted|refused|withdrawn" scripts/supervise_intake.py agents/initiative-round.md` shows both places. `grep -n "line outcome" spec/index.md` shows line 110 with all five.
- **Fix:** list `rewritten` too, or settle through the requests capability how a rewrite is written.

### 3. Minor (drop): the intake session's worker marker reads "the branch review"
- **Where:** scripts/supervise_worker.py:84 and 224.
- **What is wrong:** the intake session gets no `work_item`, so `with_scripts` sets `SHOPSYSTEM_WORK_RUN_WORKER="the branch review"`. A `work run` started inside an intake round still refuses, as r21 asks. But its message reads "…a worker of another `work run` (of the branch review)".
- **Why it does not matter much:** the wording is cosmetic. The proposal rounds share it.
- **Fix:** pass a marker such as `"the intake of q1"`.

### Also noted (not findings)
- `Intake.keep` is close to a copy of `Rounds.keep_round`. This is a duplication only.
- A non-DONE round's `round/<q>-<k>-intake` branch is not deleted. That is the same as the proposal rounds, so it is not new with this work-item.

## Risks checked
- **`Run.__init__` with "requests":** it sets `dir` to `.shop/work/requests/` and has no initiative-specific reads (supervise.py:46-63). This is sound.
- **`work run <initiative>` must stay unchanged (answer 1, Q2):** supervise.py was not touched, and only `run_all` calls `supervise_intake`.
- **Checks before anything moves (r10):** `intake.check()` runs before `push_unpushed` and before any session starts, after the initiatives' checks. When no request is due, no `Intake` is made, so the r66/r81/r82 runs keep their behaviour.
- **Tools (r13/r14):** the intake list is READER plus `work outcome *`, `work turn *` and `work show*`, with no bare Write or Edit.
- **Merge and fault handling** mirror `Rounds.round` (supervise_rounds.py:47-77). That includes `merge --abort` and committing the record so that r46 does not refuse the next run.
- **Code no line asks for:** none found. The intake's checks serve r21, r46 and r54, and its record commit serves r46/r38. The fault exit is the dated answer applied, not a new behaviour.
- **Size:** supervise_worker.py has 247 lines, supervise_all.py 66 and supervise_intake.py 112. All are under 300.

## Commands run
- `git log --oneline -15 HEAD`; `git log --format=%H -1 --grep="^work: w135 ready -> claimed$"` → b9a4f50 (`work/w135` is gone)
- `git show --stat 3b24b69`; `git show 3b24b69 -- scripts CLAUDE.md agents tests`
- `git diff --stat b9a4f50 25f47d5 -- features tests` → only the new steps module and one import line
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b9a4f50…`:
  - **ruff:** All checks passed!
  - **vulture:** clean
  - **import-linter:** the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → no output (no file is over the limit)
- `python3 -m pytest -q -n 0 -k intake_round tests/scenarios/test_supervision.py` → 2 passed
- Read-only looks: scripts/supervise.py:46-63, scripts/supervise_worker.py:30-244, scripts/supervise_rounds.py:40-110, scripts/supervise_faults.py:26-80, scripts/supervise_all.py:40-66, spec/index.md:110, spec/capabilities/supervision.md:25,133
