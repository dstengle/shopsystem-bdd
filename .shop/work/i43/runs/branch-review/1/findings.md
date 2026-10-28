# Branch review of i43

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now: the r156 commit attribution gives `none` for a
transition of a work-item made by `work answer` (and by `work withdraw`, `work retry` and `work add`). Nothing is Critical,
and every check was run. The suite is green.

## Range and work-items

- Range: `ebbf1bea..dfeaa30f` (Base `ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22`, HEAD `dfeaa30f3bb37651094585ce43250410745461f9`), 59 commits.
- **w215** (review r32-r34), green: `1b92df68`, between `c0e0ec4d` (ready -> claimed) and `c639266f` (claimed -> done).
- **w216** (supervision r154-r157), green, two implement rounds:
  - `76403ad3`, between `f75e428d` and `aaa8712c`;
  - `449bed14` (the fix of its review 4 finding 1), between `eaa2ea69` and `8647f115`.
- **Commits of no work-item:**
  - the capability-proposals' rounds: `525db3cc` (apply: spec), `243800d0` and `2aa95f13` (formulate: `features/supervision.feature`);
  - `work note`, `work answer`, `work request/outcome/turn` (q24) and `work: start i44`;
  - the proposals' and the initiative's `work:` transitions.

  None of them is a stray change. See finding 5.
- This review was started by the installed plugin 0.28.1 (`Scripts:`), not by the branch's code. So its brief has no
  `Read:`, `## Runs` or `## Commits`, and the agent prompt it ran under is the pre-w215 one. I made the runs below myself,
  as that prompt says.

## Suite

`Suite: 1031 passed, 0 failed at dfeaa30f in 34.23 s` (1 skipped, 11 xfailed, all of them w212's parked `test_requests.py`
scenarios; 56 subtests passed). The command was `python3 -m pytest -q -rfEx --work-item w215 --whole-suite`, the form
`work run`'s suite command takes.

- **Parallel:** yes, `-n auto` (pytest.ini `addopts`).
- **In-process:** no. The step definitions drive `work` as a subprocess (`tests/scenarios/test_supervision.py:79`).
- Under 60 s, so not a finding.

## Checks

