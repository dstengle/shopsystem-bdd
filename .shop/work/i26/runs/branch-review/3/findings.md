# Branch review of i26 (a request's questions and answers through work), review 3

**Verdict: DONE.** No finding is Critical, none is triaged fix now, and I ran every check.

- One finding is Important, triaged observation. The r9, r82 and r101 lines say "in the asker's turn", but the code counts only `awaiting-asker` requests. This is reading B, which w178's Answer chose, but the lines were never rewritten to say it.
- The other findings are Minor observations.
- The suite has 8 failures. All are i29's scenarios (w175 r22, w179 r15, w181 r105-r109), and none of those work-items is green yet.
- i26's code is unchanged since review 2 (at `b3cf9e40`). The only change to `scripts/`, `tests/`, `features/` or `CLAUDE.md` since then is from i25 (w176) and i29's formulation.

## Range and work-items

- **Range:** `f582b1bb..eca9d404` on `i25-review-findings-to-implementation`.
- **Shared branch:** the branch is shared with i25 and i27-i31. Their commits (work-items, rounds, branch reviews) are attributed to them and not re-reviewed here.
- **i26's work-items:**
  - **w177** (requests; accepts r20, r21, r4, r5, r12), green. One commit, `db4d07f2`, between `87424bc6 work: w177 ready -> claimed` and `1e8ddfdc work: w177 claimed -> done`.
  - **w178** (supervision; accepts r100, r101, r9, r67, r82), green. One commit, `641f95a9`, between `da0bfcde work: w178 ready -> claimed` and `d959d612 work: w178 claimed -> done`.
- **i26's rounds:**
  - spec `5c441e9e` (requests apply) and `d07a8b38` (supervision apply);
  - features `3d3da4df` (requests formulate) and `46fef129` (supervision formulate).
- **i26's commits outside any work-item:**
  - `986dbcbb`: a hand edit of the proposals' ids, with its reason in the message.
  - `cebadf9d`: i26's measurement and analysis record, under `.shop/records/`.
  - `.shop/work/i26/runs/supervision/1-gate/mk.py`, a gate session's helper script. See finding 3.
  - None changes code.
