# Branch review of i28 (review 7, at eca9d404)

**Verdict: DONE.**

- Every check of i28's six work-items passes, and I ran each one myself.
- No finding is Critical and none is triaged fix now.
- **None of i28's code has changed since review 6 (`f647911b`).** Six commits since then touch files outside `.shop/`, and none of them is i28's:
  - **`641f95a9` (i26, w178):** changes `supervise_all.py`, among other files, but only its exit code (r101). The r103 start that w170 added, at `scripts/supervise_all.py:18-35`, is unchanged.
  - **`a2d1083e` (i25, w176):** adds `--change` and `--accept` to `workqueue_answer.py`. The r30 path that w168 added (`<initiative>/<name>`) is unchanged.
  - The other four are spec, formulate and merge commits of i29 and i30.
- **The suite at head is red with 8 failures.** Each is a `StepDefinitionNotFoundError` in a scenario of another initiative whose work-item is not green yet (finding 6).
- What remains for i28 are Minor items carried over from earlier reviews.

## Range and work-items

- **Range:** `4b7dca6c..eca9d404` on `i25-review-findings-to-implementation`, 306 commits.
  - Base `4b7dca6c` is "work: start i28, fulfilling q6".
  - Head `eca9d404` is "work: w179 ready -> claimed".
- **i28's work-items and their commits** (unchanged):

| Work-item | Status | Accepts | Commits |
|---|---|---|---|
| w167 | green | supervision#r92 | `12f0b295` |
| w168 | green | work-queue#r30 | `fa6929fb` |
| w169 | green | spec-integration#r43, a guarantee | `50788670` |
| w170 | green | supervision#r102, r103, r104 | `bcc41527`, `55eea183`, `2e0f2555` |
| w171 | green | supervision#r102 | `a414d2bd` |
| w172 | green | supervision#r102, r103, r104 (fix of branch review 1) | `a1ff989a` |

- **Commits of no i28 work-item:** every other commit in the range (finding 5). Since review 6 these are:
  - w176's commits (i25), w178's (i26), and w175's, w179's and w181's (i29);
  - w180's (i30);
  - i29's supervision rounds, including spec `3bfdba68`, formulate `d073c518` and the merges `c09f8d77` and `b6f0aa7a`;
  - i30's formulation rounds, including spec `31738369` and the merge `d72ed2af`;
  - `5bf9646a` and `ed5396f5`, the records of branch review 6 of i28 and of i27;
  - `0fdb14af`, branch review 2 of i26;
  - the records `cebadf9d` and `1d0dcdeb`;
  - answer and note commits.

## Suite

`Suite: 874 passed, 8 failed at eca9d404 in 27.8 s`

pytest's own line was "8 failed, 874 passed, 1 skipped, 410 warnings, 56 subtests passed in 27.44s". The 27.8 s is the shell's `time` for the whole run.

- **Parallel:** yes. `pytest.ini` has `addopts = -n auto`; the run used 1423 % CPU.
- **In-process:** no. The step definitions run `work` and the other commands as subprocesses.
- Under 60 s, so the wall time is no finding.
- **The 8 failures**, each a `StepDefinitionNotFoundError`:

| Scenario | Work-item | Its status |
|---|---|---|
| requests @r22 | i29, w175 | claimed |
| supervision @r15 | i29, w179 | claimed |
| supervision @r107 | i29, w181 | drafted |
| supervision @r108 (gate and apply) | i29, w181 | drafted |
| supervision @r106 | i29, w181 | drafted |
| supervision @r105 | i29, w181 | drafted |
| supervision "an initiative set done is committed on the initiative branch" (feature line 1363) | i29, w181 | drafted |

- **Passing now that failed at review 6:**
  - supervision @r9, @r67, @r82, @r100 and @r101, delivered by w178, which is green;
  - work-queue @r26, @r27 and @r28, delivered by w176, which is done.

## Checks

**Each work-item's check, `python3 -m pytest -q -p work_items --work-item <w>`, which I ran myself at `eca9d404`:**

| Work-item | Result |
|---|---|
| w167 | 144 passed, 1 skipped |
| w168 | 144 passed, 1 skipped |
| w169 | 142 passed, 1 skipped |
| w170 | 146 passed, 1 skipped |
| w171 | 144 passed, 1 skipped |
| w172 | 146 passed, 1 skipped |

w169's line, spec-integration#r43, is a guarantee, so no scenario covers it. Its four instruction files are unchanged since review 3, which read them against the line.

**`tools check --base 4b7dca6c`:**

