# Branch review of i28 (review 9, at ce37512e)

**Verdict: DONE.**

- I ran every check of i28's six work-items myself, and each passes.
- No finding is Critical and none is triaged fix now.
- **None of i28's own commits has changed since review 8 (`225d3ed2`).** 49 commits followed it. Two of them change i28's modules and tests, and one more touches an i28 step's setup. All three belong to other initiatives' work-items, and I verified each against i28's lines (Shape, "Risks"):
  - `bd765f03` (i27, w187): `supervise_change.py` merges the change-list entries that name one capability into one proposal. It also adds `tests/scripts/test_supervise_change.py`.
  - `4d3113e1` and `5048b72e` (i29, w181): `supervise_change.py` gains `unknown` (r107) and `kept_path` (r108), and `supervise_brief.py` gains the gate and apply "Drafts path:" line (r108).
  - `d87a295b` (i29, w181): the r92 change-list Given (`integrate_with_changes`, first committed by w167) now commits `spec/capabilities/other.md` first. This is setup only.
- **The suite at head is red with 10 failures.** All 10 are `StepDefinitionNotFoundError` in scenarios of i31's w185, which is drafted (finding 6). None is i28's.

## Range and work-items

- **Range:** `4b7dca6c..ce37512e` on `i25-review-findings-to-implementation`, 407 commits.
  - Base `4b7dca6c` is "work: start i28, fulfilling q6".
  - Head `ce37512e` is "work: w180 ready -> claimed".
- **i28's work-items** (unchanged since review 8):

| Work-item | Status | Accepts | Commits |
|---|---|---|---|
| w167 | green | supervision#r92 | `12f0b295` |
| w168 | green | work-queue#r30 | `fa6929fb` |
| w169 | green | spec-integration#r43 (a guarantee) | `50788670` |
| w170 | green | supervision#r102, r103, r104 | `bcc41527`, `55eea183`, `2e0f2555` |
| w171 | green | supervision#r102 | `a414d2bd` |
| w172 | green | supervision#r102, r103, r104 (fix of branch review 1) | `a1ff989a` |

- **Commits of no i28 work-item:** every other commit in the range (finding 5). Since review 8 these are:
  - code commits of w181 (i29), w184 and w180 (i30) and w187 (i27);
  - the q9 intake round;
  - i29's measurement and analysis records;
  - branch-review records (`d7fbec01`, `fd46e0aa`, `ae2c017f`, `3738a8da`, `aac08dc8`);
  - queue commands.

## Suite

`Suite: 885 passed, 10 failed at ce37512e in 58.2 s`

- pytest's own line was "10 failed, 885 passed, 1 skipped, 434 warnings, 56 subtests passed in 57.71s". The 58.2 s is the shell's `time`.
- **Parallel:** yes, `-n auto` from `pytest.ini`; the run used 732 % CPU.
- **In-process:** no. The step definitions run `work` and the other commands as subprocesses.
- The suite takes under 60 s, so its wall time is no finding. It is close to the limit, though: review 8 took 25.0 s on the same suite size. That is most likely load on the host, since the CPU share fell from 1484 % to 732 %.
- **The 10 failures:** all are `StepDefinitionNotFoundError`, in supervision @r83 (the reformulated one), @r111, @r112, @r113, @r114, @r115 (4 outline rows) and @r116.
  - Every one of them is accepted by i31's w185, which is drafted.
  - None is an i28 scenario.
- **Passing now that failed at review 8:** r105 to r109 (w181, green), r110, r117 and the 80-turn r19 (w184, green).

## Checks

**Each work-item's check, `python3 -m pytest -q -p work_items --work-item <w>`, which I ran myself at `ce37512e`:**

| Work-item | Result |
|---|---|
| w167 | 145 passed, 1 skipped |
| w168 | 145 passed, 1 skipped |
| w169 | 143 passed, 1 skipped |
| w170 | 147 passed, 1 skipped |
| w171 | 145 passed, 1 skipped |
| w172 | 147 passed, 1 skipped |

