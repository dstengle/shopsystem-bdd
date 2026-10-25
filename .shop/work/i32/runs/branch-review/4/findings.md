# Branch review 4 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.**
- No finding is triaged fix now, and none is Critical.
- No code, agent, test, feature, spec, hook or `CLAUDE.md` file has changed since branch review 3 (`935c2ee0`). `git diff 935c2ee0 HEAD -- scripts agents tests features spec hooks` is empty, and `git log 935c2ee0..HEAD` over those paths and `CLAUDE.md` lists nothing.
- The status is DONE_WITH_CONCERNS because the two checks that reviews 1 to 3 could not verify still cannot be verified (see Cannot verify). Under review#r31 those stay out of `questions`, so `questions` is empty.
- As in review 3: r75 counts only `DONE` as "nothing to fix now", so i32 will not be set done from this result. q10's line 4 names that gap.

## Range and work-items

- **Range:** `d3d3839d..80506ab1`.
- **w189** (review#r31): `ee81efd0`, between `6fa7dc00` (claimed) and `72e77945` (done). It changes `agents/bdd-branch-reviewer.md:74,76`.
- **w190** (supervision#r118, r119): `6622133a` (steps) and `31c86e3c` (`scripts/supervise_answers.py`, `scripts/workqueue_answer.py`). Both lie between `2c448d35` (claimed) and `0a9226a6` (done).
- **w191** (the fix of branch review 1): `32b5f1fa`, between `25a106bd` (claimed) and `4bb8f10d` (done).
- **Commits that belong to no i32 work-item:** none of them touches code, tests, `features/` or `spec/`.
  - **Carried from review 3:** the proposal rounds `cb357911`, `57be6d74`, `f33c07a6` and `bc00efae` (r91, r96); the `work`, `work note` and `work add` commits; the branch-review records `0716bebe` and `4e5cb0cd`; `3e1cb8bb` (finding 1); `d05108fe`; and request q10, `2759e6b6`..`935c2ee0`.
  - **New since review 3:**
    - `1eccd7e3`, the record of branch review 3;
    - `6e0060e8`..`80506ab1`, i31's work-item w185 (drafted → researched → planned → ready → claimed → awaiting-answer → ready → claimed). These commits hold only `.shop/work/i31/` run records. w185 has no implementation commit yet, and the working tree is clean;
    - `1caef881` and `9bca1b1a`, the start of i33, fulfilling q10 (`.shop/work/i33/`).

    Other initiatives' work landing on i32's branch is finding 6.

## Suite

`Suite: 888 passed, 10 failed at 80506ab in 26.2 s` (26.5 s wall; also 1 skipped and 56 subtests passed). Command: `python3 -m pytest -q -p no:cacheprovider`.

- **Parallel:** yes, `-n auto` from `pytest.ini` (1401 % CPU).
- **In-process:** no. The supervision steps run `scripts/work` as a subprocess. The suite is under 60 s, so this is no finding.
- **The 10 failures:** the same 10 as in reviews 1 to 3. All are in `features/supervision.feature` and fail with `StepDefinitionNotFoundError`. They are i31's scenarios (r111–r116, r83), which w185 accepts and has not yet implemented. None of them is this branch's work-items'.

## Checks

- **w189:**
  - `pytest tests/scripts/test_agents.py tests/scripts/test_supervise_answers.py`: 9 passed, 18 subtests passed.
  - The kept-branch-review scenarios, `--whole-suite -n 0 -m "" tests/scenarios/test_supervision.py -k kept_branch_review`: 7 passed.
  - The plan's check on r31 (`measure` of a later initiative): cannot be verified (see Cannot verify).
- **w190, `--work-item w190`:** 146 passed, 1 skipped, 56 subtests passed.
- **w191:**
  - `--work-item w191`: 146 passed, 1 skipped, 56 subtests passed;
  - `test_supervise_answers.py` passed, within the 9 above.
- **`tools check --base d3d3839d`:**
  - **ruff:** 7 errors, unchanged:
    - 5 in `.shop/work/i32/runs/supervision/3-apply/apply.py` (finding 3);
    - 2 RUF100 at `tests/scripts/test_supervise_answers.py:9,10` (finding 2).
  - **vulture:** 2 hits, unused `args` at `tests/scripts/test_supervise_answers.py:36,51` (finding 2).
  - **import-linter:** "the project states no import contracts". I checked the module map myself (see Shape).
- **`tools size --limit 300`:** prints nothing.
- **`features deprecated`:** 5 deprecated scenarios: migration-tools @r15, supervision @r83 and @r102, work-queue @r1 and @r9.
  - None was added by an i32 work-item.
  - The replacement of @r83 is w185's (i31), which is not `green`. So @r83 is rightly still deprecated.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of any of its operations, so no agreement test applies.

## Removed and weakened tests

None.
- I searched for removed lines in `git diff d3d3839d HEAD -- tests features`, and for `skip`, `xfail` and `parametrize` in its added lines.
- The only removed line is `re.M` → `re.MULTILINE` at `tests/scenarios/supervision_delegation_steps.py:171`. That is the same flag.
- No skip, xfail or parametrize was added.
- `features/` changes only by adding @r118 and @r119 (formulate round `bc00efae`, not a work-item).

## Allowances

Every implementer report (w189 3-implement, w190 3-implement and 5-implement, w191 3-implement) gives `## Tests changed under an allowance` as none. The commits agree.

## Cannot verify

- **review#r31 on a real batch.** w189's plan names `measure` of a later initiative as the check.
  - The latest analysis in `.shop/records/` is still `2026-10-25-i30-analysis.md`; no measure of a later initiative exists.
  - I checked the agent text (`agents/bdd-branch-reviewer.md:74,76`), and this review follows it.
- **That a real `delegation-answerer` session gives `verdict`.**
  - `grep -c verdict agents/delegation-answerer.md` gives 0. Only the brief (`scripts/supervise_answers.py:17`) asks for it, and the scenarios use a stand-in.
  - Omitting it is safe: the question is left for the person (`supervise_answers.py:121-123`).
  - q10 line 3 (accepted) takes this up.

## Findings

### 1. Minor, no work-item (`3e1cb8bb`), observation (carried): i31's status edited by hand on this branch
- **Where:** `.shop/work/i31/initiative.md:4`, `done` → `started`, outside `work`.
- **Fix:** deliver q10 lines 1 and 2, after which no command-less reopen is needed.
- **Reproduction:** `git show 3e1cb8bb`.

### 2. Minor, w191, observation (carried): `tools check` hits in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9,10` (RUF100 for `E402`) and `:36,51` (vulture, unused `*args`).
- **Fix:** drop `E402` from both `noqa` comments, and name the parameters `*_args`.
- **Reproduction:** `tools check --base d3d3839d`, output as in Checks.

### 3. Minor, no work-item (the supervision apply round), observation (carried): `tools check` lints a committed run record
- **Where:** `.shop/work/i32/runs/supervision/3-apply/apply.py:3-13` (`f33c07a6`). It gives 5 of the 7 ruff errors.
- **Fix:** exclude `.shop/` from `tools check`, or have rounds leave no `.py` file in their stage directories.

### 4. Minor, w191, observation (carried): an answered-but-unmoved reviewer's item waits with no question shown
- **Where:** `scripts/supervise_answers.py:85-88`.
- **What happens:** `work run` exits 3 with `w1 awaiting-answer` and names no open question.
- **Reproduction:** review 2's probe gave rc 3 with w1 unmoved. The code is unchanged since.

### 5. Minor, w190, observation (carried): with several reviewer questions on one item, the last verdict wins
- **Where:** `scripts/supervise_answers.py:124`.
- **Why it is an observation:** no line names a reviewer asking several questions.
- **Hardening:** move the item to `ready` if any verdict is `change`.

### 6. Minor, no work-item, observation (new): other initiatives' work runs on i32's branch
- **What:** w185's commits (i31) and i33's start (`1caef881`, `9bca1b1a`) are on `i25-review-findings-to-implementation`, inside i32's range `d3d3839d..HEAD`.
- **Why it matters:**
  - Each commit there counts as unread for i32's next branch review. That re-reviews i32 with nothing of its own changed: this is the fourth review, and the third with no change to i32's code.
  - Once w185 commits code, that code will lie in i32's range and no i32 work-item will own it.
- **Why it is an observation:** none of it touches code yet. r95 runs rounds one at a time across initiatives on one branch by design.
- **Fix:** have a branch review read only the commits that touch its initiative's work-items' filesets, or `.shop/work/<initiative>/`.
- **Reproduction:** `git log --oneline 935c2ee0..HEAD` lists 9 commits of i31/w185 and i33, and 1 of i32 (`1eccd7e3`, review 3's record).

### Checked, no finding
- **Since review 3:** no code change, so reviews 1 to 3's checks of w189, w190, w191 and decision 0069 stand.
- **No code that no line asks for:** the `verdict` move serves r118, r119 and 0069; the no-move serves r77; w189's text serves r31.

## Shape

- **Size, 300 lines:** met. `tools size` prints nothing.
- **Module map:** each row the branch touched is met:
  - `scripts/supervise_answers.py`: answers under a delegation;
  - `scripts/workqueue_answer.py`: `work answer`, with `reviewer_status` at line 31 shared with `supervise_answers.py:86`;
  - `tests/scenarios/supervision_delegation_steps.py`: one steps module a concern;
  - `tests/scripts/test_supervise_answers.py`: tests no scenario drives.
- **Unreached code or steps:** none. vulture is clean in `scripts/`, and every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (lines 82, 106 and 121). Computing it once is complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:**
  - r118 and r119 rely on a `verdict` result field that only the brief names.
  - If the session omits it, the question goes to the person: safe, but the run stops there.
  - Naming `verdict` in `agents/delegation-answerer.md` (q10 line 3) makes it stable.
- **`tests/scripts/test_supervise_answers.py`:** it relies on `Answers` internals. A rename fails loudly, which is acceptable for a script test.
- **pytest-bdd, ruff, vulture:** used through their public CLI or API only.

## Observations

- i31's status was hand-edited on i32's branch: `git show 3e1cb8bb` (finding 1).
- `tools check --base d3d3839d` gives RUF100 at `test_supervise_answers.py:9,10` and vulture `args` at lines 36 and 51 (finding 2).
- `tools check` lints `.shop/work/i32/runs/supervision/3-apply/apply.py`, giving 5 ruff errors (finding 3).
- An answered-but-unmoved reviewer's item waits silently: rc 3, `w1 awaiting-answer` (review 2's probe; finding 4).
- With several reviewer questions the last verdict wins, at `supervise_answers.py:124` (finding 5).
- Other initiatives' commits re-open i32's branch review: `git log --oneline 935c2ee0..HEAD` lists 9 commits of i31 and i33 (finding 6).
- `grep -c verdict agents/delegation-answerer.md` gives 0 (Cannot verify; q10 line 3).
- A DONE_WITH_CONCERNS result with empty `questions` keeps i32 from done under r75 (q10 line 4).
