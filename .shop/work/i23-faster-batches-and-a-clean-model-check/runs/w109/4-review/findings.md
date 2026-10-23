# Review of w109: work run runs independent work-items side by side

**Verdict: DONE.** No Critical finding, and none to fix now. Two Minor observations.

## Commits reviewed

The branch `work/w109` is gone. The commits are those between `e8a6dda work: w109 ready -> claimed` and
`2ee80c4 work: w109 claimed -> done` on the checked-out history:

- `4232bc6 work run runs independent work-items side by side (w109)`: 13 files, +374 −118.

This is the one commit the implementer's result lists. The files are inside the work-item's fileset. Of the
fileset, `supervise_faults.py` and `workqueue.py` were not touched; the plan kept them only in case they were needed.

## features/

Only the three deprecated scenarios that the work-item's Retires section lists were removed (@r1 "…one worker at a
time…", @r20 "…not share a file… merged one at a time", @r20 "…no more than two…"). Their bindings come through
`scenarios()`, and the two steps only they used were removed. No other change. **Not a finding.**

## Removed and weakened tests

I searched the diff of `tests/` for: deleted test or step functions, dropped parametrize cases, removed or loosened
asserts, added skip or xfail, and rewritten steps.

- `supervision_then_workers.py` `one_at_a_time` ("no worker was started before the one before it had ended") was
  removed. It proved the global start/end alternation. The plan lists it in §4 (decision 1), and only the retired @r1
  scenario used it.
- `test_supervision.py` `merged_in_line` ("the initiative branch has both implementers' commits, one after the
  other, with no merge commit") was removed. It proved two implementer commits and no merge commit. The plan lists it
  in §4, and only the retired @r20 scenario used it. Its proof is now inside the stronger r61 Then
  (`merged_in_end_order`).
- `stub_claude.meet` was refactored onto `wait_until`. The condition is unchanged (count of starts of the agent ≥ n,
  within a minute). Not weakened.
- `implementers_commit_own` gained an optional `order` group. The existing texts behave as before.

Grep for remaining uses of the removed steps or of `pair`, `together` and `supervise.claimed` in code and tests:
none.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: the only tests removed are the
Retires removals above.

## Cannot verify

- The report's red counts (8 failed, 143 passed), the green run (148 passed, 1 skipped), the `--whole-suite` run of
  the module (135 passed) and "module run three more times: green". I only re-ran the 8 new or changed side-by-side
  scenarios once (all passed).
- Decision 6 (faults while other stages are in flight: drain, then r40's error) has no scenario with stages running
  side by side. I verified it by reading only:
  - `Pool.pull` starts nothing once `self.faults` or `errors` is set, waits for `running` to empty, joins the
    threads and raises the first error.
  - `step` and `implement` turn a `Fault` or `GitFailed` into `fail`.
- r62 against the real Claude Code store layout (`projects/*/<session>.jsonl` under `$CLAUDE_CONFIG_DIR` or
  `~/.claude`). Only the stand-in's layout is exercised.

## Risks named and verified

- **r61 order race:** could log order and merge-queue order differ? No. The append to `finished` happens under
  `self.lock`, the same lock `log()` takes, in the same block as the end log line (`supervise_worker.py` worker,
  end block).
- **Merge-queue deadlock:** `await_turn` is called outside `self.lock` (`supervise_merge.py` `claimed`).
  `release` runs in `finally` on every path: non-DONE outcome, a `Fault` after the end line (r28 change, r45 cut
  short), and a merge failure. So an implementer ahead in `finished` always lets the next one go.
- **blocked_by guarding planned → ready:** is this behaviour no line asks for? No. Decision 0039's lifecycle table
  guards planned → ready with "every `blocked_by` green", so it is the lifecycle's guard, which the Implementation
  section allows.
- **New refusal for a malformed `.shop/delivery.toml` or a bad `workers`:** this is r10 ("cannot start the delivery
  … exit with an error, say why, and change nothing"). It is read in `check()` before the push verification and
  before any log line.
- **Claim overlap:** a non-implementer's claim is `set()` and overlaps nothing. An implementer with no fileset
  (`None`) overlaps every other implementer, as `pair` did before.

## Findings

1. **Minor — observation.** Work-item: w109. `scripts/supervise_merge.py:103-105` together with
   `scripts/supervise_pool.py` `choose_locked` and `scripts/supervise_worker.py` `worker`.
   - **What is wrong:** a merge holds `self.lock` (an RLock) through rebase, scenarios and the whole suite. The
     pool's choice of items, and every worker's start and end bookkeeping, take that same lock. So while one branch's
     suite runs, no new worker starts and no ending worker records its end.
   - **Why it matters:** this does not break r59, r60 or r20. It does serialize research and planning behind each
     merge's suite, which works against the initiative's aim (faster batches). The implementer flagged it too.
   - **Reproduction:** found by reading the code (`with self.lock:` around `self.merge(name, tree, tests)`, which
     runs the suite). No scenario measures it.
   - **Fix:** run the suite outside `self.lock`. The merge queue (`await_turn`) already gives one merge at a time,
     so the lock is needed only for the main checkout's commit and push.
2. **Minor — observation.** Work-item: w109. `scripts/supervise_worker.py` `with_transcript`.
   - **What is wrong:** when the store holds no transcript for the session id, or claude's output is not a JSON
     object, `session.json` is written without `transcript_path`, and nothing says so.
   - **Why it matters:** r62 says "shall record". Under a real `claude -p` the transcript exists, so no client hits
     this today. `measure` reading a `session.json` without the key will need its own fallback.
   - **Reproduction:** reading the code (`if not found or not isinstance(data, dict): return stdout`). It is the
     plan's open case 1, answered in the report's Open questions.
   - **Fix:** if it matters, state in the capability's Implementation section what is recorded when no transcript
     is found.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w109 ready -> claimed$"` → `e8a6dda`. `work/w109` is not a revision
  (the branch is gone).
- `git log --format='%H %s' -1 --grep="^work: w109 claimed -> done$"` → `2ee80c4`. `git log --oneline -12`.
- `git show --stat 4232bc6`
- `git diff e8a6dda 4232bc6 -- features/`, `-- scripts/ CLAUDE.md`, and `-- tests/`
- `git show 4232bc6:scripts/supervise_worker.py`, `git show 4232bc6:scripts/supervise_merge.py` and
  `git show 4232bc6:scripts/supervise.py` (excerpts)
- `grep` of the capability's lines, of `blocked_by` in `spec/decisions/`, and of the r63 scenario
- Grep for remaining uses of the removed steps and functions: none in code or tests.
- `python3 <Scripts>/tools check --base e8a6dda…`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300`: no output, so no file is over the limit.
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "same_time or blocked_by or transcript or at_most"
  -p no:cacheprovider`: 8 passed.
- `git status --short`: clean.
