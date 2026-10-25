# Branch review of i26 (a request's questions and answers through work), review 5

**Verdict: DONE.** No finding is Critical, none is triaged fix now, and I ran every check.

- i26's code is unchanged since review 4 (`307f8496`). None of the 48 commits since then touches a file of w177's or w178's (scripts/workqueue_request.py, scripts/work, scripts/supervise_intake.py, scripts/supervise_all.py, their step modules, features/requests.feature, spec/capabilities/requests.md or supervision.md). The diff of `scripts/supervise.py` and `tests/scenarios/test_supervision.py` since `307f8496` is i29's and i30's (r105, r109, r110), outside i26's hunks.
- The Important observation from reviews 2-4 still stands, unaddressed: r9, r82 and r101 say "in the asker's turn", but the code counts only `awaiting-asker` requests (reading B, which w178's Answer chose).
- The suite has 10 failures, all of them i31's scenarios, whose work-item w185 is still `drafted`.

## Range and work-items

- **Range:** `f582b1bb..35ed351a` on `i25-review-findings-to-implementation`, 499 commits. The base, `f582b1bb`, is the commit that added `.shop/work/i26/initiative.md`.
- **Shared branch:** the branch is shared with i25 and i27-i31. Their commits are attributed to them and not re-reviewed here.
- **w177** (requests; accepts r20, r21, r4, r5, r12), green. One commit, `db4d07f2`, between `87424bc6 work: w177 ready -> claimed` and `1e8ddfdc work: w177 claimed -> done`.
- **w178** (supervision; accepts r100, r101, r9, r67, r82), green. One commit, `641f95a9`, between `da0bfcde work: w178 ready -> claimed` and `d959d612 work: w178 claimed -> done`.
- **i26's commits outside any work-item** are the same as at review 4, and none changes code:
  - the rounds: spec `5c441e9e`, `d07a8b38` and features `3d3da4df`, `46fef129`;
  - `986dbcbb`, a hand edit of the proposal ids, with its reason given;
  - `cebadf9d`, the measurement and analysis record;
  - the gate helper `.shop/work/i26/runs/supervision/1-gate/mk.py` (finding 3);
  - `11c19108` and `fd46e0aa`, branch reviews 3 and 4.

## Suite

`Suite: 885 passed, 10 failed at 35ed351a in 56.6 s`

- **Command:** `python3 -m pytest -q -p no:cacheprovider`. pytest also reported 1 skipped and 56 subtests passed, and gave 55.89 s itself.
- **Parallel:** yes. `pytest.ini` sets `addopts = -n auto`.
- **In-process:** no. The steps drive `scripts/work` through `subprocess.run` (`tests/scenarios/conftest.py`). The suite is under 60 s, so this is not a finding, but it is now close to 60 s (32.2 s at review 4); see Observations.
- **The failures, none of them i26's:** they are all i31's scenarios, and w185 is `drafted`:
  - `StepDefinitionNotFoundError` on r114 (`features/supervision.feature:972`), r112, r113, the new r83 (`:1242`), r116 and r111;
  - the r115 outline (`:1295`), 4 of its cases.

## Checks

- **w177** `python3 -m pytest -q -rfEx -p work_items --work-item w177`: 148 passed, 1 skipped, 56 subtests passed.
- **w178** `python3 -m pytest -q -rfEx -p work_items --work-item w178`: 149 passed, 1 skipped, 56 subtests passed.
- **`tools check --base f582b1bb`, ruff:** 34 errors.
  - i26's:
    - `tests/scenarios/test_supervision.py:14` I001, from w178 (finding 2);
    - `.shop/work/i26/runs/supervision/1-gate/mk.py:1` I001 and `:19` SIM115 (finding 3).
  - Not i26's:
    - the helper scripts of i29, i30 and i31 under `.shop/work/i29|i30|i31/runs/`;
    - `scripts/supervise_analysis.py:4` I001 and `scripts/supervise_brief.py:89` ISC004;
    - `tests/scenarios/supervision_all_steps.py:127`;
    - `tests/scenarios/supervision_intake_steps.py:84`, which is i28's line, outside w178's hunks;
    - `tests/scenarios/supervision_proposal_steps.py:118`;
    - `tests/scripts/stub_claude.py:189,190`;
    - `tests/scripts/test_supervise_change.py:7`.
- **`tools check`, vulture:** clean.
- **`tools check`, import-linter:** "the project states no import contracts". I read the imports for myself:
  - w178 adds `import workqueue_request` to `supervise.py` and `supervise_intake.py`. That is supervise depending on the work library, the direction the module map gives.
  - There is no cycle: `workqueue_request` imports no `supervise*` module.
- **`tools size --limit 300`:** no output. No file is over the limit.
- **`features deprecated`:** 5 scenarios, none of them i26's:
  - `migration-tools @r15`, `work-queue @r1` and `@r9`, all from before the base;
  - `supervision @r102` (i28). Its replacement's work-item, w171, is green, which is a finding for i28;
  - `supervision @r83` (i31). Its replacement's work-item, w185, is drafted.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** no operation i26 touches has a dry-run mode. Not applicable.

## Removed and weakened tests

None outside the Retires lists. This is unchanged since review 4, because no commit since touches i26's tests or `features/requests.feature`.

What I searched `db4d07f2` and `641f95a9` for:

- `features/` lines;
- removed `def`, step decorators and `assert` lines;
- parametrize and Examples rows;
- `skip` and `xfail`.

What I found:

- **`features/`:** the only removals are the six `@deprecated` scenarios the work-items list under Retires:
  - w177: requests @r4, @r5 and @r12;
  - w178: supervision @r9, the @r67 outline and @r82.
- **w178, `supervision_intake_steps.py`:** it removed `intake_writes`, `JUDGED` and `lines_have_outcomes`, steps that served only the retired r67 outline.
  - Plan section 4 lists them.
  - The new `intake_started` keeps every old condition, so it is stronger.

## Allowances

Both reports give "none" under `## Tests changed under an allowance`. There is nothing to hold.

## Cannot verify

- **Probe:** I wrote a probe of the pure helpers behind `work ask` and `work reply` (`_entries`, `_with_entries`, `_numbered`) in `.shop/scratch/i26-branch-review/probe.py`.
  - Running it needed shell approval in this non-interactive session, so it did not run, as in reviews 2-4.
  - The scratch directory is deleted.
  - The Observations' reproductions are therefore read from the code. This affects only hardening observations, not a work-item's check.
- **Working directory:** one of my early read-only shell commands left the shell in a subdirectory of the worktree. I changed back to the worktree root before running anything else, and nothing was written.

## Findings

### 1. Important (w178): r9, r82 and r101 say "in the asker's turn"; the code reads only `awaiting-asker`

- **Triage:** observation.
- **Where:** the code is `scripts/workqueue_request.py:50` (`if status == "awaiting-asker" and field(text, "asker") in mine`). The lines it disagrees with:
  - r9 at `spec/capabilities/supervision.md:83`;
  - r101 at `:84`;
  - r82 at `:88`;
  - r101's Implementation line at `:167`.
- **What is wrong:** take a request kept here whose asker is `internal`, which the upstream has settled (`accepted`, `refused` or `delivered`, `turn: asker`).
  - Read literally, r101 says `work run` exits with an error. The code exits successfully, which r9 and r82, read literally, forbid.
  - No Implementation line narrows "in the asker's turn" to `awaiting-asker`.
- **Why it matters:** by the decision taken, this is not a wrong answer. The code follows w178's Answer (reading B, given by the coordinator under the person's delegation). But the lines and the code disagree, and the next reader will take the lines' words.
- **Fix:** write reading B into r101's Implementation line, or into r9, r82 and r101, through integrating-a-proposal. For example: "a request kept in this context whose asker is this context and whose status is `awaiting-asker`".
- **Since review 4:** still unaddressed. No work-item or round on the branch takes it up.

