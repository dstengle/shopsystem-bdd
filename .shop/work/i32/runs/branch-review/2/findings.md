# Branch review 2 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.**
- No finding is triaged fix now, and none is Critical.
- Branch review 1's fix-now finding (KeyError at `scripts/supervise_answers.py:83`) is fixed by w191, and I verified the fix through the real `work run`.
- The status is DONE_WITH_CONCERNS because two checks cannot be verified here (see Cannot verify). Both were already named in review 1.

This is the re-review after a fix work-item (w191). Under the re-review triage, every finding below is an observation or a drop.

## Range and work-items

- **Range:** `d3d3839d..5d72991d`, from `work: start i32` to `work: w191 done -> green`.
- **w189** (review#r31): one commit, `ee81efd0`, which changes `agents/bdd-branch-reviewer.md`. It lies between `6fa7dc00` (claimed) and `72e77945` (done).
- **w190** (supervision#r118, r119): two commits between `2c448d35` (claimed) and `0a9226a6` (done):
  - `6622133a`: steps;
  - `31c86e3c`: `scripts/supervise_answers.py` and `scripts/workqueue_answer.py`.
- **w191** (the fix of branch review 1's findings, under r118 and r119): one commit, `32b5f1fa`, between `25a106bd` (claimed) and `4bb8f10d` (done). It changes:
  - `scripts/supervise_answers.py`;
  - `tests/scenarios/supervision_delegation_steps.py`;
  - `tests/scripts/test_supervise_answers.py` (new).

  This matches its file set and its implementer's result.
- **Commits outside every work-item:**
  - the capability-proposal rounds: `cb357911`, `57be6d74`, `f33c07a6` and `bc00efae`;
  - the `work`, `work note` and `work add` commits;
  - `0716bebe`, branch review 1's record, which touches only `.shop/work/i32/`.

  These rounds are the ones r91 and r96 call for, so they are not stray (review 1's finding 3, dropped).

## Suite

`Suite: 888 passed, 10 failed at 5d72991d in 22.4 s` (and 1 skipped, 56 subtests passed). Command: `python3 -m pytest -q -p no:cacheprovider`.

- **Parallel:** yes, `-n auto` from `pytest.ini`.
- **In-process:** no. The supervision steps run `scripts/work` as a subprocess (`tests/scenarios/test_supervision.py:71`). The suite is under 60 s, so this is no finding.
- **The 10 failures:** every one is a `StepDefinitionNotFoundError` in `features/supervision.feature`. They are exactly the 10 that the suite record in `runs/w191/3-implement/brief.md` lists as `expected`. They belong to other initiatives' unimplemented scenarios and are untouched by this branch, which only appends lines 1457-1474 of that file.

## Checks

- **w189, `python3 -m pytest -q tests/scripts/test_agents.py`:** 8 passed, 18 subtests passed.
- **w189's plan check on r31, `measure` of a later initiative:** not runnable here (see Cannot verify).
- **w190, `python3 -m pytest -q --work-item w190`:** 146 passed, 1 skipped, 56 subtests passed.
- **w191, `python3 -m pytest -q --work-item w191`:** 146 passed, 1 skipped, 56 subtests passed. This includes @r118 and @r119.
- **w191, `python3 -m pytest -q tests/scripts/test_supervise_answers.py`:** 1 passed.
- **`tools check --base d3d3839d` (exit 1):**
  - **ruff:** 7 errors.
    - 5 are in `.shop/work/i32/runs/supervision/3-apply/apply.py`, a committed run record, already in review 1 (finding 3 below).
    - 2 are RUF100 (an unused `noqa` for `E402`) at `tests/scripts/test_supervise_answers.py:9` and `:10`, new in w191 (finding 1).
    - The FURB167 of review 1 is fixed: `re.MULTILINE` at `supervision_delegation_steps.py:171`.
  - **vulture:** 2 hits, `tests/scripts/test_supervise_answers.py:36` and `:51`, unused variable `args` (finding 1).
  - **import-linter:** "the project states no import contracts". I read the module map for myself (see Shape).
- **`tools size --limit 300`:** prints nothing. The touched files have 144 (`supervise_answers.py`), 77 (`workqueue_answer.py`), 202 (`supervision_delegation_steps.py`) and 56 (`test_supervise_answers.py`) lines.
- **`features deprecated`:** 5 deprecated scenarios: migration-tools @r15, supervision @r83, supervision @r102, work-queue @r1 and work-queue @r9.
  - None was added or changed by this branch.
  - @r83's and @r102's replacements have green work-items in other initiatives (i24 w137, i28 w171), so they are already there and not this branch's.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of an operation of its own, so no agreement test applies.
- **Probe of the fixed state, through the real `work run`:** a throwaway scenario in `.shop/scratch/i32-branch-review/`, deleted. It used the suite's own Background and steps:
  - @r119's Givens;
  - a step committing w1's `## Answers` bullet before the run, so that w1 was awaiting-answer, its reviewer's question already answered, and not moved.

  The result:
  - rc 3 (`supervise.py:238`, awaiting the person) and stdout `w1 awaiting-answer`;
  - stderr empty, so no traceback;
  - w1's status still `awaiting-answer`, with no new log line;
  - no `delegation-answerer` session started.

  At `7ede38b8`, review 1's same probe gave a KeyError traceback and rc 1.

## Removed and weakened tests

None.
- I searched `git diff d3d3839d HEAD -- tests features` for removed lines, and for `skip`, `xfail` and `parametrize` in the added lines.
- The only removed line is `re.M` → `re.MULTILINE` in `supervision_delegation_steps.py:171`. That is the same flag, and the step matches what it matched before.
- `features/` changes only by the two scenarios @r118 and @r119, added by the supervision proposal's formulate round (`bc00efae`) and not by a work-item.

## Allowances

Every implementer report gives `## Tests changed under an allowance: none`: w189 3-implement, w190 3-implement and 5-implement, and w191 3-implement. The commits agree: no test that existed at Base had its assertion, expected value or cases changed.

## Cannot verify

- **review#r31 on a real batch.** review is a guarantees capability with no scenario, and w189's plan names `measure` of a later initiative as the check. I verified the agent text (`agents/bdd-branch-reviewer.md:74,76`), not a run's result. This review itself follows it: `questions` holds only fix-now findings.
- **That a real `delegation-answerer` session gives `verdict`.**
  - The scenarios use the stand-in.
  - `agents/delegation-answerer.md` still does not mention `verdict` (`grep -c` gives 0); only the brief's `VERDICT` sentence (`supervise_answers.py:17`) asks for it.
  - Omitting it is safe: the question is left for the person (`supervise_answers.py:121-123`). But a delegated run then stops at the person.

## Findings

### 1. Minor, w191, observation: `tools check` fails on the new test file
- **Where:** `tests/scripts/test_supervise_answers.py:9,10` (`# noqa: E402`, RUF100) and `:36,51` (`*args` unused, vulture).
- **What is wrong:** the regression test adds 4 lint and dead-code hits to a check that already exits 1.
- **Why it matters:** each later review must sort the new hits from the known ones.
- **Fix:**
  - drop `E402` from both `noqa` comments, keeping `F401` on line 9;
  - name the parameters `*_args`, or list them.
- **Reproduction:** `python3 <Scripts>/tools check --base d3d3839d` printed `test_supervise_answers.py:9:19: RUF100 …`, `:10:40: RUF100 …`, `:36: unused variable 'args'` and `:51: unused variable 'args'`.

### 2. Minor, w191, observation: the item left by the fix waits with no question to show
- **Where:** `scripts/supervise_answers.py:85-88`.
- **What is wrong:** take a reviewer's work-item with every question answered but no verdict from this run. It is left awaiting-answer, and `work run` prints `w1 awaiting-answer` and exits 3, with no open question named.
- **The way out:** the person can still move it with `work answer w1 "<text>" --accept` or `--change`. `workqueue_answer.py:50-56` checks only the status and the reviewer's flag, not that a question is open, so it adds a second answer bullet and moves the item.
- **Why it matters:** a stopped run's leftover is no longer a crash, but nothing tells the person what to do.
- **Not code no line asks for:** the no-move serves r77 ("leaves it for the person otherwise") and decision 0069, whose guards hold only on a known change or accept.
- **Hardening, if wanted:**
  - keep the verdict with the answer, which review 1's "better" fix proposed and w191's plan decision 2 declined because no line asks for it; or
  - have r32's exit name the item's answered-but-unmoved state.

  Either needs a line first.
- **Reproduction:** the probe in Checks: rc 3, stdout `w1 awaiting-answer`, w1 unmoved.

### 3. Minor, no work-item (the supervision apply round), observation, carried from review 1: `tools check` lints a committed run record
- **Where:** `.shop/work/i32/runs/supervision/3-apply/apply.py:3-13`, committed in `f33c07a6`.
- **What is wrong:** it gives 5 of the 7 ruff errors.
- **Fix:** have `tools check` skip `.shop/`, or have rounds not leave `.py` files in their stage directories.
- **Reproduction:** as in Checks.

### 4. Minor, w190, observation: a reviewer's item with several questions takes the last session's verdict
- **Where:** `scripts/supervise_answers.py:121-124`.
- **What is wrong:** `self.verdicts[name]` is overwritten by each question's session, so with one `change` and one `accept` the item moves by whichever came last. The verdict is also stored before the line-break check at line 125. That is harmless, because a refused answer sets `left` and prevents the move.
- **Why it matters:** no line names a reviewer asking several questions, and the scenarios have one question.
- **Hardening:** move to `ready` if any verdict is `change`.
- **Reproduction:** by reading the code; no client sends it today.

### 5. Minor, w190, drop (carried): w190's 5-implement result lists `"commits": ["see git log"]`
I verified the commits from the history.

### Checked, no finding
- **w191 against review 1's finding 1:**
  - `target` is `None` unless the item is not the reviewer's (then `asked_from`, as before) or this run holds its verdict (`supervise_answers.py:80-86`).
  - With no target, the `elif self.uncommitted` branch still commits what the run wrote.
  - The non-reviewer path is unchanged.
  - The regression test was red with the guard disabled (implementer's report) and passes now.
- **w191 adds no observable behaviour that no line asks for:** the only new behaviour is the absence of a move, which r77 and 0069 give. The new file is a test.
- **w189 and w190:** as checked in branch review 1 (`.shop/work/i32/runs/branch-review/1/findings.md`, "Checked, no finding"). Their code is unchanged since then, apart from w191's lines above.
- **Decision 0069:** it supersedes only 0063's reviewer row. `workqueue_answer.reviewer_status` (`workqueue_answer.py:30`) is the one rule, shared by `work answer` (line 58) and `work run` (`supervise_answers.py:86`).

## Shape

- **Size rule (300 lines):** met. 144, 77, 202 and 56 lines; `tools size` prints nothing.
- **Module map, `scripts/supervise_answers.py`, "`work run`'s answers under a request's delegation":** met. The fix is at lines 80-88.
- **Module map, `scripts/workqueue_answer.py`, `work answer`:** met. `reviewer_status` is shared, not copied.
- **Module map, `tests/scripts/`, "tests of the scripts that no scenario drives":** met by `tests/scripts/test_supervise_answers.py`. No scenario builds the answered-but-unmoved state.
- **Module map, `tests/scenarios/`, one `<capability>_*_steps.py` a concern:** met.
- **Unreached code or steps:**
  - in `scripts/`, none: vulture is clean there;
  - in the steps, none: `features bindings` says every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (lines 82, 106 and 121), each time reading the log again. Computing it once per item in `answers()` would be complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:** the new behaviour relies on a `verdict` field that only the brief asks for, not the agent's result section. If the session omits it, the question goes to the person, which is safe. Naming `verdict` in `agents/delegation-answerer.md` would make it stable.
- **The new test, `tests/scripts/test_supervise_answers.py`:** it relies on internals of `Answers`, not on a published contract:
  - its method names (`delegation`, `asking`, `held`, `ask`, `section`, `move`, `commit`, `uncommitted`, `push`);
  - the attributes `root`, `dir` and `initiative`;
  - `import supervise` settling the import order.

  A rename breaks the test loudly, not silently. That is acceptable for a script test.
- **pytest-bdd, ruff, vulture, import-linter:** used through their public API or CLI only. The pytest-bdd `FixtureDef` warnings come from its compat layer and were already there.

## Observations

- New lint in w191's test file: `python3 <Scripts>/tools check --base d3d3839d` gives RUF100 at lines 9 and 10, and vulture `args` at lines 36 and 51 (finding 1).
- An answered-but-unmoved reviewer's item waits silently. The scratch probe (@r119's Givens plus a committed answer, then `work run i1`) gave rc 3 and `w1 awaiting-answer`, w1 unmoved; `work answer --accept` or `--change` still moves it (finding 2).
- `tools check` lints `.shop/work/i32/runs/supervision/3-apply/apply.py`, giving 5 ruff errors (finding 3).
- Several reviewer questions: the last verdict wins (`supervise_answers.py:124`), by reading the code (finding 4).
- Deprecated scenarios with green replacements, outside this branch: supervision @r83 and @r102 (`features deprecated`).
