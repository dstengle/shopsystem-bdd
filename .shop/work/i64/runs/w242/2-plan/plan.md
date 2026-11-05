# Plan of w242: supervision#r221@0.29

Planned from `.shop/work/i64/runs/w242/1-research/notes.md`, with reads of `scripts/supervise_rounds.py` (due, route, sent_back, run_round), `scripts/supervise_glossary.py`, `scripts/supervise_outputs.py` (gives_nothing, sent_back), `scripts/supervise_change.py` (write_proposals) and the step lines the notes name. This was needed to take decisions 1 to 4 below.

## 1. What goes green

- **supervision#r221@0.29**: an apply round whose result gives an answer the drafts it applied do not hold for a glossary-proposal is followed by a new integrate round for that glossary-proposal.
  - Scenario `features/supervision.feature:2072`, "an apply round that gives an answer the drafts it applied do not hold for a glossary-proposal is followed by a new integrate round for the glossary-proposal".
  - Red today (notes §1, run): `StepDefinitionNotFoundError` on the first Given (line 2074). The answers pattern in `tests/scenarios/supervision_proposal_steps.py:142-143` refuses the comma inside the quoted answer. The next Given ("the apply round for g1 applies nothing …", `supervision_reintegrate_steps.py:30-31`) and the Then (`:69-70`) match `p1` only. In the code, `due`'s glossary loop and `supervise_glossary.route` never send a glossary-proposal back to integration. After a glossary apply's `nothing_applied`, the commit keeps the proposal `awaiting-answer`, so `due` would pick the same apply again (the notes infer this from reading).
- Deprecated scenarios retired: none. The work-item has no `Retires` section and no `## Rulings`.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: in `due`'s glossary loop, a glossary-proposal at `awaiting-answer` or `approved` whose latest round sends it back (the existing `sent_back` method) gets the round `integrate`, with `drafted` as the status after. This is checked before `supervise_glossary.route`. The file is at 275 lines with 25 lines of room, so the addition stays small.
- `scripts/supervise_glossary.py`: the docstring of `route`, or a small helper, says that being sent back is checked by the caller. `ROUTES` keeps no route for `approved` that is not sent back (r167). If the implementer puts the whole check in `supervise_rounds.py`, this file may end up unchanged. It stays in the set because it is the glossary routing's home and has room (91 lines).
- `tests/scenarios/supervision_proposal_steps.py`: in the answers pattern of the "glossary-proposal g1 is awaiting-answer, its ## Questions section with …" Given, each quoted answer or question may hold a comma. Lines 1841, 1849, 1857 and 1866 must keep matching.
- `tests/scenarios/supervision_reintegrate_steps.py`: the "apply round … applies nothing" Given and the "integrate was started … after the apply round had ended" Then take `p1` or `g1`. The Then counts the integrate rounds of the named proposal, not only of `p1`.

Removed from the researcher's set: `scripts/supervise_change.py`. The r221 scenario's integrate round is made by "every other round ends" (`supervision_integrate_steps.py:33-35`), which gives DONE with no change list. The round is therefore refused by r96 before `write_proposals` is reached. The reading A / reading B conflict in the notes is about what an integrate round started for g1 writes when it does give a change list. r171 and r189 settle that, and scenario 1183 pins it. Scenario 1183's step "a round of the kind integrate is started for g1, redrafts the term …" has no step definition today (searched `tests/`), so it belongs to r189's own work-item, not to this one (see §5).

## 3. Decisions

1. **A glossary-proposal is sent back by the same test as a capability-proposal.** It is sent back when its latest round, failed integrate rounds aside, is an apply round whose result gives `nothing_applied` or a non-empty `unheld_answers`. This reuses `supervise_outputs.sent_back` through the existing `sent_back` method on the glossary-proposal's runs directory. Rests on: supervision#r221@0.29, which uses the same wording as r150, and r147 (`nothing_applied` is the round's output).
2. **The integrate round for a sent-back glossary-proposal is due from `awaiting-answer`, after a `nothing_applied` apply that kept the status, and from `approved`, after an apply that applied drafts and also gave `unheld_answers`.** Rests on supervision#r221@0.29, together with r166 (an apply that applied its drafts moves the proposal to `approved` first).
3. **The glossary apply that gives `nothing_applied` keeps its current behaviour.** It commits with the status kept and returns (`run_round` :177-180). The loop the notes feared does not happen, because `due` now routes the proposal to integrate before the apply route. Rests on r147 and r221.
4. **The integrate round for a glossary-proposal keeps the proposal's status until it ends, and a refused round keeps it.** This is the existing `run_round` path for any name that is not the initiative. A failed integrate round leaves the proposal in `left`, and `sent_back` skips failed integrate stages, so no second integrate round starts in the same run. Rests on r96, r86 and r115 (other nodes still run before the error exit), applied as the code already applies them to every proposal.
5. **The `sent_back` check comes before `route` in the glossary loop, so it wins over the r165 apply route.** Rests on supervision#r221@0.29. Without this ordering the apply would repeat.

None of these changes what the narrator observes beyond what r221 states. No question is raised.

## 4. Tests the decisions break

None. Checked:
- The glossary apply scenarios at `features/supervision.feature` 1839, 1847, 1855 and 1864 give DONE with changes or answers and no `nothing_applied` or `unheld_answers`, so `sent_back` is false for them and their route is unchanged (notes §3, and a read of `sent_back`).
- Scenarios 1367 and 1384 (g1 awaiting-answer with no answer) never reach an apply, and have no runs directory for `sent_back` to read.
- The capability apply/integrate scenarios (1068-1567, `p1`) keep their step texts. Widening the two reintegrate steps to `[pg]1` keeps matching them.
- The answers pattern change has to keep matching lines 1841, 1849 ("… only"), 1857 and 1866. The implementer runs those scenarios after the change.

## 5. Open cases

- The integrate brief for a glossary-proposal (`supervise_brief.py:61-68`) is built as for a capability-proposal: initiative lines, ledger, earlier drafts path if g1 names one. The scenario's g1 names no drafts path and i1 may fulfil no request. If the brief cannot be built for g1, the implementer names it (it would be a file outside the set).
- What an integrate round started for g1 writes when it gives a glossary change list: g1 rewritten in place with its lists merged (reading A), or a second `glossary.md` beside it (reading B). r171 and r189 (scenario 1183) govern this; it is not exercised by r221's scenario. It is left to r189's work-item.
- Whether g1 is set `drafted` after an integrate round that gives a change list. `due` passes `drafted` as the status after, and that is the `move` `run_round` makes. No glossary counterpart of r142 states it. This is not exercised here.
- A glossary apply that gives both questions and `unheld_answers`: which wins. The scenarios are silent on this.
- The run exits with an error after the scenario's integrate round (r96, no change list). The Then only reads the log, so the exit code is not asserted.
