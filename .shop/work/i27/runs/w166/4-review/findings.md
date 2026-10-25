# Review of w166 (work-queue#r25): work start commits the initiative

**Verdict: DONE.** No Critical finding and nothing to fix now. There is one Minor observation (the commit message's form).

## Commits reviewed

The branch `work/w166` is gone. So the commits are the ones between `117402c4 work: w166 ready -> claimed` and `1a6567bd work: w166 claimed -> done` on HEAD, without `work run`'s own `work:` commits.

- `5c876c93 work start commits the initiative it writes (work-queue r25)`. It changes `scripts/workqueue_start.py`, `tests/scenarios/work_queue_git_steps.py` and `tests/scenarios/work_queue_start_steps.py`, all three in the work-item's fileset.
- The commits between those two that belong to w164 and w165 are not w166's: `0605672a`, `34ee952c`, `f547d55e` and `b57fdf6f`.

The implementer's result lists `9b8def0e`, whose parent is the claim commit. `git diff 9b8def0e 5c876c93` over the three files is empty, so `5c876c93` is the same change merged. There is no difference to report.

## Removed and weakened tests

None.

What I searched for:
- **Under `features/`:** no change.
- **Deleted test functions, parametrize cases, assertions, skips and xfails:** none in the diff.
- **`new_commit_holds`:** it gains a path resolution for the "the new initiative's …" phrases. Any other phrase passes through unchanged, so every existing use asserts what it did before.
- **`nothing_uncommitted` and `request_uncommitted`:** they gain `context`, and their assertions are unchanged. `request_uncommitted` is their only caller (grep).
- **The r25 directory phrase:** it now has to resolve to exactly one new initiative directory that exists. Before, the step passed on a path that did not exist. That makes the test stronger.
- **The r22 Given:** "a request q1 that is accepted…" now also writes `spec/index.md` (INDEX). In r22 this is the same text the `initiative` Given already writes, so r22's assertions are unchanged.

## Allowances

The report gives none. Its reason is that the Given's setup belongs to the r25 scenario itself. The Given is shared with r22, but the change adds no assert, expected value or case there, so no allowance was needed. Both r22 and r25 pass (see the commands below).

## Cannot verify

- **Commit refused (no git identity, a hook rejects it).** No test covers it, and probing it here would mean committing into this worktree. From reading the code: `workqueue.committed` unlinks `initiative.md` and resets the index, and `start` then removes the empty `i<n>/` directory. The plan's decision 1 holds on reading.
- **A directory that is not a git repository is refused before writing.** Not probed, because a scratch directory here sits inside this worktree's git repository. On reading, `committed` runs `git rev-parse --is-inside-work-tree` before `write()`. All of `start`'s own refusals (`entry`, request missing, not accepted, `context_path`) run before `committed`.
- **Detached HEAD and D1** (an existing `i<n>/` with no `initiative.md` raises `FileExistsError`). These are open cases the plan and report name. D1 is older than this change and is not caused by it.

## Findings

### 1. Minor (observation): the commit message uses `work run`'s `work: ` prefix (scripts/workqueue_start.py:48)

- **What is wrong:** `start` commits with `"work: start %s, fulfilling %s"`. Every other `work` writer uses `work <command>: …` (`work add:`, `work note:`, `work answer:`, `work request:`, `work resolve:`, `work withdraw:`, `work retry:`). The plan asked for "the style of the other writers' messages". The bare `work: ` prefix is the one `work run`'s own commits use (`supervise.py:103`, `supervise_intake.py:109`, `supervise_rounds.py:102`, `supervise_merge.py:65`).
- **Why it matters:** `measure_build.py:88` drops every commit whose subject starts with `work: ` as `work run`'s own. The review procedure also leaves out "work run's own `work:` commits". So a `work start` commit inside a measured window is counted as a supervisor commit and not as work.
- **Reproduction:** `grep -rn '"work [a-z]*:\|"work: ' scripts/*.py` lists the forms above. `measure_build.py:88` has `if not sub.startswith("work: ")`. No line or scenario names the message, so this is hardening, not a wrong answer today.
- **Fix:** `"work start: %s, fulfilling %s"`.

### Not this work-item's

`tools check` reports a vulture warning at `tests/scenarios/requests_write_steps.py:76` (unused variable `named`). That file is outside w166's commits.

## Checks

- **Behaviour against r25, r22 and r7:** consistent. `start` commits only the new `initiative.md` on the current branch through `workqueue.committed`, so others' staged changes stay out of the commit. A failed commit leaves nothing behind. Refusing to start outside git is r7's refusal of something `work` cannot do.
- **Code no line asks for:** none.
- **`tools check --base 117402c4`:**
  - ruff: all checks passed.
  - vulture: one warning, in a file outside w166.
  - import-linter: the project states no import contracts.
- **`tools size --limit 300`:** prints nothing.

## Commands run

- `git log --grep="^work: w166 "` and `git log 117402c4..1a6567bd` (the branch `work/w166` no longer exists)
- `git show 5c876c93`, `git diff 9b8def0e 5c876c93 --stat -- <the three files>` (empty), `git log -1 9b8def0e`
- `grep` for the callers of the changed steps, for `new_initiatives`, and for the commit-message forms
- `python3 -m pytest tests/scenarios/test_work_queue.py --whole-suite -k start -rA -q`: r22 and r25 PASSED (7 passed)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 117402c45f5c869b760d2af50d66dfd50f569148`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
