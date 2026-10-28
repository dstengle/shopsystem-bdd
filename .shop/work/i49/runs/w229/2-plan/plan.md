# plan of w229: supervision#r180

## 1. What goes green

- supervision#r180, scenario "a started initiative fulfilling a request, with neither a capability-proposal, a glossary-proposal nor a work-item, is given to an integrate round with the accepted lines of the request" (features/supervision.feature:1414).
  - It is not red today. The researcher ran `pytest --work-item w229`: 182 passed, the r180 scenario among them. `Rounds.due` in scripts/supervise_rounds.py already gives the integrate round only to a started initiative with no capability-proposal, no glossary-proposal and no work-item. r180 only adds the glossary-proposal clause, which the code already has.
  - The implementer runs the scenario first. If it is red, the implementer stops and reports it, because the notes do not expect that.
- Retired scenarios: none. The work-item has no Retires section. The @r93 @deprecated scenario (feature:1406) stays as it is and still passes under r180.

## 2. Where the change lands

- scripts/supervise_rounds.py: comments only. The module docstring adds the glossary-proposal clause to "a started initiative with neither proposal nor work-item". The comment on `Rounds.due` that cites the retired r93 cites r180 instead. No change in behaviour.

This is the researcher's file set, unchanged. The step modules and test_supervision.py stay as they are (see decision 1).

## 3. Decisions

1. **The r180 Given is left as it is (reading A of the notes), not made to write a glossary-proposal (reading B).** The Given in `proposed_fulfilling` writes neither a capability-proposal, a glossary-proposal nor a work-item. That is exactly the state r180 describes, so the scenario pins r180 as written. The other side, where a started initiative that has a glossary-proposal gets no integrate round, is already tested: the r161 done scenario's Given (supervision_done_steps.py:28) holds an approved glossary-proposal g1 and expects no round. Reading B would also go against the scenario's own Given, which says the initiative has no glossary-proposal. This rests on supervision#r180. It does not change anything the narrator sees.
2. **The comment in `Rounds.due` cites r180, not r93.** r93 is retired (in `retired:` in spec/capabilities/supervision.md), and r180 is the requirement now in force for this branch. This rests on supervision#r180.

## 4. Tests the decisions break

None. Neither decision changes behaviour; both are comment-only changes. The notes list no test that expects an integrate round for a started initiative holding a glossary-proposal (found by search, since there is no coverage map). The @r93 scenario and the r161 done scenario both pass under r180 without changes. The implementer confirms this by running the full suite after the comment change. The size limit is not at risk: the file only gets comment edits, and no tracked file is over 300 lines.

## 5. Open cases

- A started initiative that has a glossary-proposal that is not approved (drafted or formulated), and no capability-proposal or work-item. r180 gives it no integrate round. No scenario covers the case where the glossary-proposal is not approved; the implementer names this, does not decide it.
- A started initiative that does not fulfil any request. r180 is silent here, and no scenario covers it.
