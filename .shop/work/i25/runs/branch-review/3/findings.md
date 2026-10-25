# Branch review 3 of i25 (Review findings back to implementation)

**Verdict: DONE_WITH_CONCERNS.** One finding is Critical on the letter of the rule. w176 removed a deprecated scenario under `features/`, but w176.md has no `## Retires` that lists it. The removal is sanctioned in w176.md's `## Answers` and listed in its plan. The fix is a one-line record edit. Nothing is triaged fix now.

Every check a work-item names was run here and passed. The suite is red at HEAD by 19 scenarios. All 19 belong to i29/i30/i31 work-items that are not done, and none is i25's.

## Range and work-items

- Range: `f582b1bb..225d3ed2` on `i25-review-findings-to-implementation`.
  - The branch is shared with i26-i31. Most of its commits are those initiatives' work-items, rounds and records.
  - Branch review 2 covered the range up to `76a9ed4b`. Since then, no commit touches a file of i25's work-items. `git log f582b1bb..HEAD` on `scripts/supervise_brief.py`, `scripts/workqueue_answer.py`, `scripts/work`, `tests/scenarios/work_queue_answer_steps.py` and `tests/scenarios/supervision_answers_steps.py` shows i25's commits as the last ones.
  - Commits since `76a9ed4b` that touch code or features:
    - `0c654848` (i29 w179)
    - `959cba20` (i29 w175)
    - `2f3698be` (i30 formulate)
    - `a30cfe25` (i31 formulate)