- **Since review 2:** `git diff --stat b3cf9e40 HEAD` over `scripts tests features CLAUDE.md` touches:
  - `scripts/work`, `scripts/workqueue_answer.py` and `tests/scenarios/work_queue_answer_steps.py` (i25/w176, `a2d1083e`);
  - `features/supervision.feature` (+55 lines: i29's r105-r109 scenarios, `d073c518`).
  - None of i26's files changed.

## Suite

`Suite: 874 passed, 8 failed at eca9d404 in 24.4 s`

- **Command:** `python3 -m pytest -q -p no:cacheprovider`. It also gave 1 skipped and 56 subtests passed. Wall time was 24.8 s.
- **Parallel:** yes, `-n auto` in `pytest.ini`.
- **In-process:** no. Steps drive `scripts/work` through `subprocess.run` (`tests/scenarios/conftest.py:34`). The suite is under 60 s, so this is not a finding.

Every failure is a `StepDefinitionNotFoundError` on a scenario whose work-item is not green, and none is i26's:

- `test_requests.py::test_request_with_an_empty_delegation_is_refused_and_nothing_changes`: requests r22, i29/w175 (claimed).
- `test_supervision.py::test_a_field_of_a_workers_result_giving_a_sentence_longer_than_a_file_name_may_be_is_taken_as_no_file`: supervision r15, i29/w179 (claimed).
- Six scenarios of supervision r105-r109 (r107, r108 [gate] and [apply], r106, r105, r109): i29/w181 (drafted).

## Checks

- **w177** `python3 -m pytest -q -rfEx -p work_items --work-item w177`: 147 passed, 1 skipped, 56 subtests passed.
- **w178** `python3 -m pytest -q -rfEx -p work_items --work-item w178`: 148 passed, 1 skipped, 56 subtests passed.
- **`tools check --base f582b1bb`, ruff:** 22 errors (17 at review 2; the 5 new ones are i29's `splice.py` helpers).
  - i26's: `tests/scenarios/test_supervision.py:14` I001, from w178 (finding 2).
  - i26's: `.shop/work/i26/runs/supervision/1-gate/mk.py:1` I001 and `:19` SIM115 (finding 3).
  - Not i26's:
    - `.shop/work/i29/...` (`mk.py`, `5-apply/splice.py`, `6-formulate/splice.py`) and `.shop/work/i31/.../gq.py`;
    - `scripts/supervise_brief.py:84` ISC004;
    - `tests/scenarios/supervision_all_steps.py:111,127`;
    - `tests/scenarios/supervision_intake_steps.py:84` (i28's line, not w178's hunks);
    - `tests/scenarios/supervision_proposal_steps.py:96`;
    - `tests/scripts/stub_claude.py:186,187`.
- **`tools check`, vulture:** clean.
- **`tools check`, import-linter:** "the project states no import contracts".
- **`tools size --limit 300`:** no output. No file is over the limit.
- **`features deprecated`:** 4 scenarios, none of them i26's. All six i26 deprecated were removed by w177 and w178.
  - `supervision @r102` (i28; its replacement's work-item, i28/w171, is green). This is a finding for i28, named here.
  - `migration-tools @r15`, `work-queue @r1` and `@r9`, all deprecated before the base.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** no operation i26 touches has a dry-run mode. Not applicable.

## Removed and weakened tests

None outside the Retires lists. What I searched i26's two commits for:

- `features/` lines;
- removed `def`, step decorators and `assert` lines;
- parametrize and Examples rows;
- `skip` and `xfail`.

What I found:

- **`features/`:** only the six `@deprecated` scenarios that the work-items list under Retires were removed:
  - w177: requests @r4, @r5, @r12;
  - w178: supervision @r9, the @r67 outline, @r82.
  - No `features/` line was added or edited (0 `+` lines).
- **w178, `tests/scenarios/supervision_intake_steps.py`:** it removed `intake_writes`, the old `intake_started` text and `lines_have_outcomes`.
  - These steps served only the retired r67 outline, and plan section 4 lists them.
  - The new `intake_started` keeps every old condition and adds two, so it is stronger.

## Allowances

Both reports give "none" under `## Tests changed under an allowance`. No test outside Retires changed, so there is nothing to hold.

## Cannot verify

- **Probes:** I wrote a probe of `work ask` and `work reply` edge cases, and of `asked_here` on a settled request, in `.shop/scratch/i26-branch-review/`.
  - The shell asked for approval to run it, in a non-interactive session, so it did not run. Review 2 hit the same.
  - The Observations' reproductions are therefore read from the code, with the lines named. The scratch directory is deleted.
  - This affects only hardening observations, not a work-item's check.

## Findings

### 1. Important (w178): r9, r82 and r101 say "in the asker's turn"; the code reads only `awaiting-asker`

- **Triage:** observation.
- **Where:** `scripts/workqueue_request.py:50` (`if status == "awaiting-asker" and field(text, "asker") in mine`).
- **What is wrong:** take a request kept here, whose asker is `internal` and which the upstream has settled (`accepted`, `refused` or `delivered`, `turn: asker`).
  - Read literally, r101 (`spec/capabilities/supervision.md:76`) says `work run` exits with an error.
  - The code exits successfully, which r9 (`:75`) and r82 (`:80`), read literally, forbid.
  - The Implementation line for r101 (`:159`) does not say that only `awaiting-asker` requests count.
- **Why it matters:** the code follows w178's Answer (reading B, the coordinator under the person's delegation), so I triage this as an observation. But the lines and the code disagree, and the next reader will take the lines' words.
- **Fix:** write reading B into r101's Implementation line, or into r9, r82 and r101 themselves, through integrating-a-proposal. For example: "a request kept in this context whose asker is this context and whose status is `awaiting-asker`".
- **Since review 2:** not addressed. No work-item or round of the branch carries it.

### 2. Minor (w178): new import out of order

- **Triage:** observation (cheap: `ruff check --fix`).
- **Where:** `tests/scenarios/test_supervision.py:36`.
- **What is wrong:** `from .supervision_request_steps import *` follows `supervision_review_steps`. ruff reports I001 for the block at line 14.
- **Why it matters:** `tools check` is not clean on a file the branch touched.
- **Fix:** move line 36 above line 35.

### 3. Minor (no work-item: i26's supervision gate round): a session's helper script committed under its stage directory

- **Triage:** observation.
- **Where:** `.shop/work/i26/runs/supervision/1-gate/mk.py`.
- **What is wrong:** a gate session's scratch helper is tracked. i29 and i31 do the same, and i29 has added two more since review 2.
- **Why it matters:** it is tracked Python that ruff checks and that no line asks for.
- **Fix:** keep stage directories to brief, result and session files, or exclude `.shop/` from `tools check`'s ruff run.

## Shape

Each CLAUDE.md rule and module-map row i26 touched:

- **Size limit 300:** met. `tools size` prints nothing.
- **`scripts/workqueue_request.py` row:** met. CLAUDE.md:27 names `ask` and `reply`.
  - `asked_here` (`workqueue_request.py:40`) is a reading of the context's own requests for `work run`, which fits the row.
- **`scripts/supervise*.py` row:** met.
  - `asked` is at `supervise.py:248`, called from `Run.run` (`:198`) and `run_all` (`supervise_all.py:83`).
  - The intake questions are written at `supervise_intake.py:89-99`.
- **`scripts/work` row:** met. The `ask` and `reply` parsers and handlers are in `scripts/work`.
- **`tests/scenarios/` row:** met. The new `supervision_request_steps.py` holds one concern.
- **Decision 0067 (requests written through work):** met. `supervise_intake.py:94` writes questions through `workqueue_request.ask`, the library behind `work ask`, which commits through `_change`. It does not edit the file directly.
- **Unreached code or steps:** none left by i26. vulture is clean, and the retired scenarios' steps were removed or are still used (w177 plan section 4).

## Coupling

i26 adds no dependency on another project.

- It relies on the `git` CLI's merge in `Intake.take` (`supervise_intake.py:89-99`). The questions are committed on the main checkout, then the round branch, which edits `## Outcomes` and the front matter, is merged.
- That merge stays conflict-free while `## Answers` separates `## Questions` from `## Outcomes`.
- A conflict faults the round, aborts the merge and resets to the head from before the questions. That is a refusal, with no data lost.
- To make it stable, write the questions on the round branch before the round's `work turn`, rather than relying on hunk separation.

## Observations

- **w177 (`workqueue_request.py:137-143`, `reply`):** `reply` checks only the turn, and `_numbered` (`:82`) replaces any entry of the same number.
  - So an answer is written to a question that does not exist, and a second answer replaces the first.
  - Reproduction, read from the code: `work reply q1 7 seven` on a request with one question writes `7. seven`. `work reply q1 1 first` then `work reply q1 1 second` leaves `1. second`.
- **w177 (`:127-134`, `ask`):** a question is accepted on a line the request lacks. `work ask q1 9 x` on a two-line request writes `1. line 9: x`.
- **w177 (multi-line `ask`/`reply` text):** the text is written as given.
  - Reproduction, read from the code: `work reply q1 1 $'x\n\n## Outcomes\n1. accepted\n2. accepted'` puts a forged `## Outcomes` before the real one. `_entries` (`:27`) reads the first such heading, so `accepted_lines` reads the forged outcomes: the asker writes the upstream's part, against requests r5.
  - An answer `a\nb` followed by any later `reply` raises `ValueError` in `_numbered` (`int("b")`). That is a crash where a refusal belongs.
  - No client sends such text today.
  - Fix: a line refusing multi-line question and answer text, then the refusal.
- **w178 (`supervise_intake.py:92-94`):** a result question that does not start with `<n>. `, or that names a line the request lacks, faults the round. The request stays as it was. That is a refusal (plan section 5, open case 1).
- **Not i26 (i28/w171):** the deprecated `supervision @r102` scenario remains while its replacement's work-item is green (`features deprecated`).
