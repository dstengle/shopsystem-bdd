---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-5
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: draft
---

# Plan 5: Review at the pull request — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `pr-review` capability, so that all 8 of its requirements are met. Each batch gets one adversarial
review at its pull request, from the new `pr-reviewer` agent. The first review reads the batch's own commits and its
items' requirements. A fix-now finding sends the batch back to `building`, where it is fixed on the item's branch.
The re-review reads only the commits for each finding. A clean review sets the batch `awaiting-merge` and marks the
pull request ready. Every finding is recorded with its grade under `.shop/batches/<n>/`. This closes plan 4's two
open ends: nothing set a batch from `in-review` back to `building`, and nothing wrote `awaiting-merge`.

**Architecture:**
- **`work` keeps the state; the session dispatches the reviewer (D2).** As in plan 4, `work` starts no `claude -p`.
  The batch session (skill `building-a-batch`) works the loop:
  1. `work batch review` publishes the pull request;
  2. `work batch brief <batch>` writes what the reviewer reads;
  3. the session dispatches one fresh `pr-reviewer` agent on that brief, and the agent writes a findings file;
  4. `work batch reviewed <batch>` validates the file, numbers and records the findings, comments on the pull request
     and sets the batch `building` (a fix-now finding is open) or `awaiting-merge` (clean).
  5. Fixes are commits on the item's branch citing `Item: b<j>` and `Finding: f<m>`, made in the task's worktree.
     `work batch review` checks them and pushes only. Then comes the next brief, which is a re-review.

  The suite tests every state change with git, a bare remote and the stand-in gh. It uses no stand-in claude: a test
  writes the findings file the agent would write.
- **Each `pr-review` line is met as follows:**

  | id | line (short) | met by | checked by |
  |---|---|---|---|
  | r1 | `work` publishes → `pr-reviewer` writes a review | `building-a-batch`'s review step; `work batch review` prints the next step | skill test `test_r1_…` (Task 6) |
  | r2 | a task becomes `done` → no review | the skill dispatches no reviewer at `done`; `reviewed` refuses a `building` batch | skill test `test_r2_…` (Task 6); `test_reviewed_refuses_a_batch_that_is_building` (Task 3) |
  | r3 | first review reads every item requirement and every batch commit, no other commit | `work batch brief` (the range `forked_from..head`, `## Items`); the agent has no shell | brief tests (Task 2); agent test `test_r3_…` (Task 5) |
  | r4 | reads every `judgement` design-decision | the brief's `## Judgement decisions`; the agent text | brief test (Task 2); agent test `test_r4_…` (Task 5) |
  | r5 | a fix-now finding → `work` sets the batch `building` | `work batch reviewed` | `test_r5_…` (Task 3) |
  | r6 | re-review reads every commit for each finding | the `Finding:` trailer; the re-review brief (range `<last head>..head`, `## Earlier findings`); `review`'s fix checks | fix-loop tests (Task 4); agent test `test_r6_…` (Task 5) |
  | r7 | clean → `work` sets the batch `awaiting-merge` | `work batch reviewed`, `gh pr ready` | `test_r7_…` (Task 3) |
  | r8 | each finding graded, written to a file | the findings file's format, refused ungraded by `reviewed`; the agent text | `test_batch_findings.py` (Task 1); agent test `test_r8_…` (Task 5) |

  `pr-review` is a `guarantees` capability with no feature file, so no strict xfail holds its ids. D19's trace test
  (Task 3) takes its place: an id out of `unbuilt:` must have a test named `test_r<n>_…`, and an id still in
  `unbuilt:` must have none.
- **New modules behind `scripts/work`** (each ≤ 300 lines):
  - `batch_findings.py`: the findings file and the review record;
  - `batch_brief.py`: `work batch brief`;
  - `batch_reviewed.py`: `work batch reviewed`;
  - `batch_fix.py`: the fix loop's checks for `review` and its worktrees for `resume`.
- **Reused:**
  - plan 4's `batch_plan`, `batch_git` (the lock, `tree_for`, `trees_dir`, `remote`), `batch_gh.gh`, and
    `batch_tasks`' `building`, `lines_commit`, `item_ids`, `task_label`;
  - `backlog_items` and `backlog_lines`;
  - the stand-in `tests/scripts/stub_gh.py`, which already records and accepts `pr comment` and `pr ready`.
- **Rewritten small, not imported:** the brief shape of `supervise_review_read.py` and `supervise_branch_runs.py` (the
  commits of a range, the change less `.shop/`, runs given with their command, exit code and output). It also borrows
  `bdd-branch-reviewer`'s "What you look for" and "Triage" sections, adapted from work-items to items.
- **What plan 9 retires:** `pr-reviewer` replaces both `bdd-task-reviewer` (per task) and `bdd-branch-reviewer` (per
  initiative). Plan 9 deletes both agents, with `supervise_review_read.py`, `supervise_branch_runs.py` and the rest of
  `supervise*`. `architecture-reviewer` stays, run when the person asks. Nothing in this plan imports `supervise*`.

**Tech Stack:** Python 3.11 (standard library: `tomllib`, `subprocess`, `dataclasses`), git (worktrees, trailers, a
bare remote in tests), pytest with xdist. `gh` is reached only through `$SHOPSYSTEM_WORK_GH`, and the suite uses
`tests/scripts/stub_gh.py`.

**Spec:**
- Read first: `spec/capabilities/pr-review.md` (its 8 lines and its `unreviewed` condition).
- The glossary of `spec/index.md`:
  - `review`, `review finding`, `grade` (`Critical`, `Important`, `Minor`), `triage` (`fix now`, `observation`,
    `drop`);
  - `clean` ("A pull request is clean when no review finding on the pull request is `fix now`");
  - the batch statuses with their transitions (`in-review` → `building`: a fix-now finding; `in-review` →
    `awaiting-merge`: a clean review);
  - `tier` (`judgement`) and `pull request`.
