# Plan of w225: a glossary-proposal's gate and apply rounds, and an initiative done on the glossary alone

Work-item `.shop/work/i46/w225.md`, under supervision, accepts r161 r164 r165 r166 r167 r169 r170. No `## Retires`, no `## Rulings`.
Planned from `.shop/work/i46/runs/w225/1-research/notes.md`. I read only `supervise_glossary.py`, `supervise_done.py`,
`workqueue_done.py`, the top of `supervise_rounds.py`, `workqueue.move`, `pull_through` in `supervise.py` and the r55 steps,
to take decisions 1, 6 and 7 below.

## 1. What goes green

All of them are red today on missing step definitions (research run: 8 failed under `--work-item w225`). Behind the
missing steps, `Rounds.due`/`Rounds.proposals` route only `kind: capability-proposal`, so no glossary-proposal ever gets a round.

- **supervision#r164**: "a drafted glossary-proposal is given to a gate round asked only for the questions on the terms it adds, changes or removes". Missing Given for a drafted g1 with adds/changes/removes. No gate round is routed, and the gate brief has no wording for a glossary-proposal.
- **supervision#r170**: "the <kind> round of a glossary-proposal is given the path of the kept drafts…" (gate row, apply row). Both Givens are missing: the plain drafted one, and the awaiting-answer one, because the regex at `supervision_proposal_steps.py:133` (`[^,]+`) does not match the row's comma phrasing. The drafts-path code in `supervise_brief.py` (l.89-93) exists, but no round reaches it.
- **supervision#r169**: "when the gate round `work run` started for a glossary-proposal ends, the proposal is awaiting-answer". Missing Given. The step "the gate round gives the question … on g1" exists only for p1 (`supervision_rounds_steps.py:61`). The move is never reached.
- **supervision#r165**: "a glossary-proposal whose every question from its gate round has an answer is given to an apply round with its answers". The Then "a round of the kind apply was started for g1, given the answers …" is missing (`supervision_rounds_steps.py:238` is p1 only). No apply is routed.
- **supervision#r166**: "when the apply round … ends having applied its drafts, the proposal is approved". The Given "the apply round for g1 applies g1's drafts and gives DONE with a change list that adds the term "ledger" in the glossary" is missing. In code, `workqueue.move` refuses `approved` for a non-capability-proposal (l.155), `Changes.rewrite_lists` would empty g1's lists, and `supervise_glossary.withheld` withholds g1's own terms from its apply brief.
- **supervision#r167**: "when the apply round … ends having applied its drafts, no formulate round is started for the proposal". Same missing Given as r166. Once g1 is routed, `AFTER` must not send an approved glossary-proposal to formulate.
- **supervision#r161**: "an initiative that changes only the glossary, its glossary-proposal approved and its terms committed to spec/index.md, is set done". Two Givens are missing: the glossary-only initiative, and a one-term Glossary committed on the branch (`supervision_integrate_steps.py:49` takes three terms). In code, `set_done` needs committed measurement and analysis records, and is reached only after a branch review of green work-items.
- r172 (not accepted here, passes today) must stay green once glossary-proposals are routed.

Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/supervise_glossary.py`: the glossary-proposals of an initiative with their statuses, the routing of one through gate → awaiting-answer → apply → approved and no further (decision 1), `withheld` that leaves out the proposal being applied (decision 2), and the glossary-only done condition (decision 6). It has room (27 lines), and `supervise_rounds.py` has only 31 lines of room.
- `scripts/supervise_rounds.py`: `due` also offers a glossary-proposal's round, using the routing in `supervise_glossary`. The apply branch of `run_round` does not call `rewrite_lists` for a glossary-proposal (decision 4). Keep the additions to a few lines.
- `scripts/supervise_brief.py`: the gate brief of a glossary-proposal asks only for the questions on the terms it adds, changes or removes (r164). The apply brief's withheld line passes the proposal being applied (decision 2).
- `scripts/supervise_change.py`: only if the guard for decision 4 sits better in `rewrite_lists` (an implementer's choice of place).
- `scripts/workqueue.py`: in `move`, a glossary-proposal also accepts the proposal statuses, so `approved` is no longer refused (decision 3). This is a one-line change; the file has 6 lines of room.
- `scripts/supervise_done.py`: the glossary-only done, set and committed as in r109, without measurement or analysis (decision 6).
- `scripts/supervise.py`: `pull_through` calls the glossary-only done when the initiative has no work-item. One or two lines; the file has 7 lines of room.
- `tests/scenarios/supervision_proposal_steps.py`: the Givens for a drafted g1 (plain, and with adds/changes/removes), and a regex for the awaiting-answer Given wide enough for the r170, r165 and r166 phrasing.
- `tests/scenarios/supervision_rounds_steps.py`: "the gate round gives the question … on g1" and "a round of the kind apply was started for g1, given the answers …". Widening the p1 steps to any proposal name is preferable to adding lines (27 lines of room).
- `tests/scenarios/supervision_formulate_steps.py`: "the apply round for g1 applies g1's drafts and gives DONE with a change list that adds the term … in the glossary".
- `tests/scenarios/supervision_done_steps.py`: the glossary-only initiative Given.
- `tests/scenarios/supervision_integrate_steps.py`: the Glossary Given with one term, committed on the initiative branch.

Removed from the researcher's set:
- `scripts/workqueue_done.py`: `_holds` is work-queue r23's condition, shared with `work withdraw` and `work resolve`. Changing it would change what those commands observe. r161 is supervision's, so its condition goes in `supervise_glossary`/`supervise_done` (decision 6).
- `scripts/workqueue_answer.py`: `work answer` on a glossary-proposal is in no accepted scenario and belongs to work-queue.

## 3. Decisions

1. **Routing.** A glossary-proposal is routed like a capability-proposal as far as approval: `drafted` gets a gate round and then `awaiting-answer` (r164, r169). `awaiting-answer` with as many answers as questions gets an apply round given the answers, and then `approved` (r165, r166). `approved` gets no further round (r167). With an unanswered question it gets no apply (r172). These rounds go through the same `run_round`, serial lock (r95) and fault handling as a capability-proposal's. The send-back routes of r149/r150 and the formulate route of r116 name the capability-proposal and are not applied to it. Rests on supervision#r164, r165, r166, r167, r169, r172 and design-decision/the-glossary-is-a-target-of-spec-work.
2. **r55 vs r165/r166 (the researcher's question), taken here and not asked.** The apply round of a glossary-proposal is not withheld its own terms. It still withholds the terms of every other glossary-proposal that is not `approved`. Reading B (withhold for all) would make r166 impossible: no apply could ever bring a term in, and a glossary-only initiative could never be done (r161). Design-decision/the-glossary-is-a-target-of-spec-work says the glossary-proposal's "terms the gate approves before they are applied". In r165 the person's answers to every gate question are that approval, given to the apply round of that proposal. So r55's "while the person has not approved" holds, and the person observes nothing beyond what r165 and r166 already state. Rests on supervision#r165, r166, spec-integration#r55, design-decision/the-glossary-is-a-target-of-spec-work.
3. **`workqueue.move` takes the proposal statuses for a glossary-proposal**, as it does for a capability-proposal. Rests on supervision#r166.
4. **An applied glossary-proposal keeps the lists it was drafted with.** `work run` writes only its status. r145 (writing `adds`/`changes`/`removes` from the applied change list) names the capability-proposal only. r166 asks only for the transition. Rests on supervision#r145, r166.
5. **The gate brief of a glossary-proposal** names the `term/<term>` ids of its adds, changes and removes, and asks for questions on those terms and on no other term or line, worded as r168's capability gate is. Rests on supervision#r164.
6. **Glossary-only done.** "Changes only the glossary" means the initiative has at least one glossary-proposal and has no capability-proposal and no work-item. The condition for done:
   - every glossary-proposal of the initiative is `approved`;
   - in `spec/index.md` as committed at HEAD, every term a proposal adds or changes is a Glossary bullet (`- **<term>**:`) and no term it removes is;
   - `spec/index.md` has no uncommitted change.

   When it holds, `work run` sets the initiative `done` and commits it on the initiative branch (r109). It does so without a branch review, a measurement or an analysis (r97 already forbids the measurement with no work-item), and without `workqueue_done.holds`. Rests on supervision#r161, r109, r97 and design-decision/the-glossary-is-a-target-of-spec-work (a term is a Glossary bullet).
7. **Placement for size.** The new logic goes in `supervise_glossary.py`. `supervise_rounds.py`, `supervise.py` and `workqueue.py` get only call sites, so each stays at or under 300 lines (CLAUDE.md size limit).

## 4. Tests the decisions break

None. What I checked:
- `tests/scenarios/spec_integration_apply_steps.py` (spec-integration r55 scenario, l.59-98): g1 there is `drafted`, and the round applied is a capability-proposal's, so under decision 2 g1's terms are still withheld and the scenario stays green.
- Decision 3: the notes found no test (by search) asserting that a glossary-proposal is refused `approved`.
- Decision 4 only touches the glossary-proposal branch, so the r145 scenarios on capability-proposals are untouched.
- Decision 6 leaves `workqueue_done` and r105's path as they are, so the r105, r106 and r109 scenarios are untouched.
- r172 stays green under decision 1.

There is no coverage map (`tools map` was not run), so these lists come from search. The implementer runs the whole suite.

## 5. Open cases

- A gate round for a glossary-proposal that gives no question: r117's approval question names the capability-proposal only, so 0 answers ≥ 0 questions would send g1 straight to apply.
- An apply round of a glossary-proposal giving unheld answers (r46): r150/r151 name the capability-proposal.
- Answers that drop a drafted term, so g1's kept lists (decision 4) name a term the apply did not add, and the done condition (decision 6) never holds.
- A glossary-only initiative with a request it raised that is not `delivered`: r105 holds such an initiative back, r161 does not say.
- Whether `work run`'s printed node list (`show`) gives glossary-proposals and their questions.
- A glossary-proposal's questions under a delegation (r162/r163, w223's work): `supervise_answers` is on the path.