- i25's work-items:
  - **w173** (supervision#r98), green. One commit, `b6c4feb1`, between `906706f0` (ready -> claimed) and `9e50678a` (claimed -> done).
  - **w174** (work-queue r14, r26, r27), withdrawn. Its branch `work/w174` is still there and is not merged. Nothing of it is on the branch.
  - **w176** (work-queue r14, r26-r28), green. One commit, `a2d1083e`, between `9c79765c` (ready -> claimed) and `e0ce90ce` (claimed -> done).
- i25's round commits:
  - `112fe1b6` (spec supervision r98)
  - `1c0c4fb6` (spec work-queue r26-r28, r14 changed)
  - `159bdfdf` (work-queue scenarios; old r14 outline deprecated)
  - `46fef129` (r98's scenario)
- Commits belonging to no work-item: none among the code commits. Each code commit on the range lies inside a claim window of some initiative's work-item, as review 2 found. The four new code and features commits are i29's work-items and i30/i31's rounds.
  - The branch does track round helper scripts under `.shop/work/i26|i29|i30|i31/runs/**` (`mk.py`, `splice.py`, `gq.py`, `apply.py`). Those commits are other initiatives' rounds, not i25's (see Observations).

## Suite

`Suite: 876 passed, 19 failed at 225d3ed2 in 40.33 s`

- That is pytest's own timing. This shell would not let me chain a wall clock around the command.
- The command was `python3 -m pytest -q -n auto -p no:cacheprovider -rf`. It runs in parallel (xdist, `-n auto`).
- The step definitions drive the entry points as subprocesses (`tests/scenarios/conftest.py`, `subprocess.run`), not in-process. It is under 60 s, so this is not a finding.
- The 19 failures are all in `test_supervision.py`. Each one's tag belongs to a work-item that is not done:

| Work-item | Status | Tags |
|---|---|---|
| i29 w181 | claimed | @r105, @r106, @r107, @r108 ×2, @r109 |
| i30 w184 | drafted | @r110, @r117, @r19 (80 turns) |
| i31 w185 | drafted | @r83, @r111, @r112, @r113, @r114, @r115 ×4, @r116 |

  None is r98, r14 or r26-r28.

## Checks

- **w173's check:** `python3 -m pytest -q -n auto -p work_items --work-item w173` gave 143 passed, 1 skipped.
- **w176's check:** the same with `--work-item w176` gave 148 passed, 1 skipped.
- **i25's scenarios by tag:** `-m "r98 or r14 or r26 or r27 or r28"` on `test_supervision.py` and `test_work_queue.py` gave 22 passed.
- **`tools check --base f582b1bb`:**
  - **ruff:** 33 errors, none on a line i25's commits wrote.
    - 25 are in tracked round helpers under `.shop/work/i26|i29|i30|i31/runs/**`.
    - `scripts/supervise_brief.py:84 ISC004` is on a context line of w173's hunk (lines 83-86 are unchanged in `b6c4feb1`). Review 2's blame put it on `a4e922a6`/`a1ff989a`.
    - `tests/scenarios/supervision_all_steps.py:111,127`, `supervision_intake_steps.py:84`, `supervision_proposal_steps.py:96`, `test_supervision.py:14` and `tests/scripts/stub_claude.py:186-187` are in files no i25 commit touches.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". Nothing to read for it. The module map is under Shape.
- **`tools size --limit 300`:** printed nothing.
- **`features deprecated`:** six deprecated scenarios.
  - migration-tools @r15, work-queue @r1 and work-queue @r9 were there at Base.
  - supervision @r19 and @r83 have replacements whose work-items are not green (i30's w184 and i31's w185, both drafted).
  - supervision @r102's replacement is i28's w171, which is green. That is i28's finding, not i25's.
  - i25's own deprecated r14 outline is gone, retired by w176.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run and real modes:** none of i25's operations has one. The only `--dry-run` uses in `scripts/` are `git push --dry-run` push checks (`supervise_faults.py:67`, `supervise_review.py:41`). No agreement test applies.

## Removed and weakened tests

I searched i25's two commits for:
- removed `def` lines
- removed or loosened `assert`s
- dropped Examples or parametrize rows
- added `skip`/`xfail`
- renames

Under `tests/`, both commits only add lines. One test was removed, through its feature outline:

- **`test_work_queue.py::test_answer_on_an_awaitinganswer_workitem_transitions_it_to_the_status_the_asking_stage_started_from_deprecated`** (4 rows), removed by w176 (`a2d1083e`) with the deprecated @r14 outline.
  - What it proved: an answer returns the item to the asking stage's start, for the researcher, planner, implementer and reviewer.
  - The first three rows are still proved by the live @r14 outline.
  - The reviewer row's expectation is what r28 now refuses.
  - w176's plan lists it under "Tests the decisions break" (§4, D3).

## Allowances

Both reports, `w173/5-implement/report.md:15` and `w176/4-implement/report.md:14`, give "none". The diffs agree: no existing test was edited.

## Cannot verify

- The implementers' red runs are history and cannot be rerun at HEAD. `log.jsonl`'s suite records name the failing tests at the claim, and green was verified here. Every check a work-item names was run.

## Findings

### 1. Critical, w176: observation. A scenario removed under `features/` that w176.md does not list under Retires (`features/work-queue.feature`, the former lines 285-298, removed in `a2d1083e`)

- **What is wrong:**
  - w176 removed the deprecated @r14 outline "answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)" and its binding.
  - `.shop/work/i25/w176.md` has no `## Retires` section.
  - w174, which w176 redrafts, did list it. `work add` does not carry a Retires entry over.
- **Mitigation:**
  - The retirement is sanctioned in w176.md's `## Answers` (2026-10-25, the coordinator under the person's delegation).
  - It is planned (plan §4, D3).
  - w176's first reviewer raised it as Critical, and the second reviewer accepted the answer.
  - The scenario was properly deprecated (`159bdfdf`), and its replacement is green.
- **Why it matters:** the rule recognises only a Retires listing, and the record still does not hold one. i30 and i31 met the same gap for w184 and w185 by writing the Retires entries by hand (`0eb572a2`). w176 alone was left with the sanction in an answer.
- **Triage:** not fix now. Nothing answers wrongly, nothing crashes and no data is lost. It is graded Critical only because the rule grades every such `features/` change Critical; the person decides whether the Answers sanction stands in for the listing.
- **Fix:** add to w176.md a `## Retires` entry with the same text as w174's: `"answer on an awaiting-answer work-item transitions it to the status the asking stage started from (deprecated)" (work-queue @r14)`. As `0eb572a2` did, this is a `work:` commit. The lasting fix is a `--retires` for `work add`, or `work add` carrying the Retires entry of a redrafted work-item. Both need a line.

### 2. Important, w176 (and i25's apply round `1c0c4fb6`): observation. r26's reviewer → `ready` transition has no design-decision, and it departs from decision 0063 (`scripts/workqueue_answer.py:50-53`)

- **What is wrong:** `spec/decisions/0063-a-ruling-returns-to-the-asking-stage.md:21` gives a reviewer's question one exit, `→ done`. 0064 only renames it. `ls spec/decisions` still ends at 0068: the "decision (0069)" that the ledger's integrate round 1 names never landed.
- **Why it matters:** the decisions, the lines and the code disagree on the lifecycle.
- **Not fix now:** the code does what r26/r27 ask.
- **Fix:** a decision, through integrating-a-proposal, that replaces 0063's reviewer row with `--change → ready` and `--accept → done`.

This is carried from review 2 and is unchanged.

### 3. Important, outside i25's commits: observation. Under a delegation, an answer to a reviewer's question still lands `done` (`scripts/supervise_answers.py:77-79`)

- **What is wrong:** `answers()` moves a fully answered work-item to `workqueue_answer.asked_from(...)`, which gives `done` for a reviewer's question. So r26's `ready` is never reached on that route, and r98's findings line is never written there.
- **Why it matters:** i25's purpose holds only through `work answer --change`.
- **Not fix now:** no line names the delegated reviewer case.
- **Fix:** a supervision line, through integrating-a-proposal.

This is carried from review 2 and is unchanged. Both implementers named it as an open question.

### 4. Minor, w173: observation. `findings_lines` parses `log.jsonl` with bare `json.loads` (`scripts/supervise_brief.py:93-94`)

- Plan decision 2 said to read the log through `workqueue.logged`.
- A bad log line is refused earlier, by `work answer` (review 2's probe: rc 1, "line 4 of .shop/work/i1/log.jsonl is not a JSON object; no move is made").
- **Fix:** `workqueue.logged(self.dir / "log.jsonl", self.root)`.

### 5. Minor, w173: observation. The findings line can name a `findings.md` that does not exist (`scripts/supervise_brief.py:99-103`)

This is plan open case 1. Today no reviewer leaves its stage without `findings.md`.

### 6. Minor, w176: drop. Missing space at `scripts/work:127`

The line reads `o =sub.add_parser("note", ...)`. This is cosmetic.

### 7. Minor, w176: observation. `part_of: capability-proposal/work-queue` in w176.md is a short id

w173 and w174 use the full `capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/<name>`. Reproduction: `grep part_of .shop/work/i25/w17*.md`. Nothing reads it wrongly today: the suite and `work status` are unaffected. It is one more mark of the hand-redrafting gap in finding 1.

## Behaviour against the lines

- r14 and r26-r28 are met by `workqueue_answer.py:24-53` and `scripts/work:125-126`.
  - No flag on a reviewer's question is refused (r28).
  - `--change` gives `ready` (r26), and `--accept` gives `done` (r27).
  - Both flags together are refused. That traces to r7.
  - The flags are ignored on other askers, per the work-queue proposal's answer 2 (a).
- r98 is met by `supervise_brief.py:58-59,88-103`: it names the last review's `findings.md`, and the answer follows as r57 does.
- These are verified at HEAD by the 22 tagged scenarios, which run the real `scripts/work` as a subprocess. Review 2's end-to-end probe, `work answer --change` then `findings_lines`, is still valid, because neither file has changed since.
- **Code no line asks for:** none.

## Shape

- **Size limit (300):** met. `tools size` printed nothing.
- **Module map:** met. No new concern, so no new row is needed.
  - `scripts/work` with `workqueue_answer.py` ("`work answer`"): `workqueue_answer.py:24-53`.
  - `scripts/supervise*.py` (briefs): `supervise_brief.py:88-103`.
  - Step definitions are in `tests/scenarios/work_queue_answer_steps.py:19-45` and `supervision_answers_steps.py:37-68`.
- **Unreached code or steps:** none. vulture is clean. The retired outline's Given is still used by the live @r14 outline and by r26-r28.
- **Refactor (observation):** `findings_lines` and `asked_by_reviewer` read "the last move into a status" from the log two ways. Move both to `workqueue.logged`. Check that it is complete: `grep -n "json.loads" scripts/supervise_brief.py` prints nothing.

## Coupling

i25 adds no dependency on another project. It uses only the standard library and the repository's own `workqueue` helpers. The suite's pytest-bdd deprecation warnings come from pytest-bdd's own `compat.py`, not from i25's code.

## Observations

Each with its reproduction:

- **Finding 1:** w176.md has no `## Retires`. Reproduction: `grep -c "## Retires" .shop/work/i25/w176.md` gives 0; `git show a2d1083e -- features/work-queue.feature` shows the 15 lines removed.
- **Finding 2:** 0063 has no reviewer `→ ready` row. Reproduction: `grep -n done spec/decisions/0063-*.md` gives only line 21, `awaiting-ruling → done`, for a reviewer.
- **Finding 3:** a delegated reviewer answer lands `done`. Reproduction: read `supervise_answers.py:77-79` with `workqueue_answer.py:15-21`.
- **Finding 4:** bare `json.loads`. Reproduction: write a non-JSON log line after the answer, then write the implement brief; it raises `JSONDecodeError`. `work answer` refuses such a log first.
- **Finding 5:** a findings line for a missing file. Reproduction: a `3-review` directory without `findings.md` still gives the line (w173 review probe).
- **Finding 7:** a short `part_of`. Reproduction: `grep part_of .shop/work/i25/w17*.md`.
- **The stale `work/w174` branch:** it is unmerged after the withdrawal. Reproduction: `git branch -a --list "*w17[346]*"` gives `work/w174`.
- **Tracked round helpers that ruff flags:** these are other initiatives' rounds (i26/i29/i30/i31), not i25's. Reproduction: `git ls-files .shop/work/i31/runs | grep .py`, and `tools check` lists 25 ruff errors in them.
- **The red suite:** red at HEAD by 19 scenarios of w181, w184 and w185, none of them done. Reproduction: `python3 -m pytest -q -n auto -rf`.

## Commands run

- `git log --oneline f582b1bb..HEAD`
- `git log 76a9ed4b..HEAD -- scripts tests features hooks`
- `git log f582b1bb..HEAD -- <i25's files>`
- `git show b6c4feb1 a2d1083e`
- `git branch -a --list "*w17[346]*"`
- The suite, once
- `--work-item w173` and `--work-item w176`
- The tag run
- `tools check --base f582b1bb…`
- `tools size --limit 300`
- `features deprecated` and `features bindings`

No probe was written, and the scratch directory `.shop/scratch/i25-branch-review/` was never created. `git status --short` is clean.
