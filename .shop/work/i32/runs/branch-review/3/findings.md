# Branch review 3 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.**
- No finding is triaged fix now, and none is Critical.
- No code, test, feature or spec file has changed since branch review 2 (`5d72991d`). The commits since then are records, a request and one hand edit of another initiative's status.
- The status is DONE_WITH_CONCERNS for one reason: the same two checks as in reviews 1 and 2 still cannot be verified (see Cannot verify). Under review#r31 those stay out of `questions`, so `questions` is empty.
- How the loop will read this: r75 counts only `DONE` as "nothing to fix now". So i32 will again not be set done from this result. That is the gap q10's line 4 names (accepted 2026-10-25, not yet delivered). This review does not route around it by claiming checks it did not verify.

## Range and work-items

- **Range:** `d3d3839d..935c2ee0`.
- **w189** (review#r31): `ee81efd0`, between `6fa7dc00` (claimed) and `72e77945` (done). It changes `agents/bdd-branch-reviewer.md:74,76`.
- **w190** (supervision#r118, r119):
  - `6622133a`: steps;
  - `31c86e3c`: `scripts/supervise_answers.py` and `scripts/workqueue_answer.py`.

  Both lie between `2c448d35` (claimed) and `0a9226a6` (done).
- **w191** (the fix of branch review 1): `32b5f1fa`, between `25a106bd` (claimed) and `4bb8f10d` (done). It changes `scripts/supervise_answers.py`, `tests/scenarios/supervision_delegation_steps.py` and `tests/scripts/test_supervise_answers.py`.
- **Commits that belong to no work-item:**
  - the proposal rounds: `cb357911`, `57be6d74`, `f33c07a6` and `bc00efae` (r91 and r96, not stray);
  - the `work`, `work note` and `work add` commits;
  - the branch-review records `0716bebe` and `4e5cb0cd`;
  - since review 2:
    - `3e1cb8bb`, which hand-edits `.shop/work/i31/initiative.md` (finding 1);
    - `d05108fe`, an observation in `.shop/records/observations.md`;
    - `2759e6b6`..`935c2ee0`, request q10 and its intake round, all under `.shop/work/requests/`.

  None of these touches code, tests, `features/` or `spec/`.

## Suite

`Suite: 888 passed, 10 failed at 935c2ee in 22.1 s` (22.5 s wall; also 1 skipped and 56 subtests passed). Command: `python3 -m pytest -q -p no:cacheprovider`.

- **Parallel:** yes, `-n auto` from `pytest.ini` (1640 % CPU).
- **In-process:** no. The supervision steps run `scripts/work` as a subprocess. The suite is under 60 s, so this is no finding.
- **The 10 failures:** the same 10 as in reviews 1 and 2. All are in `features/supervision.feature`, other initiatives' scenarios with no step definitions, and not this branch's.

## Checks

- **w189:**
  - `python3 -m pytest -q tests/scripts/test_agents.py tests/scripts/test_supervise_answers.py`: 9 passed, 18 subtests passed.
  - The research notes name three kept-branch-review scenarios. I ran them with `--whole-suite -n 0 -m "" tests/scenarios/test_supervision.py -k kept_branch_review`: 7 passed.
  - The plan's own check on r31 (`measure` of a later initiative) cannot be verified here (see Cannot verify).
- **w190, `--work-item w190`:** 146 passed, 1 skipped, 56 subtests passed.
- **w191:**
  - `--work-item w191`: 146 passed, 1 skipped, 56 subtests passed;
  - `test_supervise_answers.py`: passed, within the 9 above.
- **`tools check --base d3d3839d`:**
  - **ruff:** 7 errors, the same as in review 2:
    - 5 in the committed run record `.shop/work/i32/runs/supervision/3-apply/apply.py` (finding 3);
    - 2 RUF100 at `tests/scripts/test_supervise_answers.py:9,10` (finding 2).
  - **vulture:** 2 hits, unused `args` at `tests/scripts/test_supervise_answers.py:36,51` (finding 2).
  - **import-linter:** "the project states no import contracts". I read the module map for myself (see Shape).
- **`tools size --limit 300`:** prints nothing.
- **`features deprecated`:** 5 deprecated scenarios: migration-tools @r15, supervision @r83 and @r102, work-queue @r1 and @r9. None was added or changed by this branch.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of one of its operations, so no agreement test applies.

## Removed and weakened tests

None.
- I searched `git diff d3d3839d HEAD -- tests features` for removed lines, and for `skip`, `xfail` and `parametrize` in the added lines.
- The only removed line is `re.M` → `re.MULTILINE` in `tests/scenarios/supervision_delegation_steps.py:171`. That is the same flag.
- `features/` changes only by @r118 and @r119, added by the formulate round `bc00efae`, not by a work-item.

## Allowances

Each implementer report gives `## Tests changed under an allowance` `none`: w189 3-implement, w190 3-implement and 5-implement, and w191 3-implement. The commits agree.

## Cannot verify

- **review#r31 on a real batch.** w189's plan names `measure` of a later initiative as the check, and none exists yet. I verified the agent text (`agents/bdd-branch-reviewer.md:74,76`). This review also follows it: `questions` is empty while the status is DONE_WITH_CONCERNS.
- **That a real `delegation-answerer` session gives `verdict`.**
  - `agents/delegation-answerer.md` still does not mention `verdict` (0 matches). Only the brief's sentence at `scripts/supervise_answers.py:17` asks for it.
  - The scenarios use a stand-in.
  - Omitting it is safe: the question is left for the person (`supervise_answers.py:121-123`).
  - q10's line 3 (accepted) takes this up.

## Findings

### 1. Minor, no work-item (`3e1cb8bb`), observation: another initiative's status edited by hand on this branch
- **Where:** `.shop/work/i31/initiative.md:4`, `status: done` → `started`, committed outside `work` and outside every work-item.
- **Why it matters:** i31's `log.jsonl` records no initiative transition, so nothing but the commit message tells why its status changed. The edit also bypasses the queue's commands.
- **Why it is an observation:** the commit message gives the reason. `work withdraw w183` let r23 set i31 done before w185 was added, and no command reopens an initiative. q10's lines 1 and 2 (accepted) are the fix. No code is involved.
- **Fix:** deliver q10 lines 1 and 2, after which no such edit is needed.
- **Reproduction:** `git show 3e1cb8bb`, then `git log --format='%h %s' -- .shop/work/i31/initiative.md`.

### 2. Minor, w191, observation (carried from review 2): `tools check` hits in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9,10` (RUF100: `E402` unused in `noqa`) and `:36,51` (vulture: unused `*args`).
- **Fix:** drop `E402` from both comments, and name the parameters `*_args`.
- **Reproduction:** `tools check --base d3d3839d`, as in Checks.

### 3. Minor, no work-item (the supervision apply round), observation (carried): `tools check` lints a committed run record
- **Where:** `.shop/work/i32/runs/supervision/3-apply/apply.py:3-13`, committed in `f33c07a6`.
- **What is wrong:** it gives 5 of the 7 ruff errors.
- **Fix:** exclude `.shop/` from `tools check`, or have rounds not leave `.py` files in their stage directories.

### 4. Minor, w191, observation (carried): an answered-but-unmoved reviewer's item waits with no question shown
- **Where:** `scripts/supervise_answers.py:85-88`.
- **What happens:** `work run` exits 3 with `w1 awaiting-answer` and names no open question. The person can still move the item with `work answer w1 "<text>" --accept` or `--change`.
- **Reproduction:** review 2's probe gave rc 3, w1 unmoved. The code is unchanged since.

### 5. Minor, w190, observation (carried): several reviewer questions on one item, the last verdict wins
- **Where:** `scripts/supervise_answers.py:124`.
- **Why it is an observation:** no line names a reviewer asking several questions.
- **Hardening:** move to `ready` if any verdict is `change`.

### Checked, no finding
- **Since review 2:** `git diff 5d72991d HEAD -- scripts agents tests features spec` is empty, so reviews 1 and 2's checks of w189, w190, w191 and decision 0069 stand.
- **No code that no line asks for:**
  - the `verdict` move serves r118, r119 and 0069;
  - the no-move serves r77;
  - w189's text serves r31.

## Shape

- **Size, 300 lines:** met. `tools size` prints nothing. The touched files have 144, 77, 202 and 56 lines.
- **Module map, `scripts/supervise_answers.py`, "answers under a delegation":** met.
- **Module map, `scripts/workqueue_answer.py`, `work answer`:** met. `reviewer_status` (line 31) is shared with `supervise_answers.py:86`.
- **Module map, `tests/scenarios/`, one steps module a concern:** met (`supervision_delegation_steps.py`).
- **Module map, `tests/scripts/`, tests no scenario drives:** met (`test_supervise_answers.py`).
- **Unreached code or steps:**
  - in `scripts/`, none: vulture is clean there;
  - in the steps, none: every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (lines 82, 106 and 121). Computing it once per item would be complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:**
  - r118 and r119 rely on a `verdict` result field that only the brief asks for, not the agent file.
  - If the session omits it, the question goes to the person: safe, but a delegated run stops there.
  - Naming `verdict` in `agents/delegation-answerer.md` (q10 line 3) makes it stable.
- **`tests/scripts/test_supervise_answers.py`:** it relies on `Answers` internals, its method and attribute names. A rename fails loudly. That is acceptable for a script test.
- **pytest-bdd, ruff, vulture:** used through their public CLI or API only.

## Observations

- i31's status was hand-edited on i32's branch (`git show 3e1cb8bb`); q10 lines 1 and 2 cover it (finding 1).
- New lint in w191's test: `tools check --base d3d3839d` gives RUF100 at lines 9 and 10, and vulture `args` at lines 36 and 51 (finding 2).
- `tools check` lints `.shop/work/i32/runs/supervision/3-apply/apply.py`, giving 5 ruff errors (finding 3).
- An answered-but-unmoved reviewer's item waits silently: rc 3, `w1 awaiting-answer` (review 2's probe; finding 4).
- With several reviewer questions the last verdict wins, at `supervise_answers.py:124`, by reading the code (finding 5).
- The delegation-answerer's agent file has no `verdict`: `grep -c verdict agents/delegation-answerer.md` gives 0 (Cannot verify; q10 line 3).
- A DONE_WITH_CONCERNS branch review with empty `questions` keeps i32 from done under r75 (q10 line 4).
