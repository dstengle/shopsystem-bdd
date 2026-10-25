# Branch review of i28 (review 5, at c6673e6a)

**Verdict: DONE.**

- Every check of i28's six work-items passes, and I ran each one myself.
- No finding is Critical and none is triaged fix now.
- **No code, test or step definition has changed since review 4 passed at `125b2ad1`.** `git diff --stat 125b2ad1 HEAD -- . ':!.shop'` touches only three files:
  - `features/requests.feature`
  - `features/supervision.feature`
  - `spec/capabilities/requests.md`

  The commits behind them are other initiatives' spec and formulate rounds:
  - `7c548d23` and `6cd77b2b`: requests r22, for i29;
  - `46fef129`: supervision r98, r100, r101, r9, r67 and r82, for i25 and i26.
- **The suite at head is red with 16 failures.** Every one is a `StepDefinitionNotFoundError` in a scenario that another initiative formulated (finding 6). None is i28's.
- What remains of i28 is the Minor carried over from earlier reviews: the 5 ruff errors, the module-map row and the deprecated @r102 scenario.

## Range and work-items

- **Range:** `4b7dca6c..c6673e6a` on `i25-review-findings-to-implementation`, 189 commits. Head is `c6673e6a` ("work: q8 intake round 1-intake ended").
- **i28's work-items and their commits:**

| Work-item | Accepts | Commits |
|---|---|---|
| w167 | supervision#r92 | `12f0b295` |
| w168 | work-queue#r30 | `fa6929fb` |
| w169 | spec-integration#r43, a guarantee | `50788670` |
| w170 | supervision#r102, r103, r104 | `bcc41527`, `55eea183`, `2e0f2555` |
| w171 | supervision#r102, the fix of w170's task review | `a414d2bd` |
| w172 | the fix of branch review 1 | `a1ff989a` |

- **Commits that belong to no work-item of i28** (finding 5):
  - those that reviews 3 and 4 listed;
  - since `125b2ad1`:
    - spec and feature rounds: `7c548d23` and `6cd77b2b` (i29, requests r22), and `46fef129` (supervision);
    - merges `8038d315`, `56cda243` and `cab9306a`;
    - branch-review records `5fc387ed` and `3d533646`;
    - observation records `409627b7` and `99346b49`;
    - `986dbcbb`, which renames proposal ids by hand;
    - queue commands of i25, i26, i29 and i30;
    - q8's request, outcomes and turn;
    - `4fbc25cd`, which starts i30.

## Suite

`Suite: 870 passed, 16 failed at c6673e6a in 31.8 s`

pytest's own line was "16 failed, 870 passed, 1 skipped, 404 warnings, 56 subtests passed in 31.35s".

