# Branch review of i42

**Verdict: DONE.** No Critical finding and nothing triaged fix now. Every check was run here and passed. The 11 suite failures are w212's parked scenarios (initiative i39), which this branch does not touch.

## Range reviewed

`8f90ad3e..733efe83` (Base `8f90ad3e`, "work: start i42, fulfilling q22", which adds `.shop/work/i42/initiative.md`), 32 commits.

- **w213** (spec-integration#r46, green): its commits run from `6de25e87 work: w213 ready -> claimed` to `53d57591 work: w213 claimed -> done`. Its one commit of its own is `5482e7e3` "spec-integration r46: an apply round gives each answer its drafts do not hold, in unheld_answers". That commit touches:
  - README.md
  - agents/initiative-round.md
  - scripts/supervise_brief.py (+4)
  - tests/scenarios/spec_integration_apply_steps.py (new, 78 lines)
  - tests/scenarios/test_spec_integration.py (+1)
- **Commits outside any work-item:**
  - `356ac0f4` "spec-integration: add r46": the apply round of the i42-spec-integration proposal, spec/ alone.
  - `6c1dca8d` "spec-integration: formulate r46": its formulate round, features/spec-integration.feature +11.
  - Every other commit is a `work …` commit of `work run`.
  - See finding 1.
- **The i42-supervision proposal** (r149-r153, removing r140) is awaiting-answer (gate round 4). It has no work-item yet, so nothing of it is in this branch's code.

## Suite

Suite: 1016 passed, 11 failed at 733efe83 in 30.65 s (also 1 skipped, 56 subtests passed).

- **Command:** `python3 -m pytest -q -p no:cacheprovider`. The time is pytest's own wall time.
- **Parallel:** yes. pytest.ini has `addopts = -n auto` (32 workers here).
- **In-process:** no. The step definitions drive `work run` as a subprocess (`subprocess.run([sys.executable, SCRIPTS/"work", "run", "i1"])`, tests/scenarios/spec_integration_steps.py:114). The suite is under 60 s, so that is no finding.
- **The 11 failures:** all are in tests/scenarios/test_requests.py, each a `StepDefinitionNotFoundError`. They are the scenarios of i39's w212, awaiting-answer and parked: requests between repositories, deferred to GitHub issues.
  - Plain pytest does not mark them xfail; only `--whole-suite` does (r43, r122).
  - The i39 ledger already records this ("plain pytest is red on w212's 11 parked scenarios").
  - Nothing in this branch touches requests.
  - None of the failures is of spec-integration or supervision. The r46 scenario passes inside the suite.

## Checks

- **w213's check:** the work-item names no check beyond its scenario (r46). The scenario passed in the suite run above. I did not run `--work-item w213` apart, because the suite run answers it.
- **`tools check --base 8f90ad3e…`:**
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: "the project states no import contracts" (no contracts to check; nothing missing)
- **`tools size --limit 300`:** no output, so no file is over the limit. Touched Python files: supervise_brief.py 207 lines, spec_integration_apply_steps.py 78, test_spec_integration.py 9.
- **`features deprecated`:** 11 deprecated scenarios, all "for: removal":
  - design-model-check: @r117
  - supervision: @r3, @r5, @r16, @r112, @r113
  - work-queue: @r3, @r11, @r16, @r17, @r18

  None was added or removed by this branch. Of these, @r117's replacement r121 is green: the i39 ledger records "@r117 scenario not yet removed though r121 is green". It is named here and goes under Observations. It is not this branch's.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** the system has no dry-run mode of an operation of its own. The two `--dry-run` uses (supervise_review.py:53, supervise_faults.py:71) are `git push --dry-run`, a reachability probe passed to git. They are not a mode of one of the system's operations. No randomized test is called for, and the branch touches neither.

## Removed and weakened tests

None. What I searched `git diff 8f90ad3e HEAD -- tests features` for:
- deleted `def` / step functions;
- dropped parametrize cases or Examples rows;
- removed or loosened `assert` lines;
- added skip / xfail;
- changed step text.

What the diff holds:
- one new module;
- one added `import *` in test_spec_integration.py;
- one added scenario (the formulate round's).

Nothing was deleted (0 deletions under tests/ and features/). w213's plan lists "Tests the decisions break: None", which agrees.

## Allowances

w213's report gives "## Tests changed under an allowance: none". There is no row to verify, and no test was changed.

## Cannot verify

- **Whether a real `initiative-round` compares the answers with the applied drafts correctly.** This is not a check any work-item names. In the scenario, a stand-in plays the round, and it is given `unheld_answers: [SHIPS]` by the plan itself (tests/scenarios/spec_integration_apply_steps.py:34-35). Of the scenario's Thens:
  - the ones that read the kept result (:71-78) prove only that `work run` keeps the field;
  - the brief assertion (:73) proves that `work run` asks for it.

  This follows design-decision/workflow-capabilities-are-guarantees (0065): spec-integration is a guarantees capability, checked by `measure` on real batches. The implementer and w213's review both name this.

## Findings

1. **Minor, w213's initiative (no work-item): commits `356ac0f4` and `6c1dca8d`. Triage: drop.**
   - **What is wrong:** these two commits belong to no work-item. `6c1dca8d` changes `features/spec-integration.feature` (+11, the @r46 scenario).
   - **Why it matters:** it does not, here. They are the apply and formulate rounds `work run` starts for i42-spec-integration. Design-decision/the-context-runs-without-a-coordinator (0068) makes those rounds the only writers of `spec/` and of feature files. The change under `features/` is an addition by the formulate round, not by a work-item, so it is not the Critical case.
   - **Fix:** none.
2. **Minor, w213: tests/scenarios/spec_integration_apply_steps.py:71-78. Triage: observation.**
   - **What is wrong:** the Then "the round's result does not give the answer that the customer sees the status of an order" holds by construction, since the stand-in's planned result never gives it.
   - **Why it matters:** the only part of r46 that code verifies is the brief instruction (:73). This is the stand-in practice of r44/r45 (see Cannot verify).
   - **Fix:** none now.
   - **Reproduction:** read :30-36 against :76-78.
3. **Minor, w213: scripts/supervise_brief.py:79. Triage: observation.**
   - **What is wrong:** `UNHELD_ANSWERS` ("Compare each answer below …") is added to every apply brief, including one for a proposal without `## Answers`.
   - **Why it matters:** no line names that case, and the round would give an empty list.
   - **Fix, if wanted:** guard it with `if self.answer_lines(name):`, as `ANSWER_LINES` is guarded at :63.
   - **Reproduction:** read :77-79 against :63.
4. **Minor, w213: README.md:173 and agents/initiative-round.md:36. Triage: observation.**
   - **What is wrong:** today `work run` gives `unheld_answers` no reader, so a partial apply with unheld answers still goes approved and then to formulate (r144-r146). The answer is kept only in the stage directory's result.json, which is committed under `.shop/work/i42/runs/`.
   - **Why it matters:** this is no contradiction, because r46 asks only that the result gives the answers. Plan decision 2 leaves the reader to a supervision line. That line is drafted: supervision r150 and r151, in the i42-supervision proposal at gate round 4. Until it lands, an unheld answer reaches no one unless the result is read.
   - **Fix:** deliver r150 and r151. Their reader should key on the field name `unheld_answers` that the contract and the brief now fix.

Code no line asks for: none. The one production change is the brief instruction, and it serves r46. The README and agent-contract edits are its documentation and prompt text. `work run` gains no new observable behaviour beyond the brief line.

Behaviour against lines and Purpose:
- **No contradiction found.**
- **`gives_nothing`:** risk checked: a whole-round `nothing_applied` with `unheld_answers` beside it could stop counting as nothing applied (r140, r147). `gives_nothing` (scripts/supervise_rounds.py:24-28) reads only `nothing_applied`, `questions` and `changes`, so the route is unchanged.
- **The kept result:** risk checked: `work run` might keep a result other than the round's. It reads and keeps the stage's whole result.json (scripts/supervise_worker.py:201-210), so the field reaches the kept result as the contract says.
- **Purpose:** no session writes spec. The spec and feature changes came through the apply and formulate rounds.

## Shape

- **CLAUDE.md, size limit:** met. Every touched file is ≤ 300 lines; the largest is supervise_brief.py at 207.
- **Module map, `scripts/supervise*.py` ("briefs, …"):** met. The brief instruction sits in scripts/supervise_brief.py:20-22 and :79, beside `CHANGE_LIST` and `ANSWER_LINES`.
- **Module map, `tests/scenarios/` ("one `<capability>_*_steps.py` module a concern"):** met. spec_integration_apply_steps.py is the apply-round concern of spec-integration, bound from test_spec_integration.py:5.
- **"A new concern gets a new module and a row here":** there is no new concern in scripts/, so no row is needed. The new test module falls under the existing `tests/scenarios/` row.
- **w213's fileset:** it names tests/scenarios/spec_integration_steps.py. The work changed spec_integration_apply_steps.py (new) and test_spec_integration.py instead, as plan §2 and the report's Budget provide for, so it is no finding.
- **Unreached code:** vulture is clean. Every step of the new module is used by the @r46 scenario. `formulate_did_its_work` and `rounds` are imported from supervision_rounds_steps.py and used (:37, :52).

## Coupling

- **pytest-bdd:** the new module uses only its public `given`, `when`, `then` and `scenarios`, so it is stable.
  - The suite prints `PytestRemovedIn10Warning`s from pytest-bdd's compat layer (`_register_fixture` with nodeid), plus "Unknown pytest.mark.deprecated".
  - These are in pytest-bdd's internals against pytest, not in this repository's code. A pytest 10 upgrade before pytest-bdd follows would break collection.
  - Pinning pytest < 10 alongside pytest-bdd, or registering the `deprecated` marker, would make this stable. It is not this branch's.
- **The field `unheld_answers`:** the new contract is internal. It is shared between agents/initiative-round.md:36 and supervise_brief.py:20-22, and is to be read by supervision r150. No outside project is relied on.

## Observations

- **Unguarded `UNHELD_ANSWERS`:** see finding 3 for the reproduction (supervise_brief.py:77-79 against :63).
- **Stand-in Then holds by construction:** see finding 2 for the reproduction (spec_integration_apply_steps.py:30-36 against :76-78).
- **No reader of `unheld_answers` yet:** see finding 4. To reproduce, `grep -rn unheld_answers scripts/` shows supervise_brief.py only.
- **Plain pytest is red (pre-existing, i39's w212):** run `python3 -m pytest -q`. It gives 11 failed, all `StepDefinitionNotFoundError` in tests/scenarios/test_requests.py.
- **Deprecated @r117 not retired though r121 is green (pre-existing, i39):** `features deprecated` lists "features/design-model-check.feature: an id of a kind kept in .shop/work/ with another context's path is v18 (deprecated)".
- **pytest 10 deprecation warnings from pytest-bdd (pre-existing):** the suite's warnings summary shows 263 + 3 `PytestRemovedIn10Warning`.
