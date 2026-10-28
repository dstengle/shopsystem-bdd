# Plan of w219 (spec-integration r54, r55)

Accepts spec-integration#r54 and spec-integration#r55. The work-item has no Retires section and no Rulings.

## 1. What goes green

- **spec-integration#r54**, "a round of the kind integrate that drafts a change to the glossary gives the terms it adds, changes and removes in the change list's entry for the glossary and in no entry for a capability" (features/spec-integration.feature:39). It is red today because its first Given ("spec/index.md's glossary has the terms order and basket") has no step definition, and neither do the rest of its steps except the shared When (notes §1). The code also has no glossary entry: `work run` reads every change-list entry as a capability, would refuse a list whose only other entry is `glossary` as naming no known capability (supervise_rounds.py run_round, integrate branch), and the writer's contract says "one entry for each capability" (supervise_brief.py CHANGE_LIST, agents/initiative-round.md).
- **spec-integration#r55**, "while the person has not approved the terms of a glossary-proposal, no round applies any of them to spec/index.md" (features/spec-integration.feature:51). It is red today because its first Given ("spec/index.md's glossary has the term order and no term refund") has no step definition, and neither do the rest of its steps (notes §1). Nothing in scripts/ knows the kind glossary-proposal, and nothing tells an apply round to keep any term out of spec/index.md.
- Deprecated scenarios retired: none. The work-item retires nothing.

## 2. Where the change lands

- `scripts/supervise_change.py`: `entries` reads one glossary entry as well as capability entries (decision 1). `unknown` treats it as known without a capability file. `write_proposals` and `rewrite_lists` skip it, so it gives no capability-proposal and changes no capability-proposal's lists.
- `scripts/supervise_rounds.py`: the integrate branch's refusal of unknown capabilities, the apply branch's lists from applied entries, and `raise_before_merge`'s count of unknown entries all skip the glossary entry. The apply branch calls the new module to build the brief's withheld terms (decision 4). The file has 35 lines of room, so each edit here is a call, and the logic goes in the new module.
- `scripts/supervise_brief.py`: CHANGE_LIST names the glossary entry and says terms go there and in no capability's entry (decision 2). The apply brief carries the withheld-terms text the new module gives (decision 4).
- `scripts/supervise_glossary.py` (new): reads an initiative's glossary-proposals from `.shop/work/<initiative>/` (kind `glossary-proposal`, status, `adds`, `changes`, `removes` of `term/<term>` ids), says which of them are not approved, and gives the text that withholds their terms for an apply brief. This is a new concern, so it gets its own module (CLAUDE.md).
- `CLAUDE.md`: a module-map row for `scripts/supervise_glossary.py` (CLAUDE.md: a new concern gets a new module and a row).
- `agents/initiative-round.md`: the integrate kind's change-list form gains the glossary entry, terms in it only. The apply kind applies none of the terms its brief withholds to spec/index.md.
- `agents/capability-writer.md`: the researcher did not read it. If it says one entry per capability or puts `term/` ids in a capability's lists, it gets the same glossary-entry wording. If it does not, it stays as it is.
- `tests/scenarios/spec_integration_steps.py`: the r54 steps. A stand-in integrate round whose result gives a capability entry for refunds and a glossary entry. The Thens read the brief `work run` gave the round and the result it kept.
- `tests/scenarios/spec_integration_apply_steps.py`: the r55 steps. A glossary-proposal file of i1 that is not approved, an approved capability-proposal with kept drafts, and a spec/index.md under those drafts that holds refund and a changed order. The When reuses `run_integrate`. The Thens read spec/index.md and the apply brief.

Removed from the researcher's set: `tests/scenarios/supervision_integrate_steps.py`, `tests/scenarios/supervision_proposal_steps.py` and `features/supervision.feature`. Decision 3 leaves them as they are (see §4).

## 3. Decisions

