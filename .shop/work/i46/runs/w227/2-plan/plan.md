# Plan of w227: fix the findings of branch review 2 of i46

Sources: the work-item `.shop/work/i46/w227.md` (no Retires, no Rulings), its `findings:` file `.shop/work/i46/runs/branch-review/2/findings.md`, the research notes `.shop/work/i46/runs/w227/1-research/notes.md`, `spec/capabilities/supervision.md`, the answers on `.shop/work/i46/w225.md` and the requests q30 and q36.

This plan stops at one question (decision D1). It is written as far as it goes.

## 1. What goes green

None of the accepted scenarios is red today. The research ran `pytest --work-item w227`: 189 passed, 1 skipped, nothing failed. All seven pass. They are the same seven that w225 made green:

- supervision#r161: the glossary-only initiative set `done` (`features/supervision.feature:1809`).
- supervision#r164: the gate of a drafted glossary-proposal, asking only on its terms (`:1705`).
- supervision#r165: the apply round once every gate question has an answer (`:1751`).
- supervision#r166: the proposal `approved` after its apply round (`:1767`).
- supervision#r167: no formulate round after a glossary apply (`:1776`).
- supervision#r169: the proposal `awaiting-answer` when its gate round ends (`:1742`).
- supervision#r170: the gate and apply rounds given the kept drafts (`:1727`, both Examples rows).

The work-item exists for the one fix-now finding of branch review 2, F1. Through w225's routing, `work run` writes r117's approval question on a glossary-proposal whose gate round gives no question. r117 names only a capability-proposal. The work-item retires no deprecated scenario.

## 2. Where the change lands

The file set depends on D1.

- **Reading A** (keep the approval question until q36 line 1 is integrated): no file changes in w227. Its seven scenarios are already green, and the fix belongs to an integrate round of q36, not to an implementer. `work run` reads an empty file set as a missing output (the w208 and w220 precedent). So under A, w227 is withdrawn or held behind q36's integration, not implemented.
- **Reading B** (limit r117 to capability-proposals):
  - `scripts/supervise_rounds.py`: the r117 branch of `run_round`'s gate case (near line 159) is taken only for a capability-proposal. The file has 26 lines of room under the size limit.
  - `scripts/supervise_glossary.py`: `route` gives a route to an `awaiting-answer` glossary-proposal whose gate gave no question, so that the r165 apply round is started for it (decision D2).
  - `CLAUDE.md`: the `scripts/supervise_glossary.py` row names the routing and the glossary-only done (finding F6). This is added because the module's concern widens again under B.

Left out of either set, though the research's set has it: `scripts/supervise_done.py`. Its abandoned guard and request check in `set_glossary_done` are branch-review observations, not fix-now. No line asks for either (r161 is silent), so building them would add behaviour the narrator sees with no requirement behind it. See section 5.

## 3. Decisions

- **D1, the open question: what a glossary-proposal's gate round with no question leaves for the person.**
  - r117 asks for the approval question for a capability-proposal only.
  - r169 says the glossary-proposal becomes `awaiting-answer` when its gate ends.
  - r165 starts the apply round when every gate question has an answer, which is vacuously true when there is none.
  - Against that, the coordinator's answer on w225 under the person's delegation (2026-10-28) kept the question, "which keeps glossary changes with the person as q30 rules". q30 line 4 says "the gate shall approve the terms of a proposal for the glossary before they are applied". It raised q36 line 1, still `open`, to write that into a line.
  - The branch review then triaged the same behaviour as fix now.
  - No requirement of the capability, no design-decision and no ruling of w227 settles which one stands. The two readings differ in what the narrator sees (section 5 of the result). So D1 is a question, not a decision of this plan.
- **D2, only under reading B: a zero-question glossary gate is routed to r165's apply round.** The proposal is `awaiting-answer` (r169) and has no unanswered gate question. So r165's condition holds and r172's hold does not apply. The gate round already transitions to `awaiting-answer`, so r130's "next transition" is that one; this plan reads nothing more from it. Rests on supervision#r165, #r169 and #r172.
- **D3: `scripts/supervise_done.py` is not changed.** Rests on supervision#r161, which names neither abandoned initiatives nor requests, and on the findings, which mark both as observations, not fix-now.

## 4. Tests the decisions break

- Under reading A: none, because nothing changes.
- Under reading B: none found.
  - The research searched `tests/` and `features/` by text, since there is no map. It searched for the approval-question text ("approved as drafted", "lines as drafted").
  - The r117 step (`tests/scenarios/supervision_rounds_steps.py:79`) and its scenario (`features/supervision.feature:1828`) assert the capability case only, so they stay green.
  - The r165 scenario gives an answered question, so it does not reach D2's new route and stays green.
- D3 changes nothing, so it breaks nothing.

## 5. Open cases

- Under B, no scenario drives a glossary gate with no question. Neither the removal of the approval question nor D2's route would be seen red first. The implementer names whether that case waits for a line (a widened r117, or a new line through integration) or is left unproven.
- If any wording of r117's approval question remains for a glossary-proposal elsewhere (a brief, a log line), the implementer names it.
- From the branch review, outside w227 (not chosen here):
  - an `abandoned` glossary-only initiative run by name is set `done` (`supervise_done.py:31`);
  - a glossary-only initiative with an undelivered raised request is set `done` (r105 checks requests, r161 does not);
  - F2 (r93 against `due`) stays with q35;
  - F3 (`glossary.md` overwritten whole), F4 and F5 are observations for later work.
