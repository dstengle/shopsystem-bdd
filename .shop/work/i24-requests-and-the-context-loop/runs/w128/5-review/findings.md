# Review of w128 (second review, after the answer): a request accepted, refused or resolved to delivered, each change committed

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. The commits are the same ones the first review (4-review) saw. Its one fix-now finding (`work turn` putting a `delivered` request back to `accepted`) has been answered: on 2026-10-24 the coordinator, under the person's delegation, accepted the work-item as it stands. r8 and r9 are to be narrowed to a request that is not delivered, and that change gets its own fix work-item. The finding is therefore carried as ruled and is not fix now for w128. The two Minor observations still hold.

## Commits reviewed

The branch `work/w128` is gone. On the checked-out branch, the commits between `1c90481 work: w128 ready -> claimed` and `716ce6b work: w128 claimed -> done` come to one once `work run`'s own `work:` commits (8489c7e, 2310acc) are left out:

- `d842f89 work outcome, turn and resolve: a request changed and committed (requests r8-r12)`

The implementer's result lists `15b3801`. The first review found `git diff 15b3801 d842f89` empty, so it is the same change rebased by the merge. Not a finding. After 716ce6b, the only w128 commit is `8af18e2 work answer: w128 awaiting-answer -> done`; it changes no code. Two later commits touch `scripts/workqueue_request.py` and the request steps, but they belong to w126 (97a0cec) and w131 (4e5c8de), not to w128.

Files: `CLAUDE.md`, `scripts/work`, `scripts/workqueue_request.py` (new), `tests/scenarios/requests_steps.py` (new), `tests/scenarios/test_requests.py` (new), `tests/scenarios/work_queue_git_steps.py`. All are in the fileset.

## Removed and weakened tests

None. What I searched for in `git diff 1c90481 716ce6b -- tests/ features/`:
- Removed lines: 0 (93 insertions only).
- Removed or loosened asserts, dropped parametrize cases, added skip or xfail: none.
- Changes under `features/`: none.

The one existing step that changed is `new_commit_holds` (`work_queue_git_steps.py:54`). It gains `rel = kept(rel)` before its last assert. `kept` rewrites only `q\d+`, so a plain path asserts exactly what it did before.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: no assert or expected value changed.

## Cannot verify

- Whether `tests/scenarios/test_work_queue.py` still passes. The report says it could not be run alone in the implementer's session. I did not run the suite (`work run` did). For the risk that the generalised `new_commit_holds` changes those scenarios, I read the step (above).
- The report's "Suite at start: 731 passed".

## Findings

### 1. Important, ruled (not fix now for w128): `work turn` sets a `delivered` request back to `accepted`
- **Where:** `scripts/workqueue_request.py:70-75`.
- **What is wrong:** when the upstream ends its turn on a request whose every line is settled, `turn` sets `accepted` or `refused` whatever the status was before, including `delivered` (reproduced in 4-review).
- **Status:** the answer of 2026-10-24 accepts the work-item as it stands. r8 and r9 are being changed to hold only for a request that is not delivered, and that change and its scenario go to their own fix work-item. Today's r8 and r9 (spec/capabilities/requests.md:31-32) still read literally, so nothing in w128's commits contradicts a line as it stands. The fix belongs to the coming fix work-item.

### 2. Minor, observation: an out-of-range `work outcome` lets `turn` settle a line that has no outcome
- **Where:** `scripts/workqueue_request.py:58-60` with `:71-72`.
- **Reproduction (4-review):** a request with two lines and `1. accepted`. `work outcome q1 5 accepted` exits 0, then `work turn q1` sets `status: accepted` although line 2 has no outcome.
- **Fix:** `outcome` refuses a line number outside `## Lines`, or `turn` counts outcomes by line number. This is hardening, and plan section 5 lists it as an open case.

### 3. Minor, observation: `work resolve` with no `--line` sets `delivered` with an empty resolution
- **Where:** `scripts/workqueue_request.py:78-85`.
- **Reproduction (4-review):** on an accepted request with one accepted line, `work resolve q1` exits 0 and writes `status: delivered` with an empty `## Resolution`.
- **Fix:** `resolve` refuses unless it is given exactly the accepted lines. This is hardening, and plan section 5 lists it.

### Not findings
- The refusal "there is no request …" refuses a change `work` cannot make (work-queue r7, which the Implementation section names).
- The commit messages are mechanism.
- r16, r17 and r18 are left to w127 (plan D1).
- `tools check` reports two problems, and neither file is in w128's commits:
  - ruff I001 in `tests/scenarios/test_design_model_check.py:7`, last touched by d23a6a4 (w131);
  - vulture `named` unused in `tests/scenarios/requests_write_steps.py:62`, from 97a0cec (w126).

## Commands run
- `git log --oneline -20`; `git log --format=%H -1 --grep="^work: w128 ready -> claimed$"` → 1c90481; `--grep="^work: w128 claimed -> done$"` → 716ce6b; `git log work/w128` → unknown revision
- `git log --format="%h %s" 1c90481..716ce6b`; `git log 716ce6b..HEAD -- scripts/workqueue_request.py tests/scenarios/requests_steps.py tests/scenarios/test_requests.py scripts/work` → 4e5c8de, 97a0cec (other work-items)
- `git show d842f89 --stat` and full diff
- `git diff --stat 1c90481 716ce6b -- features/ tests/` → 3 test files, 93 insertions; removed lines: 0
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 1c90481…`:
  - ruff: 1 error, I001 in test_design_model_check.py (not w128's)
  - vulture: 1, requests_write_steps.py:62 (not w128's)
  - import-linter: the project states no import contracts
- `git log 1c90481..HEAD -- tests/scenarios/test_design_model_check.py tests/scenarios/requests_write_steps.py` → d23a6a4, 97a0cec
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → nothing printed
- `python3 -m pytest -q -n 0 tests/scenarios/test_requests.py -k "upstream_ending or resolve or changes_a_request"` → 5 passed
