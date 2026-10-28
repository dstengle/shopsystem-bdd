# Review of w213 (spec-integration#r46)

**Verdict: DONE.** No Critical finding and nothing triaged fix now. Two Minor findings follow, both observations.

## Commits reviewed

- 5482e7e38fbabb8f96f07092f6d23d6b8757bd4f "spec-integration r46: an apply round gives each answer its drafts do not hold, in unheld_answers". This is the brief's `Commits:` line, and it is the one commit the implementer's result.json lists. They match.
- It touches README.md, agents/initiative-round.md, scripts/supervise_brief.py (+4), tests/scenarios/spec_integration_apply_steps.py (new, 78 lines) and tests/scenarios/test_spec_integration.py (+1 import).
- The suite result comes from the brief's record: 1016 passed, 0 failed at 5482e7e3. The expected failures are w212's parked requests scenarios. I did not run the suite.

## Removed and weakened tests

None. What I searched for in `git show 5482e7e3 -- tests/`:
- deleted `def test_`/step functions;
- parametrize cases dropped;
- `assert` lines removed or loosened;
- `skip`/`xfail` added;
- step text changed.

The only test changes are a new module and one added `import *` line in test_spec_integration.py. Nothing under `features/` changed.

## Allowances

The report's `## Tests changed under an allowance` is "none", so there is no row to verify.

## Cannot verify

- **Whether the real `initiative-round` compares answers with the applied drafts correctly.** In the scenario, a stand-in plays the round, and the plan supplies its `unheld_answers: [SHIPS]` itself (spec_integration_apply_steps.py:34-35). The two Thens that read the kept result (lines 71-78) therefore prove only two things:
  - `work run` tells the round (in its brief) to give `unheld_answers`;
  - `work run` keeps the result the round gives.

  The comparison itself lives in the prompt contract (agents/initiative-round.md:36), and no test exercises it. The implementer names this concern too.

## Findings

1. **Minor, observation**: tests/scenarios/spec_integration_apply_steps.py:71-78.
   - **What is wrong:** the Thens "the round's result gives / does not give the answer ..." assert on the stand-in's planned output, so they hold whatever the round would really do.
   - **Why it matters:** the only part of r46 that code verifies is the brief instruction checked at line 73. That fits how the r44/r45 steps already work (the stand-in practice), so it is not a defect of this work.
   - **Fix:** none now. A test of the agent contract would need a real round.
   - **Reproduction:** read lines 30-36 and 71-78. The `fields` the plan gives are the fields that are later asserted.

2. **Minor, observation**: scripts/supervise_brief.py:79.
   - **What is wrong:** `UNHELD_ANSWERS` ("Compare each answer below ...") is appended to every apply brief, including one for a proposal with no `## Answers`. In that case "below" refers to nothing.
   - **Why it matters:** no line names this case, and it does no harm, since the round would just give an empty list. The plan left it open ("Open cases") and the report names it.
   - **Fix:** if wanted, guard it with `if self.answer_lines(name):`.
   - **Reproduction:** read lines 77-79. The branch has no answers condition, unlike the `ANSWER_LINES` guard at line 63.

Risks I checked, no finding:
- **A whole-round `nothing_applied` result that also carries `unheld_answers` might stop counting as "nothing applied" (r140/r147).** `gives_nothing` (scripts/supervise_rounds.py:24-28) reads only `nothing_applied`, `questions` and `changes`, so the extra field does not change the route. Plan decision 2 holds.
- **The brief might say "answers below" when it gives no answers after the instruction.** `answer_lines` is appended after the stage lines (supervise_brief.py, `lines += self.answer_lines(name)`), and the Then at line 73 asserts `Answer: <SHIPS>` in the brief.
- **Code no Behaviour line asks for.** The one production change is the brief instruction, and it serves r46. The README and agent-contract edits are documentation and prompt text for r46. There is no new reader of `unheld_answers` in `work run` (plan decision 2), so the observable behaviour `work run` adds is only the brief line.
- **Purpose.** The capability says no session writes spec itself; nothing here writes spec. Nothing contradicts the Purpose or a Behaviour line.
- **File set.** The work-item lists tests/scenarios/spec_integration_steps.py. The implementer put the steps in a new spec_integration_apply_steps.py and bound it from test_spec_integration.py, as plan §2 provides for. The work-item's scripts/supervise_brief.py, agents/initiative-round.md and README.md were the files changed.

## Checks

- `tools check --base 8f90ad3e`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `tools size --limit 300`: no output, so no file is over the limit. Touched files: supervise_brief.py 207 lines, spec_integration_apply_steps.py 78 lines, test_spec_integration.py 9 lines.

## Commands run

- `git show --stat 5482e7e3`, `git show 5482e7e3`, `git show 5482e7e3 -- scripts/`, `git show 5482e7e3 -- tests/`
- `git log --format="%h %s" -3 8f90ad3e`
- `sed -n 20,32p scripts/supervise_rounds.py`; `sed -n 60,110p scripts/supervise_brief.py`
- `grep -n "r46\|^## \|Purpose" spec/capabilities/spec-integration.md`; `sed -n 20,40p features/spec-integration.feature`
- `python3 <Scripts>/tools check --base 8f90ad3e6acd9159e1317a8c264050c0e646a842`
- `python3 <Scripts>/tools size --limit 300`
- `wc -l` on the touched Python files
- `git status --short`: clean
