# Branch review of i25 (Review findings back to implementation)

**Verdict: DONE.** No finding is Critical and none is triaged fix now. Every check a work-item names was run here and passed. There are two Important findings, both triaged observation, for the person to read:

- r26's transition, a reviewer's question going back to `ready`, has no design-decision behind it, and it departs from decision 0063.
- Under a delegation, an answer to a reviewer's question still lands `done`.

## Range and work-items

- Range: `f582b1bb..76a9ed4b` on `i25-review-findings-to-implementation`. The branch is shared with i26 to i31, so most of its commits belong to those initiatives' work-items and rounds.
- i25's work-items:
  - **w173** (supervision#r98), green. One commit: `b6c4feb1` (`scripts/supervise_brief.py` +19, `tests/scenarios/supervision_answers_steps.py` +36). It lies between `906706f0` (ready -> claimed) and `9e50678a` (claimed -> done).
  - **w174** (work-queue r14, r26, r27), withdrawn. Its branch `work/w174` (`e0ee6404`) is **not** merged into HEAD (`git merge-base --is-ancestor work/w174 HEAD` is false). Nothing of it is on the branch.
  - **w176** (work-queue r14, r26-r28), green. One commit: `a2d1083e` (`features/work-queue.feature` -15, `scripts/work` +4/-2, `scripts/workqueue_answer.py` +15/-2, `tests/scenarios/work_queue_answer_steps.py` +29). It lies between `9c79765c` (ready -> claimed) and `e0ce90ce` (claimed -> done).
- i25's spec and formulate commits, which are rounds and not work-items:
  - `112fe1b6` (supervision r98)
  - `1c0c4fb6` (work-queue r26-r28, r14 changed)
  - `159bdfdf` (work-queue scenarios; old r14 outline deprecated)
  - `46fef129` (r98's scenario, shared with i26)
- Commits belonging to no work-item: I checked every commit on the range that touches `scripts/` or `tests/`. Each lies inside a claim window of some work-item: i27 w164-w166, i28 w167-w172, i26 w177/w178, i25 w173/w176. The rest are `work`, round, branch-review and `records:` commits. No code commit is orphaned.

## Suite

`Suite: 874 passed, 8 failed at 76a9ed4b in 24 s`

- That is pytest's own timing (24.03 s, and 22.45 s on a second run). This shell would not run `/usr/bin/time`.
- It runs in parallel (`-n auto`, xdist).
- The step definitions drive the entry points as subprocesses (`tests/scenarios/conftest.py:34`, `subprocess.run`), not in-process. At under 60 s this is not a finding.
- **None of the 8 failures is i25's.** All are scenarios of i29 work-items that are not done yet:
  - `requests @r22` (w175, claimed)
  - `supervision @r15` (w179, claimed)
  - `supervision @r105`, `@r106`, `@r107`, `@r108` ×2 and `@r109` (w181, drafted)

## Checks

- **w173's check**, `python3 -m pytest -q -n auto -p work_items --work-item w173`: 143 passed, 1 skipped.
- **w176's check**, the same with `--work-item w176`: 148 passed, 1 skipped.
- **i25's scenarios by tag**, `-m "r98 or r14 or r26 or r27 or r28"` on test_supervision.py and test_work_queue.py: 22 passed. These include:
  - r98 "an implementer started for a work-item that an answer to its reviewer's question returned to ready is given the reviewer's findings and the answer"
  - the r14 outline (3 rows)
  - r26, r27 and r28
- **`tools check --base f582b1bb`:**
  - ruff: 22 errors, **none on a line i25's commits wrote**.
    - 14 are in untracked or scratch round helpers under `.shop/work/i26|i29|i31/runs/**` (`mk.py`, `splice.py`, `gq.py`).
    - `scripts/supervise_brief.py:84 ISC004`: the lines are from `a4e922a6`/`a1ff989a` (i27 w164, i28 w172), per `git blame -L80,86`.
    - `tests/scenarios/supervision_all_steps.py:111,127`, `supervision_intake_steps.py:84`, `supervision_proposal_steps.py:96`, `test_supervision.py:14` and `tests/scripts/stub_claude.py:186-187` are in files no i25 commit touches.
  - vulture: clean.
  - import-linter: "the project states no import contracts". Nothing to read for it. The module-map check is under Shape.
- **`tools size --limit 300`:** printed nothing. Nearest to the limit: `scripts/workqueue.py` 290 (untouched by i25) and `tests/scenarios/test_work_queue.py` 288 (untouched by i25).
- **`features deprecated`:** four deprecated scenarios.
  - migration-tools @r15, work-queue @r1 and work-queue @r9 are on Base already.
  - supervision @r102's replacement is the work of i28's w171, which is green. That is i28's finding, not i25's.
  - i25's own deprecated r14 outline is gone, retired by w176.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run and real modes:** none of i25's operations has a dry-run mode. The only `--dry-run` in `scripts/` is `git push --dry-run` as a push check (`supervise_faults.py:67`, `supervise_review.py:41`). No agreement test applies.

## Removed and weakened tests

I searched i25's two commits for: `-def`, removed `assert`, dropped parametrize or Examples rows, added `skip`/`xfail`, and renamed tests. Under `tests/`, both commits only add lines. One test was removed:

- **`test_work_queue.py::test_answer_on_an_awaitinganswer_workitem_transitions_it_to_the_status_the_asking_stage_started_from_deprecated`** (4 rows) was removed by w176 (`a2d1083e`) with its deprecated @r14 outline.
  - It proved that an answer returns the item to the asking stage's start: researcher → drafted, planner → researched, implementer → ready, reviewer → done.
  - The first three rows are still proved by the live @r14 outline.
  - The reviewer row's expectation is what r28 now refuses.
  - w176's plan lists it under "Tests the decisions break" (part 4, D3).
  - w176.md has no `## Retires`, but its `## Answers` sanctions the retirement (2026-10-25, the coordinator under the person's delegation). So it is not a Critical finding under `features/`.

## Allowances

Both reports give "none" under `## Tests changed under an allowance`. The diffs agree: no existing test was edited.

## Cannot verify

- The implementers' red runs (w173: the Then failing; w176: 3 StepDefinitionNotFoundError). They are history and cannot be rerun at HEAD. The log's suite records agree: `log.jsonl` lines 74 and 97 name those tests as failing at the claim. Green was verified here.
- Nothing else. Every check a work-item names was run.

## Findings

### 1. Important, observation. r26's transition, a reviewer's question going back to `ready`, has no design-decision and departs from decision 0063 (i25's work-queue apply round, `1c0c4fb6`; code in w176, `scripts/workqueue_answer.py:50-53`)

- **What is wrong:** decision 0063 is in the `rests_on` of both work-queue and supervision. Its table gives a reviewer's question one exit: `awaiting-answer → done`. It has no row `awaiting-answer → ready` for a reviewer's question.
  - work-queue r26, and the code at `workqueue_answer.py:53` (`status = "ready" if change else "done"`), add that transition.
  - Decision 0064 only renames 0063.
  - No decision 0069 or later exists (`ls spec/decisions` ends at 0068). Integrate round 1's "1 decision (0069)" in the ledger never landed.
- **Why it matters:** the lifecycle the decisions record no longer matches the lines and the code. The next reader of 0039/0063 will take `done` as the only exit from a reviewer's question.
- **Not fix now:** the code does what r26 asks, and no answer is wrong.
- **Fix:** record a decision, through integrating-a-proposal, that replaces 0063's reviewer row with the two rows `--change → ready` and `--accept → done`.

### 2. Important, observation. Under a delegation, an answer to a reviewer's question still lands `done`, so the finding does not reach implementation (`scripts/supervise_answers.py:79`, outside i25's commits; it is the open case of w176's plan, D2 and part 5)

- **What is wrong:** `answers()` moves a fully answered work-item to `workqueue_answer.asked_from(...)`, which gives `done` for a reviewer's question. It does this whatever the answer says. It never reaches r26's `ready`, so r98's findings line is never written on that route. r28's refusal does not reach it either.
- **Why it matters:** i25's purpose is that a reviewer's finding reaches implementation. That holds through `work answer --change`. It does not hold when the question is answered by a delegated session (supervision r77/r78): the item goes back to `done` and is reviewed again.
- **Not fix now:** no line names the delegated reviewer case. r26-r28 name `work answer` only, and r77/r78 say nothing about the transition.
- **Reproduction:** read from the code. `supervise_answers.py:77-79` calls `asked_from`, and `workqueue_answer.py:15-21` returns the `before` of the last move into `awaiting-answer`, which is `done` for a reviewer.
- **Fix:** a supervision line, through integrating-a-proposal. For example, a delegated answer to a reviewer's question says whether it asks for a change, and `work run` moves the item as r26/r27 do.

### 3. Minor, observation. `findings_lines` parses `log.jsonl` with bare `json.loads` (w173, `scripts/supervise_brief.py:93-94`)

- **What is wrong:** this was w173 review finding 1, and it is still there at HEAD. Plan decision 2 said to read the log through the existing helpers (`workqueue.logged`).
- **Reproduction (probe, deleted):** a log with a `not json` line. `work answer w1 "Remove it" --change` already refuses with `work: line 4 of .shop/work/i1/log.jsonl is not a JSON object; no move is made`, rc 1. So the route to `findings_lines` refuses earlier, and the crash needs a log made bad after the answer.
- **Fix:** read the moves with `workqueue.logged(self.dir / "log.jsonl", self.root)`.

### 4. Minor, observation. The findings line can name a `findings.md` that does not exist (w173, `scripts/supervise_brief.py:99-103`)

This was w173 review finding 2, open case 1 of the plan. No reviewer leaves its stage without `findings.md` today.

### 5. Minor, drop. Missing space (w176, `scripts/work:127`)

`o =sub.add_parser("note", ...)`. The space was lost while the flags were being added. Cosmetic.

### 6. Minor, observation. The withdrawn w174's branch `work/w174` (`e0ee6404`) is still there

It is unmerged, and its content is superseded by w176. It is harmless, but it is a stale ref for the next reader. No line says what happens to the kept branch of a withdrawn work-item.

## Behaviour against the lines (verified)

I verified this with a probe (now deleted) that ran the real `scripts/work answer` in a scratch git repo. After each answer it added the `ready -> claimed` move `work run` writes, then called `Briefs.findings_lines`:

| case | `work answer` | status | findings line |
|---|---|---|---|
| reviewer, `--change` | rc 0, `w1 ready` | ready | `Reviewer's findings: .shop/work/i1/runs/w1/5-review/findings.md` |
| reviewer, `--accept` | rc 0, `w1 done` | done | none |
| reviewer, no flag | rc 1, "the answer must say whether it asks for a change (--change) or accepts the work-item as it is (--accept)" | awaiting-answer (unchanged) | n/a |
| reviewer, both flags | rc 1, "--change and --accept cannot be given together; …" | awaiting-answer (unchanged) | n/a |
| implementer, `--change` | rc 0, `w1 ready` (flag ignored; r14, as answer 2 (a) chose) | ready | none |

- So w173 and w176 together deliver r98 end to end on the `work answer --change` route. This is the gap w173's review could not check while r26 was missing. The log shape the probe used is the real one: `.shop/work/i25/log.jsonl:106-107` has `done -> awaiting-answer` by work run, then `awaiting-answer -> done` by work answer.
- **Code no line asks for:** none.
  - `--change`/`--accept` trace to r26/r27 and the Implementation line naming the flags.
  - The no-flag refusal traces to r28, and the both-flags refusal to r7.
  - `findings_lines` traces to r98 and its Implementation line.
  - Ignoring the flags on other askers is answer 2 (a) of the work-queue proposal, with no new line.

## Shape

- **Size limit (300):** met by every touched file. `scripts/work` 171, `scripts/workqueue_answer.py` 72, `scripts/supervise_brief.py` 162, `tests/scenarios/work_queue_answer_steps.py` 70, `tests/scenarios/supervision_answers_steps.py` 88.
- **Module map:** met.
  - `scripts/work` with `workqueue_answer.py` ("`work answer`"): `asked_by_reviewer` and the verdict are at `workqueue_answer.py:24-53`, and the flags at `scripts/work:125-126`.
  - `scripts/supervise*.py` ("briefs"): `supervise_brief.py:58-59,88-103`.
  - `tests/scenarios/` with one `<capability>_*_steps.py` module per concern: `work_queue_answer_steps.py:19-45` and `supervision_answers_steps.py:37-68`.
  - No new concern, so no new row is needed.
  - `workqueue.py` (290 lines) was left alone, as w173's plan asked.
- **Unreached code and steps:** none found. The retired outline's Given ("…its question asked by <asker>") is still used by the live @r14 outline and by r26-r28. Its `started` map entry `"a reviewer": "done"` (`test_work_queue.py:79`) is still the before-status of r26-r28's Given.
- **Refactor (observation):** `findings_lines` and `asked_by_reviewer` each read "the last move into a status" from the log their own way, one with bare `json.loads` and one through `workqueue.logged`. Moving both to `workqueue.logged` is the fix. The check that shows it complete: `grep -n "json.loads" scripts/supervise_brief.py` prints nothing.

## Coupling

i25 adds no dependency on another project. The new code uses only the standard library and the repository's own `workqueue` helpers. The suite's existing reliance on pytest-bdd internals does not come from i25's code: the `_register_fixture`/`FixtureDef` deprecation warnings are raised inside pytest-bdd's own `compat.py`. Nothing i25 added relies on more than a project publishes.

## Observations

- `supervise_answers.py:79`: a delegated answer to a reviewer's question lands `done`. Reproduction: read `supervise_answers.py:77-79` with `workqueue_answer.py:15-21` (Finding 2).
- Decision 0063 has no reviewer `→ ready` row. Reproduction: `ls spec/decisions` ends at 0068; 0063's table, lines 16-21 (Finding 1).
- `supervise_brief.py:93-94`, bare `json.loads`. Reproduction: write a `not json` log line after the answer, then write the implement brief; `JSONDecodeError` (w173 review probe). `work answer` itself refuses such a log first (probe above) (Finding 3).
- `supervise_brief.py:99-103` names a missing `findings.md`. Reproduction: a `3-review` directory without `findings.md` gives the line anyway (w173 review probe `test_no_findings_file`) (Finding 4).
- `work/w174` is left unmerged after w174's withdrawal. Reproduction: `git branch --list "*w174*"` gives `work/w174`, and `git merge-base --is-ancestor work/w174 HEAD` gives false (Finding 6).
- The suite is red at HEAD by 8 scenarios, all from i29 (w175, w179, w181), none of them done. Reproduction: `python3 -m pytest -q -n auto -rf`.

## Commands run

- `git log --oneline f582b1bb..HEAD`, `git log -- scripts tests hooks agents skills`, `git show b6c4feb1 a2d1083e`
- `git diff f582b1bb HEAD -- features`, `git log -- features`
- `git branch -a --list "*w17[346]*"`, `git merge-base --is-ancestor work/w174 HEAD`, `git blame -L80,86 scripts/supervise_brief.py`
- `python3 -m pytest -q -n auto -p no:cacheprovider -rf`, run twice: 874 passed, 8 failed
- `--work-item w173` and `--work-item w176` with `-p work_items`; the tag run `-m "r98 or r14 or r26 or r27 or r28"`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base f582b1bb…`, `tools size --limit 300`, `features deprecated`, `features bindings`
- The probe `.shop/scratch/i25-branch-review/test_probe_r26_r98.py`, run with pytest: 6 cases. The scratch directory is deleted, and `git status --short` is clean.
