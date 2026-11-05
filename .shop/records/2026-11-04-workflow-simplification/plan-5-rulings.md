---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-5-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 5 of the workflow simplification: rulings on the review, and what was done with each finding

`plan-5-review.md` (committed in `4f2c05f6`) asked the person three questions. The person was not available. Each
ruling below was **ruled by the main session without the person, 2026-11-05; revisit.** The fixes are on branch
`workflow-simplification`, from `a6754a4a` to `2e409776`, not pushed.

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-05; revisit) | What was done |
|---|---|---|---|
| Q1 | May a fix commit cite another in-batch item's open finding? | Yes, as plan 4's Q2 lets a commit cite an earlier item. | `c5c5fe51`: `batch_fix.check` accepts a commit citing an open finding of any in-batch item. Test: `test_a_fix_may_merge_another_items_fix_to_resolve_a_conflict`. The skill says so in `4ccdb8be`. |
| Q2 | Run `[review] checks` at the base as well? | Yes, once a batch, both exit codes shown. | `d9bfd611`: see S5. |
| Q3 | Keep refusing a fix commit for an `observation`? | Yes. An observation worth doing becomes a `work idea`. | `4ccdb8be`: one line in step 7 of `building-a-batch`. The refusal itself is unchanged. |

## The findings

| # | What was done |
|---|---|
| S1 | Fixed as ruled (Q1) in `c5c5fe51`. A commit citing no open finding is now refused with every open finding and its item named (`the open findings are f1 (b1), f3 (b2)`), or `no finding is open: take the commit off <branch>`. The new test makes two fixes conflict in one file and merges b1's branch into b2's. It failed first with the message the review quoted. |
| S2 | Fixed in `8bf54e7e`. `_sections` and `_findings` read through `_fenced`, so a `## ` or `### ` line inside a fenced block is text. This holds in the agent's file and in the record. A `## ` section other than `Verdict`, `Findings` and `Earlier findings` is refused, naming it. `pr-reviewer` is told to quote code and Markdown only in fenced blocks. Tests: `test_a_fenced_heading_is_the_findings_text` (it round-trips through `render`/`parse`), and the `an unknown section` case. |
| S3 | Fixed in `4ccdb8be`. Step 7 of `building-a-batch` now covers three things. On a refused `reviewed`: run `work batch brief` again and dispatch a fresh `pr-reviewer` with the refusal; never edit the findings file. When no item is left in-batch: `work batch abandon`. A finding's text is in `.shop/batches/<n>/review-<k>.md`. Pinned by `test_each_refusal_of_the_review_loop_has_its_way_through`. |
| S4 | Fixed in `58c65502`. The brief writes `<scratch>/commits/<short sha>.patch` for each non-merge commit of the range, less `.shop/`. It names the path as `; patch: <path>` on the commit's `## Commits` line and under each finding's `commits for it:`. `change.diff` stays the net change. `pr-reviewer` is told to read each patch. Tests: `test_the_brief_gives_each_commit_its_own_patch` (the fix's patch holds only its own file) and `test_the_reviewer_reads_each_commits_own_patch`. |
| S5 | Fixed as ruled (Q2) in `d9bfd611`. `batch_brief.base_runs` runs each check at `forked_from` in a throwaway detached worktree, `<batch>-base`, which is removed afterwards. It caches the exit codes in the first review's scratch directory as `base-runs.json`, so the base runs once a batch. A check added later is run there then. Each run reads `Exit code: <head> (base: <base>)`. `pr-reviewer` makes a finding only of a check that fails at the head and passed at the base; one that failed at the base too is at most an `observation`. The `## Implementation, may change` section of `spec/capabilities/pr-review.md` says so. Tests: `test_each_run_gives_the_bases_exit_code_once_a_batch` (`0 (base: 1)`, then the cache read) and `test_a_run_failing_at_the_base_already_is_no_fix_now_finding`. |
| S6 | Fixed in `a6754a4a`, in one place. At import, the root `conftest.py` appends `maintenance.auto=false` and `gc.auto=0` to `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n`, after any that are already set. Every git the suite runs inherits them, `work`'s included: `scripts_env` and `gh_env` merge with `os.environ`, and no test git call replaces the environment. The copies at `test_backlog_moves.py:136` and `test_intake_outcome.py:139` also leave out `*.lock`. Probe: the lock was present after 20 of 20 commits without the config and after 0 of 20 with it. Test: `test_git_quiet.py`, which failed first. The suite ran three times with no failure. |
| M1 | Fixed in `75552f76`. `reviewed` catches the parse's `Refused` and gives it as `work batch reviewed: batch-1: <file>: …`. The long line is wrapped. |
| M2 | Fixed in `75552f76`. `open_findings` returns none for a batch that is `merged` or `abandoned`. Test: `test_a_closed_batch_has_no_open_finding`. |
| M3 | Fixed in `4ccdb8be`. The skill gives `git commit -m "<subject>" --trailer "Item: b<j>" --trailer "Finding: f<m>"`, checked by hand on git 2.55. The `cites no item` refusal of `done`/`review` adds that the `Item:` line is not in the message's last paragraph, which is the only one git reads. Test: `test_an_item_line_git_does_not_read_is_explained`. |
| M4 | Fixed in `75552f76`. `1 finding` is now singular. Subjects in `## Commits` and in `commits for it:` are in one pair of quotes, with a `"` or `\` inside escaped (`batch_findings.quoted`). Tests: `test_one_finding_is_said_in_the_singular`, `test_a_commit_subject_with_quotes_is_escaped`. |
| M5 | Fixed in `8bf54e7e`. A `fix now` finding with no text after `- where:` is refused. Test: the `fix now with no text` case. |
| M6 | Fixed in `75552f76`. A missing `brief.md` is refused as `has no brief <path>; run work batch brief <batch>, …`. `head_of`'s refusal starts with the command. Test: `test_reviewed_refuses_without_a_brief`. |
| M7 | Fixed in `2e409776`, since a mark was cheap. Each pr-review test is marked `@pytest.mark.requirement("pr-review#r<n>")`, and the marker is registered in `pytest.ini`. The trace reads the marks from the six files' syntax trees. A test in a class counts. Another capability's id does not count, and neither does a name with no mark. A marked test that is also `skip`, `skipif` or `xfail` is refused. A vacuous test still passes the trace; the behavioural tests beside it carry that. |

## Figures after the fixes

| Check | Result |
|---|---|
| Suite, three runs | **1356 passed**, 1 skipped, 14 xfailed, 135 subtests passed, each run (27 s). No failure. The ceiling listed `test_supervision.py::test_a_flaky_scenario_is_run_again_before_the_merge` (12-16 s) and `test_e2e_codified.py::test_a_request_goes_through_the_requirements_system_into_delivery` (10.5-11 s). The second is a load effect: alone it takes 6.7 s here and 6.7-6.9 s at `8f6b83c6`. |
| Timing run | `1 passed, 1371 deselected` |
| Unbuilt | `False ['r3'] 15 []` |
| `model check` / `logic` / `lexicon --check` | 53 / 16 / 19 / 0; `11 findings: 6 L5, 5 L6`; `401 terms, 0 problems` |
| `features generate --check` / `vocab --check` / `bindings --unbound` | exit 0; `every step has one handler`; `every binding names a scenario` |
| `tools size --limit 300` | silent: `batch_findings.py` 272, `batch_brief.py` 232, `batch_tasks.py` 236, `test_batch_fix_loop.py` 210 |
| `tools check` (the plan's file list) | ruff passed, vulture clean, no import contracts |
| Smoke loop | Ran with a bare-repository remote and the stand-in gh, under `/home/vscode/.claude/jobs/7e9ba079/tmp/smoke5fix/`. Brief 1 took 177 ms with the base runs, and gave `Exit code: 1 (base: 1)` for a check the batch did not break. Review 1 printed `1 finding, 1 fix now -> building`, and its fenced `## Behaviour` survived into the record and brief 2. The fix was committed with `--trailer` and accepted. Brief 2 took 148 ms, with the base cached, and named the fix's patch in `## Commits` and under f1. Review 2 printed `-> awaiting-merge`, and `merged` closed the batch. Porcelain was empty. gh calls: one create, two comments, one ready, one view. |
