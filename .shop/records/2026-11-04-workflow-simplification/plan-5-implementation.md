# Plan 5 of the workflow simplification: implementation report

This is the report of the one implementer agent that executed `plan-5-pr-review.md` on 2026-11-05. It used
superpowers:executing-plans, with one commit per task and no subagents.

All 7 tasks are done. The `pr-review` capability is built: all 8 of its requirements are out of `unbuilt:`, each with
its `test_r<n>_…` test, and the trace test (D19) holds both ways. A batch's pull request now gets one review: `work
batch brief` writes what `pr-reviewer` reads, `work batch reviewed` records the findings under `.shop/batches/<n>/`,
posts them, and sets the batch `building` (a fix-now finding is open) or `awaiting-merge` (clean, the pull request
marked ready). Fixes are commits citing `Finding: f<m>`, checked by `work batch review`, and the re-review reads only
the commits after the last review. That closes plan 4's two open ends: `in-review` → `building` and `awaiting-merge`
are now written. The commits are on `workflow-simplification`, from `bb474074` to this report's commit. They are not
pushed, and no test or smoke run touched the real remote (a bare repository and the stand-in gh only). No baseline got
worse.

## Final state

| Check | Result |
|---|---|
| Suite (`python3 -m pytest -q`) | **1335 passed**, 1 skipped, **14 xfailed**, **135 subtests** passed (25 s). The start was 1277 passed, 132 subtests. The 58 new passes: findings 15, brief 10, reviewed 12, trace 2, fix loop 10, the agent 5, the skill 4. The 3 new subtests are `test_agents.py`'s rows for `pr-reviewer` (r2, r5, and the check over every agent file); the plan expected 2. Two runs of about fifteen each showed one failure in tests this plan did not touch (see Open problems). |
| Timing run (`python3 -m pytest -m timing -n 0 -q`) | `1 passed, 1350 deselected` (1.7 s) |
| Unbuilt ids | `False ['r3'] 15 []`: pr-review is absent, brainstorming r3 stays, 15 remain (23 − 8), no problems |
| `model check` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems (at baseline) |
| `model logic` | `11 findings: 6 L5, 5 L6` (at baseline) |
| `model lexicon --check` | 401 terms, 0 problems |
| `features generate --check` | exit 0 |
| `features vocab --check` | `every step has one handler` |
| `features bindings --unbound` | `every binding names a scenario` |
| `tools size --limit 300` | silent. `batch_tasks.py` 233 (231 + 2), `batch_review.py` 148 (150 − 5 + 3), `batch_cli.py` 154. New: `batch_findings.py` 238, `batch_brief.py` 187, `batch_reviewed.py` 115, `batch_fix.py` 91. `scripts/work` and `test_batch_review.py` unchanged. |
| `tools check $(git diff --name-only fbbd1466...HEAD -- '*.py')` | ruff and vulture clean; import-linter states no contracts |
| Smoke run (Task 7, Step 3, in bash) | Brief 1: **179 ms**. Reviewed 1: **192 ms**, printing `batch-1 review 1: 1 findings, 1 fix now -> building` and `open f1 Important b1 "…" spec/capabilities/work-queue.md:9: …`. `status` showed `reviews: 1, last fix-now; open f1 b1 "…"`. `resume` printed the D14 f1 line with t1's worktree. Brief 2: **195 ms**, `Review: 2 (re-review of the fix)`, `## Earlier findings` with f1 and its fix commit, `## Commits` holding only the fix and its merge. Reviewed 2: **216 ms**, `-> awaiting-merge; the pull request … is ready for the person's merge`. `merged` delivered b1. `.shop/batches/1/` on `main` holds `plan.md`, `review-1.md` and `review-2.md`. `$d.calls`: one `pr create`, two `pr comment`, one `pr ready`, one `pr view`. `status --porcelain` empty. The plan's fix commit `-m "fix" -m "Item: b1" -m "Finding: f1"` was refused by `review` (Deviation 4); amended to one trailer paragraph, it went through. |

## Commits