### 2. Minor (w178): a new import out of order

- **Triage:** observation (cheap: `ruff check --fix`).
- **Where:** `tests/scenarios/test_supervision.py:37`. The line `from .supervision_request_steps import *` comes after `supervision_review_steps` (`:36`). ruff reports I001 for the import block at line 14.
- **Why it matters:** `tools check` is not clean on a file the branch touched.
- **Fix:** move line 37 above line 36.

### 3. Minor (no work-item: i26's supervision gate round): a session's helper script is committed

- **Triage:** observation.
- **Where:** `.shop/work/i26/runs/supervision/1-gate/mk.py`.
- **What is wrong:** a gate session's scratch helper is tracked. i29, i30 and i31 do the same, and 25 of ruff's 34 errors are in such helpers.
- **Why it matters:** it is tracked Python that ruff checks and that no line asks for, and it hides the code's own lint results.
- **Fix:** either keep stage directories to the brief, the result, the session and kept files, or exclude `.shop/` from `tools check`'s ruff run.

## Shape

Each CLAUDE.md rule and module-map row i26 touched:

- **Size limit 300:** met. `tools size` prints nothing.
- **`scripts/workqueue_request.py` row:** met.
  - CLAUDE.md:27 names `ask` and `reply` (`workqueue_request.py:129`, `:139`).
  - `asked_here` (`:40`) reads this context's own requests.
