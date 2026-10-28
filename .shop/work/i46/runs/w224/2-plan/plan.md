# Plan of w224 (supervision r159, r168)

## 1. What goes green

- **supervision#r159**: "an integrate round that ends with a change list gives one drafted capability-proposal for each capability it names, with the requirement ids it adds, changes and removes on that capability" (features/supervision.feature, `@r159`). It is red today on an undefined Then (`StepDefinitionNotFoundError`). The only step near it, `proposals_written` in tests/scenarios/supervision_integrate_steps.py, matches only the text of the deprecated r92 scenario, which has the clause `and the term "ledger"`. The accepted Then has no such clause. The Givens and the When already run.
- **supervision#r168**: "the gate round of a capability-proposal is asked only for the questions on the lines that proposal adds, changes or removes" (`@r168`). It is also red on an undefined Then. `gate_names_its_ids` in tests/scenarios/supervision_proposal_steps.py matches only the deprecated r104 Then, which ends `and the term "ledger"`.
- From the notes, by reading: production already behaves as both requirements say. `supervise_change.write_proposals` writes one proposal per capability and leaves glossary entries out. The gate brief in `supervise_brief` lists only the proposal's own adds, changes and removes.
- Retired: none. The work-item has no Retires section. The deprecated r92 and r104 scenarios stay until the retiring work-item r123 drafts.

## 2. Where the change lands

- tests/scenarios/supervision_integrate_steps.py: the Then for the proposals written also matches the accepted r159 text, without the term clause. When there is no term, it expects thing's lists to hold only the ids.
- tests/scenarios/supervision_proposal_steps.py: the Then for the gate brief also matches the accepted r168 text, without the term clause. When there is no term, it expects only thing#r4, thing#r2 and thing#r3.

This is the researcher's file set unchanged. No file in scripts/ changes: the notes read the behaviour as already there. If a scenario stays red once its step binds, the implementer reports it rather than widening the set silently.

## 3. Decisions

- **D1. Both forms of each Then stay bound.** The deprecated r92 and r104 scenarios must keep passing until the work-item r123 drafts retires them, so neither step is narrowed to the new text only (the researcher's reading B is rejected). Rests on supervision#r123, and on #r159 and #r168 for the new text.
- **D2. One step per Then, with the term clause optional, rather than a second step beside each.** Each existing Then regex takes `and the term "<word>"` as an optional group. Its expectation adds `term/<word>` only when the group is present. This matches what the Given `drafted_with` and the helper `entry` already do with the same optional clause, and it leaves one step to remove when r123 retires the deprecated scenarios. This is a test-structure choice only: the narrator sees nothing different. A step written beside each existing one (the researcher's reading A) would satisfy D1 just as well. The choice rests on no requirement; it follows the file's existing practice.
- **D3. No production change.** r159's split by capability and r168's gate brief limited to the proposal's lists are already in scripts/ (notes §1, §2). r171 puts glossary terms in a glossary-proposal, so a capability-proposal never carries a `term/` id from a change list. Rests on supervision#r159, #r168, #r171 and design-decision/the-glossary-is-a-target-of-spec-work.

## 4. Tests the decisions break

None. I checked that:
- D2 keeps the deprecated r92 Then (term present, expected adds `thing#r4`, `term/ledger`) and the deprecated r104 Then (term in the brief) matching and asserting as they do today.
- The Givens of both accepted scenarios already bind (the researcher's run passed them).
- Nothing else in tests/ or tests/scenarios/ uses these two step texts (notes §2: no other `term/` use in a capability-proposal).

## 5. Open cases

- Whether the r168 Then also asserts that the gate brief names no `term/` id when the scenario gives none. The scenario is silent on this. Its "asks only for" is already covered by the step that follows it (no question on thing#r1 or other#r1).
- Whether the r159 Then, with no term, also asserts that no glossary-proposal was written in that commit. The scenario only counts the two capability-proposals it names.
- With D2, the step's name and docstring now cover both forms. Wording them is left to the implementer.