- **ruff:** fails with 18 errors.
  - Five are i28's (finding 4), the same five as before. One has moved down because of w178's insertion:
    - `scripts/supervise_brief.py:84` ISC004
    - `tests/scenarios/supervision_intake_steps.py:84` FURB167
    - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
    - `tests/scripts/stub_claude.py:186` FURB167
    - `tests/scripts/stub_claude.py:187` FURB167
  - One is new and is i26's: `tests/scenarios/test_supervision.py:14` I001. The import `641f95a9` added is out of order (finding 7).
  - Twelve are in round sessions' helper scripts tracked under `.shop/` (finding 7):
    - i29: `1-gate/mk.py`, `5-apply/splice.py` and `6-formulate/splice.py`;
    - i31: `1-gate/gq.py`.
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none either.

**The other tools:**

- **`tools size --limit 300`:** printed nothing, so no file is over the limit.
- **`features deprecated`:** 4 deprecated scenarios.
  - supervision @r102 is i28's. Its replacement's work-items, w171 and w172, are green (finding 3).
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
  - supervision @r9, @r67 and @r82 are gone. w178 retired them, and they are listed under its `## Retires`.
  - work-queue @r14 is gone too. w176 retired it; see "Removed and weakened tests".
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing i28 touches has a dry-run mode and a real mode of one operation. There is no randomized test to run and no finding.

## Removed and weakened tests

None in i28's commits.

What I searched for:

- **Since review 6:**
  - `git diff f647911b HEAD -- tests` for removed lines. I also searched the added lines for skip, xfail and marks, and found none.
  - The diffs under `features/`.
- **Since review 6, other initiatives' work-items, recorded here; none is i28's:**
  - **w178 (i26), `641f95a9`:**
    - It removes the steps `intake_writes` and `lines_have_outcomes` (with `JUDGED`) from `supervision_intake_steps.py`, and narrows `intake_started`'s step text. These steps bound only the deprecated @r67 outline.
    - It also removes the deprecated scenarios @r9, @r67 and @r82 from `features/supervision.feature`.
    - All three are listed under w178's `## Retires`, and their replacements pass.
  - **w176 (i25), `a2d1083e`:**
    - It removes the deprecated work-queue @r14 outline from `features/work-queue.feature`. w176.md has no `## Retires`.
    - w176's own reviewer raised this as Critical. The coordinator sanctioned it in w176's `## Answers` (2026-10-25): it is the Retires entry of w174, which w176 redrafts.
    - It is not i28's, so it is recorded here and not graded.
- **Over `4b7dca6c..f647911b`:** as reviews 1 to 6 found, nothing was removed or weakened in i28's commits.

## Allowances

I verified each row against its commit:

- **w171, `other_initiative`, setup: holds.** `a414d2bd` changes only the draft's path, adding `round-1/`. It changes no assert, no expected value and no case.
- **w172, `integrate_given_ids`, interim: holds.**
  - The step was first committed in `55eea183`, after Base.
  - `a1ff989a` makes it assert that the ids are on the "Ids drafted elsewhere" line, as plan decision D2 says. It is narrowed, not loosened.
  - The rest of the test diff spells `re.M` as `re.MULTILINE` and changes no behaviour.
- **w167, w168, w169 and w170:** each report gives "none".

## Cannot verify

No check is unverified.

## Findings

### 1. Branch review 1's finding 1: still resolved
- **Where:** `scripts/supervise_brief.py:81-82`, the "Ids drafted elsewhere" line. The file is unchanged since review 6, and w172's check passes.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` starts the initiative of an accepted request that no initiative fulfils, and the row does not say so.
- **Fix:** add to the row "and the start, with `work start`, of the initiative of an accepted request no initiative fulfils (r103)".
- **Triage:** observation. It is unchanged since review 1.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-items are green
- **Where:** `features/supervision.feature`, the deprecated @r102 scenario, with its step `other_initiative` in `tests/scenarios/supervision_integrate_steps.py`.
- **What is wrong:** w171 and w172 are green, and neither has a `## Retires`.
- **Fix:** a work-item that accepts supervision#r102 and retires the scenario, its binding and the step.
- **Triage:** observation.

### 4. Minor, w167, w170 and w172, drop: the 5 ruff errors of i28 under Checks
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:** parenthesize the string at `supervise_brief.py:83-86`, then run `ruff check --fix` on the other three files.
- **Triage:** drop.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item of i28
- **What:** the commits listed under Range.
- **Why it is not more:**
  - The branch is shared by i25 to i31.
  - The commits that change code belong to other initiatives' work-items (w176 and w178 since review 6), and each is reviewed under its own initiative.
  - The rest change no code: queue commands, records, and spec and feature rounds.