- **`scripts/supervise*.py` row:** met.
  - `asked` is called from `Run.run` and from `run_all` (`supervise_all.py`).
  - The intake questions are written in `supervise_intake.py:89-99`.
- **`scripts/work` row:** met. The `ask` and `reply` parsers and handlers are in `scripts/work`.
- **`tests/scenarios/` row:** met. `supervision_request_steps.py` holds one concern.
- **Decision 0067 (requests are written through work):** met. The intake writes its questions through `workqueue_request.ask`, which commits through `_change`.
- **Code no line asks for:** none found.
  - `ask` and `reply` serve requests r20 and r21.
  - `asked` and `asked_here` serve r101, r9 and r82.
  - The intake's question writing serves r100.
  - The exit code 3 is mechanism: it is the error code `work run` already uses.
- **Unreached code or steps:** none left by i26.
  - vulture is clean.
  - Every i26 step is reached in the w177 and w178 check runs.

## Coupling

i26 adds no dependency on another project.

- It relies on the `git` CLI's merge in `Intake.take` (`supervise_intake.py:89-99`):
  - the questions are committed on the main checkout;
  - then the round branch, which edits `## Outcomes` and the front matter, is merged.
- That merge stays conflict-free only while `## Answers` separates `## Questions` from `## Outcomes`.
- A conflict faults the round, aborts the merge and resets to the head from before the questions. That is a refusal, with no data lost.
- **What would make it stable:** write the questions on the round branch before the round's `work turn`, as r100's Implementation line reads, instead of relying on the hunks staying apart.

## Observations

- **w177, `reply` (`workqueue_request.py:139-145`; `_numbered` at `:82-84`):** `reply` checks only the turn.
  - An answer is written to a question that does not exist. Reproduction, read from the code: `work reply q1 7 seven` on a request with one question writes `7. seven`.
  - A second answer to a question replaces the first. Reproduction, read from the code: `work reply q1 1 first`, then `work reply q1 1 second`, leaves only `1. second`.
- **w177, `ask` (`:129-136`):** a question is accepted on a line the request does not have. Reproduction, read from the code: `work ask q1 9 x` on a two-line request writes `1. line 9: x`.
- **w177, multi-line `ask` and `reply` text:** the text is written as given. No client sends such text today.
  - A forged `## Outcomes`: `work reply q1 1 $'x\n\n## Outcomes\n1. accepted\n2. accepted'` puts it before the real one. `_entries` (`:27`) takes the first such heading, so `accepted_lines` reads the forged outcomes. The asker then writes the upstream's part, against requests r5.
  - A crash: an answer `a\nb`, followed by any later `reply`, raises `ValueError` in `_numbered` (`int("b")`). That is a crash where a refusal belongs.
  - Fix: a line that refuses multi-line question and answer text, then the refusal.
- **w178 (`supervise_intake.py:92-94`):** the round faults when a result question does not start with `<n>. ` or names a line the request does not have. The request stays as it was. That is a refusal (plan section 5, open case 1).
- **Not i26 (the suite's time):** the suite took 56.6 s at `35ed351a`, against 32.2 s at review 4. It is still parallel and under 60 s, but the steps run `scripts/work` by subprocess. One more batch of scenarios at this rate would push it past 60 s, which would be a finding. Reproduction: `python3 -m pytest -q -p no:cacheprovider` gives "10 failed, 885 passed ... in 55.89s".
- **Not i26 (i28/w171):** the deprecated `supervision @r102` scenario is still there while its replacement's work-item is green (`features deprecated`).
