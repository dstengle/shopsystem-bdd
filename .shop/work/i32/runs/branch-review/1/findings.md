# Branch review of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.** One finding is Important and triaged fix now (w190: `work run` crashes with a KeyError on a reviewer's work-item whose delegated answer was already committed). Nothing is Critical. Every work-item's named check passes. Two things cannot be verified in this review (see Cannot verify).

## Range and work-items

- Range: `d3d3839d..7ede38b8` (base `work: start i32, fulfilling q9`, head `work: w190 done -> green`).
- **w189** (review#r31, under review, group guarantees): one commit, `ee81efd0` (`agents/bdd-branch-reviewer.md`). It lies between `6fa7dc00 work: w189 ready -> claimed` and `72e77945 work: w189 claimed -> done`.
- **w190** (supervision#r118, r119): two commits between `2c448d35 work: w190 ready -> claimed` and `0a9226a6 work: w190 claimed -> done`:
  - `6622133a`: steps, `tests/scenarios/supervision_delegation_steps.py`;
  - `31c86e3c`: `scripts/supervise_answers.py`, `scripts/workqueue_answer.py`.
  - The first claim, `fc76d519..12897d9b`, holds only w189's `ee81efd0`, from the pool running both side by side. Its own `c5561011` was carried forward as `6622133a`.
- Commits that belong to no work-item: the capability-proposal rounds' commits. These are `cb357911` (spec review#r31), `57be6d74` (spec supervision r118, r119, decision 0069), `bc00efae` (features r118, r119) and `f33c07a6` (the apply round's stage directory, including `apply.py`), plus `work note` and `work` status commits. See finding 3.

## Suite

`Suite: 887 passed, 10 failed at 7ede38b in 22.4 s` (and 1 skipped, 56 subtests passed). Command: `python3 -m pytest -q -p no:cacheprovider`.

- **Parallel:** yes, `-n auto` from `pytest.ini`, with 32 workers.
- **In-process:** no. `tests/scenarios/test_supervision.py:71` runs `scripts/work` as a subprocess. The suite is under 60 s, so this is no finding.
- **The 10 failures:** all are `StepDefinitionNotFoundError` in `features/supervision.feature`, in scenarios this branch did not touch. The branch only appends lines 1457-1474. They are exactly the 10 that `work run`'s suite record lists as `expected` in `.shop/work/i32/runs/w190/5-implement/brief.md`. They are other initiatives' unimplemented scenarios: r83's replacement (i31 w185, drafted), r111-r116, r70 and others. This branch did not cause them.

## Checks

- **w189's check, `python3 -m pytest -q tests/scripts/test_agents.py`:** 8 passed, 18 subtests passed.
- **w189's plan check on r31, `measure` of a later initiative:** not runnable here (see Cannot verify). The agent text itself was read: `agents/bdd-branch-reviewer.md:74,76` say what r31 and plan decisions 1-3 ask.
- **w190's check, `python3 -m pytest -q --work-item w190`:** 145 passed, 1 skipped, 56 subtests passed. This includes the r118 and r119 scenarios.
- **`tools check --base d3d3839d` (exit 1):**
  - **ruff:** 6 errors.
    - 5 are in `.shop/work/i32/runs/supervision/3-apply/apply.py` (SIM115 ×3, PIE810, RUF015), a run record committed in `f33c07a6`. See finding 4.
    - 1 is FURB167 at `tests/scenarios/supervision_delegation_steps.py:171`. It is already in the base file (line 144 of `2c448d35`). See finding 5.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". I read the module map for myself (see Shape).
- **`tools size --limit 300`:** prints nothing. No file is over 300 lines. The touched files have 142, 77 and 202 lines.
- **`features deprecated`:** 5 deprecated scenarios, none of them added or changed by this branch:
  - migration-tools @r15;
  - supervision @r83: its replacement is accepted by i24 w137 (**green**) and i31 w185 (drafted);
  - supervision @r102: its replacement is accepted by i28 w171 (**green**);
  - work-queue @r1;
  - work-queue @r9.

  A deprecated scenario whose replacement's work-item is green stays for @r83 and @r102. Neither is this branch's, so I name them as already there.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of an operation of its own (`git push --dry-run` in `supervise_review.py:41` and `supervise_faults.py:67` is git's). No randomized agreement test applies.

## Removed and weakened tests

None. I searched `git diff d3d3839d HEAD -- tests features` for:
- removed lines (`^-`): none;
- `skip`, `xfail` and `parametrize` in the test diff: none.

The test diff adds three steps to `supervision_delegation_steps.py`. The features diff adds two scenarios (@r118, @r119) to `supervision.feature`, formulated by the supervision proposal's formulate round (`bc00efae`), not by a work-item.

## Allowances

Every implementer report gives `## Tests changed under an allowance: none` (w189 3-implement, w190 3-implement and w190 5-implement). The commits agree: no existing test changed.

## Cannot verify

- **review#r31 on a real batch.** It is a guarantees capability with no scenario. The plan names `measure` of a later initiative as its check. I verified the agent text, not a run's result.
- **That a real `delegation-answerer` session gives the `verdict` field.** The scenarios use the stand-in. `agents/delegation-answerer.md` does not mention `verdict`; only the brief's `VERDICT` sentence (`scripts/supervise_answers.py:17`) asks for it. A session that omits it leaves the question for the person (line 120), so the failure is safe but would stall a delegated run.

## Findings

### 1. Important, w190, fix now: `work run` crashes with KeyError on a reviewer's work-item whose answer is already written
- **Where:** `scripts/supervise_answers.py:83` (`self.verdicts[name]`), commit `31c86e3c`.
- **What is wrong:** `self.verdicts` is reset at line 68 and filled only by `ask()` in the same run. Take an awaiting-answer work-item asked by its reviewer whose every question already has an answer, but which is still awaiting-answer. Line 79 commits each answer before the move at line 86 ("kept now"), so a run stopped between the two leaves exactly this state. In that state the question loop never runs, `open_questions` is `[]`, and line 83 raises `KeyError`. Every later `work run` crashes the same way. The person cannot answer an item with no open question either. Before `31c86e3c` this state moved to `done` through `asked_from`.
- **Reproduction:** a probe scenario run with the suite's own harness. Given the delegation, the reviewer's question step of `6622133a`, an `## Answers` bullet committed, and the `accept` stand-in, then `work run i1`. It gave rc 1, with stderr `File "scripts/supervise_answers.py", line 83, in answers ... KeyError: 'w1'`, and w1 still `awaiting-answer`.
- **Why it matters:** this is a crash where a refusal, or leaving the question for the person, belongs. `work run` stops with a traceback on state it wrote itself.
- **Fix:** with no verdict from this run (`self.verdicts.get(name) is None`), make no move and leave the item for the person (r77/r89), or refuse naming the work-item. Better, keep the verdict with the answer (in the bullet or the log) so that a later run can move it.
- **Keep as a test:**
  ```
  Given i1 fulfils the request q1, which gives the delegation "Please get everything delivered. Do not stop to ask me questions or permission."
  And i1's work-item w1 is awaiting-answer on its reviewer's question "Is the old reader kept?", with no answer
  And w1's question already has the answer an earlier run committed
  And the session answering under the delegation answers "Yes, keep it as it is.", an answer that accepts the work-item as it is, and every worker gives DONE
  When the person runs `work run i1`
  Then `work run` does not end in a traceback, and w1 is left for the person or refused, naming w1
  ```
  The new step appends `\n## Answers\n\n- 2026-10-25: Yes, keep it as it is.\n  by: work run, under the delegation\n` to w1.md and commits it.

### 2. Minor, w190, drop: the second implement result lists no commit
- **Where:** `.shop/work/i32/runs/w190/5-implement/result.json`.
- **What is wrong:** it gives `"commits": ["see git log"]` and not `31c86e3c`. I verified the commits from the history. The task review raised this already.

### 3. Minor, no work-item, drop: commits outside every work-item
- **What:** `cb357911`, `57be6d74`, `bc00efae` and `f33c07a6` change `spec/` and `features/`, outside any claim. They are the integrate, apply and formulate rounds of the two capability-proposals, which supervision r91 and r96 call for, and each is named in the ledger. They are expected, not stray, and need no fix.

### 4. Minor, no work-item (the supervision apply round), observation: `tools check` fails on a committed run record
- **Where:** `.shop/work/i32/runs/supervision/3-apply/apply.py:3-13`, committed in `f33c07a6`.
- **What is wrong:** the apply round's throwaway script is tracked, and `tools check --base` lints it. That gives 5 of the 6 ruff errors, so the check exits 1 for every review of this branch.
- **Reproduction:** `python3 <Scripts>/tools check --base d3d3839d` printed `apply.py:3:5: SIM115 … apply.py:13:1: SIM115`.
- **Fix:** have the check skip `.shop/`, or have rounds not leave `.py` files in their stage directories.

### 5. Minor, w190 (file touched, error already there), observation: FURB167 `re.M`
- **Where:** `tests/scenarios/supervision_delegation_steps.py:171`. It was already at line 144 before the branch.
- **Reproduction:** `tools check` printed `171:103: FURB167 [*] Use of regular expression alias re.M`.
- **Fix:** `re.MULTILINE`.

### Checked, no finding
- **w189:**
  - `agents/bdd-branch-reviewer.md:74` gives in `questions` only fix-now findings (r31).
  - Line 76: `NEEDS_CONTEXT` puts its reason in `summary` and leaves `questions` empty (r28, r31).
  - The `status` rule is unchanged (r6, 0040).
  - No other file changed; the frontmatter is unchanged.
- **w190 against r118, r119 and 0069:**
  - It finds a reviewer's question by the log (`asked_by_reviewer`, the same reading `work answer` uses).
  - `change` goes to `ready` and `accept` goes to `done`, through the one helper `workqueue_answer.reviewer_status` (`workqueue_answer.py:31`), which `work answer` (line 58) uses as well.
  - r78's `by` is unchanged.
- **No verdict leaves the question for the person** (`supervise_answers.py:120`). This serves r77's "leaves it for the person otherwise" and 0069 (no guard holds), so it is not code no line asks for.
- **Decision 0069** supersedes 0063's one row only. 0063 stays `accepted` and its rest stands, as 0069 says.

## Shape

- **Size rule (300 lines):** met. 142, 77, 202 and 76 lines; `tools size` prints nothing.
- **Module map, `scripts/supervise_answers.py` ("`work run`'s answers under a request's delegation"):** met. The verdict-driven move is at `supervise_answers.py:80-86`.
- **Module map, `scripts/workqueue_answer.py` (`work answer`):** met. `reviewer_status` at `workqueue_answer.py:31` is `work answer`'s rule, shared and not copied.
- **Module map, `tests/scenarios/`, one `<capability>_*_steps.py` a concern:** met. The delegation steps are in `supervision_delegation_steps.py:56-80`.
- **`agents/`:** not a row of the map. It is a prompt file and no code.
- **Unreached code or steps:** none. vulture is clean, and `features bindings` says every binding names a scenario.
- **Observation, no refactor needed:** `asked_by_reviewer` is read three times for one question (lines 82, 104, 119), each reading the log again. Computing it once per item in `answers()` and passing it on would be complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / the delegation-answerer session:** the new behaviour relies on the session writing a `verdict` field, which only the brief asks for. If the model omits it or misspells it, the question goes to the person: safe, but the delegation stops helping. Naming `verdict` in `agents/delegation-answerer.md`'s result section would make it stable.
- **pytest-bdd:** the steps use only its public `given`/`then`/`parsers.re`. The warnings about `_register_fixture` and `FixtureDef` come from pytest-bdd's own compat layer and were already there.
- **ruff, vulture, import-linter:** used through `tools check`. Nothing new relies on more than their CLI.

## Observations

- `tools check` lints run records: `python3 <Scripts>/tools check --base d3d3839d` reports 5 ruff errors in `.shop/work/i32/runs/supervision/3-apply/apply.py` (finding 4).
- FURB167 already in the base: `tools check` reports `tests/scenarios/supervision_delegation_steps.py:171:103` (finding 5).
- Deprecated scenarios whose replacement's work-item is green, outside this branch: `features deprecated` lists supervision @r83 (i24 w137 green) and @r102 (i28 w171 green).