1. **The glossary entry's form.** A change list holds at most one entry for the glossary. It is marked as the glossary's by a field of its own, not by a capability name, so that no capability can be mistaken for it. Its `adds`, `changes` and `removes` hold `term/<term>` ids only. Rests on spec-integration#r54 and design-decision/the-glossary-is-a-target-of-spec-work (0073: "an entry for the glossary and in no capability's").
2. **What the writer is told.** The change-list text in the integrate brief (CHANGE_LIST) and in agents/initiative-round.md says that every added, changed and removed term goes in the glossary entry, and that a capability's entry holds only that capability's requirement ids. The r54 Thens assert this text in the brief `work run` gave the round, as well as the entries of the result it kept, following the r46 steps that read both brief and result. Rests on spec-integration#r54.
3. **`work run` neither refuses nor strips a `term/` id in a capability's entry.** r54 binds the round. No requirement tells `work run` to refuse, and a refusal would change what the person sees, so the reading stays as it is. A glossary entry gives no capability-proposal here: writing a `drafted` glossary-proposal for it is supervision#r158, which this work-item does not accept. Rests on spec-integration#r54, and on supervision#r158 being outside `accepts:`.
   This settles the researcher's two questions without asking the person. The scenarios at features/supervision.feature:1475-1482 and :1696-1705 are `@deprecated`, for the retired supervision r92 and r104. Under decision 3 they pass as they do today. Removing them is the work of their replacements, supervision r159 and r168, not of w219. Decision 0073 has already rejected reading (b) for new behaviour ("Alternatives: a term change riding with a capability-proposal … rejected by the person's ruling").
4. **How r55 is held.** When `work run` starts an apply round for a capability-proposal, it reads the initiative's glossary-proposals. The brief names, as withheld, every term of each one whose status is not `approved` (drafted, awaiting-answer, withdrawn), and says that none of them is applied to spec/index.md, even where the kept drafts hold them. The apply goes on as before for the capability-proposal's own drafts. Rests on spec-integration#r55, with "not approved" read as "status other than approved", and on 0073 ("approved at the gate before they are applied to spec/index.md").
   `work run` does not check spec/index.md after the round. r55 binds the round and no requirement gives `work run` a refusal here (see §5).
5. **The r55 Thens.** "the round applies the capability-proposal's drafts" reads as the r46 step "the round applies those drafts" does: one apply round, and the proposal no longer awaiting-answer. "spec/index.md's glossary has no term refund" and "… has the term order as it was before the round" compare spec/index.md after the run with its text before the run. Alongside these, the brief is asserted to withhold refund and order, so that the scenario is red until the brief carries it. Rests on spec-integration#r55.

## 4. Tests the decisions break

None. What I verified:
- tests/scenarios/supervision_integrate_steps.py `proposals_written` (:140-153) and the step `entry` (:32-38) serve the `@deprecated` @r92 scenario at features/supervision.feature:1475. Decision 3 keeps term ids in a capability entry as `work run` reads them today, so its expectation that thing's adds are thing#r4 and term/ledger still holds. It is not rewritten.
- tests/scenarios/supervision_proposal_steps.py `drafted_with` (:99-107) and `gate_names_its_ids` (:140-146) serve the `@deprecated` @r104 scenario at :1696. The gate brief's listing of a proposal's adds is not touched. They are not rewritten.
- tests/scripts/test_supervise_change.py (:16, :34, :52) pass capability entries only (notes §3). Skipping a glossary entry leaves them as they are.
- The notes found no test that asserts the CHANGE_LIST text (by search), so decision 2's rewording breaks none.

The implementer runs the supervision scenarios on r91, r92 and r107 and test_supervise_change.py after the change, because the notes found these by search and did not run them.

## 5. Open cases

- A change list with two glossary entries, or a glossary entry with an id that is not a `term/` id. The scenarios are silent.
- An apply round that applies a withheld term anyway. The scenarios are silent on what `work run` does then (decision 4 adds no check).
- An apply round for a glossary-proposal itself (supervision r165, r166), and which glossary-proposals it withholds then. That is outside this work-item, and its scenarios are silent.
- `model check` does not know the part kind glossary-proposal (scripts/model_work.py PART_KINDS). If `work run` runs `model check` on the r55 scenario's repository and reports the new file, the implementer names it. Adding the kind is design-model-check's work.
- An apply round's own result giving a glossary entry in `changes`. The apply branch skips it for the proposal's lists (§2), and nothing else is said.
