# Research of w216 (supervision r154-r157)

Method: `tools refs` ran (0 hits on `branch_review`: it does not follow `self.` calls, so call sites by search: supervise.py:231, 237). `tools tests-of` and `untested`: no coverage map ("no map: make one with tools map"), so every test list below is `by search`. `tools size --limit 300`: nothing over the limit. `git status --porcelain`: empty (the stage directory is ignored).

## 1. Why each scenario is red today

Command (`run`): `python3 -m pytest -q --work-item w216`: 10 failed, 176 passed, 1 skipped. All 10 failures are `StepDefinitionNotFoundError` on the first Given of each scenario, so no Then was reached (pytest-bdd stops at the first undefined step).

- r154 Outline, 7 examples (the whole suite; w1's scenarios; w2's check `python3 -c pass`; `tools check`; `tools size`; `features deprecated`; `features bindings`): undefined Given "i1's work-items w1 and w2 are green, w2 naming the check `python3 -c pass`".
- r155: undefined Given "i1's work-items w1 and w2 are green, w2 naming the check `python3 -c "import sys; print('too short'); sys.exit(1)"`".
- r156: undefined Given "every worker gives DONE, each implementer committing a change to src/<work-item>.py, and while w1's implementer works another session commits notes.txt ...".
- r157: undefined Given "i1's work-item w1 is under thing and w2 under other, spec/capabilities/thing.md's rests_on naming design-decision/a ...".

Missing step definitions (by search of tests/scenarios/supervision*: no text match for "naming the check", "was run at the initiative branch", "each planner writing", "brief names as files to read", "brief gives each commit"): every Given and Then of the four scenarios. Existing mechanisms to reuse: `plan["bdd-planner"] = {"notes": ...}` (supervision_review_steps.py:24), the `notes` plan key writes files beside the brief; the "another session commits" Given at supervision_given.py:167; `item_text` in supervision_world.py for `check:`.

Missing in the code behind them:
- scripts/supervise_review.py:branch_review (47-94): starts the reviewer with no run made first (r154); its brief (lines 64-71) holds only Head, Base, Worktree, Run directory (no runs r155, no commit list r156, no Read list r157).
- no code reads a work-item's `check:`: `check` appears in no scripts/supervise*.py (only model_work.py:188 for the model).
- no code runs `features deprecated`, `features bindings`, `tools check --base`, `tools size` for the branch (none in scripts/supervise*.py).
- scripts/supervise_merge.py:20-33 `tests()`: the suite command is `--work-item {work_item}`; no branch-level suite command.
- no code maps `design-decision/<slug>` to `spec/decisions/NNNN-<slug>.md` (rests_on is read only by model_facts.py:192; decision files listed by model_parse.py:270).
- commit attribution: none for the branch. Reusable: supervise_merge.py:136 logs each merged work-item's `commits` in log.jsonl (`event: merged`); supervise.py:176-183 `merged()` already gives a work-item reviewer its commit list and suite record.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_review.py:branch_review, brief lines 64-71 | writes a brief with Head, Base, Worktree only; the reviewer derives the rest | brief must give runs (r155), commits (r156), files to read (r157); runs happen first (r154) | by search: the tests/scenarios/supervision_*_steps modules that drive `work run` to a branch review (review, proposal, analysis, done, retire, faults, then_workers) | read |
| scripts/supervise_review.py:unread, line 25 | reads every line starting `Head:` of every kept brief | any run output or commit line in the brief that starts `Head:` is misread as a read head | by search: tests/scripts/test_supervise_review_due.py (unread, unread_mine); tests/scenarios/supervision_retire_steps.py:103 (`^Head: (\w+)$`) | read |
| agents/bdd-branch-reviewer.md, description line 3 and "What you run" lines 31-39 | reviewer runs the suite, each work-item's checks, `tools check`, `tools size`, `features` itself | r154 makes the runs before the review; r155 pins "without running any of them again" | none: tests/scripts/test_agents.py checks tools and model of this agent only | read |
| agents/bdd-branch-reviewer.md, "What the branch" line 25 | derives each work-item's commits from `work:` subjects and reads `git diff <Base> HEAD` (includes .shop/) | r156 gives each commit's work-item (or none) and the diff less .shop/ | none | read |
| agents/bdd-branch-reviewer.md, "Your brief" line 16 | expects a `Read:` list incl. plans, reports and findings | the brief today has no `Read:` line; r157 supplies it | none | read |
| scripts/supervise_merge.py:134 `merge --ff-only work/<name>` | no merge commit is made; the branch is deleted (r18, line 114) | r156 says "the merge of work/w1" gives w1: under ff no merge commit exists, so the attribution must come from log.jsonl `merged` commits (line 136) | not checked | read |
| scripts/supervise_merge.py:20-21 TESTS `suite` | suite command always names `--work-item {work_item}` | r154 needs the whole suite at head with no work-item | none for the branch | read |
| scripts/supervise_worker.py:39 TOOLS["review"] = READER | reviewer gets Bash for pytest, features, model, tools, git | no change required; if the reviewer stops running them its Bash may narrow | by search: none asserts this list | read |
| scripts/work_items.py:118-125 pytest_configure | `--whole-suite` refused to any worker but "the branch review" | work run's own suite run sets no WORKER, so unaffected | by search: tests/scripts/test_work_items_worker.py:32-33 | read |

