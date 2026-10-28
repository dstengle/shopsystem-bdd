# Branch review of i50

**Verdict: DONE.** No finding is Critical and none is triaged fix now. Every check has a result from the runs in the brief. One Important finding is an observation for the person to settle at the spec: r131 against r173's "one question". `tools check` exits 1. Its ruff hits are all outside w228's lines: six are in scratch scripts that rounds committed under `.shop/work/i50/runs/`, and three were already in the step files before this branch.

## Range reviewed

- `2c461ed7..837a59ee` on `main`. The base is the commit that added `.shop/work/i50/initiative.md`.
- i50 holds one work-item: **w228** (supervision#r173, `green`). Its file set is `scripts/supervise_glossary.py`, `scripts/supervise_rounds.py` and `tests/scenarios/supervision_proposal_steps.py`.
- Its commits are 829bd273, 2bd22e33, 09c07229, 5773b8b8, c7a1994d, a807b5b7 (the code), a42dfc63 and 837a59ee.
- The range also holds about 245 commits that belong to no work-item. They are the workflow's own commits for i47–i58 and q17–q38: intake, integrate, gate, apply and formulate rounds, notes, answers and starts. Among them are spec and features commits: 78f23fac and 86104ff4 (spec, r173 and r180), and e4e58445 and 6ce69452 (features). See finding 3.

## Suite

`Suite: 1060 passed, 0 failed at 837a59ee in 34.02 s`. The full line is "1060 passed, 1 skipped, 11 xfailed, 8 xpassed, 626 warnings, 56 subtests passed in 34.02s".

- **Parallel:** yes, `-n auto` (xdist).
- **In-process:** no. `tests/scenarios/conftest.py:33` runs each script as `[sys.executable, SCRIPTS/script, …]` in a subprocess.
- The suite is under 60 s, so this is not a finding.
- The 11 xfails are all w212's scenarios in `test_requests.py`, which are expected to fail.
- No dry-run mode exists. I found no `--dry-run` argument or `dry_run` in `scripts/`. `git push --dry-run` is used only inside `work run`'s own push check. So no dry-run/real agreement test is owed.

## Checks

All ran at 837a59ee.

- **w228's scenarios** (`pytest -n auto -p work_items --work-item w228`): exit 0, "182 passed, 1 skipped, 34 warnings, 56 subtests passed in 6.62s". This matches the implementer's report ("182 passed, 1 skipped").
- **`tools check --base 2c461ed7`**: exit 1.
  - **ruff**: 9 errors.
    - Six are SIM115 in `.shop/work/i50/runs/supervision/2-apply/splice.py:1,3,6` and `3-formulate/splice.py:2,3,9`. These are scratch files committed by i50's apply and formulate rounds, not by w228 (finding 4).
    - `tests/scenarios/supervision_integrate_steps.py:87` RUF059 (`commit` unused). This is in `glossary_proposal_written`. The branch changed that file only at lines 22–26, so line 87 was already there.
    - `tests/scenarios/supervision_proposal_steps.py:102` and `:137` RUF100 (unused `noqa: E731`). These are in `drafted_with` and `glossary_proposal_answered`, which the branch did not touch; its hunks are at 9 and 187–194. Already there.
    - None of the nine is in a line w228 wrote.
  - **vulture**: clean.
  - **import-linter**: "the project states no import contracts". This is not `missing`, so there is nothing to read for myself.
- **`tools size`**: exit 0, printed nothing. No file is over the limit. It ran without `--limit 300`, the limit CLAUDE.md states; the default limit gave no output. `supervise_rounds.py` is at about 275 lines after this branch.
- **`features deprecated`**: exit 0. 14 deprecated scenarios, all "for: removal". This branch adds one of them: the r93 scenario in supervision. Its replacement, r180, is to be delivered by i49/w229, which is `drafted`, not green. So it is not a deprecated scenario whose replacement's work-item is green.
- **`features bindings`**: exit 0, "every binding names a scenario".

## Removed and weakened tests

None. I searched the change for:
- deleted `def` lines under `tests/`
- `-` lines in parametrize lists or `Examples` tables
- `-` lines holding `assert`
- added `skip`, `xfail` or `@deprecated` marks
- renamed scenarios

What I found:
- The only `-` line under `tests/` is the import in `supervision_proposal_steps.py:9`, which is widened to add `bullets`.
- The only renamed scenario is r93's. The formulate commit 6ce69452 tagged it `@deprecated` and suffixed its title "(deprecated)". Its steps are unchanged and still bound: `started_fulfilling`, `supervision_integrate_steps.py:18`. It still runs and passes, so it is deprecated, not weakened. It is not in w228's commits, and w228's plan lists "None" under Tests the decisions break, which agrees.

## Allowances

w228's report gives "none" under `## Tests changed under an allowance`. Its commit a807b5b7 changes no existing test; the only test change is one new Then. Nothing to verify.

## Cannot verify

Nothing. Every check the brief requires has a run.

## Findings

1. **Important, w228, observation.** `scripts/supervise_rounds.py:159-162` against supervision r131/r132.
   - **What is wrong:** A glossary gate that gives no question gets exactly one question, r173's. It gets no r131 question naming the missing output. r132 takes "a gate round's questions" as a gate round's output, and the person answered i50's Q2 "reading (a), no change; r131 and r173 both apply" (`.shop/work/i50/supervision.md:23`). The r173 scenario asserts that exactly one question is held (`supervision_proposal_steps.py:191`, `len(held) == 1`), and r173 says "one question". So the lines as answered conflict with each other, and the code follows the scenario.
   - **Why it matters:** The person was told that both lines apply, but `work run` applies only one. r117's capability-gate branch had the same gap before this branch.
   - **Reproduction:** from reading the code. When `asked` is empty at line 159 it is set to `[glossary]`, and no r131 question is added for kind `gate`. Compare the r131 branch for `apply` at lines 181–182.
   - **Fix:** a question to the person (spec, not code). Either r132's last item becomes "a gate round's questions, or none" (Q2 reading b), or r173/r117 are reworded so that the default question is the r131 question. No code change until that is settled.
2. **Minor, w228, observation.** `scripts/supervise_glossary.py:52-55`.
   - **What is wrong:** A glossary-proposal whose `adds`, `changes` and `removes` are all empty gets the question "Are the terms of g1 approved as drafted? It ."
   - **Why it matters:** Nothing writes such a proposal today. The implementer names this case as left open, and the work-item review raised it too.
   - **Reproduction:** from reading the code. `", ".join([])` is `""`.
   - **Fix:** leave out the second sentence when `named` is empty.
   - **Test that would show it:** a unit test of `approval_question` on a glossary-proposal with three empty lists, expecting no "It ." (not run).
3. **Minor, none, observation.** Commits that belong to no work-item.
   - **What is wrong:** Every commit but w228's eight belongs to no work-item. Most are `work` bookkeeping, plus the merges of rounds for i47–i58. Four touch the spec, the features or the tests:
     - 78f23fac (spec r173) and 86104ff4 (spec r180, which retires r93) are the apply rounds' commits.
     - e4e58445 adds the r173 scenario, written by i50's formulate round.
     - 6ce69452 adds the r180 scenario and deprecates r93, written by i49's formulate round. It also adds the step `started_fulfilling_bare` (`tests/scenarios/supervision_integrate_steps.py:22-26`). That file is in no i50 work-item's file set, and w228's commit did not touch it (its review lists three files).
   - **Why it matters:** None of this is a work-item's change. Scenarios and spec lines are the formulate and apply rounds' outputs (r132), so they are not graded as a features change by a work-item. But a step definition written outside any work-item's file set escapes the work-item review.
   - **Fix:** a step definition for a new scenario lands with the work-item that delivers it (here i49/w229), or `work run` records which round's commit it is.
   - **Reproduction:** the brief's `## Commits` (all marked `none`) and `## Change` (the `supervision_integrate_steps.py` hunk).
4. **Minor, none, observation.** `.shop/work/i50/runs/supervision/2-apply/splice.py` and `3-formulate/splice.py`.
   - **What is wrong:** i50's apply and formulate rounds committed throwaway Python scripts into the tracked initiative directory.
   - **Why it matters:** They are tracked Python files, so `tools check` reports them (6 SIM115) and exits 1. `tools size` also counts them.
   - **Reproduction:** the `tools check` run in the brief.
   - **Fix:** rounds write scratch scripts under `.shop/scratch/`, or `tools check` and `tools size` leave out `.shop/`.
5. **Minor, w228, observation.** `scripts/supervise_glossary.py:52`.
   - **What is wrong:** `i[len("term/"):]` cuts five characters off every id, whether or not it starts with `term/`.
   - **Why it matters:** Every writer writes `term/<term>` today (`withheld` and `glossary_only_done` assume the same), so this is hardening only.
   - **Fix:** `i.removeprefix("term/")`.
   - **Reproduction:** from reading the code.
6. **Minor, w228, drop.** `scripts/supervise_glossary.py:55`.
   - **What is wrong:** The r173 question gives no readings, unlike r117's ("Readings: approve … as drafted (recommended), or change its lines"). Under a delegation, an answering session would have no recommended reading to take.
   - **Why it is dropped:** r162 leaves any question that names a glossary-proposal to the person anyway, so this is polish.

## Feature files

- **Deprecated scenarios whose replacement's work-item is green:** none. r93's replacement, r180, is delivered by w229, which is `drafted`.
- **Scenarios removed that were not deprecated:** none. Nothing was removed.
- **Bindings that name no scenario:** none ("every binding names a scenario").
- **Added:** r173 (bound to w228, now passing) and r180 (i49).

## Shape

- **Size limit (300 lines):** met. `tools size` prints nothing. `supervise_rounds.py` grew by one line, to about 275, so the plan's choice to keep the wording in `supervise_glossary.py` holds.
- **Module map, `scripts/supervise_glossary.py`:** the row names withheld terms (r55) and delegation questions (r162). It does not name the new `approval_question` at `supervise_glossary.py:46`, which writes the gate's default question for a glossary-proposal (r173). The module docstring at lines 1–4 does not name it either. The concern fits the module, which reads glossary-proposals. Minor: add "and the question a gate round that gave none writes (r173)" to the row and the docstring. Check that would show it complete: the row and the docstring name r173.
- **Module map, `scripts/supervise*.py` / `supervise_rounds.py`:** met. The gate default stays in `run_round` (`supervise_rounds.py:159-162`), where r117's was.
- **Module map, `tests/scenarios/`:** met. The new Then is in `supervision_proposal_steps.py:187-194`, beside the other g1 steps.
- **Readability (drop):** `supervision_proposal_steps.py:9` now imports `bullets` at module level, while `glossary_proposal_answered` (`:137`) still defines a local lambda `bullets` that shadows it.
- **Unreached code and step definitions:** none found. r93's `started_fulfilling` is still reached by the deprecated r93 scenario until that scenario is removed. After that it is reached only through `started_fulfilling_bare`'s shared helper `proposed_fulfilling`.

## Coupling

- The branch adds no dependency on another project. The new step uses only `pytest_bdd.parsers.re` and `then`, which are published API.
- Already there, not this branch's:
  - pytest-bdd's `compat.py:28` calls pytest's private `_fixturemanager._register_fixture` and `FixtureDef(baseid=…)`. The suite prints 594 `PytestRemovedIn10Warning`s for it, so it will break under pytest 10. What would make it stable: pin pytest below 10, or move to a pytest-bdd release that passes `node`.
  - The `@deprecated` tag becomes `pytest.mark.deprecated`, which is not registered (32 `PytestUnknownMarkWarning`s). Registering the mark in the conftest or ini would make it stable.

## Observations

- r131 against r173: a glossary gate with no question gets only the r173 question (`supervise_rounds.py:159-162`). Reproduction: from reading the code. `asked = [glossary]`, and no r131 question is written for a gate.
- A glossary-proposal with no terms gets "It ." (`supervise_glossary.py:55`). Reproduction: from reading the code. `", ".join([]) == ""`.
- An id not of the form `term/<term>` is cut short (`supervise_glossary.py:52`). Reproduction: from reading the code. `"x"[5:] == ""`.
- A step definition was added outside any work-item (`supervision_integrate_steps.py:22-26`, commit 6ce69452). Reproduction: the brief's Commits and Change.
- Round scratch scripts are committed under `.shop/work/i50/runs/supervision/*/splice.py`. Reproduction: the `tools check` run (exit 1, 6 SIM115).
