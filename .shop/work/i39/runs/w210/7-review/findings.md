# Review of w210, fix round (supervision r135, r136)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now.

The commit fixes both fix-now findings of review 5, as the answers of 2026-10-27 asked:
1. The raise now runs before the round's merge, so there is no `git reset --hard` on the shared checkout.
2. A failed raise commits nothing from the round (reading C): its branch is dropped, its stage directory is removed and
   its log lines are taken back.

There is one new observation (finding 1), and review 5's observations 3 and 4 are still open.

## Commits reviewed

The branch `work/w210` is gone. I took the commits between `068650ac work: w210 ready -> claimed` and
`3378558a work: w210 claimed -> done` on HEAD, leaving out `work run`'s own commits:

- `08013f27` work run raises an integrate round's lines before its merge and commits nothing when the raise fails (r135)
  - scripts/supervise_rounds.py (+37 −13)
  - tests/scenarios/spec_integration_steps.py (+5)

This is the one commit that the implementer's result.json lists, so they agree. Both files are in the work-item's file
set. Nothing under `features/` changed.

The earlier implement round's commit `b762072b` was reviewed in 5-review. I read it here only where the fix touches it.

## Removed and weakened tests

None. I read the whole diff of `08013f27`, looking for:
- a deleted `def test_` or step function;
- a removed or loosened `assert`;
- a parametrize case dropped;
- an added skip or xfail.

The only test change is an addition to the setup step `billing_gives_no_refund` (see Allowances).

## Allowances

- `tests/scenarios/spec_integration_steps.py` `billing_gives_no_refund` (setup): **holds.**
  - The diff adds only a `git init`, a config and a commit of billing's directory.
  - It adds, removes and changes no `assert`, no expected value and no parametrize case.
  - Plan part 4 predicted this break, and the rewrite the plan gives (billing a git repository) is what was done.
  - The scenario still passes: `-k named_upstream --whole-suite` gave 1 passed.

## Cannot verify

- **The failed-raise path itself.** No scenario drives a failed raise. I checked it by reading only, against the r135
  ruling (reading C) and plan decision 9:
  - `undo_round` drops the round branch, removes the uncommitted stage directory and takes it out of `self.own`;
  - it filters out of `self.unlogged` the lines of this round (`work-item`, `stage`) and rewrites `log.jsonl` as HEAD's
    copy plus the rest;
  - it commits nothing, and the initiative stays `started`, because `start_initiative` committed that before the
    round's session.
  - The report itself says that "a failed raise's log.jsonl restore when several initiatives run concurrently" was not
    probed. By reading: `log.jsonl` is per initiative (`self.dir`), and `self.unlogged` is that run's own, so other
    initiatives' logs are not touched. The pool's other work-items of the same initiative keep their lines, because the
    filter is on (name, kind).
- **The report's suite figures**: `--work-item w210` 152 passed; three modules with `--whole-suite` 294+2 passed and 26
  xfailed. I did not re-run the suite.

## Findings

### 1. Minor, observation (w210): a merge that fails after a successful raise leaves an unrecorded request upstream

**Where:** `scripts/supervise_rounds.py:131-134`.

**What is wrong:**
- The raise now commits the request in the upstream before the merge.
- If the merge then fails (`GitFailed`, for example a conflict with something that landed while the lock was free), the
  `except` path calls `note()` and refuses. The record text in `record` is dropped, so no `raised.jsonl` line is
  written.
- The next run raises the same lines again, which duplicates the request upstream. The proposal it writes then is held
  only by the new request.
- Before this commit, a merge failure came before any raise.

This is the same class as review 5's observation 3 (a raise that partly succeeds).

**Reproduction:** none run. Found by reading the code: line 131 is the raise, line 133 is the merge, and lines 135-142
handle the failure without writing a record.

**Fix:** if it is wanted, write the record (or a note naming the raised request ids) when the merge fails after a raise.

### Carried from review 5 (unchanged by this commit, still observations)

- **Observation 3:** a second raise that fails after the first succeeded leaves an unrecorded request
  (`supervise_raise.py:36-51`).
- **Observation 4:** a proposal re-drafted by a later integrate round loses its r136 hold
  (`supervise_raise.py:79-84` with `supervise_change.py:114-116`).

## Code no line asks for

None found. The new code is:
- `raise_before_merge`, which carries out r135 in the order the ruling and plan decision 8 require;
- `undo_round`, which carries out reading C and plan decision 9.

The refusal's wording follows r10/r96.

## Checks

- `tools check --base 068650ac`:
  - ruff: All checks passed;
  - vulture: clean;
  - import-linter: "the project states no import contracts".
- `tools size --limit 300`: printed nothing. `supervise_rounds.py` is 267 lines and `spec_integration_steps.py` is 160.

## Commands run

- `cat` of the brief, the work-item, the 6-implement report, result and brief, the 5-review findings and the 3-plan plan
- `git log --oneline -40`; `git log --format='%H %s' --grep="^work: w210 "`
- `git show --stat 08013f27`; `git show 08013f27`
- `sed -n 100,245p scripts/supervise_rounds.py`
- reads of `scripts/supervise.py:50-112`, `supervise_worker.py:120-200`, `supervise_change.py:35-60` and
  `supervise_faults.py:90-125`. The risk was whether `unknown(found, here)` before the merge sees the round's drafts:
  it does, because `worker` copies the stage directory into the main checkout before the merge. I also checked the log
  and `unlogged` handling.
- `grep -n "def start_initiative" -A 14 scripts/supervise*.py`
- `python3 <Scripts>/tools check --base 068650acf6bae05f4df09550a7cc73c19fbffb27`
- `python3 <Scripts>/tools size --limit 300`
- `wc -l scripts/supervise_rounds.py tests/scenarios/spec_integration_steps.py`
- `python3 -m pytest -q tests/scenarios/test_spec_integration.py tests/scenarios/test_supervision.py -k upstream`:
  2 passed (r135, r136)
- `python3 -m pytest -q tests/scenarios/test_spec_integration.py --whole-suite -k named_upstream`: 1 passed
  (spec-integration @r44)