- **Triage:** drop.

### 6. Minor, none of i28 (i29), observation: the suite at head is red on scenarios formulated for i29
- **Where:** the 8 scenarios under Suite.
- **What is wrong:** their steps are not written yet. Their work-items are w175, w179 and w181, which are claimed or drafted. This is red-first, not a regression of i28.
- **Fix:** none in i28. Do not merge or release the branch until w175, w179 and w181 are green.
- **Triage:** observation.
- **Reproduction:** `python3 -m pytest -q` at `eca9d404` gives "8 failed, 874 passed". Every `E` line is `StepDefinitionNotFoundError`.

### 7. Minor, none of i28 (i26, i29 and i31), observation: new ruff errors outside i28's code
- **Where:**
  - `tests/scenarios/test_supervision.py:14` I001: `641f95a9`, w178, puts `supervision_request_steps` after `supervision_review_steps`.
  - Round sessions' helper scripts committed under `.shop/work/i29/runs/supervision/{1-gate,5-apply,6-formulate}/` and `.shop/work/i31/runs/supervision/1-gate/`.
- **Fix:**
  - `ruff check --fix tests/scenarios/test_supervision.py`.
  - For the helper scripts, either have `work run` commit only a round's named outputs, or exclude `.shop/` in the ruff configuration.
- **Triage:** observation, for i26, i29 and i31.
- **Reproduction:** `python3 scripts/tools check --base 4b7dca6c` (the ruff section above).

## Shape

- **Size limit:** met. `tools size` prints nothing.
- **Module-map rows:**
  - met for `supervise_brief.py`, `supervise_drafts.py`, `workqueue_answer.py`, `supervise_change.py`, `supervise_draft.py` and `tests/scenarios/`;
  - not met for `supervise_all.py` (finding 2).
- **Code no scenario reaches:** none today. Once finding 3's scenario is retired, nothing will reach `other_initiative`. The check that would show it gone: `features bindings`, and a grep for "whose kept drafts add" that finds nothing.
- **Code no line asks for:** none in i28's commits.
- **Behaviour against the lines and the Purpose:** no contradiction found. I named two risks and verified each:
  - **Risk:** w178's change to `run_all` could drop w170's r103 start.
    - **Verified:** `supervise_all.py:28-35` still checks every unfulfilled request, then starts each, before taking runs. Only the return at the end changed (`asked`, r101). w170's check passes.
  - **Risk:** w176's `asked_by_reviewer` could break w168's `<initiative>/<name>` answer.
    - **Verified:** the split at `workqueue_answer.py:38-40` is unchanged and runs before `asked_by_reviewer`. That function reads the log of the resolved file's own initiative (`path.parent / "log.jsonl"`). w168's check passes.

## Coupling

The branch adds no dependence on another project. Two couplings were there before it:

- **pytest-bdd and pytest 10:** pytest-bdd relies on internals that pytest 10 removes (`PytestRemovedIn10Warning`). Pin `pytest<10` beside pytest-bdd.
- **The `@deprecated` tag:** pytest-bdd treats it as an unregistered mark (`PytestUnknownMarkWarning`). Register `deprecated` under `markers` in `pytest.ini`.

## Observations

Each is carried over from review 6, and I re-read each against head.

- **w168: a capability-proposal's commit subject drops its initiative.** The `name` the split binds is the one used in the commit subject.
  - Reproduction: `git log --oneline --grep='^work answer: supervision$' 4b7dca6c..HEAD` lists commits with that identical subject for i25's, i26's and i29's supervision proposals, for example `1d47a1e9` and `82e1010b`.
- **w170: starting several requests is not atomic.** If `work start` refuses a later request after an earlier one has committed, the earlier initiative stays started.
  - Reproduction: by reading `supervise_all.py:31-33` against `workqueue_start.py`.
- **w171: r102 gives ids that a later round of the same initiative renumbered.** The cost is only skipped ids.
  - Reproduction: i26's kept draft holds supervision r98 and r99, while `d07a8b38` applied r100 and r101.
- **w169: the dispatch templates of `integrating-a-proposal` have no slot for the given ids.**
  - Reproduction: by reading the skill's Template.
- **w168: the refusal for a missing `<initiative>/<name>` file says "work-item", even for a capability-proposal.**
  - Reproduction: `workqueue.py:190`, reached from `workqueue_answer.py`.
- **i26, i29 and i31: tracked helper scripts and an unsorted import fail ruff** (finding 7).
  - Reproduction: the `tools check` output above.
