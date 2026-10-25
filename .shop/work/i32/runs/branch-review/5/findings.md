# Branch review 5 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.**
- No finding of an i32 work-item is triaged fix now, and none is Critical.
- Since branch review 4 (`80506ab1`), nothing of i32 has changed: no code, agent, test, feature, spec, hook or `CLAUDE.md` file of w189, w190 or w191. The only i32 commit is `380be1d1`, the record of review 4.
- New since review 4: i31's work-item w185 has committed code into this range (`aef1793b`, `a0f2b5ba`, `ce5c1bfb`). Review 4's finding 6 said this would happen. w185 is now `claimed` again. Its own task review (i31 `runs/w185/5-review`) raised two Important fix-now findings, and the person's delegation has answered "fix both". Both defects are still at HEAD; see findings 7 and 8. They belong to i31, so they stay out of this review's `questions` (see finding 7's triage).
- The status is DONE_WITH_CONCERNS because two checks still cannot be verified, the same two as in reviews 1 to 4 (see Cannot verify).

## Range and work-items

- **Range:** `d3d3839d..507d361e`.
- **w189** (review#r31): `ee81efd0`, which changes `agents/bdd-branch-reviewer.md:74,76`.
- **w190** (supervision#r118, r119): `6622133a` and `31c86e3c`.
- **w191** (the fix of branch review 1): `32b5f1fa`.
- **Commits that belong to no i32 work-item:**
  - Carried from review 4: the proposal rounds, the `work`, `work note` and `work add` commits, the branch-review records, `3e1cb8bb` (finding 1), `d05108fe`, q10, w185's state commits and i33's start.
  - New since review 4:
    - `380be1d1`, the record of review 4;
    - i33's integrate round and gates: `da59b6b8`, `9a888415`, `5f743a7b`, `b0d3f5bf`, `9c08e5f0`, `bf8cd8fa`, `1bcf6ddb`, `51088ad2`. These touch `.shop/work/i33/` only;
    - **w185 (i31):** `aef1793b`, `a0f2b5ba` and `ce5c1bfb`, between `80506ab1` (claimed) and `e53f2587` (done). After them come `94ba20f1` (done → awaiting-answer), `6c5088e8` (answered) and `507d361e` (claimed). They change:
      - `scripts/supervise.py`, `scripts/supervise_change.py` and `scripts/supervise_rounds.py`;
      - `features/supervision.feature`;
      - `tests/scenarios/supervision_{done,formulate,rounds}_steps.py`, `tests/scenarios/test_supervision.py` and `tests/scripts/stub_claude.py`.

## Suite

`Suite: 897 passed, 0 failed at 507d361 in 25.75 s` (26.1 s wall; also 1 skipped and 56 subtests passed). Command: `python3 -m pytest -q -p no:cacheprovider --tb=no`.

- **Parallel:** yes, `-n auto` from `pytest.ini` (1522 % CPU).
- **In-process:** no. The supervision steps run `scripts/work` as a subprocess. The suite is under 60 s, so this is no finding.
- **Change from reviews 1 to 4:** the 10 `StepDefinitionNotFound` failures (i31's r111–r116 and r83) are gone, because w185 now has their steps.

## Checks

- **w189:**
  - `pytest tests/scripts/test_agents.py tests/scripts/test_supervise_answers.py`: 9 passed, 18 subtests passed.
  - The kept-branch-review scenarios, `--whole-suite -n 0 -m "" tests/scenarios/test_supervision.py -k kept_branch_review`: 7 passed.
  - The plan's `measure` check: cannot be verified (see Cannot verify).
- **w190, `-n 0 --work-item w190`:** 146 passed, 1 skipped, 56 subtests passed.
- **w191:**
  - `-n 0 --work-item w191`: 146 passed, 1 skipped, 56 subtests passed;
  - `test_supervise_answers.py`: passed, within the 9 above.
- **`tools check --base d3d3839d`:**
  - **ruff:** 10 errors.
    - 5 are in `.shop/work/i32/runs/supervision/3-apply/apply.py` (finding 3, carried).
    - 2 are RUF100 at `tests/scripts/test_supervise_answers.py:9,10` (finding 2, carried).
    - 3 are new to the report: I001 at `tests/scenarios/test_supervision.py:14`, and FURB167 at `tests/scripts/stub_claude.py:189,190`. They appear now because w185 touched both files. Neither hit is on a line w185 changed: w185's `stub_claude.py` hunk is at line 264, and its import line, 31, is in sorted order. This is finding 9.
  - **vulture:** clean.
    - Reviews 2 to 4 reported unused `args` at `test_supervise_answers.py:36,51`. That file is unchanged since `32b5f1fa`, and the parameters are still `*args`, but vulture no longer reports them.
    - Finding 2 keeps only the ruff part.
  - **import-linter:** "the project states no import contracts". I checked the module map myself (see Shape).
- **`tools size --limit 300`:** prints nothing, and exits 0.
- **`features deprecated`:** 4 deprecated scenarios: migration-tools @r15, supervision @r102, work-queue @r1 and @r9.
  - None of them is an i32 work-item's.
  - The old supervision @r83 was removed by w185 (i31). w185's `## Retires` lists it, so this is the allowed kind of change under `features/`.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of any of its operations, so no agreement test applies.

## Removed and weakened tests

None in i32's work-items. I searched removed lines in `git diff d3d3839d HEAD -- tests features` for deleted `def test_` and assertions, for loosened asserts, and for `skip`, `xfail` and `parametrize` in the added lines.

- **i32:** `re.M` → `re.MULTILINE` at `tests/scenarios/supervision_delegation_steps.py:171` is the same flag.
- **w185 (i31), checked because its commits lie in the range:**
  - **The removed @r83 (deprecated) scenario:** w185's Retires lists it.
  - **`questions_hold`** (`supervision_rounds_steps.py:68-73`): a text of 4 quotes still asserts `gate_question(text)`, as before. Its other branch serves only the new r113 scenario (`features/supervision.feature:1248`). `gate_question` unpacks exactly 4 quotes, so no earlier case could have taken that branch.
  - **`apply_started`:** widened to `apply|formulate`. The `apply` case asserts what it asserted before.
  - **`answered_proposal`:** writes the same proposal as before unless "its adds naming" or "given by its … round" is in the text.

  None of these is weakened.

## Allowances

- **i32:** every implementer report (w189 3-implement, w190 3-implement and 5-implement, w191 3-implement) gives none. The commits agree.
- **w185:** its `setup` row was verified by its own task review (i31 `runs/w185/5-review`), not by this review.

## Cannot verify

- **review#r31 on a real batch.** w189's plan names `measure` of a later initiative as the check.
  - The latest analysis in `.shop/records/` is still `2026-10-25-i30-analysis.md`.
  - I checked the agent text (`agents/bdd-branch-reviewer.md:74,76`), and this review follows it.
- **That a real `delegation-answerer` session gives `verdict`.**
  - `grep -c verdict agents/delegation-answerer.md` gives 0. Only the brief (`scripts/supervise_answers.py:17`) asks for it.
  - Omitting it is safe: the question is left for the person.
  - q10 line 3, delivered by i33, takes this up.

## Findings

### 1. Minor, no work-item (`3e1cb8bb`), observation (carried): i31's status edited by hand on this branch
- **Where:** `.shop/work/i31/initiative.md:4`, `done` → `started`, outside `work`.
- **Fix:** q10 lines 1 and 2.
- **Reproduction:** `git show 3e1cb8bb`.

### 2. Minor, w191, observation (carried): RUF100 in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9,10`, an unused `noqa: E402`.
- **Fix:** drop `E402` from both comments.
- **Reproduction:** `tools check --base d3d3839d`.

### 3. Minor, no work-item (the supervision apply round), observation (carried): `tools check` lints a committed run record
- **Where:** `.shop/work/i32/runs/supervision/3-apply/apply.py:3-13`, 5 ruff errors.
- **Fix:** exclude `.shop/` from `tools check`.

### 4. Minor, w191, observation (carried): an answered-but-unmoved reviewer's item waits with no question shown
- **Where:** `scripts/supervise_answers.py:85-88`.
- **What happens:** rc 3, `w1 awaiting-answer`, and no open question is named.
- **Reproduction:** review 2's probe. The code is unchanged since.

### 5. Minor, w190, observation (carried): with several reviewer questions on one item, the last verdict wins
- **Where:** `scripts/supervise_answers.py:124`.
- **Hardening:** move the item to `ready` if any verdict is `change`.

### 6. Important (was Minor), no i32 work-item, observation: other initiatives' work lands in i32's range
- **What:** review 4 said this would happen, and now it has. w185's code (i31) is inside `d3d3839d..HEAD`, and no i32 work-item owns it.
- **Why it is now Important:** the defects in that code (findings 7 and 8) show up in i32's branch review and keep its result from `DONE`. Under r75, i32 then cannot be done until another initiative's work-item is fixed.
- **Why it is an observation:** r95 (one branch, rounds one at a time across initiatives) does this by design. No line names how one initiative's branch review treats another's commits.
- **Fix:** a line for it, through integrating-a-proposal. A branch review would read only the commits of its own initiative's work-items and of `.shop/work/<initiative>/`.
- **Reproduction:** `git log --oneline 80506ab1..HEAD -- scripts tests features` lists 3 commits, all of them w185's.

### 7. Important, w185 (i31), observation for i32 (fix now in i31): an apply round's change list naming another or unknown capability is dropped silently
- **Where:** `scripts/supervise_rounds.py:126-132` and `scripts/supervise_change.py:52-65` (`rewrite_lists`).
- **What is wrong:**
  - Entries whose `capability` is not the proposal's `argues` are skipped without a word, so a capability no spec holds is never refused, against r107.
  - A list that names only other capabilities empties `adds`, `changes` and `removes`.
- **Why it matters:** the proposal's lists are lost (data lost).
- **Fix:** refuse as r107 says.
- **Triage:**
  - This is a fix-now defect, but it is w185's. w185 already holds it as an answered question ("Fix both", 2026-10-25), and it is `claimed` to fix it.
  - Listing it in i32's `questions` would draft a second fix work-item under i32 for the same lines, so it stays out.
  - It is verified at HEAD by reading: the code is as w185's 5-review found it.

### 8. Important, w185 (i31), observation for i32 (fix now in i31): a refused round stops the initiative's other proposals' rounds
- **Where:** `scripts/supervise.py:205-213` with `scripts/supervise_rounds.py:62-67`.
- **What is wrong:** `rounds()` raises at the first `Refused`, and only `draft()` and `pull()` run after it. Other due proposals get no round before the error, against r115 and r111.
- **Fix:** w185's answer: let the others have their rounds, then raise.
- **Triage:** the same as finding 7. It is held by w185, so it is not in i32's `questions`.

### 9. Minor, w185 (i31), observation: ruff hits in files w185 touched
- **Where:** `tests/scenarios/test_supervision.py:14` (I001) and `tests/scripts/stub_claude.py:189,190` (FURB167, `re.M`).
- **Why they appear:** both files are now in `tools check --base`'s set. The lines were not changed by w185, so these are already there.
- **Fix:** `re.MULTILINE`, and sort the import block (`ruff check --fix`).
- **Reproduction:** `tools check --base d3d3839d`.

### Checked, no finding
- **i32's code since review 4:** unchanged, so reviews 1 to 4's checks of w189, w190, w191 and decision 0069 stand.
- **Code that no line asks for in i32:** none. The `verdict` move serves r118, r119 and 0069, the no-move serves r77, and w189's text serves r31.
- **w185's code against a line:** not in i32's scope beyond findings 6 to 9. I read its diff once. i31's own task and branch reviews own it.

## Shape

- **Size, 300 lines:** met. `tools size` prints nothing.
- **Module map, i32's rows:** met, as in review 4:
  - `supervise_answers.py`: answers under a delegation;
  - `workqueue_answer.py:31` (`reviewer_status`), shared with `supervise_answers.py:86`;
  - `tests/scenarios/supervision_delegation_steps.py`;
  - `tests/scripts/test_supervise_answers.py`.
- **Module map, w185's new module:** `tests/scenarios/supervision_formulate_steps.py` falls under the `tests/scenarios/` row (one `<capability>_*_steps.py` module a concern). Met.
- **Unreached code or steps:** none. vulture is clean, and every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (`supervise_answers.py:82,106,121`). Computing it once is complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:** r118 and r119 rely on a `verdict` result field that only the brief names.
  - Without it, the question goes to the person: safe.
  - Naming `verdict` in `agents/delegation-answerer.md` (q10 line 3) makes it stable.
- **`tests/scripts/stub_claude.py`:** now gives `usage` (w185). The stand-in mirrors the CLI's result JSON, so a change in the CLI's fields shows only on a real run.
- **pytest-bdd, ruff, vulture:** used through their public CLI or API only.

## Observations

- i31's status was hand-edited on i32's branch: `git show 3e1cb8bb` (finding 1).
- `tools check --base d3d3839d` gives RUF100 at `test_supervise_answers.py:9,10` (finding 2).
- `tools check` lints the committed `.shop/work/i32/runs/supervision/3-apply/apply.py`: 5 ruff errors (finding 3).
- An answered-but-unmoved reviewer's item waits silently: rc 3, `w1 awaiting-answer` (review 2's probe; finding 4).
- With several reviewer questions the last verdict wins, at `supervise_answers.py:124` (finding 5).
- Other initiatives' code is now in i32's range: `git log --oneline 80506ab1..HEAD -- scripts tests features` lists `ce5c1bfb`, `a0f2b5ba` and `aef1793b`, all w185's (finding 6).
- w185's two fix-now defects are still at HEAD: `supervise_change.py:58-59` filters on `argues` with no refusal, and `supervise.py:205-213` raises after `draft` and `pull` only (findings 7 and 8; i31 `w185.md` `## Answers`).
- `tools check` gives I001 at `test_supervision.py:14` and FURB167 at `stub_claude.py:189,190`, on lines w185 did not change (finding 9).
- vulture no longer reports `*args` at `test_supervise_answers.py:36,51`, though the file is unchanged since `32b5f1fa`.
- `grep -c verdict agents/delegation-answerer.md` gives 0 (Cannot verify).
