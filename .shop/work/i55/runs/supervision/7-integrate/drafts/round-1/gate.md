# Gate, round 1: q21 (i55), integrate round 7

Drafts: `.shop/scratch/7-integrate/drafts/round-1/spec/capabilities/supervision.md`

## supervision (retired gains r149, r32, r9)

Removed:
- [r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. (answer: retire r149, keep r186)
- [r32] **When** no work-item can make a transition and a work-item is `awaiting-answer`, `work run` shall exit with an error, printing each work-item's status and each open question. (answer: retire r32 and r9; r184 covers it)
- [r9] **When** no work-item can make a transition, every work-item is `green` or `withdrawn` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status. (replaced by r212)

Added:
- [r212] **When** no node of the initiative can make a transition, every work-item is `green` or `withdrawn`, no capability-proposal is `awaiting-answer` and no request whose asker is this context is in the asker's turn, `work run` shall exit successfully, printing each work-item's status. (answer: the line the person's delegate called r187; r187 is taken in spec, so r212 above r211)

Unchanged by answer: r184, r81, r132, r131, r185, r186, r152, r153; no Implementation line; no planner file-set line.

## Glossary

No entry added, changed or removed.

## Decisions

None.

## Questions

None.
