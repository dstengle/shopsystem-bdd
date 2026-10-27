# Review of w210 (supervision r135, r136)

**Verdict: DONE_WITH_CONCERNS.** Two Important findings are triaged fix now, both in the failed-raise path of
`supervise_rounds.py`:
1. The `git reset --hard` that undoes the round's merge runs on the checkout that every initiative shares. It can throw
   away commits that other runs merged in the meantime, and every run's uncommitted `log.jsonl` lines.
2. A failed raise commits the round's stage directory. The person ruled that it commits nothing from the round.

The raise itself, `--raised-for`, the record and the hold under r136 match the plan and the lines.

## Commits reviewed

The branch `work/w210` is gone. The commits are the ones between `d2389cc0 work: w210 ready -> claimed` and
`b815fce9 work: w210 claimed -> done` on HEAD, without `work run`'s own commits:

- `b762072b` work run raises an integrate round's lines into the upstream and holds the proposal until delivered (r135, r136)
  - CLAUDE.md, scripts/supervise_draft.py, scripts/supervise_raise.py (new), scripts/supervise_rounds.py, scripts/work,
    scripts/workqueue_request.py, tests/scenarios/supervision_raise_steps.py (new),
    tests/scenarios/supervision_rounds_steps.py, tests/scenarios/test_supervision.py

This is the one commit the implementer's result.json lists, so they agree. Nothing under `features/` changed.

## Removed and weakened tests

None found. I read the whole diff, looking for:
- a deleted `def test_` or step function;
- a removed or loosened `assert`;
- a parametrize case dropped;
- an added `skip` or `xfail`.

The only test file modified (not just added to) is `supervision_rounds_steps.py` `proposed_fulfilling`. It is a setup
change and is covered under Allowances.

## Allowances

- `tests/scenarios/supervision_rounds_steps.py` `proposed_fulfilling` (setup): **holds.**
  - The diff writes a `delegation:` field into q1 only when the step text has "which gives the delegation".
  - It adds, removes and changes no `assert`, no expected value and no parametrize case.
  - The file is outside the work-item's file set, and the report says so.

## Cannot verify

- The report's green runs: `--work-item w210` 152 passed; `--whole-suite` on four modules 370 passed and 25 xfailed. I
  did not re-run the suite; `work run` runs it before it merges.
- The report says spec-integration @r44 (`features/spec-integration.feature:5`) passes unchanged.
  - From the code: its billing upstream is no git repository, so the raise now fails. `work run` in that scenario now
    exits with an error and writes no proposal.
  - Its Thens read only the brief and the kept result, so it would still pass, but the run it narrates now ends in an
    error. Not verified by a run.
- Plan part 5: whether requests @r29 and @r31 now pass while r122 counts them as expected to fail (strict xfail).

## Findings

### 1. Important, fix now (w210): the undo of a failed raise is a `git reset --hard` on the shared checkout

**Where:** `scripts/supervise_rounds.py:130` (`head` read), `:157` (the raise, outside `self.lock`), `:161-162`
(`git reset -q --hard head`).

**What is wrong:**
- `work run` with no initiative runs every open initiative in its own thread on one checkout (`supervise.py:65`, "the
  runs of one `work run` with no initiative, which share the checkout"; `supervise_all.py:46` gives them one shared
  `lock`).
- The round reads `head` and merges under the lock, then lets the lock go. The raise then writes and commits a request
  in another repository.
- While the lock is free, another initiative's pool can merge an implementer's work and commit on the same branch.
- On a failed raise, `reset --hard head` throws those commits away.
- It also reverts every uncommitted change to tracked files in the checkout. That includes the `log.jsonl` lines each
  run has appended and not yet committed (`self.unlogged`, which `supervise_faults.py:110-119` takes care to keep, for
  every run in `self.group`).
- So the round's own log lines are lost before `keep_round` commits `log.jsonl`, and `self.unlogged` no longer matches
  the file.

**Why it matters:** commits and log lines are lost, and the commits may belong to other initiatives.

**What I verified:** by reading only, with no probe run:
- the threads and the shared lock in `supervise_all.py:46,63-71`;
- that the lock is not held over the raise in `supervise_rounds.py:154-163`;
- the log handling in `supervise.py:94-108`.

**Fix:** plan decision 8 gives the first option.
- Preferred: run the r96/r107 checks and the raise before the merge, from the round's result, which is already read
  before it. A failed raise then has no merge to undo.
