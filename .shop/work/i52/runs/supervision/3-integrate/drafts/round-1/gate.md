# Gate, round 1 (brief round 3), i52 (request q38)

## supervision

- [r171] CHANGED. Now: **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and the initiative has no glossary-proposal, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
  Was: **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary.
- [r188] ADDED. **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and the initiative has a glossary-proposal that is neither `approved` nor `withdrawn`, `work run` shall add to that glossary-proposal the terms the change list adds, changes and removes in the glossary, the round's entry replacing the entry of a term the proposal already lists, keeping the proposal's status, its questions and its answers. (q38 line 1; answers Q1, Q2 of 2026-10-28)
- [r189] ADDED. **When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and the initiative's glossary-proposal is `approved`, `work run` shall transition the glossary-proposal to `drafted` with the terms the change list adds, changes and removes in the glossary added to it, the round's entry replacing the entry of a term the proposal already lists, keeping its questions and its answers. (answers Q1, Q2 of 2026-10-28)
- [r190] ADDED. **While** a question of an initiative is left for the person and has no answer, `work run` shall start no further session under the delegation for that initiative's questions. (q38 line 2; answers Q3 to Q5)

## work-queue

- [r23] CHANGED. Now: **When** a `work` command other than `work withdraw` makes it true by its change that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
  Was: **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
- [r50] ADDED. **When** `work withdraw` leaves every work-item of an initiative `green` or `withdrawn`, `work` shall leave the initiative's status as it is, for `work run` to set once the initiative's kept branch review lists nothing to fix now. (q38 line 3)
- [r51] ADDED. **When** `work` sets an initiative's status, `work` shall append a line to `.shop/work/<initiative>/log.jsonl` with the initiative and its status before and after the transition. (q38 line 4)

## Glossary

No term added, changed or removed. No decision drafted.

## Questions

1. supervision r171, r188, r189: the initiative's only glossary-proposal is `withdrawn`; r171 now applies only when there is no glossary-proposal and r188 excludes `withdrawn`, so no line covers it. (a) A new `drafted` glossary-proposal is written: r171 reads "...and the initiative has no glossary-proposal, or only a `withdrawn` one, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary." Recommended. (b) The terms are added to no proposal: a new line "**If** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and the initiative's glossary-proposal is `withdrawn`, **then** `work run` shall exit with an error, naming the glossary-proposal."
