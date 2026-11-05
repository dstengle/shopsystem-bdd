---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-5-review
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 5 of the workflow simplification: end-of-branch review

The one fresh end-of-branch review of plan 5 (review at the pull request), 2026-11-05. Range `4dd78e68..8f6b83c6` on
`workflow-simplification`, seven commits (`bb474074` … `8f6b83c6`). Read against `plan-5-pr-review.md` (Review Focus,
Global Constraints, D1-D24), `plan-5-implementation.md`, `design.md` goal 6, the rulings of plans 1-4, `CLAUDE.md`,
`agents/pr-reviewer.md` and `skills/building-a-batch/SKILL.md`. Nothing in the repository was changed except this
file, which is not committed. The hands-on loop ran in `/home/vscode/.claude/jobs/7e9ba079/tmp/review5/repo`, with a
bare remote `repo.git` and the stand-in gh. The real GitHub remote was never used.

## Verdict

**Approve, with should-fix items before plan 7 measures a real run.** Every figure in the report reproduces. The
eight `pr-review` lines are built as the plan says. All five Review Focus classes are pinned by tests that fail when
their point is broken, and they behave the same by hand. The state machine is right: `in-review` → `building` on a
fix-now finding, `in-review` → `awaiting-merge` on a clean review, nothing committed when gh fails, and parked
findings closed.

Nothing is blocking. Five things should be fixed, and one of them came from the person's list:
- The skill's own conflict remedy deadlocks the fix loop (S1).
- A `## ` line in a finding's text silently loses the rest of the finding (S2).
- The skill does not say what to do on two refusals the loop can reach (S3).
- The reviewer cannot read the individual commits it is told to read (S4).
- The runs say nothing about what the change caused (S5).
- The flaky test has a confirmed cause and a one-line fix (S6).

## Verification: report against what I got

