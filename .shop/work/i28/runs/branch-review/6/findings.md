# Branch review of i28 (review 6, at f647911b)

**Verdict: DONE.**

- Every check of i28's six work-items passes, and I ran each one myself.
- No finding is Critical and none is triaged fix now.
- **None of i28's code has changed since review 5 passed at `c6673e6a`.** Three commits since then touch files outside `.shop/`, and none is i28's:
  - **`b6c4feb1` (i25, w173, supervision r98):** adds `findings_lines` to `scripts/supervise_brief.py:88-103` and calls it for the implement stage at `:58-59`.
    - The code r102 and w172 put in, `integrate_lines` at `:73-86`, is unchanged; only its line numbers moved down by 2.
    - w170 and w172's checks still pass.
  - **`db4d07f2` (i26, w177):** adds `work ask` and `work reply`, rewrites the `CLAUDE.md` row for `workqueue_request.py`, and retires requests @r4, @r5 and @r12. Those three are all listed under w177's `## Retires`.
  - **`7fed86a0` (a formulate commit):** adds the supervision @r15 scenario for i29's w179, which is still drafted.
- **The suite at head is red with 11 failures**, down from 16. Every one is a `StepDefinitionNotFoundError` in a scenario another initiative formulated, and each has a work-item of that initiative that is not green yet (finding 6). None is i28's.
- What remains for i28 is the Minor items carried over from earlier reviews: the 5 ruff errors, the `supervise_all.py` module-map row and the deprecated @r102 scenario.

## Range and work-items

- **Range:** `4b7dca6c..f647911b` on `i25-review-findings-to-implementation`, 234 commits.
  - Base `4b7dca6c` is "work: start i28, fulfilling q6", the commit that added i28's `initiative.md`.
  - Head `f647911b` is "work: i31 proposed -> started".
- **i28's work-items and their commits**, unchanged since review 5:

| Work-item | Status | Accepts | Commits |
|---|---|---|---|
| w167 | green | supervision#r92 | `12f0b295` |
| w168 | green | work-queue#r30 | `fa6929fb` |
| w169 | green | spec-integration#r43, a guarantee | `50788670` |
| w170 | green | supervision#r102, r103, r104 | `bcc41527`, `55eea183`, `2e0f2555` |
| w171 | green | supervision#r102, the fix of w170's task review | `a414d2bd` |
| w172 | green | the fix of branch review 1 | `a1ff989a` |

- **Commits that belong to no work-item of i28** (finding 5):
  - those reviews 3 to 5 listed;
  - since `c6673e6a`, 45 more:
    - w173's commits (i25), including `b6c4feb1`;
    - w177's commits (i26), including `db4d07f2`;
    - the formulate commit `7fed86a0`;
    - the branch-review records `9b97d347` (i27) and `7f06c81c` (i28);
    - the merges `9127b86a` and `4b923353`;
    - `d365c763`, the answer sessions' records;
    - queue, answer and note commands of i25, i26, i29 and i30;
    - q8's outcomes, turn and intake;
    - `9839b05a` and `f647911b`, which start i31.

## Suite

`Suite: 873 passed, 11 failed at f647911b in 26.9 s`

pytest's own line was "11 failed, 873 passed, 1 skipped, 406 warnings, 56 subtests passed in 26.64s". The 26.9 s is the shell's `time` for the whole run.