- `design.md` goal 6, with the "Decided by the person" bullet on the merge ("When no fix-now finding is left, it marks
  the PR ready. The person merges.") and the session's call "PR review fixes happen on the batch's branch, and the
  review re-reads only what the fix touched".
- Read beside them:
  - `roadmap.md` (plan 5's row);
  - `plan-1-rulings.md`: S7 (r3's `unreviewed`), and P9 (triage and `fix now` lifted into the glossary);
  - `plan-4-batches.md` D4 (the base-branch rule), D11 and D20;
  - `plan-4-implementation.md` "Open problems";
  - `plan-4-rulings.md` Q2 (citable earlier items);
  - `spec/capabilities/batches.md`, `## Implementation, may change`.
- `brainstorming.md`: its r3 stays unbuilt and waits for plan 8's `work quote` (D17). This plan changes nothing in it.

## Global Constraints

- **Branch:** `workflow-simplification`, from `fbbd1466` or later. Every plan is built on this one branch. No new
  branch, no push.
- **Shell rule (the person's):** never combine `cp` and `rm` in one command; they need the person's approval
  together. Run them as separate commands, or leave scratch directories under
  `/home/vscode/.claude/jobs/7e9ba079/tmp`. Keep shell variables few.
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
  - `scripts/work` (213) is not changed; every new command goes through `batch_cli`.
  - `scripts/batch_tasks.py` (231) may grow by at most 10 lines.
  - `scripts/batch_review.py` (150) may grow by at most 20 lines.
  - `tests/scripts/test_batch_review.py` (172) is not changed. New tests go in new files.
- **Module map:** each new module gets a row in `CLAUDE.md`'s module map, in the task that creates it. A changed
  module's row is updated in the task that changes it. `review_testing.py` is named in the `tests/scripts/` row.
- **Spec lines:** no requirement line, group, term or relation row is edited or added anywhere.
  - In `pr-review.md` a task changes only `unbuilt:`, `## Implementation, may change` and a new `## Not yet`.
  - In `batches.md`, only `## Implementation, may change`.
  - `spec/index.md` is not changed (D16).
  - A line found wrong is reported, not changed.
- **The trace test** (D19, from Task 3 on): an id leaves `pr-review.md`'s `unbuilt:` in the same commit that adds
  its `test_r<n>_…` test, never before.
- **No network, no claude:** no test reaches a network or starts a session.
  - Pushes go to a bare repository on disk.
  - `gh` is `$SHOPSYSTEM_WORK_GH`, the stand-in (the `batch_repo` fixture sets it).
  - The agent's findings file is written by the test.
- **The person's checkout:** no command of this plan switches `--root`'s branch, or writes anywhere except:
  - `.shop/batches/` (committed on the base);
  - the worktrees directory (`[batch] worktrees`, ignored), where briefs and findings files live;
  - `.git`.

  `work batch brief` commits nothing, and `git status --porcelain` of the base is unchanged by it.
- **Refusals:** a refused command raises `workqueue.Refused`, so `work: <message>` is printed with exit 1. Nothing
  is committed, no gh call is made after the refusal's cause, and the base checkout is byte-identical. Messages start
  with the command (`work batch reviewed: …`), as plan-4 M4 ruled.
- **Names next to ids:** an item is named as `b<j> "<title>"` (`backlog_items.label`), a batch as `batch-<n>`, a
  finding as `f<m>` with its item's label, a commit as `<short sha> "<subject>"` (design goal 10).
- **Old behaviour kept:** every test of plan 4 passes unchanged. That includes `test_a_second_review_pushes_only`: a
  batch with a pull request and no recorded review is pushed with no fix check.
- **Baselines** (measured at `fbbd1466`). Every task keeps them, and none may get worse:
  - `python3 -m pytest -q`: `1277 passed, 1 skipped, 14 xfailed, 132 subtests passed` (23 s wall on this machine).
    `pr-review` has no scenarios, so xfailed stays 14. Passed grows by the new script tests, and the subtests by
    `test_agents.py`'s rows for `pr-reviewer`.
  - `python3 -m pytest -m timing -n 0 -q`: `1 passed, 1292 deselected` (the deselected count grows with the suite).
  - Unbuilt ids (`spec_unbuilt.unbuilt`): 23 with no problems. They are brainstorming r3; conversation r1-r4;
    decision-tiers r1-r6; pr-review r1-r8; telemetry r1-r4. At the end there are 15, and `pr-review` is absent.
  - `python3 scripts/model check | tail -1`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
  - `python3 scripts/model logic | tail -1`: `11 findings: 6 L5, 5 L6`.
  - `python3 scripts/model lexicon --check | tail -1`: `401 terms, 0 problems`.
  - `python3 scripts/features generate --check`: exit 0.
  - `python3 scripts/features vocab --check | tail -1`: `every step has one handler`.
  - `python3 scripts/features bindings --unbound`: `every binding names a scenario`.
  - `python3 scripts/tools size --limit 300`: silent, exit 0.
  - `python3 scripts/tools check <the branch's changed Python>`: ruff and vulture `clean`. import-linter states no
    contracts.
- **Smoke steps** run `work` through a shell function, which bash and zsh both run:
  `r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }`.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-05;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Built and committed on `workflow-simplification`, as the main session ruled for every plan. |
| D2 | **The review is an agent the session dispatches** (the design left "agent or skill" to the builder).<br>- `agents/pr-reviewer.md`: tools `Read, Glob, Grep, Write`, with no Bash, no Edit and no Agent; model `opus`.<br>- A fresh agent for each review, so that every review, the re-reviews included, is adversarial and starts from the brief alone.<br>- With no shell it cannot read a commit the brief does not give (r3's "shall not read a commit outside the batch").<br>- `work` starts no session. The batch session dispatches it (`subagent_type` `shopsystem-bdd:pr-reviewer`, prompt: the brief's path). |
| D3 | **`work batch brief <batch>`** writes the review's brief and prints its path. It takes a batch that is `in-review`, with a `pull_request`, run on its base. The batch branch must be at the remote's head of it, so that what is reviewed is what was published; otherwise it is refused, naming `work batch review`.<br>- Review k is the number of recorded reviews + 1.<br>- It writes `<trees>/batch-<n>-review-<k>/brief.md` and `change.diff`, in the ignored worktrees directory, and commits nothing.<br>- The batch worktree `<trees>/batch-<n>` is made again with `tree_for` if it is missing.<br>- A brief run again rewrites both files and removes a `findings.md` left there, printing `removed an old findings.md`. |
| D4 | **The first review's brief** (the pull request is `unreviewed`: no review is recorded) holds:<br>- `Range: <forked_from>..<head>`;<br>- `## Items`: each `in-batch` item's label, its file `.shop/backlog/b<j>.md`, and each requirement id with its line's text;<br>- `## Judgement decisions` (D6), `## Rules` (`CLAUDE.md` when it exists), `## Size` (D7), `## Runs` (D8);<br>- `## Commits`: every commit of the range, oldest first, as `<short sha> "<subject>"` with its `Item:` and `Finding:` values;<br>- `## Change`: the path of `change.diff`, which is `git diff <range> -- . ':(exclude).shop'`.<br>The base's own commits after `forked_from` (`work batch start`/`done`/`review` on `main`) are outside the batch and never listed. |
| D5 | **A re-review's brief** (a review is recorded) holds:<br>- `Range: <the last review's head>..<head>`;<br>- `## Earlier findings`: each open finding (D10) with its text, its item's file and the commits for it (D11);<br>- `## Judgement decisions`, `## Rules`, `## Size` and `## Runs` (of this range);<br>- `## Commits` and `## Change` of this range only.<br>It has no `## Items`: r3 binds the first review only (plan-1 ruling S7). The header line reads `Review: <k> (re-review of the fix)`; the first review's reads `Review: 1 (first; the pull request is unreviewed)`. |
| D6 | **Judgement decisions** are the files `spec/decisions/*.md` whose frontmatter has `tier: judgement`, each listed as `<path>: <summary>`. None has a tier today; plan 6 sorts them. Until then the brief says `none: no design-decision is tier: judgement`, and the agent reads `CLAUDE.md` as the rules. |
| D7 | **Size:** `## Size` gives `<files> files, +<insertions> -<deletions>` of the range less `.shop/`, and the limit `[review] size` of `.shop/delivery.toml` (default 1000 changed lines). Over the limit it says `over the limit`. The agent writes such a change as a `Minor` `observation` naming the items that make most of it; plan 7's telemetry reads it as the batch-size knob. |
| D8 | **Runs:** each command of `[review] checks` (a TOML array of strings) is run in the batch worktree with the plugin's scripts on `PYTHONPATH`. The brief gives each one's command, exit code and last 40 lines, indented. The default is `{scripts}/tools size --limit 300`, `{scripts}/tools check --base {forked_from}`, `{scripts}/features generate --check` and `{scripts}/features bindings --unbound`, each run with `python3`. `{scripts}` and `{forked_from}` are filled in. The tests set `checks = ["python3 -c \"print('ran')\""]`. The suite is not run again: `review` ran it on this head and refuses otherwise. |
| D9 | **The agent's findings file** is `<trees>/batch-<n>-review-<k>/findings.md`:<br>- `## Verdict`: one paragraph, not empty.<br>- `## Findings`: one `### <grade> <triage>: <title>` heading per finding, where the grade is one of `Critical`, `Important`, `Minor` and the triage one of `fix now`, `observation`, `drop`. Under each heading come `- item: b<j>` (or `-`), `- where: <path>:<line>` (or `-`), then free text. The section is `None.` when there are none.<br>- `## Earlier findings` (re-review only): one `- f<m>: fixed` or `- f<m>: not fixed: <why>` for each open finding the brief lists, and no other.<br>The agent does not number its findings. A `fix now` finding names an `in-batch` item of the batch (the branch its fix goes on); any other names an item of the batch or `-`. |
| D10 | **Open findings and `clean`.**<br>- `work batch reviewed` numbers the new findings `f<m>`, continuing across the batch's reviews.<br>- A finding is open from its review on while it is `fix now`, until a later review says `fixed`, or its item leaves the batch (D22). `not fixed` keeps it open.<br>- A review is clean when, after it, no finding is open. That is the glossary's `clean`: no review finding on the pull request is `fix now` and unfixed. |
| D11 | **Commits for a finding.** A fix is one or more commits on the finding's item's branch, made in its task worktree. Each ends with `Item: b<j>` and `Finding: f<m>` (two git trailers), and `Finding:` may name several. On a batch with a recorded review, `work batch review` adds two checks before it merges, both under the existing lock:<br>- each non-merge commit of an in-batch item's branch after the last review's head must cite an open finding of that item. Otherwise it is refused: `work batch review: batch-1: <sha> "<subject>" on batch-1-b1 cites no open finding (a Finding: f<m> line)`.<br>- each open finding must have at least one such commit. Otherwise it is refused: `work batch review: batch-1: f1 b1 "…" (fix now) has no commit citing it; fix it on batch-1-b1 with Finding: f1, or park b1`.<br>The existing `Item:` and `.shop/` checks still hold. |
| D12 | **`work batch reviewed <batch>`**, under the lock, in this order:<br>1. The batch is `in-review` on its base, and `findings.md` exists. Otherwise it is refused naming the brief and `pr-reviewer`.<br>2. The brief's `Head:` is still the batch branch's head. Otherwise: `the batch branch moved since the brief; run work batch brief again`.<br>3. The file parses (D9) against the batch's items and open findings.<br>4. It renders `.shop/batches/<n>/review-<k>.md` (D13) in the review's scratch directory.<br>5. `gh pr comment <url> --body-file <that file>`.<br>6. When the review is clean, `gh pr ready <url>`.<br>7. The batch goes `building` (open findings) or `awaiting-merge` (clean). The record and `plan.md` are committed on the base: `work batch reviewed: batch-1 review 1 -> building; open f1 b1 "…"`, or `… -> awaiting-merge`.<br>A gh failure is refused with nothing committed. A rerun then posts the comment again (accepted; noted in the report). |
| D13 | **The review record** `.shop/batches/<n>/review-<k>.md`, committed on the base only (plan 4's D4):<br>- frontmatter `id: review/<context path>/batch-<n>/review-<k>`, `kind: review`, `batch`, `pull_request`, `head`, `range`, `result: fix-now` or `clean`;<br>- `# batch-<n> review <k>`, then `## Verdict`;<br>- `## Findings`, with each heading `### f<m> <grade> <triage>: <title>` and its lines kept;<br>- `## Earlier findings` as given.<br>`batch_findings.parse(render(r), rel) == r`. Plan 7's `measure batch` reads these for its defects. |
| D14 | **`work batch resume` on a `building` batch with open findings** also gives each open finding's task its worktree again, on its branch, if it is lost. That task stays `done`. For each finding it prints `f1 Important b1 "…" scripts/x.py:12: <title>: fix in <tree> on batch-1-b1 with Item: b1 and Finding: f1; then work batch review batch-1`. It commits nothing for that. |
| D15 | **What `review` and `status` print.** `work batch review` prints, before the URL (which stays the last line), `next: work batch brief batch-1, the pr-reviewer on it, then work batch reviewed batch-1`. `work batch status` gains `reviews: none`, or `reviews: 2, last fix-now; open f3 b2 "…"`. Its `--json` gains `reviews: [{"review", "result", "findings"}]` and `open: ["f3"]`. |
| D16 | **The glossary is not changed.**<br>- `review`'s definition still names the old kinds (work-item, branch, architecture review). Plan 9 adds "pull request review" when it retires work-item review.<br>- No transition `awaiting-merge` → `abandoned` is added. `abandon` keeps refusing an `awaiting-merge` batch; the person merges it, or the next plan adds the transition. |
| D17 | **brainstorming r3** stays unbuilt for plan 8's `work quote`, as plan 3 decided. The roadmap's "pr-review, brainstorming" for plan 5 is met by pr-review alone. |
| D18 | **Agents.** `pr-reviewer` joins `test_agents.py`'s `REVIEWERS`, so role-boundaries r2 (no Edit) and r5 (opus) hold for it, and r1 (only `initiative-round` has Agent) still holds. README gains it in the agents list and the tools table. `bdd-task-reviewer` and `bdd-branch-reviewer` are untouched; plan 9 deletes them. |
| D19 | **The trace test** `tests/scripts/test_pr_review_trace.py` reads the `def test_r<n>_` names of `PR_REVIEW_TESTS` (`test_batch_findings.py`, `test_batch_brief.py`, `test_batch_reviewed.py`, `test_batch_fix_loop.py`, `test_agent_pr_reviewer.py`, `test_skill_building_a_batch.py`). An id of pr-review out of `unbuilt:` must have such a test, and an id in `unbuilt:` must have none. It is the strict xfail's stand-in for a guarantees capability. |
| D20 | **The stand-in gh** needs no new behaviour: `pr comment` and `pr ready` are recorded, print nothing, and fail under `$STUB_GH_FAIL`. Its docstring names them. |
| D21 | **Where findings are recorded:** only in `.shop/batches/<n>/review-<k>.md` and as the pull request's comment. Not in `.shop/records/`: the `## Implementation, may change` of pr-review says so. Recurring findings are plan 7's to count. |
| D22 | **A parked item's findings close.** An open finding whose item is parked after its review (`work batch park` on the `building` batch) is no longer open. `review` takes the item's lines out, as plan 4's B1 fix does; the re-review reads that commit in its range, and its brief does not list the finding. This is the way out of a finding the batch session cannot fix. |
| D23 | **No cap on rounds in code.** `building-a-batch` says: after the third review that leaves a finding open, park each item an open finding names, with the finding as its question, then review again. Revisit with plan 7's figures. |
| D24 | **Re-review triage** (in the agent): on a re-review, a new finding is `fix now` only when the fix's own change is wrong. Anything else it finds is an `observation`, so the loop converges, as `bdd-branch-reviewer`'s re-review rule does. |

**The findings file and the record** (`batch_findings` parses the first and renders the second exactly so):

```
## Verdict

The batch builds both items; one finding to fix.

## Findings

### Important fix now: abandon leaves the initiative started
- item: b1
- where: scripts/work:12
The line says `abandoned`; the code writes `started`. Fix: set the status.

### Minor observation: the message could name the initiative
- item: -
- where: -
Reproduction: …

## Earlier findings
- f1: fixed
```

```
---
id: review/ex.com/prod/ctx/batch-1/review-2
kind: review
batch: batch-1
pull_request: https://github.com/ex/ctx/pull/1
head: 4c1f…
range: 9a0e…..4c1f…
result: fix-now
---

# batch-1 review 2

## Verdict
…
## Findings

### f2 Important fix now: abandon leaves the initiative started
- item: b1
…
## Earlier findings
- f1: fixed
```

## Review Focus

These are the input classes the spec implies but no line's check exercises, most likely to bite first. Each has its
test in the task named.

1. **A findings file the agent got wrong.** Examples: no verdict; a grade or triage outside the glossary's values
   (`Major`, `later`); a `fix now` finding naming no item, a parked item or an item outside the batch; a re-review
   that leaves out an open finding or names one that is not open. `reviewed` should refuse each, naming the file and
   the line, with nothing committed and no gh call.
   Pinned in Task 3 (`test_reviewed_refuses_a_malformed_findings_file`) and Task 4
   (`test_reviewed_refuses_a_re_review_that_leaves_out_an_open_finding`).
2. **A stale review.** The batch branch moves between `brief` and `reviewed`: a fix is pushed, or `review` is run
   again. `reviewed` should refuse, naming `work batch brief`, and record nothing.
   Pinned in Task 3: `test_reviewed_refuses_a_stale_brief`.
3. **The range.** The first brief should list exactly `git rev-list forked_from..head`. That excludes the base's own
   `work batch` commits on `main`, made after the fork. A re-review should list only the commits after the last
   review's head, including `review`'s take-out commit when an item was parked during the fixing.
   Pinned in Task 2 (`test_the_first_brief_gives_the_batchs_range_and_no_other_commit`) and Task 4
   (`test_the_re_review_brief_gives_the_commits_for_each_finding`, `test_a_parked_items_finding_needs_no_fix`).
4. **A fix that does not say what it fixes.** Two cases: a commit after the review cites no open finding, or an open
   finding has no commit. `review` should refuse, naming the commit or the finding and the way out (`Finding: f<m>`,
   or park the item). Nothing should be pushed and no gh call made.
   Pinned in Task 4: `test_review_refuses_a_fix_commit_that_cites_no_finding` and
   `test_review_refuses_an_open_finding_with_no_commit`.
5. **gh failing while recording.** `pr comment` or `pr ready` fails. The batch should stay `in-review`, with no
   record committed and HEAD unchanged, and a rerun after the cause is fixed should record.
   Pinned in Task 3: `test_a_failing_gh_records_nothing`.

---

### Task 1: The findings file and the review record

Builds no requirement on its own. r8's refusal of an ungraded finding is here; r8 leaves `unbuilt:` with the agent in
Task 5.

**Files:**
- Create: `scripts/batch_findings.py`, `tests/scripts/review_testing.py`, `tests/scripts/test_batch_findings.py`
- Modify:
  - `scripts/batch_plan.py`: `commit` gains `files=None`.
  - `CLAUDE.md`: a row for `batch_findings.py`, and `review_testing.py` in the `tests/scripts/` row.

**Interfaces:**
- Produces, in `batch_findings.py`:
  - `GRADES = ("Critical", "Important", "Minor")`, `TRIAGES = ("fix now", "observation", "drop")`.
  - `@dataclass Finding: fid: str | None, grade, triage, title, item: str | None, where: str | None, body: str`.
  - `@dataclass Review: number: int, batch: str, ident, pull_request, head, range, result, verdict,
    findings: list[Finding], earlier: dict[str, str]`. `earlier` maps `f<m>` to `fixed` or `not fixed: <why>`.
  - `parse_findings(text, rel, items, in_batch, open_ids) -> tuple[str, list[Finding], dict]` (D9). Here `items`
    is the batch's item names, `in_batch` those still `in-batch`, and `open_ids` the open finding ids the file must
    answer (empty on a first review). It refuses as `<rel>: <what>`, naming the line.
  - `rel_of(batch_name, k) -> str`: `.shop/batches/<n>/review-<k>.md`.
  - `render(review) -> str` and `parse(text, rel) -> Review`, which round-trip (D13).
  - `reviews(root, batch) -> list[Review]` by number. A `review-*.md` not numbered `review-<k>.md` is refused.
  - `open_findings(root, batch) -> list[Finding]` (D10, D22): items no longer `in-batch` are dropped.
  - `next_fid(root, batch) -> int`.
  - `scratch(root, batch, k) -> Path`: `batch_git.trees_dir(root) / "<batch>-review-<k>"`.
- Produces, in `batch_plan.py`: `commit(root, batch, items, message, files=None)`. `files` is `{rel: text}`, written
  and committed with the plan.
- Produces, in `review_testing.py`:
  - `published(repo) -> str`: start, resume, build both tasks, `done` both, `review`; returns the URL. It reuses
    `test_batch_tasks.build`/`resumed`.
  - `findings(repo, k=1) -> Path`: the scratch `findings.md` path.
  - `FIX_NOW_B1`, `CLEAN`, `FIXED_F1`: findings texts in D9's form.

- [x] **Step 1: Write the failing tests** (`test_batch_findings.py`, mostly pure text):
  - `test_a_findings_file_parses`: the D9 example gives the verdict, two findings with the grade, triage, title,
    item (`b1` and None), where and body, and `{"f1": "fixed"}`.
  - `test_malformed_findings_are_refused`, parametrised. Each is refused naming `rel` and the heading or line:
    - no `## Verdict`, or an empty one;
    - `### Major fix now: x`;
    - `### Important later: x`;
    - a `fix now` with `- item: -`;
    - `- item: b9`, which is not in the batch;
    - a `fix now` naming a parked item;
    - a heading with no title;
    - `## Earlier findings` on a first review.
  - `test_none_is_no_findings`: `## Findings` holding `None.` gives `[]`.
  - `test_the_record_round_trips`: `parse(render(r), rel) == r`, and the text equals the D13 example's shape
    (frontmatter keys in order, `### f2 Important fix now: …`).
  - `test_open_findings_follow_the_reviews`, on records written by hand under `.shop/batches/1/`:
    - review 1 has f1 `fix now` (b1) and f2 `observation`;
    - review 2 has `f1: fixed` and a new f3 `fix now` (b2);
    - so `open_findings` is `[f3]`, and `next_fid` is 4;
    - with review 2's `f1: not fixed: …` it is `[f1, f3]`;
    - with b2 `needs-input` it is `[f1]`.
  - `test_a_review_file_not_numbered_is_refused`: `review-x.md` is refused.
  - `test_commit_takes_files`: `batch_plan.commit(..., files={rel: text})` makes one commit holding `plan.md` and
    that file.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_findings.py -q`
  Expected: FAIL; `batch_findings` does not exist.

- [x] **Step 3: Implement `batch_findings.py` and `commit`'s `files`, and write `review_testing.py`.**

- [x] **Step 4: Run them, and the batch plan tests.**
  Run: `python3 -m pytest tests/scripts/test_batch_findings.py tests/scripts/test_batch_plan.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/batch_findings.py scripts/batch_plan.py tests/scripts/review_testing.py tests/scripts/test_batch_findings.py`
  Expected: `14 xfailed`, no failures, passed = 1277 + the new tests; `size` silent; `check` clean.

- [x] **Step 6: Commit.**
  ```bash
  git add scripts/batch_findings.py scripts/batch_plan.py tests/scripts/review_testing.py tests/scripts/test_batch_findings.py CLAUDE.md
  git commit -m "batches: the pull request review's findings file and its record .shop/batches/<n>/review-<k>.md"
  ```

### Task 2: `work batch brief` — what the reviewer reads

Builds no requirement on its own. It is r3's and r4's mechanism; they leave `unbuilt:` with the agent in Task 5.

**Files:**
- Create: `scripts/batch_brief.py`, `tests/scripts/test_batch_brief.py`
- Modify:
  - `scripts/batch_git.py`: `remote_head(root, remote, branch) -> str | None`, moved from `batch_review._remote_head`,
    which now imports it.
  - `scripts/batch_review.py`: that import.
  - `scripts/batch_cli.py`: the `brief` parser and command.
  - `CLAUDE.md`: a row for `batch_brief.py`; the `batch_git.py` row names `remote_head`.

**Interfaces:**
- Consumes: Task 1; `batch_tasks.lines_commit`, `item_ids`; `backlog_lines.read`.
- Produces, in `batch_brief.py`:
  - `SIZE = 1000`; `CHECKS`, the four D8 strings.
  - `brief(root, name) -> tuple[Path, list[str]]`: the brief's path, and what it removed (D3).
  - `judgement(root) -> list[tuple[str, str]]`: `(rel, summary)` of each `tier: judgement` decision (D6).
  - `commits(root, rng) -> list[str]`: `<short sha> "<subject>" Item: b1 Finding: f1`, oldest first. A missing
    trailer is left out of its line.
  - `size(root, rng) -> tuple[int, int, int]`.
  - `head_of(brief_path) -> str`: the brief's `Head:` (for Task 3).
- The brief's first lines, exactly:
  ```
  # The review of batch-1's pull request

  Review: 1 (first; the pull request is unreviewed)
  Batch: batch-1
  Pull request: https://github.com/ex/ctx/pull/1
  Base: main
  Range: <forked_from>..<head>
  Head: <head>
  Tree: <trees>/batch-1
  Findings file: <trees>/batch-1-review-1/findings.md
  ```
  The sections follow in this order: `## Items` or `## Earlier findings`, `## Judgement decisions`, `## Rules`,
  `## Size`, `## Runs`, `## Commits`, `## Change`.
- `work batch brief <batch>` prints the brief's path, after one `removed an old findings.md` line when there was one.

- [x] **Step 1: Write the failing tests** (`test_batch_brief.py`, on `review_testing.published`, with
  `[review] checks = ["python3 -c \"print('ran')\""]` added to the fixture's `delivery.toml` and committed):
  - `test_the_first_brief_gives_the_batchs_range_and_no_other_commit` (Review Focus 3):
    - `Range:` is `<forked_from>..<batch-1 head>`.
    - The `## Commits` lines' shas are exactly `git rev-list --reverse forked_from..batch-1`, abbreviated.
    - No `work batch` subject of `main` appears.
    - `change.diff` holds `src/b1.txt` and no `.shop/`.
  - `test_the_first_brief_gives_every_requirement_of_its_items`: `## Items` names `b1 "Abandon"` with
    `.shop/backlog/b1.md` and `work-queue#r5: <ABANDON's text>`, and b2 with r6. A parked b2 is not listed.
  - `test_the_brief_lists_the_judgement_decisions`: the fixture's `spec/decisions/` gains two files, one
    `tier: judgement`, one `tier: check`. Only the first is listed, with its summary. With neither, the section says
    `none: no design-decision is tier: judgement`.
  - `test_the_brief_gives_the_runs_and_the_size`: the run's command, `Exit code: 0`, and `ran` in its output.
    `## Size` gives the files and counts and `limit 1000`. With `[review] size = 1` it says `over the limit`.
  - `test_brief_leaves_the_checkout_alone`: the base's HEAD and `git status --porcelain` are unchanged, and both files
    are under the worktrees directory.
  - `test_brief_refuses`, parametrised. Each is refused naming what it names, with nothing written:
    - a `building` batch: `work batch brief: batch-1 is building`;
    - a batch whose local `batch-1` has a commit the remote lacks: `work batch review`;
    - another branch checked out: the base.
  - `test_a_second_brief_starts_fresh`: with a `findings.md` written, a second `brief` prints `removed an old
    findings.md`, and the file is gone.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_brief.py -q`
  Expected: FAIL; `work batch` has no `brief`.

- [x] **Step 3: Implement `batch_brief.py`, `remote_head` and the parser.** The runs and the diff are made in the batch
  worktree. Run text is indented four spaces, so no line of it starts a brief field.

- [x] **Step 4: Run them and plan 4's review tests.**
  Run: `python3 -m pytest tests/scripts/test_batch_brief.py tests/scripts/test_batch_review.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The baselines** (Task 1's Step 5 command, with this task's files).
  Expected: `14 xfailed`, no failures; `size` silent; `check` clean.

- [x] **Step 6: Commit.**
  ```bash
  git add scripts/batch_brief.py scripts/batch_git.py scripts/batch_review.py scripts/batch_cli.py tests/scripts/test_batch_brief.py CLAUDE.md
  git commit -m "batches: work batch brief gives the pull request's reviewer the batch's own commits, its items' lines and the judgement decisions"
  ```

### Task 3: `work batch reviewed` — fix-now back to building, clean to awaiting-merge

Builds `pr-review#r5` and `r7`. It also adds the trace test (D19).

**Files:**
- Create: `scripts/batch_reviewed.py`, `tests/scripts/test_batch_reviewed.py`, `tests/scripts/test_pr_review_trace.py`
- Modify:
  - `scripts/batch_cli.py`: the `reviewed` parser and command; `status` and `as_json` show the reviews (D15).
  - `tests/scripts/stub_gh.py`: the docstring only (D20).
  - `spec/capabilities/pr-review.md`: `unbuilt: [r1, r2, r3, r4, r6, r8]`; `## Implementation, may change` names
    `work batch reviewed`, the record, `gh pr comment` and `gh pr ready`.
  - `CLAUDE.md`: a row for `batch_reviewed.py`; the `batch_cli.py` row names `brief`, `reviewed` and the reviews in
    `status`.

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces:
  - `batch_reviewed.reviewed(root, name) -> Review` (D12).
  - `batch_reviewed.said(root, review) -> str`:
    - `batch-1 review 1: 2 findings, 1 fix now -> building`, then one `  open f1 Important b1 "…" scripts/work:12:
      <title>` line for each open finding;
    - or `batch-1 review 2: 0 findings -> awaiting-merge; the pull request <url> is ready for the person's merge`.
- `test_pr_review_trace.py`: `PR_REVIEW_TESTS` (D19), with two tests:
  - `test_every_built_pr_review_line_has_its_test`;
  - `test_no_unbuilt_pr_review_line_has_a_test_yet`.

  Each lists the offending ids.

- [x] **Step 1: Write the failing tests** (`test_batch_reviewed.py`, on `published` and a brief):
  - `test_r5_a_fix_now_finding_sends_the_batch_back_to_building`, with `FIX_NOW_B1`:
    - exit 0, and the batch is `building`;
    - HEAD's commit holds exactly `.shop/batches/1/plan.md` and `.shop/batches/1/review-1.md`, with the subject
      `work batch reviewed: batch-1 review 1 -> building; open f1 b1 "Abandon"`;
    - the record parses with `result: fix-now`, its finding numbered `f1`, and `head` equal to the brief's `Head:`;
    - the gh calls end with `["pr", "comment", URL, "--body-file", <path>]` and hold no `pr ready`.
  - `test_r7_a_clean_review_awaits_the_merge`, with `CLEAN` (`None.`):
    - the batch is `awaiting-merge`, `result: clean`, and the last gh call is `["pr", "ready", URL]`;
    - after the test merges `batch-1` into `main` and writes the stand-in's `MERGED` state, `work batch merged
      batch-1` delivers b1 and b2. That is plan 4's path from `awaiting-merge`, now reached.
  - `test_reviewed_refuses_a_batch_that_is_building`, after the r5 review: a second `reviewed` is refused, naming
    `building`.
  - `test_reviewed_refuses_without_a_findings_file`: it names the brief's path and `pr-reviewer`.
  - `test_reviewed_refuses_a_malformed_findings_file` (Review Focus 1), parametrised over three of Task 1's cases run
    through the command. Each exits 1 naming `findings.md`; HEAD, the batch and the gh calls are unchanged.
  - `test_reviewed_refuses_a_stale_brief` (Review Focus 2): after the brief, a commit on `batch-1` in the batch
    worktree. Refused naming `work batch brief`, with nothing recorded.
  - `test_a_failing_gh_records_nothing` (Review Focus 5): parametrised over `STUB_GH_FAIL="pr comment"` (with
    `FIX_NOW_B1`) and `"pr ready"` (with `CLEAN`). Refused naming `gh pr …`; the batch is `in-review`, there is no
    `review-1.md`, and HEAD is unchanged. A rerun with the variable unset records.
  - `test_model_check_takes_the_review_record`: `model --root <repo> check` exits other than 2 and names no
    `review-1.md` line.
  - `test_status_shows_the_reviews`: `reviews: 1, last fix-now; open f1 b1 "Abandon"`, and `--json`'s `reviews` and
    `open`.

  And `test_pr_review_trace.py` as above.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_reviewed.py tests/scripts/test_pr_review_trace.py -q`
  Expected: FAIL. `reviewed` does not exist, and the trace test names r5 and r7 as tests of unbuilt ids.

- [x] **Step 3: Implement `batch_reviewed.py`, the parser and `status`.**

- [x] **Step 4: Run the reviewed tests.**
  Run: `python3 -m pytest tests/scripts/test_batch_reviewed.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: Take r5 and r7 out of `pr-review.md`'s `unbuilt:`, and run the trace test.**
  Run: `python3 -m pytest tests/scripts/test_pr_review_trace.py -q | tail -1`
  Expected: 2 passed.

- [x] **Step 6: Mutations,** each in a scratch edit, reverted, and recorded in the report:
  - `reviewed` setting `in-review` → `building` on a clean review fails `test_r7_…`;
  - skipping the `Head:` check fails `test_reviewed_refuses_a_stale_brief`;
  - leaving `r5` in `unbuilt:` fails the trace test.

- [x] **Step 7: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/tools size --limit 300`
  Expected: `14 xfailed`, no failures; `model check` and `logic` at baseline; `size` silent. Unbuilt ids: 21.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/batch_reviewed.py scripts/batch_cli.py tests/scripts/stub_gh.py tests/scripts/test_batch_reviewed.py \
    tests/scripts/test_pr_review_trace.py spec/capabilities/pr-review.md CLAUDE.md
  git commit -m "batches: work batch reviewed records the findings, a fix-now finding back to building, a clean review awaiting the merge (pr-review r5, r7)"
  ```

### Task 4: The fix loop — commits for a finding, the re-review

Builds no requirement on its own. It is r6's mechanism; r6 leaves `unbuilt:` with the agent in Task 5.

**Files:**
- Create: `scripts/batch_fix.py`, `tests/scripts/test_batch_fix_loop.py`
- Modify:
  - `scripts/batch_review.py`: after `checked`, `batch_fix.check(root, batch, mine, COMMAND)` when the batch has a
    recorded review.
  - `scripts/batch_brief.py`: the re-review form (D5).
  - `scripts/batch_tasks.py`: `resume` calls `batch_fix.trees`, and `resume_said` adds `batch_fix.said` (≤ 10 lines).
  - `scripts/batch_cli.py`: `review` prints D15's `next:` line before the URL.
  - `spec/capabilities/batches.md`: `## Implementation, may change`. Its bullet "a batch that has a pull request
    already is pushed only" now names D11's fix checks.
  - `CLAUDE.md`: a row for `batch_fix.py`; the `batch_review.py`, `batch_tasks.py` and `batch_brief.py` rows.

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces, in `batch_fix.py`:
  - `cited_findings(root, since, branch) -> list[tuple[str, str, set[str]]]`: `(short sha, subject, finding ids)`
    of each non-merge commit after `since`.
  - `for_finding(root, batch) -> dict[str, list[str]]`: each open finding's commits as `<short sha> "<subject>"`.
  - `check(root, batch, mine, command) -> None` (D11).
  - `trees(root, batch) -> list[tuple[Finding, Task, Path]]` (D14), re-making a lost worktree with `tree_for`.
  - `said(root, batch, found) -> list[str]`.

- [x] **Step 1: Write the failing tests** (`test_batch_fix_loop.py`). Each starts from `published`, a brief and
  `reviewed` with `FIX_NOW_B1`, so the batch is `building` with f1 open on b1:
  - `test_the_re_review_brief_gives_the_commits_for_each_finding` (Review Focus 3):
    - a commit on `batch-1-b1` with `Item: b1` and `Finding: f1` is made, then `review` and `brief`;
    - `review` exits 0, makes no `pr create`, and the batch is `in-review`;
    - the brief reads `Review: 2 (re-review of the fix)`, with `Range: <review 1's head>..<new head>`;
    - `## Earlier findings` holds f1 with that commit, and there is no `## Items`;
    - `## Commits` holds only the range's commits (the fix and its merge), and `change.diff` only the fix's file.
  - `test_review_refuses_a_fix_commit_that_cites_no_finding` (Review Focus 4): a second commit with `Item: b1` and no
    `Finding:`. Refused naming its `<sha> "<subject>"` and `Finding: f<m>`. `ls-remote` is unchanged, no gh call is
    made, and the batch is `building`.
  - `test_review_refuses_an_open_finding_with_no_commit` (Review Focus 4): no fix commit at all. Refused naming `f1 b1
    "Abandon"` and `or park b1`.
  - `test_a_parked_items_finding_needs_no_fix` (Review Focus 3, D22):
    - `park batch-1 b1 --question "<f1's title>"`, then `review`;
    - it publishes, and the take-out commit is in the next brief's `## Commits`;
    - that brief has no `## Earlier findings` entry, and a `CLEAN` `reviewed` gives `awaiting-merge`.
  - `test_reviewed_refuses_a_re_review_that_leaves_out_an_open_finding` (Review Focus 1): a re-review findings file
    with no `## Earlier findings`, and one naming `f9`. Each is refused naming f1 or f9.
  - `test_a_finding_not_fixed_stays_open`: `- f1: not fixed: still started` gives `building`, with f1 still in
    `open_findings`.
  - `test_resume_gives_the_worktree_for_each_open_finding`:
    - t1's worktree is removed;
    - `resume` gives it back on `batch-1-b1` with its commits;
    - it prints the D14 line naming `Finding: f1`;
    - t1 stays `done`, and nothing is committed.
  - `test_review_prints_the_next_step`: the line before the URL is D15's `next:` line.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_fix_loop.py -q`
  Expected: FAIL; `batch_fix` does not exist.

- [x] **Step 3: Implement `batch_fix.py` and the changes to `review`, `brief`, `resume` and `review`'s output.**

- [x] **Step 4: Run them and every batch test.**
  Run: `python3 -m pytest tests/scripts/test_batch_fix_loop.py tests/scripts/test_batch_*.py tests/scenarios/test_batches.py -q | tail -1`
  Expected: all pass. Plan 4's tests are unchanged, `test_a_second_review_pushes_only` included.

- [x] **Step 5: Mutations,** each reverted:
  - `check` skipped fails both Review Focus 4 tests;
  - the re-review range taken from `forked_from` fails the re-review brief test.

- [x] **Step 6: The baselines** (Task 3's Step 7 command). Expected: at baseline; unbuilt 21.

- [x] **Step 7: Commit.**
  ```bash
  git add scripts/batch_fix.py scripts/batch_review.py scripts/batch_brief.py scripts/batch_tasks.py scripts/batch_cli.py \
    tests/scripts/test_batch_fix_loop.py spec/capabilities/batches.md CLAUDE.md
  git commit -m "batches: the fix loop, a fix commit citing its finding, the re-review reading only what the fix changed"
  ```

### Task 5: The `pr-reviewer` agent

Builds `pr-review#r3`, `r4`, `r6` and `r8`.

**Files:**
- Create: `agents/pr-reviewer.md`, `tests/scripts/test_agent_pr_reviewer.py`
- Modify:
  - `tests/scripts/test_agents.py`: `REVIEWERS` gains `"pr-reviewer"`, and `test_r5_each_agent_names_its_model`
    covers it through that tuple (D18).
  - `README.md`: the agents list, and a row in "Agents: rules enforced by tools":
    `| \`pr-reviewer\` | Read, Glob, Grep, Write | opus | a batch's pull request review, from its brief: the batch's own commits, its items' lines, the judgement decisions; changes nothing |`.
  - `spec/capabilities/pr-review.md`: `unbuilt: [r1, r2]`; `## Implementation, may change` names the agent and its
    brief.

**The agent** (the implementer writes the prose; `bdd-branch-reviewer`'s sections are the model, with work-items read
as items):
- **Frontmatter:**
  - `name: pr-reviewer`
  - `description: The one adversarial review of a batch's pull request. Reads the brief work batch brief wrote: the
    batch's own commits and change, its items' requirement lines, the judgement decisions and the runs; grades and
    triages each finding and writes the findings file, changing nothing. Dispatched by the batch session
    (building-a-batch) with the brief's path; not for general use.`
  - `tools: Read, Glob, Grep, Write`
  - `model: opus`
- **Sections:**
  1. Your brief: its fields, as Task 2 gives them.
  2. What you read.
  3. What you change: only the findings file.
  4. What you look for: correctness against each requirement line; code no line asks for; tests removed or weakened;
     a `.feature` changed other than by `features generate` (the run of `features generate --check`); `CLAUDE.md`'s
     rules and module map; the judgement decisions; the size (D7).
  5. Triage: `bdd-branch-reviewer`'s fix now / observation / drop, with D24's re-review rule.
  6. The findings file: D9's format, the example verbatim.
  7. Your reply: the findings file's path and a summary of at most five lines.
- **Pinned sentences**, each held by a test:
  - r3: "Read every requirement the brief's `## Items` gives and every commit its `## Commits` lists, with their change
    in `change.diff`; read no other commit."
  - r3: "You have no shell: a commit the brief does not give is outside the batch, and you do not read it."
  - r4: "Read every design-decision the brief's `## Judgement decisions` lists, and check the change against each."
  - r6: "On a re-review, read every commit the brief lists under each finding of `## Earlier findings`, and write
    `fixed` or `not fixed: <why>` for each."
  - r8: "Give every finding a grade (`Critical`, `Important` or `Minor`) and a triage (`fix now`, `observation` or
    `drop`), and write them to the findings file the brief names."
  - D24: "On a re-review, a new finding is `fix now` only when the fix's own change is wrong."

- [x] **Step 1: Write the failing tests** (`test_agent_pr_reviewer.py`):
  - `test_r3_the_reviewer_reads_the_items_lines_and_only_the_batchs_commits`: both r3 sentences are there, and its
    tools are exactly `Read, Glob, Grep, Write` (no Bash).
  - `test_r4_the_reviewer_reads_every_judgement_decision`: the r4 sentence.
  - `test_r6_the_re_review_reads_every_commit_for_each_finding`: the r6 sentence and the D24 sentence.
  - `test_r8_each_finding_is_graded_and_written_to_the_findings_file`: the r8 sentence. The agent's format example (the
    first fenced block after its findings-file heading) parses with `batch_findings.parse_findings`, given items
    `{"b1"}`, `in_batch` `{"b1"}` and open `{"f1"}`, and each finding has a grade.
  - `test_the_reviewer_changes_nothing_and_starts_no_agent`: no `Edit`, `Agent`, `Task` or `Bash` in its tools; model
    `opus`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_agent_pr_reviewer.py -q`
  Expected: FAIL; the agent does not exist.

- [x] **Step 3: Write the agent; add it to `REVIEWERS` and README.**

- [x] **Step 4: Take r3, r4, r6, r8 out of `unbuilt:`, then run the agent, role-boundaries and trace tests.**
  Run: `python3 -m pytest tests/scripts/test_agent_pr_reviewer.py tests/scripts/test_agents.py tests/scripts/test_pr_review_trace.py -q | tail -1`
  Expected: all pass (r1 of role-boundaries still names only `initiative-round`).

- [x] **Step 5: The baselines.** Expected: at baseline, with subtests now 134 (`test_agents`' two rows for
  `pr-reviewer`); unbuilt 17.

- [x] **Step 6: Commit.**
  ```bash
  git add agents/pr-reviewer.md tests/scripts/test_agent_pr_reviewer.py tests/scripts/test_agents.py README.md spec/capabilities/pr-review.md
  git commit -m "agents: pr-reviewer, the one review of a batch's pull request, from its brief (pr-review r3, r4, r6, r8)"
  ```

### Task 6: The batch session reviews and fixes — `building-a-batch`

Builds `pr-review#r1` and `r2`. pr-review's `unbuilt:` becomes `[]`.

**Files:**
- Modify:
  - `skills/building-a-batch/SKILL.md`: a new step after "Publish", and its Red Flags.
  - `tests/scripts/test_skill_building_a_batch.py`: the tests below. `ORDER` gains `work batch brief` and `work batch
    reviewed` after `work batch review`.
  - `spec/capabilities/pr-review.md`: `unbuilt: []`; `## Implementation, may change` names the loop. A new `## Not
    yet` holds:
    - a cap on review rounds in code (D23);
    - findings posted as inline comments on the pull request's lines;
    - recurring findings counted (plan 7);
    - the `awaiting-merge` → `abandoned` transition (D16).

**The new step**, "Review and fix", says:
1. After `work batch review`, run `work batch brief <batch>`.
2. Dispatch one fresh `pr-reviewer` agent with the brief's path as its prompt, and no other context.
3. Run `work batch reviewed <batch>`.
4. On `-> awaiting-merge`, give the person the pull request's link. The person merges, then `work batch merged`.
5. On `-> building`, run `work batch resume <batch>`. It prints each open finding with its worktree. Dispatch one
   subagent for each item an open finding names, all at once, in that task's worktree. Give each the finding's text
   and this rule: fix only what the finding says, red first where a test can show it, and end each commit with
   `Item: b<j>` and `Finding: f<m>`.
6. Then run `work batch review` again, which pushes only, and go back to 1.
7. After the third review that leaves a finding open, park each item an open finding names, with the finding's title
   as its question, and review again (D23).

The step also says: no review is written when a task becomes `done`; the reviewer is dispatched only after `work
batch review`. Nothing in this step asks the person.

- [ ] **Step 1: Write the failing tests** (in `test_skill_building_a_batch.py`):
  - `test_r1_the_published_pull_request_is_reviewed`: the first step naming `pr-reviewer` comes after the step naming
    `work batch review`. In it, `work batch brief`, `pr-reviewer` and `work batch reviewed` appear in that order.
  - `test_r2_no_review_after_a_task`: no step naming `work batch done` names `pr-reviewer` or `work batch brief`.
  - `test_the_fix_loop_cites_item_and_finding`: the review step holds `Item: b`, `Finding: f`, `work batch resume`
    and `at once` (or `in parallel`).
  - `test_the_review_loop_asks_nothing`: the review step holds neither "ask the person" nor "wait for".
  - `test_the_process_runs_the_batch_commands_in_order` passes with the longer `ORDER`.

- [ ] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_skill_building_a_batch.py -q`
  Expected: FAIL. There is no review step, and the trace test fails once `test_r1_`/`test_r2_` exist while r1 and r2
  are unbuilt.

- [ ] **Step 3: Write the step and its Red Flags.** Red Flags gain these rows:
  - a reviewer dispatched after a task's `done`;
  - a reviewer given the session's context;
  - a fix commit with no `Finding:`;
  - a finding argued with instead of fixed or parked.

- [ ] **Step 4: Take r1 and r2 out of `unbuilt:`, then run the skill, command and trace tests.**
  Run: `python3 -m pytest tests/scripts/test_skill_building_a_batch.py tests/scripts/test_skill_shaping_items.py tests/scripts/test_pr_review_trace.py tests/scripts/test_agents.py -q | tail -1`
  Expected: all pass.

- [ ] **Step 5: Commit.**
  ```bash
  git add skills/building-a-batch/SKILL.md tests/scripts/test_skill_building_a_batch.py spec/capabilities/pr-review.md
  git commit -m "skills: building-a-batch reviews the published pull request with pr-reviewer and fixes each finding (pr-review r1, r2)"
  ```

### Task 7: Whole-plan verification and records

**Files:**
- Create: `.shop/records/2026-11-04-workflow-simplification/plan-5-implementation.md`
- Modify: `.shop/records/README.md` (a row for the report); this plan (every box ticked)

- [ ] **Step 1: Every requirement of the plan is built.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print('pr-review' in d, sorted(d.get('brainstorming', ())), sum(map(len,d.values())), u.problems(pathlib.Path('.')))"`
  Expected: `False ['r3'] 15 []`.

- [ ] **Step 2: The baselines, all at once.**
  Run: `python3 -m pytest -q | tail -2; python3 -m pytest -m timing -n 0 -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/features generate --check; python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound; python3 scripts/tools size --limit 300; python3 scripts/tools check $(git diff --name-only fbbd1466...HEAD -- '*.py')`
  Expected:
  - the suite: `14 xfailed`, no failures, passed = 1277 + the new script tests, and subtests 134;
  - the timing run: `1 passed`;
  - `model check`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`;
  - `model logic`: `11 findings: 6 L5, 5 L6`;
  - the lexicon: `401 terms, 0 problems`;
  - `generate --check`: exit 0;
  - `vocab --check`: `every step has one handler`;
  - `bindings --unbound`: `every binding names a scenario`;
  - `size`: silent;
  - `check`: clean.

- [ ] **Step 3: A smoke run of the review loop**, in bash, in a scratch repository under the job's tmp directory.
  Each `cp` and each `rm` is its own command (the person's rule). The test's own hand stands in for `pr-reviewer`.
  ```bash
  d=$(mktemp -d -p /home/vscode/.claude/jobs/7e9ba079/tmp) && git -C "$d" init -q -b main && git -C "$d" config user.name t && git -C "$d" config user.email t@example.com
  cp -r tests/scripts/fixtures/generate/repo/spec "$d/"
  rm "$d/spec/capabilities/legacy.md"
  sed -i 's#^id: bounded-context/.*#id: bounded-context/ex.com/prod/ctx#' "$d/spec/index.md"
  mkdir -p "$d/.shop" && printf '[batch]\ntests = "python3 -c pass"\n\n[review]\nchecks = ["python3 -c \\"print(1)\\""]\n' > "$d/.shop/delivery.toml"
  git -C "$d" add -A && git -C "$d" commit -qm init && git init -q --bare "$d.git" && git -C "$d" remote add origin "$d.git" && git -C "$d" push -q origin main
  export SHOPSYSTEM_WORK_GH="$PWD/tests/scripts/stub_gh.py" STUB_GH_CALLS="$d.calls" STUB_GH_STATE="$d.state"
  r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }
  W idea "Abandon a started initiative" && W shape b1 && W line b1 --into work-queue 'When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to `abandoned`.' && W ready b1
  W batch start && W batch resume batch-1
  ```
  Then, in t1's worktree, take `r5` out of `unbuilt:` and commit with `-m "build b1" -m "Item: b1"`. Then:
  ```bash
  W batch done batch-1 t1 && W batch review batch-1 && W batch brief batch-1
  ```
  Write the first review's `findings.md` (its path is the brief's `Findings file:`): a verdict and one `### Important
  fix now: …` finding with `- item: b1`. Then:
  ```bash
  W batch reviewed batch-1 && W batch status batch-1 && W batch resume batch-1
  ```
  In t1's worktree, commit a change with `-m "fix" -m "Item: b1" -m "Finding: f1"`. Then:
  ```bash
  W batch review batch-1 && W batch brief batch-1
  ```
  Write review 2's `findings.md`: a verdict, `None.` and `- f1: fixed`. Then:
  ```bash
  W batch reviewed batch-1 && W batch status batch-1
  git -C "$d" merge -q --no-ff batch-1 -m "merge the pull request" && printf '{"https://github.com/ex/ctx/pull/1": {"state": "MERGED", "mergeCommit": {"oid": "%s"}}}' "$(git -C "$d" rev-parse HEAD)" > "$d.state"
  W batch merged batch-1 && git -C "$d" log --format=%s -8 main && git -C "$d" status --porcelain
  ```
  Expected:
  - review 1 prints `-> building` with `open f1`, and resume prints the f1 line;
  - brief 2 reads `Review: 2 (re-review of the fix)` and lists only the fix and its merge;
  - review 2 prints `-> awaiting-merge`;
  - `$d.calls` holds two `pr comment` calls and one `pr ready`;
  - `merged` delivers b1;
  - `.shop/batches/1/` on `main` holds `review-1.md` and `review-2.md`;
  - `status --porcelain` is empty.

  Record the time of each `brief` and `reviewed`.

- [ ] **Step 4: Write the implementation report** at `plan-5-implementation.md`, in `plan-4-implementation.md`'s form
  (no frontmatter):
  - Final state: each Step 2 figure as measured, and the smoke run's times.
  - The commits: a table of each task's commit, what was done and its verification, the mutations included.
  - Deviations, each with its reason.
  - D1-D24, each kept or changed.
  - Open problems for plans 6-9. Among them:
    - the judgement decisions are empty until plan 6;
    - a real `pr-reviewer` run on a real batch has not been measured (plan 7);
    - plan 9 deletes `bdd-task-reviewer`, `bdd-branch-reviewer`, `supervise_review_read.py` and
      `supervise_branch_runs.py`, and updates the glossary's `review`;
    - a rerun after a failed `pr ready` posts a second comment.
  - Files.

- [ ] **Step 5: Index the records.** Add a row to `.shop/records/README.md` after the row for `plan-5-pr-review.md`:
  `| \`2026-11-04-workflow-simplification/plan-5-implementation.md\` | plan 5 executed: the pull request review built (\`work batch brief\`, \`reviewed\`, the fix loop's \`Finding:\` commits and re-review, the \`pr-reviewer\` agent, building-a-batch's review step), a fix-now finding back to \`building\` and a clean review to \`awaiting-merge\`, 8 requirements out of \`unbuilt:\` | report |`.
  Tick every box of this plan.

- [ ] **Step 6: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-5-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-5-pr-review.md
  git commit -m "records: plan 5 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-5-review.md`. It reads `<this plan's
  commit>..HEAD` on `workflow-simplification` against this plan's Review Focus.
