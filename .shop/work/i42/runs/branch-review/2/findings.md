# Branch review 2 of i42

**Verdict: DONE.** There is no Critical finding and nothing is triaged fix now. Every check a work-item names was run here and passed. The suite's 11 failures are w212's parked requests scenarios (initiative i39), which this branch does not touch. One probe could not be run (see Cannot verify); what it would have shown was checked by reading the code.

## Range reviewed

`8f90ad3e..7ac8eb59`, 60 commits. Base `8f90ad3e` is the commit that adds `.shop/work/i42/initiative.md`.

- **w213** (spec-integration#r46, green): the commits from `6de25e87` (ready -> claimed) to `53d57591` (claimed -> done). Its one commit of its own is `5482e7e3`. Branch review 1 (`.shop/work/i42/runs/branch-review/1/findings.md`) reviewed it, and those findings are carried forward below.
- **w214** (supervision#r149-r153, green): the commits from `13faa004` (ready -> claimed) to `9c34d167` (claimed -> done). Its one commit of its own is `2b4cbe78`. That commit touches:
  - agents/initiative-round.md
  - features/supervision.feature (the Retires removal)
  - scripts/supervise_brief.py
  - scripts/supervise_outputs.py
  - scripts/supervise_rounds.py
  - tests/scenarios/supervision_formulate_steps.py
  - tests/scenarios/supervision_reintegrate_steps.py
- **Commits outside any work-item:**
  - the rounds `work run` started: `356ac0f4` and `83361ea7` (apply, spec/ only), and `6c1dca8d` and `0b2f17e0` (formulate, features/ only);
  - `333fba50` (branch review 1, .shop/ only);
  - `4afb2e48` (measure and analysis record, .shop/records only);
  - every other commit is a `work …` commit of `work run`.

  See finding 1.

## Suite

Suite: 1020 passed, 11 failed at 7ac8eb59 in 30.08 s (also 1 skipped, 56 subtests passed).

- **Command:** `python3 -m pytest -q -p no:cacheprovider`. The time is pytest's own wall time.
- **Parallel:** yes. pytest.ini has `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions run `work run` as a subprocess. The suite is under 60 s, so that is no finding.
- **The 11 failures:** all are in tests/scenarios/test_requests.py. They are the scenarios of i39's w212, which is parked: plain pytest marks them no xfail, and only `--whole-suite` does. The i39 ledger already records this. None of the failures is of spec-integration or supervision.

## Checks

- **w213's check (its scenario, r46):** `python3 -m pytest -q --work-item w213` gives 177 passed, 1 skipped.
- **w214's check (its scenarios, r149-r153):** `python3 -m pytest -q --work-item w214` gives 181 passed, 1 skipped.
- **`tools check --base 8f90ad3e…`:**
  - **ruff:** 12 errors, so it fails. None of them is in code a work-item wrote:
    - 10 are in `.shop/work/i42/runs/supervision/5-apply/apply.py` and `6-formulate/splice.py`. These are helper scripts the apply and formulate rounds committed (`2c410087`, `1e71da84`). See finding 2.
    - 2 are in `tests/scenarios/supervision_reintegrate_steps.py`: `:13` (an unused import of `git`) and `:174` (`re.M`). Both lines are present at Base. w214 touched the file and left them. See finding 3.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". Nothing is missing.
- **`tools size --limit 300`:** no output, so no file is over the limit. The largest touched files are supervise_rounds.py (265 lines), supervise_brief.py (212), supervision_reintegrate_steps.py (175) and supervise_outputs.py (103).
- **`features deprecated`:** 11, all "for: removal". None was added by this branch, and the @r140 scenario that 0b2f17e0 deprecated was removed by w214. Pre-existing: @r117's replacement r121 is green but @r117 is still there (i39).
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** the system has no dry-run mode of an operation of its own. The only `--dry-run` uses are `git push --dry-run` reachability probes. No randomized test is called for.

## Removed and weakened tests

- **The one removal:** `git diff 8f90ad3e HEAD -- tests features` shows 3 deletions, all in features/supervision.feature. Commit by commit, they are:
  - `0b2f17e0` (formulate round): it tags `@r140` as `@deprecated`, "Deprecated for:" the r150 scenario.
  - `2b4cbe78` (w214): it removes that deprecated scenario. The same steps live on in the new @r150 scenario, which is word for word the old body. w214's Retires lists it, and test_supervision.py had no binding for it.
- **Nothing else:**
  - no test function was deleted;
  - no parametrize case or Examples row was dropped;
  - no assert was removed or loosened;
  - no skip or xfail was added;
  - no step text was changed.

  The step modules only gain lines.
- **Plans:** both plans list "Tests the decisions break: None". w214's plan names r46's scenario as still passing under decision 2, and it does.

## Allowances

Both reports give "Tests changed under an allowance: none". The commits agree: no existing test was changed.

## Cannot verify

- **The scratch probe of `supervise_outputs.sent_back` and `Rounds.route` was not run.** The probe covered `unheld_answers` beside `changes`, the `approved` route, and a string `unheld_answers`. The sandbox asks for approval to run a script, which this session cannot give, and the probe has been deleted. I checked the same cases by reading `supervise_outputs.py:29-56` and `supervise_rounds.py:55-80`. No work-item names this as a check, so it fails no check.
- **Whether real `initiative-round` sessions give `unheld_answers` and `nothing_formulated` correctly.** The scenarios use stand-ins. This is a guarantees capability (design-decision/workflow-capabilities-are-guarantees), measured on real batches.

## Findings

1. **Minor. No work-item: the rounds' commits `356ac0f4`, `83361ea7`, `6c1dca8d` and `0b2f17e0`. Triage: drop.**
   - **What is wrong:** these commits belong to no work-item. `0b2f17e0` changes features/supervision.feature: it adds r149-r153 and deprecates r140.
   - **Why it does not matter:** these are the apply and formulate rounds `work run` starts, the only writers of spec/ and of feature files (design-decision/the-context-runs-without-a-coordinator). The change under features/ is not a work-item's, so it is not the Critical case.
2. **Minor. No work-item: the supervision rounds' committed helpers `.shop/work/i42/runs/supervision/5-apply/apply.py` and `6-formulate/splice.py`. Triage: observation.**
   - **What is wrong:** the tracked Python files a round leaves in its stage directory fail ruff (10 errors). So `tools check` is red for files no work-item owns.
   - **Why it matters:** a red check that is always red hides a new red. This is pre-existing practice (i29, i30 and others have the same files), and the i39 ledger notes it.
   - **Fix:** exclude `.shop/` in ruff's configuration, or have rounds keep helpers in `.shop/scratch/`.
   - **Reproduction:** `python3 <Scripts>/tools check --base 8f90ad3e` gives "Found 12 errors."
3. **Minor. w214: tests/scenarios/supervision_reintegrate_steps.py:13 and :174. Triage: drop.**
   - **What is wrong:** the file has 2 pre-existing ruff errors (an unused import of `git`, and `re.M`). w214 touched the file and left them.
   - **Fix:** a two-token change, for the next work on that file.
4. **Minor. w214: tests/scenarios/supervision_reintegrate_steps.py:90-94 (`awaiting_when_formulate_ended`). Triage: observation (carried from w214's review).**
   - **What is wrong:** `assert not moved or moved[-1]["after"] == "awaiting-answer"` passes with no move logged. The file check rules out only `status: formulated`.
   - **Why it matters:** nothing goes wrong today, because r152's second Then catches any move.
   - **Fix:** assert `status: awaiting-answer` in p1.md.
5. **Minor. w214: scripts/supervise_rounds.py:59 with scripts/supervise_outputs.py:53-56. Triage: observation.**
   - **What is wrong:** the widening of r150 to a partial apply (`unheld_answers` beside `changes`, the proposal `approved`, then integrate) is reached by no scenario. The @r150 scenario drives only `nothing_applied`. Branch review 1's r46 scenario (spec_integration_apply_steps.py) gives `unheld_answers` beside `changes`. Since w214, `work run` in that scenario goes on to an integrate round. The stand-in has no plan for it, so the run ends in r96's error, and r46's Thens still hold (plan §4).
   - **Why it matters:** the path r151 exists for (a partial apply goes to integrate, not to formulate) is checked only by reading.
   - **What I read:**
     - `route` sends `approved` to `("integrate", "drafted")` when `sent_back`.
     - `sent_back` pops trailing `-integrate` stages, then judges the latest apply or formulate result.
     - After a successful integrate the proposal is `drafted` (r142), so `route`'s check is not reached, and no loop follows.
     - A full apply (no `unheld_answers`) still routes to formulate.
   - **Fix:** a formulate round for a scenario of r150/r151 with a partial apply.
6. **Minor. w214: agents/initiative-round.md:36. Triage: observation.**
   - **What is wrong:** the apply contract still ends "`work run` keeps the result as you give it". Since w214, a non-empty `unheld_answers` also makes `work run` start an integrate round (r150), as the line beside it says for `nothing_applied`.
   - **Why it matters:** the round is not told the consequence of the field. That can matter to a round deciding whether a loosely held answer is "unheld".
   - **Fix:** append "`work run` then starts an integrate round for the proposal."
7. **Minor. w214: scripts/supervise_brief.py:26. Triage: drop (carried from w214's review).**
   - **What is wrong:** `UPSTREAM =re.compile` lost a space.
   - **Why it matters:** it is noise, with no behaviour.
8. **Minor. w213: scripts/supervise_brief.py:82. Triage: observation (carried from branch review 1, finding 3).**
   - **What is wrong:** `UNHELD_ANSWERS` is given to every apply brief, including one with no `## Answers`.
   - **Why it matters more now:** since w214 a non-empty `unheld_answers` sends the proposal back to integrate.
   - **Fix:** guard it with `if self.answer_lines(name):`, as `ANSWER_LINES` is guarded.

Branch review 1's finding 4 ("unheld_answers has no reader") is closed by w214: `supervise_outputs.sent_back` reads it.

**Code no line asks for:** none.
- `sent_back`, `formulated_nothing`, the formulate short-circuit (`supervise_rounds.py:173-176`) and `NOTHING_FORMULATED` serve r149-r153.
- The `approved` branch of `route` serves r150/r151.
- The brief and agent text is their prompt.
- The one edit without a line is the whitespace of finding 7.

**Behaviour against lines and Purpose:** no contradiction found. What I checked:
- **r83 and r131/r132:** they still run when `nothing_formulated` is absent or a question is given (`supervise_rounds.py:173-183`).
- **r152:** `commit(name, before, before)` keeps the status from `approved` and from `awaiting-answer`.
- **r116:** an awaiting-answer proposal whose formulate round asked still routes to formulate, because the latest formulate result gives questions and so `sent_back` is false.
- **r147:** `gives_nothing` is unchanged in substance, moved to `supervise_outputs.py`.

## Shape

- **CLAUDE.md, size limit:** met. Every touched file is ≤ 300 lines; supervise_rounds.py went from 267 to 265 by moving its readers out.
- **Module map, `scripts/supervise_outputs.py` ("reading of what a stage's result must give (its output)"):** met. `says`, `gives_nothing`, `formulated_nothing` and `sent_back` are at `supervise_outputs.py:29-56`.
- **Module map, `scripts/supervise*.py` (rounds):** met. `route` and `sent_back` are at `supervise_rounds.py:55-80`.
- **Module map, `tests/scenarios/` (one `<capability>_*_steps.py` module a concern):** met. The Given is at `supervision_formulate_steps.py:21-25`, and the Thens are at `supervision_reintegrate_steps.py:76-110`.
- **Module docstring:** `supervision_reintegrate_steps.py:1` still names "r140-r143" while the module now holds r149-r153 (w214's review, finding 2). Observation: the check is `grep -n r140 tests/scenarios` returning nothing.
- **Unreached code:** vulture is clean, and every new step is used by a scenario.

## Coupling

- **pytest-bdd:** unchanged from branch review 1. Only the public `given`, `when`, `then` and `scenarios` are used. The `PytestRemovedIn10Warning`s come from pytest-bdd's compat layer, so a pytest 10 upgrade ahead of pytest-bdd would break collection. Pinning `pytest<10` would make it stable. Pre-existing.
- **The fields `unheld_answers` and `nothing_formulated`:** contracts internal to this plugin, between agents/initiative-round.md and supervise_outputs.py. No outside project is relied on.

## Observations

- **Ruff red on the rounds' helper scripts:** `python3 <Scripts>/tools check --base 8f90ad3e` gives 10 errors under `.shop/work/i42/runs/supervision/` (finding 2).
- **Weak r152 Then:** read `supervision_reintegrate_steps.py:90-94`. It passes with no move logged (finding 4).
- **The partial apply's route to integrate is unscenarioed:** read `supervise_outputs.py:53-56` with `supervise_rounds.py:59`. `grep -n unheld_answers features/` shows only spec-integration's r46 (finding 5).
- **The apply contract does not say `unheld_answers` sends the proposal back:** read `agents/initiative-round.md:36` against `:37` (finding 6).
- **`UNHELD_ANSWERS` is unguarded:** read `supervise_brief.py:80-82` against the `ANSWER_LINES` guard (finding 8).
- **`unheld_answers: [""]` sends the proposal back:** `isinstance(unheld, list) and bool(unheld)` at `supervise_outputs.py:55` checks no element. A string `unheld_answers` is ignored. Both by reading; no line names either.
- **`nothing_formulated` beside committed scenarios:** the scenarios are merged and the proposal still goes to integrate (`supervise_rounds.py:173`). This is plan §5's open case.
- **README:173 still cites "supervision r140-r148":** r140 is retired, and r149-r153 are not in the release notes (w214's report, Other).
- **Plain pytest is red (pre-existing, i39's w212):** run `python3 -m pytest -q`. It gives 11 failed in tests/scenarios/test_requests.py.
- **@r117 is still deprecated though r121 is green (pre-existing, i39):** it is shown by `features deprecated`.