- **Parallel:** yes. `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions run `work` and the other commands as subprocesses.
- Under 60 s, so the wall time is no finding.
- **The 16 failures**, each a `StepDefinitionNotFoundError`:
  - `features/requests.feature`: @r4, @r5, @r12, @r20 and @r21 (i26), and @r22 (i29);
  - `features/supervision.feature`: @r9, @r101, @r100, @r98, @r67 (two examples) and @r82 (i25 and i26);
  - `features/work-queue.feature`: @r26, @r27 and @r28 (i25).

## Checks

**Each work-item's check, `python3 -m pytest -q -p work_items --work-item <w>`, which I ran myself at `c6673e6a`:**

| Work-item | Result |
|---|---|
| w167 | 144 passed, 1 skipped |
| w168 | 144 passed, 1 skipped |
| w169 | 142 passed, 1 skipped |
| w170 | 146 passed, 1 skipped |
| w171 | 144 passed, 1 skipped |
| w172 | 146 passed, 1 skipped |

w169's spec-integration#r43 is a guarantee, so no scenario covers it. The four instruction files that carry it are unchanged since review 3, which read them against the line.

The real queue now shows r43 and r102 at work:

- i29's kept requests draft numbers its line r22, above i26's r20 and r21, and spec apply `7c548d23` used r22.
- i29's kept supervision draft uses r105 to r108, above i26's r100 and r101.

**`tools check --base 4b7dca6c`:**

- **ruff:** fails with 7 errors.
  - Five are the same as in reviews 2 to 4, all i28's (finding 4):
    - `scripts/supervise_brief.py:82` ISC004
    - `tests/scenarios/supervision_intake_steps.py:65` FURB167
    - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
    - `tests/scripts/stub_claude.py:186` FURB167
    - `tests/scripts/stub_claude.py:187` FURB167
  - Two are new and not i28's (finding 7):
    - `.shop/work/i29/runs/supervision/1-gate/mk.py:1` I001
    - `.shop/work/i29/runs/supervision/1-gate/mk.py:15` SIM115
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none either.

**The other tools:**

- **`tools size --limit 300`:** printed nothing and exited 0, so no file is over the limit.
- **`features deprecated`:** 11 deprecated scenarios.
  - supervision @r102 is i28's. Its replacement's work-items, w171 and w172, are green (finding 3).
  - These come from other initiatives' formulate rounds, and their replacements wait for work-items that are not green yet:
    - requests @r4, @r5 and @r12;
    - supervision @r9, @r67 and @r82;
    - work-queue @r14.
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing i28 touches has a dry-run mode and a real mode of one operation. There is no randomized test to run and no finding.

## Removed and weakened tests

None in i28's commits.

What I searched for over `4b7dca6c..HEAD`:

- **Removed test lines**, from `git diff 4b7dca6c HEAD -- tests | grep '^-'`. There are seven, and none is an assertion or a parametrize case:
  - three import lines;
  - the field regex at `re.M`, rewritten;
  - the stub's docstring line;
  - the stub's heading regex, widened.
- **Skips, xfails and marks added:** `grep -E '^\+.*(skip|xfail|mark\.)'` over the same diff finds none.
- **Under `features/`:** the only removed lines are the old tag and title lines of these scenarios:
  - requests @r4, @r5 and @r12;
  - supervision @r9, @r67 and @r82;
  - work-queue @r14.

  Each is re-added with `@deprecated` and "(deprecated)" by a formulate commit, not a work-item. `features deprecated` lists each one. i28's own @r102 deprecation (`7636eb12`, a formulate commit) also keeps the old scenario.
- **Since review 4:** nothing under `tests/` changed.

## Allowances

The commits behind these are unchanged since review 3:

- **w171, `other_initiative`, setup: holds.** `a414d2bd` changes only the draft's path, adding `round-1/`. It changes no assert, no expected value and no case.
- **w172, `integrate_given_ids`, interim: holds.** The step was first committed in `55eea183`, after Base, and now asserts plan decision D2.
- **w167, w168, w169 and w170:** each report gives "none".

## Cannot verify

No check is unverified.

## Findings

### 1. Branch review 1's finding 1: still resolved
- **Where:** `scripts/supervise_brief.py:79`.
- **What I verified:** the line is unchanged, and w172's check passes.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` starts the initiative of an accepted request that no initiative fulfils, and the row does not say so.
- **Fix:** add "and the start, with `work start`, of the initiative of an accepted request no initiative fulfils (r103)" to the row.
- **Triage:** observation. It is unchanged since review 1.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-item is green
- **Where:** `features/supervision.feature`, the deprecated @r102 scenario, with its step `other_initiative` (`tests/scenarios/supervision_integrate_steps.py:157-167`).
- **What is wrong:** w171 and w172 are green, and neither has a `## Retires`.
- **Fix:** a work-item accepting supervision#r102 that retires the scenario, its binding and the step.
- **Triage:** observation.

### 4. Minor, w167, w170 and w172, drop: the 5 ruff errors under Checks
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:** parenthesize the string at `supervise_brief.py:81-83`, then run `ruff check --fix` on the other three files.
- **Triage:** drop.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item of i28
- **What:** the commits listed under Range.
- **Why it is not more:**
  - This branch is shared by i25, i26, i27, i28, i29 and i30.
  - The code-free kinds land on whatever branch is checked out (work-queue r9): queue commands, records, and the spec and feature rounds.
  - None of them changes code or tests.
- **Triage:** drop.

### 6. Minor, none of i28 (i25, i26 and i29), observation: the suite at head is red on scenarios formulated for other initiatives
- **Where:** the 16 scenarios listed under Suite.
- **What is wrong:** their steps are not written yet. This is the red-first state of in-flight work, not a regression of i28.
- **Who delivers them:**
  - **i25:** w176 (drafted) now accepts work-queue r14, r26, r27 and r28, so review 4's note about r28 is answered. w173 (researched) accepts supervision r98.
  - **i29:** w175 (awaiting-answer) accepts requests r22.
  - **i26:** has no work-item yet for requests r4, r5, r12, r20 and r21, or for supervision r9, r67, r82, r100 and r101.
