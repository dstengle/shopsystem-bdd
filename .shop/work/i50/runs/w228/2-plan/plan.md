# Plan of w228 (supervision#r173)

## 1. What goes green

- **supervision#r173**: scenario "when the gate round `work run` started for a glossary-proposal ends with no question, one question asking the person to approve the terms it adds, changes and removes is written" (`features/supervision.feature:1838`).
  - Red today (notes §1): its last Then, `one question was written for g1, asking the person to approve the terms "ledger", "shelf" and "loan"`, has no step definition (`StepDefinitionNotFoundError`). Were it defined it would still fail: `run_round` in `scripts/supervise_rounds.py` (lines 158-161) writes the capability wording "Are the lines of g1 approved as drafted?" for every gate that gives no question, and that names no term.
  - Its Givens and the first Then are defined already: `glossary_drafted` (`supervision_proposal_steps.py:169`, which writes adds `term/ledger`, changes `term/shelf`, removes `term/loan`), the no-question gate result (`supervision_rounds_steps.py:66`), and the gate round started for g1 (`supervision_rounds_steps.py:97`).
- No deprecated scenarios: the work-item has no Retires section.

## 2. Where the change lands

- `scripts/supervise_glossary.py`: a new helper that builds the approval question for a glossary-proposal from its front matter's `adds`, `changes` and `removes` (ids `term/<term>`, read the way `withheld` reads them), naming each term by its bare name.
- `scripts/supervise_rounds.py`: in `run_round`'s no-question default for a gate, call that helper for a glossary-proposal; a capability-proposal keeps the current lines wording. The file has 274 lines and room for 26, so the branch stays a few lines and the wording stays in `supervise_glossary.py`.
- `tests/scenarios/supervision_proposal_steps.py`: the new Then for g1's question, beside the g1 gate-brief Then (`gate_g1_terms`). It reads `g1.md`'s `## Questions`, checks that it has exactly one bullet, and checks that this bullet asks for approval and names each quoted term. It reuses `terms_of`. The file has 195 lines, so there is room.

The researcher also listed `scripts/supervise.py`, `scripts/workqueue.py` and `scripts/supervise_brief.py` as on the path. Its notes say they do not change, so they are left out of the file set. `supervise.py` has only 5 lines of room, which is one more reason not to touch it.

## 3. Decisions

1. **The question is written as r117's is**: one bullet under the proposal's `## Questions`, through the existing `move`. The proposal then has the same status as after a capability gate with no question. Rests on supervision#r173 ("write one question"), with supervision#r117 as the existing form of a gate's no-question default, and on design-decision/the-glossary-is-a-target-of-spec-work (glossary-proposals go through the same gate-and-approve path).
2. **The proposal is told apart by its kind.** It is a glossary-proposal when its front matter's `kind` is `glossary-proposal`, the same test `supervise_glossary` already uses. Any other gate keeps the r117 wording unchanged. Rests on supervision#r117 and #r173, which are two branches of one default.
3. **The question names every term the proposal lists and what the proposal does with it.** It gives the bare term (`ledger`, not `term/ledger`) and says whether the proposal adds, changes or removes it. It asks the person to approve them. Rests on supervision#r173: it asks for approval of "the terms the proposal adds, changes and removes", and the person reads the question in the proposal file.

## 4. Tests the decisions break

None. Checked against the notes (§3): `questions_hold_approval` in `tests/scenarios/supervision_rounds_steps.py` and the r117 scenario (`features/supervision.feature:1828`) assert "approv", "p1" and "as drafted" for a capability-proposal, and decision 2 leaves that branch unchanged. A text search found no test that expects a glossary gate with no question to get the lines wording. The existing g1 steps (`gate_g1_terms`, `gate_g1_no_other`, `glossary_proposal_answered`) read the gate brief or set up an awaiting-answer g1, and none of them reads the no-question default.

## 5. Open cases

- A glossary-proposal with one or two of `adds`, `changes` or `removes` empty: the scenario fills all three. The implementer names how an empty list shows in the question (for example, left out).
- A glossary-proposal whose three lists are all empty: the scenario is silent on what the question says.
- The exact wording of the question beyond decision 3: the scenario checks only that it asks for approval and names the three terms.
- An id in the lists that is not in the form `term/<term>`: the scenario is silent on how it is shown.
