# Branch review of i28 (review 8, at 225d3ed2)

**Verdict: DONE.**

- I ran every check of i28's six work-items myself, and each passes.
- No finding is Critical and none is triaged fix now.
- **None of i28's code has changed since review 7 (`eca9d404`).** Seven commits since then touch files outside `.shop/`, and none is i28's:
  - `0c654848` (i29, w179): `supervise_worker.py` keep_named (r15);
  - `959cba20` (i29, w175): `workqueue_request.py`, which refuses an empty delegation (requests r22);
  - spec, feature and merge commits of the i30 and i31 supervision rounds (`d54f006a`, `2f3698be`, `fa05204d`, `6e0b1d9e`, `a30cfe25`).
  - None of them touches `supervise_brief.py`, `supervise_drafts.py`, `supervise_all.py`, `supervise_change.py`, `supervise_draft.py`, `workqueue_answer.py`, or i28's scenarios and steps. `git diff eca9d404 HEAD -- features spec` has no added or removed line that names r92, r102, r103, r104, r30 or r43.
- **The suite at head is red with 19 failures.** Each one is in a scenario that another initiative formulated and whose work-item is not green yet (finding 6).

## Range and work-items

- **Range:** `4b7dca6c..225d3ed2` on `i25-review-findings-to-implementation`.
  - Base `4b7dca6c` is "work: start i28, fulfilling q6".
  - Head `225d3ed2` is "work: w180 ready -> claimed".
- **i28's work-items** (unchanged since review 7):

| Work-item | Status | Accepts | Commits |
|---|---|---|---|
| w167 | green | supervision#r92 | `12f0b295` |
| w168 | green | work-queue#r30 | `fa6929fb` |
| w169 | green | spec-integration#r43 (a guarantee) | `50788670` |
| w170 | green | supervision#r102, r103, r104 | `bcc41527`, `55eea183`, `2e0f2555` |
| w171 | green | supervision#r102 | `a414d2bd` |
| w172 | green | supervision#r102, r103, r104 (fix of branch review 1) | `a1ff989a` |

- **Commits of no i28 work-item:** every other commit in the range (finding 5). Since review 7 these are:
  - w175's and w179's (i29), w180's and w182's to w185's (i30 and i31);
  - the i30 and i31 supervision rounds;
  - branch-review and record commits (`46ee3735`, `11c19108`, `d694050c`, `1cf12c89`, `f7135e20`);
  - answer, note, add and withdraw commits.

## Suite

`Suite: 876 passed, 19 failed at 225d3ed2 in 25.0 s`

- pytest's own line was "19 failed, 876 passed, 1 skipped, 436 warnings, 56 subtests passed in 24.67s". The 25.0 s is the shell's `time` for the whole run.
- **Parallel:** yes, `-n auto` from `pytest.ini`; the run used 1484 % CPU.
- **In-process:** no. The step definitions run `work` and the other commands as subprocesses.
- The suite takes under 60 s, so its wall time is no finding.
- **The 19 failures:**
  - 18 are `StepDefinitionNotFoundError`:
    - i29's w181 (claimed): r105 to r109, including "an initiative set done is committed";
    - i30's w184 (drafted): r110 and r117, the branch review restarted after a fix work-item;
    - i31's w185 (drafted): r111 to r116 and the reformulated r83 (formulate, gate and apply rounds, and the kept drafts' path).
  - 1 is an `AssertionError`: "a researcher is given … a limit of 80 turns" (r19, i30). The code still passes `--max-turns 40`. Its work-item, w180, is claimed.
  - None of them is an i28 scenario.
- **Passing now that failed at review 7:** requests @r22 (w175, green) and supervision @r15 (w179, green).

## Checks

**Each work-item's check, `python3 -m pytest -q -p work_items --work-item <w>`, which I ran myself at `225d3ed2`:**

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

- **ruff:** fails with 29 errors.
  - Five are i28's (finding 4), the same five at the same lines as review 7:
    - `scripts/supervise_brief.py:84` ISC004
    - `tests/scenarios/supervision_intake_steps.py:84` FURB167
    - `tests/scenarios/supervision_proposal_steps.py:96` RUF100
    - `tests/scripts/stub_claude.py:186` FURB167
    - `tests/scripts/stub_claude.py:187` FURB167
  - One is i26's: `tests/scenarios/test_supervision.py:14` I001 (finding 7).
  - Twenty-three are in round sessions' helper scripts tracked under `.shop/` (finding 7):
    - i29: `1-gate/mk.py`, `5-apply/splice.py` and `6-formulate/splice.py`;
    - i30: `3-formulate/splice.py`, which is new;
    - i31: `1-gate/gq.py`, with `2-apply/apply.py` and `3-formulate/splice.py`, both new.
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none either.

**The other tools:**

- **`tools size --limit 300`:** printed nothing, so no file is over the limit.
- **`features deprecated`:** 6 deprecated scenarios.
  - supervision @r102 is i28's. Its replacement's work-items, w171 and w172, are green (finding 3).
  - supervision @r19 (i30) and @r83 (i31) are newly deprecated. Their replacements' work-items are not green.
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing i28 touches has a dry-run mode and a real mode of one operation. There is no randomized test to run, and no finding.

## Removed and weakened tests

None in i28's commits.

What I searched for since review 7:

- `git diff eca9d404 HEAD -- tests features` for removed lines. It has 4, and each belongs to a deprecation:
  - the `@r19` tag line and its scenario title, each re-added with `@deprecated` and a "Deprecated for:" line (i30, `2f3698be`);
  - the same for `@r83` (i31, `a30cfe25`).
  - Neither is i28's.
