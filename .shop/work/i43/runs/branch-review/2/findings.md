# Branch review 2 of i43 (re-review after the fix work-item w217)

**Verdict: DONE_WITH_CONCERNS.**

- Branch review 1's fix-now finding is fixed: w217's `9d61d97a` makes the r156 commit attribution take `work answer`, `work withdraw`, `work retry` and `work add` commits as their work-item's.
- No finding is triaged fix now, and nothing is Critical.
- Every work-item check and plugin command was run.
- The concern is the suite: one scenario failed in the one whole-suite run, so the suite is not green at HEAD. The failure is in a test fixture that was there before the branch, and the run's output shows a race with git's background maintenance (finding 1). Under the brief, I may not rerun the whole suite, so I cannot show it passing at HEAD. The person decides.

## Range and work-items

- Range: `ebbf1bea..fdf90439` (Base `ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22`, HEAD `fdf90439e529ae8110ccad5bb72dd1cc962518b4`), 68 commits.
- Since branch review 1 (`087967a1`), the new commits are:
  - `93c97155 work add: i43/w217 drafted`;
  - w217's transitions;
  - one work-item commit.
- **w215** (review r32-r34), green: `1b92df68`, between `c0e0ec4d` (ready -> claimed) and `c639266f` (claimed -> done).
- **w216** (supervision r154-r157), green:
  - `76403ad3`, between `f75e428d` and `aaa8712c`;
  - `449bed14`, between `eaa2ea69` and `8647f115`.
- **w217** (fix of branch review 1, finding 1; supervision r154-r157), green: `9d61d97a`, between `ba199fc1` (ready -> claimed) and `5d14aef6` (claimed -> done). It touches only `scripts/supervise_review_read.py` and `tests/scripts/test_supervise_review_read.py`, both in its `fileset:`.
- **Commits of no work-item:**
  - the proposals' apply and formulate rounds (`525db3cc`, `243800d0`, `2aa95f13`);
  - `work note`, a proposal's `work answer`, `work request`/`outcome`/`turn` (q24) and `work: start i44`;
  - the proposal and initiative transitions;
  - `087967a1 branch review 1 of i43`, which touches only `.shop/work/i43/`.

  All of these are the workflow's own commits. None is a stray change (branch review 1, finding 5, still holds).
- **How this review ran:** it was started by the installed plugin 0.28.1 (`Scripts:`), not by the branch's code. So its brief has no `Read:`, `## Runs` or `## Commits`, and the agent prompt is the pre-w215 one. I made the runs below myself, as that prompt says. HEAD's `agents/bdd-branch-reviewer.md` and review r32 say the branch reviewer runs nothing. They take effect only once the plugin is released.

## Suite

`Suite: 1032 passed, 1 failed at fdf90439 in 33.80 s` (1 skipped, 11 xfailed, 56 subtests passed). The 11 xfailed are w212's parked `test_requests.py` scenarios. The command was `python3 -m pytest -q -rfEx -p no:cacheprovider --work-item w217 --whole-suite`.

- **The failure:** `tests/scenarios/test_supervision.py::test_work_run_that_cannot_do_what_it_was_asked_exits_with_an_error_says_why_and_changes_nothing[... in a directory that is not a git repository ...]`.
  - It fails in the Given step: `tests/scenarios/supervision_given.py:72`, `shutil.rmtree(repo / ".git")`.
  - The error is `FileNotFoundError: 'maintenance.lock'` under `.git/objects`. See finding 1.
- **Parallel:** yes, `-n auto` (pytest.ini `addopts`; "bringing up nodes").
- **In-process:** no. The step definitions drive `work` as a subprocess.
- The run is under 60 s, so that is not a finding.

## Checks

- **Work-items' checks:** none of w215, w216 or w217 names a `check:` (a search of their files for `check:` found none). There is nothing to run.
- **Work-items' scenarios** (`python3 -m pytest -q --work-item <name>`, without `--whole-suite`):
  - w217: 189 passed, 1 skipped;
  - w216: 189 passed, 1 skipped;
  - w215: 179 passed, 1 skipped.

  The failed suite scenario is in none of these selections: `--collect-only -k cannot_do_what_it_was_asked` under `--work-item w217` collects no "not a git repository" case.
- **`tools check --base ebbf1bea`:**
  - **ruff:** 19 errors, the same 19 as branch review 1 (its finding 3), and none of them in w217's files:
    - 5 SIM115 in `.shop/work/i43/runs/review/2-apply/apply.py`;
    - 9 FURB167, 1 PLC0206 and 1 PIE810 in `tests/scenarios/supervision_branch_steps.py` (w216);
    - 1 I001 in `tests/scenarios/test_supervision.py:14` (w216);
    - 2 FURB167 in `tests/scripts/stub_claude.py:196-197`, there before the branch.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts".