- **Parallel:** yes. `pytest.ini` has `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions run `work` and the other commands as subprocesses.
- Under 60 s, so the wall time is no finding.
- **The 11 failures**, each a `StepDefinitionNotFoundError`:

| Scenario | Delivered by | Its status |
|---|---|---|
| requests @r22 | i29, w175 | researched |
| supervision @r9 | i26, w178 | researched |
| supervision @r101 | i26, w178 | researched |
| supervision @r67 (two examples) | i26, w178 | researched |
| supervision @r100 | i26, w178 | researched |
| supervision @r82 | i26, w178 | researched |
| supervision @r15, new in `7fed86a0` | i29, w179 | drafted |
| work-queue @r26, @r27 and @r28 | i25, w176 | drafted |

- **Passing now that failed at review 5:**
  - requests @r4, @r5, @r12, @r20 and @r21, delivered by w177, which is green;
  - supervision @r98, delivered by w173, which is done.

## Checks

**Each work-item's check, `python3 -m pytest -q -p work_items --work-item <w>`, which I ran myself at `f647911b`:**

| Work-item | Result |
|---|---|
| w167 | 144 passed, 1 skipped |
| w168 | 144 passed, 1 skipped |
| w169 | 142 passed, 1 skipped |
| w170 | 146 passed, 1 skipped |
| w171 | 144 passed, 1 skipped |
| w172 | 146 passed, 1 skipped |

w169's spec-integration#r43 is a guarantee, so no scenario covers it. The four instruction files that carry it have not changed since review 3, which read them against the line.

**`tools check --base 4b7dca6c`:**

- **ruff:** fails with 7 errors, the same 7 as review 5.
  - Five are i28's (finding 4). One has moved down by 2 lines because of w173's insertion:
    - `scripts/supervise_brief.py:84` ISC004
    - `tests/scenarios/supervision_intake_steps.py:65` FURB167
    - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
    - `tests/scripts/stub_claude.py:186` FURB167
    - `tests/scripts/stub_claude.py:187` FURB167
  - Two are i29's (finding 7):
    - `.shop/work/i29/runs/supervision/1-gate/mk.py:1` I001
    - `.shop/work/i29/runs/supervision/1-gate/mk.py:15` SIM115
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none either.

**The other tools:**

- **`tools size --limit 300`:** printed nothing, so no file is over the limit.
- **`features deprecated`:** 8 deprecated scenarios.
  - supervision @r102 is i28's. Its replacement's work-items, w171 and w172, are green (finding 3).
  - These come from other initiatives' formulate rounds, and their replacements wait for work-items that are not green:
    - supervision @r9, @r67 and @r82: w178;
    - work-queue @r14: w176.
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
  - requests @r4, @r5 and @r12 are gone. w177 retired them, and they are listed under its Retires.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing i28 touches has a dry-run mode and a real mode of one operation. There is no randomized test to run and no finding.

## Removed and weakened tests

None in i28's commits.

What I searched for:

- **Since review 5, `git diff c6673e6a HEAD -- tests`:** additions only, in `requests_write_steps.py` (w177) and `supervision_answers_steps.py` (w173). No line is removed, and no skip, xfail or mark is added.
- **Under `features/` since review 5:**
  - The only removed lines are the three deprecated requests scenarios @r4, @r5 and @r12. They were removed by w177's `db4d07f2`, they are listed under w177's `## Retires`, and their replacements pass.
  - `features bindings` is clean afterwards.
  - The only other change is the scenario `7fed86a0` adds.
- **Over `4b7dca6c..c6673e6a`:** as review 5 found, no assertion, parametrize case, skip or xfail was removed or added.

## Allowances

The commits behind these are unchanged since review 3:

- **w171, `other_initiative`, setup: holds.** `a414d2bd` changes only the draft's path, adding `round-1/`. It changes no assert, no expected value and no case.
- **w172, `integrate_given_ids`, interim: holds.** The step was first committed in `55eea183`, after Base, and now asserts plan decision D2.
- **w167, w168, w169 and w170:** each report gives "none".

## Cannot verify

No check is unverified.

## Findings

### 1. Branch review 1's finding 1: still resolved
- **Where:** `scripts/supervise_brief.py:81-82`, the line of ids drafted elsewhere. It was at `:79-80` before w173's insertion.
- **What I verified:** the line is unchanged, and w172's check passes.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` starts the initiative of an accepted request that no initiative fulfils, and the row does not say so.
- **Fix:** add "and the start, with `work start`, of the initiative of an accepted request no initiative fulfils (r103)" to the row.
- **Triage:** observation. It is unchanged since review 1.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-item is green
- **Where:** `features/supervision.feature:1312`, the deprecated @r102 scenario, with its step `other_initiative` (`tests/scenarios/supervision_integrate_steps.py`).
- **What is wrong:** w171 and w172 are green, and neither has a `## Retires`.
- **Fix:** a work-item accepting supervision#r102 that retires the scenario, its binding and the step.
- **Triage:** observation.

### 4. Minor, w167, w170 and w172, drop: the 5 ruff errors of i28 under Checks
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:** parenthesize the string at `supervise_brief.py:83-86`, then run `ruff check --fix` on the other three files.
- **Triage:** drop.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item of i28
- **What:** the commits listed under Range.
- **Why it is not more:**
  - This branch is shared by i25, i26, i27, i28, i29, i30 and i31.
  - Most of those commits are code-free: queue commands, records, and spec and feature rounds.
  - The ones that change code are other initiatives' work-items (w173 and w177), and each is reviewed under its own initiative.