- Otherwise: hold `self.lock` from the merge until the raise is decided, and undo only the merge (for example
  `git reset --keep`, and only when HEAD is still the merge commit). Never use `--hard`.

### 2. Important, fix now (w210): a failed raise commits the round's stage directory, against the ruling

**Where:** `scripts/supervise_rounds.py:163` (`self.keep_round(name, kind, label)`).

**What is wrong:**
- The person answered r135 with reading C: "write no proposal and commit nothing from the round, then exit with an
  error … as r10 does" (r10: "change nothing").
- Plan decision 9 says the same, and leaves `.shop/work/` as its last commit has it.
- The implementer instead commits the stage directory and the log lines as `work: <name> integrate round <label>
  faulted`. That commit includes the `request-lines-<n>.md` files the raise wrote.
- The report says why (r46 would refuse the next run on what is left uncommitted). The plan had asked for the stage
  directory not to be left behind uncommitted, not for it to be committed.

**Why it matters:** what the person sees differs from the ruling: there is a commit from the round. A ruling decides
this, not the implementer.

**Fix:** do one of these:
- follow decision 9: remove the round's uncommitted stage directory and put `log.jsonl` back as committed plus the
  lines not from this round, then commit nothing;
- or take the r96 precedent to the person as a change to the r135 ruling.

### 3. Important, observation (w210): a raise that fails after an earlier one succeeded leaves an unrecorded request upstream

**Where:** `scripts/supervise_raise.py:36-51`.

**What is wrong:**
- With two `requests` entries, the first `work request` writes and commits q<n> in its upstream. The second fails.
- The round then records nothing (reading C), so no record line holds anything for q<n>.
- The round runs again on the next run and raises the same lines again, which leaves a duplicate request in the first
  upstream.

This is plan part 5's open case. No scenario reaches it and no client sends two upstreams today.

**Reproduction:** none run. From reading the code: the loop raises Refused on the second entry after
`workqueue_request.request` has committed in the first upstream (`workqueue.py:268-283`).

**Fix:** check every entry before writing any request (the upstream root, strict form, delegation). Alternatively,
record the requests already raised before refusing.

### 4. Important, observation (w210): a proposal re-drafted by a later integrate round loses its hold

**Where:** `scripts/supervise_raise.py:79-84` together with `scripts/supervise_change.py:114-116`.

**What is wrong:**
- `waits` finds the round that raised a request through the text "The drafts of this proposal are in <round>."
- When an r140 round re-drafts the proposal, `write_proposals` replaces that sentence with the new round's path.
- If the new round raised nothing, the proposal no longer names the round that raised the undelivered request. The
  proposal's work-items are then drafted, against r136.

This is plan part 5's open case. No scenario pins it.

**Reproduction:** none run; found by reading the code.

**Fix:** tie the hold to the proposal (record its name or id in the `raised.jsonl` line), or carry the earlier rounds
forward when re-drafting.

### 5. Minor, drop: ruff I001 in a touched file

**Where:** `tests/scenarios/test_supervision.py:14`.

The import block was already unsorted at the claim commit (`supervision_review_steps` before
`supervision_reintegrate_steps`). The added line is in its sorted place, so this commit did not cause it.

## Checks

- `tools check --base d2389cc0`:
  - ruff: 1 error, I001 in tests/scenarios/test_supervision.py:14, already there before (finding 5);
  - vulture: clean;
  - import-linter: "the project states no import contracts".
- `tools size --limit 300`: printed nothing. No tracked Python file is over the limit.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w210 ready -> claimed$"` (and the same for `claimed -> done`)
- `git log --format='%H %s' --stat d2389cc0..b815fce9`
- `git show b762072b`
- `git show b762072b:scripts/supervise_rounds.py | sed -n 90,240p`
- `git show d2389cc0:tests/scenarios/test_supervision.py | grep -n "^from \.supervision_r"`
- `grep` / `sed` reads of:
  - scripts/supervise.py, supervise_all.py, supervise_faults.py, supervise_change.py, supervise_answers.py,
    supervise_brief.py, workqueue.py, workqueue_request.py;
  - spec/capabilities/supervision.md, spec/capabilities/requests.md;
  - features/spec-integration.feature.
- `python3 <Scripts>/tools check --base d2389cc079e0c05b71c91e58605e5d499676c87a`
- `python3 <Scripts>/tools size --limit 300`
