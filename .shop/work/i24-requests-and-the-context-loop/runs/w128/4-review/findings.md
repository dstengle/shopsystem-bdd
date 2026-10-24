# Review of w128: a request accepted, refused or resolved to delivered, each change committed

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now: `work turn` puts a `delivered` request back to `accepted` in an ordinary flow. The commits do what the plan says for r8 to r12. No change under `features/`, no test removed or weakened, and check and size are clean.

## Commits reviewed

The branch `work/w128` is gone. On the checked-out branch, the commits between `1c90481 work: w128 ready -> claimed` and `716ce6b work: w128 claimed -> done`, leaving out `work run`'s `work:` commits (8489c7e and 2310acc), come to one commit:

- `d842f89 work outcome, turn and resolve: a request changed and committed (requests r8-r12)`

The implementer's result lists `15b3801`, which has the same message and author date. `git diff 15b3801 d842f89 -- scripts tests CLAUDE.md features` is empty, so it is the same change rebased onto 8489c7e by the merge. This is not a finding.

Files: `CLAUDE.md`, `scripts/work`, `scripts/workqueue_request.py` (new), `tests/scenarios/requests_steps.py` (new), `tests/scenarios/test_requests.py` (new), `tests/scenarios/work_queue_git_steps.py`. All of them are in the work-item's fileset.

## Removed and weakened tests

None. What I searched for in `git diff 1c90481 716ce6b -- tests/ features/`:
- Deleted lines: there are none (93 insertions, 0 deletions).
- Removed or changed asserts, dropped parametrize cases, added skip or xfail: none.
- Changes to `features/`: none.

The one changed existing step is `new_commit_holds` (`work_queue_git_steps.py:54`). Its only new line is `rel = kept(rel)`, placed before the last assert. `kept` maps only `q\d+` to the request's path and returns any other path unchanged, so the work-queue scenarios that pass a path assert exactly what they did before.

## Allowances

The report's `## Tests changed under an allowance` says "none". This holds: no assert or expected value changed (see above).

## Cannot verify

- The report says `tests/scenarios/test_work_queue.py` could not be run alone in its session. I did not run the whole suite either (`work run` ran it before merging). What I verified for the risk that the generalised `new_commit_holds` changes those scenarios is the reading above.
- The report's figure "Suite at start: 731 passed". I can only take it from the report.

## Findings

### 1. Important, fix now: `work turn` sets a `delivered` request back to `accepted`
- **Where:** `scripts/workqueue_request.py:70-75` (`turn`).
- **What is wrong:** when the turn passes from the upstream and every line is settled, `turn` sets the status to `accepted` or `refused` whatever the status was. Take a request the upstream resolved in its own turn (r10 allows resolve in either side's turn), so its status is `delivered`. When the upstream then hands the turn back with `work turn`, the status drops back to `accepted`, while its `## Resolution` stays written.
- **Reproduction:** a pytest probe in `.shop/scratch/w128-4-review/test_probe.py`, `test_turn_on_delivered`. The request had `status: delivered`, `turn: upstream` and one line `1. accepted`. `work turn q1` exited 0 and the file then read `status: accepted`, `turn: asker`.
- **Why it matters:** the status r11 set is lost. The request then reads as accepted and not yet delivered, and r10 lets it be resolved a second time.
- **The fix:** read literally, r8 and r9 ask for this. The fix is therefore a line ruling through integrating-a-proposal: r8 and r9 hold only for a request that is not yet `delivered` (or only one that is `open`, `awaiting-upstream` or `awaiting-asker`). After the ruling, `turn` leaves a `delivered` status as it is. This is for the person to rule on.

### 2. Minor, observation: an out-of-range `work outcome` lets `turn` settle a line that has no outcome
- **Where:** `scripts/workqueue_request.py:58-60` (`outcome` takes any line number and any word) together with `:71-72` (`turn` compares how many outcomes there are with how many lines).
- **Reproduction:** `test_out_of_range_outcome_settles`. The request had two lines and the outcome `1. accepted`. `work outcome q1 5 accepted` exited 0 and wrote `5. accepted`. `work turn q1` exited 0 and set `status: accepted`, although line 2 has no outcome. r8 needs every line to have an outcome, so this is the wrong status. It is reached only through a line number no line asks to refuse, and the plan's section 5 lists it as an open case.
- **The fix:** `outcome` refuses a line number outside `## Lines`; or `turn` counts outcomes by line number. Hardening.

### 3. Minor, observation: `work resolve` with no `--line` writes an empty resolution and sets `delivered`
- **Where:** `scripts/workqueue_request.py:78-85`.
- **Reproduction:** `test_resolve_no_lines`. The request was `accepted` with one accepted line. `work resolve q1` exited 0 and the file read `status: delivered` with an empty `## Resolution`. r10 asks for each accepted line's requirement id and version. The plan's section 5 lists missing lines and non-accepted lines as open cases.
- **The fix:** `resolve` refuses unless it is given exactly the accepted lines. Hardening.

### Not findings
- The refusal "there is no request …" (`workqueue_request.py:18-19`) is a refusal of a change `work` cannot make (work-queue r7, which the capability's Implementation section names). It is not new observable behaviour.
- The commit messages (`work <cmd>: <id>`) are mechanism.
- `outcome` does not check whose turn it is (r16), and `turn` sets no `awaiting-*` status (r17, r18). Plan D1 leaves these to w127.

## Commands run
- `git log --oneline -15`; `git log --format=%H -1 --grep=...` for the claimed and done commits (`work/w128` is unknown)
- `git log --format="%h %s" 1c90481..716ce6b`; `git show --stat d842f89`; `git show d842f89 -- scripts/ CLAUDE.md`; `git show d842f89 -- tests/`
- `git diff --stat 1c90481 716ce6b -- features/ tests/`: only the 3 test files, insertions only
- `git show -s --format="%T %P" 15b3801 d842f89`; `git diff --stat 15b3801 d842f89 -- scripts tests CLAUDE.md features`: empty
- `python3 -m pytest -q -n 0 tests/scenarios/test_requests.py -k "r8 or r9 or r10 or r11 or r12 or …"`: 5 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 1c90481…`:
  - ruff: All checks passed
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: nothing printed (no file over the limit)
- `python3 -m pytest -q -s -n 0 .shop/scratch/w128-4-review/test_probe.py`: 3 probes, with the outputs quoted above