- **Work-items' checks:** neither w215 nor w216 names a `check:` in its frontmatter. There is none to run.
- **`tools check --base ebbf1bea`:**
  - **ruff:** 19 errors (finding 3):
    - 5 SIM115 in `.shop/work/i43/runs/review/2-apply/apply.py` (the apply round's helper script, committed with the round);
    - 9 FURB167, 1 PLC0206 and 1 PIE810 in `tests/scenarios/supervision_branch_steps.py` (w216);
    - 1 I001 in `tests/scenarios/test_supervision.py` (w216's import is out of order);
    - 2 FURB167 in `tests/scripts/stub_claude.py:196-197`, there before the branch.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- **`tools size --limit 300`** (CLAUDE.md's limit): no output, so no file is over the limit. The branch's files:
  - `supervision_branch_steps.py` 183 lines;
  - `supervise_review.py` 100;
  - `supervise_review_read.py` 66;
  - `supervise_branch_runs.py` 51.
- **`features deprecated`:** 11 deprecated scenarios, all there before the branch. None of them is i43's, and none is
  touched by the branch. One has a replacement that is green: `design-model-check.feature` "an id of a kind kept in
  .shop/work/ with another context's path is v18" (@r117), replaced by r121, which is green (i39 ledger). That is i39's,
  not i43's.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run/real agreement:** not applicable. The plugin has no operation with a dry-run and a real mode of its own.
  The only `--dry-run` is `git push --dry-run` in the push check (`supervise_review.py:55`).
- **w215's and w216's scenarios:** taken from the suite run, which has no failure. I did not run them apart from it.

## Removed and weakened tests

None. I searched the diff `ebbf1bea..HEAD -- tests` for:
- deleted `def test_` or step functions;
- dropped parametrize or Examples rows;
- removed or loosened `assert`s;
- added `skip` or `xfail`.

Three helpers changed. Each only widens, and its default is unchanged:
- `supervision_given.py:66`: `under` from `context["unders"]`;
- `supervision_world.py:90`: optional `check=`;
- `stub_claude.py:220`: `elsewhere` filtered by an optional `work_item`.

## Allowances

- **w215:** `## Tests changed under an allowance` is "none", and its commit changes no test.
- **w216** (both reports): "none". Its test changes are new step definitions, a new test and the three helpers above, and none of them changes an `assert`, an expected value or a parametrize case. Nothing needed an allowance.

## Cannot verify

- That a `claude -p` session under `--allowedTools Read,Glob,Grep` with `acceptEdits` (the new `branch-review` list) can
  still write `findings.md` and `result.json`, and is refused every Bash call. The `plan` and `answer` stages already
  run this way, and this session's own refusals of commands outside its list agree. But no branch review has run under
  the new list. This is not a check a work-item names.
  - Test that would show it: a scenario asserting that the branch reviewer's `--allowedTools` holds no `Bash`. Not run.

## Findings

### 1. Important · w216 · fix now: transitions made by `work answer`, `work withdraw`, `work retry` and `work add` are given as `none` (r156)

- **Where:** `scripts/supervise_review_read.py:11` (`TRANSITION = re.compile(r"^work: (\S+) \S+ -> \S+$")`) and `:42`.
- **What is wrong:** r156 asks for each commit with the work-item it belongs to, and its scenario names "each commit of a
  transition of w1". `work answer` commits a work-item's transition as `work answer: <name> awaiting-answer -> <status>`
  (`workqueue_answer.py:76`). `work withdraw` and `work retry` use `work withdraw: <name> <s> -> withdrawn` and
  `work retry: <name> failed -> <s>` (`workqueue.py:217,242`). A work-item's creation is `work add: <i>/<name> drafted`
  (`workqueue.py:105`). The regex takes only `work: `, so the brief gives all of these as `none`.
- **Reproduction (probe in scratch, since deleted):** `ReviewRead.commits_text(ebbf1bea, dfeaa30f)` over i43's own
  log gives:
  - `2faf85d3… none work answer: w216 awaiting-answer -> ready`;
  - `afc6f024… none work add: i43/w215 drafted`;
  - `667ad9d2… none work add: i43/w216 drafted`;
  - and `w215` / `w216` for every `work: wNNN …` transition and for the three merged commits (`1b92df68`, `76403ad3`,
    `449bed14`).
- **Why it matters:** this is a wrong answer in the brief. The branch reviewer is told to take attribution from the
  brief (agent line 25), and that a commit that belongs to no work-item is a finding. So every initiative with an
  answered, withdrawn or retried work-item gets a false finding, and the work-item's history is shown cut.
- **Fix:**
  - Take the name from any of work's transition subjects, kept only when it is one of the initiative's work-items:
    `^work(?: answer| withdraw| retry)?: (\S+) \S+ -> \S+$`, and `^work add: [^/]+/(\S+) drafted$`.
  - Add a case to `tests/scripts/test_supervise_review_read.py` or a row to the r156 scenario: a
    `work answer: w1 awaiting-answer -> ready` commit expecting `w1`.
  - `measure_build.py:81` reads transitions by a similar subject pattern. One shared pattern would keep the two
    together.

### 2. Minor · w216 · observation: the brief still tells the branch reviewer to run every command

- **Where:** `scripts/supervise_review.py:71-72`: "You start in your worktree: run every command from there and never change directory."
- **What is wrong:** this contradicts review r32 ("shall run nothing") and the agent body (line 29). w216 rewrote this
  brief and kept the sentence. It was raised as w215 review finding 1, with w216 named to drop it.
- **Why it matters:** the stage list has no Bash, so nothing is run. The text is only inconsistent.
- **Fix:** replace it with "Read what this brief gives; write only the findings and the result file."
- **Reproduction:** a search for "run every command" in `scripts/supervise_review.py` finds line 71.

### 3. Minor · w216 · observation: new ruff errors

- **Where:** `tests/scenarios/supervision_branch_steps.py:31,37,88,89,106,129,137` (FURB167), `:147` (PLC0206) and
  `:148` (PIE810); `tests/scenarios/test_supervision.py:14` (I001: the `supervision_branch_steps` import comes before
  `supervision_answers_steps`).
- **Why it matters:** `tools check` is red at the head. Each later branch review will show these.
- **Fix:** `ruff check --fix` on the two files, then `.items()` at line 147 and a tuple `startswith` at line 148.
- **Reproduction:** `tools check --base ebbf1bea` above.
- Also: `.shop/work/i43/runs/review/2-apply/apply.py` (5 × SIM115) belongs to no work-item. It is the apply round's
  helper, committed in its run directory. It is noted here, and it is a drop for this initiative. The i39 ledger records
  the same for round helper scripts.

### 4. Minor · w215 · observation: the agent no longer excepts `work run`'s own commits from "a commit that belongs to no work-item is a finding"

- **Where:** `agents/bdd-branch-reviewer.md:25`.
- **What is wrong:** the old text read the commits "less the `work:` commits of `work run` itself". The new text drops
  that and keeps "A commit that belongs to no work-item is a finding". The brief gives `none` for every `work note`,
  `work answer: <proposal>`, request, round and proposal-transition commit. The probe of finding 1 gives 41 of this
  branch's 59 commits as `none`, 3 of them finding 1's.
- **Why it matters:** every branch review is told to raise dozens of findings for the workflow's own commits. That
  noise hides a real stray commit.
- **Fix:** restore the exception in the agent body: "less the commits of `work`, `work run` and the capability-proposals'
  rounds". Or have r156's brief mark those commits as the workflow's (a line first, through integrating-a-proposal).
- **Reproduction:** `git show ebbf1bea:agents/bdd-branch-reviewer.md` line 25 against HEAD's.

### 5. Minor · none · drop: the commits of no work-item are the capability-proposals' rounds and work's own

- `525db3cc` (spec), `243800d0` and `2aa95f13` (`features/supervision.feature`, +51 lines, scenarios @r154-@r157 only
  added) are the apply and formulate rounds of `i43-review` and `i43-supervision`. That is the route the workflow gives
  for spec and scenarios. No work-item's commit touches `features/` (`git log --stat ebbf1bea..HEAD -- features`), so
  r10 is not met by any work-item.
- `243800d0`'s subject says "(i43 review proposal)" while it formulates supervision's lines. The ledger says the review
  proposal's round 3 wrote them.

### 6. Minor · w215 · observation: a consumer's `[allowed_tools].review` no longer reaches the branch review

- **Where:** `scripts/supervise_worker.py:42` and `supervise_review.py:81`. The branch review's stage key is now `branch-review`.
- **What is wrong:** a consuming repository whose `.shop/delivery.toml` widened `[allowed_tools].review` for the branch
  review loses that widening silently. No upgrade note or `migrate` step names the new key.
- **Why it matters:** this follows r32, which says the branch reviewer runs nothing. But the change is not announced.
  This repository has no `.shop/delivery.toml`.
- **Fix:** name the `branch-review` key in the release notes or a `migrate status` note.

### 7. Minor · w216 · observation: `Ran at:` and `Head:` are read from the checkout, not from the review's worktree

- **Where:** `scripts/supervise_review.py:62,67`.
- **What is wrong:** the worktree is made at the checkout's HEAD at line 62. `head` is read from `self.root` at line 67,
  outside `self.lock`. Another initiative's `Run` that commits in between makes `Ran at:` name a commit the runs did not
  run at (r155). This was w216 review 4 finding 3, and it is unchanged.
- **Fix:** `git(tree, "rev-parse", "HEAD")`.
- **Test that would show it** (not run): commit on main from the stub's `elsewhere` during the worktree's creation, then
  assert that `Ran at:` equals the worktree's HEAD.

### 8. Minor · w216 · observation: the r154 runs have no timeout, and their whole output and the whole diff go into the brief

- **Where:** `scripts/supervise_branch_runs.py:40`, where `subprocess.run` has no timeout, and `:51` and
  `supervise_review_read.py:44`, which give the output and the diff unbounded.
- **What is wrong:**
  - A hung check holds `work run` before the review, with no fault.
  - On a large initiative, the brief can pass what the reviewer's Read takes in one call. This initiative's diff less
    `.shop/` is 46 KB.
- **Fix:** a timeout line for the runs, and a bound on the brief, each written as a line first. No line asks for either
  today.
- **Test that would show it** (not run): an item whose `check:` is `python3 -c "import time; time.sleep(3600)"`.

### 9. Minor · w216 · drop: a `check:` is split by shlex and run without a shell; design-decisions are given by id, not path

- A check written with `&&` or a pipe is run as one wrong argument list. `spec/decisions/` paths are left to the reader.
  Both are open cases the plan names. They are mechanisms, not contradictions of r154 or r157.

## Shape

- **Size limit (300):** met. No file is over it (`tools size`).
- **Module map:**
  - `scripts/supervise_branch_runs.py` and `scripts/supervise_review_read.py` each have their own row (CLAUDE.md:32-33):
    met.
  - `scripts/supervise_review.py` and `scripts/supervise_worker.py` fall under the `supervise*.py` row: met.
  - `supervise_review_read.py:8` imports `indented` from `supervise_branch_runs`. That couples two sibling parts of
    `Run`. A small helper module, or `indented` kept in `supervise_review.py`, would remove it. The check that shows
    it complete: no `from supervise_branch_runs` in `supervise_review_read.py`.
- **`tests/scenarios/`, one `<capability>_*_steps.py` a concern:** `supervision_branch_steps.py`: met.
- **`tests/scripts/`, tests no scenario drives:** `test_supervise_review_read.py` covers the proposal-transition case,
  which no scenario has: met.
- **File sets:** w216 changed `tests/scripts/stub_claude.py`, `tests/scenarios/supervision_given.py` and
  `tests/scripts/test_supervise_review_read.py` outside its `fileset:`. Its report names the first two under "Outside
  the file set", and its review 6 named the third. Minor.
- **Unreached code or steps:** vulture is clean. Every new step is matched by the five new scenarios (all pass in the
  suite).

## Coupling

- **git:**
  - the `:(exclude).shop` pathspec magic (`supervise_review_read.py:44`) and `log --format=%H %s`: both published, so
    stable.
  - the attribution's reading of commit subjects is a coupling to `work`'s own message formats, inside this repository.
    Finding 1 is that coupling breaking. One shared pattern module would hold it.
- **pytest / pytest-xdist:** the suite is run as `-n auto` only when `xdist` imports (`supervise_merge.py:30`). The
  reviewer reads pytest's last summary line, a published format.
- **claude CLI:** the branch review relies on `--allowedTools` without Bash under `--permission-mode acceptEdits`
  refusing Bash in `-p`, and still allowing writes in the worktree. That is the CLI's published permission model, and
  `plan` and `answer` rely on it already. A change to acceptEdits' scope would break all three. A scenario asserting
  the branch reviewer's `--allowedTools` (see Cannot verify) would pin our side.
- **ruff, vulture, import-linter:** reached only through `tools check`. This branch adds no new reliance on them.

## Observations

- Finding 2: a search for "run every command" in `scripts/supervise_review.py` gives line 71.
- Finding 3: `tools check --base ebbf1bea` gives 19 ruff errors, 12 of them in w216's lines.
- Finding 4: `agents/bdd-branch-reviewer.md:25` against `git show ebbf1bea:agents/bdd-branch-reviewer.md`; the probe of
  finding 1 gives 41 `none` commits on this branch.
- Finding 6: `supervise_worker.py:42` has the key `branch-review`. A search of `scripts/` for "branch-review" finds it
  only there and in `supervise_review.py:12`, and no upgrade step names it.
- Finding 7: `supervise_review.py:62` (worktree at HEAD, under the lock) against `:67` (`rev-parse` on the root, after
  it). Test not run.
- Finding 8: `supervise_branch_runs.py:40`, `subprocess.run(command, cwd=tree, capture_output=True, text=True,
  env=with_scripts())`, has no timeout. Test not run.