- **`tools size --limit 300`:** no output. No file is over the limit.
- **`features deprecated`:** 11 deprecated scenarios. All of them were there before the branch, and none is i43's. The @r117 scenario in `design-model-check.feature` has a replacement, r121, that is green. That is i39's, as in branch review 1.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run/real agreement:** not applicable. The plugin has no operation with a dry-run and a real mode of its own.

## Removed and weakened tests

None. I searched the diff `ebbf1bea..HEAD -- tests` for:
- deleted `def test_` or step functions;
- dropped parametrize or Examples rows;
- removed or loosened `assert`s;
- added `skip` or `xfail`.

w217's only removed test line is the module docstring's second line, which it widened. It adds two tests and an `owners` helper. `test_a_proposals_transition_commit_belongs_to_no_work_item` is unchanged.

Branch review 1's three widened helpers (`supervision_given.py:66`, `supervision_world.py:90`, `stub_claude.py:220`) are unchanged since then.

## Allowances

- **w215**, **w216** (both reports) and **w217:** `## Tests changed under an allowance` is "none".
- No existing test's `assert`, expected value or parametrize case changed. Nothing needed an allowance.

## Cannot verify

- **That the suite's one failure passes at HEAD.** The output shows its cause (finding 1). Under the brief, the whole-suite run is made once, and the failing scenario is in no work-item's selection, so I did not run it again.
  - Test that would show it, not run: `python3 -m pytest -q tests/scenarios/test_supervision.py -k "not_a_git_repository"`, repeated.
- **The real-range attribution probe.** I wrote a probe of `ReviewRead.commits_text(ebbf1bea, fdf90439)` with i43's three work-items, but running a script from the scratch directory needed an approval this session cannot get. I deleted it unrun. Instead I checked by reading:
  - this range's subjects from `git log --grep='^work \(answer\|add\|withdraw\|retry\): '`;
  - the new regex `supervise_review_read.py:11` against each.

  The results (see What I verified under finding 2) agree with w217's unit tests, which passed in the suite and in `--work-item w217`.
- **Carried from branch review 1, unchanged:** that a `claude -p` session under `--allowedTools Read,Glob,Grep` (the `branch-review` key, `supervise_worker.py:42`) with `acceptEdits` can write `findings.md` and `result.json` and is refused every Bash call. No branch review has run under the new list. This one ran under 0.28.1.
  - Test that would show it, not run: a scenario asserting that the branch reviewer's `--allowedTools` holds no `Bash`.

## Findings

### 1. Minor · none (before the branch) · observation: a race between the "not a git repository" Given step and git's background maintenance

