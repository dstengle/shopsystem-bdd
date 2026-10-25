# Branch review of i26 (a request's questions and answers through work), review 4

**Verdict: DONE.** No finding is Critical, none is triaged fix now, and I ran every check.

- The Important observation from review 3 still stands, unaddressed. r9, r82 and r101 say "in the asker's turn", but the code counts only `awaiting-asker` requests (reading B, which w178's Answer chose).
- The suite has 19 failures (one run also had a 20th). None is i26's:
  - 18 are `StepDefinitionNotFoundError` on scenarios of i29, i30 and i31 whose work-items are not green;
  - one is i30's new r19 scenario (80 turns), which is not implemented: its work-item, w182, was withdrawn and redrafted as w184;
  - the 20th was i27's r95 scenario, failing under load only. It passes alone.
- i26's code is unchanged since review 3 (`eca9d404`). One later commit touches an i26 file: `959cba20` (i29/w175, requests r22) adds two lines to `scripts/workqueue_request.py:93-94`, outside i26's functions.

## Range and work-items

- **Range:** `f582b1bb..307f8496` on `i25-review-findings-to-implementation`, 450 commits.
  - The base, `f582b1bb`, is the commit that added `.shop/work/i26/initiative.md`.
- **Shared branch:** the branch is shared with i25 and i27-i31. Their commits are attributed to them and not re-reviewed here.
- **w177** (requests; accepts r20, r21, r4, r5, r12), green.
  - One commit, `db4d07f2`, between `87424bc6 work: w177 ready -> claimed` and `1e8ddfdc work: w177 claimed -> done`.
- **w178** (supervision; accepts r100, r101, r9, r67, r82), green.
  - One commit, `641f95a9`, between `da0bfcde work: w178 ready -> claimed` and `d959d612 work: w178 claimed -> done`.
- **i26's commits outside any work-item** (as in review 3):
  - its rounds: spec `5c441e9e`, `d07a8b38` and features `3d3da4df`, `46fef129`;
  - `986dbcbb`, a hand edit of the proposal ids, with its reason given;
  - `cebadf9d`, the measurement and analysis record;
  - the gate helper `.shop/work/i26/runs/supervision/1-gate/mk.py` (finding 3);
  - `11c19108`, branch review 3.
  - None changes code.
- **Since review 3:** `git diff --stat eca9d404 HEAD -- scripts tests features CLAUDE.md spec` touches only:
  - `scripts/supervise_worker.py` (i29/w179);
  - `scripts/workqueue_request.py` +2 and `tests/scenarios/requests_write_steps.py` +5 (i29/w175);
  - `tests/scenarios/supervision_given.py` (i29/w179);
  - `features/supervision.feature` and `spec/capabilities/supervision.md` (i30's and i31's rounds).
  - None of i26's hunks changed. r9, r82, r100, r101 and their Implementation lines are as review 3 read them.

## Suite

`Suite: 876 passed, 19 failed at 307f8496 in 32.2 s`

- **Command:** `python3 -m pytest -q -p no:cacheprovider`. It also gave 1 skipped and 56 subtests passed. Wall time was 32.8 s.
- **Parallel:** yes, `-n auto` (1225 % CPU).
- **In-process:** no. Steps drive `scripts/work` through `subprocess.run` (`tests/scenarios/conftest.py`). The suite is under 60 s, so this is not a finding.

The failures, none of them i26's:

- **i30 (w184, drafted after w182 was withdrawn):**
  - r19 at 80 turns, an `AssertionError` at `supervision_then_workers.py:218`;
  - r110, r117: `StepDefinitionNotFoundError`.
- **i31 (w185 drafted, w183 withdrawn):** r111, r112, r113, r114, r116, the new r83, and r115 ×4, all `StepDefinitionNotFoundError`.
- **i29 (w181):** r105, r106, r107, r108 [gate] and [apply], and r109, all `StepDefinitionNotFoundError`, as at review 3.
- **i27 (r95):** `test_work_run_started_with_no_initiative_runs_the_integrate_apply_and_formulate_rounds_of_different_initiatives_one_at_a_time` failed in one of my two full runs and passed when run alone. It is flaky under load and not i26's (see Observations).

## Checks

- **w177** `python3 -m pytest -q -rfEx -p work_items --work-item w177`: 147 passed, 1 skipped, 56 subtests passed.
- **w178** `python3 -m pytest -q -rfEx -p work_items --work-item w178`: 148 passed, 1 skipped, 56 subtests passed.
- **`tools check --base f582b1bb`, ruff:** 33 errors (22 at review 3; the 11 new ones are i30's and i31's helper scripts under `.shop/work/i30|i31/runs/`).
  - i26's: `tests/scenarios/test_supervision.py:14` I001, from w178 (finding 2).
  - i26's: `.shop/work/i26/runs/supervision/1-gate/mk.py:1` I001 and `:19` SIM115 (finding 3).
  - Not i26's:
    - `.shop/work/i29`, `i30` and `i31` helper scripts;
    - `scripts/supervise_brief.py:84` ISC004;
    - `tests/scenarios/supervision_all_steps.py:111,127`;
    - `tests/scenarios/supervision_intake_steps.py:84` (i28's line, outside w178's hunks);
    - `tests/scenarios/supervision_proposal_steps.py:96`;
    - `tests/scripts/stub_claude.py:186,187`.
- **`tools check`, vulture:** clean.
- **`tools check`, import-linter:** "the project states no import contracts".
  - I read the imports for myself: w178 adds `import workqueue_request` to `supervise.py` and `supervise_intake.py`. That is supervise depending on the work library, which is the direction the module map has. There is no cycle: `workqueue_request` imports no `supervise*`.
- **`tools size --limit 300`:** no output. No file is over the limit.
- **`features deprecated`:** 6 scenarios, none of them i26's:
  - `migration-tools @r15`, `work-queue @r1` and `@r9`, all from before the base;
  - `supervision @r102` (i28; its replacement's work-item, w171, is green, a finding for i28);
  - `supervision @r19` (i30) and `@r83` (i31), whose replacements' work-items are not green.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** no operation i26 touches has a dry-run mode. Not applicable.

## Removed and weakened tests

None outside the Retires lists. What I searched `db4d07f2` and `641f95a9` for:

- `features/` lines;
- removed `def`, step decorators and `assert` lines;
- parametrize and Examples rows;
- `skip` and `xfail`.

What I found:

- **`features/`:** the only removals are the six `@deprecated` scenarios the work-items list under Retires:
  - w177: requests @r4, @r5, @r12;
  - w178: supervision @r9, the @r67 outline, @r82.
  - No `features/` line was added or edited.
- **w178, `tests/scenarios/supervision_intake_steps.py`:** it removed `intake_writes`, `JUDGED` and `lines_have_outcomes`.
  - These steps served only the retired r67 outline, and plan section 4 lists them.
  - The new `intake_started` keeps every old condition and adds two, so it is stronger.
  - `line_one_has_outcome` replaces `lines_have_outcomes` for the new r67 scenario, whose line 2 gets a question rather than an outcome.

## Allowances

Both reports give "none" under `## Tests changed under an allowance`. No test outside Retires changed, so there is nothing to hold.

## Cannot verify

- **Probe:** I wrote a probe of the pure helpers behind `work ask` and `work reply` (`_entries`, `_with_entries`, `_numbered`) in `.shop/scratch/i26-branch-review/probe.py`.
  - Running it needed shell approval in this non-interactive session, so it did not run. Reviews 2 and 3 hit the same.
  - The scratch directory is deleted.
  - The Observations' reproductions are therefore read from the code, with the lines named. This affects only hardening observations, not a work-item's check.

## Findings

### 1. Important (w178): r9, r82 and r101 say "in the asker's turn"; the code reads only `awaiting-asker`

- **Triage:** observation.
- **Where:** `scripts/workqueue_request.py:50` (`if status == "awaiting-asker" and field(text, "asker") in mine`), against:
  - r9 at `spec/capabilities/supervision.md:83`;
  - r101 at `:84`;
  - r82 at `:88`;
  - r101's Implementation line at `:167`.
- **What is wrong:** take a request kept here, whose asker is `internal` and which the upstream has settled (`accepted`, `refused` or `delivered`, `turn: asker`).
  - Read literally, r101 says `work run` exits with an error.
  - The code exits successfully, which r9 and r82, read literally, forbid.
  - The Implementation line for r101 does not narrow "in the asker's turn" to `awaiting-asker`.
- **Why it matters:** the code follows w178's Answer (reading B, the coordinator under the person's delegation), so this is no wrong answer by the decision taken, and I triage it as an observation. But the lines and the code disagree, and the next reader takes the lines' words.
- **Fix:** write reading B into r101's Implementation line, or into r9, r82 and r101 themselves, through integrating-a-proposal. For example: "a request kept in this context whose asker is this context and whose status is `awaiting-asker`".
- **Since review 3:** unaddressed. No work-item or round of the branch carries it.

### 2. Minor (w178): new import out of order

- **Triage:** observation (cheap: `ruff check --fix`).
- **Where:** `tests/scenarios/test_supervision.py:36`.
- **What is wrong:** `from .supervision_request_steps import *` follows `supervision_review_steps`. ruff reports I001 for the block at line 14.
- **Why it matters:** `tools check` is not clean on a file the branch touched.
- **Fix:** move line 36 above line 35.

### 3. Minor (no work-item: i26's supervision gate round): a session's helper script committed under its stage directory

- **Triage:** observation.
- **Where:** `.shop/work/i26/runs/supervision/1-gate/mk.py`.
- **What is wrong:** a gate session's scratch helper is tracked.
  - i29, i30 and i31 now do the same, and ruff counts 25 of its 33 errors in such helpers.
- **Why it matters:** it is tracked Python that ruff checks and that no line asks for, and it hides the code's own lint results.
- **Fix:** keep stage directories to brief, result, session and kept files, or exclude `.shop/` from `tools check`'s ruff run.

## Shape

Each CLAUDE.md rule and module-map row i26 touched:

- **Size limit 300:** met. `tools size` prints nothing.
- **`scripts/workqueue_request.py` row:** met. CLAUDE.md:27 names `ask` and `reply`, and `asked_here` (`workqueue_request.py:40`) reads the context's own requests.
- **`scripts/supervise*.py` row:** met.
  - `asked` is at `supervise.py:248`, called from `Run.run` (`:198`) and `run_all` (`supervise_all.py:83`).
  - The intake questions are written at `supervise_intake.py:89-99`.
- **`scripts/work` row:** met. The `ask` and `reply` parsers and handlers are in `scripts/work`.
- **`tests/scenarios/` row:** met. `supervision_request_steps.py` holds one concern.
- **Decision 0067 (requests written through work):** met. The intake writes questions through `workqueue_request.ask`, which commits through `_change`.
- **Code no line asks for:** none found.
  - `ask` and `reply` serve requests r20 and r21.
  - `asked` and `asked_here` serve r101, r9 and r82.
  - The intake's question writing serves r100.
  - The `3` exit code is mechanism: the error code `work run` already uses.
- **Unreached code or steps:** none left by i26. vulture is clean, and every i26 step is reached by a scenario of r4, r5, r12, r20, r21, r9, r67, r82, r100 or r101 (the w177 and w178 check runs).

## Coupling

i26 adds no dependency on another project.

- It relies on the `git` CLI's merge in `Intake.take` (`supervise_intake.py:89-99`). The questions are committed on the main checkout, then the round branch, which edits `## Outcomes` and the front matter, is merged.
- That merge stays conflict-free while `## Answers` separates `## Questions` from `## Outcomes`.
- A conflict faults the round, aborts the merge and resets to the head from before the questions. That is a refusal, with no data lost.
- To make it stable, write the questions on the round branch before the round's `work turn`, as r100's Implementation line (`supervision.md:166`) reads, rather than relying on hunk separation.

## Observations

- **w177 (`workqueue_request.py:139-145`, `reply`; `_numbered` `:82-84`):** `reply` checks only the turn.
  - So an answer is written to a question that does not exist, and a second answer to the same question replaces the first.
  - Reproduction, read from the code: `work reply q1 7 seven` on a request with one question writes `7. seven`. `work reply q1 1 first` then `work reply q1 1 second` leaves `1. second`.
- **w177 (`:129-136`, `ask`):** a question is accepted on a line the request lacks. `work ask q1 9 x` on a two-line request writes `1. line 9: x`.
- **w177 (multi-line `ask`/`reply` text):** the text is written as given.
  - `work reply q1 1 $'x\n\n## Outcomes\n1. accepted\n2. accepted'` puts a forged `## Outcomes` before the real one. `_entries` (`:27`) takes the first such heading, so `accepted_lines` reads the forged outcomes: the asker writes the upstream's part, against requests r5.
  - An answer `a\nb` followed by any later `reply` raises `ValueError` in `_numbered` (`int("b")`). That is a crash where a refusal belongs.
  - No client sends such text today.
  - Fix: a line refusing multi-line question and answer text, then the refusal.
- **w178 (`supervise_intake.py:92-94`):** a result question that does not start with `<n>. `, or that names a line the request lacks, faults the round. The request stays as it was. That is a refusal (plan section 5, open case 1).
- **Not i26 (i27, supervision r95):** the scenario "`work run` started with no initiative runs the integrate, apply and formulate rounds of different initiatives one at a time" (`features/supervision.feature:885`) failed in one full parallel run and passed in the other and when run alone (`-k one_at_a_time`: 2 passed).
- **Not i26 (i28/w171):** the deprecated `supervision @r102` scenario remains while its replacement's work-item is green (`features deprecated`).
