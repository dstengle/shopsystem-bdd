# review of w214 (supervision r149-r153)

**Verdict: DONE.** No Critical finding, none triaged fix now. Three Minor findings, each an observation.

## Commits reviewed

- 2b4cbe78 "supervision r149-r153: a proposal whose round gave answers its lines do not hold goes back to integration".
  It is the only commit after `13faa004 work: w214 ready -> claimed`. The brief's `Commits:` gives the same one, and so does the implementer's result.json.
- Suite from the brief's record: 1020 passed, 0 failed at 2b4cbe78. The expected failures are w212's parked requests scenarios, none of them w214's.

## Removed and weakened tests

None. What I searched for:
- `git diff 2b4cbe78^ 2b4cbe78 -- tests/scenarios/test_*.py` is empty, so no binding was removed or changed.
- Both step modules only gain lines: one Given and five Thens. No assertion was removed or loosened, and no skip or xfail was added.
- `features/supervision.feature` loses one scenario: the `@r140 @deprecated` scenario "an apply round that applies nothing because ... (deprecated)". The work-item's Retires lists it. `test_supervision.py` is unchanged because it had no binding. The live `@r150` scenario still pins r140's behaviour.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commits agree.

## Cannot verify

- The report's red run (3 failed on r149, r152 and r153 before any code) cannot be checked from the commits. I only checked that these scenarios are green now.
- r150 widened to `unheld_answers` beside `changes`, and the approved-status route (plan decisions 2 and 3): no scenario drives either path. I verified both by reading `supervise_outputs.sent_back` and `Rounds.route` only.

## Findings

1. **Minor, observation.** `tests/scenarios/supervision_reintegrate_steps.py:90-94` (`awaiting_when_formulate_ended`) is weak.
   - What is wrong: `assert not moved or moved[-1]["after"] == "awaiting-answer"` passes when p1 has no logged move at all. The file check only rules out `status: formulated`.
   - Why it matters: a formulate branch that moved p1 to some other status, say `approved`, would pass this Then. The r152 scenario's other Then ("no transition of p1 ... between the start of the formulate round ... and the start of the integrate round") does catch that case, so nothing goes wrong today.
   - Fix: assert `status: awaiting-answer` in p1.md's frontmatter at the formulate round's end, or assert the commit at that point.
2. **Minor, observation.** `tests/scenarios/supervision_reintegrate_steps.py:1`: the module docstring still names "r140-r143". The plan (§2) says it names r149-r153 and not r140.
   - Fix: update the docstring.
3. **Minor, observation.** `scripts/supervise_brief.py:26`: `UPSTREAM = re.compile` became `UPSTREAM =re.compile`. No line asks for this whitespace edit.
   - Why it matters: it is noise in the diff, and it does not change behaviour.
   - Fix: restore the space.

### Hardening (observations, no line names them)

These were all checked by reading the code, not by running it.
- **`nothing_formulated` with committed scenarios.** A formulate result can give `nothing_formulated` after the round has committed scenarios. Those commits are merged, and the proposal still goes to integrate. `formulated_nothing` does not look at scenarios. The plan lists this case as open.
- **`unheld_answers` beside `questions`.** The apply round's questions are asked. Once they are answered, `route` sends the proposal to integrate, not back to apply, because `sent_back` ignores questions on the `unheld_answers` path (`supervise_outputs.py:55`). This follows r150, and the plan lists it as open.
- **`unheld_answers` given as a string, not a list.** It is ignored, so it does not send the proposal back.

### Risks checked

- **A route loop.** The risk: `sent_back` skips integrate stages, so it would judge an old apply round again after a successful integrate round. I verified that `route` calls it only for `awaiting-answer` and `approved`. A successful integrate round leaves the proposal `drafted` (r142), and the gate round that follows is then the latest stage. No loop.
- **r141 after a formulate round.** I verified that the integrate brief for a proposal (`supervise_brief.py:58-66`) still gives the ledger and the earlier drafts in the new path.
- **r83 and r131/r132.** I verified that the `formulated_nothing` short-circuit runs only when the result gives the field and no question. Otherwise the existing formulate branch, with its missing-scenario question, runs unchanged.

## Commands run

- `git log --stat -1 2b4cbe78`; `git show 2b4cbe78 -- scripts agents tests features`; `git log --oneline -3 2b4cbe78`
- `grep -n ... spec/capabilities/supervision.md`; `sed -n` on supervise_brief.py and supervise_rounds.py
- `python3 <Scripts>/tools check --base 8f90ad3e`:
  - **ruff:** 12 errors, none introduced by 2b4cbe78. The run's own `.shop/work/i42/runs/supervision/{5-apply,6-formulate}/*.py` give 10. `supervision_reintegrate_steps.py:13` (unused `git`) and `:174` (`re.M`) give 2, and both lines are already in 13faa004's version.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `python3 <Scripts>/tools size --limit 300`: printed nothing. supervise_rounds.py has 265 lines and supervise_outputs.py 103.
- `git diff 2b4cbe78^ 2b4cbe78 --stat -- tests/scenarios/test_*.py`: empty.
- `grep -rn r140 scripts tests features/supervision.feature`: only the docstring in finding 2.
- `python3 -m pytest -q tests/scenarios/test_supervision.py tests/scenarios/test_spec_integration.py -k "r149 or r150 or r151 or r152 or r153 or r46 or nothing or hold"`: 5 passed.
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "formulat or apply"`: 5 passed.
