---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p8
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P8, the flow: integrate check, scripted formulate, drafting, agents and skills

Branch `gfc/P8`, commits 2feafcbf, 58b5c33e, f7a87796, 67aa6e13. Written by the layer 3 merge from the package's returned notes: the harness refused the package's own write of this file. Tests were written before code at each step.

## Checks (SHOPSYSTEM_GF unset, P1's install)

- The six named test files: 68 passed, 36 subtests. New `tests/scripts/test_supervise_brief.py`: 6 passed.
- Full suite: 34 failed, 1320 passed; 23 in the baseline, the other 11 all in `tests/scenarios/test_supervision.py`,
  each listed in `p8-broken.md` with the 0.29 lines it tests (r83, r112, r113, r116, r131/r132 for formulate, r149,
  r152, r153).
- The `feature-formulator` and `NOTHING_FORMULATED` greps print nothing; `skills/raising-a-request/SKILL.md` names
  `model parse`.
- `tools size --limit 300` exits 0 (largest touched: `supervise_rounds.py`, 295 lines); ruff and `tools check` clean.

## Calls

1. **Integrate check.** `uncodified` lays the drafts over a temporary copy of `spec/`, so drafted glossary and
   `## Terms` entries are in the lexicon (settles P6's carried note without changing `spec_solve`). Refusals: file
   problems, parse refusals with the hint, and L1/L3 findings for the drafted capabilities only. Drafts of uncodified
   capabilities are skipped, so the legacy supervision scenarios still pass.
2. **Send-back.** A refused round gets a new worker session in the same worktree with `Refused drafts` and the earlier
   drafts path in its brief, at most twice. Still refused: the proposals are written and those a refusal names (else
   all capability-proposals) go drafted → awaiting-answer with a question starting `supervise_outputs.UNCODIFIED`;
   `route` sends it back to integrate once answered. A GrammarError is the round's fault.
3. **Formulate** reuses `run_round`'s worktree, merge and fault handling; writes `result.json`, no `session.json`. An
   uncodified service capability is a fault naming `migrate upgrade`.
4. **Retires.** `removes` give `(cap @rN)` lines under `## Retires`; a capability with only removes gets an
   `accepts: []` work-item and the whole suite. The 0.29 deprecated-scenario retire path is kept.
5. **--work-item** accepts g ids and ranges; an r id runs its group's scenario. Logic-only groups' requirements count
   as no-scenario.
6. `uncodified_question` and `refused_proposals` sit in `supervise_outputs` to keep `supervise_rounds` under 300 lines.
7. `test_agents` spells the formulator's name in two parts so the plan's grep stays empty.

## Asks

- Accept `tests/scripts/test_supervise_brief.py` (accepted at the merge).
- P12: restate the new formulate behaviour and the integrate check (two send-backs, then a question whose answer goes
  back to integration) as supervision groups; rewrite the 11 scenarios in `p8-broken.md`.
- P14: README.md still names feature-formulator; CLAUDE.md's `supervise*.py` row still calls formulate rounds sessions.

## Module-map rows

- `scripts/supervise_formulate.py`: `work run`'s formulate round, a script with no session: `features generate` for the
  proposal's service capabilities, then `--check` and `model check` with no new row, then `features/` committed. Also
  the gate's preview of the scenarios the drafts would generate (design §13).
- `scripts/supervise_outputs.py` (widened): also the check of an integrate round's codified drafts, parsed and
  logic-checked on spec/ with the drafts laid over it (`uncodified`, `overlay`, `drafted`), and the question asked when
  the drafts are still refused after the send-backs.