- **Fix:** none in i28. Do not merge or release this branch until those work-items are green.
- **Triage:** observation.
- **Reproduction:** `python3 -m pytest -q` at `c6673e6a` gives "16 failed, 870 passed". Each failure's `E` line is `StepDefinitionNotFoundError`.

### 7. Minor, none of i28 (i29), observation: a gate session's helper script is tracked and fails ruff
- **Where:** `.shop/work/i29/runs/supervision/1-gate/mk.py`, committed with the run directory by `5540f7d4` ("work: supervision drafted -> awaiting-answer").
- **What is wrong:**
  - The gate session wrote a Python script to build its result file, and `work run` committed it with the run's records.
  - `tools check` now reports I001 and SIM115 on it.
  - The size limit and lint rules cover every tracked Python file.
- **Why it matters:** `tools check` stays red for a file no one maintains.
- **Fix:** either have `work run` commit only a run's `brief.md`, `result.json`, `session.json` and its named outputs, or exclude `.shop/` in the ruff configuration.
- **Triage:** observation, for i29 or i30.
- **Reproduction:** `python3 scripts/tools check --base 4b7dca6c`, then `git log -- .shop/work/i29/runs/supervision/1-gate/mk.py`.

## Shape

Unchanged since review 4, because no code changed:

- **Size limit:** met.
- **Module-map rows:**
  - met for `supervise_brief.py`, `supervise_drafts.py` (`CLAUDE.md:32`), `workqueue_answer.py`, `supervise_change.py`, `supervise_draft.py` and `tests/scenarios/`;
  - not met for `supervise_all.py` (finding 2).
- **Code no scenario reaches:** none today. Once finding 3's scenario is retired, `other_initiative` is reached by nothing. The check that would show it gone: `features bindings`, and a grep for "whose kept drafts add" that finds nothing.
- **Code no line asks for:** none.
- **Behaviour against the lines and the Purpose:** no contradiction found. The real queue agrees:
  - **r103:** `4fbc25cd` ("work: start i30, fulfilling q7") started i30 for the accepted q7, which no initiative fulfilled.
  - **r102:** all six kept drafts on the queue sit under `runs/<i>/<n>-integrate/drafts/round-1/spec/capabilities/`, the layout `kept_drafts` globs, and i29's ids avoided i26's (see Checks).
  - **New lines since review 4:** supervision r9, r82 and r101 change `work run`'s exit, for i26. They do not touch r103's start in `supervise_all.py`, and their delivery is i26's.

## Coupling

The branch adds no dependence on another project. Two couplings were there before it:

- **pytest-bdd and pytest 10:** pytest-bdd relies on internals that pytest 10 removes (`PytestRemovedIn10Warning`, `_pytest/fixtures.py:1986`). Pin `pytest<10` beside pytest-bdd.
- **The `@deprecated` tag:** pytest-bdd treats it as an unregistered mark (`PytestUnknownMarkWarning`). Register `deprecated` under `markers` in `pytest.ini`.

## Observations

- **w168: a capability-proposal's commit subject drops the initiative.**
  - `workqueue_answer.py:30` rebinds `name` before `:56` and `:58` use it.
  - Reproduction: `git show --stat 056ba39a 134a84a8` gives the same subject "work answer: supervision" for i25's and i26's `supervision.md`.
- **w170: a start of several requests is not atomic.** If `work start` refuses a later request after an earlier one has committed, the earlier initiative stays started.
  - Reproduction: by reading `supervise_all.py:31-35` against `workqueue_start.py:25-33`.
- **w171: r102 gives ids that a later round of the same initiative renumbered.** The cost is only skipped ids.
  - Reproduction: i26's kept draft holds supervision r98 and r99, while `d07a8b38` applied r100 and r101.
- **w169: `integrating-a-proposal`'s dispatch templates have no slot for the given ids.**
  - Reproduction: by reading the skill's Template.
- **w168: the refusal for a missing `<initiative>/<name>` file says "work-item" even for a capability-proposal.**
  - Reproduction: `workqueue.py:190`, reached from `workqueue_answer.py:37`.
- **i29: `mk.py` is tracked and fails ruff** (finding 7).
  - Reproduction: `tools check` output above.
