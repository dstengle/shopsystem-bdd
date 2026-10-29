# Gate, round 2: q21 (i55)

Drafts: `.shop/scratch/13-integrate/drafts/round-2/spec/capabilities/{requests,supervision,work-queue}.md`. Every line below comes from the person's answers (delegation of 2026-10-27, answers of 2026-10-29), which the round-1 drafts did not hold.

## requests (retired gains r14)

Removed:
- [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.

Added:
- [r64] **When** `work list` is run, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names. (answer: "Retire r14 and add r59 as worded")

## supervision (retired gains r149, r32, r9, r105)

Removed:
- [r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. (its duplicate, applied from round 1, stays)
- [r32] **When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall exit with an error, printing each work-item's status and each open question.
- [r9] **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status.
- [r105] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.

Added:
- [r212] **When** no node of the initiative can make a transition, every work-item is `green` or `withdrawn`, no capability-proposal is `awaiting-answer` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status. (answer: "retire r32 and r9 and add r187 as worded")
- [r213] **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose every capability-proposal is `formulated` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. (answer: "retire supervision r105 for r188")

## work-queue (retired gains r23)

Removed:
- [r23] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.

Added:
- [r59] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. (answer: "retire work-queue r23 for r48")

Implementation line "r23: a request names the initiative..." becomes "r59: ..." (no Behaviour change).

## Glossary

No entry added, changed or removed.

## Decisions

None.

## Questions

None.