- The added test lines, for skip, xfail and marks. The only hit is the word "remark" in `supervision_given.py:208`, which is not a mark.

Over `4b7dca6c..eca9d404`, reviews 1 to 7 found nothing removed or weakened in i28's commits, and none of those commits has changed since.

## Allowances

Unchanged since review 7, and verified against the commits then:

- **w171, `other_initiative`, setup: holds.** `a414d2bd` changes only the draft's path, adding `round-1/`. It changes no assert, no expected value and no case.
- **w172, `integrate_given_ids`, interim: holds.**
  - The step was first committed in `55eea183`, after Base.
  - `a1ff989a` makes it assert the ids on the "Ids drafted elsewhere" line, as plan decision D2 says.
- **w167, w168, w169 and w170:** each report gives "none".

## Cannot verify

None. I ran every check myself.

## Findings

### 1. Branch review 1's finding 1: still resolved
- **Where:** `scripts/supervise_brief.py:81-82`, the "Ids drafted elsewhere" line.
- **Evidence:** the file is unchanged since review 6, and w172's check passes.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` also starts the initiative of an accepted request that no initiative fulfils, and the row does not say so.
- **Fix:** add to the row "and the start (`work start`) of the initiative of an accepted request no initiative fulfils (r103)".
- **Triage:** observation.

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
- **What:** the branch is shared by i25 to i31.
- **Why it is not more:**
  - The commits that change code belong to other initiatives' work-items (w175 and w179 since review 7), and each is reviewed under its own initiative.
  - The rest change no code: queue commands, records, and spec and feature rounds.
- **Triage:** drop.

### 6. Minor, none of i28 (i29, i30 and i31), observation: the suite at head is red on other initiatives' scenarios
- **Where:** the 19 failures under Suite.
- **What is wrong:** they are red-first scenarios whose work-items are claimed or drafted: w181, w180, w184 and w185. They are not a regression of i28.
- **Fix:** none in i28. Do not merge or release the branch until those work-items are green.
- **Reproduction:** `python3 -m pytest -q -rfE` at `225d3ed2` gives "19 failed, 876 passed". 18 `E` lines are `StepDefinitionNotFoundError`. The last asserts `--max-turns 80` against `40`.
- **Triage:** observation.

### 7. Minor, none of i28 (i26, i29, i30 and i31), observation: ruff errors outside i28's code
- **Where:**
  - `tests/scenarios/test_supervision.py:14` I001, from w178 (i26);
  - the round helper scripts committed under `.shop/work/i29`, `i30` and `i31/runs/supervision/`. This review counts 23 errors in them, up from 12.
- **Fix:**
  - `ruff check --fix tests/scenarios/test_supervision.py`;
  - for the helper scripts, either have `work run` commit only a round's named outputs, or exclude `.shop/` in the ruff configuration.
- **Reproduction:** `python3 scripts/tools check --base 4b7dca6c`.
- **Triage:** observation.

## Shape

- **Size limit:** met. `tools size` prints nothing.
- **Module-map rows:**
  - met for `supervise_brief.py`, `supervise_drafts.py`, `workqueue_answer.py`, `supervise_change.py`, `supervise_draft.py` and `tests/scenarios/`;
  - not met for `supervise_all.py` (finding 2).
- **Code no scenario reaches:** none today. Once finding 3's scenario is retired, nothing will reach `other_initiative`. The check that would show it gone: `features bindings`, and a grep for "whose kept drafts add" that finds nothing.
- **Code no line asks for:** none in i28's commits.
- **Behaviour against the lines and the Purpose:** no contradiction found. The risk I named for this review:
  - **Risk:** the i30 and i31 feature edits, and w179's change to `supervise_worker.py`, could alter i28's r92 and r102 to r104 scenarios or the integrate brief.
  - **Verified:**
    - the diff since `eca9d404` names none of those ids in `features/` or `spec/`;
    - the change to `supervise_worker.py` is confined to `keep_named` (lines 233-238);
    - w167, w170, w171 and w172's checks pass at head.

## Coupling

The branch adds no dependence on another project. Two couplings were there before it:

- **pytest-bdd and pytest 10:** pytest-bdd relies on internals that pytest 10 removes (`PytestRemovedIn10Warning`). Pin `pytest<10` beside pytest-bdd.
- **The `@deprecated` tag:** pytest-bdd treats it as an unregistered mark (`PytestUnknownMarkWarning`). Register `deprecated` under `markers` in `pytest.ini`.

## Observations

These are carried over from review 7 and still hold at head:

- **w168: a capability-proposal's commit subject drops its initiative.**
  - Reproduction: `git log --oneline --grep='^work answer: supervision$' 4b7dca6c..HEAD` gives identical subjects across i25, i26, i29 and i30.
- **w170: starting several requests is not atomic.** If `work start` refuses a later request after an earlier one committed, the earlier initiative stays started.
  - Reproduction: read `supervise_all.py:31-33` against `workqueue_start.py`.
- **w171: r102 gives ids that a later round of the same initiative renumbered.** The cost is only skipped ids.
  - Reproduction: i26's kept draft has r98 and r99, while `d07a8b38` applied r100 and r101.
- **w169: the dispatch templates of `integrating-a-proposal` have no slot for the given ids.**
  - Reproduction: read the skill's Template.
- **w168: the refusal for a missing `<initiative>/<name>` file says "work-item", even for a capability-proposal.**
  - Reproduction: `workqueue.py:190`, reached from `workqueue_answer.py`.
- **i26, i29, i30 and i31: tracked helper scripts and an unsorted import fail ruff** (finding 7).