| Task | Commit | What was done | Verification |
|---|---|---|---|
| 1 | `bb474074` | `batch_findings.py`: `GRADES`, `TRIAGES`, `Finding`, `Review`, `parse_findings` (D9; refusals name the file and the line), `render`/`parse` of the record (D13), `reviews`, `open_findings` (D10, D22), `next_fid`, `scratch`, `rel_of`. `batch_plan.commit(..., files=None)`. `review_testing.py` (`published`, `findings`, `FIX_NOW_B1`, `CLEAN`, `FIXED_F1`). Module-map row; `review_testing.py` in the `tests/scripts/` row. | The tests failed first (no `batch_findings`), then 15 passed; with `test_batch_plan.py`, 25. Suite: 1292 passed, 14 xfailed. |
| 2 | `57233bdf` | `batch_brief.py` (`brief`, `judgement`, `commits`, `size`, `head_of`, `SIZE`, `CHECKS`; the first-review form, D3, D4, D6-D8). `batch_git.remote_head`, moved from `batch_review._remote_head`. `work batch brief`. Module-map rows. | The tests failed first (`invalid choice: 'brief'`), then 10 passed; with `test_batch_review.py`, 22. Suite: 1302 passed. |
| 3 | `69899547` | `batch_reviewed.py` (`reviewed`, D12; `said`; `status_line`, `as_json`, D15). `work batch reviewed`; `status` and `--json` show the reviews. `stub_gh.py`'s docstring (D20). `test_pr_review_trace.py` (D19). r5, r7 out of `unbuilt:`; `## Implementation, may change` names `reviewed`, the record, `gh pr comment` and `gh pr ready`. | The tests failed first (13, the trace test naming r5, r7), then 12 + 2 passed. Mutations, each reverted: clean → `building` failed `test_r7_…`; the `Head:` check skipped failed `test_reviewed_refuses_a_stale_brief`; r5 left in `unbuilt:` failed the trace test, naming r5. Suite: 1316 passed; model check and logic at baseline; unbuilt 21. |
| 4 | `19beb0de` | `batch_fix.py` (`cited_findings`, `for_finding`, `check`, D11; `trees`, `said`, D14). `review` runs `batch_fix.check` once a review is recorded; the brief's re-review form (D5); `resume` gives each open finding's worktree back and prints its line; `review` prints D15's `next:` line before the URL. batches.md's Implementation bullet names the fix checks. Module-map rows. | 6 of 10 tests failed first (no `batch_fix`, no re-review form, no `next:`); 4 passed at once (Deviation 2). Then 10 passed; with every batch test and the batches scenarios, 146. Mutations, each reverted: `check` skipped failed both Review Focus 4 tests; the re-review range from `forked_from` failed the re-review brief test. Suite: 1325 passed (plus one flake, Open problems). |
| 5 | `405a3105` | `agents/pr-reviewer.md` (tools Read, Glob, Grep, Write; opus; the six pinned sentences; D9's example verbatim, with a reproduction in place of `…`). `REVIEWERS` gains it; README's agents list and tools table. r3, r4, r6, r8 out of `unbuilt:`; Implementation names the agent and its brief. | The tests failed first (no agent), then 5 passed; with `test_agents.py` and the trace, 23 passed, 46 subtests. Suite: 1331 passed, 135 subtests; unbuilt 17. |
| 6 | `930dad0f` | building-a-batch's step 7 "Review and fix" (brief, a fresh `pr-reviewer` on the brief's path alone, `reviewed`; on `awaiting-merge` the link to the person; on `building`, `resume` and one subagent an item at once, with `Item:` and `Finding:`; `review` again; parking after the third review, D23), four Red Flags rows. `ORDER` grows. pr-review `unbuilt: []`, the loop in its Implementation section, and a `## Not yet` (D23's cap, inline comments, recurring findings, `awaiting-merge` → `abandoned`). | 4 of the 5 tests failed first (the trace test too); `test_r2_…` passed at once, being a negative check (Deviation 2). Then 11 passed; with shaping-items, the trace and agents, 36. Suite: 1335 passed. |
| 7 | this commit | Every figure above; the smoke run; the skill's trailer sentence (Deviation 4); this report; the records index row; every box of the plan ticked. | As in Final state. |

## Deviations

1. **`published` commits `src/b1.txt`** on `batch-1-b1` (`Item: b1`), so the first brief's `change.diff` holds a file
   that is not `spec/` (the plan's `test_the_first_brief_…` asks for `src/b1.txt`, which `build` alone does not
   write). `published(park=True)` parks b2 instead of finishing it, for the parked-item brief test, which is its own
   test (`test_a_parked_item_is_not_in_the_brief`) because `park` needs a `building` batch.
2. **Tests that passed at RED.** In Task 4, the two re-review refusals and the fixed/not-fixed tests passed before
   `batch_fix` existed: their mechanism is `parse_findings` (Task 1) and `reviewed` (Task 3). In Task 6,
   `test_r2_no_review_after_a_task` is a negative check that holds while no step names `pr-reviewer`. Each still fails
   when its point is broken (checked by hand for r2: `pr-reviewer` put into step 5 fails it). Task 4 also gained
   `test_a_fixed_finding_closes_and_the_review_is_clean`, the one use of `FIXED_F1`.
3. **`work batch status` prints `reviews:` only for a batch with a pull request.** Plan 4's
   `test_status_prints_items_tasks_and_their_statuses` pins every line of an unpublished batch and must pass
   unchanged. A published batch with no review shows `reviews: none`, as D15 says.
4. **The plan's smoke fix commit** `-m "fix" -m "Item: b1" -m "Finding: f1"` makes `Item: b1` a paragraph of its own;
   git reads trailers from the last paragraph only, so `review` refused it as citing no item. Committed instead as one
   trailer paragraph. building-a-batch's step 7 now says the two lines go together as the last paragraph, and why.
5. **Smaller calls** (decided by the implementer; revisit):
   - `reviewed` returns the `Review`; `said(root, review)` reads the open findings after it.
   - `reviewed`'s `range` is computed (`forked_from`, or the last review's head, `..head`); only `Head:` is read from
     the brief.
   - `--json`'s `reviews[].findings` is the list of the review's finding ids.
   - The judgement decisions, `[review] size` and `[review] checks` are read from the base checkout; the diff, the
     size counts and the runs from the batch worktree.
   - The brief refuses another branch with its own message (`work batch brief: batch-1 is built from main; …`),
     command first as plan-4 M4 ruled, rather than `batch_plan.on_base`'s `work batch:`.
   - An empty `## Earlier findings` is accepted when no finding is open (a re-review after D22's park); an entry for
     an id that is not open is refused.
   - A fix commit citing no open finding is refused with the item's open findings named, or "take the commit off
     <branch>" when it has none.
6. **The end-of-branch review** is not part of this run: the plan gives it to a separate reviewer, into
   `plan-5-review.md`, over `4dd78e68..HEAD`.

## Decisions D1-D24

All kept, with these notes:
- D3: kept; the stale check is `remote_head` (moved to `batch_git`, Task 2).
- D9: kept; the grade and triage are checked before the item, so a heading's error is named first.
- D12: kept; step 1's refusal names the brief's path and `pr-reviewer`.
- D14: kept; `resume` prints the finding lines after the task lines.
- D15: kept, with Deviation 3.
- D19: kept; the helper that reads the names is `named_tests` (a `tested` was collected by pytest as a test).
- D20: kept; the stand-in needed no change but its docstring.

## Open problems for plans 6-9

- The judgement decisions are empty until plan 6 sorts `spec/decisions/` by tier: every brief says `none: no
  design-decision is tier: judgement`.
- A real `pr-reviewer` run on a real batch has not been measured (plan 7): only the test's hand has written a findings
  file.
- Plan 9 deletes `bdd-task-reviewer`, `bdd-branch-reviewer`, `supervise_review_read.py` and `supervise_branch_runs.py`,
  and updates the glossary's `review` to name the pull request review.
- A rerun after a failed `gh pr ready` posts a second comment (accepted, D12).
- `said` prints `1 findings` for one finding.
- A flaky failure in tests this plan did not touch: `tests/scripts/test_backlog_moves.py::test_work_answer_on_a_work_item_is_unchanged`
  failed once, with `shutil.Error` copying `.git/objects/maintenance.lock`, which git's background maintenance had
  removed during the copy. It passes alone 3 of 3. An earlier failure, whose name was not captured, is likely the
  same one.
- D16 still holds: `abandon` refuses an `awaiting-merge` batch.

## Files

- Created: `scripts/batch_findings.py`, `scripts/batch_brief.py`, `scripts/batch_reviewed.py`, `scripts/batch_fix.py`,
  `agents/pr-reviewer.md`, `tests/scripts/review_testing.py`, `tests/scripts/test_batch_findings.py`,
  `tests/scripts/test_batch_brief.py`, `tests/scripts/test_batch_reviewed.py`, `tests/scripts/test_pr_review_trace.py`,
  `tests/scripts/test_batch_fix_loop.py`, `tests/scripts/test_agent_pr_reviewer.py`, this report.
- Modified: `scripts/batch_plan.py`, `scripts/batch_git.py`, `scripts/batch_review.py`, `scripts/batch_tasks.py`,
  `scripts/batch_cli.py`, `tests/scripts/stub_gh.py`, `tests/scripts/test_agents.py`,
  `tests/scripts/test_skill_building_a_batch.py`, `skills/building-a-batch/SKILL.md`,
  `spec/capabilities/pr-review.md` (`unbuilt:`, `## Implementation, may change`, `## Not yet`),
  `spec/capabilities/batches.md` (`## Implementation, may change`), `README.md`, `CLAUDE.md`,
  `.shop/records/README.md`, `plan-5-pr-review.md` (boxes ticked).
