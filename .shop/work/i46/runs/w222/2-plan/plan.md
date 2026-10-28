# w222 plan: supervision r171, r172

## 1. What goes green

- **supervision#r171**, scenario "an integrate round that ends with a change list naming the glossary gives a drafted glossary-proposal with the terms it adds, changes and removes in the glossary" (features/supervision.feature:1516). Red today (notes §1): its first Given ("spec/index.md's Glossary holds the terms ...") is undefined, and so are its change-list Given for the glossary and both Thens. With the steps defined it would still fail: `Changes.write_proposals` skips every glossary entry, so no glossary-proposal is written or committed.
- **supervision#r172**, scenario "a glossary-proposal awaiting-answer with a question from its gate round that has no answer is given to no apply round" (features/supervision.feature:1800). Red today (notes §1): its Given about "i1's glossary-proposal g1 is awaiting-answer ..." and its Then "no round of the kind apply was started for g1" are undefined. No production code starts an apply round for a glossary-proposal, so once the steps exist the Then holds.
- Retires: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/supervise_change.py`: `write_proposals` also writes one `drafted` glossary-proposal from the change list's glossary entries and returns its path with the others, so it goes into the integrate round's commit. Update the module docstring. This file has room for about 170 more lines.
- `scripts/supervise_rounds.py`: the r93 condition in `Rounds.due` counts a glossary-proposal as an output of the initiative (Decision D3). The integrate branch of `run_round` already joins what `write_proposals` returns into the commit, so it needs no change unless the writer's signature changes. Update the docstring. This file has only 35 lines of room: keep the change to a few lines. A helper that lists the initiative's glossary-proposals may go in `scripts/supervise_glossary.py`.
- `scripts/supervise_glossary.py`: optional home for a small helper, either "does the initiative have a glossary-proposal" or the writer itself if `supervise_change.py` would grow too much. It already reads glossary-proposals, and it has room for about 270 more lines.
- `tests/scenarios/supervision_integrate_steps.py`: add the Given for spec/index.md's Glossary terms, the Given for the integrate round's change list that adds, changes and removes terms "in the glossary" (a glossary entry carrying `term/<term>` ids), and the two Thens on the commit that wrote i1's glossary-proposal (exactly one, drafted, with the three lists, and "reader" in none of them). This file has room for about 100 more lines.
- `tests/scenarios/supervision_proposal_steps.py`: add the Given for an initiative's glossary-proposal at a status with its `## Questions` and `## Answers`, and the Then that no apply round was started for g1. You may reuse the `rounds` helper of supervision_rounds_steps. This file has room for about 150 more lines.
- `CLAUDE.md`: in the module-map row for `scripts/supervise_change.py`, add the glossary-proposal to what it writes, because the module's concern grows.
- `tests/scenarios/test_supervision.py` is not in the set: both scenario bindings already exist (notes §4).

## 3. Decisions

- **D1. The writer writes the glossary-proposal from the glossary entry, beside the capability-proposals.** It is one file in the initiative's directory with `kind: glossary-proposal`, `part_of` the initiative, `status: drafted`, `adds`/`changes`/`removes` holding the entry's ids exactly as the round gave them, a date, and the sentence giving the path of the round's kept drafts. It has no `argues`. Several glossary entries in one change list merge into one proposal, ids in the order first named, as capability entries merge today. It rests on supervision#r171 ("a drafted glossary-proposal") and design-decision/the-glossary-is-a-target-of-spec-work (0073: "`work run` writes a glossary-proposal for that entry"). The drafts sentence is there for supervision#r170, which gives the gate and apply rounds that path. The fields are the ones `supervise_glossary.withheld` already reads (kind, status, the three lists).
- **D2. Its file name is `glossary.md` in the initiative directory, and its id is `glossary-proposal/<prefix>/<initiative>-glossary`.** This mirrors a capability-proposal named after the capability it argues. It rests on 0073: the glossary is a target "beside the capabilities".
- **D3. A started initiative whose only output is a glossary-proposal is not given another integrate round (notes reading R1b).** The r93 test in `Rounds.due` becomes: started, and none of capability-proposal, glossary-proposal or work-item. It rests on:
  - design-decision 0073: "an initiative that changes only the glossary is delivered with no capability-proposal";
  - supervision#r93's pin: an initiative "whose integration left nothing behind";
  - supervision#r171 together with r111. Under the literal reading (R1a), r171's own scenario would start integrate rounds without end, each writing a glossary-proposal, and could not give "wrote one".

  The r161 scenario (glossary-only initiative set done) has the same shape.
- **D4. The term ids inside a capability's entry pass through as today (notes reading R2-A).** The capability-proposal writer is not changed. Decision 0073 tells the integrate round to give terms in the glossary entry and "in no capability's", and the round's brief CHANGE_LIST already says so. Filtering terms out of a capability entry is not required by r159, r171 or r172. The deprecated r92 scenario keeps passing.
- **D5. r172 is met by absence; this item builds no apply route for glossary-proposals (notes R3).** The apply round for a glossary-proposal is supervision#r165, which this item does not accept. `Rounds.proposals` and the routing in `due` stay limited to capability-proposals. When r165 is built, its route must count the glossary-proposal's Answers against its Questions, as `due` does for capability-proposals; that is r165's work. It rests on the work-item's `accepts` (r171, r172 only) and supervision#r172.

## 4. Tests the decisions break

None. I checked:
- D1 and D2 only add a file. `tests/scenarios/supervision_integrate_steps.py` `proposals_written` (l.140-155, deprecated r92 scenario) lists the `.md` files added under `.shop/work/i1/` outside runs. Its change list has no glossary entry, so no `glossary.md` is written and its expected list still holds.
- D4 leaves `term/ledger` in thing's adds, so l.150 holds.
- D3 changes `due` only for an initiative with a glossary-proposal. The notes found no step that puts a glossary-proposal under a started initiative, and `spec_integration_apply_steps.py` (`withheld`, l.68-111) writes glossary-proposals under initiatives that are not given to `due`'s r93 path. Implementer: confirm that no `work run` scenario there has a started initiative with neither capability-proposal nor work-item. Per the notes it does not.
- `spec_integration_steps.py:85-126` reads the kept change list's glossary entry, which the writer does not alter.

The new Given for an awaiting-answer glossary-proposal also binds the r165 and r166 scenarios. Those are not accepted here and stay red at their Thens (no apply route), as unaccepted scenarios are expected to be.

## 5. Open cases

- A later integrate round (for example r141's re-integration of a capability-proposal) whose change list again names the glossary while the initiative already has a glossary-proposal: rewrite it in place, merge into it, or write a second one. No scenario covers this.
- A change list naming the glossary with all three lists empty.
- A capability actually named `glossary` (its proposal's file name would collide with D2's).
- Term ids given in a short form (`term/ledger`) or the full form of 0073 (`term/<context path>/<term>`): the writer copies them as given. The new Then should match the form its Given wrote.
- A glossary entry from a round that also names an unknown capability (r107): whether the glossary-proposal is still written along with the known capabilities' proposals before the error.