w169's line, spec-integration#r43, is a guarantee, so no scenario covers it. None of its four instruction files has changed since review 3, which read them against the line. I confirmed this with `git log 225d3ed2..HEAD` on those paths, which lists no commit.

**`tools check --base 4b7dca6c`:**

- **ruff:** fails with 32 errors.
  - **Four are on lines i28 added** (finding 4):
    - `scripts/supervise_brief.py:89` ISC004, the "Ids drafted elsewhere" list item of w172. It sat at :84 before i29's r108 lines were added above it.
    - `tests/scenarios/supervision_intake_steps.py:84` FURB167 (w170, `bcc41527`)
    - `tests/scenarios/supervision_proposal_steps.py:118` RUF100 (w170, `2e0f2555`). It sat at :96 before i29's steps were added above it.
    - `tests/scripts/stub_claude.py:189` FURB167 (w167, `12f0b295`)
  - **A correction to reviews 1 to 8:** `tests/scripts/stub_claude.py:190` FURB167 is not i28's. `git blame` gives `6e6d3143`, an ancestor of Base, so it was already there before the branch, in a file i28 touched.
  - **Three are new since review 8, and none is i28's** (finding 7):
    - `scripts/supervise_analysis.py:4` I001 (i29, w181, `c482f4f8`: the `git` added to the `supervise_worker` import);
    - `tests/scenarios/supervision_all_steps.py:127` RUF007 (i27, w187, `bd765f03`);
    - `tests/scripts/test_supervise_change.py:7` RUF100 (i27, w187, `bd765f03`).
  - **The rest are not i28's** (finding 7):
    - i26's `tests/scenarios/test_supervision.py:14` I001;
    - 23 errors in round helper scripts tracked under `.shop/work/i29`, `i30` and `i31`, the same as review 8.
- **vulture:** clean.
- **import-linter:** "the project states no import contracts". `CLAUDE.md` states none either.

**The other tools:**

- **`tools size --limit 300`:** printed nothing and exited 0, so no file is over the limit.
- **`features deprecated`:** 5 deprecated scenarios.
  - supervision @r102 is i28's. Its replacement's work-items, w171 and w172, are green (finding 3).
  - supervision @r83 is i31's. Its replacement is accepted by w185, which is drafted.
  - migration-tools @r15 and work-queue @r1 and @r9 were there before the branch.
  - The deprecated @r19 that review 8 listed was removed by w184 (i30, `cd134f29`), which retired it, and its 80-turn replacement passes. It is not i28's.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** nothing i28 touches has a dry-run mode and a real mode of one operation. There is no randomized test to run, and no finding.

## Removed and weakened tests

None in i28's commits.

What I searched for since review 8:

