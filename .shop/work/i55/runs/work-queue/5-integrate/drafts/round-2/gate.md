# Gate: work-queue, integrate round 2

## work-queue
- Removed [r23] (retired): **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.
- Added [r59]: **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. (answer of 2026-10-29, reading (a); numbered r59 as ids up to work-queue#r58 are drafted elsewhere)
- Implementation line "r23: a request names the initiative..." now names r59.
- [r47] unchanged (answer 2, reading (a)).

## supervision
- Removed [r105] (retired): **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
- Added [r213]: **When** `work run` finds an initiative that is not `done`, that has at least one work-item that is `green`, whose every work-item is `green` or `withdrawn`, whose every capability-proposal is `formulated` or `withdrawn`, whose kept branch review lists nothing to fix now, whose measurement and analysis record `work run` has committed and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. (answer of 2026-10-29; numbered r213 as supervision#r212 is drafted elsewhere)

Glossary: none. Decisions: none. Questions: none.
Note: the supervision draft here replaces only r105; supervision#r212 and the removals of r149, r32, r9 are drafted in the supervision proposal's own drafts.
