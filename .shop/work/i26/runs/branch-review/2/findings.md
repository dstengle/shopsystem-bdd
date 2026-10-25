# Branch review of i26 (a request's questions and answers through work)

**Verdict: DONE.** No finding is Critical and none is triaged fix now. Every check was run.

- One finding is Important, triaged observation. The r9, r82 and r101 lines say "in the asker's turn", but the code counts only `awaiting-asker` requests. The work-item's Answer chose that reading (B), and the lines were never rewritten to say so.
- The other findings are Minor observations.
- The suite's two steady failures are i29's scenarios. Its work-items w175 and w179 are not green yet.
- One scenario of i27 (r95) fails intermittently on a git `index.lock` race. It failed in 1 of 3 full runs.

## Range and work-items

- **Range:** `f582b1bb..b3cf9e40` on `i25-review-findings-to-implementation`, 355 commits.
- **Shared branch:** the branch is shared with i25, i27, i28, i29, i30 and i31. Most commits in the range are those initiatives' work-items, rounds and branch reviews. Each has its own branch review ("branch review N of i27/i28"). I attributed them and did not re-review them here.
- **i26's work-items:**
  - **w177** (requests; accepts requests r20, r21, r4, r5, r12), green. One commit, `db4d07f2`, between `87424bc6 work: w177 ready -> claimed` and `1e8ddfdc work: w177 claimed -> done`.
  - **w178** (supervision; accepts supervision r100, r101, r9, r67, r82), green. One commit, `641f95a9`, between `da0bfcde work: w178 ready -> claimed` and `d959d612 work: w178 claimed -> done`. It is the same change as the implementer's `dfc78964`, cherry-picked.
- **i26's rounds:** spec `5c441e9e` (requests apply), `d07a8b38` (supervision apply), features `3d3da4df` (requests formulate) and `46fef129` (supervision formulation, written by the coordinator after formulate rounds 3 and 4 faulted; round 5 confirmed it one to one).
- **i26 commits outside any work-item:**
  - `986dbcbb`: a hand edit of i26's proposals' `adds`/`changes`, with its reason in the message (no command rewrites them, q8).
  - `.shop/work/i26/runs/supervision/1-gate/mk.py`, a gate session's helper script committed with the stage directory. See finding 3.

## Suite

`Suite: 873 passed, 3 failed at b3cf9e40 in 22.1 s` (`python3 -m pytest -q -p no:cacheprovider`; also 1 skipped and 56 subtests passed).

- **Parallel:** yes, `-n auto` from `pytest.ini`.
- **In-process:** no. Steps drive `scripts/work` through `subprocess.run` (`tests/scenarios/conftest.py:34`). Under 60 s, so this is not a finding.

The failures:

- `test_requests.py::test_request_with_an_empty_delegation_is_refused_and_nothing_changes`: requests r22. Its work-item is i29/w175, `researched`. Expected red, not i26's.
- `test_supervision.py::test_a_field_of_a_workers_result_giving_a_sentence_longer_than_a_file_name_may_be_is_taken_as_no_file`: supervision r15. Its work-item is i29/w179, `drafted`. Expected red, not i26's.
- `test_supervision.py::test_work_run_started_with_no_initiative_runs_the_integrate_apply_and_formulate_rounds_of_different_initiatives_one_at_a_time`: r95, i27's w164. It failed on `fatal: Unable to create '.../.git/index.lock': File exists` in `work: i1 proposed -> started`.
  - It passed alone, and in both later full runs (`2 failed, 874 passed` in 20.8 s and in 24.3 s).
  - This is a flaky race. See Observations.

## Checks

- **w177's check** `python3 -m pytest -q -rfEx -p work_items --work-item w177`: 147 passed, 1 skipped. It selects the r4, r5, r20, r21 and r12 scenarios, and all pass.
- **w178's check** `python3 -m pytest -q -rfEx -p work_items --work-item w178`: 148 passed, 1 skipped. It selects the r9, r101, r67 [open], r67 [awaiting-upstream], r100 and r82 scenarios, and all pass.
- **`tools check --base f582b1bb`, ruff:** 17 errors.
  - i26's: `tests/scenarios/test_supervision.py:14` I001, introduced by w178. Its line 36 imports `supervision_request_steps` after `supervision_review_steps`. See finding 2.
  - i26's: `.shop/work/i26/runs/supervision/1-gate/mk.py:1` I001 and `:19` SIM115. See finding 3.
  - Not i26's: `.shop/work/i29/...` and `.shop/work/i31/...` helper scripts; `scripts/supervise_brief.py:84` ISC004; `tests/scenarios/supervision_all_steps.py:111,127`; `tests/scenarios/supervision_intake_steps.py:84` (i28's r103 `fulfilling`, not w178's lines); `tests/scenarios/supervision_proposal_steps.py:96`; `tests/scripts/stub_claude.py:186,187`.