- **Triage:** drop.

### 6. Minor, none of i28 (i25, i26 and i29), observation: the suite at head is red on scenarios formulated for other initiatives
- **Where:** the 11 scenarios listed under Suite.
- **What is wrong:** their steps are not written yet. This is the red-first state of in-flight work, not a regression of i28.
- **Who delivers them:** each has a delivering work-item of its own initiative, shown in the Suite table: w175, w176, w178 and w179.
- **Fix:** none in i28. Do not merge or release this branch until those work-items are green.
- **Triage:** observation.
- **Reproduction:** `python3 -m pytest -q` at `f647911b` gives "11 failed, 873 passed". Each failure's `E` line is `StepDefinitionNotFoundError`.

### 7. Minor, none of i28 (i29), observation: a gate session's helper script is tracked and fails ruff
- **Where:** `.shop/work/i29/runs/supervision/1-gate/mk.py`.
- **What is wrong:** it is unchanged since review 5, and `tools check` still reports I001 and SIM115 on it.
- **Fix:** either have `work run` commit only a run's named outputs, or exclude `.shop/` in the ruff configuration.
- **Triage:** observation, for i29 or i30.
- **Reproduction:** `python3 scripts/tools check --base 4b7dca6c`.

## Shape

- **Size limit:** met. `tools size` prints nothing.
- **Module-map rows:**
  - met for `supervise_brief.py`, `supervise_drafts.py` (`CLAUDE.md:32`), `workqueue_answer.py`, `supervise_change.py`, `supervise_draft.py` and `tests/scenarios/`;
  - not met for `supervise_all.py` (finding 2).
  - w177 brought the `workqueue_request.py` row up to date with `ask` and `reply`. That row is not i28's.
- **Code no scenario reaches:** none today. Once finding 3's scenario is retired, `other_initiative` is reached by nothing. The check that would show it gone: `features bindings`, and a grep for "whose kept drafts add" that finds nothing.
- **Code no line asks for:** none in i28's commits.
- **Behaviour against the lines and the Purpose:** no contradiction found.
  - **The risk I named:** w173's change to `Briefs.write` could alter the briefs that r102 and r104 shape.
  - **What I verified:** at `supervise_brief.py:58-59`, `findings_lines` is called only when `stage == "implement"`. The integrate-round lines at `:73-86` and the gate lines at `:43-46` are as i28 left them, and w170 and w172's checks pass.

## Coupling

The branch adds no dependence on another project. Two couplings were there before it:

- **pytest-bdd and pytest 10:** pytest-bdd relies on internals that pytest 10 removes (`PytestRemovedIn10Warning`). Pin `pytest<10` beside pytest-bdd.
- **The `@deprecated` tag:** pytest-bdd treats it as an unregistered mark (`PytestUnknownMarkWarning`). Register `deprecated` under `markers` in `pytest.ini`.

## Observations

- **w168: a capability-proposal's commit subject drops the initiative.**
  - `workqueue_answer.py:30` rebinds `name` before `:56` and `:58` use it.
  - Reproduction: `git log --oneline --grep='^work answer: supervision$' 4b7dca6c..HEAD` lists 19 commits with the identical subject "work answer: supervision". They are for capability-proposals named supervision in i25, i26 and i29; `056ba39a` and `134a84a8` are two of them.
- **w170: a start of several requests is not atomic.** If `work start` refuses a later request after an earlier one has committed, the earlier initiative stays started.
  - Reproduction: by reading `supervise_all.py:31-35` against `workqueue_start.py:25-33`.
- **w171: r102 gives ids that a later round of the same initiative renumbered.** The cost is only skipped ids.
  - Reproduction: i26's kept draft holds supervision r98 and r99, while `d07a8b38` applied r100 and r101.
- **w169: `integrating-a-proposal`'s dispatch templates have no slot for the given ids.**
  - Reproduction: by reading the skill's Template.
- **w168: the refusal for a missing `<initiative>/<name>` file says "work-item" even for a capability-proposal.**
  - Reproduction: `workqueue.py:190`, reached from `workqueue_answer.py:37`.
- **i29: `mk.py` is tracked and fails ruff** (finding 7).
  - Reproduction: the `tools check` output above.
