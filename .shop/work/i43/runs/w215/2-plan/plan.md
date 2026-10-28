# Plan of w215: review r32, r33, r34

## 1. What goes green

Review is a `guarantees` capability (design-decision/workflow-capabilities-are-guarantees): it has no scenarios, and
`measure` checks it on real batches. The notes found no `review.feature` and no accepted scenario. The `@r32`–`@r34`
tags in other feature files carry other capabilities' ids. `python3 -m pytest -q --work-item w215` is green today
(176 passed, 1 skipped), and none of those tests is a review scenario. No deprecated scenario is retired.

- **review#r32**, the branch reviewer runs nothing. No scenario. It is not met today: the agent's description and its
  "What you run" section have it run the suite, each work-item's pytest, `tools check`, `tools size`,
  `features deprecated`/`bindings` and the dry-run test. The branch review is started with stage `review`, whose list
  (`READER`) allows pytest, the plugin's scripts and git.
- **review#r33**, a behaviour only a run would show becomes a finding with its test, marked not run. No scenario. The
  agent today writes probes in scratch and gives each observation a reproduction made of commands.
- **review#r34**, the randomized dry-run/real agreement test is verified from `work run`'s suite run. No scenario.
  The agent today runs that test itself.

## 2. Where the change lands

- `agents/bdd-branch-reviewer.md`: the description and the body. "What you run" becomes what `work run` gives. The
  branch, probes, reproductions, findings file and result are reworded to r32–r34. The `tools:` line is unchanged
  (decision 1).
- `scripts/supervise_worker.py`: a stage list of its own for the branch review, with Read, Glob and Grep and no Bash
  entry. `review` keeps `READER` for the work-item reviewer. The comment above `TOOLS` says so.
- `scripts/supervise_review.py`: `branch_review` starts its session under the branch review's own stage, the
  `branch-review` its log lines already carry (`STAGE`), not `review`. Nothing else here changes. The brief's runs,
  commits and files are w216's (decision 4).

Removed from the researcher's set, and why:
- `spec/decisions/0053-the-v3-agents.md` and `tests/scripts/test_agents.py`: the Bash tool comes off the agent
  through q24 (i44), not here (decision 1).
- `scripts/work_items.py` and `tests/scripts/test_work_items_worker.py`: the `--whole-suite` exemption is kept
  (decision 5).

On the path, not edited: `scripts/supervise.py`, `scripts/supervise_merge.py`, `tests/scripts/stub_claude.py`,
`tests/scenarios/supervision_*_steps.py`.

## 3. Decisions

1. **The agent's `tools:` line keeps Bash. Decision 0053's row and `test_agents.py` are not touched. r32 is held by
   the agent's body and by the stage's allowed list.** This is the ruling of 2026-10-28 in `.shop/work/i43/review.md`
   and the ledger, made by the coordinator under the person's delegation. Reading B was taken: the Bash removal is
   request q24 (i44), "r32 held by the brief until then". This settles the researcher's conflict C1.
2. **The branch review gets its own stage list, keyed `branch-review`, with Read, Glob and Grep and no Bash entry: no
   pytest, no plugin script, no git.** The work-item reviewer's `review` list stays `READER`. This rests on review#r32
   (it runs nothing) and supervision r14 (Bash only for what the stage runs and the git commands it needs, here none).
   The commits and the change it would have read with git come from `work run` (supervision r156, w216). A
   `.shop/delivery.toml` `[allowed_tools]` entry for `review` no longer applies to the branch review. Its own key is
   `branch-review`.
3. **The agent reads every run from the brief.** "What you run" is replaced by a section on what `work run` gives:
   each run of supervision r154, with its command, how it exited, its output and the commit it ran at (r155).
   - **The findings file.** `Suite` (its line and wall time, review#r7) and `Checks` (each work-item's check, the
     `tools check` headings, `tools size`, `features deprecated`, `features bindings`) are taken from those runs,
     naming the commit.
   - **A check `work run` did not give.** A check a work-item names with no run in the brief is listed under
     `Cannot verify` and fails the review (review#r6 with r32). "A check you did not run is not a check that passed"
     goes.
   - **The branch section.** It reads the commits, each with its work-item, and the change from the brief (r156), not
     from `git log`/`git diff`/`git show`.
   - **Writes and probes.** Its only writes are `findings.md` and the result (r32). No probes, no scratch directory.

   Rests on review#r32, #r7, #r6 and supervision r154–r156.
4. **w215 depends on w216** (supervision r154–r157). The body names the brief's runs, commits and files as w216's
   brief gives them. Until w216 lands there is nothing in the brief to read them from. This rests on review#r34 ("from
   the suite run `work run` gave it") and supervision r155. It settles the researcher's conflict C2 as reading A:
   w215 changes the agent's reading, and the plugin carries no case count of its own. `depends_on: [w216]` is in the
   result.
5. **The `--whole-suite` exemption in `scripts/work_items.py` stays.** The worker name "the branch review" is set for
   every session with no work-item (`supervise_worker.py`'s environment), so rounds and intake have it too. Removing it
   would change what those sessions may run, which no line of w215's asks. With decision 2, no branch reviewer can
   reach pytest anyway. This rests on review#r32 (scope) and red-green r1 as `work_items.py` cites it.
6. **r34 and r33 together.** Where the system has a dry-run and a real mode of one operation:
   - The reviewer finds the agreement test in the suite run's output and gives that it ran and how many cases it
     tried (r34).
   - Where the output does not show it ran or its case count, or the suite has no such test, that is a finding with
     the test that would show it, marked not run (r33). This replaces the old "Keep as a test:" probe.

   More generally, any behaviour that only a run would show is given as a finding with its test, marked not run, in
   place of a reproduction (r33). An observation's reproduction (r12) is drawn from the given runs' output or from
   what was read. Rests on review#r33, #r34, #r12.

## 4. Tests the decisions break

None. Verified:
- **`tests/scripts/test_agents.py`.** It reads the agents' tools and model lines. Those are unchanged (decision 1),
  and no test reads the branch reviewer's description or body (search of `tests/`).
- **The stub's allowed tools.** No branch-reviewer plan in the supervision step definitions
  (`supervision_review_steps.py`, `_analysis_`, `_proposal_`, `_done_`, `_faults_`) gives a `run` list.
  `supervision_faults_steps.py:159` uses `touch`, which the stub does without a worker tool (`stub_claude.py:23`,
  206). The only `--allowedTools` assertion is on the researcher's list (`supervision_then_workers.py:123-126`), and no
  worker gets a bare Write or Edit (`:162`). Decision 2's list has neither.
- **The log lines.** `supervision_review_steps.py:78-85` reads them, and they already carry `branch-review`.
  Decision 2 changes the stage passed to the session, not the log.
- **`tests/scripts/test_work_items_worker.py::test_the_branch_review_runs_the_whole_suite`**: kept and still true
  (decision 5).

## 5. Open cases

- What the reviewer does when the brief gives no suite run at all, or a run without its output: `Cannot verify` and a
  failed review (r6), or a stop (r28). The scenarios are silent.
- The grade of the r34/r33 finding when the agreement test's run or case count is missing.
- The exact field names of the runs, commits and files in the brief. They are w216's, and the body follows them.
- A consuming repository whose `.shop/delivery.toml` set `[allowed_tools].review` for the branch review: whether the
  new `branch-review` key is named anywhere a consumer reads (an upgrade note), or left to the module comment.