| Check (the plan's exact invocation) | Report | Got |
|---|---|---|
| `python3 -m pytest -q` | 1335 passed, 1 skipped, 14 xfailed, 135 subtests | **same** (26.6 s). The run also printed `tests over the 10 s ceiling: 16.02 test_supervision.py::test_a_flaky_scenario_is_run_again_before_the_merge`. That is not this plan's code; it is a load effect, and the report does not mention it. |
| `python3 -m pytest -m timing -n 0 -q` | 1 passed, 1350 deselected | **same** (1.7 s) |
| unbuilt (Task 7 Step 1) | `False ['r3'] 15 []` | **same** |
| `model check \| tail -1` | 53 / 16 / 19 / 0 | **same** |
| `model logic \| tail -1` | 11 findings: 6 L5, 5 L6 | **same** |
| `model lexicon --check \| tail -1` | 401 terms, 0 problems | **same** |
| `features generate --check` | exit 0 | **exit 0** |
| `features vocab --check \| tail -1` | every step has one handler | **same** |
| `features bindings --unbound` | every binding names a scenario | **same** |
| `tools size --limit 300` | silent | **silent, exit 0**. `batch_tasks.py` 233 (cap 241), `batch_review.py` 148 (cap 170), `batch_cli.py` 154. `scripts/work`, `test_batch_review.py` and `spec/index.md` are unchanged in the range. |
| `tools check $(git diff --name-only fbbd1466...HEAD -- '*.py')` | clean | **ruff passed, vulture clean, import-linter has no contracts** |
| Module map | rows for 4 new modules, `review_testing.py` named | **present**. The `batch_git`, `batch_plan`, `batch_tasks`, `batch_review` and `batch_cli` rows are updated. |
| Smoke: brief time | 179 ms, 195 ms | 189 ms, 193 ms (stand-in checks). 577 ms with the four default `CHECKS` in the fixture repo. |

### The review loop by hand (scratch repo, stand-in gh)

| Step | Result |
|---|---|
| brief 1 | `Review: 1 (first; …)`. The range is `forked_from..head`. `## Commits` holds exactly the batch's 5 commits and none of `main`'s `work batch` commits. `## Items` gives both items with their lines. `status --porcelain` stays empty. A check exiting 3 shows `Exit code: 3`. |
| malformed findings | Refused, naming the file and the line, with HEAD and the gh calls unchanged, for: no verdict; `fix now` with `- item: -`; `- item: b1 "label"`; `Fix now`; `fix-now`; a bold grade; `None.` followed by a finding; `- f1: not fixed` with no reason. **Accepted by mistake: a finding whose text holds a fenced `## ` line (S2).** |
| stale brief | A commit on `batch-1` after the brief: refused with `the batch branch moved since the brief; run work batch brief batch-1 again`. Nothing recorded. |
| reviewed, fix-now | `-> building` and `open f1 …`. `status` gives `reviews: 1, last fix-now; open f1 …`. `--json` gives `reviews` and `open`. `resume` prints the D14 line. |
| fix commit trailers | Two `-m` paragraphs: refused as `cites no item`. `Item:` only: refused, naming `b1's open findings are f1`. `Finding: f7` and `Finding: F1`: refused. One paragraph `Item: b1` + `Finding: f1 (abandon status)`: accepted, because extra words are tolerated. |
| no fix for an open finding | `f2 b4 "Fourth" (fix now) has no commit citing it; fix it on batch-2-b4 with Finding: f2, or park b4`. |
| re-review range | `Range: <review 1 head>..<new head>`. `## Earlier findings` gives f1 with its fix commit. `## Commits` holds only the fix and its merge (and the take-out commit when an item was parked). `change.diff` holds only the fix. |
| gh failing | `pr comment` failing, and `pr ready` failing on a clean review: exit 1, HEAD unchanged, the batch `in-review`, no record. Each rerun records. After the `pr ready` failure, PR 2 has a duplicate comment, as D12 accepts. |
| park closes findings | Park b3, which has f1: `review` asks only for f2. Brief 2 does not list f1. Clean → `awaiting-merge`. |
| merged | `batch-1 merged`. b1 and b2 are `delivered`. `.shop/batches/1/` holds `plan.md`, `review-1.md` and `review-2.md`. Porcelain is empty. |
| extra: all items parked | Park batch-3's only item after a fix-now finding, then `review`: refused with `batch-3 has no item that is in-batch`. `abandon` works (S3). |
| extra: conflicting fixes | Two findings' fixes in one file on two items, then the skill's conflict remedy: refused (S1). |

## Findings

### S1, should fix: the skill's conflict remedy is refused inside the fix loop

- **Where:** `scripts/batch_fix.py:55-62`, against `skills/building-a-batch/SKILL.md:29`.
- **Evidence:** batch-4 had f1 on b5 and f2 on b6, and both fixes write `src/shared.txt`.
  - `review` refuses the conflict.
  - Step 6 of the skill says: "have the later item's subagent merge the earlier item's branch into its own". Done that way, in a resolving commit citing `Item: b6` and `Finding: f2`.
  - `review` then refuses: `7ca63fa "fix f1" on batch-4-b6 cites no open finding (a Finding: f<m> line); b6's open findings are f2`.
- **Why:** `check` runs `since..task.branch`, which includes the merged-in commits of the other item. Each of those must cite a finding of *this* item.
- **Effect:** The only way out is to park an item. The message is also wrong: the commit does cite an open finding, f1.
- **Fix:** Mirror plan 4's `citable` rule (rulings Q2) and accept a commit whose `Finding:` names an open finding of any in-batch item. Equivalently, leave out of an item's range the commits reachable from another in-batch item's branch. When it still refuses, say `cites f1, an open finding of b5, not of b6`. Add a fix-loop test: two items, conflicting fixes, resolved by the merge.

### S2, should fix: a `## ` line in a finding's text, or an unknown section, is dropped silently

- **Where:** `scripts/batch_findings.py:63-75` (`_sections`), `:142-151`.
- **Evidence:** A finding whose text quotes a diff in a code fence holding `## Behaviour` was accepted.
  - The record `review-1.md` and the PR comment keep the text only up to the unclosed fence (`The diff:` and three backticks).
  - The rest went into a section `Behaviour`, which `parse_findings` ignores.
  - Re-review brief 2 then shows f1 with the unclosed fence. Every later section of the brief renders inside that fence.
  - `## Notes` after the findings is ignored in the same way.
  - A fenced `### [g1] …` line, a spec heading quoted in a finding, is refused as a malformed heading. That refusal at least is not silent.
- **Effect:** In a repository whose spec and records are all Markdown headings, a reviewer quoting a file is likely. The fixer then gets half a finding.
- **Fix:**
  - Make `_sections` and `_findings` fence-aware: a line inside a fenced block is text.
  - Refuse any `## ` section other than `Verdict`, `Findings` and `Earlier findings`, naming it.
  - Add one sentence to the agent's findings-file section: "Quote code and Markdown only inside fenced blocks."
  - Test: the fenced `## ` case round-trips through `render`/`parse`; an unknown section is refused.

### S3, should fix: the skill does not explain two refusals its loop reaches

- **Where:** `skills/building-a-batch/SKILL.md:35` and `:39`.
- **First refusal:** `work batch reviewed` refuses a malformed findings file, naming the file and the line. The skill has no step for this.
  - The session may hand-edit the reviewer's file, which defeats the review.
  - Or it may send the refusal back to the finished agent, which breaks "fresh".
  - **Fix:** add a bullet: "A refused `reviewed` names the line: run `work batch brief` again (it removes the old file) and dispatch a fresh `pr-reviewer` with the brief's path and the refusal's text; never edit the findings file."
- **Second refusal:** after "the third review … park each item an open finding names … and review again", a batch whose every item is parked gets `review` refused with `has no item that is in-batch`, shown by hand on batch-3.
  - **Fix:** add "when no item is left in-batch, `work batch abandon <batch>`".
- **Related (minor):** step 7 says to give each fix subagent "the finding's text". `resume` prints the title only (`batch_fix.py:89`). Name the record `.shop/batches/<n>/review-<k>.md` as where the text is, or have `said` print the record's path.

### S4, should fix: the reviewer cannot read the individual commits it is told to read

- **Where:**
  - `scripts/batch_brief.py:176` and `:182`;
  - `agents/pr-reviewer.md:33`, `:37`;
  - `scripts/batch_brief.py:150-159` (`## Earlier findings`).
- **Evidence:** The brief gives each commit only as `<sha> "<subject>"`, plus one combined `change.diff` for the whole range. The agent has no shell (D2). So "read every commit its `## Commits` lists" (r3) and "read every commit the brief lists under each finding" (r6) can only mean reading subjects and the combined diff.
  - On a re-review with two findings fixed in one range, the agent cannot tell which hunks belong to f1's commits.
  - On a first review it cannot see that a test was weakened in one commit and restored in another.
- **Assessment:** r3 and r6 are met in letter, and the pinned sentences promise more than the brief delivers.
- **Fix:**
  - Write one patch per non-merge commit of the range into the scratch directory: `git format-patch --no-merges -o <where>/commits <range>`, or `git show --format=… <sha>` each.
  - Name each path in `## Commits`, and under each finding's `commits for it:`.
  - Keep `change.diff` as the net change.
  - A brief test: the fix commit's patch exists and holds only its own file.

### S5, should fix: the runs report the tree, not the change, and the agent makes every failing run a finding

- **Where:** `scripts/batch_brief.py:87-97`, `agents/pr-reviewer.md:54`.
- **Evidence:** Each check runs once, at `Head:`. The agent's rule is "a check that exited other than 0 is a finding".
  - With the default `CHECKS` in the fixture repo, three of the four exit 1 for reasons the batch did not cause: no Python, a stale `features/supervision.feature`, unbound fixture scenarios.
  - A failure already present at the base becomes a finding at every review. Graded `fix now`, it would hold the loop open until the D23 park.
  - In shopsystem-bdd itself the base passes all four today, so the risk is mostly for target repositories.
- **Fix:** Pick one:
  - (a) Also run each check at `forked_from`, in a throwaway worktree, once per batch and cached in the batch's first scratch directory. Give both exit codes: `Exit code: 1 (base: 1)`.
  - (b) At least tell the agent that a check failing on lines the change does not touch is an `observation`.

  (a) is better. It is also what plan 7 will want to measure.

### S6, should fix (outside the range): the flaky `test_work_answer_on_a_work_item_is_unchanged`

- **Where:**
  - `tests/scripts/conftest.py:63-65` (`backlog_repo`);
  - the copy at `tests/scripts/test_backlog_moves.py:136`. The same pattern is at `tests/scripts/test_intake_outcome.py:139`.
- **Cause, confirmed:** On this machine's git 2.55, every `git commit` starts a detached `git maintenance run --auto`, which holds `.git/objects/maintenance.lock` just after the commit returns.
  - Probe: 40 commits in a fresh repository; the lock was present right after **40/40** of them.
  - With `maintenance.auto=false`: **0/40**.
  - `shutil.copytree` races that process: the lock is listed, removed, then copied, which raises `shutil.Error`.
- **Fix:** Add `("maintenance.auto", "false"), ("gc.auto", "0")` to the config loop of `backlog_repo`, and to every fixture repository that a test copies or that `work` commits in (`batch_repo`, the bare remotes).
  - Simplest global form: at import in `tests/conftest.py`, `os.environ.update(GIT_CONFIG_COUNT="2", GIT_CONFIG_KEY_0="maintenance.auto", GIT_CONFIG_VALUE_0="false", GIT_CONFIG_KEY_1="gc.auto", GIT_CONFIG_VALUE_1="0")`. Every git subprocess, `work`'s included, inherits it.
  - Check that `batch_testing.py:23`'s env dict is merged with `os.environ`, not used in its place.
  - A belt on top: `copytree(..., ignore=shutil.ignore_patterns("*.lock"))`.

### M1, minor: `reviewed`'s parse refusals do not start with the command

- **Where:** `scripts/batch_reviewed.py:64-65`, `scripts/batch_findings.py` (each `Refused("%s: …" % rel)`).
- **Evidence:** `work: /…/findings.md: ## Verdict is missing or empty`. The Global Constraints say messages start with `work batch reviewed: …` (plan-4 M4).
- **Fix:** Catch `Refused` around `parse_findings` in `reviewed` and re-raise as `work batch reviewed: batch-1: <message>`.
- **Same place:** line 65 is 168 characters. Wrap it.

### M2, minor: a closed batch shows a parked item's finding as open again

- **Where:** `scripts/batch_findings.py:219-234`.
- **Evidence:** b3 was parked in batch-2 with f1. batch-2 was merged. b3 was answered, made ready and started in batch-3. Then `work batch status batch-2` says `reviews: 2, last clean; open f1 b3 "Third"`. `_still_in` asks whether the item is `in-batch` anywhere, not in this batch.
- **Effect:** Only one batch is open at a time (`batch_start.py:128`), so only a closed batch's `status` and `--json` are wrong. The fix loop is not affected.
- **Fix:** In `open_findings`, return `[]` for a batch that is `merged` or `abandoned`. Or also require the item to be a task of the open batch (`batch_plan.open_batch`) that is this batch.

### M3, minor: the trailer pitfall is explained, but awkwardly, and the refusal misleads

- **Where:** `skills/building-a-batch/SKILL.md:37`; the `cites no item` refusal of `review`/`done`.
- **Evidence:** A commit made with `-m "Item: b1" -m "Finding: f1"` is refused as `cites no item (an Item: b1 line)` while it holds that line. The skill's workaround, a newline inside one `-m`, is hard for a subagent to type right.
- **Fix:** In the skill, `git commit -m "<subject>" --trailer "Item: b<j>" --trailer "Finding: f<m>"` (git ≥ 2.32; 2.55 here). In the refusal, when a non-final paragraph holds `Item:`, add "git reads trailers from the last paragraph only".

### M4, minor: cosmetic output

- **Where:** `batch_reviewed.py:94`, `:96`; `batch_brief.py:59`.
- `1 findings`.
- `## Commits` lines nest quotes: `"batch-1: b1 "Abandon …""`.
- **Fix:** Pluralise. Quote subjects with `repr`-free escaping, or drop the outer quotes for subjects that hold `"`.

### M5, minor: a `fix now` finding with no text is accepted

- **Where:** `scripts/batch_findings.py:113-116`.
- **Evidence:** A finding with only `- item:` and `- where:` parses with an empty body. The fixer then gets a title only.
- **Fix:** Refuse an empty body for `fix now` (D9 says free text follows).

### M6, minor: `reviewed` with findings but no brief says the branch moved

- **Where:** `scripts/batch_reviewed.py:59`.
- **Fix:** Refuse a missing `brief.md` with its own message: `no brief …; run work batch brief`. `head_of`'s refusal (`batch_brief.py:80`) also lacks the command prefix.

### M7, minor: the trace test is a real check of the bookkeeping, not of the behaviour

- **Where:** `tests/scripts/test_pr_review_trace.py:16-37`.
- **Judgement:** It is more than a ritual. It failed under the Task 3 mutation (r5 left in `unbuilt:`), so it really ties `unbuilt:` to the existence of a test. But it checks names only:
  - a vacuous `test_r2_…`, which passed at RED (Deviation 2), satisfies it;
  - a `test_r3_…` written for another capability in one of the six files would satisfy pr-review r3;
  - a test of r<n> marked skip or xfail still counts;
  - a test inside a class does not count.
- **Fix, cheap:** a `@pytest.mark.requirement("pr-review#r5")` mark read through pytest's collection, in a conftest hook or a `pytest --collect-only -q -m …` run. Refuse a marked test that is skipped or xfailed. This is low priority; the strong checks of each line are the behavioural tests beside it.

## Questions for the person (recommended rulings; the person is unavailable)

- **Q1 (S1).** May a fix commit cite another in-batch item's open finding, as plan-4 Q2 lets a commit cite an earlier item?
  **Recommended: yes.** It is the same reason (a branch that merged another's carries its commits), and it is the only way two fixes in one file meet without a park.
- **Q2 (S5).** Run `[review] checks` at the base as well, and pay about twice the brief's run time once per batch?
  **Recommended: yes, cached per batch.** A finding must be the batch's own, or the loop chases the base.
- **Q3 (D11, observed by hand).** A commit after a review that cites no fix-now finding is refused, so an `observation` cannot be fixed in the loop.
  **Recommended: keep it.** Convergence matters more. An observation worth doing becomes an `idea` in the backlog (`work idea`). The skill should say so in one line.

## The deviations, judged

1. **`published` commits `src/b1.txt`; `park=True` parks b2.** Right: the plan asked for a non-spec file in `change.diff`, and `build` alone writes none.
2. **Tests that passed at RED.** Honest and acceptable. Their mechanism existed already, and the r2 negative check was mutated by hand. Recording it is the right practice.
3. **`reviews:` only with a pull request.** Right: plan 4's pinned `status` lines must pass unchanged, and D15's `reviews: none` still shows for a published batch.
4. **The plan's smoke fix commit was wrong.** A good catch, and fixing the skill was the right call. M3 gives a less error-prone command than the newline inside one `-m`.
5. **Smaller calls.** Each is sound:
   - `reviewed`'s range is computed rather than read from the brief. It is the same value, and one fewer thing trusted from a scratch file.
   - The brief has its own message on another branch, command first, as M4 ruled.
   - `## Earlier findings` may be empty when nothing is open, which is needed after a D22 park.
   - "take the commit off <branch>" is a good way out.
6. **The end-of-branch review is separate.** This is it.

The decisions D1-D24 are kept as the report says. D3's stale check, D11's two refusals, D12's order with nothing committed on a gh failure, and D22's park were each confirmed by hand. D2's claim "with no shell it cannot read a commit the brief does not give" holds, but S4 shows the flip side: it cannot read the commits the brief does give, either, except as one diff.
