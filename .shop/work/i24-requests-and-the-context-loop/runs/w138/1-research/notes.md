# w138 research notes

Work-item w138 (`under: supervision`), accepts supervision#r72, r73, r74. Scenarios: features/supervision.feature lines 889-912.
Tools: `tools tests-of` and `untested` answer "no map" (no map made; not run: the whole suite). Every count below is `by search` or `refs`. `refs` gave 2 uses of `workqueue.add` (tests only) and 0 for `Reviews.branch_review` (method, not seen by refs).
Scripts used: `/home/vscode/shopsystem-bdd/scripts` (the brief's Scripts). Probes ran there, in scratch repositories, with `tests/scripts/stub_claude.py` as the stand-in claude.

## 1. Why each scenario is red today

Command for all three: `python3 -m pytest -q -p no:warnings <3 node ids>` (run). Each fails at its first Given, `StepDefinitionNotFoundError`; pytest-bdd stops there, so later steps are `read`.

- **r72** `test_a_formulated_capabilityproposal_gets_one_workitem_...` (features line 890). Undefined Given "i1's capability-proposal p1 is formulated, its adds naming thing#r1 and thing#r2, and its changes naming thing#r3 and other#r4" (line 892). Missing: a step that writes a formulated capability-proposal file (`.shop/work/i1/p1.md`, kind capability-proposal; the writer exists only in `tests/scenarios/conftest.py:145` `Workspace.proposal`, not reached by supervision steps). Read: Then "`work add` drafted two work-items ..." is undefined too. Code missing: no function in `scripts/supervise*.py` reads a capability-proposal or drafts (`supervise.py` `Run.run` 182-207 only pulls MOVABLE and runs `branch_review`).
- **r73** `test_a_workitem_drafted_for_a_formulated_...lists_under_its_retires_...` (line 898). Undefined Given "i1's capability-proposal p1 is formulated, its changes naming thing#r2" (line 900). Read: the tagged-scenario Given (line 901) exists (`supervision_given.py:229`); the Then "lists ... under its ## Retires" does not. Code missing: `scripts/workqueue.py:74` `add()` writes no `## Retires`; `scripts/work:95-100` `add` subparser has no `--retires`. No reader of scenario tags for drafting exists in supervise code.
- **r74** `test_a_kept_branch_reviews_findings_...` (line 907). Undefined Given "i1's work-items w1 is green, part of the capability-proposal p1, and w2 is withdrawn" (line 909): `supervision_given.py:54` items regex has no comma. Read: next Given "every worker gives DONE, and the branch reviewer's result lists two findings to fix now ..." (line 910) fails too: `supervision_review_steps.py:21` accepts only `ends` or `writes findings.md beside its brief`. Code missing: `scripts/supervise_review.py:64-66` `branch_review` copies the review's directory and discards its `result.json`; nothing reads `questions`, `findings` or the Findings triage; no drafting after the review.

## 2. What the system answers today

Probe file: `.shop/scratch/w138-1-research/probe_w138.py` and `probe_push.py` (run: `python3 -m pytest -q -s -n 0 <path>`, 6 passed). Scratch repositories under `.shop/scratch/w138-1-research/world/`. Stub plan: `default` DONE.

- **P1 r72 Givens and When, proposal formulated** (run). `work run i1` with `p1.md` `status: formulated`, `adds: [thing#r1, thing#r2]`, `changes: [thing#r3, other#r4]`: stdout empty, exit 0, and **a branch review ran** ("branch review 1 of i1" committed; the initiative had no work-items). No work-item drafted.
- **P1b `work add` today** (run): `work add i1 "Draft thing" --part-of capability-proposal/p1 --under thing --accepts thing#r1 --accepts thing#r2 --accepts thing#r3` -> exit 0, prints `w1`, writes `w1.md`. `... --retires "it used to wait"` -> exit 2, `unrecognized arguments: --retires`.
- **P2 nearest: proposal `drafted`** (run): `work run i1` -> exit 0, nothing drafted; also a branch review (same as P1).
- **P3 r73 Givens** (run): `features/thing.feature` with "it used to wait" (@deprecated @r2), "it used to answer" (@deprecated @r5), "it waits" (@r2); proposal formulated, changes thing#r2. `work run i1` -> exit 0, nothing drafted. `features deprecated --json` (run) gives, per deprecated scenario, `file`, `title`, `deprecated_for`, `replacement: null`: **no @r tag of the deprecated scenario**; the tag must come from the scenario's own tags (`scripts/features_gherkin.py:16` `Scenario`, read).
- **P4 r74 Givens and When** (run): w1 green, w2 withdrawn, reviewer result `status: DONE_WITH_CONCERNS`, `questions: ["fix now, w1, thing.py:3: ..."]`, `findings: findings.md` with a "Triage: fix now" line. `work run i1` -> stdout `w1 green` / `w2 withdrawn`, exit 0; no work-item drafted. The kept `runs/branch-review/1/result.json` holds the fix-now question; nothing reads it.
- **P5 nearest: reviewer ends at its turn limit, no result file** (run; see defect D1).
- **P6 push after `work add`** (run, `probe_push.py`): after `work add`, local `main` is `b23fe82`, the remote's `main` still `d2e497d` (`the repository`). `work add` commits and does not push.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py:Run.run 182-207 | pulls MOVABLE once, then branch review once, then prints and exits; exit 0 when all green/withdrawn | after r74 drafts fix items the initiative is not done; the run must go on or exit 1/3, not 0 | none by map; by search: tests/scenarios/test_supervision.py r9, r27, r50, r51 scenarios through `work run` | read, P4 |
| scripts/supervise.py:Run.run `all(...)` on items | true for zero work-items, so a branch review runs over an initiative with only a proposal | r72 creates the items; until then the review is vacuous (defect D2) | by search: supervision_review_steps.py (has items) | P1 |
| scripts/supervise_review.py:Reviews.branch_review 64-69 | keeps the review directory, discards its `result.json` | r74 must read the review's findings and its fix-now list | by search: supervision_review_steps.py, test_supervision.py r47-r49 | read, P4 |
| scripts/supervise_review.py:Reviews.unread 19-33 | commits not read by a kept review; `own()` excludes review and log commits only | a `work add` commit of a fix item after the review is unread, so the next run reviews again (see conflict C3) | by search: supervision_review_steps.py, test_supervision.py r50 | read |
| scripts/workqueue.py:add 74-97 | writes fixed frontmatter and body; no Retires; commit only the file, no push, no log line | r73 writes `## Retires`; r72/r74 draft through it | tests/scripts/test_work_item_ids.py:66,73 and tests/scripts/test_work_add_title.py:35 (positional call `add(repo,"i1",title,"p","c",["c#r1"])`) | refs (2 uses), read |
| scripts/work:95-100 `add` subparser | `--part-of --under --accepts` only | r73 needs `--retires` if drafting goes through the CLI | tests/scenarios/test_work_queue.py (`work add` scenarios, by search) | read, P1b |
| scripts/supervise_merge.py whole-suite expectation (r43) | counts failing scenarios of requirements another non-green, non-withdrawn item accepts as expected | a fix item drafted for a failing scenario makes other merges pass the suite | by search: supervision_tests_steps.py, supervision_faults_steps.py | read |

## 4. Tests the requirements make impossible to keep

No map (`tools tests-of: no map`), so by search. Searched tests for `formulated`, `Retires`, `fix now`, `findings`, `questions` in reviewer results, `add(`:
- tests/scripts/test_work_item_ids.py:66,73 and test_work_add_title.py:35 call `workqueue.add` positionally: **kept** if the new parameter is a keyword with a default. Verified by read.
- tests/scenarios/supervision_review_steps.py:17,21 write FINDINGS "Nothing found." and status DONE: no fix-now line, so no drafting; **kept**. Verified by read.
- tests/scenarios/test_supervision.py r27, r47-r51, r75-r76 (exit and reviewer counts with no findings): **kept**, unless drafting or a second review loop changes the count. Verified by read.
- No test uses a formulated proposal in supervision scenarios (`grep formulated` in tests/scenarios/supervision*: none). Design-model tests (v15f, design_model_check_*) read proposals only through `model`, unaffected.
- Result: none of the existing tests can no longer pass as written, by search. The exit-code tests for r9, r81, r82 pass unchanged because no proposal is present.

## 5. A step the work-item skips

`work add` (the path r72 and r74 use to draft) skips the push that every `work run` commit makes (r38) and the push check before it (r35):
- Effect only the push produces: the remote holds the commit. Shown by P6: remote `main` stays at the "the repository" commit after `work add`. Existing way (`Run.commit`, supervise.py:89-99) pushes after each commit (r38) and is `read` to verify `push` first (`Run.push` / `git_push --dry-run`, supervise_faults.py:26).
- Refusal only the verification gives: "cannot push the initiative branch to the remote" (`Reviews.branch_review` 41-45, and `verify_push` before workers). `work add` never refuses for it. Read.
- Log: `work add` writes no `log.jsonl` line; `Run.log` (supervise.py:83-87) writes start/end lines for each worker and stage (r8). Read.
- Uncommitted-`.shop/work/` refusal (r46, `Run.check` 77-81) is not applied when `work add` runs; a drafted file can be committed beside uncommitted work. Read.
- Lock: `Run.lock` (supervise.py:48) is not taken by `work add`. Read (drafting runs after the pool ends, so no overlap today).
- Refusals `work add` already has (all `read`, workqueue.py:74-96): initiative missing, empty or multi-line title, path exists, not a git work tree (`committed` 253-268).

## 6. Defects

D1 — a branch review that ends with no result is kept and exits 0.
Reproduction (run, probe `test_defect_reviewer_turn_limit_today`): initiative with w1 green, w2 withdrawn, a commit after base; stub reviewer `result: none`, `subtype: error_max_turns`, `num_turns: 26`. `work run i1` -> stdout `w1 green` / `w2 withdrawn`, exit 0. Kept directory `runs/branch-review/1/` holds `brief.md` and `session.json`, no `result.json`; "branch review 1 of i1" committed. Reading: r45 names a worker's session; the review is not a worker in `supervise_worker.py` (its `worker()` raises a Fault on this case, `branch_review` does not call it). Reading is mine; the spec's r27 says only "start a session".

D2 — a branch review runs over an initiative with no work-items.
Reproduction (run, probe `test_r72_formulated_proposal_today`, first `work run i1`): initiative with only `p1.md` (formulated) committed after base. Output empty, exit 0, and a branch review was started and kept ("branch review 1 of i1"). Cause: `Run.run` checks `all(...)` over an empty list (supervise.py:189, 205).

## 7. The file set

Production and test files the change must touch or keep passing, with the line counts `wc -l` gave (room = 300 - lines, CLAUDE.md's limit):

- scripts/supervise.py — 218 (room 82). Run.run: draft for formulated proposals after pull; findings after the review; loop or exit for new items. Found: read of Run.run.
- scripts/supervise_review.py — 77 (room 223). branch_review: keep and read the review's result, return its fix-now findings (r74). Found: read, P4.
- scripts/workqueue.py — 279 (room 21). add(): optional retires section (r73), keep positional signature. Only 21 lines free: a change over 21 lines breaks CLAUDE.md's limit; split add/highest into a module first. Found: refs, read.
- scripts/work — 147 (room 153). cmd_add and argparse: `--retires` only if drafting goes through the CLI. Found: read, P1b.
- scripts/supervise_draft.py — NEW. The concern of drafting formulated proposals and findings work-items: one module, one row in CLAUDE.md's module map. Found: the requirements.
- scripts/features_gherkin.py — 175 (room 125). Read-only: the scenario reader with tags (r73). Found: read.
- scripts/model_work.py — 219 (room 81), scripts/model_facts.py — 287 (room 13), scripts/model_parse.py — 271 (room 29). Read-only: `model` reads proposal frontmatter (`adds`/`changes`, model_work.py:153-155) and `workqueue._load_model` reuses it. Found: read; not edited.
- scripts/supervise_pool.py — 142 (room 158). On the path (pull, step); not edited unless drafted items are pulled in the same run. Found: read.
- tests/scenarios/supervision_proposal_steps.py — NEW. Givens and Thens of the three scenarios (formulated proposal, changes, Retires, findings). Found: scenario lines.
- tests/scenarios/test_supervision.py — 246 (room 54). One import line for the new step module (the file imports step modules with `*`, lines 25-32). Found: read.
- tests/scenarios/supervision_review_steps.py — 96 (room 204). Extend `reviewer_does` (line 21) for a reviewer whose result lists fix-now findings. Found: read.
- tests/scenarios/supervision_world.py — 173 (room 127). Proposal writer for supervision (or in the new step module). Found: read; conftest.py:145 has `Workspace.proposal`.
- tests/scenarios/supervision_given.py — 250 (room 50). Items regex line 54 has no comma; the new step module should take the r74 Given instead. Found: read.
- tests/scripts/test_work_item_ids.py — 77; tests/scripts/test_work_add_title.py — 50. Keep passing, no edit. Found: refs.
- tests/scenarios/test_work_queue.py — 287 (room 13). Keeps passing, no edit. Found: by search.
- tests/scripts/stub_claude.py — 258 (room 42). No edit: `fields` and `notes` carry the reviewer's findings. Found: read.
- agents/bdd-branch-reviewer.md — no edit proposed; its result (`questions` = fix-now lines, findings.md Triage) is the source for r74 (see C1). Found: read.

## Conflicts and readings for the plan

- C1 (r74): "findings to fix now" come from two places: findings.md's Triage (`fix now`, the agent file's findings shape) and the result's `questions` (agent file: "each fix-now or Critical finding"). The scenario says the result "lists" them "in its findings.md". Plan must pick one, or read both.
- C2 (r73): a work-item with no deprecated scenario for its requirement: write `## Retires` with "none", or omit it. The requirement says only "list ... each". Both readings.
- C3 (r74 vs r50): a fix item drafted after the review makes its commit unread, so the next run starts a second review; r50 is met only if the review reads the draft's commit. Plan must say which.
- C4 (r72): accepts = requirements named on that capability in `adds` and `changes` (removes excluded); `part_of: capability-proposal/p1`. Read: the scenario's "each part of p1" matches this.
- C5 (r73): the deprecated scenario's own @r tags are needed; `features deprecated --json` gives none (P3). Plan must read tags from the feature file.

## Gaps

- The three scenarios' later steps (after their first undefined Given) are `read`, not run.
- Scratch remains under `.shop/scratch/` (ignored by git: `git status --porcelain` clean).