- **Where:** `tests/scenarios/supervision_given.py:71-72`: `commit_all(repo, "work-items")`, then `shutil.rmtree(repo / ".git")`. These lines are unchanged since Base (`git show ebbf1bea:tests/scenarios/supervision_given.py` lines 70-72).
- **What is wrong:** `git commit` can start `git maintenance run --auto` in the background. That removes `.git/objects/maintenance.lock` while `rmtree` is walking the directory, so `rmtree` raises `FileNotFoundError`, and the scenario fails before its When step.
- **Why it matters:** the suite is red at random, and `work run`'s merge gate (the whole suite) can fail a work-item for nothing.
- **Fix:** in the test repositories, set `git config maintenance.auto false` and `gc.auto 0` (in `supervision_world`'s repo init). Or use `shutil.rmtree(repo / ".git", ignore_errors=True)` followed by an assertion that `.git` is gone.
- **Reproduction:** the suite run above, `[gw10] ... supervision_given.py:72: in work_items ... FileNotFoundError: [Errno 2] No such file or directory: 'maintenance.lock'`.

### 2. Minor · w217 · drop: `work add: <initiative>/<name>` does not check the initiative

- **Where:** `scripts/supervise_review_read.py:11`, where group 2 takes `<name>` from any initiative.
- **What is wrong:** a `work add: i99/w1 drafted` commit would be given to this initiative's `w1`.
- **Why it hardly matters:** work-item numbers are global across initiatives, so nothing makes this input today. w217's plan, its report and its review 4 name it as an open case.
- **What I verified:**
  - **Risk:** the regex does not match what `work` writes. I checked `workqueue.py:105` (add), `:217` (retry) and `:242` (withdraw), and `workqueue_answer.py:74` (a proposal's answer, no transition) and `:76` (a work-item's answer, with transition). Each matches or does not match as r156 wants.
  - This range's subjects:
    - the ten `work answer: review|supervision` commits fail both alternatives and give `none`;
    - `afc6f024`, `667ad9d2` and `93c97155` (`work add: i43/w21x drafted`) give w215, w216 and w217;
    - `2faf85d3` (`work answer: w216 awaiting-answer -> ready`) gives w216.
  - `name = found and (...)` is `None` with no match, and `None in names` is False, so such a commit gives `none`.

### 3-9. Branch review 1's findings 2-9, unchanged at HEAD: observations or drops, as triaged there

w217 fixed only finding 1, and the plan's decision 5 says so. On a re-review, none of the rest is data left invalid, a fault on input, or a write where a refusal belongs. Each was checked again at HEAD:

- **Finding 2 (w216), Minor, observation:** `scripts/supervise_review.py:71` still says "You start in your worktree: run every command from there", against review r32.
- **Finding 3 (w216), Minor, observation:** the same 19 ruff errors (see Checks).
- **Finding 4 (w215), Minor, observation:** `agents/bdd-branch-reviewer.md:25` still says "A commit that belongs to no work-item is a finding", with no exception for the workflow's own commits. In this range that covers about 50 of the 68 commits.
  - Also: the agent's frontmatter `tools: Read, Glob, Grep, Bash, Write` (line 4) still lists Bash, while its body and r32 say it runs nothing. The `--allowedTools` stage list is the boundary, so this is only inconsistent text.
- **Finding 6 (w215), Minor, observation:** a consumer's `[allowed_tools].review` no longer reaches the branch review (`supervise_worker.py:42`), and no note says so.
- **Finding 7 (w216), Minor, observation:** `Head:` and `Ran at:` are still read from the checkout root (`supervise_review.py:67`), not from the review's worktree.
- **Finding 8 (w216), Minor, observation:** the r154 runs still have no timeout (`supervise_branch_runs.py:40`), and their output and the diff go into the brief unbounded.
- **Findings 5 and 9:** drops, as before.

No code no line asks for: w217's change serves r156 only. Its observable behaviour is the owner column of the brief's `## Commits`.

## Shape

- **Size limit (300):** met.
  - `supervise_review_read.py`: 65 lines;
  - `test_supervise_review_read.py`: 55 lines;
  - the branch's other files are as in branch review 1.
- **Module map:** `scripts/supervise_review_read.py` row (CLAUDE.md:33), "its commits with their work-items": w217's change is that concern. Met.
- **`tests/scripts/`, tests of scripts no scenario drives:** w217's cases are not in the r156 scenario (its step builds only `work:` subjects, `supervision_branch_steps.py:144`), so a unit test is where they belong. Met.
- **Carried from branch review 1:** `supervise_review_read.py:8` imports `indented` from `supervise_branch_runs`.
  - The check that would show it complete: no `from supervise_branch_runs` in `supervise_review_read.py`.
- **Unreached code or steps:** vulture is clean. w217 adds no step.

## Coupling

- **git:** the attribution now reads four more of `work`'s own subject formats (`workqueue.py:105,217,242`, `workqueue_answer.py:76`). This is a coupling inside the repository, to text no contract publishes. If a subject format changes, the attribution falls back to `none` without saying so.
  - `measure_build.py:81` reads only `work: <name> ... -> ...` and still misses these subjects.
  - What would make it stable: one module exporting the subject formats, used by `workqueue*.py`, `supervise_review_read.py` and `measure_build.py`, with a test that checks the round trip of each.
- **pytest-xdist, the claude CLI, ruff, vulture, import-linter:** as in branch review 1. Nothing new.

## Observations

- **Finding 1:** suite run at fdf90439. 1 failed, `supervision_given.py:72` `rmtree` → `FileNotFoundError: 'maintenance.lock'`.
- **Finding 2:** reasoned from `supervise_review_read.py:11`. No `work add: <other initiative>/…` subject exists in `.shop/work/`'s numbering.
- **Finding 3 (BR1 #2):** a search for "run every command" in `scripts/supervise_review.py` gives line 71.
- **Finding 4 (BR1 #3):** `tools check --base ebbf1bea` gives 19 ruff errors.
- **Finding 5 (BR1 #4):** `agents/bdd-branch-reviewer.md:25` and line 4 (`tools: ... Bash ...`).
- **Finding 6 (BR1 #7):** `supervise_review.py:67` has `git(self.root, "rev-parse", "HEAD")`.
- **Finding 7 (BR1 #8):** `supervise_branch_runs.py:40` has `subprocess.run(...)` with no `timeout`.