## 3. Tests the requirements make impossible to keep

No map: each test list is `by search`. Searched: every test that names the branch review or reads its brief.

- tests/scenarios/supervision_review_steps.py:88-97 `verified_before_all`: counts exactly five `start` lines for w1 (a line with no work-item counts as w1) and the last one the branch review. Sound today. Constraint: a run's own log line with `event: start` and no work-item would break it. Not impossible, but the run's logging must avoid that form.
- tests/scenarios/supervision_retire_steps.py:101-115 (`^Head:` regex): sound; keep the `Head:` line exact and start no other brief line with `Head:`.
- tests/scripts/test_supervise_review_due.py: sound; uses unread and unread_mine only; keep the Head format.
- tests/scripts/test_agents.py: sound; asserts only the reviewer's frontmatter tools and model, which need not change.
- tests/scenarios/supervision_then_workers.py:268-279 and supervision_analysis_steps.py:23-28, 68-70: sound; order of reviewer start and brief mtime unchanged.
- tests/scripts/test_work_items_worker.py:32-33: sound.
- No test asserts the branch reviewer's brief beyond `Head:` (search of "branch reviewer's brief": only the undefined r154-r157 steps).

So: none that the requirements make impossible; one constraint above.

## 4. The file set

Production:
- scripts/supervise_review.py: branch_review runs the r154 runs first, writes r155-r157 into the brief. Read (above).
- scripts/supervise_branch_runs.py (new): the r154 runs and their record. Proposed new concern, per CLAUDE.md.
- scripts/supervise_review_read.py (new): commit attribution and diff less .shop/ (r156), files to read (r157), via decision ids. Proposed.
- scripts/supervise_merge.py: reuse suite_record (35-53) and merged commits (136); no change expected. Read.
- scripts/supervise.py: branch_review call sites 231, 237; no change expected. Read.
- agents/bdd-branch-reviewer.md: runs and attribution now given; reviewer must not run them again. Read; required so the reviewer does not contradict r155.
- CLAUDE.md: module-map row for each new module. Read.

Tests:
- tests/scenarios/supervision_branch_steps.py (new): Givens and Thens of r154-r157. Proposed new module, one concern.
- tests/scenarios/supervision_world.py: `item_text` needs a `check:` value. Read (173 lines).
- tests/scenarios/supervision_given.py: Givens for named checks, planner plan.md, concurrent notes.txt commit. Read (259 lines).
- tests/scripts/test_supervise_review_due.py and test_agents.py: unchanged, sound.
- optional new tests/scripts/ module for the new scripts (none drives them today).

Modules on the change path (lines; room under 300 per `tools size`):
- scripts/supervise.py: 293; room 7.
- scripts/supervise_review.py: 94; room 206.
- scripts/supervise_merge.py: 138; room 162.
- scripts/supervise_worker.py: 256; room 44.
- scripts/supervise_brief.py: 212; room 88 (reference only).
- scripts/supervise_draft.py: 122; room 178 (reference only).
- scripts/work_items.py: 164; room 136 (reference only).
- scripts/model_parse.py: 271; room 29 (decision-file listing, reference only).
- agents/bdd-branch-reviewer.md: 77 lines; no CLAUDE.md size rule (300 lines applies to Python).
- tests/scenarios/supervision_world.py: 173; room 127.
- tests/scenarios/supervision_given.py: 259; room 41.
- tests/scenarios/supervision_review_steps.py: 102; room 198 (reference only).

Conflicts for the planner (both readings given):
- C1 (r156, "the merge of work/w1"): reading A: attribute w1 to commits in log.jsonl `merged` (supervise_merge.py:136). Reading B: the range of w1's transition commits `work: w1 ... ` plus the commits between them. Both give the scenario's answer; A is the one the code can read after r18 deletes work/w1.
- C2 (r154, "the whole suite", the suite command names a work-item): reading A: run `python3 -m pytest -q -rfEx -p work_items --whole-suite` with no name; reading B: name one work-item. The scenario does not say which.
- C3 (r154, `tools check`): the agent asks for `--base <Base>`; the scenario line gives no base. Reading A: with --base; reading B: bare.
- C4 (r154 and the ledger, not verified here): the coordinator's ledger says ruff errors exist in design_model_check_requests.py and round scripts, so `tools check` may report red at head. Not run here (no tools run beyond the list). A red run must be given, not hidden (r155).