- `git diff 225d3ed2 HEAD -- tests` for removed lines. There are 10, none in i28's commits, and none removes an assertion:
  - `supervision_all_steps.py` (w187, i27, r95):
    - `linger` raised from 1 to 3;
    - `re.M` written out as `re.MULTILINE`;
    - `strict=False` added to a `zip`;
    - a comment added to the `sorted`.
  - `supervision_proposal_steps.py` (w184, i30, r110): `reviewer_lists` now gives two results, the second "lists nothing", for the second review. Its asserts are unchanged.
  - `supervision_rounds_steps.py` (w184, r117): the `questions_hold` pattern is narrowed to a quoted text, so that the new approval step does not collide with it. The assertion is unchanged.
  - `test_supervision.py` (w181 or w184): `is_green` is narrowed from `{name}` to `w\d+`. The assertion is unchanged.
  - Import lines of the two step modules (`calls` and `supervision_done_steps` added).
  - The signature of `integrate_with_changes`, the r92 step w167 first committed (`d87a295b`, i29, w181). `repo` is added and so is a setup commit of `spec/capabilities/other.md`, because r107 now refuses a capability nothing has. It changes no assert, no expected value and no case, and the r92 scenario still asserts a proposal for both thing and other (w167's check passes).
- `git diff 225d3ed2 HEAD -- features`: the only removed lines are the deprecated @r19 scenario, retired by w184 (i30). It is not i28's.
- The added test lines, searched for `skip`, `xfail` and `mark.`: there are no hits.

Over `4b7dca6c..225d3ed2`, reviews 1 to 8 found nothing removed or weakened in i28's commits, and none of those commits has changed since.

## Allowances

Unchanged since review 8, and verified against the commits then:

- **w171, `other_initiative`, setup: holds.** `a414d2bd` changes only the draft's path, adding `round-1/`. It changes no assert, no expected value and no case.
- **w172, `integrate_given_ids`, interim: holds.**
  - The step was first committed in `55eea183`, after Base.
  - `a1ff989a` makes it assert the ids on the "Ids drafted elsewhere" line, as plan decision D2 says.
- **w167, w168, w169 and w170:** each report gives "none".

## Cannot verify

None. I ran every check myself.

## Findings

### 1. Branch review 1's finding 1: still resolved
- **Where:** `scripts/supervise_brief.py:85-87`, the "Ids drafted elsewhere" line. i29's r108 insert moved it down 5 lines.
- **Evidence:** the text is unchanged, and w172's check passes.

### 2. Minor, w170, observation: the module-map row of `supervise_all.py` does not name r103
- **Where:** `CLAUDE.md:30`, against `scripts/supervise_all.py:18-35`.
- **What is wrong:** `run_all` also starts the initiative of an accepted request that no initiative fulfils, and the row does not say so. The row is unchanged by w187's edit of `CLAUDE.md`.
- **Fix:** add to the row "and the start (`work start`) of the initiative of an accepted request no initiative fulfils (r103)".
- **Triage:** observation.

### 3. Minor, w171, observation: the deprecated @r102 scenario remains, though its replacement's work-items are green
- **Where:** `features/supervision.feature`, the deprecated @r102 scenario, with its step `other_initiative` in `tests/scenarios/supervision_integrate_steps.py`.
- **What is wrong:** w171 and w172 are green, and neither has a `## Retires`.
- **Fix:** a work-item that accepts supervision#r102 and retires the scenario, its binding and the step. w184 did this for @r19.
- **Triage:** observation.

### 4. Minor, w167, w170 and w172, drop: the 4 ruff errors of i28 under Checks
- **Why it matters:** `tools check` fails on ruff. No behaviour changes.
- **Fix:**
  - parenthesize the string in the list at `supervise_brief.py:85-91`;
  - run `ruff check --fix` on `supervision_intake_steps.py`, `supervision_proposal_steps.py` and `stub_claude.py`. In `stub_claude.py` this also fixes the error at :190, which was there before the branch.
- **Triage:** drop.

### 5. Minor, none (initiative-level), drop: commits that belong to no work-item of i28
- **What:** the branch is shared by i25 to i31.
- **Why it is not more:**
  - The commits that change code belong to other initiatives' work-items (w180, w181, w184 and w187 since review 8), and each is reviewed under its own initiative.
  - The rest change no code: queue commands, intake, records, and spec and feature rounds.
- **Triage:** drop.

### 6. Minor, none of i28 (i31), observation: the suite at head is red on another initiative's scenarios
- **Where:** the 10 failures under Suite.
- **What is wrong:** they are i31's red-first scenarios (r83, r111 to r116), all accepted by w185, which is drafted. They are not a regression of i28.
- **Fix:** none in i28. Do not merge or release the branch until w185 is green.
- **Reproduction:** `python3 -m pytest -q -rfE` at `ce37512e` gives "10 failed, 885 passed". Every `E` line is `StepDefinitionNotFoundError`.
- **Triage:** observation.

### 7. Minor, none of i28 (i26, i27, i29, i30 and i31), observation: ruff errors outside i28's code
- **Where:**
  - `tests/scenarios/test_supervision.py:14` (i26);
  - `scripts/supervise_analysis.py:4` (i29, w181);
  - `tests/scenarios/supervision_all_steps.py:127` and `tests/scripts/test_supervise_change.py:7` (i27, w187);
  - 23 errors in round helper scripts tracked under `.shop/work/i29`, `i30` and `i31/runs/supervision/`.
- **Fix:**
  - `ruff check --fix` on the four code files;
  - for the helper scripts, either have `work run` commit only a round's named outputs, or exclude `.shop/` in the ruff configuration.
- **Reproduction:** `python3 scripts/tools check --base 4b7dca6c`.
- **Triage:** observation.

## Shape

- **Size limit:** met. `tools size` prints nothing.
- **Module-map rows:**
  - met for `supervise_brief.py`, `supervise_drafts.py`, `workqueue_answer.py`, `supervise_change.py` (still "one drafted capability-proposal for each capability it names", which w187's merge now makes exact), `supervise_draft.py` and `tests/scenarios/`;
  - not met for `supervise_all.py` (finding 2).
- **Code no scenario reaches:** none today. Once finding 3's scenario is retired, nothing will reach `other_initiative`. The check that would show it gone: `features bindings`, and a grep for "whose kept drafts add" that finds nothing.
- **Code no line asks for:** none in i28's commits.
- **Behaviour against the lines and the Purpose:** no contradiction found. The risks I named for this review, each with what I verified:
  - **Risk:** w187's merge in `write_proposals` (`supervise_change.py:61-65`) could drop an id that r92 says the proposal carries.
    - **Verified:** the merge unions each field and keeps first-named order. `tests/scripts/test_supervise_change.py` asserts `adds: [thing#r3, thing#r4]` and the `removes` of the second entry. r92 asks for "a drafted capability-proposal for each capability the change list names", so one proposal per capability is the line, not a departure from it.
  - **Risk:** r107's `unknown` could refuse the capabilities of a change list that r92 must write.
    - **Verified:** `unknown` admits any capability in `spec/capabilities/` or in a kept draft `drafts/round-*/spec/capabilities/` of the stage. r107 is the line that refuses the rest. The r92 scenario's setup now commits `other` (setup only, see Removed and weakened tests), and w167's check passes.
  - **Risk:** r108's `kept_path` changes the sentence "The drafts of this proposal are in …" in a way r102's reader of kept drafts depends on.
    - **Verified:** `supervise_drafts.py` is unchanged since review 8. It globs `runs/<i>/*-integrate/drafts/round-*/spec/capabilities/*.md` and does not read the sentence. w170's, w171's and w172's checks pass.
  - **Risk:** the r108 "Drafts path:" insert in `supervise_brief.py:47-51` alters the r104 gate question line or the r102 integrate ids line.
    - **Verified:** it is added after the r104 block, for the `gate` and `apply` stages only. The integrate branch at :85-87 is unchanged, and w170's and w172's checks pass.

## Coupling

The branch adds no dependence on another project. Two couplings were there before it:

- **pytest-bdd and pytest 10:** pytest-bdd relies on internals that pytest 10 removes (`PytestRemovedIn10Warning`, 402 warnings in this run). Pin `pytest<10` beside pytest-bdd.
- **The `@deprecated` tag:** pytest-bdd treats it as an unregistered mark (`PytestUnknownMarkWarning`). Register `deprecated` under `markers` in `pytest.ini`.

## Observations

These are carried over from review 8 and still hold at head:

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
- **i26, i27, i29, i30 and i31: tracked helper scripts and code lines outside i28 fail ruff** (finding 7).
- **Suite wall time:** 58.2 s at this review against 25.0 s at review 8, with the same tests and half the CPU share. If it goes over 60 s on an idle host, the suite needs a reason in `CLAUDE.md` or a faster run.
  - Reproduction: `time python3 -m pytest -q`.