- **`tools check`, vulture:** clean.
- **`tools check`, import-linter:** "the project states no import contracts".
- **`tools size --limit 300`:** no output. No file is over the limit.
- **`features deprecated`:** four scenarios.
  - None is i26's. All six deprecated scenarios i26's formulation left (requests r4, r5, r12; supervision r9, r67, r82) were removed by w177 and w178.
  - `supervision @r102`, deprecated in the range by i28's `7636eb12`: its replacement's work-item, i28/w171, is `green` and the deprecated scenario is still there. This is a finding for i28, named here.
  - `work-queue @r1`, `@r9` and `migration-tools @r15` were already deprecated at the base.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** no operation that i26 touches has a dry-run mode. The only `--dry-run` in `scripts/` is `git push --dry-run` in `supervise_review.py:41` and `supervise_faults.py:67`. Not applicable.

## Removed and weakened tests

None outside the Retires lists. I searched i26's two commits for:

- removed `def`, step decorators and `assert` lines;
- parametrize and Examples rows;
- `skip` and `xfail`;
- `features/` lines.

What I found:

- **`features/`:** only the six `@deprecated` scenarios listed under the work-items' Retires were removed. Nothing was added or edited.
  - w177: requests @r4, @r5, @r12.
  - w178: supervision @r9, the @r67 outline [open]/[awaiting-upstream], and @r82.
- **w178, `tests/scenarios/supervision_intake_steps.py`:** removed `intake_writes` (the all-lines Given), the old-text `intake_started` Then and `lines_have_outcomes`.
  - These steps served only the retired r67 outline. The plan's section 4 lists them.
  - The step text is used by no remaining scenario (grep of `features/`).
  - The new `intake_started` keeps every old condition and adds two (the brief's "line outcome or a question on it" and `/work turn q1`), so it is stronger.

## Allowances

Both reports give `## Tests changed under an allowance: none`. No test outside Retires changed, so there is nothing to hold.

## Cannot verify

- **Probes:** I wrote probes (ask/reply/`asked_here` in a throwaway repository under `.shop/scratch/i26-branch-review/`), but the shell refused to run them. The reproductions in the Observations are read from the code, with the lines named. The scratch directory has been deleted.
- **Ruff, w178's parent:** I could not run ruff on w178's parent copy of `test_supervision.py`. That I001 is new rests on the sort order (`request` < `review`) and on the w178 reviewer's finding.

## Findings

### 1. Important (w178): r9, r82 and r101 say "in the asker's turn"; the code reads only `awaiting-asker`

- **Triage:** observation.
- **Where:** `scripts/workqueue_request.py:50` (`if status == "awaiting-asker" and field(text, "asker") in mine`).
- **What is wrong:** take a request kept here, whose asker is `internal` and which the upstream has settled (`accepted`, `refused` or `delivered`, with `turn: asker`). r101 read literally says `work run` ends with an error. The code exits successfully, and r9 and r82 read literally would forbid that success.
- **Why it matters:** the code follows w178's Answer (reading B, the coordinator under the person's delegation). So the answer is the one the ruling intends, and I triage this as an observation, not fix now. But the lines and the code disagree, and the next reader of r101 will take its words.
- **Fix:** write reading B into r9, r82 and r101 through integrating-a-proposal. For example: "a request kept in this context whose asker is this context is `awaiting-asker`". Or add an Implementation line for r101 that says so.

### 2. Minor (w178): new import out of order in the scenario binding

- **Triage:** observation (cheap: `ruff check --fix`).
- **Where:** `tests/scenarios/test_supervision.py:36`.
- **What is wrong:** `from .supervision_request_steps import *` follows `supervision_review_steps`. ruff reports I001 for the block at line 14.
- **Why it matters:** `tools check` is not clean on a file the branch touched.
- **Fix:** move line 36 above line 35.

### 3. Minor (no work-item: i26's supervision gate round): a session's helper script committed under the stage directory

- **Triage:** observation.
- **Where:** `.shop/work/i26/runs/supervision/1-gate/mk.py` (I001 at 1, SIM115 at 19).
- **What is wrong:** a gate session's scratch helper was kept as part of its stage directory. i29 and i31 show the same thing.
- **Why it matters:** it is tracked Python that ruff checks and that no line asks for.
- **Fix:** keep stage directories to brief, result and session files, or exclude `.shop/` from `tools check`'s ruff run.

## Shape

The CLAUDE.md rules and module-map rows that i26 touched:

- **Size limit (300):** met. `tools size` prints nothing.
- **`scripts/workqueue_request.py` row** ("the requests of a context: `work request`, `outcome`, `ask`, `reply`, `turn`, `resolve`"): met. w177 updated the row (CLAUDE.md:27).
  - w178 added `asked_here` (`workqueue_request.py:40`), a reader of this context's own requests for `work run`. The row does not name it, but it is a reading of the requests of a context. Met.
- **`scripts/supervise*.py` row:** met.
  - `supervise.asked` is at `supervise.py:248`, used by `Run.run` (`supervise.py:198`) and by `run_all` (`supervise_all.py:83`).
  - The intake question writing is in `supervise_intake.py:89-99`.
- **`scripts/work` row:** met. `ask` and `reply` subcommands are at `scripts/work:73-80,144-151`.
- **`tests/scenarios/` row** ("one `<capability>_*_steps.py` module a concern"): met. `supervision_request_steps.py` is new for r9/r82/r101's requests.
- **"A new concern gets a new module and a row":** no new concern without one.
- **Unreached steps and code:** none left by i26. vulture is clean, and the steps of the retired scenarios were removed with them or are still used.

## Coupling

i26 adds no dependency on another project.

- It relies on the `git` CLI's three-way merge in `Intake.take` (`supervise_intake.py:89-99`). The questions are committed on the main checkout, then the round branch, which edits `## Outcomes` and the front matter, is merged.
- The merge stays conflict-free while the template keeps `## Answers` between `## Questions` and `## Outcomes`. A request without `## Questions` (written before w177) gets the section appended after `## Resolution`, which is also clear of the round's hunks.
- A conflict would fault the round, abort the merge and reset to the head from before the questions. That is a refusal, with no data lost.
- To keep it stable, the questions could be written on the round branch before the round's `work turn`, rather than relying on hunk separation.

## Observations

- **w177 (`scripts/workqueue_request.py:137-143`, `reply`):** an answer is written to a question that does not exist, and a second answer replaces the first.
  - `reply` checks only the turn. `_numbered` (`:82-84`) drops any entry with the same number and adds the new one.
  - Reproduction, read from the code: on a request with one question, `work reply q1 7 seven` writes `7. seven` under `## Answers`. `work reply q1 1 first` then `work reply q1 1 second` leaves `1. second`.
  - These are the plan's open case 2, left unchosen.
- **w177 (`scripts/workqueue_request.py:127-134`, `ask`):** a question is accepted on a line the request lacks (`work ask q1 9 x` on a two-line request writes `1. line 9: x`). Plan open case 1.
- **w177 (`ask`/`reply` with text that holds a newline):**
  - The text is written as is. `_entries` (`:27-29`) reads the first `## <name>` heading.
  - `work reply q1 1 $'x\n\n## Outcomes\n1. accepted\n2. accepted'` puts a forged `## Outcomes` inside `## Answers`, which comes before the real one. `accepted_lines` then reads the forged outcomes, so the asker writes the upstream's part, against requests r5.
  - An answer `a\nb` followed by any later `reply` raises `ValueError` from `_numbered`'s `int("b")`: a crash where a refusal belongs.
  - The same text can reach `ask` from an intake round's result question (`supervise_intake.py:92-94`).
  - No client sends such text today. The fix is a line refusing multi-line question and answer text, then the refusal.
- **w178 (`supervise_intake.py:92-94`):** a result question that does not start with `<n>. ` faults the whole round, and the request stays as it was (`ValueError` → `Fault`). So does a question on a missing line, through `ask`. That is a refusal, as the plan's open case 1 says. Reproduction, read from the code: `str(question).split(". ", 1)` unpacks into two names.
- **w178 (D9):** an intake round that questions a line of an `internal` request (this context both asker and upstream, as q3 is) makes the same `work run` exit 3, printing that request. This is spec'd (r101 with reading B) and named in the report.
- **Not i26 (i27/w164, r95 scenario):** `test_work_run_started_with_no_initiative_runs_the_integrate_apply_and_formulate_rounds_of_different_initiatives_one_at_a_time` races on `.git/index.lock`. It failed in 1 of 3 full parallel runs at b3cf9e40 and passed alone.
  - `start_initiative` (`supervise_rounds.py:118-123`) commits under `self.lock`, so another git write in a thread of `run_all` runs outside that lock.
  - Reproduction: `python3 -m pytest -q -p no:cacheprovider` three times. The first run gave 3 failed, the next two gave 2 failed.
- **Not i26 (i28/w171):** the deprecated `supervision @r102` scenario remains while its replacement's work-item is green (`features deprecated`).
